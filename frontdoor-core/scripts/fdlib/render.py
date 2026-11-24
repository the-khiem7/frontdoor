"""Render every .item of an HTML source page to an image per theme, keeping one browser and one encoder pool for many jobs.

The engine behind `fd render`, used in three ways: once per command, kept open by `--watch`, and kept open by the daemon.
Capture happens in the browser one item at a time; finishing and encoding run in a process pool, because the WebP encode,
not the browser, is the slow step (about 1.5 s per 2400 px picture at method 4, 3.4 s at method 6).

How an item is finished is set on the item itself:

    (default)                  rounded corners and a border in its --cardline colour, lossless WebP
    data-finish="plain"        the rectangle as captured, no rounding and no border, lossless WebP
    data-finish="transparent"  the page and item ground left out, alpha kept, lossless WebP (icons, marks)
    data-social                a 640x320 GitHub social preview, saved as a still 1280x640 PNG with its extra checks
    data-radius / data-border  the corner radius and border width in output pixels for the default finish (24 and 3)
"""

import concurrent.futures
import functools
import http.server
import io
import os
import re
import sys
import threading
import time
from pathlib import Path

FALLBACK_BORDER = {"light": (191, 211, 227), "dark": (44, 74, 102)}
SOCIAL_MAX_BYTES = 1_000_000
DEFAULT_METHOD = 4

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

SAFE_JS = """(item) => {
  const box = item.getBoundingClientRect(), bad = [], m = 40;
  for (const el of item.querySelectorAll('*')) {
    if (el.closest('[data-bleed]')) continue;
    if (!Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    const r = el.getBoundingClientRect();
    if (r.left < box.left + m - 1 || r.top < box.top + m - 1 || r.right > box.right - m + 1 || r.bottom > box.bottom - m + 1)
      bad.push((el.id || el.tagName).slice(0, 40));
  }
  return bad.slice(0, 5);
}"""

TEXT_BLOCKS_JS = """(item) => Array.from(item.querySelectorAll('h1,h2,h3,h4,h5,h6,p,li,blockquote,figcaption,small'))
  .filter(el => !el.closest('[data-bleed]') && el.textContent.trim()).map(el => (el.id || el.tagName).slice(0, 40))"""

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

ITEMS_JS = """els => els.map(e => ({id: e.id, finish: e.dataset.finish || (e.hasAttribute('data-social') ? 'social' : 'card'),
  radius: e.dataset.radius || '', border: e.dataset.border || ''}))"""

# Make every ancestor of the item paint no ground, so a transparent item keeps its alpha; returns a function that restores it.
CLEAR_GROUND_JS = """(item) => {
  const saved = [];
  for (let el = item.parentElement; el; el = el.parentElement) { saved.push([el, el.style.background]); el.style.background = 'transparent'; }
  window.__fdRestore = () => { for (const [el, bg] of saved) el.style.background = bg; };
}"""


