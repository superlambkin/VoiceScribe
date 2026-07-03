# VoiceScribe v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 基于 R03 VoiceScribe 设计文档 v1.0，交付一个可在 Python 3.14 环境下运行、whisper 日英 ASR 完整的 v1.0 CLI 工具（含 GUI 骨架）。

**Architecture:** Python 包 `voicescribe/`，core 层（asr 抽象 + whisper + io + config + 高级模块）共享给 CLI 和 GUI。CLI 走 Click + rich，GUI 走 Tkinter + tkinterdnd2。pytest 单元测试覆盖核心模块。

**Tech Stack:** Python 3.14.5, click 8.x, rich 13.x, faster-whisper 0.10+, soundfile, numpy, watchdog 4.x, PyYAML 6.x, pytest 7.x, tkinter + tkinterdnd2 0.4.0

---

## Global Constraints

[From spec — applies to every task unless explicitly overridden]

- **Python version:** 3.14.5（唯一可用版本）
- **Working directory:** `D:\AI-Agent\MyWisper-PaddleSpeech\`（git 仓库根）
- **Package name:** `voicescribe`（顶层目录保留 `MyWisper-PaddleSpeech`）
- **Product name:** VoiceScribe
- **OB project folder:** `C:\Users\superlambkin\OneDrive\Edge\Obsidian Vault\80_POC_Projects\POC_012_VoiceScribe\`（OB 侧设计归档，由 OB 模板填充任务单独处理，不在 v1 代码交付范围）
- **Python 3.14 incompatibility:** PaddleSpeech 中文 ASR 仅 stub（导入时清晰报错），仅 faster-whisper 后端真实可用
- **License:** MIT
- **Code style:** Match R03 设计文档代码示例（type hints、docstring、ABC 抽象）
- **Commit message format:** `Phase X: <description>` (A/B1/B2/B3/B4/C 各自一个)
- **OB 规范:** 所有写入 OB 的 MD 必须遵循用户全局 CLAUDE.md 的 Obsidian 规范（OB 侧由专门 subagent 处理）

---

## Task 1: 项目初始化 + git 仓库

**Files:**
- Create: `D:\AI-Agent\MyWisper-PaddleSpeech\.gitignore`
- Create: `D:\AI-Agent\MyWisper-PaddleSpeech\README.md`
- Create: `D:\AI-Agent\MyWisper-PaddleSpeech\LICENSE`
- Create: `D:\AI-Agent\MyWisper-PaddleSpeech\pyproject.toml`

**Interfaces:**
- Consumes: 无
- Produces: 可用的 git 仓库 + Python 项目元数据

### Step 1.1: git init

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
git init
git config user.email "voicescribe@local"
git config user.name "VoiceScribe Dev"
```

### Step 1.2: 写 .gitignore

**File:** `D:\AI-Agent\MyWisper-PaddleSpeech\.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.eggs/
.pytest_cache/
.coverage
htmlcov/

# 虚拟环境
venv/
.venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 模型缓存（懒下载）
models/

# 用户配置
config.yaml
voicescribe.log

# OS
.DS_Store
Thumbs.db

# 测试音频
tests/fixtures/audio/
```

### Step 1.3: 写 LICENSE (MIT)

**File:** `D:\AI-Agent\MyWisper-PaddleSpeech\LICENSE`

```
MIT License

Copyright (c) 2026 VoiceScribe Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Step 1.4: 写 pyproject.toml

**File:** `D:\AI-Agent\MyWisper-PaddleSpeech\pyproject.toml`

```toml
[project]
name = "voicescribe"
version = "0.1.0"
description = "VoiceScribe · 离线音频转文字工具（CLI + GUI）"
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.14"
authors = [
    { name = "VoiceScribe Dev" }
]

dependencies = [
    "click>=8.1",
    "rich>=13.0",
    "faster-whisper>=0.10",
    "soundfile>=0.12",
    "numpy>=1.26",
    "watchdog>=4.0",
    "PyYAML>=6.0",
    "tkinterdnd2>=0.4.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "pytest-cov>=4.1",
]

[project.scripts]
voicescribe = "voicescribe.cli:main"
voicescribe-gui = "voicescribe.gui:main"

