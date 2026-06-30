"""Extract a brand palette from screenshots / logo using Pillow."""
from __future__ import annotations
from collections import Counter
from PIL import Image
from .colorutil import rgb_to_hex, saturation, pick_text_color


def _image_colors(path, sample=120, colors=16):
    im = Image.open(path).convert("RGB").resize((sample, sample))
    q = im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT).convert("RGB")
    return list(q.getdata())


def extract_palette(paths, k=5):
    if not paths:
        raise ValueError("no image paths provided")
    counter = Counter()
    for p in paths:
        counter.update(_image_colors(p))
    dominant = [c for c, _ in counter.most_common(k)]
    accent_rgb = max(dominant, key=saturation)
    return {
        "dominant": [rgb_to_hex(c) for c in dominant],
        "accent": rgb_to_hex(accent_rgb),
        "text_on_dominant": pick_text_color(dominant[0]),
        "caption_fill": rgb_to_hex(accent_rgb),
        "caption_outline": pick_text_color(accent_rgb),
    }
