"""CLI 入口"""
import click


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
def main(input_path):
    """VoiceScribe · 离线音频转文字工具"""
    click.echo(f"voicescribe v0.1.0 (placeholder): {input_path}")


if __name__ == "__main__":
    main()
