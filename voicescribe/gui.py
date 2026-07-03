"""GUI 入口"""
import tkinter as tk


def main():
    """启动 VoiceScribe GUI"""
    root = tk.Tk()
    root.title("VoiceScribe")
    root.geometry("300x100")
    tk.Label(root, text="VoiceScribe GUI placeholder").pack()
    root.mainloop()


if __name__ == "__main__":
    main()
