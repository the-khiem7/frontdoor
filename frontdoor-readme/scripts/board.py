#!/usr/bin/env python
"""Keep one local board of design directions for a repository: every round, newest first.

    uvx python -I board.py add    <dir> <round.json> [--no-open] [--inline]
    uvx python -I board.py build  <dir> [--no-open] [--inline]
    uvx python -I board.py choose <dir> <round> <ids> [--note TEXT] [--no-open] [--inline]

<dir> is the `.frontdoor` folder of the repository being worked on. It holds the rough sources and renders
of each round (for example round-1/, round-2/), `directions.json` (the record of every round) and
`directions.html` (the board, rebuilt from the record on every command).

add     appends the round described by <round.json> and rebuilds the board. The file looks like
        {"title": "...", "note": "...", "directions": [{"id": "4", "title": "...", "concept": "...",
         "strengths": "...", "risks": "...", "flaws": "...",
         "images": [{"label": "Light", "file": "round-2/hero.webp"}],
         "links": [{"label": "Open the page", "file": "round-3/a/index.html"}]}]}
        `id` is optional: a missing id continues the numbering of the board. Every `file` is a path
        relative to <dir> and must exist inside it.
build   rebuilds the board after a hand edit of directions.json.
choose  records which direction ids (comma separated, for a mix list each id) the user picked in a round.

The board links its images by relative path, so it stays small however many rounds it holds; keep it beside
its folders. --inline embeds every image instead, to get one file that can be sent on its own. The script
adds `.frontdoor/` to the repository's .gitignore when the entry is missing, opens the board in the default
browser unless --no-open is given, and prints its path. Standard library only; nothing is uploaded.
"""
import argparse
import base64
import datetime
import html
import json
import mimetypes
import os
import subprocess
import sys
import urllib.parse
from pathlib import Path

CSS = """
:root { --bg:#f4f4f1; --panel:#ffffff; --fg:#1d2024; --muted:#565c66; --line:#d8d9d4; --accent:#0b5cad; --chip:#e7eef7; }
@media (prefers-color-scheme: dark) { :root { --bg:#14161a; --panel:#1d2025; --fg:#eceae5; --muted:#a9aeb8; --line:#33373e; --accent:#7db4f0; --chip:#25303d; color-scheme: dark; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 16px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif; padding-inline: 16px; padding-block: 32px; }
main { max-width: 1080px; margin: 0 auto; display: flex; flex-direction: column; gap: 28px; }
header { display: flex; flex-direction: column; gap: 8px; }
h1 { margin: 0; font-size: 1.7rem; line-height: 1.2; text-wrap: balance; }
h2, h3 { margin: 0; line-height: 1.25; }
p { margin: 0; }
.meta { color: var(--muted); font-size: .9rem; }
nav { display: flex; flex-wrap: wrap; gap: 8px; }
nav a { color: var(--accent); background: var(--chip); border-radius: 999px; padding: 4px 12px; font-size: .88rem; text-decoration: none; }
nav a:focus-visible, summary:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
details.round { border-top: 1px solid var(--line); padding-top: 18px; }
details.round > summary { cursor: pointer; display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 14px; list-style-position: inside; }
details.round > summary h2 { font-size: 1.3rem; display: inline; }
.round-body { display: flex; flex-direction: column; gap: 22px; margin-top: 16px; }
.tag { font-size: .78rem; letter-spacing: .06em; text-transform: uppercase; color: var(--accent); background: var(--chip); border-radius: 4px; padding: 2px 8px; }
.card { background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 18px; display: flex; flex-direction: column; gap: 14px; min-width: 0; }
.card.chosen { border-color: var(--accent); border-width: 2px; }
.card-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 12px; }
.card-head .id { font-variant-numeric: tabular-nums; font-weight: 700; color: var(--muted); }
dl { margin: 0; display: grid; grid-template-columns: max-content 1fr; gap: 6px 16px; }
dt { color: var(--muted); font-size: .8rem; letter-spacing: .06em; text-transform: uppercase; padding-top: 3px; }
dd { margin: 0; min-width: 0; }
figure { margin: 0; display: flex; flex-direction: column; gap: 4px; }
figcaption { font-size: .78rem; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); }
img { display: block; width: 100%; max-width: 100%; height: auto; }
.links { display: flex; flex-wrap: wrap; gap: 8px 16px; }
.links a { color: var(--accent); }
@media (max-width: 560px) { dl { grid-template-columns: 1fr; } dt { padding-top: 0; } }
"""


