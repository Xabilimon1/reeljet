from scripts.lib.captions import format_ts, build_ass

PAL = {"caption_fill": "#0AC828", "caption_outline": "#000000"}
SHOTS = [
    {"id": "s01", "duration": 2.0, "caption": "Meet Numo"},
    {"id": "s02", "duration": 3.0, "caption": "Ship faster"},
    {"id": "s03", "duration": 1.5},  # no caption
]


def test_format_ts():
    assert format_ts(2.0) == "0:00:02.00"
    assert format_ts(65.25) == "0:01:05.25"


def test_build_ass_timings_and_text():
    ass = build_ass(SHOTS, PAL, 1920, 1080)
    assert "Dialogue: 0,0:00:00.00,0:00:02.00,Kinetic,,0,0,0,,Meet Numo" in ass
    assert "0:00:02.00,0:00:05.00,Kinetic,,0,0,0,,Ship faster" in ass


def test_build_ass_skips_missing_caption():
    ass = build_ass(SHOTS, PAL, 1920, 1080)
    assert ass.count("Dialogue:") == 2


def test_palette_color_in_style():
    ass = build_ass(SHOTS, PAL, 1920, 1080)
    # #0AC828 -> ASS &H0028C80A (BBGGRR)
    assert "&H0028C80A" in ass