[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["."]
include = ["voicescribe*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short"
```

### Step 1.5: 写 README.md

**File:** `D:\AI-Agent\MyWisper-PaddleSpeech\README.md`

```markdown
# 🎙️ VoiceScribe

> 离线音频转文字工具 · 中日英多语言 · CLI + GUI 双模式 · Python 3.14

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](pyproject.toml)

## 快速开始

```bash
# 安装依赖（需要 Python 3.14）
pip install -e .

# CLI 转写（首次使用会下载模型）
voicescribe meeting_jp.mp3 -l ja -f srt,txt

# 启动 GUI
voicescribe-gui
```

## 状态

⚠️ **v0.1.0 - Python 3.14 适配版**
- ✅ faster-whisper 日/英 ASR 完整支持
- ❌ PaddleSpeech 中文 ASR 暂不可用（Python 3.14 兼容性，详见 docs/）

## 文档

- 设计文档：`docs/superpowers/specs/2026-07-04-voicescribe-implementation-design.md`
- 上游设计：R03 PaddleSpeech Research / 07-POC参考

## License

MIT
```

### Step 1.6: 首次 commit

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
git add .gitignore LICENSE pyproject.toml README.md
git commit -m "Phase 1: project init (git + pyproject + README + LICENSE)"
```

**Verify:** `git log --oneline` 应显示 1 个 commit。

---

## Task 2: 骨架 + 接口契约（Phase A）

**Files:**
- Create: `voicescribe/__init__.py`
- Create: `voicescribe/__version__.py`
- Create: `voicescribe/cli.py` (空骨架 + main 占位)
- Create: `voicescribe/gui.py` (空骨架 + main 占位)
- Create: `voicescribe/core/__init__.py`
- Create: `voicescribe/core/config.py` (Config dataclass 骨架)
- Create: `voicescribe/core/asr_backend.py` (完整 ASRBackend + Segment + 工厂)
- Create: `voicescribe/core/whisper_asr.py` (空骨架)
- Create: `voicescribe/core/paddle_asr.py` (完整 stub)
- Create: `voicescribe/core/audio_loader.py` (空骨架)
- Create: `voicescribe/core/language_detector.py` (空骨架)
- Create: `voicescribe/core/output_formats.py` (完整 FORMATTERS dict + 4 个 Formatter 类)
- Create: `voicescribe/core/batch_processor.py` (空骨架)
- Create: `voicescribe/core/file_watcher.py` (空骨架)
- Create: `voicescribe/ui/__init__.py`
- Create: `voicescribe/ui/main_window.py` (空骨架)
- Create: `voicescribe/ui/drop_zone.py` (空骨架)
- Create: `voicescribe/ui/queue_panel.py` (空骨架)
- Create: `voicescribe/ui/preview_panel.py` (空骨架)
- Create: `voicescribe/ui/progress_bar.py` (空骨架)
- Create: `voicescribe/ui/widgets.py` (空骨架)
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`
- Create: `tests/test_asr_backend.py` (空骨架)
- Create: `tests/test_whisper_asr.py` (空骨架)
- Create: `tests/test_output_formats.py` (空骨架)
- Create: `tests/test_batch_processor.py` (空骨架)
- Create: `tests/test_audio_loader.py` (空骨架)
- Create: `tests/test_language_detector.py` (空骨架)
- Create: `tests/test_cli.py` (空骨架)

**Interfaces:**
- Consumes: 无（这是 Phase A，所有骨架）
- Produces:
  - `voicescribe.core.asr_backend.ASRBackend`（ABC）
  - `voicescribe.core.asr_backend.Segment`（dataclass: start, end, text, confidence）
  - `voicescribe.core.asr_backend.get_asr_backend(lang, config)`（工厂函数）
  - `voicescribe.core.config.Config`（dataclass: model_dir, output_dir, log_level, etc.）
  - `voicescribe.core.output_formats.FORMATTERS`（dict: txt/md/srt/vtt → Formatter 类）
  - `voicescribe.cli.main()`（Click entry）
  - `voicescribe.gui.main()`（Tk entry）

### Step 2.1: 写 `voicescribe/__init__.py`

```python
"""VoiceScribe · 离线音频转文字工具"""

from .__version__ import __version__

__all__ = ["__version__"]
```

### Step 2.2: 写 `voicescribe/__version__.py`

```python
"""VoiceScribe 版本号"""

__version__ = "0.1.0"
```

### Step 2.3: 写 `voicescribe/core/__init__.py`

```python
"""核心业务层（CLI/GUI 共享）"""
```

### Step 2.4: 写 `voicescribe/core/asr_backend.py`（完整接口契约）

```python
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
```

### Step 2.5: 写 `voicescribe/core/paddle_asr.py`（完整 stub）

```python
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
```

### Step 2.6: 写 `voicescribe/core/config.py`（Config dataclass 完整骨架）

```python
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
```

### Step 2.7: 写 `voicescribe/core/output_formats.py`（完整 Formatter 接口）

```python
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
```

### Step 2.8: 写空骨架文件（一次性创建所有剩余文件）

每个空骨架文件遵循以下模式（仅写最小占位代码）：

**`voicescribe/cli.py`**：
```python
"""CLI 入口"""
import click


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
def main(input_path):
    """VoiceScribe · 离线音频转文字工具"""
    click.echo(f"voicescribe v0.1.0 (placeholder): {input_path}")


if __name__ == "__main__":
    main()
```

**`voicescribe/gui.py`**：
```python
"""GUI 入口"""
import tkinter as tk


def main():
    """启动 VoiceScribe GUI"""
    root = tk.Tk()
    root.title("VoiceScribe")
    root.geometry("300x100")
    tk.Label(root, text="VoiceScribe GUI placeholder").pack()
    root.mainloop()


if __name__ == "__main__":
    main()
```

**`voicescribe/core/whisper_asr.py`**：
```python
"""faster-whisper 日/英 ASR"""
from pathlib import Path
from typing import Callable, Optional

from .asr_backend import ASRBackend, Segment


class WhisperASR(ASRBackend):
    def __init__(self, lang: str, config):
        self.lang = lang
        self.config = config
        self.model = None

    def transcribe(self, audio_path: Path, lang: str = None) -> list[Segment]:
        raise NotImplementedError

    def is_model_ready(self) -> bool:
        return False

    def download_model(self, progress_callback: Optional[Callable[[float, str], None]] = None) -> None:
        raise NotImplementedError
```

**所有 `voicescribe/core/` 和 `voicescribe/ui/` 空骨架文件**（除上面 3 个 + asr_backend + paddle_asr + config + output_formats 已写）：

```python
"""<module name> · skeleton"""
# 实现将在对应 Phase B 子任务中完成
raise NotImplementedError("<module> not implemented yet")
```

适用文件：
- `voicescribe/core/audio_loader.py`
- `voicescribe/core/language_detector.py`
- `voicescribe/core/batch_processor.py`
- `voicescribe/core/file_watcher.py`
- `voicescribe/ui/__init__.py`
- `voicescribe/ui/main_window.py`
- `voicescribe/ui/drop_zone.py`
- `voicescribe/ui/queue_panel.py`
- `voicescribe/ui/preview_panel.py`
- `voicescribe/ui/progress_bar.py`
- `voicescribe/ui/widgets.py`

**所有 `tests/` 空骨架文件**（除下面 Step 2.10 的 test_output_formats.py 测试）：

```python
"""测试 <module>"""
# 测试将在对应 Phase B 子任务中添加
```

适用文件：
- `tests/__init__.py`
- `tests/conftest.py`
- `tests/test_asr_backend.py`
- `tests/test_whisper_asr.py`
- `tests/test_batch_processor.py`
- `tests/test_audio_loader.py`
- `tests/test_language_detector.py`
- `tests/test_cli.py`

### Step 2.9: 写 `tests/test_output_formats.py`（TDD：先写测试）

**File:** `tests/test_output_formats.py`

```python
"""output_formats 模块的单元测试"""

import pytest

from voicescribe.core.asr_backend import Segment
from voicescribe.core.output_formats import (
    FORMATTERS,
    TxtFormatter,
    MdFormatter,
    SrtFormatter,
    VttFormatter,
    _format_srt_time,
    _format_vtt_time,
)


# ----- TxtFormatter -----

def test_txt_formatter_returns_text():
    segs = [Segment(0.0, 5.0, "你好", 1.0), Segment(5.0, 10.0, "世界", 1.0)]
    f = TxtFormatter()
    result = f.format(segs)
    assert result == "你好\n世界"


def test_txt_formatter_extension():
    assert TxtFormatter().extension() == "txt"


# ----- MdFormatter -----

def test_md_formatter_includes_metadata():
    segs = [Segment(0.0, 5.0, "你好", 1.0)]
    f = MdFormatter()
    f.audio_path = None  # 测试不依赖 audio_path
    result = f.format(segs)
    assert "# 转写结果" in result
    assert "片段数: 1" in result
    assert "你好" in result


def test_md_formatter_extension():
    assert MdFormatter().extension() == "md"


# ----- SrtFormatter -----

def test_srt_formatter_produces_valid_srt():
    segs = [Segment(1.5, 3.5, "测试文本", 1.0)]
    result = SrtFormatter().format(segs)
    assert "1\n" in result
    assert "00:00:01,500 --> 00:00:03,500\n" in result
    assert "测试文本" in result


def test_srt_formatter_extension():
    assert SrtFormatter().extension() == "srt"


# ----- VttFormatter -----

def test_vtt_formatter_starts_with_webvtt():
    segs = [Segment(0.0, 2.0, "hello", 1.0)]
    result = VttFormatter().format(segs)
    assert result.startswith("WEBVTT")


def test_vtt_uses_dot_for_milliseconds():
    segs = [Segment(0.0, 2.5, "x", 1.0)]
    result = VttFormatter().format(segs)
    assert "00:00:00.000 --> 00:00:02.500" in result


def test_vtt_formatter_extension():
    assert VttFormatter().extension() == "vtt"


# ----- FORMATTERS dict -----

def test_formatters_dict_has_all_keys():
    assert set(FORMATTERS.keys()) == {"txt", "md", "srt", "vtt"}


def test_formatters_dict_returns_classes():
    for key, cls in FORMATTERS.items():
        assert callable(cls)


# ----- 时间格式化辅助 -----

def test_format_srt_time_zero():
    assert _format_srt_time(0) == "00:00:00,000"


def test_format_srt_time_complex():
    assert _format_srt_time(3725.123) == "01:02:05,123"


def test_format_vtt_uses_dot():
    assert _format_vtt_time(1.5) == "00:00:01.500"
```

### Step 2.10: 跑测试验证实现

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
pip install -e ".[dev]"
pytest tests/test_output_formats.py -v
```

**Expected:** 全部 12 个测试通过（因为 output_formats.py 已在 Step 2.7 完整实现）。

### Step 2.11: 验证导入

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
python -c "import voicescribe; print(voicescribe.__version__)"
python -c "from voicescribe.core.asr_backend import ASRBackend, Segment, get_asr_backend; print('OK')"
python -c "from voicescribe.core.paddle_asr import PaddleASR; print(PaddleASR.__name__)"
python -c "from voicescribe.core.output_formats import FORMATTERS; print(list(FORMATTERS.keys()))"
python -m voicescribe.cli --help
```

**Expected:**
- `0.1.0`
- `OK`
- `PaddleASR`
- `['txt', 'md', 'srt', 'vtt']`
- Click usage 输出

### Step 2.12: Commit

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
git add voicescribe/ tests/
git commit -m "Phase A: skeleton + interfaces (ASR/Segment/Formatter)"
```

---

## Task 3: ASR 后端实现（Phase B1）

**Files:**
- Modify: `voicescribe/core/whisper_asr.py`（实现 transcribe / is_model_ready / download_model）
- Modify: `tests/test_whisper_asr.py`（添加单元测试）
- Modify: `tests/test_asr_backend.py`（测试工厂函数）

**Interfaces:**
- Consumes:
  - `Config` (from `voicescribe.core.config`)
  - `ASRBackend`, `Segment` (from `voicescribe.core.asr_backend`)
- Produces:
  - `WhisperASR(lang: str, config: Config)` 实例
  - `WhisperASR.transcribe(audio_path: Path, lang: str = None) -> list[Segment]`
  - `WhisperASR.is_model_ready() -> bool`
  - `WhisperASR.download_model(progress_callback) -> None`

### Step 3.1: 写 `tests/test_asr_backend.py`（TDD 工厂函数测试）

**File:** `tests/test_asr_backend.py`

```python
"""asr_backend 模块的单元测试"""

import pytest
from pathlib import Path

from voicescribe.core.asr_backend import (
    ASRBackend,
    Segment,
    get_asr_backend,
)
from voicescribe.core.config import Config
from voicescribe.core.whisper_asr import WhisperASR
from voicescribe.core.paddle_asr import PaddleASR


def test_segment_dataclass():
    seg = Segment(start=0.0, end=1.5, text="hello", confidence=0.9)
    assert seg.start == 0.0
    assert seg.end == 1.5
    assert seg.text == "hello"
    assert seg.confidence == 0.9


def test_factory_returns_whisper_for_ja():
    config = Config()
    backend = get_asr_backend("ja", config)
    assert isinstance(backend, WhisperASR)
    assert backend.lang == "ja"


def test_factory_returns_whisper_for_en():
    config = Config()
    backend = get_asr_backend("en", config)
    assert isinstance(backend, WhisperASR)
    assert backend.lang == "en"


def test_factory_returns_paddle_for_zh():
    config = Config()
    backend = get_asr_backend("zh", config)
    assert isinstance(backend, PaddleASR)


def test_factory_raises_for_unsupported():
    config = Config()
    with pytest.raises(ValueError, match="Unsupported language"):
        get_asr_backend("xx", config)


def test_paddle_backend_unsupported_transcribe():
    """PaddleASR 在 3.14 上调用 transcribe 必须抛清晰错误"""
    backend = PaddleASR(Config())
    with pytest.raises(NotImplementedError, match="Python 3.14"):
        backend.transcribe(Path("fake.wav"), "zh")


def test_paddle_backend_is_model_ready_returns_false():
    assert PaddleASR(Config()).is_model_ready() is False


def test_paddle_backend_download_raises():
    with pytest.raises(NotImplementedError, match="Python 3.14"):
        PaddleASR(Config()).download_model()
```

### Step 3.2: 跑测试验证通过（这部分测试只验证工厂 + PaddleASR stub，已实现）

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
pytest tests/test_asr_backend.py -v
```

**Expected:** 7 个测试全部通过。

### Step 3.3: 写 `tests/test_whisper_asr.py`（TDD WhisperASR 测试）

**File:** `tests/test_whisper_asr.py`

```python
"""whisper_asr 模块的单元测试"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from voicescribe.core.asr_backend import Segment
from voicescribe.core.config import Config
from voicescribe.core.whisper_asr import WhisperASR


def test_whisper_init_stores_lang_and_config():
    config = Config(whisper_model="small")
    asr = WhisperASR("ja", config)
    assert asr.lang == "ja"
    assert asr.config.whisper_model == "small"
    assert asr.model is None  # 懒加载


def test_whisper_is_model_ready_false_when_no_dir():
    config = Config(model_dir=Path("/tmp/nonexistent_models_xyz"))
    asr = WhisperASR("ja", config)
    assert asr.is_model_ready() is False


def test_whisper_is_model_ready_true_when_dir_exists_with_files(tmp_path):
    model_dir = tmp_path / "whisper-large-v3"
    model_dir.mkdir()
    (model_dir / "model.bin").touch()
    config = Config(model_dir=tmp_path)
    asr = WhisperASR("ja", config)
    assert asr.is_model_ready() is True


def test_whisper_transcribe_lazy_loads_model(tmp_path):
    """首次转写触发模型加载"""
    fake_audio = tmp_path / "test.wav"
    fake_audio.touch()

    config = Config(whisper_model="tiny", whisper_compute_type="int8")

    # 模拟 faster_whisper.WhisperModel
    with patch("voicescribe.core.whisper_asr._import_whisper_model") as mock_import:
        mock_model = MagicMock()
        mock_segment = MagicMock()
        mock_segment.start = 0.0
        mock_segment.end = 1.5
        mock_segment.text = "こんにちは"
        mock_segment.avg_logprob = -0.1
        mock_model.transcribe.return_value = ([mock_segment], MagicMock())
        mock_import.return_value = mock_model

        asr = WhisperASR("ja", config)
        segments = asr.transcribe(fake_audio, "ja")

    assert len(segments) == 1
    assert segments[0].text == "こんにちは"
    assert segments[0].start == 0.0
    assert segments[0].end == 1.5
    # confidence 从 avg_logprob 转换
    assert 0.0 <= segments[0].confidence <= 1.0


def test_whisper_transcribe_reuses_loaded_model(tmp_path):
    """第二次转写复用已加载模型"""
    fake_audio = tmp_path / "test.wav"
    fake_audio.touch()
    config = Config(whisper_model="tiny")

    with patch("voicescribe.core.whisper_asr._import_whisper_model") as mock_import:
        mock_model = MagicMock()
        mock_model.transcribe.return_value = ([], MagicMock())
        mock_import.return_value = mock_model

        asr = WhisperASR("ja", config)
        asr.transcribe(fake_audio, "ja")
        asr.transcribe(fake_audio, "ja")

    # _import_whisper_model 只调用一次
    assert mock_import.call_count == 1
```

### Step 3.4: 实现 `voicescribe/core/whisper_asr.py`

**File:** `voicescribe/core/whisper_asr.py`（完整实现，替换 Step 2.8 的骨架）

```python
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

    def transcribe(self, audio_path: Path, lang: str = None) -> list[Segment]:
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
```

### Step 3.5: 跑测试

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
pytest tests/test_whisper_asr.py tests/test_asr_backend.py -v
```

**Expected:** 12 个测试全部通过（7 from test_asr_backend + 5 from test_whisper_asr）。

### Step 3.6: Commit

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
git add voicescribe/core/whisper_asr.py tests/test_whisper_asr.py tests/test_asr_backend.py
git commit -m "Phase B1: ASR backends (Whisper + PaddleASR stub)"
```

---

## Task 4: I/O 工具模块（Phase B2）

**Files:**
- Modify: `voicescribe/core/audio_loader.py`（完整实现）
- Modify: `voicescribe/core/language_detector.py`（完整实现）
- Modify: `tests/test_audio_loader.py`
- Modify: `tests/test_language_detector.py`

**Interfaces:**
- Consumes: `pathlib.Path`
- Produces:
  - `audio_loader.load_audio(path: Path) -> tuple[int, np.ndarray]`（采样率 + 音频数据）
  - `audio_loader.get_duration(path: Path) -> float`
  - `audio_loader.SUPPORTED_EXTENSIONS` (frozenset)
  - `language_detector.detect_language(path: Path) -> str`（返回 "zh"/"ja"/"en"/"auto"）
  - `language_detector.detect_language_from_path(path: Path) -> str`（基于文件名启发式）

### Step 4.1: 写 `tests/test_audio_loader.py`

**File:** `tests/test_audio_loader.py`

```python
"""audio_loader 模块的单元测试"""

import numpy as np
import pytest
import soundfile as sf
from pathlib import Path

from voicescribe.core.audio_loader import (
    SUPPORTED_EXTENSIONS,
    load_audio,
    get_duration,
)


def test_supported_extensions_includes_common():
    assert ".wav" in SUPPORTED_EXTENSIONS
    assert ".mp3" in SUPPORTED_EXTENSIONS
    assert ".m4a" in SUPPORTED_EXTENSIONS
    assert ".flac" in SUPPORTED_EXTENSIONS


def test_load_audio_returns_tuple(tmp_path):
    """加载 WAV 文件返回 (sample_rate, audio_data)"""
    audio_path = tmp_path / "test.wav"
    sample_rate = 16000
    duration = 1.0
    audio_data = np.random.randn(int(sample_rate * duration)).astype(np.float32) * 0.1
    sf.write(str(audio_path), audio_data, sample_rate)

    sr, data = load_audio(audio_path)
    assert sr == sample_rate
    assert isinstance(data, np.ndarray)
    assert len(data) == int(sample_rate * duration)


def test_load_audio_unsupported_extension(tmp_path):
    fake = tmp_path / "test.xyz"
    fake.touch()
    with pytest.raises(ValueError, match="Unsupported audio format"):
        load_audio(fake)


def test_load_audio_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_audio(tmp_path / "nonexistent.wav")


def test_get_duration_short_wav(tmp_path):
    audio_path = tmp_path / "short.wav"
    sr = 16000
    data = np.zeros(sr * 2, dtype=np.float32)  # 2 秒静音
    sf.write(str(audio_path), data, sr)
    duration = get_duration(audio_path)
    assert 1.9 < duration < 2.1
```

### Step 4.2: 跑测试（首次应该失败：audio_loader 还是骨架）

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
pytest tests/test_audio_loader.py -v
```

**Expected:** 5 个测试全部 FAIL（"module not implemented yet"）。

### Step 4.3: 实现 `voicescribe/core/audio_loader.py`

**File:** `voicescribe/core/audio_loader.py`

```python
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
```

### Step 4.4: 跑测试验证

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
pytest tests/test_audio_loader.py -v
```

**Expected:** 5 个测试全部通过。

### Step 4.5: 写 `tests/test_language_detector.py`

**File:** `tests/test_language_detector.py`

```python
"""language_detector 模块的单元测试"""

from pathlib import Path

from voicescribe.core.language_detector import detect_language_from_path


def test_detect_chinese_from_path():
    assert detect_language_from_path(Path("meeting_zh.wav")) == "zh"


def test_detect_japanese_from_path():
    assert detect_language_from_path(Path("meeting_jp.mp3")) == "ja"


def test_detect_japanese_from_japanese_name():
    assert detect_language_from_path(Path("会议_jp.wav")) == "ja"


def test_detect_english_from_path():
    assert detect_language_from_path(Path("podcast_en.m4a")) == "en"


def test_detect_returns_auto_for_unknown():
    """无法识别时返回 'auto'"""
    assert detect_language_from_path(Path("unknown_file.wav")) == "auto"
```

### Step 4.6: 实现 `voicescribe/core/language_detector.py`

**File:** `voicescribe/core/language_detector.py`

```python
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
```

### Step 4.7: 跑测试

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
pytest tests/test_language_detector.py -v
```

**Expected:** 5 个测试全部通过。

### Step 4.8: Commit

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
git add voicescribe/core/audio_loader.py voicescribe/core/language_detector.py tests/test_audio_loader.py tests/test_language_detector.py
git commit -m "Phase B2: I/O tools (audio_loader + language_detector)"
```

---

## Task 5: 高级模块（Phase B3）

**Files:**
- Modify: `voicescribe/core/batch_processor.py`（完整实现）
- Modify: `voicescribe/core/file_watcher.py`（完整实现）
- Modify: `tests/test_batch_processor.py`

**Interfaces:**
- Consumes: `Config`, `Segment`, `FORMATTERS`, `Path`
- Produces:
  - `batch_processor.process_batch(input_dir: Path, lang: str, output_dir: Path, formats: list[str], config: Config) -> dict`
  - `file_watcher.watch_folder(folder: Path, lang: str, formats: list[str], config: Config) -> None`

### Step 5.1: 写 `tests/test_batch_processor.py`

**File:** `tests/test_batch_processor.py`

```python
"""batch_processor 模块的单元测试"""

from pathlib import Path
from unittest.mock import patch, MagicMock

import numpy as np
import pytest
import soundfile as sf

from voicescribe.core.asr_backend import Segment
from voicescribe.core.batch_processor import process_batch
from voicescribe.core.config import Config


def _make_wav(path: Path, duration: float = 1.0, sr: int = 16000):
    data = np.zeros(int(sr * duration), dtype=np.float32)
    sf.write(str(path), data, sr)


def test_process_batch_empty_dir(tmp_path):
    """空目录处理应该返回 0 个文件"""
    result = process_batch(
        input_dir=tmp_path,
        lang="ja",
        output_dir=tmp_path / "out",
        formats=["txt"],
        config=Config(),
    )
    assert result["total"] == 0
    assert result["succeeded"] == 0
    assert result["failed"] == 0


def test_process_batch_skips_unsupported_files(tmp_path):
    """非音频文件被跳过"""
    (tmp_path / "readme.txt").write_text("not audio")
    result = process_batch(
        input_dir=tmp_path,
        lang="ja",
        output_dir=tmp_path / "out",
        formats=["txt"],
        config=Config(),
    )
    assert result["total"] == 0


def test_process_batch_one_file(tmp_path):
    """处理单个 WAV 文件（mock ASR）"""
    audio = tmp_path / "meeting.wav"
    _make_wav(audio)

    mock_segments = [Segment(0.0, 1.0, "テスト", 1.0)]

    with patch("voicescribe.core.batch_processor._run_transcription") as mock_run:
        mock_run.return_value = mock_segments
        result = process_batch(
            input_dir=tmp_path,
            lang="ja",
            output_dir=tmp_path / "out",
            formats=["txt"],
            config=Config(),
        )

    assert result["total"] == 1
    assert result["succeeded"] == 1
    assert result["failed"] == 0
    # 输出文件存在
    assert (tmp_path / "out" / "meeting.txt").exists()
    assert (tmp_path / "out" / "meeting.txt").read_text(encoding="utf-8") == "テスト"


def test_process_batch_multiple_formats(tmp_path):
    """多种输出格式"""
    audio = tmp_path / "podcast.wav"
    _make_wav(audio)

    mock_segments = [Segment(0.0, 1.0, "hello", 1.0)]

    with patch("voicescribe.core.batch_processor._run_transcription") as mock_run:
        mock_run.return_value = mock_segments
        result = process_batch(
            input_dir=tmp_path,
            lang="en",
            output_dir=tmp_path / "out",
            formats=["txt", "srt", "md"],
            config=Config(),
        )

    assert result["succeeded"] == 1
    assert (tmp_path / "out" / "podcast.txt").exists()
    assert (tmp_path / "out" / "podcast.srt").exists()
    assert (tmp_path / "out" / "podcast.md").exists()


def test_process_batch_continues_on_failure(tmp_path):
    """单个文件失败不影响其他"""
    audio1 = tmp_path / "good.wav"
    audio2 = tmp_path / "bad.wav"
    _make_wav(audio1)
    _make_wav(audio2)

    def mock_run_side_effect(audio_path, lang, config):
        if "bad" in str(audio_path):
            raise RuntimeError("mock failure")
        return [Segment(0.0, 1.0, "ok", 1.0)]

    with patch("voicescribe.core.batch_processor._run_transcription") as mock_run:
        mock_run.side_effect = mock_run_side_effect
        result = process_batch(
            input_dir=tmp_path,
            lang="en",
            output_dir=tmp_path / "out",
            formats=["txt"],
            config=Config(),
        )

    assert result["total"] == 2
    assert result["succeeded"] == 1
    assert result["failed"] == 1
    assert "good.wav" in result["success_files"]
    assert "bad.wav" in result["failed_files"]
```

### Step 5.2: 跑测试（应失败）

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
pytest tests/test_batch_processor.py -v
```

**Expected:** 5 个测试全部 FAIL（batch_processor 还是骨架）。

### Step 5.3: 实现 `voicescribe/core/batch_processor.py`

**File:** `voicescribe/core/batch_processor.py`

```python
"""批量处理：递归扫描文件夹，转写所有音频文件"""

from pathlib import Path
from typing import Optional

import click

from .asr_backend import Segment, get_asr_backend
from .audio_loader import SUPPORTED_EXTENSIONS
from .config import Config
from .output_formats import FORMATTERS
from .language_detector import detect_language_from_path


def _run_transcription(audio_path: Path, lang: str, config: Config) -> list[Segment]:
    """运行单文件转写（统一入口，便于 mock）"""
    backend = get_asr_backend(lang, config)
    if not backend.is_model_ready():
        click.echo(f"⏳ 首次使用 {lang} 模型，下载中...")
        backend.download_model()
    return backend.transcribe(audio_path, lang)


def process_batch(
    input_dir: Path,
    lang: str,
    output_dir: Path,
    formats: list[str],
    config: Config,
) -> dict:
    """批量处理目录中的所有音频文件"""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 扫描音频文件
    audio_files = sorted(
        f for f in input_dir.rglob("*")
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    total = len(audio_files)
    if total == 0:
        click.echo(f"⚠️ 目录 {input_dir} 中没有找到音频文件")
        return {"total": 0, "succeeded": 0, "failed": 0,
                "success_files": [], "failed_files": []}

    click.echo(f"📁 找到 {total} 个音频文件")

    succeeded = 0
    failed = 0
    success_files = []
    failed_files = []

    for i, audio_path in enumerate(audio_files, 1):
        click.echo(f"\n[{i}/{total}] 处理 {audio_path.name}")

        # 单文件语言检测
        file_lang = lang if lang != "auto" else detect_language_from_path(audio_path)
        if file_lang == "auto":
            click.echo(f"  ⚠️ 无法识别语言（文件名无 _zh/_jp/_en 后缀），默认用 ja")
            file_lang = "ja"

        try:
            segments = _run_transcription(audio_path, file_lang, config)

            # 多格式输出
            for fmt in formats:
                formatter_class = FORMATTERS[fmt]
                formatter = formatter_class()
                formatter.audio_path = audio_path
                formatter.lang = file_lang
                output_path = output_dir / f"{audio_path.stem}.{fmt}"
                output_path.write_text(formatter.format(segments), encoding="utf-8")
                click.echo(f"  ✅ {output_path.name}")

            succeeded += 1
            success_files.append(audio_path.name)

        except Exception as e:
            click.echo(f"  ❌ 失败: {e}")
            failed += 1
            failed_files.append(audio_path.name)

    click.echo(f"\n📊 批量处理完成: 成功 {succeeded}, 失败 {failed}")
    return {
        "total": total,
        "succeeded": succeeded,
        "failed": failed,
        "success_files": success_files,
        "failed_files": failed_files,
    }
```

### Step 5.4: 实现 `voicescribe/core/file_watcher.py`

**File:** `voicescribe/core/file_watcher.py`

```python
"""文件监控：使用 watchdog 监听文件夹，新文件自动转写"""

from pathlib import Path
from typing import Optional

import click
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .audio_loader import SUPPORTED_EXTENSIONS
from .batch_processor import _run_transcription
from .config import Config
from .output_formats import FORMATTERS
from .language_detector import detect_language_from_path


class AudioFileHandler(FileSystemEventHandler):
    """音频文件事件处理器"""

    def __init__(self, lang: str, formats: list[str], output_dir: Path, config: Config):
        self.lang = lang
        self.formats = formats
        self.output_dir = output_dir
        self.config = config
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            return

        click.echo(f"🆕 检测到新文件: {path.name}")
        # 等 1 秒确保文件写入完成
        import time
        time.sleep(1)

        file_lang = self.lang if self.lang != "auto" else detect_language_from_path(path)
        if file_lang == "auto":
            file_lang = "ja"

        try:
            segments = _run_transcription(path, file_lang, self.config)
            for fmt in self.formats:
                formatter = FORMATTERS[fmt]()
                formatter.audio_path = path
                formatter.lang = file_lang
                output_path = self.output_dir / f"{path.stem}.{fmt}"
                output_path.write_text(formatter.format(segments), encoding="utf-8")
                click.echo(f"  ✅ {output_path.name}")
        except Exception as e:
            click.echo(f"  ❌ 处理失败: {e}")


def watch_folder(folder: Path, lang: str, formats: list[str], config: Config) -> None:
    """监控文件夹，新音频文件自动转写"""
    folder = Path(folder).resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a directory: {folder}")

    click.echo(f"👀 监控文件夹: {folder}")
    click.echo(f"   语言: {lang}, 格式: {', '.join(formats)}")
    click.echo("   按 Ctrl+C 停止...")

    event_handler = AudioFileHandler(lang, formats, config.output_dir, config)
    observer = Observer()
    observer.schedule(event_handler, str(folder), recursive=False)
    observer.start()

    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        click.echo("\n👋 停止监控")
    observer.join()
```

### Step 5.5: 跑测试验证

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
pytest tests/test_batch_processor.py -v
```

**Expected:** 5 个测试全部通过。

### Step 5.6: Commit

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
git add voicescribe/core/batch_processor.py voicescribe/core/file_watcher.py tests/test_batch_processor.py
git commit -m "Phase B3: advanced modules (batch_processor + file_watcher)"
```

---

## Task 6: CLI 实现（Phase B4）

**Files:**
- Modify: `voicescribe/cli.py`（完整 Click 实现）
- Modify: `tests/test_cli.py`（Click CliRunner 测试）

**Interfaces:**
- Consumes: 全部 core 模块
- Produces: `voicescribe.cli.main` (Click 命令)

### Step 6.1: 写 `tests/test_cli.py`

**File:** `tests/test_cli.py`

```python
"""CLI 模块的单元测试"""

from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest
import soundfile as sf
from click.testing import CliRunner

from voicescribe.cli import main


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "VoiceScribe" in result.output


def test_cli_nonexistent_file():
    runner = CliRunner()
    result = runner.invoke(main, ["/nonexistent/file.wav"])
    # click.Path(exists=True) 会在参数解析时报错
    assert result.exit_code != 0


def _make_wav(path: Path):
    data = np.zeros(16000, dtype=np.float32)
    sf.write(str(path), data, 16000)


def test_cli_single_file_txt_output(tmp_path):
    audio = tmp_path / "test.wav"
    _make_wav(audio)
    output = tmp_path / "out.txt"

    mock_segments = [
        # Segment(start, end, text, confidence)
    ]

    from voicescribe.core.asr_backend import Segment
    mock_segments = [Segment(0.0, 1.0, "テスト音声", 1.0)]

    with patch("voicescribe.cli._run_transcription") as mock_run:
        mock_run.return_value = mock_segments
        runner = CliRunner()
        result = runner.invoke(main, [
            str(audio), "-l", "ja", "-f", "txt", "-o", str(output),
        ])

    assert result.exit_code == 0, f"CLI failed: {result.output}"
    assert output.exists()
    assert output.read_text(encoding="utf-8") == "テスト音声"


def test_cli_multiple_formats(tmp_path):
    audio = tmp_path / "multi.wav"
    _make_wav(audio)

    from voicescribe.core.asr_backend import Segment
    mock_segments = [Segment(0.0, 1.0, "hello world", 1.0)]

    with patch("voicescribe.cli._run_transcription") as mock_run:
        mock_run.return_value = mock_segments
        runner = CliRunner()
        result = runner.invoke(main, [
            str(audio), "-l", "en", "-f", "txt,srt",
        ])

    assert result.exit_code == 0
    assert (audio.parent / "multi.txt").exists()
    assert (audio.parent / "multi.srt").exists()


def test_cli_batch_mode(tmp_path):
    """--batch 处理目录"""
    audio1 = tmp_path / "a.wav"
    audio2 = tmp_path / "b.wav"
    _make_wav(audio1)
    _make_wav(audio2)

    from voicescribe.core.asr_backend import Segment
    mock_segments = [Segment(0.0, 1.0, "test", 1.0)]

    with patch("voicescribe.cli._run_transcription") as mock_run:
        mock_run.return_value = mock_segments
        runner = CliRunner()
        result = runner.invoke(main, [
            str(tmp_path), "-l", "ja", "--batch", "-f", "txt",
        ])

    assert result.exit_code == 0
    assert (tmp_path / "out" / "a.txt").exists()
    assert (tmp_path / "out" / "b.txt").exists()


def test_cli_paddle_zh_gives_friendly_error(tmp_path):
    """中文 ASR 应给出清晰的 Python 3.14 错误"""
    audio = tmp_path / "cn.wav"
    _make_wav(audio)

    runner = CliRunner()
    result = runner.invoke(main, [str(audio), "-l", "zh"])

    assert result.exit_code != 0
    assert "Python 3.14" in result.output
```

### Step 6.2: 跑测试（应失败）

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
pytest tests/test_cli.py -v
```

**Expected:** 6 个测试大部分 FAIL（CLI 还没实现）。

### Step 6.3: 实现 `voicescribe/cli.py`

**File:** `voicescribe/cli.py`（替换 Step 2.8 的骨架）

```python
"""VoiceScribe CLI 入口"""

from pathlib import Path
from typing import Optional

import click

from .__version__ import __version__
from .core.asr_backend import get_asr_backend
from .core.audio_loader import SUPPORTED_EXTENSIONS
from .core.batch_processor import _run_transcription, process_batch
from .core.config import Config
from .core.file_watcher import watch_folder
from .core.language_detector import detect_language_from_path
from .core.output_formats import FORMATTERS


def _process_single(
    audio_path: Path,
    lang: str,
    output: Optional[Path],
    formats: list[str],
    config: Config,
) -> None:
    """处理单个音频文件"""
    # 语言检测
    if lang == "auto":
        detected = detect_language_from_path(audio_path)
        if detected == "auto":
            detected = "ja"  # 默认 fallback
            click.echo(f"⚠️ 无法识别语言，默认用 ja")
        lang = detected
        click.echo(f"🔍 检测到语言: {lang}")

    # 检查文件格式
    if audio_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise click.ClickException(
            f"不支持的音频格式: {audio_path.suffix}. "
            f"支持的格式: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    # 转写
    click.echo(f"🎙️ 正在转写 {audio_path.name}...")
    try:
        segments = _run_transcription(audio_path, lang, config)
    except NotImplementedError as e:
        raise click.ClickException(str(e))

    click.echo(f"✅ 转写完成: {len(segments)} 个片段")

    # 多格式输出
    for fmt in formats:
        formatter = FORMATTERS[fmt]()
        formatter.audio_path = audio_path
        formatter.lang = lang
        formatted = formatter.format(segments)

        if output and len(formats) == 1:
            output_path = output
        else:
            output_path = audio_path.with_suffix(f".{fmt}")

        output_path.write_text(formatted, encoding="utf-8")
        click.echo(f"  📄 {output_path}")


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option(
    "-l", "--lang",
    default="auto",
    type=click.Choice(["zh", "ja", "en", "auto"]),
    help="语言代码（默认 auto，自动检测）",
)
@click.option(
    "-o", "--output",
    type=click.Path(),
    default=None,
    help="输出文件路径（仅单文件 + 单格式时生效）",
)
@click.option(
    "-f", "--format", "formats",
    default="txt",
    help="输出格式（逗号分隔：txt,md,srt,vtt）",
)
@click.option(
    "--batch", "batch_mode",
    is_flag=True,
    help="批量模式（处理整个目录）",
)
@click.option(
    "--watch",
    is_flag=True,
    help="监控模式（新文件自动转写）",
)
@click.option(
    "--gui",
    is_flag=True,
    help="启动 GUI 模式",
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="详细日志",
)
@click.version_option(version=__version__, prog_name="voicescribe")
def main(input_path, lang, output, formats, batch_mode, watch, gui, verbose):
    """VoiceScribe · 离线音频转文字工具

    INPUT_PATH: 音频文件（WAV/FLAC/OGG）或文件夹路径

    示例：

      voicescribe meeting.wav -l ja -f srt,txt

      voicescribe recordings/ -l en --batch

      voicescribe ./new_recordings --watch -l ja
    """
    if gui:
        from .gui import main as gui_main
        gui_main()
        return

    config = Config.load()
    formats_list = [f.strip() for f in formats.split(",")]
    invalid = [f for f in formats_list if f not in FORMATTERS]
    if invalid:
        raise click.ClickException(
            f"无效的输出格式: {', '.join(invalid)}. "
            f"支持的格式: {', '.join(FORMATTERS.keys())}"
        )

    input_path = Path(input_path)

    if watch:
        watch_folder(input_path, lang, formats_list, config)
    elif batch_mode or input_path.is_dir():
        process_batch(
            input_dir=input_path,
            lang=lang,
            output_dir=config.output_dir,
            formats=formats_list,
            config=config,
        )
    else:
        _process_single(input_path, lang, output, formats_list, config)


if __name__ == "__main__":
    main()
```

### Step 6.4: 跑测试验证

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
pytest tests/test_cli.py -v
```

**Expected:** 6 个测试全部通过。

### Step 6.5: 手动 smoke test

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
python -m voicescribe.cli --help
```

**Expected:** 完整 Click usage 输出，包含所有选项。

### Step 6.6: Commit

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
git add voicescribe/cli.py tests/test_cli.py
git commit -m "Phase B4: CLI (Click command + multi-format output)"
```

---

## Task 7: GUI 骨架（Phase B4 续）

**Files:**
- Modify: `voicescribe/gui.py`（完整 Tkinter 入口）
- Modify: `voicescribe/ui/main_window.py`（主窗口组装）
- Modify: `voicescribe/ui/drop_zone.py`（拖拽区）
- Modify: `voicescribe/ui/queue_panel.py`（队列 Treeview）
- Modify: `voicescribe/ui/preview_panel.py`（字幕预览）
- Modify: `voicescribe/ui/progress_bar.py`（进度条）
- Modify: `voicescribe/ui/widgets.py`（自定义控件）

**Interfaces:**
- Consumes: `tkinter`, `tkinterdnd2`
- Produces: 可启动的 GUI（不在测试套件验证，需要显示器）

### Step 7.1: 实现 `voicescribe/ui/widgets.py`

**File:** `voicescribe/ui/widgets.py`

```python
"""自定义 Tkinter 控件（ttk 主题优化）"""

import tkinter as tk
from tkinter import ttk


def apply_vista_theme(root: tk.Tk) -> None:
    """应用 Windows Vista 主题（Windows 11 风格）"""
    style = ttk.Style(root)
    try:
        style.theme_use("vista")
    except tk.TclError:
        style.theme_use("default")


class StatusBar(tk.Frame):
    """底部状态栏"""

    def __init__(self, parent):
        super().__init__(parent, relief="sunken", bd=1)
        self.label = tk.Label(self, text="🟢 就绪", anchor="w", padx=5)
        self.label.pack(fill="x")

    def set_status(self, text: str) -> None:
        self.label.config(text=text)
```

### Step 7.2: 实现 `voicescribe/ui/drop_zone.py`

**File:** `voicescribe/ui/drop_zone.py`

```python
"""文件拖拽区（tkinterdnd2）"""

from pathlib import Path
import tkinter as tk

from tkinterdnd2 import DND_FILES

from voicescribe.core.audio_loader import SUPPORTED_EXTENSIONS


class DropZone(tk.Frame):
    """文件拖拽接收区"""

    def __init__(self, parent, on_drop):
        super().__init__(parent, relief="ridge", borderwidth=2, bg="#F5F5F5")
        self.on_drop = on_drop
        self.label = tk.Label(
            self,
            text="📂 拖拽音频文件到此处\n\n支持格式: WAV / FLAC / OGG",
            font=("Yu Gothic UI", 12),
            bg="#F5F5F5",
            pady=40,
        )
        self.label.pack(fill="both", expand=True, padx=20, pady=20)

        # 注册拖拽
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self._handle_drop)

    def _handle_drop(self, event):
        files = self.tk.splitlist(event.data)
        expanded = self._expand_paths(files)
        if expanded:
            self.on_drop(expanded)

    def _expand_paths(self, paths):
        result = []
        for p in paths:
            path = Path(p)
            if path.is_dir():
                result.extend(
                    f for f in path.rglob("*")
                    if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
                )
            elif path.suffix.lower() in SUPPORTED_EXTENSIONS:
                result.append(path)
        return result
```

### Step 7.3: 实现 `voicescribe/ui/queue_panel.py`

**File:** `voicescribe/ui/queue_panel.py`

```python
"""文件队列面板（ttk.Treeview）"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path


class QueuePanel(ttk.Treeview):
    """文件队列管理"""

    COLUMNS = ("status", "filename", "size", "lang")

    def __init__(self, parent):
        super().__init__(parent, columns=self.COLUMNS, show="headings", height=8)
        self.heading("status", text="状态")
        self.heading("filename", text="文件名")
        self.heading("size", text="大小")
        self.heading("lang", text="语言")
        self.column("status", width=80, anchor="center")
        self.column("filename", width=300)
        self.column("size", width=80, anchor="e")
        self.column("lang", width=80, anchor="center")

        # 添加滚动条
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=scrollbar.set)

    def add_file(self, file_path: Path, lang: str = "auto") -> str:
        size_mb = file_path.stat().st_size / 1024 / 1024
        item_id = self.insert("", "end", values=(
            "📋 待处理",
            file_path.name,
            f"{size_mb:.1f}MB",
            lang,
        ))
        return item_id

    def update_status(self, item_id: str, status: str) -> None:
        values = list(self.item(item_id)["values"])
        values[0] = status
        self.item(item_id, values=values)

    def clear(self) -> None:
        for item in self.get_children():
            self.delete(item)
