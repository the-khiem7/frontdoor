#!/usr/bin/env python
"""Render every state listed in a gallery.json from a mocked frontend, or check the gallery page.

    uvx --from playwright --with pillow python -I shoot.py render <gallery.json> [--base <url>] [--only id,id]
    uvx --from playwright python -I shoot.py check <gallery dir> [--out <dir>]

`render` opens each state at <base><view url>?state=<scenario> in the light and the dark color scheme
(or the themes the view lists), runs the state's actions (click, fill, hover, press, eval, wait), screenshots
the whole window, the full scroll height, or the union of the elements a crop selects, and saves
shots/<id>-<theme>.webp beside gallery.json. It writes gallery-data.js, which the gallery page reads;
with --only it re-shoots only the listed states and keeps the images of the others, while titles,
notes and every other text are always taken from gallery.json. A page error, a crop that finds fewer
elements than it names, or an action whose target is missing or ambiguous stops the run with exit
code 1. A view with "timers": "paused" runs on a paused fake clock: every wait advances it by exactly
that many ms, so app timers (polling, timeouts that clear a message) fire at the same moment in every
run.
<base> defaults to the "base" of gallery.json; the mocked dev server must already be running there.

`check` opens <gallery dir>/index.html at 390 and 1440 px in both color schemes and prints FAIL for a
page error, a broken image, a state whose image file is missing, or horizontal overflow; it saves a
screenshot of each combination to --out (default: a ui-gallery-check folder in the system temp
folder, outside the repository). Exit code 1 on FAIL.

A browser is taken from the machine (Edge, then Chrome); nothing is downloaded.
"""
import argparse
import io
import json
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

from playwright.sync_api import sync_playwright

MEASURE = """([scroller, crop]) => {
  const doc = document.scrollingElement;
  const box = (scroller && document.querySelector(scroller)) || doc;
  box.scrollTop = 0; doc.scrollTop = 0;
  // A scroller below fixed chrome (a title bar) is shorter than the window by that chrome.
  const extra = box === doc ? 0 : window.innerHeight - box.clientHeight;
  let found = 0, clip = null;
  if (crop) {
    const pick = [...document.querySelectorAll(crop.selector)].filter(el => {
      if (!crop.text) return true;
      const h = crop.heading ? el.querySelector(crop.heading) : el;
      return h && crop.text.some(t => h.textContent.trim().startsWith(t));
    });
    found = pick.length;
    const r = pick.map(el => el.getBoundingClientRect());
    if (r.length) clip = { top: Math.min(...r.map(x => x.top)), bottom: Math.max(...r.map(x => x.bottom)) };
  }
  return { height: box.scrollHeight + extra, found, clip };
}"""


def launch(p):
    last = None
    for name in ["msedge", "chrome", "chromium"]:
        try:
            return p.chromium.launch() if name == "chromium" else p.chromium.launch(channel=name)
        except Exception as e:
            last = e
    sys.exit(f"shoot.py: no browser could be launched ({last}). Install Edge or Chrome.")


def view_of(g, state):
    v = dict(g.get("defaults", {}))
    v.update(g["views"][state["view"]])
    v.update({k: state[k] for k in ("size", "url", "scroller", "themes", "clock", "timers", "settle", "reducedMotion", "omitBackground") if k in state})
    return v


def theme_script(theme_cfg, theme):
    # Runs before the page's own scripts, so an app that reads its theme at start-up sees it.
    by = (theme_cfg or {}).get("by", "media")
    if by == "storage":
        value = theme_cfg.get("values", {}).get(theme, theme)
        return f"try {{ localStorage.setItem({json.dumps(theme_cfg['key'])}, {json.dumps(value)}); }} catch (e) {{}}"
    if by == "script":
        return f"(() => {{ const THEME = {json.dumps(theme)}; {theme_cfg['code']} }})();"
    return ""


def target(page, step):
    # The control a click or fill acts on: by accessible name (inside "within", the "nth" match), or by a CSS selector.
    scope = page.locator(step["within"]) if "within" in step else page
    if "selector" in step:
        loc = scope.locator(step["selector"])
    elif "click" in step or "hover" in step:
        loc = scope.get_by_role(step.get("role", "button"), name=step.get("click") or step["hover"], exact=True)
    else:
        loc = scope.get_by_label(step["fill"], exact=True)
    return loc.nth(step["nth"]) if "nth" in step else loc


def act(page, step, wait):
    if "value" in step:
        target(page, step).fill(step["value"], timeout=5000)
    elif "hover" in step:
        target(page, step).hover(timeout=5000)
    elif "click" in step or "selector" in step:
        target(page, step).click(timeout=5000)
    elif "press" in step:
        page.keyboard.press(step["press"])
    elif "eval" in step:
        page.evaluate(step["eval"])
    wait(step.get("wait", 450))


