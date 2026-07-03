---
title: "VoiceScribe · MultiAgent 实施设计"
type: implementation-spec
status: ✅ 已批准
created: 2026-07-04
modified: 2026-07-04
project_id: POC_012_VoiceScribe
source_design: 60_Tech_Research/R03_PaddleSpeech-Research/07-POC参考/技术方案/VoiceScribe-设计文档.md
tags:
  - VoiceScribe
  - MultiAgent
  - 实施设计
  - POC_012
---

# 🎙️ VoiceScribe · MultiAgent 实施设计

> **〔卷首语〕** *「基于已批准的 R03 VoiceScribe 设计文档 v1.0，制定 MultiAgent 实施流程的简洁规范文档」*

---

> 📂 **路径**: `docs/superpowers/specs/2026-07-04-voicescribe-implementation-design.md`
> 📌 **上游设计**: [[../../../60_Tech_Research/R03_PaddleSpeech-Research/07-POC参考/技术方案/VoiceScribe-设计文档|VoiceScribe 设计文档 v1.0]]
> 🎯 **项目代号**: **VoiceScribe**（OB: POC_012_VoiceScribe, 代码: MyWisper-PaddleSpeech）
> 👤 **目标用户**: 主人个人（CNC 业务、会议记录、诗心朗读素材）

---

## 🎯 任务目标

> **基于已批准的 R03 VoiceScribe 设计文档 v1.0，通过 MultiAgent 协作交付一个可在 Python 3.14 环境下运行的 v1 实现。**

### 与 R03 设计文档的关系

| 文档 | 角色 | 状态 |
|------|------|------|
| [[../../../60_Tech_Research/R03_PaddleSpeech-Research/07-POC参考/技术方案/VoiceScribe-设计文档\|R03 VoiceScribe 设计文档]] | **产品设计**（接口、架构、指标） | ✅ v1.0 已批准 |
| **本规范文档** | **实施规范**（MultiAgent 流程、Python 3.14 适配） | ✅ 本次批准 |
| POC_012_VoiceScribe/02_设计文档/ | OB 侧设计归档 | 由 OB 模板填充任务产出 |
| `voicescribe/` 源码 | 实施产物 | 由 MultiAgent Phase A/B/C 产出 |

---

## 🏗️ 双轨项目结构

### OB 侧（设计归档）

```
C:\Users\superlambkin\OneDrive\Edge\Obsidian Vault\80_POC_Projects\POC_012_VoiceScribe\
├── 00_使用指南.md
├── 00_项目进程_课题记录.md
├── README.md
├── CHANGELOG.md
├── 01_需求文档/        ← 引用 R03 设计文档目标与成功标准
├── 02_设计文档/        ← 8 个拆分文档（按 v3.0 模板）
├── 03_开发文档/        ← _代码归档/ + _进度计划/MultiAgent开发计划.md
├── 04_测试文档/        ← 测试策略.md
├── 05_部署运维/        ← PyInstaller打包方案.md
└── 06_复盘总结/        ← 留空
```

### 代码侧（实施产物）

```
D:\AI-Agent\MyWisper-PaddleSpeech\          ← git 仓库根
├── .git/
├── .gitignore
├── README.md
├── LICENSE                                ← MIT
├── pyproject.toml                         ← 依赖声明（适配 Python 3.14）
├── docs/
│   └── superpowers/specs/                 ← 本规范文档
│
├── voicescribe/                           ← Python 包
│   ├── __init__.py
│   ├── __version__.py                     ← "0.1.0"
│   ├── cli.py                             ← Click CLI 入口
│   ├── gui.py                             ← Tkinter GUI 入口
│   │
│   ├── core/                              ← 共享核心
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── asr_backend.py                 ← ASR 抽象 + Segment + 工厂
│   │   ├── whisper_asr.py                 ← faster-whisper ✅
│   │   ├── paddle_asr.py                  ← stub-only ⚠️
│   │   ├── audio_loader.py
│   │   ├── language_detector.py
│   │   ├── output_formats.py
│   │   ├── batch_processor.py
│   │   └── file_watcher.py
│   │
│   └── ui/                                ← Tkinter GUI 组件
│       ├── __init__.py
│       ├── main_window.py
│       ├── drop_zone.py
│       ├── queue_panel.py
│       ├── preview_panel.py
│       ├── progress_bar.py
│       └── widgets.py
│
├── tests/                                 ← pytest 单元测试
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_asr_backend.py
│   ├── test_whisper_asr.py
│   ├── test_output_formats.py
│   ├── test_batch_processor.py
│   ├── test_audio_loader.py
│   ├── test_language_detector.py
│   └── test_cli.py
│
└── scripts/
    ├── build_cli.bat                       ← PyInstaller CLI 打包
    ├── build_gui.bat                       ← PyInstaller GUI 打包
    └── download_models.py                  ← 模型预下载脚本
```