```

### Step 7.4: 实现 `voicescribe/ui/preview_panel.py`

**File:** `voicescribe/ui/preview_panel.py`

```python
"""字幕预览面板"""

import tkinter as tk
from tkinter import ttk


class PreviewPanel(tk.Frame):
    """字幕预览（只读 Text + Scrollbar）"""

    def __init__(self, parent):
        super().__init__(parent)
        self.text = tk.Text(self, wrap="word", height=10, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)
        self.text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def set_content(self, content: str) -> None:
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)

    def clear(self) -> None:
        self.text.delete("1.0", "end")
```

### Step 7.5: 实现 `voicescribe/ui/progress_bar.py`

**File:** `voicescribe/ui/progress_bar.py`

```python
"""进度条（ttk.Progressbar）"""

import tkinter as tk
from tkinter import ttk


class ProgressBar(tk.Frame):
    """总进度条 + 标签"""

    def __init__(self, parent):
        super().__init__(parent)
        self.label = tk.Label(self, text="总进度: 0%")
        self.label.pack(anchor="w")
        self.progress = ttk.Progressbar(self, length=400, mode="determinate")
        self.progress.pack(fill="x", pady=2)

    def set_progress(self, current: int, total: int) -> None:
        if total > 0:
            percent = int(current / total * 100)
            self.progress["value"] = percent
            self.label.config(text=f"总进度: {percent}% ({current}/{total})")
