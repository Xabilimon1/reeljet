"""Build ffmpeg argv lists. Pure string building -> unit-testable, no exec.

Captions are composited via the `overlay` filter (full-frame transparent PNGs
from caption_render), not libass, so this works on ffmpeg builds without
subtitles/drawtext support.
"""
from __future__ import annotations
import os


def build_frames_cmd(video, out_dir, threshold=0.4):
    pattern = os.path.join(out_dir, "frame_%03d.png")
    vf = f"select='gt(scene,{threshold})',showinfo"
    return ["ffmpeg", "-y", "-i", video, "-vf", vf, "-vsync", "vfr", pattern]


def build_master_cmd(concat_list, music, overlays, out_path,
                     width=1920, height=1080, fps=30):
    """Concat clips, scale/pad to width x height, overlay timed caption PNGs,
    mux music at -14 LUFS.

    overlays: list of {"path": str, "start": float, "end": float}.
    """
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list]
    for ov in overlays:
        cmd += ["-i", ov["path"]]
    if music:
        cmd += ["-i", music]

    parts = [
        f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1[base]"
    ]
    cur = "base"
    for i, ov in enumerate(overlays, start=1):
        nxt = f"v{i}"
        parts.append(
            f"[{cur}][{i}:v]overlay=0:0:"
            f"enable='between(t,{ov['start']},{ov['end']})'[{nxt}]")
        cur = nxt

    cmd += ["-filter_complex", ";".join(parts), "-map", f"[{cur}]",
            "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p"]
    if music:
        music_idx = 1 + len(overlays)
        cmd += ["-c:a", "aac", "-b:a", "192k",
                "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                "-map", f"{music_idx}:a", "-shortest"]
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
