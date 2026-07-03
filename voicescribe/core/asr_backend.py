"""ASR 后端抽象层

定义所有 ASR 实现必须遵循的接口。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional


@dataclass
class Segment:
    """转写片段"""
    start: float       # 开始时间（秒）
    end: float         # 结束时间（秒）
    text: str          # 识别文本
    confidence: float  # 置信度（0.0-1.0）


class ASRBackend(ABC):
    """ASR 后端抽象基类"""

    @abstractmethod
    def transcribe(self, audio_path: Path, lang: str) -> list[Segment]:
        """转写音频文件，返回带时间戳的 Segment 列表"""
        raise NotImplementedError

    @abstractmethod
    def is_model_ready(self) -> bool:
        """检查模型是否已下载"""
        raise NotImplementedError

    @abstractmethod
    def download_model(self, progress_callback: Optional[Callable[[float, str], None]] = None) -> None:
        """下载模型（懒加载），progress_callback(downloaded_bytes, status_msg)"""
        raise NotImplementedError


def get_asr_backend(lang: str, config) -> ASRBackend:
    """工厂方法：根据语言返回对应 ASR 后端"""
    # 延迟导入避免循环依赖
    from .whisper_asr import WhisperASR
    from .paddle_asr import PaddleASR

    if lang == "zh":
        return PaddleASR(config)
    elif lang in ("ja", "en"):
        return WhisperASR(lang, config)
    else:
        raise ValueError(f"Unsupported language: {lang}")
