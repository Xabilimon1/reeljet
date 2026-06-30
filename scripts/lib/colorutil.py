"""Pure color helpers (no Pillow dependency)."""
from __future__ import annotations


def rgb_to_hex(rgb):
    r, g, b = (int(max(0, min(255, round(c)))) for c in rgb)
    return "#{:02X}{:02X}{:02X}".format(r, g, b)


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def relative_luminance(rgb):
    def chan(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def pick_text_color(bg_rgb):
    return "#000000" if relative_luminance(bg_rgb) > 0.179 else "#FFFFFF"


def saturation(rgb):
    r, g, b = rgb
    mx, mn = max(r, g, b), min(r, g, b)
    return 0.0 if mx == 0 else (mx - mn) / mx