def fail(msg):
    sys.exit(f"board.py: {msg}")


def load(board_dir):
    path = board_dir / "directions.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data.get("rounds"), list):
            fail(f"{path} has no rounds list.")
        return data
    return {"project": board_dir.resolve().parent.name, "rounds": []}


def save(board_dir, data):
    board_dir.mkdir(parents=True, exist_ok=True)
    tmp = board_dir / "directions.json.tmp"
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(board_dir / "directions.json")


def inside(board_dir, rel):
    target = (board_dir / rel).resolve()
    try:
        target.relative_to(board_dir.resolve())
    except ValueError:
        fail(f"{rel} points outside {board_dir}.")
    if not target.is_file():
        fail(f"{rel} does not exist under {board_dir}.")
    return target


def text(value):
    return value.strip() if isinstance(value, str) else ""


def numeric_ids(data):
    ids = []
    for rnd in data["rounds"]:
        for d in rnd["directions"]:
            if str(d["id"]).isdigit():
                ids.append(int(d["id"]))
    return ids


def normalise_round(board_dir, data, raw):
    if not isinstance(raw, dict) or not isinstance(raw.get("directions"), list) or not raw["directions"]:
        fail("the round file needs a non-empty `directions` list.")
    seen = {str(d["id"]) for r in data["rounds"] for d in r["directions"]}
    nxt = max(numeric_ids(data) or [0]) + 1
    directions, in_round = [], set()
    for d in raw["directions"]:
        if not text(d.get("title")):
            fail("every direction needs a title.")
        did = str(d.get("id") or "").strip()
        if not did:
            did = str(nxt)
            nxt += 1
        if did in seen or did in in_round:
            fail(f"direction id {did} is already used on the board.")
        in_round.add(did)
        images = []
        for img in d.get("images") or []:
            inside(board_dir, img["file"])
            images.append({"label": text(img.get("label")), "file": img["file"]})
        links = []
        for link in d.get("links") or []:
            inside(board_dir, link["file"])
            links.append({"label": text(link.get("label")) or link["file"], "file": link["file"]})
        directions.append({
            "id": did, "title": text(d["title"]), "concept": text(d.get("concept")),
            "strengths": text(d.get("strengths")), "risks": text(d.get("risks")), "flaws": text(d.get("flaws")),
            "images": images, "links": links,
        })
    return {
        "id": max([r["id"] for r in data["rounds"]] or [0]) + 1,
        "created": datetime.date.today().isoformat(),
        "title": text(raw.get("title")), "note": text(raw.get("note")),
        "directions": directions, "chosen": [], "choice_note": "",
    }


def src(board_dir, rel, inline):
    if not inline:
        return urllib.parse.quote(Path(rel).as_posix())
    path = inside(board_dir, rel)
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def e(value):
    return html.escape(value, quote=True)


def card(board_dir, d, chosen, inline):
    parts = [f'<article class="card{" chosen" if chosen else ""}">',
             f'<div class="card-head"><span class="id">{e(d["id"])}</span><h3>{e(d["title"])}</h3>'
             + ('<span class="tag">Chosen</span>' if chosen else "") + "</div>"]
    if d["concept"]:
        parts.append(f'<p>{e(d["concept"])}</p>')
    rows = [(k, d[f]) for k, f in (("Strengths", "strengths"), ("Risks", "risks"), ("Known flaws", "flaws")) if d[f]]
    if rows:
        parts.append("<dl>" + "".join(f"<dt>{k}</dt><dd>{e(v)}</dd>" for k, v in rows) + "</dl>")
    for img in d["images"]:
        label = f'<figcaption>{e(img["label"])}</figcaption>' if img["label"] else ""
        alt = f'{d["title"]}, {img["label"]}'.strip(", ")
        parts.append(f'<figure>{label}<img loading="lazy" src="{e(src(board_dir, img["file"], inline))}" alt="{e(alt)}"></figure>')
    if d["links"]:
        parts.append('<div class="links">' + "".join(
            f'<a href="{e(urllib.parse.quote(Path(l["file"]).as_posix()))}">{e(l["label"])}</a>' for l in d["links"]) + "</div>")
    parts.append("</article>")
    return "".join(parts)


