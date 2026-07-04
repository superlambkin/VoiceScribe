# 🤝 VoiceScribe · Developer Handoff (v0.1.0)

> **For the next developer / agent taking over this codebase.**
> Read this + `OB/00_接棒指南.md` and you're ready in 10 min.

---

## TL;DR

```bash
cd "D:\AI-Agent\MyWisper-PaddleSpeech"
pytest --tb=short                 # → 53/53 passed
./dist/voicescribe.exe --version  # → voicescribe, version 0.1.0
./dist/voicescribe-gui.exe        # → GUI launches
```

**That's it. The product works.**

---

## Current State

| Item | Value |
|------|-------|
| Version | v0.1.0 (released 2026-07-04) |
| Python | 3.14.5 |
| Git branch | `main` (clean, 17 commits) |
| Tests | 53/53 passing |
| Coverage | 86% core, 80% CLI, 58% overall |
| CLI exe | `dist/voicescribe.exe` (407 MB) |
| GUI exe | `dist/voicescribe-gui.exe` (381 MB) |
| Whisper model | `~/.cache/huggingface/hub/models--Systran--faster-whisper-large-v3/` (2.9 GB, already downloaded) |

---

## What's Where

```
D:\AI-Agent\MyWisper-PaddleSpeech\
├── voicescribe/              ← main package (25 .py files)
│   ├── __main__.py           ← CLI entry (used by PyInstaller)
│   ├── cli.py                ← Click CLI
│   ├── gui.py                ← Tkinter GUI
│   ├── core/
│   │   ├── asr_backend.py    ← ABC + factory (add new ASR here)
│   │   ├── whisper_asr.py    ← faster-whisper (ja/en)
│   │   ├── paddle_asr.py     ← PaddleSpeech (zh, STUB on Python 3.14)
│   │   ├── audio_loader.py   ← WAV/FLAC/OGG + MP3/M4A via ffmpeg
│   │   ├── output_formats.py ← TXT/MD/SRT/VTT (Strategy)
│   │   ├── batch_processor.py
│   │   ├── file_watcher.py
│   │   ├── language_detector.py
│   │   └── config.py
│   └── ui/                   ← 6 GUI components
├── tests/                    ← 53 pytest tests
├── scripts/
│   ├── build_cli.bat         ← PyInstaller CLI build
│   ├── build_gui.bat         ← PyInstaller GUI build
│   └── download_models.py    ← pre-download Whisper
├── docs/
│   ├── HANDOFF.md            ← THIS FILE
│   ├── PROJECT_STRUCTURE.md  ← full directory layout
│   └── superpowers/          ← spec + plan (history)
├── .superpowers/sdd/         ← SDD process artifacts (gitignored)
│   ├── progress.md           ← 9-task ledger
│   ├── task-N-brief.md       ← task requirements
│   ├── task-N-report.md      ← task reports
│   └── review-*.diff         ← reviewer snapshots
├── dist/                     ← built exes (gitignored, but kept)
├── pyproject.toml            ← deps + entry points
└── CHANGELOG.md
```

---

## Architecture (DO NOT break)

### 1. ASR Backend = ABC + Factory

```python
# voicescribe/core/asr_backend.py
class ASRBackend(ABC):
    @abstractmethod
    def transcribe(self, audio_path: Path, lang: str) -> list[Segment]: ...
    @abstractmethod
    def is_model_ready(self) -> bool: ...
    @abstractmethod
    def download_model(self, progress_callback=None) -> None: ...

def get_asr_backend(lang: str, config: Config) -> ASRBackend:
    if lang in ("ja", "en"):
        return WhisperASR(lang, config)
    elif lang == "zh":
        return PaddleASR(config)
    raise ValueError(...)
```

**To add a new backend** (e.g. Vosk): subclass `ASRBackend`, register in `get_asr_backend`.

### 2. Output Formats = Strategy

```python
# voicescribe/core/output_formats.py
FORMATTERS = {
    "txt": TxtFormatter,
    "md":  MdFormatter,
    "srt": SrtFormatter,
    "vtt": VttFormatter,
}
```

**To add a new format** (e.g. JSON): subclass `BaseFormatter`, register in `FORMATTERS`.

### 3. Segment + Config = dataclass

Don't change to dict / namedtuple — code depends on type.

---

## Critical ADRs (Architectural Decisions)

| ADR | Decision | Why |
|-----|----------|-----|
| **ADR-001** | Python 3.14 + skip PaddleSpeech → stub | Env only has 3.14 |
| **ADR-002** | MultiAgent SDD workflow | 9-task plan, dual roles |
| **ADR-003** | tkinterdnd2 fallback to plain Tk | GUI must always work |
| **ADR-004** | ffmpeg subprocess (not pydub) | Python 3.13+ removed `audioop` |
| **ADR-005** | `voicescribe/__main__.py` as PyInstaller entry | Avoids relative import error |

---

## 6 Technical Pitfalls (avoid these)

