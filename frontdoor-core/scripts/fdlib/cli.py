"""Command line of the frontdoor harness. See `fd --help`; the commands are described in references/harness.md."""

import argparse
import json
import os
import sys
import time
import webbrowser
from pathlib import Path

from . import VERSION, FdError, daemon
from . import board as boardlib
from .paths import SCRIPTS, board_dir, ensure_ignored, repo_root

WATCH_EXT = {".html", ".htm", ".css", ".js", ".mjs", ".svg", ".json", ".woff", ".woff2", ".ttf", ".otf"}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}

EPILOG = """examples:
  fd page add icons --title "App icons"
  fd round new icons --count 3 --title "First marks"
  fd render .frontdoor/board/icons/round-1/a/icons.html --out .frontdoor/board/icons/round-1/a/out
  fd round add icons
  fd choose icons 1 B --note "B, with the stroke of A"
  fd status --json
  fd daemon start            (then every fd render reuses one open browser)
  fd render assets/source/readme.html --root assets --out assets --watch
"""


def parser():
    ap = argparse.ArgumentParser(prog="fd", description="The frontdoor harness: the design board, the renderer and its browser daemon.",
                                 epilog=EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=f"fd {VERSION}")
    ap.add_argument("--repo", help="the repository root (default: the nearest folder with .git above the current folder)")
    sub = ap.add_subparsers(dest="cmd", required=True, metavar="<command>")

    page = sub.add_parser("page", help="add or list the pages of the board").add_subparsers(dest="action", required=True, metavar="<action>")
    p = page.add_parser("add", help="add a page, one per use case (readme, icons, navbar)")
    p.add_argument("slug")
    p.add_argument("--title", default="")
    page.add_parser("list", help="list the pages")

    rnd = sub.add_parser("round", help="start or publish a round of variants").add_subparsers(dest="action", required=True, metavar="<action>")
    p = rnd.add_parser("new", help="start the next round of a page: one folder per variant and a round.json to fill in")
    p.add_argument("slug")
    p.add_argument("--count", type=int, required=True, help="how many variants; ask the user, there is no default")
    p.add_argument("--title", default="")
    p.add_argument("--note", default="")
    p.add_argument("--seed", help="a file copied into every variant folder to start from, such as a starter source page")
    p = rnd.add_parser("add", help="publish a round on the board from its round.json and the renders in each variant folder")
    p.add_argument("slug")
    p.add_argument("n", nargs="?", type=int, help="the round number (default: the latest draft, else the latest round)")
    p.add_argument("--open", action="store_true", help="open the board in the default browser")

    p = sub.add_parser("choose", help="record which variants the user chose in a round")
    p.add_argument("slug")
    p.add_argument("n", type=int)
    p.add_argument("ids", help="variant ids, comma separated; several ids record a mix")
    p.add_argument("--note", default="", help="what was mixed or changed")

    p = sub.add_parser("status", help="summarise the board (and the daemon) in a few lines")
    p.add_argument("slug", nargs="?")
    p.add_argument("--json", action="store_true")

    brd = sub.add_parser("board", help="rebuild or open the board page").add_subparsers(dest="action", required=True, metavar="<action>")
    p = brd.add_parser("build", help="rebuild index.html and board-data.js after a hand edit of board.json")
    p.add_argument("--open", action="store_true")
    brd.add_parser("open", help="open the board in the default browser")

    p = sub.add_parser("render", help="render every .item of a source page to a light and a dark image")
    p.add_argument("source")
    p.add_argument("--out", required=True)
    p.add_argument("--root", help="the folder served over HTTP (default: the folder holding the page)")
    p.add_argument("--themes", default="light,dark")
    p.add_argument("--items", default="all", help="comma separated item ids (default: all)")
    p.add_argument("--max-kb", type=int, default=300)
    p.add_argument("--method", type=int, default=None, help="libwebp effort 0 to 6 (default 4)")
    p.add_argument("--viewport-width", type=int, default=2600)
    p.add_argument("--browser", choices=["msedge", "chrome", "chromium"])
    p.add_argument("--watch", action="store_true", help="render again whenever a file under the root changes; Ctrl-C stops")
    p.add_argument("--no-daemon", action="store_true", help="render in this process even when a daemon is running")

    p = sub.add_parser("animate", help="render a looping animated WebP; every option after it is animate.py's (see animate.py --help)")
    p.add_argument("rest", nargs=argparse.REMAINDER)

    p = sub.add_parser("contrast", help="print the WCAG contrast ratio of colour pairs: fd contrast <fg> <bg> [...]")
    p.add_argument("rest", nargs=argparse.REMAINDER)

    dmn = sub.add_parser("daemon", help="keep one browser open between renders").add_subparsers(dest="action", required=True, metavar="<action>")
    p = dmn.add_parser("start", help="start the daemon in the background")
    p.add_argument("--idle", type=int, default=daemon.IDLE_DEFAULT, help="seconds without a job before it stops (default 1800)")
    p.add_argument("--browser", choices=["msedge", "chrome", "chromium"])
    dmn.add_parser("stop")
    dmn.add_parser("status")
    p = dmn.add_parser("run", help="run the daemon in the foreground")
    p.add_argument("--idle", type=int, default=daemon.IDLE_DEFAULT)
    p.add_argument("--browser", choices=["msedge", "chrome", "chromium"])
    return ap


