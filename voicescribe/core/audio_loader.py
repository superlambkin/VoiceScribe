"""音频加载

- WAV / FLAC / OGG：soundfile 直接解码
- MP3 / M4A：pydub + ffmpeg 解码（需安装 pydub + 系统 ffmpeg）

环境兼容：
- 若 pydub 未安装，MP3/M4A 加载会报清晰错误（仍可加载 WAV/FLAC/OGG）
- 若 pydub 已装但 ffmpeg 缺失，同样报错
"""

from pathlib import Path

import numpy as np
import soundfile as sf


SUPPORTED_EXTENSIONS = frozenset({".wav", ".flac", ".ogg", ".mp3", ".m4a"})

# soundfile 原生支持（无需 ffmpeg）
SOUNDFILE_EXTENSIONS = frozenset({".wav", ".flac", ".ogg"})
# 需要 pydub + ffmpeg
PYDUB_EXTENSIONS = frozenset({".mp3", ".m4a"})


def _import_pydub():
    """延迟导入 pydub，给清晰错误信息"""
    try:
        from pydub import AudioSegment
        return AudioSegment
    except ImportError as e:
        raise ImportError(
            "pydub 未安装。MP3/M4A 需要 pydub + ffmpeg。\n"
            "执行：pip install pydub imageio-ffmpeg\n"
            "(imageio-ffmpeg 提供 ffmpeg 二进制，无需手动装系统 ffmpeg)"
        ) from e


def _convert_with_pydub(path: Path, target_sr: int = 16000) -> tuple[int, np.ndarray]:
    """用 pydub 加载 MP3/M4A 并转 numpy"""
    AudioSegment = _import_pydub()

    suffix = path.suffix.lower()
    fmt = "mp3" if suffix == ".mp3" else "m4a"

    audio = AudioSegment.from_file(str(path), format=fmt)
    # 转单声道
    if audio.channels > 1:
        audio = audio.set_channels(1)
    # 重采样到目标采样率
    if audio.frame_rate != target_sr:
        audio = audio.set_frame_rate(target_sr)
    # 转 numpy float32
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    # 归一化到 [-1, 1]（pydub 默认是 int16）
    samples = samples / 32768.0
    return target_sr, samples


def load_audio(path: Path) -> tuple[int, np.ndarray]:
    """加载音频文件，返回 (sample_rate, audio_data)

    Args:
        path: 音频文件路径

    Returns:
        (sample_rate, audio_data as np.ndarray float32)

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 不支持的格式
        ImportError: MP3/M4A 但 pydub 未装
    """
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported audio format: {suffix}. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    if suffix in SOUNDFILE_EXTENSIONS:
        data, sr = sf.read(str(path), dtype="float32")
        # 多声道转单声道（取均值）
        if data.ndim > 1:
            data = data.mean(axis=1)
        return sr, data
    else:
        # MP3 / M4A 走 pydub
        return _convert_with_pydub(path, target_sr=16000)


def get_duration(path: Path) -> float:
    """获取音频时长（秒）"""
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    suffix = path.suffix.lower()

    if suffix in SOUNDFILE_EXTENSIONS:
        info = sf.info(str(path))
        return info.duration
    elif suffix in PYDUB_EXTENSIONS:
        AudioSegment = _import_pydub()
        fmt = "mp3" if suffix == ".mp3" else "m4a"
        audio = AudioSegment.from_file(str(path), format=fmt)
        return len(audio) / 1000.0  # 毫秒 → 秒
    else:
        raise ValueError(
            f"Unsupported audio format: {suffix}. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )