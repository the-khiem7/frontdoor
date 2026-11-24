"""Tests that drive the installed Edge or Chrome. Run with --browser-tests."""

import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest
from fdlib import daemon
from fdlib.render import Renderer, make_job
from PIL import Image

pytestmark = pytest.mark.browser

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<script>document.documentElement.dataset.theme = new URLSearchParams(location.search).get("theme") === "dark" ? "dark" : "light";</script>
<link rel="stylesheet" href="s.css"></head><body><div class="sheet">
<div class="item" id="card" style="width:200px;height:100px"><p>card</p></div>
<div class="item" id="flat" data-finish="plain" style="width:120px;height:60px"></div>
<div class="item" id="mark" data-finish="transparent" style="width:64px;height:64px;background:transparent">
  <svg width="64" height="64"><circle cx="32" cy="32" r="16" fill="#c00"/></svg></div>
</div></body></html>"""

CSS = """:root { --paper:#fafafa; --cardline:#102030; }
html[data-theme="dark"] { --paper:#111111; --cardline:#a0b0c0; }
html, body { margin:0; background:#888; } .sheet { width:max-content; padding:24px; display:flex; flex-direction:column; gap:16px; }
.item { position:relative; overflow:hidden; background:var(--paper); font:16px system-ui, sans-serif; }"""


@pytest.fixture
def site(tmp_path):
    root = tmp_path / "src"
    root.mkdir()
    (root / "page.html").write_text(PAGE, encoding="utf-8")
    (root / "s.css").write_text(CSS, encoding="utf-8")
    return root


@pytest.fixture(scope="module")
def renderer():
    with Renderer() as r:
        yield r


def test_render_writes_each_finish_in_both_themes(site, tmp_path, renderer):
    out = tmp_path / "out"
    lines = []
    assert renderer.render(make_job(site / "page.html", out), lines.append) == 0
    assert sorted(p.name for p in out.iterdir()) == sorted(
        ["card.webp", "card-dark.webp", "flat.webp", "flat-dark.webp", "mark.webp", "mark-dark.webp"])
    card, card_dark = Image.open(out / "card.webp").convert("RGBA"), Image.open(out / "card-dark.webp").convert("RGBA")
    assert card.size == (200, 100) and card.getpixel((0, 0))[3] == 0
    assert card.getpixel((100, 1))[:3] == (16, 32, 48) and card_dark.getpixel((100, 1))[:3] == (160, 176, 192)
    flat = Image.open(out / "flat.webp")
    assert flat.mode == "RGB" and flat.getpixel((0, 0)) == (250, 250, 250)
    mark = Image.open(out / "mark.webp").convert("RGBA")
    assert mark.getpixel((2, 2))[3] == 0 and mark.getpixel((32, 32))[:3] == (204, 0, 0)
    assert any(line.startswith("rendered in") for line in lines)


def test_render_subset_and_unknown_item(site, tmp_path, renderer):
    out = tmp_path / "out"
    assert renderer.render(make_job(site / "page.html", out, items="flat", themes="light"), lambda _: None) == 0
    assert [p.name for p in out.iterdir()] == ["flat.webp"]
    with pytest.raises(ValueError, match="no item with id nope"):
        renderer.render(make_job(site / "page.html", out, items="nope"), lambda _: None)


def test_render_refuses_an_id_used_twice(site, tmp_path, renderer):
    (site / "page.html").write_text(PAGE.replace('id="flat"', 'id="card"'), encoding="utf-8")
    with pytest.raises(ValueError, match="used twice: card"):
        renderer.render(make_job(site / "page.html", tmp_path / "out"), lambda _: None)


def test_render_warns_when_content_leaves_the_item(site, tmp_path, renderer):
    (site / "page.html").write_text(PAGE.replace("<p>card</p>", '<p style="position:absolute;left:190px;width:80px">wide</p>'),
                                    encoding="utf-8")
    lines = []
    assert renderer.render(make_job(site / "page.html", tmp_path / "out", items="card", themes="light"), lines.append) == 1
    assert any("content leaves the item box" in line for line in lines)


def test_render_counts_a_family_served_only_in_another_weight_as_loaded(site, tmp_path, renderer):
    # the family is served in two weights, 600 and 800, fetched over HTTP like a web font, and the page uses only 800;
    # a probe drawn at weight 400 matches the 600 face, which was never downloaded
    fonts = [p for d in (Path("C:/Windows/Fonts"), Path("/usr/share/fonts"), Path("/System/Library/Fonts"), Path("/Library/Fonts"))
             if d.is_dir() for p in sorted(d.rglob("*.ttf"))[:50]]
    if not fonts:
        pytest.skip("no .ttf font on this machine to serve")
    shutil.copy(fonts[0], site / "heavy-600.ttf")
    shutil.copy(fonts[0], site / "heavy-800.ttf")
    face = ''.join(f'@font-face {{ font-family: "Heavy Only"; font-weight: {w}; src: url("heavy-{w}.ttf"); }}\n' for w in (600, 800))
    (site / "s.css").write_text(face + CSS, encoding="utf-8")
    item = ('<p style="font-family:\'Heavy Only\';font-weight:800">heavy</p>'
            '<p style="font-family:\'No Such Family Xyz\'">missing</p>')
    (site / "page.html").write_text(PAGE.replace("<p>card</p>", item), encoding="utf-8")
    lines = []
    renderer.render(make_job(site / "page.html", tmp_path / "out", items="card", themes="light"), lines.append)
    warn = next(line for line in lines if line.startswith("WARN fonts requested but not loaded"))
    assert "No Such Family Xyz" in warn and "Heavy Only" not in warn
    assert "Heavy Only" in next(line for line in lines if line.startswith("fonts:"))


def test_a_long_lived_renderer_sees_an_edited_stylesheet(site, tmp_path, renderer):
    out = tmp_path / "out"
    job = make_job(site / "page.html", out, items="flat", themes="light")
    renderer.render(job, lambda _: None)
    (site / "s.css").write_text(CSS.replace("#fafafa", "#00ff00"), encoding="utf-8")
    renderer.render(job, lambda _: None)
    assert Image.open(out / "flat.webp").getpixel((0, 0)) == (0, 255, 0)


def test_daemon_renders_and_stops(repo, site, tmp_path):
    from fdlib.paths import SCRIPTS, daemon_state

    state, fresh = daemon.start(repo, SCRIPTS / "fd.py", idle=60)
    try:
        assert fresh and daemon.alive(repo)["pid"] == state["pid"]
        res = daemon.render(state, make_job(site / "page.html", tmp_path / "out", items="card", themes="light"))
        assert res["problems"] == 0 and any(line.startswith("card.webp") for line in res["lines"])
        bad = dict(state, token="0" * 32)
        with pytest.raises(OSError):
            daemon.call(bad, "/status")
    finally:
        assert daemon.stop(repo)
    assert not daemon_state(repo).exists() and daemon.alive(repo) is None


def test_watch_renders_again_after_a_change(repo, site, tmp_path):
    from fdlib.paths import SCRIPTS

    out = tmp_path / "out"
    cmd = [sys.executable, "-I", str(SCRIPTS / "fd.py"), "--repo", str(repo), "render", str(site / "page.html"),
           "--out", str(out), "--items", "flat", "--themes", "light", "--watch", "--no-daemon"]
    with open(tmp_path / "watch.log", "w", encoding="utf-8") as log:
        proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, text=True)
        try:
            deadline = time.time() + 60
            while not (out / "flat.webp").exists() and time.time() < deadline:
                time.sleep(0.2)
            first = (out / "flat.webp").stat().st_mtime_ns
            time.sleep(1.0)
            (site / "s.css").write_text(CSS.replace("#fafafa", "#0000ff"), encoding="utf-8")
            while time.time() < deadline:
                if (out / "flat.webp").stat().st_mtime_ns != first:
                    break
                time.sleep(0.2)
            time.sleep(0.5)
            assert Image.open(out / "flat.webp").getpixel((0, 0)) == (0, 0, 255)
        finally:
            proc.kill()
            proc.wait(timeout=10)
    assert "change seen" in (tmp_path / "watch.log").read_text(encoding="utf-8")
