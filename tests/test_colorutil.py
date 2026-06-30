from scripts.lib.colorutil import (
    rgb_to_hex, hex_to_rgb, relative_luminance, pick_text_color, saturation,
)


def test_rgb_to_hex():
    assert rgb_to_hex((255, 0, 0)) == "#FF0000"
    assert rgb_to_hex((10, 200, 40)) == "#0AC828"


def test_hex_to_rgb_roundtrip():
    assert hex_to_rgb("#0AC828") == (10, 200, 40)


def test_luminance_bounds():
    assert relative_luminance((0, 0, 0)) == 0.0
    assert round(relative_luminance((255, 255, 255)), 3) == 1.0


def test_pick_text_color():
    assert pick_text_color((255, 255, 255)) == "#000000"
    assert pick_text_color((0, 0, 0)) == "#FFFFFF"


def test_saturation():
    assert saturation((255, 0, 0)) == 1.0
    assert saturation((100, 100, 100)) == 0.0
