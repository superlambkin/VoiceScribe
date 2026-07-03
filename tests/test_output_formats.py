"""output_formats 模块的单元测试"""

import pytest

from voicescribe.core.asr_backend import Segment
from voicescribe.core.output_formats import (
    FORMATTERS,
    TxtFormatter,
    MdFormatter,
    SrtFormatter,
    VttFormatter,
    _format_srt_time,
    _format_vtt_time,
)


# ----- TxtFormatter -----

def test_txt_formatter_returns_text():
    segs = [Segment(0.0, 5.0, "你好", 1.0), Segment(5.0, 10.0, "世界", 1.0)]
    f = TxtFormatter()
    result = f.format(segs)
    assert result == "你好\n世界"


def test_txt_formatter_extension():
    assert TxtFormatter().extension() == "txt"


# ----- MdFormatter -----

def test_md_formatter_includes_metadata():
    segs = [Segment(0.0, 5.0, "你好", 1.0)]
    f = MdFormatter()
    f.audio_path = None  # 测试不依赖 audio_path
    result = f.format(segs)
    assert "# 转写结果" in result
    assert "片段数: 1" in result
    assert "你好" in result


def test_md_formatter_extension():
    assert MdFormatter().extension() == "md"


# ----- SrtFormatter -----

def test_srt_formatter_produces_valid_srt():
    segs = [Segment(1.5, 3.5, "测试文本", 1.0)]
    result = SrtFormatter().format(segs)
    assert "1\n" in result
    assert "00:00:01,500 --> 00:00:03,500\n" in result
    assert "测试文本" in result


def test_srt_formatter_extension():
    assert SrtFormatter().extension() == "srt"


# ----- VttFormatter -----

def test_vtt_formatter_starts_with_webvtt():
    segs = [Segment(0.0, 2.0, "hello", 1.0)]
    result = VttFormatter().format(segs)
    assert result.startswith("WEBVTT")


def test_vtt_uses_dot_for_milliseconds():
    segs = [Segment(0.0, 2.5, "x", 1.0)]
    result = VttFormatter().format(segs)
    assert "00:00:00.000 --> 00:00:02.500" in result


def test_vtt_formatter_extension():
    assert VttFormatter().extension() == "vtt"


# ----- FORMATTERS dict -----

def test_formatters_dict_has_all_keys():
    assert set(FORMATTERS.keys()) == {"txt", "md", "srt", "vtt"}


def test_formatters_dict_returns_classes():
    for key, cls in FORMATTERS.items():
        assert callable(cls)


# ----- 时间格式化辅助 -----

def test_format_srt_time_zero():
    assert _format_srt_time(0) == "00:00:00,000"


def test_format_srt_time_complex():
    assert _format_srt_time(3725.123) == "01:02:05,123"


def test_format_vtt_uses_dot():
    assert _format_vtt_time(1.5) == "00:00:01.500"