def describe(step):
    if "label" in step:
        return step["label"]
    what = step.get("click") or step.get("fill") or step.get("hover") or step.get("selector")
    if "value" in step:
        return f"type {what}"
    if "hover" in step:
        return f"hover {what}"
    if "click" in step or "selector" in step:
        return f"click {what}"
    if "press" in step:
        return f"press {step['press']}"
    if "eval" in step:
        return "script"
    return f"wait {step.get('wait', 0)} ms"


def shoot(browser, g, state, theme, out_dir, base, scale, quality):
    from PIL import Image

    v = view_of(g, state)
    w, h = v["size"]
    ctx = browser.new_context(
        viewport={"width": w, "height": h},
        device_scale_factor=scale,
        color_scheme=theme,
        reduced_motion="reduce" if v.get("reducedMotion") else "no-preference",
    )
    script = theme_script(v.get("theme"), theme)
    if script:
        ctx.add_init_script(script)
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    paused = v.get("timers") == "paused"
    start = datetime.fromisoformat(v["clock"]) if v.get("clock") else datetime.now().replace(microsecond=0)
    if paused:
        page.clock.install(time=start - timedelta(seconds=1))
        page.clock.pause_at(start)
    elif v.get("clock"):
        page.clock.set_fixed_time(start)

    def wait(ms):
        if paused:
            page.clock.run_for(ms)
            page.wait_for_timeout(80)  # let the browser paint what the timers changed
        else:
            page.wait_for_timeout(ms)

    url = v.get("url", "/")
    page.goto(f"{base}{url}{'&' if '?' in url else '?'}state={state['state']}")
    wait(v.get("settle", 700))
    for step in state.get("actions", []):
        try:
            act(page, step, wait)
        except Exception as e:
            raise SystemExit(f"{state['id']} ({theme}): action {describe(step)} failed: {str(e).splitlines()[0]}")
    if state.get("actions") and not state.get("keepHover"):
        # The pointer stays where the last click was; move it off the page so no hover style is shot as the state.
        page.mouse.move(-20, -20)
        wait(100)
    crop = state.get("crop", "window")
    if crop != "window":
        # Grow the window until the scroller no longer scrolls; a layout tied to the window height can grow with it.
        for _ in range(4):
            m = page.evaluate(MEASURE, [v.get("scroller"), crop if isinstance(crop, dict) else None])
            if m["height"] <= page.viewport_size["height"]:
                break
            page.set_viewport_size({"width": w, "height": max(h, m["height"])})
            wait(200)
    clip = None
    if isinstance(crop, dict):
        m = page.evaluate(MEASURE, [v.get("scroller"), crop])
        want = len(crop.get("text", [])) or 1
        if m["found"] < want or not m["clip"]:
            raise SystemExit(f"{state['id']} ({theme}): crop found {m['found']} element(s), expected {want}")
        pad = crop.get("pad", 12)
        top = max(0, m["clip"]["top"] - pad)
        clip = {"x": 0, "y": top, "width": w, "height": m["clip"]["bottom"] + pad - top}
    png = page.screenshot(clip=clip, omit_background=bool(v.get("omitBackground")))
    ctx.close()
    if errors:
        raise SystemExit(f"{state['id']} ({theme}): page error {errors[0]}")
    img = Image.open(io.BytesIO(png))
    img = img.convert("RGBA" if v.get("omitBackground") else "RGB")
    out = out_dir / "shots" / f"{state['id']}-{theme}.webp"
    img.save(out, "WEBP", quality=quality, method=6)
    return {"w": img.width // scale, "h": img.height // scale, "kb": round(out.stat().st_size / 1024)}


def render(args):
    gfile = Path(args.gallery).resolve()
    out_dir = gfile.parent
    g = json.loads(gfile.read_text(encoding="utf-8"))
    base = (args.base or g.get("base", "")).rstrip("/")
    if not base:
        sys.exit("shoot.py: no base URL; set \"base\" in gallery.json or pass --base")
    scale, quality = g.get("scale", 2), g.get("quality", 80)
    ids = [s["id"] for s in g["states"]]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        sys.exit(f"shoot.py: state id used twice: {', '.join(sorted(dup))}")
    for s in g["states"]:
        if s["view"] not in g["views"]:
            sys.exit(f"shoot.py: {s['id']} names an unknown view {s['view']!r}")
    only = {s for s in (args.only or "").split(",") if s}
    (out_dir / "shots").mkdir(exist_ok=True)
    data_file = out_dir / "gallery-data.js"
    old = {}
    if data_file.exists():
        text = data_file.read_text(encoding="utf-8")
        old = {s["id"]: s for s in json.loads(text[text.index("{"): text.rindex("}") + 1])["states"]}

    states = []
    with sync_playwright() as p:
        browser = launch(p)
        for s in g["states"]:
            v = view_of(g, s)
            entry = {k: s.get(k, "") for k in ("id", "view", "state", "title", "how", "note")}
            entry["actions"] = [describe(a) for a in s.get("actions", [])]
            crop = s.get("crop", "window")
            entry["crop"] = "cards" if isinstance(crop, dict) else crop
            entry["themes"] = v.get("themes", ["light", "dark"])
            if "size" in s:
                entry["size"] = s["size"]
            prev = old.get(s["id"], {})
            keep = only and s["id"] not in only and all(
                t in prev and (out_dir / "shots" / f"{s['id']}-{t}.webp").exists() for t in entry["themes"])
            if keep:
                entry.update({t: prev[t] for t in entry["themes"]})
                states.append(entry)
                continue
            for theme in entry["themes"]:
                entry[theme] = shoot(browser, g, s, theme, out_dir, base, scale, quality)
            sizes = " + ".join(str(entry[t]["kb"]) for t in entry["themes"])
            first = entry[entry["themes"][0]]
            print(f"{s['id']:30} {first['w']}x{first['h']}  {sizes} KB")
            states.append(entry)
        browser.close()

    real = []
    for r in g.get("real", []):
        f = out_dir / "real" / f"{r['id']}.png"
        if f.exists():
            from PIL import Image

            with Image.open(f) as im:
                real.append({**r, "w": im.width, "h": im.height})
        else:
            print(f"WARN {r['id']}: real/{r['id']}.png not found, left out")
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=out_dir).stdout.strip()
    views = {k: {**g.get("defaults", {}), **v} for k, v in g["views"].items()}
    data = {
        "title": g.get("title", "UI gallery"),
        "lede": g.get("lede", ""),
        "regenerate": g.get("regenerate", []),
        "generated": date.today().isoformat(),
        "commit": commit,
        "storageKey": g.get("storageKey", "ui-gallery:" + g.get("title", "")),
        "views": views,
        "states": states,
        "skipped": g.get("skipped", []),
        "real": real,
    }
    data_file.write_bytes(("window.GALLERY = " + json.dumps(data, indent=1, ensure_ascii=False) + ";\n").encode("utf-8"))
    kb = sum(f.stat().st_size for f in (out_dir / "shots").glob("*.webp")) // 1024
    print(f"{len(states)} states, {len(real)} real screenshots, shots/ {kb} KB -> {data_file.name}")


