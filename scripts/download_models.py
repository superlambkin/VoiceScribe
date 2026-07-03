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