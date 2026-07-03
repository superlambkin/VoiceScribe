"""音频加载

- WAV / FLAC / OGG：soundfile 直接解码
- MP3 / M4A：通过 ffmpeg subprocess 转 WAV → soundfile 读取

环境兼容：
- 不依赖 pydub（pydub 在 Python 3.13+ 有 audioop 兼容问题）
- 仅需 imageio-ffmpeg 提供 ffmpeg 二进制（pip 可装）
- 若没有 ffmpeg，MP3/M4A 加载会报清晰错误
"""

import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf


SUPPORTED_EXTENSIONS = frozenset({".wav", ".flac", ".ogg", ".mp3", ".m4a"})

# soundfile 原生支持（无需 ffmpeg）
SOUNDFILE_EXTENSIONS = frozenset({".wav", ".flac", ".ogg"})
# 需要 ffmpeg 转换
FFMPEG_EXTENSIONS = frozenset({".mp3", ".m4a"})


def _get_ffmpeg_path() -> str:
    """获取 ffmpeg 可执行路径，优先用 imageio-ffmpeg（pip 安装，无需系统 ffmpeg）"""
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as e:
        raise ImportError(
            "MP3/M4A 需要 ffmpeg。\n"
            "执行：pip install imageio-ffmpeg\n"
            "(提供 ffmpeg 二进制，无需手动装系统 ffmpeg)"
        ) from e


def _ffmpeg_convert_to_wav(src_path: Path, target_sr: int = 16000) -> tuple[int, np.ndarray]:
    """用 ffmpeg 将 MP3/M4A 转 WAV，再用 soundfile 读取"""
    ffmpeg = _get_ffmpeg_path()

    # 用临时文件保存 ffmpeg 输出
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        # ffmpeg 转码：单声道 + 目标采样率 + PCM 16-bit
        cmd = [
            ffmpeg,
            "-y",                  # 覆盖输出
            "-i", str(src_path),   # 输入
            "-ac", "1",            # 单声道
            "-ar", str(target_sr), # 采样率
            "-f", "wav",           # 输出格式
            str(tmp_path),
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"ffmpeg 转码失败 (exit {result.returncode}): {result.stderr[:300]}"
            )

        # 用 soundfile 读 WAV
        data, sr = sf.read(str(tmp_path), dtype="float32")
        return sr, data
    finally:
        # 清理临时文件
        try:
            tmp_path.unlink()
        except OSError:
            pass


def _ffmpeg_get_duration(src_path: Path) -> float:
    """用 ffprobe 获取 MP3/M4A 时长"""
    ffmpeg = _get_ffmpeg_path()
    # ffprobe 一般和 ffmpeg 同目录
    ffmpeg_dir = Path(ffmpeg).parent
    ffprobe = ffmpeg_dir / ("ffprobe.exe" if Path(ffmpeg).suffix == ".exe" else "ffprobe")

    # 如果 ffprobe 不存在（imageio-ffmpeg 只提供 ffmpeg），用 ffmpeg 解析
    if not ffprobe.exists():
        # 退而求其次：用 ffmpeg -i 输出 stderr 的 Duration 字段
        result = subprocess.run(
            [ffmpeg, "-i", str(src_path)],
            capture_output=True,
            text=True,
        )
        # stderr 形如: "Duration: HH:MM:SS.cc, ..."
        import re
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", result.stderr)
        if m:
            h, mi, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
            return h * 3600 + mi * 60 + s
        raise RuntimeError(f"无法解析音频时长: {src_path}")

    result = subprocess.run(
        [
            str(ffprobe),
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(src_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def load_audio(path: Path) -> tuple[int, np.ndarray]:
    """加载音频文件，返回 (sample_rate, audio_data)

    Args:
        path: 音频文件路径

    Returns:
        (sample_rate, audio_data as np.ndarray float32)

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 不支持的格式
        ImportError: MP3/M4A 但 ffmpeg 缺失
        RuntimeError: ffmpeg 转码失败
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
        # MP3 / M4A 走 ffmpeg 转 WAV
        return _ffmpeg_convert_to_wav(path, target_sr=16000)


def get_duration(path: Path) -> float:
    """获取音频时长（秒）"""
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    suffix = path.suffix.lower()

    if suffix in SOUNDFILE_EXTENSIONS:
        info = sf.info(str(path))
        return info.duration
    elif suffix in FFMPEG_EXTENSIONS:
        return _ffmpeg_get_duration(path)
    else:
        raise ValueError(
            f"Unsupported audio format: {suffix}. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )