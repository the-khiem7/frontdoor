"""The design board of one repository: pages (one per use case), each with its own numbered rounds of variants.

Layout under <repo>/.frontdoor/board/ (ignored by git):

    board.json                the record of every page, round and choice
    board-data.js             the same record as a script, because a page opened from file:// cannot fetch JSON
    index.html                the board page, copied from the core's assets on every write
    <page>/round-<n>/round.json   the text of one round, edited by the agent before `fd round add`
    <page>/round-<n>/<id>/        one folder per variant (a, b, c ...), holding its sources and renders

Every path stored in board.json is relative to the board folder, so the folder can be moved or sent as a whole.
"""

import datetime
import json
import re
import shutil
import string
from pathlib import Path

from . import FdError
from .paths import ASSETS

SCHEMA = 1
SLUG = re.compile(r"[a-z0-9][a-z0-9-]{0,39}")
VARIANT_ID = re.compile(r"[A-Z0-9]{1,8}")
IMAGE_EXT = (".webp", ".png", ".jpg", ".jpeg", ".gif")
TEXT_FIELDS = ("title", "concept", "strengths", "risks", "flaws")
MAX_COUNT = 12


def today():
    return datetime.date.today().isoformat()


def text(value):
    return value.strip() if isinstance(value, str) else ""


def rel(board, path):
    return Path(path).resolve().relative_to(Path(board).resolve()).as_posix()


def inside(board, base, value):
    """Resolve value (relative to base) and require it to exist inside the board folder."""
    target = (Path(base) / value).resolve()
    try:
        target.relative_to(Path(board).resolve())
    except ValueError:
        raise FdError(f"{value} points outside the board folder {board}.") from None
    if not target.is_file():
        raise FdError(f"{value} does not exist under {base}.")
    return target


