"""Build a kinetic-caption ASS subtitle file from plan shots + palette."""
from __future__ import annotations


def format_ts(seconds):
    cs = int(round(seconds * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


def _ass_color(hex_rgb):
    h = hex_rgb.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H00{b}{g}{r}".upper()


def build_ass(shots, palette, width, height):
    primary = _ass_color(palette.get("caption_fill", "#FFFFFF"))
    outline = _ass_color(palette.get("caption_outline", "#000000"))
    font_size = int(height * 0.06)
    margin_v = int(height * 0.12)
    header = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        f"PlayResX: {width}\nPlayResY: {height}\nWrapStyle: 2\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, "
        "BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, "
        "MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Kinetic,Arial,{font_size},{primary},{outline},"
        f"&H64000000,1,1,3,0,2,40,40,{margin_v},1\n\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, "
        "MarginV, Effect, Text\n"
    )
    lines = []
    t = 0.0
    for sh in shots:
        dur = float(sh["duration"])
        cap = sh.get("caption")
        if cap:
            start, end = format_ts(t), format_ts(t + dur)
            txt = str(cap).replace("\n", "\\N")
            lines.append(
                f"Dialogue: 0,{start},{end},Kinetic,,0,0,0,,{txt}")
        t += dur
    return header + "\n".join(lines) + ("\n" if lines else "")
