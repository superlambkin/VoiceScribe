"""faster-whisper 日/英 ASR"""
from pathlib import Path
from typing import Callable, Optional

from .asr_backend import ASRBackend, Segment


class WhisperASR(ASRBackend):
    def __init__(self, lang: str, config):
        self.lang = lang
        self.config = config
        self.model = None

    def transcribe(self, audio_path: Path, lang: str) -> list[Segment]:
        raise NotImplementedError

    def is_model_ready(self) -> bool:
        return False

    def download_model(self, progress_callback: Optional[Callable[[float, str], None]] = None) -> None:
        raise NotImplementedError
