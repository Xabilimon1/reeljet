#!/usr/bin/env python3
"""CLI: pick best track from MusicLibrary given a brief. Prints the path."""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.lib.musiclib import scan_library, pick_music

DEFAULT_LIB = os.path.expanduser("~/x-brain/Resources/MusicLibrary")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--library", default=DEFAULT_LIB)
    ap.add_argument("--mood")
    ap.add_argument("--bpm", type=int)
    ap.add_argument("--keywords", default="")
    args = ap.parse_args()
    brief = {"mood": args.mood, "bpm": args.bpm,
             "keywords": [k for k in args.keywords.split(",") if k]}
    tracks = scan_library(args.library)
    best = pick_music(tracks, brief)
    if not best:
        print("no tracks found in library", file=sys.stderr)
        sys.exit(1)
    print(best["path"])


if __name__ == "__main__":
    main()
