"""VoiceScribe 包入口

允许 `python -m voicescribe` 直接调用 CLI。
PyInstaller 打包时用此文件作入口，避免相对导入失败。
"""

from voicescribe.cli import main

if __name__ == "__main__":
    main()