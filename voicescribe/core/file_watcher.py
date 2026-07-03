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