def render(board_dir, data, inline):
    rounds = sorted(data["rounds"], key=lambda r: r["id"], reverse=True)
    project = data.get("project") or "project"
    nav = "".join(f'<a href="#round-{r["id"]}">Round {r["id"]}</a>' for r in rounds)
    sections = []
    for i, r in enumerate(rounds):
        by_id = {d["id"]: d for d in r["directions"]}
        picked = [by_id[c]["title"] for c in r["chosen"] if c in by_id]
        head = f'<h2>Round {r["id"]}{(": " + e(r["title"])) if r["title"] else ""}</h2><span class="meta">{e(r["created"])}</span>'
        if picked:
            head += f'<span class="tag">Chosen: {e(", ".join(picked))}</span>'
        body = []
        if r["note"]:
            body.append(f'<p>{e(r["note"])}</p>')
        if r["choice_note"]:
            body.append(f'<p class="meta">Choice note: {e(r["choice_note"])}</p>')
        body += [card(board_dir, d, d["id"] in r["chosen"], inline) for d in r["directions"]]
        sections.append(f'<details class="round" id="round-{r["id"]}"{" open" if i == 0 else ""}><summary>{head}</summary>'
                        f'<div class="round-body">{"".join(body)}</div></details>')
    empty = '<p class="meta">No round has been added yet.</p>' if not rounds else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{e(project)} design directions</title><style>{CSS}</style></head><body><main>'
            f'<header><h1>{e(project)} design directions</h1>'
            f'<p class="meta">{len(rounds)} round(s), newest first. Local file, not committed, built from directions.json.</p>'
            f'<nav aria-label="Rounds">{nav}</nav></header>{empty}{"".join(sections)}</main></body></html>')


def ensure_ignored(board_dir):
    root = board_dir.resolve().parent
    if not ((root / ".git").exists() or (root / ".gitignore").exists()):
        return
    entry = board_dir.name
    ignore = root / ".gitignore"
    lines = ignore.read_text(encoding="utf-8").splitlines() if ignore.exists() else []
    if any(l.strip().strip("/") == entry for l in lines):
        return
    prefix = "" if not lines or ignore.read_text(encoding="utf-8").endswith("\n") else "\n"
    with ignore.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"{prefix}{entry}/\n")
    print(f"board.py: added {entry}/ to {ignore}")


def open_board(path):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except Exception as exc:  # no desktop session: the printed path is enough
        print(f"board.py: could not open the board ({exc}); open the path above by hand.")


def finish(board_dir, data, args):
    save(board_dir, data)
    ensure_ignored(board_dir)
    out = board_dir / "directions.html"
    out.write_text(render(board_dir, data, args.inline), encoding="utf-8")
    path = out.resolve()
    print(f"board.py: {len(data['rounds'])} round(s) on the board")
    print(path)
    print(path.as_uri())
    if not args.no_open:
        open_board(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("command", choices=["add", "build", "choose"])
    ap.add_argument("dir")
    ap.add_argument("args", nargs="*")
    ap.add_argument("--note", default="")
    ap.add_argument("--no-open", action="store_true")
    ap.add_argument("--inline", action="store_true")
    a = ap.parse_args()
    board_dir = Path(a.dir)
    data = load(board_dir)
    if a.command == "add":
        if len(a.args) != 1:
            fail("add takes the board folder and one round file.")
        raw = json.loads(Path(a.args[0]).read_text(encoding="utf-8"))
        data["rounds"].append(normalise_round(board_dir, data, raw))
    elif a.command == "choose":
        if len(a.args) != 2 or not a.args[0].isdigit():
            fail("choose takes the board folder, a round number and the direction ids (comma separated).")
        rnd = next((r for r in data["rounds"] if r["id"] == int(a.args[0])), None)
        if rnd is None:
            fail(f"there is no round {a.args[0]}.")
        ids = [i.strip() for i in a.args[1].split(",") if i.strip()]
        known = {d["id"] for d in rnd["directions"]}
        if not ids or any(i not in known for i in ids):
            fail(f"round {rnd['id']} has direction ids: {', '.join(sorted(known))}.")
        rnd["chosen"], rnd["choice_note"] = ids, a.note.strip()
    elif a.args:
        fail("build takes only the board folder.")
    finish(board_dir, data, a)


if __name__ == "__main__":
    main()
