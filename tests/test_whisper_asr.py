"""whisper_asr 模块的单元测试"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from voicescribe.core.asr_backend import Segment
from voicescribe.core.config import Config
from voicescribe.core.whisper_asr import WhisperASR


def test_whisper_init_stores_lang_and_config():
    config = Config(whisper_model="small")
    asr = WhisperASR("ja", config)
    assert asr.lang == "ja"
    assert asr.config.whisper_model == "small"
    assert asr.model is None  # 懒加载


def test_whisper_is_model_ready_false_when_no_dir():
    config = Config(model_dir=Path("/tmp/nonexistent_models_xyz"))
    asr = WhisperASR("ja", config)
    with patch.object(Path, "home", return_value=Path("/nonexistent_home")):
        assert asr.is_model_ready() is False


def test_whisper_is_model_ready_true_when_dir_exists_with_files(tmp_path):
    model_dir = tmp_path / "whisper-large-v3"
    model_dir.mkdir()
    (model_dir / "model.bin").touch()
    config = Config(model_dir=tmp_path)
    asr = WhisperASR("ja", config)
    assert asr.is_model_ready() is True


def test_whisper_transcribe_lazy_loads_model(tmp_path):
    """首次转写触发模型加载"""
    fake_audio = tmp_path / "test.wav"
    fake_audio.touch()

    config = Config(whisper_model="tiny", whisper_compute_type="int8")

    # 模拟 faster_whisper.WhisperModel
    with patch("voicescribe.core.whisper_asr._import_whisper_model") as mock_import:
        # mock_model_instance 是真正被用作 self.model 的实例
        mock_model_instance = MagicMock()
        mock_segment = MagicMock()
        mock_segment.start = 0.0
        mock_segment.end = 1.5
        mock_segment.text = "こんにちは"
        mock_segment.avg_logprob = -0.1
        mock_model_instance.transcribe.return_value = ([mock_segment], MagicMock())
        # _import_whisper_model 返回的类在被调用时返回 mock_model_instance
        mock_import.return_value = lambda *args, **kwargs: mock_model_instance

        asr = WhisperASR("ja", config)
        segments = asr.transcribe(fake_audio, "ja")

    assert len(segments) == 1
    assert segments[0].text == "こんにちは"
    assert segments[0].start == 0.0
    assert segments[0].end == 1.5
    # confidence 从 avg_logprob 转换
    assert 0.0 <= segments[0].confidence <= 1.0


def test_whisper_transcribe_reuses_loaded_model(tmp_path):
    """第二次转写复用已加载模型"""
    fake_audio = tmp_path / "test.wav"
    fake_audio.touch()
    config = Config(whisper_model="tiny")

    with patch("voicescribe.core.whisper_asr._import_whisper_model") as mock_import:
        # mock_model_instance 是真正被用作 self.model 的实例
        mock_model_instance = MagicMock()
        mock_model_instance.transcribe.return_value = ([], MagicMock())
        # _import_whisper_model 返回的类在被调用时返回 mock_model_instance
        mock_import.return_value = lambda *args, **kwargs: mock_model_instance

        asr = WhisperASR("ja", config)
        asr.transcribe(fake_audio, "ja")
        asr.transcribe(fake_audio, "ja")

    # _import_whisper_model 只调用一次
    assert mock_import.call_count == 1
