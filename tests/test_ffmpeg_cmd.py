from scripts.lib.ffmpeg_cmd import (
    build_frames_cmd, build_master_cmd, build_reframe_cmd,
)


def test_frames_cmd_has_scene_select():
    cmd = build_frames_cmd("in.mp4", "/out", threshold=0.4)
    joined = " ".join(cmd)
    assert "select='gt(scene,0.4)'" in joined
    assert cmd[0] == "ffmpeg"


def test_master_cmd_encodes_and_loudnorm():
    cmd = build_master_cmd("list.txt", "music.mp3", "caps.ass",
                           "master.mp4", fps=30)
    j = " ".join(cmd)
    assert "-c:v libx264" in j
    assert "-c:a aac" in j
    assert "loudnorm=I=-14" in j
    assert "subtitles=caps.ass" in j
    assert "-r 30" in j


def test_master_cmd_without_music_has_no_audio_map():
    cmd = build_master_cmd("list.txt", None, "caps.ass", "master.mp4", fps=30)
    j = " ".join(cmd)
    assert "loudnorm" not in j
    assert "libx264" in j


def test_reframe_cmd_blurred_background_vertical():
    cmd = build_reframe_cmd("master.mp4", "vert.mp4", w=1080, h=1920)
    j = " ".join(cmd)
    assert "boxblur" in j
    assert "overlay=" in j
    assert "scale=1080:1920" in j
    assert "libx264" in j
