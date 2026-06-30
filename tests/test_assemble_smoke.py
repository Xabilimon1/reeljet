import json, os, shutil, subprocess
import pytest

pytestmark = pytest.mark.skipif(
    shutil.which("ffmpeg") is None, reason="ffmpeg not installed")


def _make_clip(path, color, seconds=1):
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i",
         f"color=c={color}:s=320x180:d={seconds}:r=30",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", path],
        check=True, capture_output=True)


def test_end_to_end_master_and_vertical(tmp_path):
    cdir = tmp_path / "camp"
    (cdir / "generated").mkdir(parents=True)
    _make_clip(str(cdir / "generated" / "s01.mp4"), "red")
    _make_clip(str(cdir / "generated" / "s02.mp4"), "blue")
    plan = {
        "app": "T", "campaign": "c", "date": "2026-06-30",
        "aspect_master": "16:9", "fps": 30,
        "shots": [
            {"id": "s01", "source": "higgsfield_broll", "duration": 1,
             "status": "done", "output_path": "generated/s01.mp4",
             "caption": "Hello"},
            {"id": "s02", "source": "higgsfield_broll", "duration": 1,
             "status": "done", "output_path": "generated/s02.mp4"},
        ],
    }
    (cdir / "plan.json").write_text(json.dumps(plan))
    (cdir / "palette.json").write_text(json.dumps(
        {"caption_fill": "#0AC828", "caption_outline": "#000000"}))
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(
        ["python3", os.path.join(repo, "scripts", "assemble.py"),
         "--campaign-dir", str(cdir)], check=True, capture_output=True)
    assert (cdir / "master_16x9.mp4").exists()
    assert (cdir / "master_9x16.mp4").exists()
