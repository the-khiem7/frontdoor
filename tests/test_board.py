import json

import pytest

ROUND = ".frontdoor/board/{page}/round-{n}"


def write(path, data=b"x"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def fill(repo, page, n, variants, **extra):
    """Write round.json with a title per variant."""
    spec = {"title": "t", "note": "", "variants": [{"id": v, "title": f"Variant {v}", **extra.get(v, {})} for v in variants]}
    (repo / ROUND.format(page=page, n=n) / "round.json").write_text(json.dumps(spec), encoding="utf-8")


def test_page_add_writes_board_and_ignores_frontdoor(repo, fd, board):
    code, _, err = fd("page", "add", "readme", "--title", "README")
    assert code == 0
    assert board()["pages"][0] == {**board()["pages"][0], "slug": "readme", "title": "README", "rounds": []}
    for name in ("board.json", "board-data.js", "index.html"):
        assert (repo / ".frontdoor" / "board" / name).is_file()
    assert ".frontdoor/" in (repo / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert "added .frontdoor/" in err


@pytest.mark.parametrize("slug", ["Readme", "_x", "a b", "x" * 41, ""])
def test_page_add_rejects_bad_slug(fd, slug):
    assert fd("page", "add", slug)[0] == 2


def test_page_add_twice_fails(fd):
    fd("page", "add", "icons")
    code, _, err = fd("page", "add", "icons")
    assert code == 1 and "already exists" in err


def test_round_new_requires_count(fd):
    fd("page", "add", "icons")
    with pytest.raises(SystemExit) as e:
        fd("round", "new", "icons")
    assert e.value.code == 2


@pytest.mark.parametrize("count", [0, 13])
def test_round_new_rejects_count_out_of_range(fd, count):
    fd("page", "add", "icons")
    assert fd("round", "new", "icons", "--count", count)[0] == 2


def test_round_new_on_missing_page_names_the_fix(fd):
    code, _, err = fd("round", "new", "icons", "--count", "2")
    assert code == 1 and "fd page add icons" in err


def test_rounds_are_numbered_per_page(repo, fd, board):
    fd("page", "add", "readme")
    fd("page", "add", "icons")
    for _ in range(3):
        fd("round", "new", "readme", "--count", "2")
    code, out, _ = fd("round", "new", "icons", "--count", "3")
    assert code == 0 and "round 1 of icons" in out
    pages = {p["slug"]: p for p in board()["pages"]}
    assert [r["n"] for r in pages["readme"]["rounds"]] == [1, 2, 3]
    assert [r["n"] for r in pages["icons"]["rounds"]] == [1]


def test_round_new_makes_a_folder_per_variant_and_a_round_file(repo, fd):
    fd("page", "add", "icons")
    fd("round", "new", "icons", "--count", "3", "--title", "First marks")
    folder = repo / ROUND.format(page="icons", n=1)
    assert sorted(p.name for p in folder.iterdir()) == ["a", "b", "c", "round.json"]
    spec = json.loads((folder / "round.json").read_text(encoding="utf-8"))
    assert spec["title"] == "First marks" and spec["compare"] is False
    assert [v["id"] for v in spec["variants"]] == ["A", "B", "C"]


def test_round_new_copies_the_seed_into_every_variant(repo, fd, tmp_path):
    seed = write(tmp_path / "seed" / "page.html", b"<html></html>")
    fd("page", "add", "nav")
    fd("round", "new", "nav", "--count", "2", "--seed", seed)
    for v in "ab":
        assert (repo / ROUND.format(page="nav", n=1) / v / "page.html").read_bytes() == b"<html></html>"


def test_round_add_lists_what_is_missing(fd):
    fd("page", "add", "icons")
    fd("round", "new", "icons", "--count", "2")
    code, _, err = fd("round", "add", "icons")
    assert code == 1
    assert "A: no title" in err and "B: no image found" in err


def test_round_add_pairs_light_and_dark_by_file_name(repo, fd, board):
    fd("page", "add", "readme")
    fd("round", "new", "readme", "--count", "1")
    out = repo / ROUND.format(page="readme", n=1) / "a" / "out"
    for name in ("hero.webp", "hero-dark.webp", "mark-light.png", "mark-dark.png", "banner.draft.webp", "banner-dark.draft.webp", "notes.txt"):
        write(out / name)
    fill(repo, "readme", 1, "A")
    assert fd("round", "add", "readme")[0] == 0
    images = {i["label"]: i for i in board()["pages"][0]["rounds"][0]["variants"][0]["images"]}
    assert set(images) == {"hero", "mark", "banner (draft)"}
    assert images["hero"]["light"] == "readme/round-1/a/out/hero.webp"
    assert images["hero"]["dark"] == "readme/round-1/a/out/hero-dark.webp"
    assert images["mark"]["light"].endswith("mark-light.png") and images["banner (draft)"]["dark"].endswith("banner-dark.draft.webp")


def test_round_add_prefers_the_out_folder(repo, fd, board):
    fd("page", "add", "readme")
    fd("round", "new", "readme", "--count", "1")
    variant = repo / ROUND.format(page="readme", n=1) / "a"
    write(variant / "logo.png")
    write(variant / "out" / "hero.webp")
    fill(repo, "readme", 1, "A")
    fd("round", "add", "readme")
    assert [i["label"] for i in board()["pages"][0]["rounds"][0]["variants"][0]["images"]] == ["hero"]


def test_round_add_links_index_html_unless_links_are_given(repo, fd, board):
    fd("page", "add", "landing-page")
    fd("round", "new", "landing-page", "--count", "2")
    folder = repo / ROUND.format(page="landing-page", n=1)
    write(folder / "a" / "index.html")
    write(folder / "b" / "index.html")
    write(folder / "b" / "out" / "shot.png")
    fill(repo, "landing-page", 1, "AB", B={"links": []})
    assert fd("round", "add", "landing-page")[0] == 0
    a, b = board()["pages"][0]["rounds"][0]["variants"]
    assert a["links"] == [{"label": "Open the page", "file": "landing-page/round-1/a/index.html"}]
    assert b["links"] == [] and b["images"][0]["label"] == "shot"


def test_round_add_refuses_a_file_outside_the_board(repo, fd):
    write(repo / "elsewhere.webp")
    fd("page", "add", "readme")
    fd("round", "new", "readme", "--count", "1")
    fill(repo, "readme", 1, "A", A={"images": [{"label": "x", "light": "../../../../../elsewhere.webp"}]})
    code, _, err = fd("round", "add", "readme")
    assert code == 1 and "outside the board" in err


def test_round_add_again_refreshes_and_keeps_the_choice(repo, fd, board):
    fd("page", "add", "readme")
    fd("round", "new", "readme", "--count", "2")
    folder = repo / ROUND.format(page="readme", n=1)
    write(folder / "a" / "out" / "hero.webp")
    write(folder / "b" / "out" / "hero.webp")
    fill(repo, "readme", 1, "AB")
    fd("round", "add", "readme")
    fd("choose", "readme", "1", "b", "--note", "B with the rail of A")
    write(folder / "b" / "out" / "hero-dark.webp")
    fd("round", "add", "readme", "1")
    rnd = board()["pages"][0]["rounds"][0]
    assert rnd["choice"]["chosen"] == ["B"] and rnd["choice"]["note"] == "B with the rail of A"
    assert "dark" in rnd["variants"][1]["images"][0]


def test_choose_rejects_unknown_ids_and_drafts(repo, fd):
    fd("page", "add", "readme")
    fd("round", "new", "readme", "--count", "2")
    code, _, err = fd("choose", "readme", "1", "A")
    assert code == 1 and "still a draft" in err
    for v in "ab":
        write(repo / ROUND.format(page="readme", n=1) / v / "out" / "hero.webp")
    fill(repo, "readme", 1, "AB")
    fd("round", "add", "readme")
    code, _, err = fd("choose", "readme", "1", "A,Z")
    assert code == 1 and "variants A, B" in err


def test_status_json_summarises_each_page(repo, fd):
    fd("page", "add", "readme")
    fd("page", "add", "icons")
    fd("round", "new", "icons", "--count", "3")
    code, out, _ = fd("status", "--json")
    info = json.loads(out)
    assert code == 0 and info["daemon"] is None
    pages = {p["slug"]: p for p in info["pages"]}
    assert pages["readme"]["latest"] is None
    assert pages["icons"]["latest"]["variants"] == ["A", "B", "C"] and pages["icons"]["drafts"] == [1]


def test_status_without_a_board_writes_nothing(repo, fd):
    code, out, _ = fd("status")
    assert code == 0 and "no page yet" in out
    assert not (repo / ".frontdoor").exists()


def test_board_data_script_holds_the_record_and_escapes_closing_tags(repo, fd):
    fd("page", "add", "readme", "--title", "</script><b>")
    script = (repo / ".frontdoor" / "board" / "board-data.js").read_text(encoding="utf-8")
    assert "</script>" not in script
    data = json.loads(script.removeprefix("window.FD_BOARD = ").rstrip().rstrip(";"))
    assert data["pages"][0]["title"] == "</script><b>"


def test_broken_board_json_is_reported_not_overwritten(repo, fd):
    fd("page", "add", "readme")
    path = repo / ".frontdoor" / "board" / "board.json"
    path.write_text("{ broken", encoding="utf-8")
    code, _, err = fd("page", "add", "icons")
    assert code == 1 and "not valid JSON" in err
    assert path.read_text(encoding="utf-8") == "{ broken"
