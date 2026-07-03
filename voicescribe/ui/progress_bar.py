"""进度条（ttk.Progressbar）"""

import tkinter as tk
from tkinter import ttk


class ProgressBar(tk.Frame):
    """总进度条 + 标签"""

    def __init__(self, parent):
        super().__init__(parent)
        self.label = tk.Label(self, text="总进度: 0%")
        self.label.pack(anchor="w")
        self.progress = ttk.Progressbar(self, length=400, mode="determinate")
        self.progress.pack(fill="x", pady=2)

    def set_progress(self, current: int, total: int) -> None:
        if total > 0:
            percent = int(current / total * 100)
            self.progress["value"] = percent
            self.label.config(text=f"总进度: {percent}% ({current}/{total})")
