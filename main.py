import time
import tkinter as tk
from tkinter import ttk


class ReoTimer:
    BACKGROUND = "#050505"
    PANEL = "#0D0D0D"
    BORDER = "#202020"
    GREEN = "#39FF88"
    RED = "#FF4545"
    MUTED = "#777777"
    WHITE = "#F2F2F2"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Reo")
        self.root.geometry("650x300")
        self.root.minsize(560, 340)
        self.root.configure(bg=self.BACKGROUND)

        self.running = False
        self.started_at = 0.0
        self.elapsed_before_start = 0.0
        self.after_id: str | None = None

        self._build_ui()
        self._render_time()
        self.root.protocol("WM_DELETE_WINDOW", self._close)

    def _build_ui(self) -> None:
        outer = tk.Frame(self.root, bg=self.BACKGROUND)
        outer.pack(fill="both", expand=True, padx=34, pady=26)

        header = tk.Frame(outer, bg=self.BACKGROUND)
        header.pack(fill="x")

        tk.Label(
            header, text="REO", font=("Segoe UI", 15, "bold"),
            fg=self.WHITE, bg=self.BACKGROUND
        ).pack(side="left")

        self.status_dot = tk.Label(
            header, text="●  STOPPED", font=("Segoe UI", 9, "bold"),
            fg=self.RED, bg=self.BACKGROUND
        )
        self.status_dot.pack(side="right")

        tk.Frame(outer, bg=self.BORDER, height=1).pack(fill="x", pady=(18, 0))

        display_area = tk.Frame(outer, bg=self.BACKGROUND)
        display_area.pack(fill="both", expand=True)

        self.time_label = tk.Label(
            display_area,
            text="0.0000",
            font=("Consolas", 62, "bold"),
            fg=self.RED,
            bg=self.BACKGROUND
        )
        self.time_label.pack(expand=True, pady=(12, 0))

        tk.Label(
            display_area,
            text="",
            font=("Segoe UI", 9),
            fg=self.MUTED,
            bg=self.BACKGROUND
        ).pack(pady=(0, 16))

        controls = tk.Frame(outer, bg=self.BACKGROUND)
        controls.pack(fill="x")

        self.start_button = tk.Button(
            controls, text="▶   Start", command=self.start,
            font=("Segoe UI", 11, "bold"), fg=self.BACKGROUND,
            bg=self.GREEN, activebackground="#70FFA9",
            activeforeground=self.BACKGROUND, relief="flat",
            bd=0, cursor="hand2", padx=24, pady=13
        )
        self.start_button.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.reset_button = tk.Button(
            controls, text="↺   Reset", command=self.reset,
            font=("Segoe UI", 11, "bold"), fg=self.WHITE,
            bg=self.PANEL, activebackground="#202020",
            activeforeground=self.WHITE, relief="flat",
            bd=0, cursor="hand2", padx=24, pady=13
        )
        self.reset_button.pack(side="left", fill="x", expand=True, padx=(8, 0))

        tk.Label(
            outer, text="SPACE  Start / Pause     •     R  Reset",
            font=("Segoe UI", 9), fg="#555555", bg=self.BACKGROUND
        ).pack(pady=(16, 0))

        self.root.bind("<space>", self._toggle)
        self.root.bind("r", self._reset_key)
        self.root.bind("R", self._reset_key)

    def _elapsed(self) -> float:
        if self.running:
            return self.elapsed_before_start + (time.perf_counter() - self.started_at)
        return self.elapsed_before_start

    def _render_time(self) -> None:
        elapsed = self._elapsed()
        self.time_label.configure(text=f"{elapsed:.4f}")
        if self.running:
            self.time_label.configure(fg=self.GREEN)
            self.status_dot.configure(text="●  RUNNING", fg=self.GREEN)
        else:
            self.time_label.configure(fg=self.RED)
            self.status_dot.configure(text="●  STOPPED", fg=self.RED)

    def _tick(self) -> None:
        self._render_time()
        if self.running:
            self.after_id = self.root.after(16, self._tick)

    def start(self) -> None:
        if self.running:
            return
        self.running = True
        self.started_at = time.perf_counter()
        self.start_button.configure(
            text="Ⅱ   Pause", command=self.pause,
            fg=self.WHITE, bg="#292929", activebackground="#383838",
            activeforeground=self.WHITE
        )
        self._tick()

    def pause(self) -> None:
        if not self.running:
            return
        self.elapsed_before_start += time.perf_counter() - self.started_at
        self.running = False
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.start_button.configure(
            text="▶   Resume", command=self.start,
            fg=self.BACKGROUND, bg=self.GREEN, activebackground="#70FFA9",
            activeforeground=self.BACKGROUND
        )
        self._render_time()

    def reset(self) -> None:
        self.running = False
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.elapsed_before_start = 0.0
        self.started_at = 0.0
        self.start_button.configure(
            text="▶   Start", command=self.start,
            fg=self.BACKGROUND, bg=self.GREEN, activebackground="#70FFA9",
            activeforeground=self.BACKGROUND
        )
        self._render_time()

    def _toggle(self, _event: tk.Event) -> str:
        self.pause() if self.running else self.start()
        return "break"

    def _reset_key(self, _event: tk.Event) -> str:
        self.reset()
        return "break"

    def _close(self) -> None:
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    ReoTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
