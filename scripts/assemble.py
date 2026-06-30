#!/usr/bin/env python3
"""Assemble a campaign master (16:9) + reframed (9:16) from plan.json.

Reads plan.json + palette.json from a campaign dir, writes captions.ass,
builds a concat list of per-shot clips (already rendered into generated/ or
copied real clips), runs ffmpeg for the master, then reframes to vertical.
"""
import argparse, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.lib.plan_schema import validate_plan
from scripts.lib.caption_render import timed_captions, render_caption_png
from scripts.lib.ffmpeg_cmd import build_master_cmd, build_reframe_cmd

RES = {"16:9": (1920, 1080), "9:16": (1080, 1920)}


def _clip_path(campaign_dir, shot):
    # generated shots carry output_path; real clips carry asset path
    rel = shot.get("output_path") or shot.get("asset")
    if not rel:
        raise SystemExit(f"shot {shot['id']} has no clip path")
    return rel if os.path.isabs(rel) else os.path.join(campaign_dir, rel)


def _concat_line(path):
    # ffmpeg concat demuxer: single-quote the path; escape any literal quote
    # using the demuxer's '\'' idiom so paths containing ' don't break parsing.
    return "file '%s'\n" % path.replace("'", "'\\''")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign-dir", required=True)
    args = ap.parse_args()
    cdir = args.campaign_dir
    plan = json.load(open(os.path.join(cdir, "plan.json")))
    errs = validate_plan(plan)
    if errs:
        print("\n".join(errs), file=sys.stderr)
        sys.exit(2)
    palette = {}
    pf = os.path.join(cdir, "palette.json")
    if os.path.exists(pf):
        palette = json.load(open(pf))

    w, h = RES[plan["aspect_master"]]
    capdir = os.path.join(cdir, "captions")
    os.makedirs(capdir, exist_ok=True)
    overlays = []
    for i, (text, start, end) in enumerate(timed_captions(plan["shots"])):
        png = os.path.join(capdir, f"cap_{i:02d}.png")
        render_caption_png(text, w, h, palette, png)
        overlays.append({"path": png, "start": start, "end": end})

    concat = os.path.join(cdir, "_concat.txt")
    with open(concat, "w") as f:
        for sh in plan["shots"]:
            f.write(_concat_line(_clip_path(cdir, sh)))

    music = plan.get("music", {}).get("track")
    fps = plan.get("fps", 30)
    master = os.path.join(cdir, "master_16x9.mp4")
    subprocess.run(build_master_cmd(concat, music, overlays, master, w, h, fps),
                   check=True)

    vert = os.path.join(cdir, "master_9x16.mp4")
    subprocess.run(build_reframe_cmd(master, vert, 1080, 1920), check=True)
    print(master)
    print(vert)


if __name__ == "__main__":
    main()
