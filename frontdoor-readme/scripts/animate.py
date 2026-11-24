#!/usr/bin/env python
"""Render one .item of an HTML source page as a looping animated WebP, once per theme, by calling a drawing function per frame.

    uvx --from playwright --with pillow python -I animate.py <source.html> --item <id> --call "draw({v})" --out <dir>
        [--root <dir>] [--name banner] [--motion sway|loop] [--amp 30] [--frames 30] [--fps 12] [--quality 68]
        [--size 1200x420] [--method 4] [--themes light,dark] [--max-kb 700] [--draft] [--workers N]
        [--browser msedge|chrome|chromium]
    uvx --from playwright --with pillow python -I animate.py --batch jobs.json [--draft] [--workers N]

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
Output: <name>.webp for light, <name>-dark.webp for dark, lossy at --quality, looping forever, one loop lasting frames / fps
seconds. --size scales the frames and must keep the aspect ratio; the default keeps the 2x size of the still pictures. The script
prints each file size and exits 1 with a WARN when one is over --max-kb; fewer --frames, a smaller --size or a lower --quality bring
it down. --method is libwebp's effort, 0 to 6; 4 is the default because on one 2400x840 frame 6 took about twelve times as long for a
file under 1 percent smaller. A picture of many thin lines (rippling rings, a grid) stayed under 700 KB at 1500 px wide, 20 frames and
quality 55.

How it is fast: every theme is captured in its own browser page at the same time; a sway value that repeats (the sine passes each
value twice) is drawn and captured once; each frame is finished and encoded in its own worker process, --workers at once (default:
the number of CPUs), as soon as it is captured; a frame stores only the rectangle that changed since the previous frame; and the
frames are joined into the animated WebP container here, without re-encoding. Memory stays bounded by the number of workers, and
each file is written to a .part file first and renamed when complete, so a stopped run never leaves a half-written picture.

--draft renders a quick preview to check the motion: 600 px wide, at most 12 frames over the same loop length, method 2, quality
50, written as <name>.draft.webp and <name>-dark.draft.webp, with no size limit. An explicit --size, --method or --quality still
applies; --frames sets the loop length, of which the draft keeps 12 frames.

--batch reads a JSON list of jobs and renders them in one run with one browser and one pool of workers, which is faster than one
run per picture. Each job is an object with the long option names as keys (dashes or underscores), for example
  [{"source": "assets/source/readme.html", "root": "assets", "item": "banner", "call": "drawBanner({v})", "out": "assets"},
   {"source": "assets/source/readme.html", "root": "assets", "item": "flow", "call": "drawFlow({v})", "out": "assets",
    "motion": "loop", "frames": 20}]
Options given on the command line are the defaults of every job; relative paths are taken from the current folder.

A browser is taken from the machine (Edge, then Chrome); pass --browser chromium for Playwright's own build.
"""
import argparse
import asyncio
import concurrent.futures
import functools
import http.server
import io
import json
import math
import os
import re
import sys
import threading
import time
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

FALLBACK_BORDER = {"light": (191, 211, 227), "dark": (44, 74, 102)}
PAGES = 4  # browser pages captured at the same time; each holds a large viewport, so the number stays small
DRAFT = {"width": 600, "frames": 12, "method": 2, "quality": 50}
SETTLE = """() => Promise.race([
  Promise.all([...document.images].filter(i => !i.complete).map(i => new Promise(r => {
    i.addEventListener('load', r, {once: true}); i.addEventListener('error', r, {once: true}); })))
    .then(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))),
  new Promise(r => setTimeout(r, 1000))])"""


