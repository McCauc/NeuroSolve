import customtkinter as ctk
import tkinter as tk

class HeaderFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Pure white background, no internal borders. Border rendered by app.py Grid.
        super().__init__(
            master, 
            fg_color="#FFFFFF", 
            corner_radius=0, 
            border_width=0, 
            height=75,
            **kwargs
        )
        self.pack_propagate(False) # Force strict brutalist 75px height
        
        # We only want the bottom border, but CTkFrame borders all sides.
        # It's okay because we'll pack it tightly to the top edge.
        
        # -------------------
        # 1. ICON (LEFT)
        # -------------------
        self.icon_container = ctk.CTkFrame(self, fg_color="transparent", width=52, height=52)
        self.icon_container.place(x=20, rely=0.5, anchor="w") # Perfectly vertically centered
        self.icon_container.pack_propagate(False)

        # Hard shadow
        self.icon_shadow = ctk.CTkFrame(self.icon_container, fg_color="#000000", corner_radius=0, width=48, height=48)
        self.icon_shadow.place(x=4, y=4)

        self.icon_box = ctk.CTkFrame(
            self.icon_container, 
            fg_color="#000000", 
            corner_radius=0,
            width=48,
            height=48
        )
        self.icon_box.place(x=0, y=0)
        self.icon_box.pack_propagate(False) # Force size
        
        self.icon_label = ctk.CTkLabel(
            self.icon_box,
            text="ƒx", # Math symbol placeholder
            font=ctk.CTkFont(family="Space Grotesk", size=24, weight="bold", slant="italic"),
            text_color="#A6FFD6" # Mint green text
        )
        self.icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # -------------------
        # 2. TITLE & BADGE
        # -------------------
        self.title_container = ctk.CTkFrame(self, fg_color="transparent")
        self.title_container.place(x=87, rely=0.5, anchor="w") # Vertically centered next to icon
        
        # Row 1: Top Title Text
        self.title_text_frame = ctk.CTkFrame(self.title_container, fg_color="transparent")
        self.title_text_frame.pack(side="top", anchor="w")

        self.title_main = ctk.CTkLabel(
            self.title_text_frame,
            text="NEUROSOLVE",
            font=ctk.CTkFont(family="Space Grotesk", size=28, weight="bold"),
            text_color="#000000"
        )
        self.title_main.pack(side="left")
        
        self.title_sub = ctk.CTkLabel(
            self.title_text_frame,
            text=".NEO",
            font=ctk.CTkFont(family="Space Grotesk", size=28, weight="bold"),
            text_color="#FF00FF" # Pure Magenta
        )
        self.title_sub.pack(side="left")

        # Row 2: Method Sticker Badge with hard shadow
        self.badge_container = ctk.CTkFrame(self.title_container, fg_color="transparent", width=320, height=34)
        self.badge_container.pack(side="top", anchor="w")
        self.badge_container.pack_propagate(False)

        # Hard shadow using raw tk.Frame to prevent bleed
        self.badge_shadow = tk.Frame(self.badge_container, bg="#000000")
        self.badge_shadow.place(x=4, y=4, width=278, height=30)

        # Solid black border using raw tk.Frame to prevent bleed
        self.badge_border = tk.Frame(self.badge_container, bg="#000000")
        self.badge_border.place(x=0, y=0, width=276, height=30)
        self.badge_border.pack_propagate(False)

        self.badge = ctk.CTkFrame(
            self.badge_border, 
            fg_color="#00FFFF", # Pure Cyan
            corner_radius=0,
            border_width=0,  # Native tk.Frame handles the border now
        )
        self.badge.pack(expand=True, fill="both", padx=3, pady=3)
        self.badge.pack_propagate(False)
        
        self.badge_label = ctk.CTkLabel(
            self.badge,
            text="SECANT METHOD",
            font=ctk.CTkFont(family="Space Grotesk", size=15, weight="bold"),
            text_color="#000000",
            justify="center",
            wraplength=252,
        )
        self.badge_label.pack(expand=True, fill="both", padx=6, pady=4)

        # -------------------
        # 3. ACTIONS (RIGHT)
        # -------------------
        self.actions_container = ctk.CTkFrame(self, fg_color="transparent")
        # Anchor east (right side) and rely 0.5 (vertically centered)
        self.actions_container.place(relx=1.0, x=-20, rely=0.5, anchor="e")

        # Settings Container
        self.settings_container = ctk.CTkFrame(self.actions_container, fg_color="transparent", width=44, height=44)
        self.settings_container.pack(side="left", padx=(0, 10))
        self.settings_container.pack_propagate(False)

        # Shadow
        self.settings_shadow = ctk.CTkFrame(self.settings_container, fg_color="#000000", corner_radius=0, width=40, height=40)
        self.settings_shadow.place(x=4, y=4)

        # Load action icons
        try:
            from PIL import Image
            settings_image = Image.open("assets/setting_icon_black.png")
            settings_icon = ctk.CTkImage(light_image=settings_image, size=(20, 20))
            
            help_image = Image.open("assets/question_icon_black.png")
            help_icon = ctk.CTkImage(light_image=help_image, size=(20, 20))
        except FileNotFoundError:
            settings_icon = None
            help_icon = None

        # Settings Button
        self.settings_btn = ctk.CTkButton(
            self.settings_container,
            text="", # Clean empty text, use icon
            image=settings_icon,
            width=40,
            height=40,
            corner_radius=0,
            fg_color="#FFFFFF",
            hover_color="#E2E8F0",
            text_color="#000000",
            border_width=3,
            border_color="#000000"
        )
        self.settings_btn.place(x=0, y=0)

        # Help Container
        self.help_container = ctk.CTkFrame(self.actions_container, fg_color="transparent", width=44, height=44)
        self.help_container.pack(side="left")
        self.help_container.pack_propagate(False)

        # Shadow
        self.help_shadow = ctk.CTkFrame(self.help_container, fg_color="#000000", corner_radius=0, width=40, height=40)
        self.help_shadow.place(x=4, y=4)

        # Help Button
        self.help_btn = ctk.CTkButton(
            self.help_container,
            text="", # Clean empty text, use icon
            image=help_icon,
            width=40,
            height=40,
            corner_radius=0,
            fg_color="#FFFFFF",
            hover_color="#E2E8F0",
            text_color="#000000",
            border_width=3,
            border_color="#000000"
        )
        self.help_btn.place(x=0, y=0)

    def bind_dev_tools(self, valid_filler_callback, invalid_filler_callback):
        """Binds the secret developer filler tools to the header titles."""
        # Main Title -> Valid Inputs
        self.title_main.bind("<Button-1>", valid_filler_callback)
        self.title_main.configure(cursor="hand2")
        self.title_sub.bind("<Button-1>", valid_filler_callback)
        self.title_sub.configure(cursor="hand2")
        
        # Sub Badge -> Invalid Inputs
        self.badge_label.bind("<Button-1>", invalid_filler_callback)
        self.badge_label.configure(cursor="hand2")

    def set_help_callback(self, callback) -> None:
        """Assigns the About/Help action for the header help button."""
        self.help_btn.configure(command=callback)

    def set_method_badge(self, method_name: str) -> None:
        """Updates the header badge to reflect the currently selected method."""
        normalized = (method_name or "").strip().lower()
        if "secant" in normalized:
            sticker_color = "#00FFFF"
            label = "SECANT METHOD"
        elif "bisection" in normalized:
            sticker_color = "#FFFF00"
            label = "BISECTION METHOD"
        elif normalized:
            sticker_color = "#FFFFFF"
            label = method_name.strip().upper()
        else:
            sticker_color = "#00FFFF"
            label = "SECANT METHOD"

        self.badge.configure(fg_color=sticker_color)
        if len(label) <= 18:
            font_size = 15
            display = label
        elif len(label) <= 24:
            font_size = 13
            display = label
        else:
            font_size = 12
            display = f"{label[:21]}..."

        self.badge_label.configure(
            text=display,
            font=ctk.CTkFont(family="Space Grotesk", size=font_size, weight="bold"),
        )