```

### Step 7.6: 实现 `voicescribe/ui/main_window.py`

**File:** `voicescribe/ui/main_window.py`

```python
"""主窗口（组装所有面板）"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path

from .drop_zone import DropZone
from .queue_panel import QueuePanel
from .preview_panel import PreviewPanel
from .progress_bar import ProgressBar
from .widgets import StatusBar, apply_vista_theme


class MainWindow:
    """VoiceScribe 主窗口"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🎙️ VoiceScribe · 离线音频转文字工具")
        self.root.geometry("900x700")
        apply_vista_theme(root)

        self._build_ui()

    def _build_ui(self):
        # 工具栏
        toolbar = tk.Frame(self.root, bd=1, relief="raised")
        toolbar.pack(fill="x", padx=5, pady=5)

        tk.Label(toolbar, text="语言:").pack(side="left", padx=5)
        self.lang_var = tk.StringVar(value="auto")
        lang_combo = ttk.Combobox(
            toolbar,
            textvariable=self.lang_var,
            values=["auto", "zh", "ja", "en"],
            state="readonly",
            width=10,
        )
        lang_combo.pack(side="left", padx=5)

        # 拖拽区
        self.drop_zone = DropZone(self.root, on_drop=self._on_files_dropped)
        self.drop_zone.pack(fill="x", padx=5, pady=5)

        # 队列
        queue_frame = tk.LabelFrame(self.root, text="文件队列")
        queue_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.queue = QueuePanel(queue_frame)
        self.queue.pack(side="left", fill="both", expand=True)

        # 进度
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(fill="x", padx=5, pady=5)
        self.progress = ProgressBar(progress_frame)
        self.progress.pack(fill="x")

        # 预览
        preview_frame = tk.LabelFrame(self.root, text="字幕预览")
        preview_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.preview = PreviewPanel(preview_frame)
        self.preview.pack(fill="both", expand=True)

        # 状态栏
        self.status = StatusBar(self.root)
        self.status.pack(fill="x", side="bottom")

    def _on_files_dropped(self, files: list[Path]) -> None:
        for f in files:
            self.queue.add_file(f, self.lang_var.get())
        self.status.set_status(f"已添加 {len(files)} 个文件")
