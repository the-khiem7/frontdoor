"""The board page (frontdoor-core/assets/board.html) driven in the installed Edge or Chrome from file://, as a user opens it."""

import json

import pytest
from PIL import Image

pytestmark = pytest.mark.browser

ROUND = ".frontdoor/board/{page}/round-{n}"


def picture(path, colour, size=(400, 900)):
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", size, colour).save(path, "WEBP")


@pytest.fixture
def built(repo, fd):
    """A board with a long-picture round that allows comparison, a second page with two rounds, and a draft."""
    fd("page", "add", "settings", "--title", "Settings window")
    fd("round", "new", "settings", "--count", "3", "--title", "Three layouts")
    folder = repo / ROUND.format(page="settings", n=1)
    for v, (light, dark) in zip("abc", [("#eeeeee", "#111111"), ("#ffeedd", "#221100"), ("#ddeeff", "#001122")]):
        picture(folder / v / "out" / "settings-light.webp", light, (520, 1900))
        picture(folder / v / "out" / "settings-dark.webp", dark, (520, 1900))
    spec = {"title": "Three layouts", "note": "", "compare": True,
            "variants": [{"id": v, "title": f"Layout {v}", "concept": "c", "risks": "r"} for v in "ABC"]}
    (folder / "round.json").write_text(json.dumps(spec), encoding="utf-8")
    fd("round", "add", "settings")
    fd("page", "add", "icons")
    for n in (1, 2):
        fd("round", "new", "icons", "--count", "2")
        f = repo / ROUND.format(page="icons", n=n)
        for v in "ab":
            picture(f / v / "out" / "mark.webp", "#88aa88", (300, 300))
        (f / "round.json").write_text(json.dumps({"title": f"Marks {n}", "variants": [{"id": v, "title": v} for v in "AB"]}), encoding="utf-8")
        fd("round", "add", "icons")
    fd("choose", "icons", "1", "B")
    fd("round", "new", "icons", "--count", "2")
    return (repo / ".frontdoor" / "board" / "index.html").resolve().as_uri()


@pytest.fixture
def page():
    from fdlib.render import launch
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = launch(p)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        ctx.grant_permissions(["clipboard-read", "clipboard-write"])
        pg = ctx.new_page()
        pg.errors = []
        pg.on("pageerror", lambda e: pg.errors.append(str(e)))
        pg.on("console", lambda m: m.type == "error" and pg.errors.append(m.text))
        yield pg
        browser.close()


def test_board_shows_rounds_pictures_and_states(built, page):
    page.goto(built + "#/settings/1")
    page.wait_for_load_state("networkidle")
    assert page.locator(".card").count() == 3
    imgs = page.locator(".card .stack img.base")
    assert imgs.count() == 3 and all(page.evaluate("(i) => i.complete && i.naturalWidth > 0", imgs.nth(k).element_handle()) for k in range(3))
    assert page.locator(".card .stack").first.bounding_box()["height"] < 900, "a long picture must fit inside its card"
    assert page.locator(".toc").bounding_box()["width"] < 60, "the table of contents starts collapsed"
    page.keyboard.press("d")
    assert page.locator(".card .stack").first.get_attribute("data-mode") == "dark"
    page.goto(built + "#/icons/3")
    assert "draft" in page.inner_text("main").lower() and page.locator("#dock").is_hidden()
    assert page.errors == []