def open_page(path):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        else:
            webbrowser.open(Path(path).resolve().as_uri())
    except Exception as e:  # noqa: BLE001 - no desktop session: the printed path is enough
        print(f"fd: could not open the board ({e}); open the path above by hand.", file=sys.stderr)


def report_board(b, root, open_it=False):
    note = ensure_ignored(root)
    if note:
        print(f"fd: {note}", file=sys.stderr)
    page = (b.dir / "index.html").resolve()
    print(f"board: {page}")
    print(f"open:  {page.as_uri()}")
    if open_it:
        open_page(page)


def cmd_page(a, root):
    b = boardlib.Board(board_dir(root))
    if a.action == "list":
        for p in b.data["pages"]:
            print(f"{p['slug']}  {len(p['rounds'])} round(s)  {p['title']}")
        return 0
    b.add_page(a.slug, a.title)
    b.save()
    print(f"page {a.slug} added; start its first round with: fd round new {a.slug} --count N")
    report_board(b, root)
    return 0


def cmd_round(a, root):
    b = boardlib.Board(board_dir(root))
    if a.action == "new":
        rnd, folder = b.new_round(a.slug, a.count, a.title, a.note, a.seed)
        b.save()
        print(f"round {rnd['n']} of {a.slug}: {folder.resolve()}")
        for v in rnd["variants"]:
            print(f"  variant {v['id']}: {(folder / v['id'].lower()).resolve()}")
        print(f"  text:      {(folder / 'round.json').resolve()}")
        print("next: build each variant in its folder, render into <variant>/out/, fill round.json, then "
              f"fd round add {a.slug}")
        return 0
    rnd = b.publish_round(a.slug, a.n)
    b.save()
    images = sum(len(v["images"]) for v in rnd["variants"])
    print(f"round {rnd['n']} of {a.slug} is on the board: {len(rnd['variants'])} variant(s), {images} picture(s)")
    for v in rnd["variants"]:
        pics = ", ".join(f"{i['label']}[{'+'.join(t for t in ('light', 'dark') if t in i)}]" for i in v["images"]) or "no picture"
        print(f"  {v['id']}  {v['title']}  {pics}" + (f"  {len(v['links'])} link(s)" if v["links"] else ""))
    report_board(b, root, a.open)
    return 0


def cmd_choose(a, root):
    b = boardlib.Board(board_dir(root))
    rnd = b.choose(a.slug, a.n, a.ids, a.note)
    b.save()
    print(f"round {rnd['n']} of {a.slug}: chose {', '.join(rnd['choice']['chosen'])}" + (f" ({rnd['choice']['note']})" if rnd["choice"]["note"] else ""))
    return 0


def cmd_status(a, root):
    bdir = board_dir(root)
    info = boardlib.Board(bdir).status(a.slug) if (bdir / "board.json").exists() else {"board": None, "pages": []}
    state = daemon.alive(root)
    info["daemon"] = None if not state else {"pid": state["pid"], "port": state["port"], "jobs": state.get("jobs")}
    if a.json:
        print(json.dumps(info, ensure_ascii=False))
        return 0
    if not info["pages"]:
        print("board: no page yet; add one with `fd page add <slug>`")
    else:
        print(f"board: {info['board']}")
    for p in info["pages"]:
        last = p["latest"]
        if last is None:
            print(f"{p['slug']}: no round yet")
            continue
        chosen = f"chosen {','.join(last['chosen'])}" if last["chosen"] else "no choice yet"
        drafts = f", draft round(s) {','.join(map(str, p['drafts']))}" if p["drafts"] else ""
        print(f"{p['slug']}: {p['rounds']} round(s); round {last['n']} {last['status']}, variants {','.join(last['variants'])}, {chosen}{drafts}")
    print("daemon: " + (f"running, pid {state['pid']}, {state.get('jobs', 0)} job(s)" if state else "not running"))
    return 0


