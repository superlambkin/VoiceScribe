"""faster-whisper 日/英 ASR"""

from pathlib import Path
from typing import Callable, Optional

from .asr_backend import ASRBackend, Segment
from .config import Config


def _import_whisper_model():
    """延迟导入 faster_whisper（避免未安装时报错影响其他模块）"""
    try:
        from faster_whisper import WhisperModel
        return WhisperModel
    except ImportError as e:
        raise ImportError(
            "faster-whisper 未安装。请执行：pip install faster-whisper"
        ) from e


def _logprob_to_confidence(avg_logprob: float) -> float:
    """将 Whisper 的 avg_logprob（负数，越接近 0 越好）转换为 0-1 置信度"""
    # avg_logprob 通常在 [-1, 0] 之间
    # 简单线性映射：-1 → 0, 0 → 1
    clamped = max(-1.0, min(0.0, avg_logprob))
    return clamped + 1.0


class WhisperASR(ASRBackend):
    """faster-whisper 日/英 ASR（Whisper large-v3 量化版）"""

    def __init__(self, lang: str, config: Config):
        self.lang = lang
        self.config = config
        self.model = None  # 懒加载
        self._WhisperModel = None  # 类引用缓存

    def _ensure_model(self):
        """懒加载模型"""
        if self.model is None:
            if self._WhisperModel is None:
                self._WhisperModel = _import_whisper_model()
            self.model = self._WhisperModel(
                self.config.whisper_model,
                device="cpu",
                compute_type=self.config.whisper_compute_type,
            )

    def transcribe(self, audio_path: Path, lang: str) -> list[Segment]:
        """转写音频文件"""
        self._ensure_model()
        lang = lang or self.lang
        segments_iter, info = self.model.transcribe(
            str(audio_path),
            language=lang,
            beam_size=5,
        )
        return [
            Segment(
                start=seg.start,
                end=seg.end,
                text=seg.text.strip(),
                confidence=_logprob_to_confidence(seg.avg_logprob),
            )
            for seg in segments_iter
        ]

    def is_model_ready(self) -> bool:
        """检查 Whisper 模型目录是否存在且非空"""
        # faster-whisper 默认使用 HuggingFace 缓存
        # 我们也允许自定义 model_dir
        model_dir = self.config.model_dir / f"whisper-{self.config.whisper_model}"
        if not model_dir.exists():
            # 检查 HF 默认缓存
            hf_cache = Path.home() / ".cache" / "huggingface" / "hub"
            return hf_cache.exists() and any(hf_cache.iterdir())
        return any(model_dir.iterdir())

    def download_model(self, progress_callback: Optional[Callable[[float, str], None]] = None) -> None:
        """触发 Whisper 模型下载"""
        if progress_callback:
            progress_callback(0, f"开始下载 {self.config.whisper_model}...")
        self._WhisperModel = _import_whisper_model()
        # 实例化即触发下载
        self.model = self._WhisperModel(
            self.config.whisper_model,
            device="cpu",
            compute_type=self.config.whisper_compute_type,
        )
        if progress_callback:
            progress_callback(1.0, "下载完成")
