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