```

### Step 7.7: 实现 `voicescribe/gui.py`

**File:** `voicescribe/gui.py`（替换 Step 2.8 的骨架）

```python
"""VoiceScribe GUI 入口"""

import tkinter as tk

try:
    from tkinterdnd2 import TkinterDnD
    _TK_BASE = TkinterDnD.Tk
except ImportError:
    # tkinterdnd2 未安装，使用普通 Tk（不支持拖拽）
    _TK_BASE = tk.Tk


def main():
    """启动 VoiceScribe GUI"""
    root = _TK_BASE()
    root.title("🎙️ VoiceScribe · 离线音频转文字工具")
    root.geometry("900x700")

    from .ui.main_window import MainWindow
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
```

### Step 7.8: 验证 GUI 导入（不启动窗口）

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
python -c "from voicescribe.gui import main; from voicescribe.ui.main_window import MainWindow; print('GUI import OK')"
```

**Expected:** `GUI import OK`（无错误即通过）。

### Step 7.9: Commit

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
git add voicescribe/gui.py voicescribe/ui/
git commit -m "Phase B4 cont: GUI skeleton (Tkinter + tkinterdnd2)"
```

---

## Task 8: 打包脚本（Phase B4 终）

**Files:**
- Create: `scripts/build_cli.bat`
- Create: `scripts/build_gui.bat`
- Create: `scripts/download_models.py`

### Step 8.1: 写 `scripts/build_cli.bat`

**File:** `scripts/build_cli.bat`

```batch
@echo off
echo ========================================
echo  Building VoiceScribe CLI
echo ========================================

