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
    output_path = Path(output) if output else None

    if watch:
        watch_folder(input_path, lang, formats_list, config)
    elif batch_mode or input_path.is_dir():
        process_batch(
            input_dir=input_path,
            lang=lang,
            output_dir=input_path / "out",
            formats=formats_list,
            config=config,
        )
    else:
        _process_single(input_path, lang, output_path, formats_list, config)


if __name__ == "__main__":
    main()