def test_keys_deep_links_and_the_viewer(built, page):
    page.goto(built + "#/settings/1/B")
    page.wait_for_load_state("networkidle")
    assert page.locator(".card.current").get_attribute("data-id") == "B"
    page.keyboard.press("ArrowRight")
    assert page.evaluate("location.hash") == "#/settings/1/C"
    page.keyboard.press("Enter")
    assert page.locator("#viewer").is_visible() and page.evaluate("location.hash") == "#/settings/1/C/view/1"
    page.keyboard.press("ArrowLeft")
    assert page.inner_text("#v-id") == "B"
    page.keyboard.press("Escape")
    page.wait_for_function("location.hash === '#/settings/1/B'", timeout=3000)
    page.keyboard.press("c")
    assert page.evaluate("location.hash").startswith("#/settings/1/compare/")
    page.keyboard.press("Escape")
    page.keyboard.press("}")
    assert page.evaluate("location.hash").startswith("#/icons/")
    page.goto(built + "#/icons/1")
    assert page.locator("#compare").is_hidden(), "comparison is off unless the round allows it"
    page.keyboard.press("]")
    assert page.evaluate("location.hash").startswith("#/icons/2")
    page.go_back()
    assert page.evaluate("location.hash").startswith("#/icons/1")
    assert page.errors == []


def test_copy_choice_gives_text_fd_choose_reads(built, page, repo, fd, board):
    page.goto(built + "#/settings/1")
    page.wait_for_load_state("networkidle")
    page.keyboard.press("2")
    page.keyboard.press("p")
    page.locator(".card").nth(2).locator(".vnote").fill("keep the gauge")
    page.fill("#round-note", "B with the bands of C")
    page.click("#copy")
    page.wait_for_function("document.getElementById('copy-status').textContent.length > 0")
    text = page.evaluate("navigator.clipboard.readText()")
    assert "Chosen: B Layout B" in text
    (repo / "pasted.txt").write_text(text, encoding="utf-8")
    assert fd("choose", "--from", str(repo / "pasted.txt"))[0] == 0
    choice = board()["pages"][0]["rounds"][0]["choice"]
    assert choice["chosen"] == ["B"] and choice["note"] == "B with the bands of C" and choice["notes"] == {"C": "keep the gauge"}
    page.reload()
    assert page.locator(".card.picked").get_attribute("data-id") == "B" and page.inner_text("#picked").split() == ["Picked", "B"]
    assert "chosen in the record" in page.locator(".card.picked").get_attribute("aria-label")
    assert page.errors == []


def test_layout_one_variant_per_row_floating_dock_and_fact_icons(built, page):
    page.goto(built + "#/settings/1")
    page.wait_for_load_state("networkidle")
    cards = page.locator(".card")
    a, b = cards.nth(0).bounding_box(), cards.nth(1).bounding_box()
    assert b["y"] > a["y"] + a["height"] - 1, "one variant per row by default"
    head, pics = cards.nth(0).locator(".card-head").bounding_box(), cards.nth(0).locator(".pics").bounding_box()
    assert pics["x"] > head["x"] + head["width"], "the text stands beside the pictures"
    tabs, top = page.locator("#tabs").bounding_box(), page.locator(".bar-top").bounding_box()
    assert tabs["y"] >= top["y"] + top["height"] - 1 and tabs["x"] < 80, "the rounds sit in a row of their own"
    title = page.locator("#page-title").bounding_box()
    assert abs(title["x"] + title["width"] / 2 - (top["x"] + top["width"] / 2)) < 4, "the page title is centred"
    assert page.inner_text(".brand").strip() == "Frontdoor Design Board"
    assert page.evaluate("getComputedStyle(document.getElementById('dock')).backgroundColor") == "rgba(0, 0, 0, 0)"
    assert page.locator(".round-head .meta").count() == 0 and page.locator(".chosen-tag").count() == 0
    dt = cards.nth(0).locator(".facts dt").first
    assert dt.locator("svg").count() == 1 and dt.get_attribute("data-tip") == "Risks" and dt.inner_text().strip() == "Risks"
    page.click('#cols button[data-cols="3"]')
    a, b = cards.nth(0).bounding_box(), cards.nth(1).bounding_box()
    assert abs(a["y"] - b["y"]) < 2, "three per row on request"
    page.reload()
    page.wait_for_load_state("networkidle")
    assert page.locator(".variants").get_attribute("data-cols") == "3", "the choice of columns is remembered"
    assert page.errors == []
