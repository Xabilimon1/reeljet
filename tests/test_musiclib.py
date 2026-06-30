from scripts.lib.musiclib import parse_track_meta, score_track, pick_music


def test_parse_meta_from_filename():
    m = parse_track_meta("/lib/uplifting_120bpm_corporate.mp3")
    assert m["mood"] == "uplifting"
    assert m["bpm"] == 120


def test_parse_meta_no_hints():
    m = parse_track_meta("/lib/track1.wav")
    assert m["bpm"] is None and m["mood"] is None


def test_score_prefers_matching_mood_and_bpm():
    brief = {"mood": "uplifting", "bpm": 120, "keywords": ["corporate"]}
    good = parse_track_meta("/lib/uplifting_120bpm_corporate.mp3")
    bad = parse_track_meta("/lib/dark_80bpm_horror.mp3")
    assert score_track(good, brief) > score_track(bad, brief)


def test_pick_music_returns_best():
    brief = {"mood": "energetic", "bpm": 128, "keywords": []}
    tracks = [parse_track_meta("/lib/calm_70bpm.mp3"),
              parse_track_meta("/lib/energetic_130bpm.mp3")]
    assert pick_music(tracks, brief)["path"].endswith("energetic_130bpm.mp3")


def test_pick_music_empty_is_none():
    assert pick_music([], {"mood": "x"}) is None
