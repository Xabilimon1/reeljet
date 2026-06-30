from scripts.lib.plan_schema import validate_plan


def _valid_plan():
    return {
        "app": "Numo", "campaign": "launch", "date": "2026-06-30",
        "aspect_master": "16:9", "fps": 30,
        "shots": [
            {"id": "s01", "source": "real_clip", "duration": 2.5,
             "status": "pending", "caption": "Meet Numo"},
            {"id": "s02", "source": "higgsfield_broll", "duration": 3.0,
             "status": "done", "output_path": "generated/s02.mp4"},
        ],
    }


def test_valid_plan_has_no_errors():
    assert validate_plan(_valid_plan()) == []


def test_missing_top_field_reported():
    p = _valid_plan(); del p["fps"]
    assert any("missing 'fps'" in e for e in validate_plan(p))


def test_bad_source_reported():
    p = _valid_plan(); p["shots"][0]["source"] = "magic"
    assert any("invalid source" in e for e in validate_plan(p))


def test_nonpositive_duration_reported():
    p = _valid_plan(); p["shots"][0]["duration"] = 0
    assert any("duration must be > 0" in e for e in validate_plan(p))


def test_done_generated_shot_needs_output_path():
    p = _valid_plan(); del p["shots"][1]["output_path"]
    assert any("needs output_path" in e for e in validate_plan(p))


def test_duplicate_ids_reported():
    p = _valid_plan(); p["shots"][1]["id"] = "s01"
    assert any("duplicate id" in e for e in validate_plan(p))
