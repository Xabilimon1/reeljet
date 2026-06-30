from PIL import Image
from scripts.lib.caption_render import timed_captions, render_caption_png

PAL = {"caption_fill": "#0AC828", "caption_outline": "#000000"}


def test_timed_captions_accumulate_and_skip():
    shots = [
        {"duration": 2.0, "caption": "Meet Numo"},
        {"duration": 3.0},                       # no caption
        {"duration": 1.5, "caption": "Ship it"},
    ]
    assert timed_captions(shots) == [
        ("Meet Numo", 0.0, 2.0),
        ("Ship it", 5.0, 6.5),
    ]


def test_render_caption_png_is_rgba_and_has_text(tmp_path):
    out = tmp_path / "cap.png"
    render_caption_png("Hello world", 400, 200, PAL, str(out))
    im = Image.open(out)
    assert im.size == (400, 200)
    assert im.mode == "RGBA"
    # text drawn -> some fully-opaque pixels exist
    assert im.getchannel("A").getextrema()[1] == 255


def test_render_long_caption_wraps(tmp_path):
    # a long caption must still fit (wrap), producing a valid image
    out = tmp_path / "long.png"
    render_caption_png("This is a fairly long caption that needs wrapping",
                       640, 360, PAL, str(out))
    assert Image.open(out).size == (640, 360)
