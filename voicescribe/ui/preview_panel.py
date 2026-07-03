"""字幕预览面板"""

import tkinter as tk
from tkinter import ttk


class PreviewPanel(tk.Frame):
    """字幕预览（只读 Text + Scrollbar）"""

    def __init__(self, parent):
        super().__init__(parent)
        self.text = tk.Text(self, wrap="word", height=10, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)
        self.text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def set_content(self, content: str) -> None:
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)

    def clear(self) -> None:
        self.text.delete("1.0", "end")
