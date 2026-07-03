"""配置管理"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    """VoiceScribe 配置"""
    model_dir: Path = field(default_factory=lambda: Path.home() / ".voicescribe" / "models")
    output_dir: Path = field(default_factory=lambda: Path.cwd() / "output")
    log_level: str = "INFO"
    default_lang: str = "auto"
    whisper_model: str = "large-v3"
    whisper_compute_type: str = "int8"

    @classmethod
    def load(cls, config_path: Path = None) -> "Config":
        """加载配置（暂不实现 YAML 解析，使用默认值）"""
        return cls()
