#!/usr/bin/env python
"""Render one .item of an HTML source page as a looping GIF, once per theme, by calling a drawing function per frame.

    uvx --from playwright --with pillow python -I animate.py <source.html> --item <id> --call "draw({v})" --out <dir>
        [--root <dir>] [--name banner] [--amp 30] [--frames 90] [--fps 10] [--colors 128] [--size 1200x420] [--themes light,dark]

The source page must expose a global function that redraws the item for a value v; --call is the JavaScript expression
run once per frame with {v} replaced by the number. v follows amp * sin(2 * pi * frame / frames), so frame 0 and the frame after
the last are equal and the loop is seamless with few frames, and the motion is a slow sway rather than a spin. The defaults
(+-30, 90 frames at 10 per second) are a 9 second loop with a peak change of about 21 units per second; if v is degrees, that is
gentle enough to read the banner while it moves. Keep v small and slow: a fast spin makes readers dizzy.

The page is served over HTTP from --root (default: the folder holding the page), opened as <page>?theme=<theme>, and the item is
screenshotted at CSS scale. Output: <name>.gif for light, <name>-dark.gif for dark, with one palette per file (--colors, up to
256), no dithering, no rounded corners and no border: a GIF has one-bit transparency, so rounding would be jagged. --size scales
the frames; it must keep the aspect ratio. The file size is printed; for the README banner keep it near 2 MB (fewer colours, a
smaller --size, fewer --frames). It is for the README banner only: the GitHub social preview is a still PNG.

A browser is taken from the machine (Edge, then Chrome); pass --browser chromium for Playwright's own build.
"""
import argparse
import functools
import http.server
import math
import sys
import tempfile
import threading
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--item", required=True)
    ap.add_argument("--call", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--root")
    ap.add_argument("--name")
    ap.add_argument("--amp", type=float, default=30)
    ap.add_argument("--frames", type=int, default=90)
    ap.add_argument("--fps", type=int, default=10)
    ap.add_argument("--colors", type=int, default=128)
    ap.add_argument("--size")
    ap.add_argument("--themes", default="light,dark")
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

    with sync_playwright() as p, tempfile.TemporaryDirectory() as tmp:
        browser = launch(p, a.browser)
        for theme in [t for t in a.themes.split(",") if t]:
            page = browser.new_page(viewport={"width": 2600, "height": 1400})
            page.goto(f"http://127.0.0.1:{port}/{rel}?theme={theme}", wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            el = page.locator(f"#{a.item}")
            frames = []
            for i in range(a.frames):
                page.evaluate(a.call.replace("{v}", repr(a.amp * math.sin(2 * math.pi * i / a.frames))))
                page.wait_for_timeout(200 if i == 0 else 40)  # the first frame loads the images; later ones come from cache
                shot = Path(tmp) / "frame.png"
                el.screenshot(path=str(shot), scale="css")
                frames.append(Image.open(shot).convert("RGB").copy())
            size = tuple(int(x) for x in a.size.lower().split("x")) if a.size else (frames[0].width // 2, frames[0].height // 2)
            frames = [f.resize(size, Image.LANCZOS) for f in frames]
            pal = frames[0].convert("P", palette=Image.ADAPTIVE, colors=a.colors)
            quant = [f.quantize(palette=pal, dither=Image.NONE) for f in frames]
            dst = out / (f"{name}.gif" if theme == "light" else f"{name}-{theme}.gif")
            quant[0].save(dst, save_all=True, append_images=quant[1:], duration=1000 // a.fps, loop=0, optimize=True, disposal=1)
            print(f"{dst.name}  {size[0]}x{size[1]}  {a.frames} frames at {a.fps}/s  {dst.stat().st_size / 1e6:.2f} MB")
            page.close()
        browser.close()
    server.shutdown()


if __name__ == "__main__":
    main()
