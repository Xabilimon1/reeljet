"""Validation for reeljet plan.json (single source of truth for a campaign)."""
from __future__ import annotations

VALID_SOURCES = {"real_clip", "higgsfield_broll", "animated_screenshot"}
VALID_STATUS = {"pending", "generating", "done", "failed"}
GENERATED = {"higgsfield_broll", "animated_screenshot"}
SHOT_REQUIRED = ["id", "source", "duration", "status"]
PLAN_REQUIRED = ["app", "campaign", "date", "aspect_master", "fps", "shots"]


def validate_shot(shot, idx):
    errs = []
    for f in SHOT_REQUIRED:
        if f not in shot:
            errs.append(f"shot[{idx}]: missing '{f}'")
    if "source" in shot and shot["source"] not in VALID_SOURCES:
        errs.append(f"shot[{idx}]: invalid source '{shot['source']}'")
    if "status" in shot and shot["status"] not in VALID_STATUS:
        errs.append(f"shot[{idx}]: invalid status '{shot['status']}'")
    if "duration" in shot:
        try:
            if float(shot["duration"]) <= 0:
                errs.append(f"shot[{idx}]: duration must be > 0")
        except (TypeError, ValueError):
            errs.append(f"shot[{idx}]: duration not a number")
    if shot.get("source") in GENERATED and shot.get("status") == "done":
        if not shot.get("output_path"):
            errs.append(f"shot[{idx}]: done generated shot needs output_path")
    return errs


def validate_plan(plan):
    errs = []
    for f in PLAN_REQUIRED:
        if f not in plan:
            errs.append(f"plan: missing '{f}'")
    shots = plan.get("shots", [])
    if not isinstance(shots, list) or not shots:
        errs.append("plan: shots must be a non-empty list")
        return errs
    ids = set()
    for i, sh in enumerate(shots):
        errs += validate_shot(sh, i)
        sid = sh.get("id")
        if sid in ids:
            errs.append(f"shot[{i}]: duplicate id '{sid}'")
        ids.add(sid)
    return errs
