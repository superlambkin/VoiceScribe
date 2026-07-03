"""language_detector 模块的单元测试"""

from pathlib import Path

from voicescribe.core.language_detector import detect_language_from_path


def test_detect_chinese_from_path():
    assert detect_language_from_path(Path("meeting_zh.wav")) == "zh"


def test_detect_japanese_from_path():
    assert detect_language_from_path(Path("meeting_jp.mp3")) == "ja"


def test_detect_japanese_from_japanese_name():
    assert detect_language_from_path(Path("会议_jp.wav")) == "ja"


def test_detect_english_from_path():
    assert detect_language_from_path(Path("podcast_en.m4a")) == "en"


def test_detect_returns_auto_for_unknown():
    """无法识别时返回 'auto'"""
    assert detect_language_from_path(Path("unknown_file.wav")) == "auto"