"""自定义 Tkinter 控件（ttk 主题优化）"""

import tkinter as tk
from tkinter import ttk


def apply_vista_theme(root: tk.Tk) -> None:
    """应用 Windows Vista 主题（Windows 11 风格）"""
    style = ttk.Style(root)
    try:
        style.theme_use("vista")
    except tk.TclError:
        style.theme_use("default")


class StatusBar(tk.Frame):
    """底部状态栏"""

    def __init__(self, parent):
        super().__init__(parent, relief="sunken", bd=1)
        self.label = tk.Label(self, text="🟢 就绪", anchor="w", padx=5)
        self.label.pack(fill="x")

    def set_status(self, text: str) -> None:
        self.label.config(text=text)
