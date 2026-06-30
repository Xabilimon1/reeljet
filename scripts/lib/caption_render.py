"""Render kinetic captions as transparent PNG overlays.

The installed ffmpeg may be built without libass/freetype (no `subtitles` or
`drawtext` filter), so we draw captions with Pillow and composite them with the
always-available `overlay` filter. PNGs are full master-frame size, drawn once
per captioned shot, and overlaid for that shot's time window.
"""
from __future__ import annotations
import os
from PIL import Image, ImageDraw, ImageFont
from .colorutil import hex_to_rgb

_FONT_CANDIDATES = (
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
)


def _load_font(size):
    for path in _FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def timed_captions(shots):
    """Return [(text, start, end)] for captioned shots, accumulating durations."""
    out = []
    t = 0.0
    for sh in shots:
        dur = float(sh["duration"])
        cap = sh.get("caption")
        if cap:
            out.append((str(cap), t, t + dur))
        t += dur
    return out


def _wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if not cur or draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def render_caption_png(text, width, height, palette, out_path):
    """Draw `text` centered in a bottom band on a transparent WxH PNG."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = _load_font(max(12, int(height * 0.06)))
    fill = hex_to_rgb(palette.get("caption_fill", "#FFFFFF")) + (255,)
    outline = hex_to_rgb(palette.get("caption_outline", "#000000")) + (255,)
    stroke = max(2, int(height * 0.004))
    lines = _wrap(draw, text, font, int(width * 0.86))
    ascent, descent = font.getmetrics()
    line_h = ascent + descent
    y = int(height * 0.82) - line_h * len(lines)
    for line in lines:
        x = (width - draw.textlength(line, font=font)) / 2
        draw.text((x, y), line, font=font, fill=fill,
                  stroke_width=stroke, stroke_fill=outline)
        y += line_h
    img.save(out_path)
    return out_path
