"""文件拖拽区（tkinterdnd2）"""

from pathlib import Path
import tkinter as tk

from tkinterdnd2 import DND_FILES

from voicescribe.core.audio_loader import SUPPORTED_EXTENSIONS


class DropZone(tk.Frame):
    """文件拖拽接收区"""

    def __init__(self, parent, on_drop):
        super().__init__(parent, relief="ridge", borderwidth=2, bg="#F5F5F5")
        self.on_drop = on_drop
        self.label = tk.Label(
            self,
            text="📂 拖拽音频文件到此处\n\n支持格式: WAV / FLAC / OGG",
            font=("Yu Gothic UI", 12),
            bg="#F5F5F5",
            pady=40,
        )
        self.label.pack(fill="both", expand=True, padx=20, pady=20)

        # 注册拖拽
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self._handle_drop)

    def _handle_drop(self, event):
        files = self.tk.splitlist(event.data)
        expanded = self._expand_paths(files)
        if expanded:
            self.on_drop(expanded)

    def _expand_paths(self, paths):
        result = []
        for p in paths:
            path = Path(p)
            if path.is_dir():
                result.extend(
                    f for f in path.rglob("*")
                    if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
                )
            elif path.suffix.lower() in SUPPORTED_EXTENSIONS:
                result.append(path)
        return result
