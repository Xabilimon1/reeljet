#!/usr/bin/env python3
"""Assemble a campaign master (16:9) + reframed (9:16) from plan.json.

Reads plan.json + palette.json from a campaign dir, writes captions.ass,
builds a concat list of per-shot clips (already rendered into generated/ or
copied real clips), runs ffmpeg for the master, then reframes to vertical.
"""
import argparse, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.lib.plan_schema import validate_plan
from scripts.lib.captions import build_ass
from scripts.lib.ffmpeg_cmd import build_master_cmd, build_reframe_cmd

RES = {"16:9": (1920, 1080), "9:16": (1080, 1920)}


def _clip_path(campaign_dir, shot):
    # generated shots carry output_path; real clips carry asset path
    rel = shot.get("output_path") or shot.get("asset")
    if not rel:
        raise SystemExit(f"shot {shot['id']} has no clip path")
    return rel if os.path.isabs(rel) else os.path.join(campaign_dir, rel)


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
    ass = build_ass(plan["shots"], palette, w, h)
    ass_path = os.path.join(cdir, "captions.ass")
    open(ass_path, "w").write(ass)

    concat = os.path.join(cdir, "_concat.txt")
    with open(concat, "w") as f:
        for sh in plan["shots"]:
            f.write(f"file '{_clip_path(cdir, sh)}'\n")

    music = plan.get("music", {}).get("track")
    fps = plan.get("fps", 30)
    master = os.path.join(cdir, "master_16x9.mp4")
    subprocess.run(build_master_cmd(concat, music, ass_path, master, fps),
                   check=True)

    vert = os.path.join(cdir, "master_9x16.mp4")
    subprocess.run(build_reframe_cmd(master, vert, 1080, 1920), check=True)
    print(master)
    print(vert)


if __name__ == "__main__":
    main()
