"""Pick the most fitting track from a local royalty-free library."""
from __future__ import annotations
import glob, os, re

AUDIO_EXTS = (".mp3", ".m4a", ".wav", ".aac", ".flac", ".ogg")
MOODS = ["uplifting", "energetic", "calm", "epic", "corporate", "chill",
         "dramatic", "happy", "dark", "playful", "horror"]


def parse_track_meta(path):
    name = os.path.splitext(os.path.basename(path))[0].lower()
    tokens = [t for t in re.split(r"[ _\-]+", name) if t]
    bpm = None
    for t in tokens:
        m = re.match(r"^(\d{2,3})bpm$", t) or re.match(r"^(\d{2,3})$", t)
        if m:
            v = int(m.group(1))
            if 40 <= v <= 220:
                bpm = v
    mood = next((t for t in tokens if t in MOODS), None)
    return {"path": path, "bpm": bpm, "mood": mood, "tokens": tokens}


def scan_library(root):
    out = []
    for e in AUDIO_EXTS:
        out += glob.glob(os.path.join(root, "**", "*" + e), recursive=True)
    return [parse_track_meta(p) for p in sorted(out)]


def score_track(meta, brief):
    score = 0.0
    if brief.get("mood") and meta.get("mood") == brief["mood"]:
        score += 2.0
    bm, mb = brief.get("bpm"), meta.get("bpm")
    if bm and mb:
        score += max(0.0, 1.0 - abs(mb - bm) / 60.0)
    kw = set(brief.get("keywords", []))
    score += 0.25 * len(kw.intersection(meta.get("tokens", [])))
    return score


def pick_music(tracks, brief):
    if not tracks:
        return None
    return max(tracks, key=lambda m: score_track(m, brief))