class QuietServer(http.server.ThreadingHTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        pass  # a browser closing a connection early is not an error here


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")  # an edited stylesheet must reach the next render of a long-lived browser
        super().end_headers()


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


# ---- worker side ----

@functools.lru_cache(maxsize=16)
def _masks(w, h, radius, border, supersample=4):
    from PIL import Image, ImageChops, ImageDraw

    def mask(inset, r):
        m = Image.new("L", (w * supersample, h * supersample), 0)
        ImageDraw.Draw(m).rounded_rectangle(
            (inset * supersample, inset * supersample, (w - inset) * supersample - 1, (h - inset) * supersample - 1),
            radius=r * supersample, fill=255)
        return m.resize((w, h), Image.LANCZOS)

    outer, inner = mask(0, radius), mask(border, max(0, radius - border))
    return outer, ImageChops.subtract(outer, inner)


def finish_and_save(png, dst, finish, line, radius, border, method):
    """Finish one captured item and write it. Runs in a worker process. Returns (width, height, bytes written)."""
    from PIL import Image

    img = Image.open(io.BytesIO(png))
    if finish == "social":
        img = img.convert("RGB")
        img.save(dst, "PNG", optimize=True)
    elif finish == "transparent":
        img.convert("RGBA").save(dst, "WEBP", lossless=True, method=method)
    elif finish == "plain":
        img.convert("RGB").save(dst, "WEBP", lossless=True, method=method)
    else:
        img = img.convert("RGB")
        w, h = img.size
        outer, ring = _masks(w, h, radius, border)
        out = img.convert("RGBA")
        out.paste(Image.new("RGBA", (w, h), tuple(line) + (255,)), (0, 0), ring)
        out.putalpha(outer)
        out.save(dst, "WEBP", lossless=True, method=method)
    return img.size[0], img.size[1], os.path.getsize(dst)


# ---- main side ----

def launch(playwright, choice=None):
    last = None
    for name in [choice] if choice else ["msedge", "chrome", "chromium"]:
        try:
            return playwright.chromium.launch() if name == "chromium" else playwright.chromium.launch(channel=name)
        except Exception as e:  # noqa: BLE001 - browser not installed: try the next one
            last = e
    raise RuntimeError(f"no browser could be launched ({last}). Install Edge or Chrome, or run `playwright install chromium`.")


def make_job(source, out, root=None, themes="light,dark", items="all", max_kb=300, method=DEFAULT_METHOD, viewport_width=2600):
    source = Path(source).resolve()
    root = Path(root).resolve() if root else source.parent
    try:
        page = source.relative_to(root).as_posix()
    except ValueError:
        raise ValueError(f"{source} is not inside --root {root}. Pass a --root that contains the page and everything it links to.") from None
    if not source.is_file():
        raise ValueError(f"the source page {source} does not exist.")
    if method not in range(7):
        raise ValueError("--method must be 0 to 6.")
    return {"source": str(source), "root": str(root), "page": page, "out": str(Path(out).resolve()),
            "themes": [t for t in str(themes).split(",") if t], "items": None if items in (None, "all") else [i for i in items.split(",") if i],
            "max_kb": max_kb, "method": method, "viewport_width": viewport_width}


class Renderer:
    """One browser, one static server per served root and one encoder pool, reused by every job given to render()."""

    def __init__(self, browser=None, workers=None, keep_pool=False):
        self.choice = browser
        self.workers = workers or os.cpu_count() or 2
        self.keep_pool = keep_pool
        self._pw = self.browser = self._pool = None
        self._servers = {}

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def start(self):
        if self.browser is None or not self.browser.is_connected():
            if self._pw is None:
                from playwright.sync_api import sync_playwright
                self._pw = sync_playwright().start()
            self.browser = launch(self._pw, self.choice)
        if self.keep_pool and self._pool is None:
            self._pool = concurrent.futures.ProcessPoolExecutor(max_workers=self.workers)
        return self

    def close(self):
        for server in self._servers.values():
            server.shutdown()
            server.server_close()
        self._servers.clear()
        if self._pool is not None:
            self._pool.shutdown(cancel_futures=True)
            self._pool = None
        if self.browser is not None:
            try:
                self.browser.close()
            except Exception:  # noqa: BLE001, S110 - the browser is already gone
                pass
            self.browser = None
        if self._pw is not None:
            self._pw.stop()
            self._pw = None

    def _port(self, root):
        if root not in self._servers:
            server = QuietServer(("127.0.0.1", 0), functools.partial(Quiet, directory=root))
            threading.Thread(target=server.serve_forever, daemon=True).start()
            self._servers[root] = server
        return self._servers[root].server_address[1]

    def render(self, job, emit=print):
        """Render one job; emit() receives each output line. Returns the number of problems (WARN lines), 0 when clean."""
        t0 = time.perf_counter()
        self.start()
        out = Path(job["out"])
        out.mkdir(parents=True, exist_ok=True)
        port = self._port(job["root"])
        problems, tasks = 0, []
        fonts_used, grounds, checked = [], {}, False
        pool, own_pool = self._pool, None
        try:
            for theme in job["themes"]:
                page = self.browser.new_page(viewport={"width": job["viewport_width"], "height": 1400})
                try:
                    page.goto(f"http://127.0.0.1:{port}/{job['page']}?theme={theme}", wait_until="networkidle")
                    page.evaluate("document.fonts.ready.then(() => true)")
                    page.wait_for_timeout(300)
                    items = page.eval_on_selector_all(".item", ITEMS_JS)
                    ids = [i["id"] for i in items]
                    if not ids or any(not i for i in ids):
                        raise ValueError("every .item needs an id; it becomes the file name.")
                    repeated = sorted({i for i in ids if ids.count(i) > 1})
                    if repeated:
                        raise ValueError(f"item ids used twice: {', '.join(repeated)}; each id becomes one file name.")
                    if job["items"]:
                        unknown = [i for i in job["items"] if i not in ids]
                        if unknown:
                            raise ValueError(f"no item with id {', '.join(unknown)} in {job['page']} (items: {', '.join(ids)}).")
                    if not checked:
                        checked = True
                        total = len(job["items"] or ids) * len(job["themes"])
                        if pool is None and total > 1:  # one picture encodes faster here than a worker starts
                            pool = own_pool = concurrent.futures.ProcessPoolExecutor(max_workers=min(total, self.workers))
                        info = page.evaluate(FONT_JS)
                        fonts_used = info["used"] + info["plain"]
                        if info["missing"]:
                            problems += 1
                            emit(f"WARN fonts requested but not loaded, so a fallback face is in the images: {', '.join(info['missing'])}. "
                                 "Render online, install the font, or load it from a font host.")
                        if page.evaluate(PLACEHOLDER_JS):
                            problems += 1
                            emit("WARN starter placeholder tokens are still in use: replace them with the repository's own "
                                 "and delete --starter-placeholder from the stylesheet.")
                    grounds[theme] = page.eval_on_selector(".item", "e => getComputedStyle(e).backgroundColor")
                    for item in items:
                        if job["items"] and item["id"] not in job["items"]:
                            continue
                        problems += self._capture(page, item, theme, out, job, tasks, emit, pool)
                finally:
                    page.close()
            t1 = time.perf_counter()
            problems += self._collect(tasks, job, emit)
        finally:
            if own_pool is not None:
                own_pool.shutdown(cancel_futures=True)
        emit("fonts: " + (", ".join(fonts_used) if fonts_used else "none found"))
        emit("grounds: " + ", ".join(f"{t} {c}" for t, c in grounds.items()))
        emit(f"rendered in {time.perf_counter() - t0:.1f} s (encode finished {time.perf_counter() - t1:.1f} s after the last capture)")
        return problems

    def _capture(self, page, item, theme, out, job, tasks, emit, pool):
        problems = 0
        el = page.locator(f"#{item['id']}")
        clipped = el.evaluate(OVERFLOW_JS)
        if clipped:
            problems += 1
            emit(f"WARN {item['id']} ({theme}): content leaves the item box: {', '.join(clipped)}")
        finish = item["finish"] if item["finish"] in ("card", "plain", "transparent", "social") else "card"
        if finish == "social":
            unsafe = el.evaluate(SAFE_JS)
            if unsafe:
                problems += 1
                emit(f"WARN {item['id']} ({theme}): text inside the 40 px safe border of the social preview: {', '.join(unsafe)}")
            blocks = el.evaluate(TEXT_BLOCKS_JS)
            if len(blocks) > 1:
                problems += 1
                emit(f"WARN {item['id']} ({theme}): more than one text block ({', '.join(blocks[:5])}); the social card holds "
                     "the brand name only, a tagline cannot be read in a chat thumbnail")
        line = parse_color(el.evaluate("e => getComputedStyle(e).getPropertyValue('--cardline')"),
                           FALLBACK_BORDER.get(theme, FALLBACK_BORDER["light"]))
        if finish == "transparent":
            el.evaluate(CLEAR_GROUND_JS)
            png = el.screenshot(scale="css", omit_background=True)
            page.evaluate("window.__fdRestore()")
        else:
            png = el.screenshot(scale="css")
        ext = ".png" if finish == "social" else ".webp"
        dst = out / (f"{item['id']}{ext}" if theme == "light" else f"{item['id']}-{theme}{ext}")
        radius = int(item["radius"]) if str(item["radius"]).isdigit() else 24
        border = int(item["border"]) if str(item["border"]).isdigit() else 3
        args = (png, str(dst), finish, line, radius, border, job["method"])
        tasks.append((finish, str(dst), pool.submit(finish_and_save, *args) if pool is not None else args))
        return problems

    def _collect(self, tasks, job, emit):
        problems = 0
        for finish, dst, work in tasks:
            w, h, size = work.result() if isinstance(work, concurrent.futures.Future) else finish_and_save(*work)
            name = Path(dst).name
            flags = ""
            if finish == "social":
                if (w, h) != (1280, 640):
                    flags += "  WARN not 1280x640 (the item must be 640x320 CSS px)"
                if size > SOCIAL_MAX_BYTES:
                    flags += "  WARN over the 1 MB GitHub limit"
            elif size / 1024 > job["max_kb"]:
                flags += f"  WARN over {job['max_kb']} KB"
            problems += bool(flags)
            emit(f"{name}  {w}x{h}  {size / 1024:.0f} KB{flags}")
        return problems


def render_once(job, browser=None, emit=print):
    try:
        with Renderer(browser=browser) as r:
            return r.render(job, emit)
    except (ValueError, RuntimeError) as e:
        print(f"fd: {e}", file=sys.stderr)
        return -1
