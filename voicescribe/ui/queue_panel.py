"""文件队列面板（ttk.Treeview）"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path


class QueuePanel(ttk.Treeview):
    """文件队列管理"""

    COLUMNS = ("status", "filename", "size", "lang")

    def __init__(self, parent):
        super().__init__(parent, columns=self.COLUMNS, show="headings", height=8)
        self.heading("status", text="状态")
        self.heading("filename", text="文件名")
        self.heading("size", text="大小")
        self.heading("lang", text="语言")
        self.column("status", width=80, anchor="center")
        self.column("filename", width=300)
        self.column("size", width=80, anchor="e")
        self.column("lang", width=80, anchor="center")

        # 添加滚动条
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=scrollbar.set)

    def add_file(self, file_path: Path, lang: str = "auto") -> str:
        size_mb = file_path.stat().st_size / 1024 / 1024
        item_id = self.insert("", "end", values=(
            "📋 待处理",
            file_path.name,
            f"{size_mb:.1f}MB",
            lang,
        ))
        return item_id

    def update_status(self, item_id: str, status: str) -> None:
        values = list(self.item(item_id)["values"])
        values[0] = status
        self.item(item_id, values=values)

    def clear(self) -> None:
        for item in self.get_children():
            self.delete(item)