| Pitfall | Solution |
|---------|----------|
| `pydub` ImportError on Python 3.13+ | Use `subprocess` + `imageio_ffmpeg` (not `pydub`) |
| PyInstaller `ImportError: relative import` | Use `voicescribe/__main__.py`, NOT `cli.py` |
| tkinterdnd2 drag-drop broken in exe | Add `--collect-all tkinterdnd2` |
| numpy.libs DLL missing | Add `--collect-all numpy` |
| Whisper repeated phrases | Use `repetition_penalty` param (v0.2.0 todo) |
| Whisper model first download = 1.5 GB | Lazy download + `download_models.py` script |

---

## TODO Priority

### P0 (user can verify right now)

```bash
# Re-run tests
pytest --tb=short

# Try the CLI exe
./dist/voicescribe.exe "D:/AI-Agent/20260617_160514.m4a" -l ja -f srt

# Try the GUI exe
./dist/voicescribe-gui.exe
```

### P1 (v0.2.0 candidates)

| # | Task | Where to start |
|---|------|----------------|
| 1 | CI integration (GitHub Actions) | `.github/workflows/test.yml` |
| 2 | Fix Whisper repetition | Add `repetition_penalty` in `whisper_asr.py` |
| 3 | GUI unit tests | Add `pytest-tkinter` + `tests/test_gui_smoke.py` |
| 4 | `file_watcher` unit tests | `tests/test_file_watcher.py` (tmpdir + sleep) |
| 5 | Validate PaddleSpeech on Python 3.12 | Switch env, install, test |

### P2 (v0.2.0+)

| # | Task |
|---|------|
| 6 | CUDA support |
| 7 | Whisper base model option (`--model`) |
| 8 | NSIS installer |
| 9 | Code signing + VirusTotal upload |

### P3 (backlog)

| # | Task |
|---|------|
| 10 | Speaker diarization (pyannote.audio) |
| 11 | macOS / Linux builds |
| 12 | Real-time streaming |
| 13 | Web UI |

---

## SDD Workflow Cheat Sheet (if continuing)

```
brainstorming → spec → writing-plans → subagent-driven-development
                                              ↓
                                     1 implementer + 1 reviewer per task
                                              ↓
                                     1 whole-branch review at end
```

**Artifacts**:

- Spec: `docs/superpowers/specs/*.md`
- Plan: `docs/superpowers/plans/*.md`
- Task brief/report: `.superpowers/sdd/task-N-*`
- Progress ledger: `.superpowers/sdd/progress.md`
- Review diffs: `.superpowers/sdd/review-*.diff`

**Lessons learned**:

1. Reviewer false positive rate is ~30%. Pre-attach "anti-FP guide" + grep-validated signatures
2. **Trust `.superpowers/sdd/progress.md` and `git log` over your own memory** (context compaction will save you)
3. Pure transcribe tasks (git init, .bat scripts) don't need subagents — do them manually
4. PyInstaller always uses `__main__.py` as entry, NEVER direct module path
5. GUI 0% coverage is acceptable for v0.1.0; v0.2.0 MUST add GUI tests

---

## Env Recovery (if starting fresh)

```bash
cd "D:\AI-Agent\MyWisper-PaddleSpeech"

# Install project + dev deps + PyInstaller
pip install -e ".[dev]" pyinstaller

# Verify
pytest --tb=short   # expect 53 passed

# Re-build exes if needed
scripts\build_cli.bat
scripts\build_gui.bat

# Pre-download model if cache is gone
python scripts/download_models.py -l ja
```

---

## Related Docs

| Doc | What |
|-----|------|
| `OB/00_接棒指南.md` | OB-side handoff (more detail, Chinese) |
| `OB/00_项目进程_课题记录.md` | PDCA + ADR + issue list |
| `OB/06_复盘总结/v0.1.0复盘.md` | v0.1.0 retrospective |
| `OB/09_对话总结/2026-07-04.md` | Day-of-implementation log |
| `OB/03_开发文档/_进度计划/MultiAgent开发计划.md` | SDD 9-task detail |
| `docs/PROJECT_STRUCTURE.md` | Full repo layout |
| `.superpowers/sdd/progress.md` | Task ledger |

---

## "Things NOT to do"

- ❌ Don't rewrite ASR backend (stable)
- ❌ Don't refactor `core/` (86% covered, 53 tests prove it works)
- ❌ Don't change OB doc structure (aligned to v3 template)
- ❌ Don't use `pydub` (Python 3.13+ breaks it)
- ❌ Don't PyInstaller-pack `cli.py` directly (use `__main__.py`)

## "Things you CAN do"

- ✅ Add v0.2.0 spec + plan (continue SDD)
- ✅ Implement any P1 item
- ✅ Fix Whisper repetition (10-line change)
- ✅ Add new ASR backend / output format (well-defined extension points)

---

*🤝 VoiceScribe v0.1.0 Handoff · MiuMiu 🐾 · 2026-07-04*

> *"Inheriting a complete v0.1.0 is 10× more fun than starting from scratch."*