pyinstaller ^
    --onefile ^
    --name voicescribe ^
    --add-data "voicescribe/core;voicescribe/core" ^
    --hidden-import=faster_whisper ^
    --hidden-import=watchdog ^
    --hidden-import=PyYAML ^
    voicescribe/cli.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  Build SUCCESS
    echo  Output: dist\voicescribe.exe
    echo ========================================
) else (
    echo.
    echo ========================================
    echo  Build FAILED
    echo ========================================
    exit /b 1
)
```

### Step 8.2: 写 `scripts/build_gui.bat`

**File:** `scripts/build_gui.bat`

```batch
@echo off
echo ========================================
echo  Building VoiceScribe GUI
echo ========================================

pyinstaller ^
    --onefile ^
    --windowed ^
    --name voicescribe-gui ^
    --add-data "voicescribe/core;voicescribe/core" ^
    --hidden-import=faster_whisper ^
    --hidden-import=tkinterdnd2 ^
    --collect-all tkinterdnd2 ^
    voicescribe/gui.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  Build SUCCESS
    echo  Output: dist\voicescribe-gui.exe
    echo ========================================
) else (
    echo.
    echo ========================================
    echo  Build FAILED
    echo ========================================
    exit /b 1
)
```

### Step 8.3: 写 `scripts/download_models.py`

**File:** `scripts/download_models.py`

```python
"""模型预下载脚本

手动触发 Whisper 模型下载，避免首次转写等待。
"""