CHECK = """() => {
  const vw = window.innerWidth;
  return {
    overflowX: document.documentElement.scrollWidth > vw + 1,
    broken: [...document.images].filter(i => i.getAttribute('src') && i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src')),
    hasData: !!window.GALLERY,
  };
}"""


def check(args):
    root = Path(args.dir).resolve()
    page_file = root / "index.html"
    if not page_file.exists():
        sys.exit(f"shoot.py: {page_file} not found")
    fails = []
    data_file = root / "gallery-data.js"
    if data_file.exists():
        text = data_file.read_text(encoding="utf-8")
        data = json.loads(text[text.index("{"): text.rindex("}") + 1])
        for s in data["states"]:
            for t in s.get("themes", ["light", "dark"]):
                if not (root / "shots" / f"{s['id']}-{t}.webp").exists():
                    fails.append(f"missing image shots/{s['id']}-{t}.webp")
    else:
        fails.append("gallery-data.js not found; run render first")
    shots = Path(args.out) if args.out else Path(tempfile.gettempdir()) / "ui-gallery-check"
    shots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = launch(p)
        for width in (390, 1440):
            for scheme in ("light", "dark"):
                page = browser.new_page(viewport={"width": width, "height": 1000}, color_scheme=scheme)
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.goto(page_file.as_uri())
                page.wait_for_timeout(600)
                page.evaluate("() => document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
                page.wait_for_timeout(900)
                facts = page.evaluate(CHECK)
                tag = f"{width}px {scheme}"
                fails += [f"{tag}: page error {e}" for e in errors]
                if not facts["hasData"]:
                    fails.append(f"{tag}: the page found no gallery data")
                if facts["overflowX"]:
                    fails.append(f"{tag}: horizontal overflow")
                fails += [f"{tag}: broken image {b}" for b in facts["broken"]]
                page.screenshot(path=str(shots / f"{width}-{scheme}.png"))
                page.close()
        browser.close()
    for f in dict.fromkeys(fails):
        print("FAIL", f)
    print(f"check: {len(set(fails))} FAIL; screenshots in {shots}")
    sys.exit(1 if fails else 0)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Render a UI gallery from a mocked frontend, or check its page.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render")
    r.add_argument("gallery")
    r.add_argument("--base")
    r.add_argument("--only")
    c = sub.add_parser("check")
    c.add_argument("dir")
    c.add_argument("--out")
    args = ap.parse_args()
    render(args) if args.cmd == "render" else check(args)


if __name__ == "__main__":
    main()
