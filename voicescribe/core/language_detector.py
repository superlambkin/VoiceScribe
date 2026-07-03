"""自动语言检测

v1 实现：仅基于文件名的启发式检测（_zh / _jp / _en 后缀）。
后续可扩展：用 Whisper 的 language detection（但需要先加载模型，违反懒加载）。
"""

from pathlib import Path


_ZH_PATTERNS = ("_zh", "_cn", "中文", "汉语")
_JA_PATTERNS = ("_jp", "_ja", "_japan", "日语", "日本")
_EN_PATTERNS = ("_en", "_eng", "英语", "英文")


def detect_language_from_path(path: Path) -> str:
    """基于文件名的语言检测（启发式）"""
    name = path.stem.lower()
    for pat in _ZH_PATTERNS:
        if pat.lower() in name:
            return "zh"
    for pat in _JA_PATTERNS:
        if pat.lower() in name:
            return "ja"
    for pat in _EN_PATTERNS:
        if pat.lower() in name:
            return "en"
    return "auto"


def detect_language(audio_path: Path) -> str:
    """综合语言检测（当前仅基于文件名）"""
    return detect_language_from_path(audio_path)