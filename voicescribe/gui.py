"""VoiceScribe GUI 入口"""

import tkinter as tk

try:
    from tkinterdnd2 import TkinterDnD
    _TK_BASE = TkinterDnD.Tk
except ImportError:
    # tkinterdnd2 未安装，使用普通 Tk（不支持拖拽）
    _TK_BASE = tk.Tk


def main():
    """启动 VoiceScribe GUI"""
    root = _TK_BASE()
    root.title("🎙️ VoiceScribe · 离线音频转文字工具")
    root.geometry("900x700")

    from .ui.main_window import MainWindow
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
