#!/usr/bin/env python
"""Render every .item of an HTML source page to a rounded, bordered WebP, once per theme.

    uvx --from playwright --with pillow python -I render.py <source.html> --out <dir>
        [--root <dir>] [--themes light,dark] [--items id1,id2] [--max-kb 300]

The page is served over HTTP from --root (default: the folder holding the page) so relative
references such as ../logo.png and shared.css resolve. It is opened as <page>?theme=<theme>,
and each .item is screenshotted. Output: <id>.webp for light, <id>-dark.webp for dark.

A browser is taken from the machine (Edge, then Chrome) so nothing has to be downloaded; pass
--browser chromium to use Playwright's own build after `playwright install chromium`.

The box check covers only the .item itself, not a card or node inside it, and skips anything inside an
element marked data-bleed (a shape that is meant to run off the edge). Look at every image.

Besides the images it prints the fonts and the page grounds it found, and a WARN (counted toward
exit 1) when a requested font did not load, so a fallback face is in the images, or when the
stylesheet still carries the starter's --starter-placeholder marker.
"""
import argparse
import functools
import http.server
import re
import sys
import tempfile
import threading
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw
from playwright.sync_api import sync_playwright

FALLBACK_BORDER = {"light": (191, 211, 227), "dark": (44, 74, 102)}


class QuietServer(http.server.ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        pass  # a browser closing a connection early is not an error here


def round_and_border(png, dst, line, radius=24, border=3, supersample=4):
    img = Image.open(png).convert("RGB")
    w, h = img.size

    def mask(inset, r):
        m = Image.new("L", (w * supersample, h * supersample), 0)
        ImageDraw.Draw(m).rounded_rectangle(
            (inset * supersample, inset * supersample,
             (w - inset) * supersample - 1, (h - inset) * supersample - 1),
            radius=r * supersample, fill=255)
        return m.resize((w, h), Image.LANCZOS)

    outer, inner = mask(0, radius), mask(border, radius - border)
    out = img.convert("RGBA")
    out.paste(Image.new("RGBA", (w, h), line + (255,)), (0, 0), ImageChops.subtract(outer, inner))
    out.putalpha(outer)
    out.save(dst, "WEBP", lossless=True, method=6)
    return w, h


def parse_color(value, fallback):
    value = (value or "").strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{6})", value)
    if m:
        h = m.group(1)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.fullmatch(r"#([0-9a-fA-F]{3})", value)
    if m:
        return tuple(int(c * 2, 16) for c in m.group(1))
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", value)
    if m:
        return tuple(int(x) for x in m.groups())
    return fallback


OVERFLOW_JS = """(item) => {
  const box = item.getBoundingClientRect(), bad = [];
  const name = (el) => el.id || (typeof el.className === 'string' ? el.className : el.getAttribute('class')) || el.tagName;
  for (const el of item.querySelectorAll('*')) {
    if (el.closest('[data-bleed]')) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (r.right > box.right + 1 || r.bottom > box.bottom + 1 || r.left < box.left - 1 || r.top < box.top - 1)
      bad.push(String(name(el)).slice(0, 40));
  }
  return bad.slice(0, 5);
}"""


FONT_JS = """() => {
  const generic = new Set(['serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'system-ui', 'ui-serif',
    'ui-sans-serif', 'ui-monospace', 'ui-rounded', 'emoji', 'math', 'fangsong']);
  const wanted = new Set();
  for (const el of document.querySelectorAll('.item, .item *, svg text, svg tspan')) {
    if (!Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    wanted.add(getComputedStyle(el).fontFamily.split(',')[0].trim().replace(/^["']|["']$/g, ''));
  }
  const probe = document.createElement('span');
  probe.textContent = 'mmmmmmmmmmlliWWW@#';
  probe.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap;font-size:72px';
  document.body.appendChild(probe);
  const width = (f) => { probe.style.fontFamily = f; return probe.getBoundingClientRect().width; };
  const used = [], missing = [], plain = [];
  for (const f of wanted) {
    if (generic.has(f.toLowerCase())) { plain.push(f); continue; }
    const q = '"' + f + '"';
    const here = width(q + ', monospace') !== width('monospace') || width(q + ', serif') !== width('serif');
    (here ? used : missing).push(f);
  }
  probe.remove();
  return { used, missing, plain };
}"""