class Board:
    def __init__(self, folder, project=None):
        self.dir = Path(folder)
        self.file = self.dir / "board.json"
        if self.file.exists():
            try:
                self.data = json.loads(self.file.read_text(encoding="utf-8"))
            except ValueError as e:
                raise FdError(f"{self.file} is not valid JSON ({e}); fix it by hand, then run `fd board build`.") from None
            if not isinstance(self.data.get("pages"), list):
                raise FdError(f"{self.file} has no pages list.")
        else:
            self.data = {"schema": SCHEMA, "project": project or self.dir.resolve().parent.parent.name, "pages": []}

    # ---- lookup ----

    def page(self, slug):
        for p in self.data["pages"]:
            if p["slug"] == slug:
                return p
        known = ", ".join(p["slug"] for p in self.data["pages"]) or "none yet"
        raise FdError(f"there is no page {slug} (pages: {known}); create it with `fd page add {slug}`.")

    def round(self, slug, n=None, draft_first=False):
        page = self.page(slug)
        rounds = page["rounds"]
        if not rounds:
            raise FdError(f"page {slug} has no round yet; start one with `fd round new {slug} --count N`.")
        if n is None:
            drafts = [r for r in rounds if r["status"] == "draft"]
            return (drafts or rounds)[-1] if draft_first else rounds[-1]
        for r in rounds:
            if r["n"] == n:
                return r
        raise FdError(f"page {slug} has no round {n} (rounds: {', '.join(str(r['n']) for r in rounds)}).")

    def round_dir(self, slug, n):
        return self.dir / slug / f"round-{n}"

    # ---- commands ----

    def add_page(self, slug, title=""):
        if not SLUG.fullmatch(slug):
            raise FdError(f"page name {slug!r} must be lowercase letters, digits and hyphens, 1 to 40 characters, starting with a letter or digit.", 2)
        if any(p["slug"] == slug for p in self.data["pages"]):
            raise FdError(f"page {slug} already exists.")
        page = {"slug": slug, "title": text(title) or slug, "created": today(), "rounds": []}
        self.data["pages"].append(page)
        return page

    def new_round(self, slug, count, title="", note="", seed=None):
        page = self.page(slug)
        if not 1 <= count <= MAX_COUNT:
            raise FdError(f"--count must be 1 to {MAX_COUNT}.", 2)
        n = max([r["n"] for r in page["rounds"]] or [0]) + 1
        folder = self.round_dir(slug, n)
        if folder.exists():
            raise FdError(f"{folder} already exists but is not on the board; move it away or delete it first.")
        seed_path = Path(seed).resolve() if seed else None
        if seed_path and not seed_path.is_file():
            raise FdError(f"the seed file {seed} does not exist.")
        ids = list(string.ascii_uppercase[:count])
        for vid in ids:
            (folder / vid.lower()).mkdir(parents=True)
            if seed_path:
                shutil.copy2(seed_path, folder / vid.lower() / seed_path.name)
        draft = {
            "title": text(title), "note": text(note), "compare": False,
            "variants": [{"id": vid, "title": "", "concept": "", "strengths": "", "risks": "", "flaws": ""} for vid in ids],
        }
        (folder / "round.json").write_text(json.dumps(draft, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        rnd = {"n": n, "status": "draft", "created": today(), "title": text(title), "note": text(note), "compare": False,
               "variants": [{"id": vid} for vid in ids], "choice": {"chosen": [], "note": ""}}
        page["rounds"].append(rnd)
        return rnd, folder

    def publish_round(self, slug, n=None):
        rnd = self.round(slug, n, draft_first=True)
        folder = self.round_dir(slug, rnd["n"])
        spec_file = folder / "round.json"
        if not spec_file.is_file():
            raise FdError(f"{spec_file} is missing; it holds the text of the round.")
        try:
            spec = json.loads(spec_file.read_text(encoding="utf-8"))
        except ValueError as e:
            raise FdError(f"{spec_file} is not valid JSON: {e}") from None
        raw = spec.get("variants")
        if not isinstance(raw, list) or not raw:
            raise FdError(f"{spec_file} needs a non-empty variants list.")
        variants, seen, problems = [], set(), []
        for v in raw:
            vid = text(str(v.get("id", ""))).upper()
            if not VARIANT_ID.fullmatch(vid) or vid in seen:
                raise FdError(f"variant id {v.get('id')!r} in {spec_file} is empty, repeated or not letters and digits.")
            seen.add(vid)
            vdir = folder / vid.lower()
            entry = {f: text(v.get(f)) for f in TEXT_FIELDS}
            entry["id"] = vid
            entry["notes"] = text(v.get("notes"))
            entry["images"] = self._images(vdir, v)
            entry["links"] = self._links(vdir, v)
            if not entry["title"]:
                problems.append(f"{vid}: no title")
            if not entry["images"] and not entry["links"]:
                problems.append(f"{vid}: no image found in {vdir.name}/out/ or {vdir.name}/, and no index.html or links")
            variants.append(entry)
        if problems:
            raise FdError(f"round {rnd['n']} of {slug} is not ready: " + "; ".join(problems))
        rnd.update({"status": "published", "published": today(), "title": text(spec.get("title")), "note": text(spec.get("note")),
                    "compare": bool(spec.get("compare")), "variants": variants})
        known = {v["id"] for v in variants}
        rnd["choice"]["chosen"] = [c for c in rnd["choice"]["chosen"] if c in known]
        return rnd

    def _images(self, vdir, v):
        if "images" in v:
            out = []
            for img in v["images"] or []:
                entry = {"label": text(img.get("label"))}
                for theme in ("light", "dark"):
                    if img.get(theme):
                        entry[theme] = rel(self.dir, inside(self.dir, vdir, img[theme]))
                if "light" not in entry and "dark" not in entry:
                    raise FdError(f"an image of variant {vdir.name.upper()} has neither a light nor a dark file.")
                out.append(entry)
            return out
        scan = vdir / "out" if (vdir / "out").is_dir() else vdir
        if not scan.is_dir():
            return []
        return [{k: (rel(self.dir, p) if isinstance(p, Path) else p) for k, p in g.items()}
                for g in pair_images(sorted(f for f in scan.iterdir() if f.is_file() and f.suffix.lower() in IMAGE_EXT))]

    def _links(self, vdir, v):
        if "links" in v:
            return [{"label": text(link.get("label")) or link["file"], "file": rel(self.dir, inside(self.dir, vdir, link["file"]))}
                    for link in v["links"] or []]
        page = vdir / "index.html"
        return [{"label": "Open the page", "file": rel(self.dir, page)}] if page.is_file() else []

    def choose(self, slug, n, ids, note=""):
        rnd = self.round(slug, n)
        if rnd["status"] != "published":
            raise FdError(f"round {rnd['n']} of {slug} is still a draft; publish it with `fd round add {slug}` first.")
        known = [v["id"] for v in rnd["variants"]]
        picked = [i.strip().upper() for i in ids.split(",") if i.strip()]
        if not picked or any(i not in known for i in picked):
            raise FdError(f"round {rnd['n']} of {slug} has variants {', '.join(known)}.")
        rnd["choice"] = {"chosen": picked, "note": text(note), "date": today()}
        return rnd

    def status(self, slug=None):
        pages = [self.page(slug)] if slug else self.data["pages"]
        out = []
        for p in pages:
            last = p["rounds"][-1] if p["rounds"] else None
            out.append({
                "slug": p["slug"], "title": p["title"], "rounds": len(p["rounds"]),
                "drafts": [r["n"] for r in p["rounds"] if r["status"] == "draft"],
                "latest": None if last is None else {
                    "n": last["n"], "status": last["status"], "title": last["title"],
                    "variants": [v["id"] for v in last["variants"]],
                    "chosen": last["choice"]["chosen"], "choice_note": last["choice"]["note"],
                    "folder": rel(self.dir, self.round_dir(p["slug"], last["n"])) if self.round_dir(p["slug"], last["n"]).exists() else None,
                },
            })
        return {"board": str((self.dir / "index.html").resolve()), "project": self.data.get("project"), "pages": out}

    # ---- writing ----

    def save(self):
        self.dir.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(self.data, indent=2, ensure_ascii=False) + "\n"
        tmp = self.file.with_name("board.json.tmp")
        tmp.write_text(payload, encoding="utf-8")
        tmp.replace(self.file)
        self.build()

    def build(self):
        self.dir.mkdir(parents=True, exist_ok=True)
        script = "window.FD_BOARD = " + json.dumps(self.data, ensure_ascii=False).replace("</", "<\\/") + ";\n"
        (self.dir / "board-data.js").write_text(script, encoding="utf-8")
        shutil.copyfile(ASSETS / "board.html", self.dir / "index.html")
        return self.dir / "index.html"


def pair_images(files):
    """Group rendered files into one entry per picture: <name>.ext or <name>-light.ext is light, <name>-dark.ext is dark.
    A .draft before the extension (an animate.py preview) is kept apart and labelled as a draft."""
    groups = {}
    for f in files:
        stem, draft = f.stem, False
        if stem.endswith(".draft"):
            stem, draft = stem[: -len(".draft")], True
        theme = "light"
        if stem.endswith("-dark"):
            stem, theme = stem[: -len("-dark")], "dark"
        elif stem.endswith("-light"):
            stem = stem[: -len("-light")]
        label = stem + (" (draft)" if draft else "")
        groups.setdefault(label, {"label": label})[theme] = f
    return list(groups.values())
