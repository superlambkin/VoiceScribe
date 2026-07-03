"""输出格式器（TXT/MD/SRT/VTT）"""

from abc import ABC, abstractmethod
from pathlib import Path

from .asr_backend import Segment


class OutputFormatter(ABC):
    """输出格式抽象基类"""
    audio_path: Path = None
    lang: str = "auto"

    @abstractmethod
    def format(self, segments: list[Segment]) -> str:
        raise NotImplementedError

    @abstractmethod
    def extension(self) -> str:
        raise NotImplementedError


class TxtFormatter(OutputFormatter):
    """纯文本输出"""
    def format(self, segments: list[Segment]) -> str:
        return "\n".join(seg.text for seg in segments)

    def extension(self) -> str:
        return "txt"


class MdFormatter(OutputFormatter):
    """Markdown 输出（带元数据）"""
    def format(self, segments: list[Segment]) -> str:
        md = "# 转写结果\n\n"
        if self.audio_path:
            md += f"- 文件: {self.audio_path.name}\n"
        md += f"- 语言: {self.lang}\n"
        md += f"- 片段数: {len(segments)}\n\n"
        md += "## 内容\n\n"
        md += "\n\n".join(seg.text for seg in segments)
        return md

    def extension(self) -> str:
        return "md"


def _format_srt_time(t: float) -> str:
    """SRT 时间格式 HH:MM:SS,mmm"""
    h = int(t // 3600)
    m = int(t // 60 % 60)
    s = int(t % 60)
    ms = int((t - int(t)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _format_vtt_time(t: float) -> str:
    """WebVTT 时间格式 HH:MM:SS.mmm"""
    return _format_srt_time(t).replace(",", ".")


class SrtFormatter(OutputFormatter):
    """SRT 字幕输出"""
    def format(self, segments: list[Segment]) -> str:
        lines = []
        for i, seg in enumerate(segments, 1):
            lines.append(f"{i}\n")
            lines.append(f"{_format_srt_time(seg.start)} --> {_format_srt_time(seg.end)}\n")
            lines.append(f"{seg.text}\n\n")
        return "".join(lines)

    def extension(self) -> str:
        return "srt"


class VttFormatter(OutputFormatter):
    """WebVTT 字幕输出"""
    def format(self, segments: list[Segment]) -> str:
        lines = ["WEBVTT\n\n"]
        for i, seg in enumerate(segments, 1):
            lines.append(f"{i}\n")
            lines.append(f"{_format_vtt_time(seg.start)} --> {_format_vtt_time(seg.end)}\n")
            lines.append(f"{seg.text}\n\n")
        return "".join(lines)

    def extension(self) -> str:
        return "vtt"


FORMATTERS = {
    "txt": TxtFormatter,
    "md": MdFormatter,
    "srt": SrtFormatter,
    "vtt": VttFormatter,
}
