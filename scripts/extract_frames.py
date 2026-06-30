#!/usr/bin/env python3
"""CLI: scene-detect key frames from a recording into out_dir."""
import argparse, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.lib.ffmpeg_cmd import build_frames_cmd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--threshold", type=float, default=0.4)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    cmd = build_frames_cmd(args.video, args.out, args.threshold)
    subprocess.run(cmd, check=True)
    print(args.out)


if __name__ == "__main__":
    main()
