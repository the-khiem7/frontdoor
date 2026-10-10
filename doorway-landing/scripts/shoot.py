#!/usr/bin/env python
"""Screenshot and check a static landing page, or render its social preview image.

    uvx --from playwright python -I shoot.py check <root> [--page index.html] [--widths 390,820,1280]
        [--schemes light,dark] [--axe <axe.min.js>] [--out <dir>]
    uvx --from playwright python -I shoot.py og <page.html> --out og.png [--root <dir>]

`check` serves <root> over HTTP and opens the page at each width, in the light and the dark color
scheme, scrolling to the bottom so scroll-triggered content appears. It saves a full-page PNG per
combination and prints FAIL for a broken local image or link, a missing anchor target, horizontal
overflow or a page error, and WARN for missing metadata, an image without alt text, or an og:image
that is not a file under <root> or is not 1200x630. With --axe it injects axe-core (the file
axe.min.js that ships inside an npx lighthouse install) and reports contrast and accessibility
violations in each scheme. It also takes one extra screenshot with reduced motion (after scrolling,
so lazy images load), which must still show all content. Exit code 1 on FAIL. Use
--widths 1280 --schemes light for a quick look at a rough draft.

`og` renders a page at 1200x630 to a PNG (social scrapers do not read WebP).

A browser is taken from the machine (Edge, then Chrome); nothing is downloaded.
"""
import argparse
import functools
import http.server
import sys
import threading
from pathlib import Path
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright


class QuietServer(http.server.ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        pass  # a browser closing a connection early is not an error here


def launch(p, choice):
    last = None
    for name in ([choice] if choice else ["msedge", "chrome", "chromium"]):
        try:
            return p.chromium.launch() if name == "chromium" else p.chromium.launch(channel=name)
        except Exception as e:
            last = e
    sys.exit(f"shoot.py: no browser could be launched ({last}). Install Edge or Chrome.")


def serve(root):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    server = QuietServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(root)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1]


PAGE_FACTS = """() => {
  const vw = window.innerWidth;
  const wide = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.width && r.right > vw + 1) wide.push((el.id || el.className || el.tagName).toString().slice(0, 40));
  }
  const meta = (sel, attr) => { const e = document.querySelector(sel); return e ? e.getAttribute(attr) : null; };
  return {
    overflowX: document.documentElement.scrollWidth > vw + 1,
    wide: wide.slice(0, 5),
    brokenImgs: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src')),
    noAlt: [...document.images].filter(i => !i.hasAttribute('alt')).map(i => i.getAttribute('src')),
    anchors: [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1),
    missingTargets: [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1 && !document.getElementById(decodeURIComponent(h.slice(1)))),
    links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')),
    lang: document.documentElement.lang,
    title: document.title,
    description: meta('meta[name=description]', 'content'),
    ogTitle: meta('meta[property="og:title"]', 'content'),
    ogImage: meta('meta[property="og:image"]', 'content'),
    twitter: meta('meta[name="twitter:card"]', 'content'),
    icon: meta('link[rel~=icon]', 'href'),
    viewport: meta('meta[name=viewport]', 'content'),
  };
}"""


def scroll_through(page):
    height = page.evaluate("document.documentElement.scrollHeight")
    step = page.evaluate("window.innerHeight")
    y = 0
    while y < height:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(120)
        y += step
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(200)


def local_file_for(url, root):
    """Map an absolute site URL to a file under root by trying the longest path suffix that exists."""
    parts = [x for x in urlparse(url).path.split("/") if x]
    for i in range(len(parts)):
        candidate = root.joinpath(*parts[i:])
        if candidate.is_file():
            return candidate
    return None


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[1:4] != b"PNG":
        return None
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


