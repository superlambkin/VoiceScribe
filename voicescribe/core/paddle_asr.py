"""PaddleSpeech 中文 ASR · Python 3.14 适配版 stub

⚠️ PaddleSpeech 官方仅支持 Python 3.10-3.12，本环境（3.14）不可用。
切换 Python 版本后，pip install paddlespeech 即可启用。
"""

from pathlib import Path
from typing import Callable, Optional

from .asr_backend import ASRBackend, Segment


class PaddleASR(ASRBackend):
    """⚠️ PaddleSpeech 中文 ASR stub（Python 3.14 不兼容）"""

    _UNSUPPORTED_MSG = (
        "PaddleSpeech 中文 ASR 当前环境（Python 3.14）不支持。\n"
        "解决：切换 Python 3.10-3.12 后执行：\n"
        "    pip install paddlespeech\n"
        "    python -m voicescribe.cli --download zh\n"
        "本 v1 仅支持 faster-whisper（日/英）后端。"
    )

    def __init__(self, config):
        self.config = config

    def transcribe(self, audio_path: Path, lang: str = "zh") -> list[Segment]:
        raise NotImplementedError(self._UNSUPPORTED_MSG)

    def is_model_ready(self) -> bool:
        return False

    def download_model(self, progress_callback: Optional[Callable[[float, str], None]] = None) -> None:
        raise NotImplementedError(self._UNSUPPORTED_MSG)
