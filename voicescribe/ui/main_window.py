"""主窗口（组装所有面板）"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path

from .drop_zone import DropZone
from .queue_panel import QueuePanel
from .preview_panel import PreviewPanel
from .progress_bar import ProgressBar
from .widgets import StatusBar, apply_vista_theme


class MainWindow:
    """VoiceScribe 主窗口"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🎙️ VoiceScribe · 离线音频转文字工具")
        self.root.geometry("900x700")
        apply_vista_theme(root)

        self._build_ui()

    def _build_ui(self):
        # 工具栏
        toolbar = tk.Frame(self.root, bd=1, relief="raised")
        toolbar.pack(fill="x", padx=5, pady=5)

        tk.Label(toolbar, text="语言:").pack(side="left", padx=5)
        self.lang_var = tk.StringVar(value="auto")
        lang_combo = ttk.Combobox(
            toolbar,
            textvariable=self.lang_var,
            values=["auto", "zh", "ja", "en"],
            state="readonly",
            width=10,
        )
        lang_combo.pack(side="left", padx=5)

        # 拖拽区
        self.drop_zone = DropZone(self.root, on_drop=self._on_files_dropped)
        self.drop_zone.pack(fill="x", padx=5, pady=5)

        # 队列
        queue_frame = tk.LabelFrame(self.root, text="文件队列")
        queue_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.queue = QueuePanel(queue_frame)
        self.queue.pack(side="left", fill="both", expand=True)

        # 进度
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(fill="x", padx=5, pady=5)
        self.progress = ProgressBar(progress_frame)
        self.progress.pack(fill="x")

        # 预览
        preview_frame = tk.LabelFrame(self.root, text="字幕预览")
        preview_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.preview = PreviewPanel(preview_frame)
        self.preview.pack(fill="both", expand=True)

        # 状态栏
        self.status = StatusBar(self.root)
        self.status.pack(fill="x", side="bottom")

    def _on_files_dropped(self, files: list[Path]) -> None:
        for f in files:
            self.queue.add_file(f, self.lang_var.get())
        self.status.set_status(f"已添加 {len(files)} 个文件")
