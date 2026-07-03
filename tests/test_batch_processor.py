"""batch_processor 模块的单元测试"""

from pathlib import Path
from unittest.mock import patch, MagicMock

import numpy as np
import pytest
import soundfile as sf

from voicescribe.core.asr_backend import Segment
from voicescribe.core.batch_processor import process_batch
from voicescribe.core.config import Config


def _make_wav(path: Path, duration: float = 1.0, sr: int = 16000):
    data = np.zeros(int(sr * duration), dtype=np.float32)
    sf.write(str(path), data, sr)


def test_process_batch_empty_dir(tmp_path):
    """空目录处理应该返回 0 个文件"""
    result = process_batch(
        input_dir=tmp_path,
        lang="ja",
        output_dir=tmp_path / "out",
        formats=["txt"],
        config=Config(),
    )
    assert result["total"] == 0
    assert result["succeeded"] == 0
    assert result["failed"] == 0


def test_process_batch_skips_unsupported_files(tmp_path):
    """非音频文件被跳过"""
    (tmp_path / "readme.txt").write_text("not audio")
    result = process_batch(
        input_dir=tmp_path,
        lang="ja",
        output_dir=tmp_path / "out",
        formats=["txt"],
        config=Config(),
    )
    assert result["total"] == 0


def test_process_batch_one_file(tmp_path):
    """处理单个 WAV 文件（mock ASR）"""
    audio = tmp_path / "meeting.wav"
    _make_wav(audio)

    mock_segments = [Segment(0.0, 1.0, "テスト", 1.0)]

    with patch("voicescribe.core.batch_processor._run_transcription") as mock_run:
        mock_run.return_value = mock_segments
        result = process_batch(
            input_dir=tmp_path,
            lang="ja",
            output_dir=tmp_path / "out",
            formats=["txt"],
            config=Config(),
        )

    assert result["total"] == 1
    assert result["succeeded"] == 1
    assert result["failed"] == 0
    # 输出文件存在
    assert (tmp_path / "out" / "meeting.txt").exists()
    assert (tmp_path / "out" / "meeting.txt").read_text(encoding="utf-8") == "テスト"


def test_process_batch_multiple_formats(tmp_path):
    """多种输出格式"""
    audio = tmp_path / "podcast.wav"
    _make_wav(audio)

    mock_segments = [Segment(0.0, 1.0, "hello", 1.0)]

    with patch("voicescribe.core.batch_processor._run_transcription") as mock_run:
        mock_run.return_value = mock_segments
        result = process_batch(
            input_dir=tmp_path,
            lang="en",
            output_dir=tmp_path / "out",
            formats=["txt", "srt", "md"],
            config=Config(),
        )

    assert result["succeeded"] == 1
    assert (tmp_path / "out" / "podcast.txt").exists()
    assert (tmp_path / "out" / "podcast.srt").exists()
    assert (tmp_path / "out" / "podcast.md").exists()


def test_process_batch_continues_on_failure(tmp_path):
    """单个文件失败不影响其他"""
    audio1 = tmp_path / "good.wav"
    audio2 = tmp_path / "bad.wav"
    _make_wav(audio1)
    _make_wav(audio2)

    def mock_run_side_effect(audio_path, lang, config):
        if "bad" in str(audio_path):
            raise RuntimeError("mock failure")
        return [Segment(0.0, 1.0, "ok", 1.0)]

    with patch("voicescribe.core.batch_processor._run_transcription") as mock_run:
        mock_run.side_effect = mock_run_side_effect
        result = process_batch(
            input_dir=tmp_path,
            lang="en",
            output_dir=tmp_path / "out",
            formats=["txt"],
            config=Config(),
        )

    assert result["total"] == 2
    assert result["succeeded"] == 1
    assert result["failed"] == 1
    assert "good.wav" in result["success_files"]
    assert "bad.wav" in result["failed_files"]
