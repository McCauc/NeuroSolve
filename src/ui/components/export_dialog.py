import tkinter as tk
from typing import Callable

import customtkinter as ctk


class ExportFormatDialog(ctk.CTkToplevel):
    """Small modal picker for selecting the report export format."""

    def __init__(self, master, on_select: Callable[[str], None], on_close=None):
        super().__init__(master)
        self._dialog_width = 360
        self._dialog_height = 230
        self._on_select = on_select
        self._on_close = on_close

        self.title("Export Report")
        self.geometry(f"{self._dialog_width}x{self._dialog_height}")
        self.resizable(False, False)
        self.configure(fg_color="#F8F5F8")
        self.transient(master)
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self._close)
        self.after(10, self._center_on_parent)

        shadow = tk.Frame(self, bg="#000000")
        shadow.place(x=16, y=16, relwidth=0.88, relheight=0.78)

        border = tk.Frame(self, bg="#000000")
        border.place(x=10, y=10, relwidth=0.88, relheight=0.78)

        card = ctk.CTkFrame(border, fg_color="#FFFFFF", corner_radius=0)
        card.pack(fill="both", expand=True, padx=4, pady=4)

        title = ctk.CTkLabel(
            card,
            text="EXPORT REPORT",
            font=ctk.CTkFont(family="Space Grotesk", size=24, weight="bold"),
            text_color="#000000",
        )
        title.pack(anchor="w", padx=18, pady=(18, 4))

        subtitle = ctk.CTkLabel(
            card,
            text="Choose a file format for the current solution trail.",
            font=ctk.CTkFont(family="Space Mono", size=12, weight="bold"),
            text_color="#000000",
            wraplength=300,
            justify="left",
        )
        subtitle.pack(anchor="w", padx=18, pady=(0, 16))

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(0, 14))

        for fmt, color in (("TXT", "#00FFFF"), ("HTML", "#FFFF00"), ("PDF", "#FFB347")):
            button = ctk.CTkButton(
                row,
                text=fmt,
                command=lambda value=fmt.lower(): self._select(value),
                width=92,
                height=42,
                corner_radius=0,
                fg_color=color,
                hover_color="#E2E8F0",
                text_color="#000000",
                border_width=3,
                border_color="#000000",
                font=ctk.CTkFont(family="Space Grotesk", size=15, weight="bold"),
            )
            button.pack(side="left", expand=True, padx=4)

    def _select(self, format_name: str) -> None:
        if callable(self._on_select):
            self._on_select(format_name)
        self._close()

    def _center_on_parent(self) -> None:
        self.update_idletasks()
        parent = self.master
        width = self._dialog_width
        height = self._dialog_height
        if parent and parent.winfo_exists():
            parent.update_idletasks()
            x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
            y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2
        else:
            x = (self.winfo_screenwidth() - width) // 2
            y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _close(self) -> None:
        if callable(self._on_close):
            self._on_close()
        self.destroy()