class QuietServer(http.server.ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        pass


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


async def launch(p, choice):
    last = None
    for name in [choice] if choice else ["msedge", "chrome", "chromium"]:
        try:
            return await (p.chromium.launch() if name == "chromium" else p.chromium.launch(channel=name))
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


# ---- worker side: finish one frame and encode it ----

@functools.lru_cache(maxsize=8)
def masks(w, h, radius, border, supersample=4):
    """The rounded alpha mask and the border ring for one frame size; built once per worker, not once per frame."""
    def mask(inset, r):
        m = Image.new("L", (w * supersample, h * supersample), 0)
        ImageDraw.Draw(m).rounded_rectangle(
            (round(inset * supersample), round(inset * supersample),
             round((w - inset) * supersample) - 1, round((h - inset) * supersample) - 1),
            radius=round(r * supersample), fill=255)
        return m.resize((w, h), Image.LANCZOS)

    outer, inner = mask(0, radius), mask(border, radius - border)
    return outer, ImageChops.subtract(outer, inner)


def target_size(native, size):
    if size is None:
        return native
    if size[0] == "width":
        return size[1], max(1, round(size[1] * native[1] / native[0]))
    return size[1]


def finish(png, size, line):
    """The finish render.py gives the still pictures (rounded corners, a border), applied at the output size. Radius and border
    scale with the output, so a smaller file shows the same corners as the still picture at the same display width."""
    img = Image.open(io.BytesIO(png)).convert("RGB")
    native = img.size
    w, h = target_size(native, size)
    if (w, h) != native:
        img = img.resize((w, h), Image.LANCZOS)
    s = w / native[0]
    outer, ring = masks(w, h, 24 * s, 3 * s)
    out = img.convert("RGBA")
    out.paste(Image.new("RGBA", (w, h), line + (255,)), (0, 0), ring)
    out.putalpha(outer)
    return out


def riff_chunks(data):
    pos = 12
    while pos + 8 <= len(data):
        n = int.from_bytes(data[pos + 4:pos + 8], "little")
        yield data[pos:pos + 4], data[pos + 8:pos + 8 + n]
        pos += 8 + n + (n & 1)


def chunk(fourcc, payload):
    return fourcc + len(payload).to_bytes(4, "little") + payload + (b"\0" if len(payload) & 1 else b"")


def changed_blocks(cur, prev, block=8):
    """An L mask of the crop, 255 on every block x block square that differs from the previous frame, 0 elsewhere."""
    r, g, b = ImageChops.difference(cur.convert("RGB"), prev.convert("RGB")).split()
    diff = ImageChops.lighter(ImageChops.lighter(r, g), b).point(lambda p: 255 if p else 0)
    small = diff.reduce(block).point(lambda p: 255 if p else 0)  # reduce averages, so any changed pixel leaves a value above 0
    return small.resize((small.width * block, small.height * block), Image.NEAREST).crop((0, 0) + cur.size)


def encode_frame(cur_png, prev_png, size, line, quality, method):
    """Finish frame i, keep only the rectangle that changed since frame i-1 and encode it as a still WebP.
    Inside the rectangle, blocks that did not change are made transparent and the frame is blended over the previous one, the
    way libwebp's own animation encoder saves bytes; a transparent block costs almost nothing in the lossy stream.
    Returns (x, y, w, h, blend, frame data, canvas size), or None when nothing changed. Runs in a worker process."""
    cur = finish(cur_png, size, line)
    x = y = 0
    crop, blend = cur, False
    if prev_png is not None:
        prev = finish(prev_png, size, line)
        box = ImageChops.difference(cur.convert("RGB"), prev.convert("RGB")).getbbox()  # the alpha is the same in every frame
        if box is None:
            return None
        x, y = box[0] - box[0] % 2, box[1] - box[1] % 2  # ANMF offsets are stored halved, so they must be even
        crop = cur.crop((x, y, box[2], box[3]))
        keep = changed_blocks(crop, prev.crop((x, y, box[2], box[3])))
        alpha = crop.getchannel("A")
        # Blending is exact only where the new pixels are opaque; a changed block on a rounded corner keeps the plain overwrite.
        if ImageChops.lighter(alpha, ImageChops.invert(keep)).getextrema()[0] == 255:
            crop.putalpha(ImageChops.multiply(alpha, keep))
            blend = True
    buf = io.BytesIO()
    crop.save(buf, "WEBP", quality=quality, method=method)
    data = b"".join(chunk(fc, p) for fc, p in riff_chunks(buf.getvalue()) if fc in (b"ALPH", b"VP8 ", b"VP8L"))
    return x, y, crop.width, crop.height, blend, data, cur.size


def mux(canvas, frames):
    """Join encoded frames (x, y, w, h, duration ms, blend, data) into a looping animated WebP; no frame is disposed."""
    u24 = lambda n: int(n).to_bytes(3, "little")  # noqa: E731
    body = chunk(b"VP8X", bytes([0x12, 0, 0, 0]) + u24(canvas[0] - 1) + u24(canvas[1] - 1))  # flags: alpha, animation
    body += chunk(b"ANIM", bytes(4) + (0).to_bytes(2, "little"))  # transparent background, loop forever
    for x, y, w, h, dur, blend, data in frames:
        flags = 0x00 if blend else 0x02  # bit 1 set: overwrite the rectangle instead of blending it over the canvas
        body += chunk(b"ANMF", u24(x // 2) + u24(y // 2) + u24(w - 1) + u24(h - 1) + u24(dur) + bytes([flags]) + data)
    return b"RIFF" + (len(body) + 4).to_bytes(4, "little") + b"WEBP" + body


# ---- main side: jobs, capture, assembly ----

def make_jobs(a, ap):
    defaults = {k: v for k, v in vars(a).items() if k not in ("batch", "workers", "browser")}
    if a.batch:
        try:
            entries = json.loads(Path(a.batch).read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            sys.exit(f"animate.py: cannot read --batch {a.batch}: {e}")
        if not isinstance(entries, list) or not all(isinstance(e, dict) for e in entries):
            sys.exit("animate.py: --batch must hold a JSON list of objects.")
        known = set(defaults)
        raw = []
        for e in entries:
            e = {k.replace("-", "_"): v for k, v in e.items()}
            unknown = set(e) - known
            if unknown:
                sys.exit(f"animate.py: unknown key in --batch: {', '.join(sorted(unknown))}")
            raw.append({**defaults, **e})
    else:
        raw = [defaults]

    jobs = []
    for j in raw:
        for key in ("source", "item", "call", "out"):
            if not j.get(key):
                ap.error(f"every job needs {key}" if a.batch else f"the {key} is required")
        if "{v}" not in j["call"]:
            sys.exit("animate.py: --call needs {v}, the place the value goes, for example \"draw({v})\".")
        if j["motion"] not in ("sway", "loop"):
            sys.exit(f"animate.py: motion must be sway or loop, not {j['motion']}.")
        method = j["method"] if j["method"] is not None else (DRAFT["method"] if j["draft"] else 4)
        if method not in range(7):
            sys.exit("animate.py: method must be 0 to 6.")
        source = Path(j["source"]).resolve()
        root = Path(j["root"]).resolve() if j["root"] else source.parent
        try:
            rel = source.relative_to(root).as_posix()
        except ValueError:
            sys.exit(f"animate.py: {source} is not inside --root {root}.")
        loop_frames = j["frames"] or 30
        frames = min(DRAFT["frames"], loop_frames) if j["draft"] else loop_frames
        if j["size"]:
            size = ("fixed", tuple(int(x) for x in str(j["size"]).lower().split("x")))
        else:
            size = ("width", DRAFT["width"]) if j["draft"] else None
        period = 1000 * loop_frames / j["fps"] / frames  # ms per frame; a draft keeps the loop length of the real file
        values = [j["amp"] * math.sin(2 * math.pi * i / frames) if j["motion"] == "sway" else i / frames for i in range(frames)]
        jobs.append({
            "source": source, "root": root, "rel": rel, "item": j["item"], "call": j["call"], "name": j["name"] or j["item"],
            "out": Path(j["out"]).resolve(), "themes": [t for t in str(j["themes"]).split(",") if t], "values": values,
            "durations": [round((i + 1) * period) - round(i * period) for i in range(frames)], "size": size,
            "quality": j["quality"] if j["quality"] is not None else (DRAFT["quality"] if j["draft"] else 68),
            "method": method, "max_kb": None if j["draft"] else j["max_kb"], "suffix": ".draft" if j["draft"] else "",
        })
    return jobs


async def render(job, theme, browser, port, sem, pool, t0):
    loop = asyncio.get_running_loop()
    shots, tasks, prev, prev_key = {}, [], None, None
    unique = 0
    async with sem:
        page = await browser.new_page(viewport={"width": 2600, "height": 1400})
        try:
            await page.goto(f"http://127.0.0.1:{port}/{job['rel']}?theme={theme}", wait_until="networkidle")
            await page.evaluate("document.fonts.ready.then(() => true)")
            el = page.locator(f"#{job['item']}")
            if await el.count() == 0:
                raise LookupError(f"no element with id {job['item']} in {job['rel']}")
            line = parse_color(
                await el.evaluate("e => getComputedStyle(e).getPropertyValue('--cardline')"),
                FALLBACK_BORDER.get(theme, FALLBACK_BORDER["light"]))
            for i, v in enumerate(job["values"]):
                key = round(v, 9)  # the sine gives each sway value twice; draw and capture it once
                if key not in shots:
                    await page.evaluate(job["call"].replace("{v}", repr(v)))
                    if i == 0:
                        await page.wait_for_timeout(200)  # the first frame loads the images; later ones come from cache
                    await page.evaluate(SETTLE)
                    shots[key] = await el.screenshot(scale="css")
                    unique += 1
                cur = shots[key]
                if key == prev_key:
                    tasks.append(None)
                else:
                    tasks.append(loop.run_in_executor(
                        pool, encode_frame, cur, prev, job["size"], line, job["quality"], job["method"]))
                prev, prev_key = cur, key
        except BaseException:
            for t in tasks:
                if t is not None:
                    t.cancel()
            raise
        finally:
            await page.close()
    del shots
    results = [await t if t is not None else None for t in tasks]

    frames, canvas = [], None
    for res, dur in zip(results, job["durations"]):
        if res is None:  # nothing changed: the previous frame stays on screen longer
            x, y, w, h, d, blend, data = frames[-1]
            frames[-1] = (x, y, w, h, d + dur, blend, data)
            continue
        x, y, w, h, blend, data, canvas = res
        frames.append((x, y, w, h, dur, blend, data))
    dst = job["out"] / (f"{job['name']}{job['suffix']}.webp" if theme == "light" else f"{job['name']}-{theme}{job['suffix']}.webp")
    part = dst.with_name(dst.name + ".part")
    part.write_bytes(mux(canvas, frames))
    os.replace(part, dst)
    kb = dst.stat().st_size / 1024
    flag = f"  WARN over {job['max_kb']} KB" if job["max_kb"] is not None and kb > job["max_kb"] else ""
    print(f"{dst.name}  {canvas[0]}x{canvas[1]}  {len(job['values'])} frames ({unique} drawn)  {kb:.0f} KB"
          f"  done at {time.time() - t0:.0f} s{flag}", flush=True)
    return bool(flag)


async def run(jobs, a):
    from playwright.async_api import async_playwright

    t0 = time.time()
    servers = {}
    for job in jobs:
        if job["root"] not in servers:
            server = QuietServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(job["root"])))
            threading.Thread(target=server.serve_forever, daemon=True).start()
            servers[job["root"]] = server
        job["out"].mkdir(parents=True, exist_ok=True)

    sem = asyncio.Semaphore(PAGES)
    problems = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=a.workers) as pool:
        async with async_playwright() as p:
            browser = await launch(p, a.browser)
            work = [(job, theme) for job in jobs for theme in job["themes"]]
            outcomes = await asyncio.gather(
                *[render(job, theme, browser, servers[job["root"]].server_address[1], sem, pool, t0) for job, theme in work],
                return_exceptions=True)
            await browser.close()
    for (job, theme), res in zip(work, outcomes):
        if isinstance(res, BaseException):
            print(f"animate.py: {job['name']} ({theme}) failed: {res}", file=sys.stderr)
            problems += 1
        else:
            problems += res
    for server in servers.values():
        server.shutdown()
    print(f"total {time.time() - t0:.0f} s")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", nargs="?")
    ap.add_argument("--item")
    ap.add_argument("--call")
    ap.add_argument("--out")
    ap.add_argument("--root")
    ap.add_argument("--name")
    ap.add_argument("--motion", choices=["sway", "loop"], default="sway")
    ap.add_argument("--amp", type=float, default=30)
    ap.add_argument("--frames", type=int)
    ap.add_argument("--fps", type=int, default=12)
    ap.add_argument("--quality", type=int)
    ap.add_argument("--method", type=int, choices=range(7))
    ap.add_argument("--size")
    ap.add_argument("--themes", default="light,dark")
    ap.add_argument("--max-kb", type=int, default=700)
    ap.add_argument("--draft", action="store_true")
    ap.add_argument("--batch")
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 2)
    ap.add_argument("--browser")
    a = ap.parse_args()
    jobs = make_jobs(a, ap)
    sys.exit(1 if asyncio.run(run(jobs, a)) else 0)


if __name__ == "__main__":
    main()