def cmd_board(a, root):
    b = boardlib.Board(board_dir(root))
    if a.action == "build":
        b.build()
    elif not b.file.exists():
        raise FdError("there is no board yet; add a page with `fd page add <slug>`.")
    report_board(b, root, a.action == "open" or a.open)
    return 0


def snapshot(root):
    seen = {}
    for folder, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if os.path.splitext(name)[1].lower() in WATCH_EXT:
                path = os.path.join(folder, name)
                try:
                    seen[path] = os.stat(path).st_mtime_ns
                except OSError:
                    pass
    return seen


def cmd_render(a, root):
    from . import render as renderlib

    try:
        job = renderlib.make_job(a.source, a.out, a.root, a.themes, a.items, a.max_kb,
                                 renderlib.DEFAULT_METHOD if a.method is None else a.method, a.viewport_width)
    except ValueError as e:
        raise FdError(str(e), 2) from None
    state = None if a.no_daemon else daemon.alive(root)
    local = None

    def once():
        nonlocal local
        if state:
            res = daemon.render(state, job)
            for line in res["lines"]:
                print(line, file=sys.stderr if line.startswith("fd: ") else sys.stdout)
            return res["problems"]
        if local is None:
            local = renderlib.Renderer(browser=a.browser, keep_pool=a.watch)
        try:
            return local.render(job)
        except (ValueError, RuntimeError) as e:
            print(f"fd: {e}", file=sys.stderr)
            return -1

    try:
        problems = once()
        if not a.watch:
            return 0 if problems == 0 else 1
        print(f"watching {job['root']} (Ctrl-C stops)", flush=True)
        seen = snapshot(job["root"])
        while True:
            time.sleep(0.4)
            now = snapshot(job["root"])
            if now != seen:
                time.sleep(0.25)  # let an editor finish writing
                seen = snapshot(job["root"])
                print(f"--- change seen at {time.strftime('%H:%M:%S')}", flush=True)
                once()
    except KeyboardInterrupt:
        return 0
    finally:
        if local is not None:
            local.close()


def cmd_passthrough(module, rest):
    """Run animate.py or contrast.py with their own options, imported so their worker processes can find their functions."""
    sys.path.insert(0, str(SCRIPTS))
    mod = __import__(module)
    sys.argv = [f"{module}.py", *rest]
    try:
        mod.main()
    except SystemExit as e:
        if isinstance(e.code, str):
            print(e.code, file=sys.stderr)
            return 1
        return e.code or 0
    return 0


def cmd_daemon(a, root):
    if a.action == "run":
        daemon.run(root, a.idle, a.browser)
        return 0
    if a.action == "start":
        state, fresh = daemon.start(root, SCRIPTS / "fd.py", a.idle, a.browser)
        print(f"daemon {'started' if fresh else 'already running'}: pid {state['pid']}, port {state['port']}")
        return 0
    if a.action == "stop":
        print("daemon stopped" if daemon.stop(root) else "daemon was not running")
        return 0
    state = daemon.alive(root)
    print(f"daemon running: pid {state['pid']}, port {state['port']}, {state['jobs']} job(s), stops after {state['idle_left']} s idle"
          if state else "daemon not running")
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    # animate and contrast keep their own options, which argparse would try to read as fd's own
    head = 2 if argv[:1] == ["--repo"] else 0
    if len(argv) > head and argv[head] in ("animate", "contrast"):
        return cmd_passthrough(argv[head], argv[head + 1:])
    a = parser().parse_args(argv)
    root = Path(a.repo).resolve() if a.repo else repo_root()
    try:
        if a.cmd == "page":
            return cmd_page(a, root)
        if a.cmd == "round":
            return cmd_round(a, root)
        if a.cmd == "choose":
            return cmd_choose(a, root)
        if a.cmd == "status":
            return cmd_status(a, root)
        if a.cmd == "board":
            return cmd_board(a, root)
        if a.cmd == "render":
            return cmd_render(a, root)
        if a.cmd == "daemon":
            return cmd_daemon(a, root)
    except FdError as e:
        print(f"fd: {e}", file=sys.stderr)
        return e.code
    except KeyboardInterrupt:
        return 130
    return 2
