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
    assert page.inner_text(".bar-top .brand").strip() == "Frontdoor Design Board"
    assert "FD Fraunces" in page.evaluate("getComputedStyle(document.getElementById('page-title')).fontFamily")
    assert page.evaluate("getComputedStyle(document.getElementById('tabs')).backgroundColor") == "rgba(0, 0, 0, 0)"
    assert " ".join(page.inner_text("#tab-1 .tn").split()) == "Round 1" and page.locator("#tab-vars button").count() == 3
    page.click("#tab-vars button >> nth=2")
    assert page.locator(".card.current").get_attribute("data-id") == "C" and page.locator("#tab-vars button").nth(2).get_attribute("aria-current") == "true"
    assert page.locator(".card .pic-index").first.is_visible() and page.locator(".card .pic-bar").first.is_hidden(), "picture bars sit in the side column"
    assert page.locator("#toc #help").count() == 1, "the shortcuts button sits in the rail"
    assert page.evaluate("getComputedStyle(document.getElementById('dock')).backgroundColor") == "rgba(0, 0, 0, 0)"
    assert page.locator(".round-head .meta").count() == 0 and page.locator(".chosen-tag").count() == 0
    dt = cards.nth(0).locator(".facts dt").first
    assert dt.locator("svg").count() == 1 and dt.get_attribute("data-tip") == "Risks" and dt.inner_text().strip() == "Risks"
    page.click('#cols button[data-cols="3"]')
    a, b = cards.nth(0).bounding_box(), cards.nth(1).bounding_box()
    assert abs(a["y"] - b["y"]) < 2, "three per row on request"
    assert page.locator(".card .pic-bar").first.is_visible() and page.locator(".card .pic-index").first.is_hidden()
    page.reload()
    page.wait_for_load_state("networkidle")
    assert page.locator(".variants").get_attribute("data-cols") == "3", "the choice of columns is remembered"
    assert page.errors == []


SETTLED = "await Promise.all(document.getAnimations().map((a) => a.finished.catch(() => null)));"


def test_motion_pick_button_widens_and_shrinks(built, page):
    page.goto(built + "#/settings/1")
    page.wait_for_load_state("networkidle")
    page.evaluate(f"(async () => {{ {SETTLED} }})()")
    probe = """async () => {
      const b = document.querySelector('.card[data-id="B"] .pick'); const w = () => b.getBoundingClientRect().width;
      const w0 = w(); b.click(); await new Promise((r) => setTimeout(r, 110)); const mid = w(); const live = document.getAnimations().length;
      @S const end = w(); b.click(); await new Promise((r) => setTimeout(r, 110)); const back = w(); @S
      return { w0, mid, end, live, back, back2: w(), text: b.innerText.replace(/\\s+/g, '') };
    }""".replace("@S", SETTLED)
    r = page.evaluate(probe)
    assert r["w0"] < r["mid"] < r["end"], r
    assert r["live"] > 0 and r["end"] - r["w0"] > 20, "Pick grows into [check] Picked"
    assert r["back"] < r["end"] and abs(r["back2"] - r["w0"]) < 1, "and shrinks back when unpicked"
    page.emulate_media(reduced_motion="reduce")
    r = page.evaluate("""() => { const b = document.querySelector('.card[data-id="B"] .pick'); b.click(); const w = b.getBoundingClientRect().width;
      return { w, live: document.getAnimations().filter((a) => a.effect && a.effect.target === b).length }; }""")
    assert r["live"] == 0 and r["w"] > 80, "with reduced motion the button changes at once"
    assert page.errors == []


def test_motion_round_tabs_stay_in_the_dom_and_open_and_close(built, page):
    page.goto(built + "#/icons/1")
    page.wait_for_load_state("networkidle")
    page.evaluate(f"(async () => {{ {SETTLED} }})()")
    page.evaluate("document.getElementById('tab-1').dataset.mark = 'x'")
    g1, g2 = '.tab-group[data-n="1"]', '.tab-group[data-n="2"]'
    assert page.locator(f"{g1} .tab-vars button").first.is_visible() and page.locator(f"{g2} .tab-vars button").first.is_hidden()
    probe = """async () => {
      const w = (s) => document.querySelector(s).getBoundingClientRect().width;
      const a0 = w('@1'), b0 = w('@2'); document.getElementById('tab-2').click(); await new Promise((r) => setTimeout(r, 110));
      const a1 = w('@1'), b1 = w('@2'); @S
      return { a0, b0, a1, b1, a2: w('@1'), b2: w('@2') };
    }""".replace("@1", g1).replace("@2", g2).replace("@S", SETTLED)
    r = page.evaluate(probe)
    assert r["b0"] < r["b1"] < r["b2"], r
    assert r["a0"] > r["a1"] > r["a2"], r
    assert page.get_attribute("#tab-1", "data-mark") == "x", "the tab is the same element, so it can animate"
    assert page.locator(f"{g1} .tab-vars button").first.is_hidden() and page.locator(f"{g2} .tab-vars button").first.is_visible()
    assert page.locator("#tab-vars").count() == 1 and page.locator(f"{g2} #tab-vars").count() == 1
    page.goto(built + "#/settings/1")
    page.wait_for_load_state("networkidle")
    assert page.get_attribute("#tab-1", "data-mark") is None, "another page gets its own tabs"
    page.set_viewport_size({"width": 390, "height": 800})
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert page.errors == []


def test_motion_content_pictures_and_dialogs(built, page):
    page.goto(built + "#/icons/1")
    page.wait_for_load_state("networkidle")
    names = page.evaluate("""() => { document.getElementById('tab-2').click();
      return document.getAnimations().map((a) => a.effect.target.className).filter((c) => /card|round-head/.test(c)); }""")
    assert len(names) >= 2, "a round switch settles the header and the cards in"
    names = page.evaluate("""() => { document.querySelector('#cols button[data-cols="2"]').click();
      return document.getAnimations().filter((a) => a.effect.target.classList.contains('card')).length; }""")
    assert names >= 2, "a change of columns settles the cards in"
    page.goto(built + "#/settings/1")
    page.wait_for_load_state("networkidle")
    page.evaluate(f"(async () => {{ {SETTLED} }})()")
    r = page.evaluate("""async () => {
      const over = document.querySelector('.stack img.over'), base = document.querySelector('.stack img.base');
      document.querySelector('#theme-all [data-mode="dark"]').click(); await new Promise((r) => setTimeout(r, 120));
      const mid = +getComputedStyle(over).opacity; @S const end = +getComputedStyle(over).opacity; const hidden = getComputedStyle(base).visibility;
      document.querySelector('#theme-all [data-mode="light"]').click();
      return { mid, end, hidden, back: getComputedStyle(base).visibility };
    }""".replace("@S", SETTLED))
    assert 0 < r["mid"] < 1 and r["end"] == 1 and r["hidden"] == "hidden" and r["back"] == "visible", r
    page.keyboard.press("?")
    page.wait_for_function("document.getElementById('keys-sheet').open")
    page.evaluate(f"(async () => {{ {SETTLED} }})()")
    assert page.evaluate("getComputedStyle(document.getElementById('keys-sheet')).opacity") == "1"
    page.click("#keys-sheet [data-close]")
    assert page.evaluate("!document.getElementById('keys-sheet').open && getComputedStyle(document.getElementById('keys-sheet')).display") == "block", "it fades out first"
    page.wait_for_function("getComputedStyle(document.getElementById('keys-sheet')).display === 'none'")
    assert page.errors == []
