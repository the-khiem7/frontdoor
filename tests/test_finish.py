import io

import pytest
from fdlib.render import finish_and_save, parse_color
from PIL import Image


def png(size=(200, 120), color=(250, 245, 234, 255), mode="RGBA"):
    buf = io.BytesIO()
    Image.new(mode, size, color).save(buf, "PNG")
    return buf.getvalue()


def test_card_finish_rounds_the_corners_and_draws_the_border(tmp_path):
    dst = tmp_path / "card.webp"
    w, h, size = finish_and_save(png(), str(dst), "card", (10, 20, 30), 24, 3, 4)
    img = Image.open(dst).convert("RGBA")
    assert (w, h) == (200, 120) and size == dst.stat().st_size
    assert img.getpixel((0, 0))[3] == 0  # corner cut away
    assert img.getpixel((100, 1))[:3] == (10, 20, 30)  # border on the top edge
    assert img.getpixel((100, 60)) == (250, 245, 234, 255)  # inside untouched


def test_card_finish_takes_its_own_radius_and_border(tmp_path):
    dst = tmp_path / "card.webp"
    finish_and_save(png(), str(dst), "card", (10, 20, 30), 0, 0, 4)
    img = Image.open(dst).convert("RGBA")
    assert img.getpixel((0, 0)) == (250, 245, 234, 255)


def test_plain_finish_keeps_the_rectangle(tmp_path):
    dst = tmp_path / "plain.webp"
    finish_and_save(png(), str(dst), "plain", (10, 20, 30), 24, 3, 4)
    img = Image.open(dst)
    assert img.mode == "RGB" and img.getpixel((0, 0)) == (250, 245, 234)


def test_transparent_finish_keeps_alpha(tmp_path):
    dst = tmp_path / "icon.webp"
    finish_and_save(png(color=(0, 0, 0, 0)), str(dst), "transparent", (10, 20, 30), 24, 3, 4)
    assert Image.open(dst).convert("RGBA").getpixel((100, 60))[3] == 0


def test_social_finish_writes_an_opaque_png(tmp_path):
    dst = tmp_path / "banner-social.png"
    w, h, _ = finish_and_save(png((1280, 640)), str(dst), "social", (10, 20, 30), 24, 3, 4)
    img = Image.open(dst)
    assert (w, h) == (1280, 640) and img.format == "PNG" and img.mode == "RGB"


@pytest.mark.parametrize("method", [4, 6])
def test_lossless_encode_is_pixel_exact_at_every_method(tmp_path, method):
    src = Image.effect_noise((160, 90), 60).convert("RGB")
    buf = io.BytesIO()
    src.save(buf, "PNG")
    dst = tmp_path / f"m{method}.webp"
    finish_and_save(buf.getvalue(), str(dst), "plain", (0, 0, 0), 0, 0, method)
    assert Image.open(dst).convert("RGB").tobytes() == src.tobytes()


@pytest.mark.parametrize("value, expected", [("#0a1b2c", (10, 27, 44)), ("#abc", (170, 187, 204)), (" rgb(1, 2, 3)", (1, 2, 3)), ("nope", (9, 9, 9))])
def test_parse_color(value, expected):
    assert parse_color(value, (9, 9, 9)) == expected