---

## ⚠️ Python 3.14 适配决策

环境约束：**只有 Python 3.14.5**，但 R03 设计文档要求 3.10-3.12。

### 决策矩阵

| R03 设计要求 | 3.14 兼容性 | 决策 |
|---|---|---|
| PaddleSpeech 中文 ASR | ❌ 官方仅支持 ≤ 3.12 | **stub-only**（导入时报清晰错误） |
| faster-whisper 日英 | ✅ 一般兼容 | **完整实现** |
| click / rich / watchdog / PyYAML | ✅ 兼容 | 完整实现 |
| tkinter + tkinterdnd2 | ✅ 内建 + pip | 完整实现 |
| PyInstaller 6.x | ⚠️ 未测 | 脚本就绪，不实际打包 |
| pytest 7.x | ✅ 兼容 | 完整测试 |

### `paddle_asr.py` stub 策略

```python
"""PaddleSpeech 中文 ASR · Python 3.14 适配版 stub"""

class PaddleASR:
    """⚠️ PaddleSpeech 不支持 Python 3.14"""

    def transcribe(self, audio_path, lang="zh"):
        raise NotImplementedError(
            "PaddleSpeech 中文 ASR 当前环境（Python 3.14）不支持。\n"
            "解决：切换 Python 3.10-3.12 后 pip install paddlespeech。\n"
            "本 v1 仅支持 faster-whisper（日/英）后端。"
        )

    def is_model_ready(self) -> bool:
        return False

    def download_model(self, progress_callback=None):
        raise NotImplementedError("见 transcribe() 的错误说明")
```

`asr_backend.py` 工厂方法在 `lang == "zh"` 时**仍返回 PaddleASR 实例**（保持接口一致），用户调用 `.transcribe()` 时才会触发清晰错误。

---

## 🤖 MultiAgent 三阶段流程

### Phase A · 架构师 Agent（串行，单 agent）

**输入**：R03 设计文档 + 本规范  
**输出**：
- `voicescribe/__init__.py`、`__version__.py`
- `voicescribe/core/__init__.py` + 全部模块空骨架（仅函数签名 + docstring + `pass` / `raise NotImplementedError`）
- `voicescribe/ui/__init__.py` + 全部 ui 模块空骨架
- `tests/conftest.py` + 每个测试文件空骨架
- `pyproject.toml` + `.gitignore` + `README.md` + `LICENSE`
- **接口契约文档**（明确 ASRBackend 抽象、Segment dataclass、FORMATTERS dict、Config dataclass 字段）

**验证**：
```bash
python -c "import voicescribe"
python -c "from voicescribe.core.asr_backend import ASRBackend, Segment, get_asr_backend"
```
两条命令均退出码 0。

**Git commit**：`Phase A: skeleton + interfaces`

---

### Phase B · 模块开发 Agent（并行，3-4 agent 同时）

| Agent | 负责文件 | 接口依赖 | 输出验证 |
|---|---|---|---|
| **B1: ASR 后端** | `whisper_asr.py`, `paddle_asr.py` | ASRBackend 抽象（Phase A 产出） | `from voicescribe.core.whisper_asr import WhisperASR` 成功 |
| **B2: I/O 工具** | `audio_loader.py`, `output_formats.py`, `language_detector.py` | Segment dataclass | `pytest tests/test_output_formats.py` 全通过 |
| **B3: 高级模块** | `config.py`, `batch_processor.py`, `file_watcher.py` | Config + Segment | 导入成功 |
| **B4: CLI/GUI** | `cli.py`, `gui.py`, `ui/*.py` | 全部 core 模块 | `python -m voicescribe.cli --help` 输出 usage |

