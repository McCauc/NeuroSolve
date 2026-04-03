import tkinter as tk
import customtkinter as ctk

from src.ui.app_metadata import APP_MILESTONE, APP_NAME, APP_VERSION, TEAM_MEMBERS


class AboutHelpDialog(ctk.CTkToplevel):
    """Lightweight About/Help surface for the Week 7 package."""

    def __init__(self, master, on_close=None):
        super().__init__(master)
        self._dialog_width = 700
        self._dialog_height = 580
        self._on_close = on_close

        self.title("NeuroSolve - About / Help")
        self.geometry(f"{self._dialog_width}x{self._dialog_height}")
        self.minsize(620, 500)
        self.resizable(True, True)
        self.configure(fg_color="#F8F5F8")
        self.transient(master)
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self._close)
        self.after(10, self._center_on_parent)

        shadow = tk.Frame(self, bg="#000000")
        shadow.place(x=18, y=18, relwidth=0.94, relheight=0.92)

        border = tk.Frame(self, bg="#000000")
        border.place(x=12, y=12, relwidth=0.94, relheight=0.92)

        card = ctk.CTkFrame(border, fg_color="#FFFFFF", corner_radius=0)
        card.pack(fill="both", expand=True, padx=4, pady=4)

        footer_separator = ctk.CTkFrame(card, fg_color="#000000", height=3, corner_radius=0)
        footer_separator.pack(side="bottom", fill="x", padx=8, pady=(0, 0))

        footer = ctk.CTkFrame(card, fg_color="transparent")
        footer.pack(side="bottom", fill="x", padx=20, pady=(10, 16))

        close_btn = ctk.CTkButton(
            footer,
            text="CLOSE",
            command=self._close,
            width=130,
            height=40,
            corner_radius=0,
            fg_color="#00FFFF",
            hover_color="#95F5FF",
            text_color="#000000",
            border_width=3,
            border_color="#000000",
            font=ctk.CTkFont(family="Space Grotesk", size=16, weight="bold"),
        )
        close_btn.pack(side="right")

        # Keep content scrollable so footer remains visible on smaller windows/high DPI.
        body = ctk.CTkScrollableFrame(
            card,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
        )
        body.pack(side="top", fill="both", expand=True, padx=20, pady=(16, 0))

        title = ctk.CTkLabel(
            body,
            text="ABOUT / HELP",
            font=ctk.CTkFont(family="Space Grotesk", size=30, weight="bold"),
            text_color="#000000",
        )
        title.pack(anchor="w", pady=(0, 6))

        subtitle = ctk.CTkLabel(
            body,
            text=APP_NAME,
            font=ctk.CTkFont(family="Space Grotesk", size=24, weight="bold"),
            text_color="#FF00FF",
        )
        subtitle.pack(anchor="w")

        version = ctk.CTkLabel(
            body,
            text=f"Version: {APP_VERSION}",
            font=ctk.CTkFont(family="Space Mono", size=14, weight="bold"),
            text_color="#000000",
        )
        version.pack(anchor="w", pady=(14, 2))

        milestone = ctk.CTkLabel(
            body,
            text=f"Milestone: {APP_MILESTONE}",
            font=ctk.CTkFont(family="Space Mono", size=14, weight="bold"),
            text_color="#000000",
        )
        milestone.pack(anchor="w", pady=(0, 14))

        team_title = ctk.CTkLabel(
            body,
            text="Team Members",
            font=ctk.CTkFont(family="Space Grotesk", size=20, weight="bold"),
            text_color="#000000",
        )
        team_title.pack(anchor="w", pady=(0, 8))

        team_grid = ctk.CTkFrame(body, fg_color="transparent")
        team_grid.pack(fill="x", pady=(0, 12))
        for col in range(len(TEAM_MEMBERS)):
            team_grid.grid_columnconfigure(col, weight=1, uniform="member")

        member_photo = None
        photo_missing = False
        try:
            from PIL import Image
            member_photo = ctk.CTkImage(
                light_image=Image.open("assets/developer.png"),
                size=(92, 92),
            )
        except FileNotFoundError:
            photo_missing = True

        for idx, member in enumerate(TEAM_MEMBERS):
            slot = ctk.CTkFrame(team_grid, fg_color="transparent", width=206, height=178)
            slot.grid(row=0, column=idx, padx=8, pady=0, sticky="nsew")
            slot.grid_propagate(False)

            image_holder = ctk.CTkFrame(
                slot,
                fg_color="#FFFFFF",
                corner_radius=0,
                border_width=2,
                border_color="#000000",
                width=108,
                height=108,
            )
            image_holder.pack(padx=0, pady=(0, 8))
            image_holder.pack_propagate(False)

            if member_photo is not None:
                image_label = ctk.CTkLabel(image_holder, text="", image=member_photo)
                image_label.image = member_photo
                image_label.pack(expand=True)
            elif photo_missing:
                missing = ctk.CTkLabel(
                    image_holder,
                    text="image\nmissing",
                    justify="center",
                    font=ctk.CTkFont(family="Space Mono", size=10, weight="bold"),
                    text_color="#000000",
                )
                missing.pack(expand=True)

            name_holder = ctk.CTkFrame(slot, fg_color="transparent", height=44)
            name_holder.pack(fill="x")
            name_holder.pack_propagate(False)

            member_name = ctk.CTkLabel(
                name_holder,
                text=member,
                justify="center",
                wraplength=190,
                font=ctk.CTkFont(family="Space Mono", size=12, weight="bold"),
                text_color="#000000",
            )
            member_name.pack(expand=True)

        help_text = ctk.CTkLabel(
            body,
            text=(
                "NeuroSolve focuses on a local, solver-first workflow.\n"
                "Use the command strip to set f(x), method, and parameters,\n"
                "then run Calculate to inspect graph and solution trail."
            ),
            justify="left",
            font=ctk.CTkFont(family="Space Mono", size=12, weight="bold"),
            text_color="#000000",
        )
        help_text.pack(anchor="w", pady=(8, 0))

    def _center_on_parent(self) -> None:
        """Centers this dialog relative to the parent window."""
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
