#!/usr/bin/env python3
"""CLI: scan an assets dir for images -> write palette.json."""
import argparse, glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.lib.palette import extract_palette

EXTS = ("*.png", "*.jpg", "*.jpeg", "*.webp")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("-k", type=int, default=5)
    args = ap.parse_args()
    paths = []
    for e in EXTS:
        paths += glob.glob(os.path.join(args.assets, "**", e), recursive=True)
    if not paths:
        print("no images found", file=sys.stderr)
        sys.exit(1)
    pal = extract_palette(sorted(paths), k=args.k)
    with open(args.out, "w") as f:
        json.dump(pal, f, indent=2)
    print(args.out)


if __name__ == "__main__":
    main()
