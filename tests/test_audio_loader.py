"""audio_loader 模块的单元测试"""

import numpy as np
import pytest
import soundfile as sf
from pathlib import Path

from voicescribe.core.audio_loader import (
    SUPPORTED_EXTENSIONS,
    load_audio,
    get_duration,
)


def test_supported_extensions_includes_common():
    # v0.1.0+ supports WAV, FLAC, OGG, MP3, M4A (requires pydub + ffmpeg for MP3/M4A)
    assert ".wav" in SUPPORTED_EXTENSIONS
    assert ".flac" in SUPPORTED_EXTENSIONS
    assert ".ogg" in SUPPORTED_EXTENSIONS
    assert ".mp3" in SUPPORTED_EXTENSIONS
    assert ".m4a" in SUPPORTED_EXTENSIONS


def test_load_audio_returns_tuple(tmp_path):
    """加载 WAV 文件返回 (sample_rate, audio_data)"""
    audio_path = tmp_path / "test.wav"
    sample_rate = 16000
    duration = 1.0
    audio_data = np.random.randn(int(sample_rate * duration)).astype(np.float32) * 0.1
    sf.write(str(audio_path), audio_data, sample_rate)

    sr, data = load_audio(audio_path)
    assert sr == sample_rate
    assert isinstance(data, np.ndarray)
    assert len(data) == int(sample_rate * duration)


def test_load_audio_unsupported_extension(tmp_path):
    fake = tmp_path / "test.xyz"
    fake.touch()
    with pytest.raises(ValueError, match="Unsupported audio format"):
        load_audio(fake)


def test_load_audio_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_audio(tmp_path / "nonexistent.wav")


def test_get_duration_short_wav(tmp_path):
    audio_path = tmp_path / "short.wav"
    sr = 16000
    data = np.zeros(sr * 2, dtype=np.float32)  # 2 秒静音
    sf.write(str(audio_path), data, sr)
    duration = get_duration(audio_path)
    assert 1.9 < duration < 2.1