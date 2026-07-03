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

### Test Results
- 48 / 48 unit tests passing
- CLI `--help` + `--version` verified
- All module imports verified

### Notes
- 需要 Python 3.14.5
- 首次使用会下载模型（约 1.5GB）
- 实际打包 .exe 未测试，需要手动验证