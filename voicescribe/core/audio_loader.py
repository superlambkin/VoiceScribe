"""音频加载（soundfile 解码 WAV/FLAC，pydub 处理 MP3/M4A）"""

from pathlib import Path

import numpy as np
import soundfile as sf


SUPPORTED_EXTENSIONS = frozenset({".wav", ".flac", ".ogg"})
# MP3 / M4A 需要 pydub + ffmpeg，本 v1 暂不支持（保持依赖最小化）
# 若需要 MP3 支持：pip install pydub + 系统安装 ffmpeg


def load_audio(path: Path) -> tuple[int, np.ndarray]:
    """加载音频文件，返回 (sample_rate, audio_data)"""
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported audio format: {suffix}. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    data, sr = sf.read(str(path), dtype="float32")
    # 多声道转单声道（取均值）
    if data.ndim > 1:
        data = data.mean(axis=1)
    return sr, data


def get_duration(path: Path) -> float:
    """获取音频时长（秒）"""
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")
    info = sf.info(str(path))
    return info.duration