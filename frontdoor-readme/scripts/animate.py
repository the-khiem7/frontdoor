#!/usr/bin/env python
"""Render one .item of an HTML source page as a looping animated WebP, once per theme, by calling a drawing function per frame.

    uvx --from playwright --with pillow python -I animate.py <source.html> --item <id> --call "draw({v})" --out <dir>
        [--root <dir>] [--name banner] [--motion sway|loop] [--amp 30] [--frames 30] [--fps 12] [--quality 68]
        [--size 1200x420] [--themes light,dark] [--max-kb 700] [--browser msedge|chrome|chromium]

WebP is the only animated format of these skills: on the same 30 frames of a 1200x420 banner a GIF came out near 3 MB and the
animated WebP near 300 KB, and WebP keeps 24-bit colour and the rounded, bordered corners of the still pictures.

The source page must expose a global function that redraws the item for a value v; --call is the JavaScript expression run once
per frame with {v} replaced by the number. --motion sets how v moves over one loop of --frames frames:

  sway  v = amp * sin(2 * pi * i / frames): a slow back-and-forth, for shapes that turn a few degrees and back. --amp is the peak
        (default 30). Keep it small and slow; a fast spin makes readers dizzy.
  loop  v = i / frames, 0 up to just under 1: one position in a cycle, for motion that repeats by itself, such as waves that drift
        one period, bobbing shapes or rising bubbles. Frame 0 and the frame after the last are equal, so the loop is seamless.

The page is served over HTTP from --root (default: the folder holding the page), opened as <page>?theme=<theme>, and the item is
screenshotted at CSS scale, then finished like the still pictures: rounded corners and a border in the item's --cardline colour.
Output: <name>.webp for light, <name>-dark.webp for dark, lossy at --quality with --fps frames a second, looping forever. --size
scales the frames and must keep the aspect ratio; the default keeps the 2x size of the still pictures. The script prints each file
size and exits 1 with a WARN when one is over --max-kb; fewer --frames, a smaller --size or a lower --quality bring it down.

A browser is taken from the machine (Edge, then Chrome); pass --browser chromium for Playwright's own build.
"""
import argparse
import functools
import http.server
import math
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
        pass


def launch(p, choice):
    last = None
    for name in [choice] if choice else ["msedge", "chrome", "chromium"]:
        try:
            return p.chromium.launch() if name == "chromium" else p.chromium.launch(channel=name)
        except Exception as e:  # browser not installed: try the next one
            last = e
    sys.exit(f"animate.py: no browser could be launched ({last}). Install Edge or Chrome, or run `playwright install chromium`.")


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


def round_and_border(png, line, radius=24, border=3, supersample=4):
    """The same finish as render.py gives the still pictures: rounded corners and a border, as an RGBA image."""
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
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--item", required=True)
    ap.add_argument("--call", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--root")
    ap.add_argument("--name")
    ap.add_argument("--motion", choices=["sway", "loop"], default="sway")
    ap.add_argument("--amp", type=float, default=30)
    ap.add_argument("--frames", type=int, default=30)
    ap.add_argument("--fps", type=int, default=12)
    ap.add_argument("--quality", type=int, default=68)
    ap.add_argument("--size")
    ap.add_argument("--themes", default="light,dark")
    ap.add_argument("--max-kb", type=int, default=700)
    ap.add_argument("--browser")
    a = ap.parse_args()
    if "{v}" not in a.call:
        sys.exit("animate.py: --call needs {v}, the place the value goes, for example \"draw({v})\".")

    source = Path(a.source).resolve()
    root = Path(a.root).resolve() if a.root else source.parent
    try:
        rel = source.relative_to(root).as_posix()
    except ValueError:
        sys.exit(f"animate.py: {source} is not inside --root {root}.")
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    name = a.name or a.item

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    server = QuietServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(root)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    port = server.server_address[1]

    problems = 0
    with sync_playwright() as p, tempfile.TemporaryDirectory() as tmp:
        browser = launch(p, a.browser)
        for theme in [t for t in a.themes.split(",") if t]:
            page = browser.new_page(viewport={"width": 2600, "height": 1400})
            page.goto(f"http://127.0.0.1:{port}/{rel}?theme={theme}", wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            el = page.locator(f"#{a.item}")
            line = parse_color(
                el.evaluate("e => getComputedStyle(e).getPropertyValue('--cardline')"),
                FALLBACK_BORDER.get(theme, FALLBACK_BORDER["light"]))
            frames = []
            for i in range(a.frames):
                v = a.amp * math.sin(2 * math.pi * i / a.frames) if a.motion == "sway" else i / a.frames
                page.evaluate(a.call.replace("{v}", repr(v)))
                page.wait_for_timeout(200 if i == 0 else 40)  # the first frame loads the images; later ones come from cache
                shot = Path(tmp) / "frame.png"
                el.screenshot(path=str(shot), scale="css")
                frames.append(round_and_border(shot, line))
            size = tuple(int(x) for x in a.size.lower().split("x")) if a.size else frames[0].size
            if size != frames[0].size:
                frames = [f.resize(size, Image.LANCZOS) for f in frames]
            dst = out / (f"{name}.webp" if theme == "light" else f"{name}-{theme}.webp")
            frames[0].save(dst, "WEBP", save_all=True, append_images=frames[1:], duration=1000 // a.fps,
                           loop=0, quality=a.quality, method=6)
            kb = dst.stat().st_size / 1024
            flag = "" if kb <= a.max_kb else f"  WARN over {a.max_kb} KB"
            problems += bool(flag)
            print(f"{dst.name}  {size[0]}x{size[1]}  {a.frames} frames at {a.fps}/s  {kb:.0f} KB{flag}")
            page.close()
        browser.close()
    server.shutdown()
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
