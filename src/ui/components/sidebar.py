import customtkinter as ctk
import tkinter as tk
import os

# Set to "1" locally to enable dev fillers, disable for production.
IS_DEV_MODE = os.environ.get("NEUROSOLVE_DEV", "0") == "1"

if IS_DEV_MODE:
    from src.utils.dev_tools import get_random_test_case, get_invalid_test_case

class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master, calculate_callback, clear_callback, **kwargs):
        # Neo-Brutalist Strip: Mint green background, no internal borders
        super().__init__(master, fg_color="#A6FFD6", border_width=0, corner_radius=0, height=90, **kwargs)
        self.pack_propagate(False) # Force strict brutalist 90px height
        
        self.calculate_callback = calculate_callback
        self.clear_callback = clear_callback
        
        # We will use pack for a horizontal layout
        
        # Empty space padding container to offset from left edge if desired
        self.padding_frame = ctk.CTkFrame(self, fg_color="transparent", width=10)
        self.padding_frame.pack(side="left", fill="y")

        # Inputs Container (Middle)
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(side="left", expand=True, fill="x", padx=10, pady=(5, 5), anchor="w")

        self.func_entry = self._create_input_group(self.input_frame, "INITIAL f(x)", "|→", "x**2 - 4", width=160)
        self.x0_entry = self._create_input_group(self.input_frame, "INITIAL X0", "|→", "1.0", width=160)
        self.x1_entry = self._create_input_group(self.input_frame, "INITIAL X1", "→", "2.0", width=160)
        self.tol_entry = self._create_input_group(self.input_frame, "TOLERANCE", "×", "1e-6", width=160)
        self.iter_entry = self._create_input_group(self.input_frame, "MAX ITER.", "↻", "100", width=160)

        # Action Buttons (Rightmost)
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(side="right", padx=(10, 20), pady=(5, 5), anchor="e")

        # Clear Button Container & Shadow
        self.clear_container = ctk.CTkFrame(self.btn_frame, fg_color="transparent", width=84, height=49)
        self.clear_container.pack(side="left", padx=(0, 15), anchor="s")
        self.clear_container.pack_propagate(False)

        # Hard shadow using raw tk.Frame
        self.clear_shadow = tk.Frame(self.clear_container, bg="#000000")
        self.clear_shadow.place(x=4, y=4, width=80, height=45)

        # Border layer using raw tk.Frame
        self.clear_border = tk.Frame(self.clear_container, bg="#000000")
        self.clear_border.place(x=0, y=0, width=80, height=45)
        self.clear_border.pack_propagate(False)

        self.clear_button = ctk.CTkButton(
            self.clear_border, 
            text="CLEAR", 
            command=self.clear_callback,
            font=ctk.CTkFont(family="Space Grotesk", size=16, weight="bold"),
            corner_radius=0,
            fg_color="#FFFFFF",
            hover_color="#E2E8F0",
            text_color="#000000",
            border_width=0, # Border handled by parent tk.Frame now
        )
        # Pad by 3px symmetrically so the black border shows through under the button
        self.clear_button.pack(expand=True, fill="both", padx=3, pady=3)

        # Calculate Button Container & Shadow
        self.calc_container = ctk.CTkFrame(self.btn_frame, fg_color="transparent", width=194, height=54)
        self.calc_container.pack(side="right", padx=(0, 0), anchor="s")
        self.calc_container.pack_propagate(False)

        # Hard shadow using raw tk.Frame
        self.calc_shadow = tk.Frame(self.calc_container, bg="#000000")
        self.calc_shadow.place(x=4, y=4, width=190, height=50)

        # Border layer using raw tk.Frame
        self.calc_border = tk.Frame(self.calc_container, bg="#000000")
        self.calc_border.place(x=0, y=0, width=190, height=50)
        self.calc_border.pack_propagate(False)

        # Load the Icon (using a placeholder if the file doesn't exist yet)
        try:
            from PIL import Image
            calc_image = Image.open("assets/calc_icon_white.png")
            calc_icon = ctk.CTkImage(light_image=calc_image, size=(24, 24))
        except FileNotFoundError:
            calc_icon = None

        self.solve_button = ctk.CTkButton(
            self.calc_border, 
            text="CALCULATE", 
            image=calc_icon,
            compound="left",
            command=self.calculate_callback,
            font=ctk.CTkFont(family="Space Grotesk", size=20, weight="bold"),
            corner_radius=0,
            fg_color="#FF00FF", # Pure Magenta
            hover_color="#CC00CC", # Dim Magenta
            text_color="#FFFFFF",
            border_width=0, # Border handled by parent tk.Frame now
        )
        # Pad by 3px symmetrically so the black border shows through under the button
        self.solve_button.pack(expand=True, fill="both", padx=3, pady=3)

    def _create_input_group(self, parent, top_label_text, inner_icon_text, placeholder, width=160):
        """
        Creates a standardized Neo-Brutalist input field with a drop shadow.

        Args:
            parent: The CTkFrame to attach this widget to.
            top_label_text (str): The label displayed above the input (e.g., "INITIAL X0").
            inner_icon_text (str): The mathematical symbol shown inside the left of the box.
            placeholder (str): The ghost text shown when the input is empty.
            width (int): The absolute pixel width of the input field.

        Returns:
            ctk.CTkEntry: The actual text entry widget so its value can be retrieved later.
        """
        group = ctk.CTkFrame(parent, fg_color="transparent")
        group.pack(side="left", padx=(0, 15), anchor="s")
        
        label = ctk.CTkLabel(
            group, 
            text=top_label_text, 
            font=ctk.CTkFont(family="Space Grotesk", size=11, weight="bold"),
            text_color="#000000"
        )
        label.pack(anchor="w", pady=(0, 2))
        
        # Shadow container for the input box
        shadow_container = ctk.CTkFrame(group, fg_color="transparent", width=width+4, height=44)
        shadow_container.pack(anchor="w")
        shadow_container.pack_propagate(False)

        # Black shadow
        shadow = ctk.CTkFrame(shadow_container, fg_color="#000000", corner_radius=0, width=width, height=40)
        shadow.place(x=4, y=4)

        # White content box holding the icon and entry
        content_box = ctk.CTkFrame(
            shadow_container,
            fg_color="#FFFFFF",
            corner_radius=0,     # Sharp corners
            border_width=3,      # Thick black border
            border_color="#000000",
            width=width,
            height=40
        )
        content_box.place(x=0, y=0)
        content_box.pack_propagate(False)

        # Inner Icon/Symbol
        inner_icon_label = ctk.CTkLabel(
            content_box,
            text=inner_icon_text,
            font=ctk.CTkFont(family="Space Mono", size=16, weight="bold"),
            text_color="#000000",
            height=34
        )
        # Using a slight left padding to avoid the 3px border
        inner_icon_label.pack(side="left", padx=(7, 2), pady=3)

        # The actual entry widget inside the content box
        entry = ctk.CTkEntry(
            content_box, 
            placeholder_text=placeholder, 
            font=ctk.CTkFont(family="Space Mono", size=14, weight="bold"),
            width=50,            # CRITICAL: Overrides default 140px width which was stretching the frame
            height=34,
            corner_radius=0,
            border_width=0,      # We remove the CTkEntry border, the content_box provides the border
            fg_color="#FFFFFF",
            text_color="#000000",
            placeholder_text_color="#A0A0A0"
        )
        # Add a tiny bit of right padding so text doesn't hit the right border
        entry.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=3)

        return entry

    def _dev_fill_random_inputs(self, event=None):
        """DEV ONLY: Fills fields with curated valid random test cases."""
        if not IS_DEV_MODE:
            return
            
        test_case = get_random_test_case()
        
        self.clear_inputs()
        
        self.func_entry.insert(0, test_case["func"])
        self.x0_entry.insert(0, test_case["x0"])
        self.x1_entry.insert(0, test_case["x1"])
        self.tol_entry.insert(0, test_case["tol"])
        self.iter_entry.insert(0, test_case["max_iter"])

    def _dev_fill_invalid_inputs(self, event=None):
        """DEV ONLY: Fills fields with curated INVALID test cases to demo validation."""
        if not IS_DEV_MODE:
            return
            
        test_case = get_invalid_test_case()
        
        self.clear_inputs()
        
        self.func_entry.insert(0, test_case["func"])
        self.x0_entry.insert(0, test_case["x0"])
        self.x1_entry.insert(0, test_case["x1"])
        self.tol_entry.insert(0, test_case["tol"])
        self.iter_entry.insert(0, test_case["max_iter"])

    def get_inputs(self) -> dict:
        """Returns the raw string inputs currently in the sidebar."""
        return {
            "func": self.func_entry.get().strip(),
            "x0": self.x0_entry.get(),
            "x1": self.x1_entry.get(),
            "tol": self.tol_entry.get(),
            "max_iter": self.iter_entry.get()
        }

    def clear_inputs(self):
        """Clears the sidebar input fields."""
        self.func_entry.delete(0, 'end')
        self.x0_entry.delete(0, 'end')
        self.x1_entry.delete(0, 'end')
        self.tol_entry.delete(0, 'end')
        self.iter_entry.delete(0, 'end')