import click

from voicescribe.core.config import Config
from voicescribe.core.whisper_asr import WhisperASR


@click.command()
@click.option("-l", "--lang", default="ja", type=click.Choice(["ja", "en"]))
def main(lang):
    """下载 Whisper 模型"""
    config = Config()
    asr = WhisperASR(lang, config)

    click.echo(f"⏳ 下载 Whisper 模型: {config.whisper_model} ({config.whisper_compute_type})")
    click.echo("   这可能需要几分钟（模型约 1.5GB）...")

    def progress(downloaded: float, msg: str):
        click.echo(f"  [{downloaded*100:.0f}%] {msg}")

    asr.download_model(progress_callback=progress)
    click.echo("✅ 模型下载完成！")


if __name__ == "__main__":
    main()
```

### Step 8.4: Commit

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
git add scripts/
git commit -m "Phase B4 end: build scripts (PyInstaller + model download)"
```

---

## Task 9: 集成验证（Phase C）

**Files:**
- Modify: `CHANGELOG.md`
- 无代码改动

### Step 9.1: 跑完整测试套件

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
pytest tests/ -v --tb=short
```

**Expected:** 全部测试通过（至少 35+ 测试）。

如果失败，修复后重新跑直到全绿。

### Step 9.2: 跑 CLI smoke test

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
python -m voicescribe.cli --help
python -m voicescribe.cli --version
```