PLACEHOLDER_JS = "() => getComputedStyle(document.documentElement).getPropertyValue('--starter-placeholder').trim()"


def launch(p, choice):
    order = [choice] if choice else ["msedge", "chrome", "chromium"]
    last = None
    for name in order:
        try:
            if name == "chromium":
                return p.chromium.launch()
            return p.chromium.launch(channel=name)
        except Exception as e:  # browser not installed: try the next one
            last = e
    sys.exit(f"render.py: no browser could be launched ({last}). Install Edge or Chrome, or run `playwright install chromium`.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", required=True)
    ap.add_argument("--root")
    ap.add_argument("--themes", default="light,dark")
    ap.add_argument("--items", default="all")
    ap.add_argument("--max-kb", type=int, default=300)
    ap.add_argument("--browser")
    ap.add_argument("--viewport-width", type=int, default=2600)
    a = ap.parse_args()

    source = Path(a.source).resolve()
    root = Path(a.root).resolve() if a.root else source.parent
    try:
        rel = source.relative_to(root).as_posix()
    except ValueError:
        sys.exit(f"render.py: {source} is not inside --root {root}. Pass a --root that contains the page and everything it links to.")
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    themes = [t for t in a.themes.split(",") if t]
    wanted = None if a.items == "all" else set(a.items.split(","))

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = functools.partial(Quiet, directory=str(root))
    server = QuietServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    port = server.server_address[1]

    problems = 0
    fonts_checked = False
    fonts_used, grounds = [], {}
    with sync_playwright() as p, tempfile.TemporaryDirectory() as tmp:
        browser = launch(p, a.browser)
        for theme in themes:
            page = browser.new_page(viewport={"width": a.viewport_width, "height": 1400})
            page.goto(f"http://127.0.0.1:{port}/{rel}?theme={theme}", wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(300)
            ids = page.eval_on_selector_all(".item", "els => els.map(e => e.id)")
            if not ids or any(not i for i in ids):
                sys.exit("render.py: every .item needs a unique id; it becomes the file name.")
            if not fonts_checked:
                fonts_checked = True
                info = page.evaluate(FONT_JS)
                fonts_used = info["used"] + info["plain"]
                if info["missing"]:
                    problems += 1
                    print(f"WARN fonts requested but not loaded, so a fallback face is in the images: {', '.join(info['missing'])}. "
                          "Render online, install the font, or load it from a font host.")
                if page.evaluate(PLACEHOLDER_JS):
                    problems += 1
                    print("WARN starter placeholder tokens are still in use: replace them with the repository's own "
                          "and delete --starter-placeholder from the stylesheet.")
            grounds[theme] = page.eval_on_selector(".item", "e => getComputedStyle(e).backgroundColor")
            for item_id in ids:
                if wanted is not None and item_id not in wanted:
                    continue
                el = page.locator(f"#{item_id}")
                clipped = el.evaluate(OVERFLOW_JS)
                if clipped:
                    problems += 1
                    print(f"WARN {item_id} ({theme}): content leaves the item box: {', '.join(clipped)}")
                line = parse_color(
                    el.evaluate("e => getComputedStyle(e).getPropertyValue('--cardline')"),
                    FALLBACK_BORDER.get(theme, FALLBACK_BORDER["light"]))
                raw = Path(tmp) / f"{item_id}-{theme}.png"
                el.screenshot(path=str(raw), scale="css")
                dst = out / (f"{item_id}.webp" if theme == "light" else f"{item_id}-{theme}.webp")
                w, h = round_and_border(raw, dst, line)
                kb = dst.stat().st_size / 1024
                flag = "" if kb <= a.max_kb else f"  WARN over {a.max_kb} KB"
                problems += bool(flag)
                print(f"{dst.name}  {w}x{h}  {kb:.0f} KB{flag}")
            page.close()
        browser.close()
    server.shutdown()
    print("fonts: " + (", ".join(fonts_used) if fonts_used else "none found"))
    print("grounds: " + ", ".join(f"{t} {c}" for t, c in grounds.items()))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
