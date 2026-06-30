from PIL import Image
from scripts.lib.palette import extract_palette


def _solid(tmp_path, name, rgb):
    p = tmp_path / name
    Image.new("RGB", (60, 60), rgb).save(p)
    return str(p)


def test_solid_image_dominant_is_exact(tmp_path):
    img = _solid(tmp_path, "a.png", (10, 200, 40))
    pal = extract_palette([img])
    assert pal["dominant"][0] == "#0AC828"
    assert pal["accent"] == "#0AC828"


def test_caption_colors_present(tmp_path):
    img = _solid(tmp_path, "a.png", (255, 255, 255))
    pal = extract_palette([img])
    assert pal["caption_outline"] in ("#000000", "#FFFFFF")
    assert pal["caption_fill"].startswith("#")


def test_empty_raises():
    import pytest
    with pytest.raises(ValueError):
        extract_palette([])
