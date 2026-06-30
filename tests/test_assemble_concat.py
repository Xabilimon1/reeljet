from scripts.assemble import _concat_line


def test_concat_line_plain_path():
    assert _concat_line("/c/s01.mp4") == "file '/c/s01.mp4'\n"


def test_concat_line_escapes_single_quote():
    # ffmpeg concat demuxer idiom: ' -> '\''
    assert _concat_line("/c/it's.mp4") == "file '/c/it'\\''s.mp4'\n"
