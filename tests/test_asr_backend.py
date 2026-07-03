"""asr_backend 模块的单元测试"""

import pytest
from pathlib import Path

from voicescribe.core.asr_backend import (
    ASRBackend,
    Segment,
    get_asr_backend,
)
from voicescribe.core.config import Config
from voicescribe.core.whisper_asr import WhisperASR
from voicescribe.core.paddle_asr import PaddleASR


def test_segment_dataclass():
    seg = Segment(start=0.0, end=1.5, text="hello", confidence=0.9)
    assert seg.start == 0.0
    assert seg.end == 1.5
    assert seg.text == "hello"
    assert seg.confidence == 0.9


def test_factory_returns_whisper_for_ja():
    config = Config()
    backend = get_asr_backend("ja", config)
    assert isinstance(backend, WhisperASR)
    assert backend.lang == "ja"


def test_factory_returns_whisper_for_en():
    config = Config()
    backend = get_asr_backend("en", config)
    assert isinstance(backend, WhisperASR)
    assert backend.lang == "en"


def test_factory_returns_paddle_for_zh():
    config = Config()
    backend = get_asr_backend("zh", config)
    assert isinstance(backend, PaddleASR)


def test_factory_raises_for_unsupported():
    config = Config()
    with pytest.raises(ValueError, match="Unsupported language"):
        get_asr_backend("xx", config)


def test_paddle_backend_unsupported_transcribe():
    """PaddleASR 在 3.14 上调用 transcribe 必须抛清晰错误"""
    backend = PaddleASR(Config())
    with pytest.raises(NotImplementedError, match="Python 3.14"):
        backend.transcribe(Path("fake.wav"), "zh")


def test_paddle_backend_is_model_ready_returns_false():
    assert PaddleASR(Config()).is_model_ready() is False


def test_paddle_backend_download_raises():
    with pytest.raises(NotImplementedError, match="Python 3.14"):
        PaddleASR(Config()).download_model()