def check(a):
    root = Path(a.root).resolve()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    server, port = serve(root)
    base = f"http://127.0.0.1:{port}/"
    widths = [int(w) for w in a.widths.split(",")]
    schemes = [s for s in a.schemes.split(",") if s]
    axe_source = Path(a.axe).read_text(encoding="utf-8") if a.axe else None
    fails = warns = 0
    checked_links = set()
    with sync_playwright() as p:
        browser = launch(p, a.browser)
        for scheme in schemes:
            for width in widths:
                tag = f"{width}px {scheme}"
                ctx = browser.new_context(viewport={"width": width, "height": 900}, color_scheme=scheme)
                page = ctx.new_page()
                errors, failed = [], []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.on("requestfailed", lambda r: failed.append(r.url))
                page.on("response", lambda r: failed.append(f"{r.status} {r.url}") if r.status >= 400 else None)
                page.goto(base + a.page, wait_until="networkidle")
                scroll_through(page)
                facts = page.evaluate(PAGE_FACTS)
                shot = out / f"{Path(a.page).stem}-{width}-{scheme}.png"
                page.screenshot(path=str(shot), full_page=True)

                def fail(msg):
                    nonlocal fails
                    fails += 1
                    print(f"FAIL {tag}: {msg}")

                def warn(msg):
                    nonlocal warns
                    warns += 1
                    print(f"WARN {tag}: {msg}")

                if facts["overflowX"]:
                    fail(f"horizontal overflow, from: {', '.join(facts['wide']) or 'unknown'}")
                if facts["brokenImgs"]:
                    fail(f"images did not load: {facts['brokenImgs']}")
                if facts["missingTargets"]:
                    fail(f"anchors with no target: {facts['missingTargets']}")
                for e in errors:
                    fail(f"page error: {e}")
                for f in failed:
                    host = urlparse(f.split(" ", 1)[-1]).hostname or ""
                    (warn if host not in ("127.0.0.1", "localhost") else fail)(f"request failed: {f}")
                if facts["noAlt"]:
                    warn(f"images without alt: {facts['noAlt']}")
                if axe_source:
                    page.evaluate(axe_source)
                    result = page.evaluate("axe.run().then(r => r.violations.map(v => ({id: v.id, n: v.nodes.length, impact: v.impact, sample: v.nodes[0].target.join(' ')})))")
                    for v in result:
                        fail(f"axe {v['id']} ({v['impact']}, {v['n']} nodes), first: {v['sample']}")
                if scheme == schemes[0] and width == widths[0]:
                    for key, label in (("lang", "html lang"), ("title", "title"), ("description", "meta description"),
                                       ("ogTitle", "og:title"), ("ogImage", "og:image"), ("twitter", "twitter:card"),
                                       ("icon", "favicon link"), ("viewport", "meta viewport")):
                        if not facts[key]:
                            warn(f"missing {label}")
                    if facts["ogImage"]:
                        img = local_file_for(facts["ogImage"], root)
                        if img is None:
                            warn(f"og:image {facts['ogImage']} matches no file under {root}")
                        else:
                            size = png_size(img)
                            if size is None:
                                warn(f"og:image {img.name} is not a PNG, size not checked")
                            elif size != (1200, 630):
                                warn(f"og:image {img.name} is {size[0]}x{size[1]}, expected 1200x630")
                    for href in facts["links"]:
                        if href in checked_links or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                            continue
                        checked_links.add(href)
                        if urlparse(href).scheme in ("http", "https"):
                            continue
                        resp = page.request.get(urljoin(base + a.page, href))
                        if resp.status >= 400:
                            fail(f"local link {href} returns {resp.status}")
                print(f"shot {shot.name}")
                ctx.close()
        ctx = browser.new_context(viewport={"width": widths[-1], "height": 900}, reduced_motion="reduce")
        page = ctx.new_page()
        page.goto(base + a.page, wait_until="networkidle")
        scroll_through(page)
        shot = out / f"{Path(a.page).stem}-reduced-motion.png"
        page.screenshot(path=str(shot), full_page=True)
        print(f"shot {shot.name}  (reduced motion: every section must be visible; look at it)")
        ctx.close()
        browser.close()
    server.shutdown()
    external = sum(1 for _ in checked_links if urlparse(_).scheme in ("http", "https"))
    print(f"external links not fetched: {external}. Check them yourself.")
    print(f"shoot check: {fails} FAIL, {warns} WARN")
    sys.exit(1 if fails else 0)


def og(a):
    page_path = Path(a.page).resolve()
    root = Path(a.root).resolve() if a.root else page_path.parent
    server, port = serve(root)
    with sync_playwright() as p:
        browser = launch(p, a.browser)
        page = browser.new_page(viewport={"width": 1200, "height": 630})
        page.goto(f"http://127.0.0.1:{port}/{page_path.relative_to(root).as_posix()}", wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(300)
        page.screenshot(path=a.out, clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        browser.close()
    server.shutdown()
    print(f"{a.out} 1200x630")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("root")
    c.add_argument("--page", default="index.html")
    c.add_argument("--widths", default="390,820,1280")
    c.add_argument("--schemes", default="light,dark")
    c.add_argument("--axe")
    c.add_argument("--out", default="shots")
    c.add_argument("--browser")
    o = sub.add_parser("og")
    o.add_argument("page")
    o.add_argument("--out", required=True)
    o.add_argument("--root")
    o.add_argument("--browser")
    a = ap.parse_args()
    check(a) if a.cmd == "check" else og(a)


if __name__ == "__main__":
    main()
