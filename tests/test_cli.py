"""CLI 模块的单元测试"""

from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest
import soundfile as sf
from click.testing import CliRunner

from voicescribe.cli import main


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "VoiceScribe" in result.output


def test_cli_nonexistent_file():
    runner = CliRunner()
    result = runner.invoke(main, ["/nonexistent/file.wav"])
    # click.Path(exists=True) 会在参数解析时报错
    assert result.exit_code != 0


def _make_wav(path: Path):
    data = np.zeros(16000, dtype=np.float32)
    sf.write(str(path), data, 16000)


def test_cli_single_file_txt_output(tmp_path):
    audio = tmp_path / "test.wav"
    _make_wav(audio)
    output = tmp_path / "out.txt"

    from voicescribe.core.asr_backend import Segment
    mock_segments = [Segment(0.0, 1.0, "テスト音声", 1.0)]

    with patch("voicescribe.cli._run_transcription") as mock_run:
        mock_run.return_value = mock_segments
        runner = CliRunner()
        result = runner.invoke(main, [
            str(audio), "-l", "ja", "-f", "txt", "-o", str(output),
        ])

    assert result.exit_code == 0, f"CLI failed: {result.output}"
    assert output.exists()
    assert output.read_text(encoding="utf-8") == "テスト音声"


def test_cli_multiple_formats(tmp_path):
    audio = tmp_path / "multi.wav"
    _make_wav(audio)

    from voicescribe.core.asr_backend import Segment
    mock_segments = [Segment(0.0, 1.0, "hello world", 1.0)]

    with patch("voicescribe.cli._run_transcription") as mock_run:
        mock_run.return_value = mock_segments
        runner = CliRunner()
        result = runner.invoke(main, [
            str(audio), "-l", "en", "-f", "txt,srt",
        ])

    assert result.exit_code == 0
    assert (audio.parent / "multi.txt").exists()
    assert (audio.parent / "multi.srt").exists()


def test_cli_batch_mode(tmp_path):
    """--batch 处理目录"""
    audio1 = tmp_path / "a.wav"
    audio2 = tmp_path / "b.wav"
    _make_wav(audio1)
    _make_wav(audio2)

    from voicescribe.core.asr_backend import Segment
    mock_segments = [Segment(0.0, 1.0, "test", 1.0)]

    with patch("voicescribe.cli._run_transcription") as mock_run:
        mock_run.return_value = mock_segments
        runner = CliRunner()
        result = runner.invoke(main, [
            str(tmp_path), "-l", "ja", "--batch", "-f", "txt",
        ])

    assert result.exit_code == 0
    assert (tmp_path / "out" / "a.txt").exists()
    assert (tmp_path / "out" / "b.txt").exists()


def test_cli_paddle_zh_gives_friendly_error(tmp_path):
    """中文 ASR 应给出清晰的 Python 3.14 错误"""
    audio = tmp_path / "cn.wav"
    _make_wav(audio)

    runner = CliRunner()
    result = runner.invoke(main, [str(audio), "-l", "zh"])

    assert result.exit_code != 0
    assert "Python 3.14" in result.output