**并行安全保障**：
- B1/B2/B3 互不写同一文件（独立 `.py`）
- B4 在自己的文件工作，通过 `from voicescribe.core.X import Y` 引用
- **如有冲突**：B4 等待其他三个 Phase 完成（依赖 Config/ASR/Formatter）

**派发顺序决策**：先派发 B1+B2+B3 并行（同时启动），等三者全部完成后，再派发 B4。四个 agent 总耗时 = max(B1,B2,B3) + B4。

**Git commit**：每个 agent 一个 commit（`Phase B1: ASR backends`, `Phase B2: I/O`, `Phase B3: advanced`, `Phase B4: CLI/GUI`）

---

### Phase C · 集成验证 Agent（串行，单 agent）

**任务**：
1. 跑完整测试套件：`pytest tests/ -v --tb=short`
2. 跑 CLI smoke test：`python -m voicescribe.cli --help && python -m voicescribe.cli nonexistent.wav`（期望友好错误）
3. 跑 GUI smoke test：`python -c "import voicescribe.gui"` （不实际启动窗口）
4. 修复任何集成错误
5. 更新 `CHANGELOG.md`（v0.1.0 entry）
6. 最终 git commit：`Phase C: v0.1.0 integration verified`

**输出验证**：上述 4 条命令全部通过。

---

## ✅ 验收标准

### 每个 Phase 必须满足

```bash
# 1. 导入无错
python -c "import voicescribe"

# 2. CLI 帮助可用
python -m voicescribe.cli --help

# 3. 单元测试通过
python -m pytest tests/ -v

# 4. Git 状态干净（除已提交文件）
git status
```

### 最终交付（Phase C 完成后）

| 项目 | 要求 |
|---|---|
| `voicescribe/__version__.py` | `"0.1.0"` |
| `voicescribe.cli --help` | 列出设计文档第 681-693 行所有参数 |
| `pytest tests/` | 全绿（包含 at least 15 个测试用例） |
| `git log` | 至少 6 个 commits（init + A + B1~B4 + C） |
| `pyproject.toml` | 列出全部依赖（click, rich, watchdog, PyYAML, pytest, faster-whisper, soundfile, numpy, tkinterdnd2） |
| 代码行数 | ~800-1200 行（不含注释） |

---

## 🚫 不做事项（YAGNI）

明确**不实现**，以避免范围蔓延：

1. ❌ **PaddleSpeech 中文 ASR 真实实现** — Python 3.14 不兼容，留 stub
2. ❌ **PyInstaller 实际打包** — 环境未验证，脚本就绪即可
3. ❌ **Whisper 模型实际下载** — 1.5GB 网络成本，由用户手动触发
4. ❌ **NSIS 安装包脚本** — 超出 v1 范围
5. ❌ **E2E 手动验收** — 文档列出验收清单，由主人手测
6. ❌ **GUI 实际启动验证** — 需要显示器，本次只验证导入
7. ❌ **多平台兼容** — Windows only（设计文档已限定）
8. ❌ **CI/CD 配置** — 不在 v1 范围
9. ❌ **国际化 i18n** — 界面中文/英文混排可接受

---

## 🔗 关联文档

- [[../../../60_Tech_Research/R03_PaddleSpeech-Research/07-POC参考/技术方案/VoiceScribe-设计文档|R03 VoiceScribe 设计文档 v1.0]]
- [[../../../60_Tech_Research/R03_PaddleSpeech-Research/07-POC参考/技术方案/POC方案|R03 POC 方案]]
- [[../../../../../80_POC_Projects/POC_012_VoiceScribe/README|POC_012 README]]（将由 OB 模板填充任务创建）

---

## 📅 实施时间表（参考 R03 设计文档第 1039-1052 行）

| Phase | 内容 | 预计耗时 |
|:----:|------|:---:|
| **A** | 骨架 + 接口契约 | ~1 agent 任务 |
| **B1+B2+B3** | 模块并行 | ~1 agent 任务（最长者） |
| **B4** | CLI/GUI | ~1 agent 任务 |
| **C** | 集成验证 | ~1 agent 任务 |
| **总计** | 4-5 个 agent 任务 | ~半天人工 + agent 时间 |

---

*🎙️ VoiceScribe 实施设计 v1.0 · MiuMiu 🐾 · 2026-07-04*
*📐 基于 R03 设计 v1.0 · 适配 Python 3.14 · MultiAgent 三阶段*