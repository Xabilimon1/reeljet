"""Build ffmpeg argv lists. Pure string building -> unit-testable, no exec."""
from __future__ import annotations
import os


def escape_subtitles_path(path):
    """Escape a path for use inside the libavfilter `subtitles=` argument.

    Inside a filtergraph `:` separates options, `,` separates filters, and
    `\\'[]` are special. Campaign paths can contain spaces or `:` (e.g. an app
    named "Lince: Data"), which would otherwise break the filter at render time.
    """
    for ch in ("\\", ":", "'", ",", "[", "]"):
        path = path.replace(ch, "\\" + ch)
    return path


def build_frames_cmd(video, out_dir, threshold=0.4):
    pattern = os.path.join(out_dir, "frame_%03d.png")
    vf = f"select='gt(scene,{threshold})',showinfo"
    return ["ffmpeg", "-y", "-i", video, "-vf", vf, "-vsync", "vfr", pattern]


def build_master_cmd(concat_list, music, ass_path, out_path, fps=30):
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list]
    if music:
        cmd += ["-i", music]
    cmd += ["-vf", f"subtitles={escape_subtitles_path(ass_path)}", "-r", str(fps),
            "-c:v", "libx264", "-pix_fmt", "yuv420p"]
    if music:
        cmd += ["-c:a", "aac", "-b:a", "192k",
                "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                "-map", "0:v", "-map", "1:a", "-shortest"]
    cmd += [out_path]
    return cmd


def build_reframe_cmd(src, out_path, w=1080, h=1920):
    fc = (
        f"[0:v]scale={w}:{h}:force_original_aspect_ratio=increase,"
        f"crop={w}:{h},boxblur=20:5[bg];"
        f"[0:v]scale={w}:-2[fg];"
        f"[bg][fg]overlay=(W-w)/2:(H-h)/2[v]"
    )
    return ["ffmpeg", "-y", "-i", src, "-filter_complex", fc,
            "-map", "[v]", "-map", "0:a?",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", out_path]
