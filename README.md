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
- 实施计划：`docs/superpowers/plans/2026-07-04-voicescribe-v1.md`
- 上游设计：R03 PaddleSpeech Research / 07-POC参考

## License

MIT