**Expected:**
- `--help` 输出完整 usage
- `--version` 输出 `voicescribe, version 0.1.0`

### Step 9.3: 跑导入 smoke test

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
python -c "
import voicescribe
from voicescribe.core import asr_backend, config, output_formats, audio_loader, language_detector, batch_processor, file_watcher
from voicescribe.core.whisper_asr import WhisperASR
from voicescribe.core.paddle_asr import PaddleASR
from voicescribe.cli import main as cli_main
from voicescribe.gui import main as gui_main
from voicescribe.ui.main_window import MainWindow
print('All imports OK')
print(f'Version: {voicescribe.__version__}')
print(f'ASR backends: {asr_backend.get_asr_backend.__name__}')
print(f'Formatters: {list(output_formats.FORMATTERS.keys())}')
"
```

**Expected:** `All imports OK` + 3 行元信息。

### Step 9.4: 写 CHANGELOG.md

**File:** `CHANGELOG.md`

```markdown
# Changelog

All notable changes to VoiceScribe will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - 2026-07-04

### Added
- 🎙️ **v0.1.0 首发版本** - 基于 R03 VoiceScribe 设计文档 v1.0
- ✅ **CLI 模式** - Click 命令行，多格式输出 (TXT/MD/SRT/VTT)
- ✅ **GUI 模式** - Tkinter + tkinterdnd2 拖拽
- ✅ **faster-whisper 日英 ASR** - 完整实现（large-v3 + int8 量化）
- ⚠️ **PaddleSpeech 中文 ASR** - stub-only（Python 3.14 不兼容）
- ✅ **批量处理** - 递归扫描文件夹
- ✅ **Watch 模式** - watchdog 文件夹监控
- ✅ **语言自动检测** - 基于文件名启发式
- ✅ **PyInstaller 打包脚本** - CLI + GUI 双 .exe

### Notes
- 需要 Python 3.14.5
- 首次使用会下载模型（约 1.5GB）
- 实际打包 .exe 未测试，需要手动验证
```

### Step 9.5: 最终 commit

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
git add CHANGELOG.md
git commit -m "Phase C: v0.1.0 integration verified (CHANGELOG + smoke tests pass)"
git log --oneline
```

**Expected:** `git log --oneline` 显示至少 7 个 commit（init + A + B1 + B2 + B3 + B4 + B4-cont + B4-end + C）。

### Step 9.6: 最终验收

```bash
cd "D:/AI-Agent/MyWisper-PaddleSpeech"
echo "=== 文件结构 ==="
find . -type f -not -path "./.git/*" -not -path "./.pytest_cache/*" -not -path "./__pycache__/*" -not -path "*/__pycache__/*" | sort

echo ""
echo "=== 测试统计 ==="
pytest tests/ -v --co -q | tail -5

echo ""
echo "=== Git 历史 ==="
git log --oneline
```

**Expected:**
- 30+ 文件
- 35+ 测试
- 8+ commits

---

## Self-Review

**1. Spec coverage:**
- ✅ Task 1: 项目初始化（spec §3 Phase A 前置）
- ✅ Task 2: 骨架 + 接口契约（spec §3 Phase A）
- ✅ Task 3: ASR 后端（spec §3 Phase B1）
- ✅ Task 4: I/O 工具（spec §3 Phase B2）
- ✅ Task 5: 高级模块（spec §3 Phase B3）
- ✅ Task 6: CLI（spec §3 Phase B4 一部分）
- ✅ Task 7: GUI（spec §3 Phase B4 一部分）
- ✅ Task 8: 打包脚本（spec §3 Phase B4 收尾）
- ✅ Task 9: 集成验证（spec §3 Phase C）

**2. 占位符扫描:**
- ✅ 无 TBD/TODO/占位符
- ✅ 每个 step 都有完整代码或精确命令
- ✅ 所有函数签名跨 task 一致（如 `_run_transcription` 在 batch_processor 和 CLI 都引用）

**3. 类型一致性:**
- ✅ `WhisperASR(lang, config)` 在 Task 2/3/6 一致
- ✅ `Segment(start, end, text, confidence)` 跨 Task 2/3/4/6 一致
- ✅ `Config` dataclass 字段在 Task 2 定义，Task 3/5/6 引用一致
- ✅ `_run_transcription(audio_path, lang, config)` 在 Task 5/6 一致
- ✅ `FORMATTERS` dict 键（txt/md/srt/vtt）跨 Task 2/4/6 一致

**4. 范围检查:**
- ✅ 单一可执行 v1.0
- ✅ OB 侧模板填充单独处理（不在 v1 代码交付范围）
- ✅ 9 个任务，可在一个会话内串行执行（约 1-2 小时）

---

*🎙️ VoiceScribe v1 Implementation Plan · MiuMiu 🐾 · 2026-07-04*
*📋 9 Tasks · TDD 流程 · Python 3.14 适配 · MIT 协议*