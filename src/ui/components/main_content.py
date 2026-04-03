import tkinter as tk
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from typing import Optional, List
import random
from datetime import datetime
from src.utils.tooltip import Tooltip
from src.utils.warning_classification import format_log_title, resolve_message_level
from src.ui.app_metadata import APP_MILESTONE, APP_VERSION


class MainContentFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Transparent so the app's mint green background bleeds through
        super().__init__(master, fg_color="transparent", corner_radius=0, **kwargs)
        
        # 2 Column Split (60% / 40%)
        self.grid_columnconfigure(0, weight=3) # Left Graph
        self.grid_columnconfigure(1, weight=2) # Right Log
        self.grid_rowconfigure(0, weight=1)

        # ---------------------------------------------------------
        # LEFT COLUMN (POP-ART GRAPH)
        # ---------------------------------------------------------
        self.graph_container = ctk.CTkFrame(self, fg_color="transparent")
        self.graph_container.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        self.graph_container.grid_columnconfigure(0, weight=1)
        self.graph_container.grid_rowconfigure(1, weight=1)

        # The Sticker Status (Floats above or sits on top)
        self.result_frame = ctk.CTkFrame(
            self.graph_container, 
            corner_radius=0, 
            fg_color="#FFFF00", # Chunky yellow sticker
            border_width=3, 
            border_color="#000000"
        )
        self.result_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.result_title = ctk.CTkLabel(
            self.result_frame, 
            text="STATUS",
            font=ctk.CTkFont(family="Space Grotesk", size=14, weight="bold"),
            text_color="#000000"
        )
        self.result_title.pack(anchor="w", padx=10, pady=(5, 0))
        
        self.result_value = ctk.CTkLabel(
            self.result_frame, 
            text="AWAITING INPUT",
            font=ctk.CTkFont(family="Space Grotesk", size=32, weight="bold"),
            text_color="#000000"
        )
        self.result_value.pack(anchor="w", padx=10)

        self.result_status = ctk.CTkLabel(
            self.result_frame, 
            text="ENTER PARAMETERS TO BEGIN",
            font=ctk.CTkFont(family="Space Mono", size=12, weight="bold"),
            text_color="#000000"
        )
        self.result_status.pack(anchor="w", padx=10, pady=(0, 10))

        # The Graph Frame
        self.graph_frame = ctk.CTkFrame(
            self.graph_container, 
            corner_radius=0, 
            fg_color="#FFFFFF", 
            border_width=3, 
            border_color="#000000"
        )
        self.graph_frame.grid(row=1, column=0, sticky="nsew")
        self.graph_frame.grid_columnconfigure(0, weight=1)
        self.graph_frame.grid_rowconfigure(0, weight=1)

        # Brutalist Matplotlib Figure
        self.figure = Figure(figsize=(5, 4), dpi=100, facecolor='#FFFFFF')
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#FFFFFF')
        self.ax.tick_params(colors='#000000', labelsize=10, width=2)
        
        # Thick black spines
        for spine in self.ax.spines.values():
            spine.set_color('#000000')
            spine.set_linewidth(3)
            
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        
        self._show_graph_placeholder()

        # ---------------------------------------------------------
        # RIGHT COLUMN (DOT-MATRIX RECEIPT LOG)
        # ---------------------------------------------------------
        self.log_container = ctk.CTkFrame(self, fg_color="transparent")
        self.log_container.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self.log_container.grid_columnconfigure(0, weight=1)
        self.log_container.grid_rowconfigure(0, weight=1)

        # 1. Outer black shadow (Raw tk.Frame avoids CTk Canvas sub-pixel bleeding!)
        # Offset using pure absolute math relative to the container. relwidth=1.0 - 6px means it matches the border layer exactly!
        self.log_unified_shadow = tk.Frame(self.log_container, bg="#000000")
        self.log_unified_shadow.place(relwidth=1.0, relheight=1.0, x=6, y=6, width=-6, height=-6)

        # 2. Border layer (Raw tk.Frame)
        # Gridded to automatically force the log_container to respects its children's minimum sizes.
        self.log_border_layer = tk.Frame(self.log_container, bg="#000000")
        self.log_border_layer.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=(0, 6))

        # 3. Actual white main container (CTkFrame inside the tk.Frame border)
        # Packed with 3px to reveal the black border layer underneath it.
        self.log_unified_main = ctk.CTkFrame(self.log_border_layer, fg_color="#F8F8F8", corner_radius=0)
        self.log_unified_main.pack(fill="both", expand=True, padx=3, pady=3)

        # 1. Header Frame inside unified main
        self.log_header_frame = ctk.CTkFrame(self.log_unified_main, fg_color="transparent", corner_radius=0)
        # Pack header inside main box
        self.log_header_frame.pack(fill="x", pady=(3, 0))

        # Title with Icon
        self.log_title_frame = ctk.CTkFrame(self.log_header_frame, fg_color="transparent")
        self.log_title_frame.pack(side="left", padx=10, pady=8)
        
        # Load terminal icon (optional)
        try:
            from PIL import Image
            term_icon = ctk.CTkImage(light_image=Image.open("assets/log_icon_black.png"), size=(20, 20))
        except FileNotFoundError:
            term_icon = None

        self.log_header_lbl = ctk.CTkLabel(
            self.log_title_frame, 
            text="ALGORITHMIC LOG",
            image=term_icon,
            compound="left",
            padx=5,
            font=ctk.CTkFont(family="Space Grotesk", size=22, weight="bold"),
            text_color="#000000"
        )
        self.log_header_lbl.pack(side="left")

        # Action Buttons (Download)
        self.log_actions_frame = ctk.CTkFrame(self.log_header_frame, fg_color="transparent")
        self.log_actions_frame.pack(side="right", padx=(0, 10), pady=8)
        
        try:
            from PIL import Image
            dl_icon = ctk.CTkImage(light_image=Image.open("assets/download_icon_black.png"), size=(20, 20))
        except FileNotFoundError:
            dl_icon = None

        self.dl_btn = ctk.CTkButton(self.log_actions_frame, text="", image=dl_icon, width=34, height=34, corner_radius=0, fg_color="#F8F8F8", hover_color="#E2E8F0", border_width=2, border_color="#000000")
        self.dl_btn.pack(side="left", padx=4)
        Tooltip(self.dl_btn, "Download the algorithmic log as a text file")

        # 2. Horizontal Black Separator Line
        self.log_separator = ctk.CTkFrame(self.log_unified_main, fg_color="#000000", height=3, corner_radius=0)
        # Pad left and right to touch the inside of the 3px borders but not overwrite them
        self.log_separator.pack(fill="x", padx=3)

        # 3. Scrollable Log Area (No border)
        self.log_scroll_frame = ctk.CTkScrollableFrame(
            self.log_unified_main, 
            corner_radius=0,
            border_width=0,
            fg_color="transparent" # Let the unified main #F8F8F8 show through
        )
        # Pad exactly to fit within the 3px border, padding bottom 3px
        self.log_scroll_frame.pack(fill="both", expand=True, padx=3, pady=(0, 3))
        
        self._wrap_length = 350
        self.log_scroll_frame.bind("<Configure>", self._update_wraplength, add="+")
        
        self.reset_view()

    def _update_wraplength(self, event):
        self._wrap_length = max(200, event.width - 40)
        stack = list(self.log_scroll_frame.winfo_children())
        while stack:
            widget = stack.pop()
            stack.extend(widget.winfo_children())
            if isinstance(widget, ctk.CTkLabel):
                try:
                    if int(widget.cget("wraplength")) != 0:
                        widget.configure(wraplength=self._wrap_length)
                except (TypeError, ValueError, tk.TclError):
                    continue

    def _clear_log(self):
        """Destroys all child widgets in the scrollable log frame, resetting it to empty."""
        for widget in self.log_scroll_frame.winfo_children():
            widget.destroy()

    def _append_log(self, text: str, title: Optional[str] = None, style: str = "normal"):
        """Appends a styled text block to the algorithmic log.

        Args:
            text: The body content to display.
            title: Optional heading rendered as a Neo-Brutalist badge above the text.
            style: Visual style ('normal', 'success', 'warning', 'error', 'code') controlling badge color.
        """
        frame = ctk.CTkFrame(self.log_scroll_frame, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=(5, 5))
        
        if title:
            # Title gets Cyan, Magenta, or Yellow based on style
            if style in {"normal", "success"}:
                bg_color = "#00FFFF"
            elif style == "warning":
                bg_color = "#FFB347"
            elif style == "code":
                bg_color = "#FFFF00"
            else:
                bg_color = "#FF00FF"
            
            # Neo-Brutalist Shadow Container for Title
            title_container = ctk.CTkFrame(frame, fg_color="transparent")
            title_container.pack(anchor="w", pady=(0, 5))
            
            title_shadow = ctk.CTkFrame(title_container, fg_color="#000000", corner_radius=0)
            title_shadow.pack(anchor="w") 
            
            lbl_title_frame = ctk.CTkFrame(title_shadow, fg_color=bg_color, corner_radius=0, border_width=2, border_color="#000000")
            lbl_title_frame.pack(anchor="w", padx=(0, 3), pady=(0, 3)) 
            
            lbl_title = ctk.CTkLabel(
                lbl_title_frame, 
                text=format_log_title(title, style),
                font=ctk.CTkFont(family="Space Grotesk", size=16, weight="bold"), 
                text_color="#000000"
            )
            lbl_title.pack(padx=8, pady=4)
            
        color = "#000000"
        font = ctk.CTkFont(family="Space Mono", size=14, weight="bold")
            
        lbl_text = ctk.CTkLabel(frame, text=text, font=font, text_color=color, justify="left", wraplength=self._wrap_length)
        lbl_text.pack(anchor="w")

    def _append_method_log(self, method_name: str, supporting_text: str):
        """Renders a compact dedicated METHOD block for the selected solver."""
        normalized = (method_name or "").strip().lower()
        if "secant" in normalized:
            method_color = "#00FFFF"
            method_label = "SECANT"
        elif "bisection" in normalized:
            method_color = "#FFFF00"
            method_label = "BISECTION"
        elif normalized:
            method_color = "#FFFFFF"
            method_label = method_name.strip().upper()
        else:
            method_color = "#FFFFFF"
            method_label = "UNKNOWN"

        frame = ctk.CTkFrame(self.log_scroll_frame, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=(5, 6))

        method_container = ctk.CTkFrame(frame, fg_color="transparent")
        method_container.pack(anchor="w", pady=(0, 4))

        method_shadow = ctk.CTkFrame(method_container, fg_color="#000000", corner_radius=0)
        method_shadow.pack(anchor="w")

        method_box = ctk.CTkFrame(
            method_shadow,
            fg_color=method_color,
            corner_radius=0,
            border_width=2,
            border_color="#000000",
        )
        method_box.pack(anchor="w", padx=(0, 3), pady=(0, 3))

        method_row = ctk.CTkFrame(method_box, fg_color="transparent")
        method_row.pack(anchor="w", padx=10, pady=6)

        method_prefix = ctk.CTkLabel(
            method_row,
            text="Method:",
            font=ctk.CTkFont(family="Space Mono", size=13, weight="bold"),
            text_color="#000000",
            justify="left",
        )
        method_prefix.pack(side="left")

        method_text = ctk.CTkLabel(
            method_row,
            text=f" {method_label}",
            font=ctk.CTkFont(family="Space Grotesk", size=16, weight="bold"),
            text_color="#000000",
            justify="left",
            wraplength=self._wrap_length - 40,
        )
        method_text.pack(side="left")

        support = (supporting_text or "").strip() or "Algorithm Initialized."
        support_label = ctk.CTkLabel(
            frame,
            text=support,
            font=ctk.CTkFont(family="Space Mono", size=14, weight="bold"),
            text_color="#000000",
            justify="left",
            wraplength=self._wrap_length,
        )
        support_label.pack(anchor="w")

    def add_step(self, heading: str, content: str, style: str = "normal"):
        """Adds a formally headed step to the algorithmic trail log.

        Args:
            heading: The trail heading label (e.g., 'GIVEN', 'METHOD', 'FINAL').
            content: The body text content for this step.
            style: Visual style ('normal', 'success', 'warning', 'error', 'code') controlling badge color.
        """
        normalized_heading = (heading or "").strip().upper()
        if normalized_heading == "METHOD":
            parts = (content or "").split("\n", 1)
            method_name = parts[0] if parts else "Unknown"
            supporting_text = parts[1] if len(parts) > 1 else "Algorithm Initialized."
            self._append_method_log(method_name, supporting_text)
            return

        self._append_log(content, title=heading, style=style)

    def set_computing_status(
        self,
        expr_str: str,
        x0: float,
        x1: float,
        tol: float,
        method_name: str = "Secant",
        label_left: str = "x0",
        label_right: str = "x1"
    ):
        self.result_value.configure(text="CALCULATING...", text_color="#000000") 
        self.result_status.configure(text="PROCESSING INPUTS...", text_color="#000000")
        
        self._clear_log()
        
        session_id = f"#{random.randint(0, 99):02X}{random.randint(0, 99):02X}-{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
        timestamp = datetime.utcnow().strftime("%H:%M:%S")
        boot_msg = f"NeuroSolve Processor {APP_VERSION} ({APP_MILESTONE})\nSESSION ID: {session_id}\nTIMESTAMP: {timestamp} UTC\n{'-'*41}"
        
        frame = ctk.CTkFrame(self.log_scroll_frame, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=(15, 15))
        
        # Render the centered boot text block
        font = ctk.CTkFont(family="Space Mono", size=13, weight="bold")
        lbl_text = ctk.CTkLabel(frame, text=boot_msg, font=font, text_color="#7A7A7A", justify="center")
        lbl_text.pack(anchor="center")

        self.add_step("GIVEN", f"Function: f(x) = {expr_str}\n{label_left}={x0} | {label_right}={x1} | tol={tol}", style="code")
        self.add_step("METHOD", f"{method_name}\nAlgorithm Initialized.", style="normal")
        self.add_step("STEPS", "Beginning numerical iteration sequence...", style="normal")

    def update_success(self, root: float, iterations: int):
        self.add_step("FINAL", f"Root bounded at x = {root:.8f}", style="success")
        self.add_step("VERIFICATION", f"f({root:.6f}) ≈ 0\nResidual error mapping is within acceptable tolerance constraints.", style="success")
        self.add_step("SUMMARY", f"The Root Finder protocol successfully converged to the root after {iterations} mathematical steps.", style="normal")
        
        self.result_frame.configure(fg_color="#00FFFF") # Cyan sticker for success
        self.result_value.configure(text=f"{root:.6f}")
        self.result_status.configure(text=f"ROOT FOUND IN {iterations} ITERS")

    def update_error(
        self,
        message: str,
        root_so_far: Optional[float] = None,
        total_iters: int = 0,
        message_level: Optional[str] = None,
    ):
        classification = resolve_message_level(message_level, message)
        if classification == "warning":
            self.add_step(
                "SUMMARY",
                f"Calculation completed with a handled warning.\n{message}",
                style="warning",
            )
            self.result_frame.configure(fg_color="#FFB347")
            if root_so_far is not None:
                self.result_value.configure(text=f"{root_so_far:.6f}")
            else:
                self.result_value.configure(text="WARN")
            self.result_status.configure(text=f"WARNING ({total_iters} ITERS): REVIEW TRAIL")
            return

        self.add_step("SUMMARY", f"Calculation halted due to algorithmic failure.\n{message}", style="error")
        self.result_frame.configure(fg_color="#FF00FF") # Magenta sticker for error
        if root_so_far is not None:
            self.result_value.configure(text=f"{root_so_far:.6f}")
        else:
            self.result_value.configure(text="NULL")
        self.result_status.configure(text=f"FAILED ({total_iters} ITERS): ERROR")
        
    def render_log_history(self, history_list: List[dict]):
        """
        Renders the step-by-step mathematical execution trail onto the UI scroll plane.

        Args:
            history_list (List[dict]): A list of dictionaries generated by the solver. 
                                       Expected keys are:
                                       - 'n' (int): Iteration number.
                                       - 'x_n' (float): The current x estimate.
                                       - 'f(x_n)' (float): The evaluated function at x.
                                       - 'error' (float): The calculated residual error.
                                       - 'explanation' (str): Plain english description of the step.
        """
        # ARCHITECTURAL OVERRIDE: Render entries in a single optimized block to prevent UI lag.
        for index, step in enumerate(history_list):
            n = step['n']
            xn = step['x_n']
            fxn = step['f(x_n)']
            err = step['error']
            explanation = step.get('explanation', 'No explanation provided.')
            
            # Format combined mathematical block using f-strings for alignment
            math_text = f"x_curr:      {xn:.6f}\nf(x):        {fxn:.6f}"
            if err is not None:
                err_str = f"{err:.6e}" if err < 0.0001 else f"{err:.6f}"
                math_text += f"\nerror:       {err_str}"
            else:
                math_text += f"\nerror:       --"
                
            # Simulate the vertical indentation line using a left border on the container frame
            frame = ctk.CTkFrame(self.log_scroll_frame, fg_color="transparent") 
            frame.pack(fill="x", padx=10, pady=(5, 15))
            
            inner_content = ctk.CTkFrame(frame, fg_color="transparent")
            inner_content.pack(fill="both", expand=True, padx=(16, 0)) # Indent content
            
            # Vertical line (absolute positioned to left edge of inner content)
            vline = ctk.CTkFrame(frame, fg_color="#000000", width=2)
            vline.place(relheight=1.0, x=4, y=14) # Simulate line starting below the node
            
            # Fancy Node Point
            node_point = ctk.CTkFrame(frame, fg_color="#00FFFF", border_color="#000000", border_width=2, width=10, height=10, corner_radius=10)
            node_point.place(x=0, y=10)

            # Neo-Brutalist Title Box
            title_container = ctk.CTkFrame(inner_content, fg_color="transparent")
            title_container.pack(anchor="w", pady=(0, 10))
            
            title_shadow = ctk.CTkFrame(title_container, fg_color="#000000", corner_radius=0)
            title_shadow.pack(anchor="w")
            
            lbl_title_frame = ctk.CTkFrame(title_shadow, fg_color="#00FFFF", corner_radius=0, border_width=2, border_color="#000000")
            lbl_title_frame.pack(anchor="w", padx=(0, 3), pady=(0, 3))
            
            # Use index + 1 for pure UI auto-numbering, completely decoupled from math logic
            lbl_title = ctk.CTkLabel(lbl_title_frame, text=f"STEP {index + 1:02d}", font=ctk.CTkFont(family="Space Grotesk", size=16, weight="bold"), text_color="#000000")
            lbl_title.pack(padx=8, pady=2)
            
            # Human Explanation (Directly below title)
            lbl_exp = ctk.CTkLabel(inner_content, text=explanation, font=ctk.CTkFont(family="Space Grotesk", size=15), text_color="#000000", justify="left", wraplength=self._wrap_length - 20)
            lbl_exp.pack(anchor="w", pady=(0, 6))
            
            # Mathematical Data (Combined text block for performance)
            lbl_math = ctk.CTkLabel(inner_content, text=math_text, font=ctk.CTkFont(family="Space Mono", size=15, weight="bold"), text_color="#000000", justify="left")
            lbl_math.pack(anchor="w")

            # PERFORMANCE FIX: Flush UI tasks every 5 iterations to prevent freezing
            if index > 0 and index % 5 == 0:
                self.update_idletasks()

    def log_input_error(self, error_msg: str):
        self._clear_log()
        self.add_step("SUMMARY", f"VALIDATION FAIL\n{error_msg}", style="error")
        self.result_frame.configure(fg_color="#FF00FF")
        self.result_value.configure(text="ERROR")
        self.result_status.configure(text="BAD INPUT. CHECK PARAMETERS.")
        self._show_graph_placeholder()

    def log_unexpected_error(self, error_msg: str):
        self._clear_log()
        self.add_step("SUMMARY", f"FATAL SYSTEM CRASH\n{error_msg}", style="error")
        self.result_frame.configure(fg_color="#FF00FF")
        self.result_value.configure(text="CRASH")
        self.result_status.configure(text="SYSTEM FAILURE.")
        self._show_graph_placeholder()

    def reset_view(self):
        self.result_frame.configure(fg_color="#FFFF00") # Yellow
        self.result_value.configure(text="STANDBY")
        self.result_status.configure(text="SYSTEM READY. ENTER COMMAND.")
        
        self._clear_log()
        self._show_graph_placeholder()
        self._show_standby_screen()

    def _show_standby_screen(self):
        """Renders a faux-terminal diagnostics screen as the idle state placeholder."""
        boot_msg = (
            "=========================================\n"
            "      NEUROSOLVE.NEO SECANT ENGINE       \n"
            "=========================================\n\n"
            "[ SYS_STATUS ] : STANDBY\n"
            "[  MEMORY  ]   : ALLOCATED\n"
            "[ ALGORITHM ]  : SECANT METHOD ROUTINE\n\n"
            "> Awaiting parameter input...\n"
            "> Configure [X0, X1, TOLERANCE] above.\n"
            "> Initialize sequence via [CALCULATE]."
        )
        
        frame = ctk.CTkFrame(self.log_scroll_frame, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=(40, 15))
        
        font = ctk.CTkFont(family="Space Mono", size=13, weight="bold")
        lbl_text = ctk.CTkLabel(frame, text=boot_msg, font=font, text_color="#7A7A7A", justify="left")
        lbl_text.pack(anchor="center")

    def _show_graph_placeholder(self):
        self.ax.clear()
        self.ax.text(0.5, 0.5, "NO SIGNAL", 
                     horizontalalignment='center', verticalalignment='center', 
                     transform=self.ax.transAxes, color='#000000', fontfamily="Space Grotesk", fontweight="bold", fontsize=24)
        self.ax.grid(True, color="#000000", linewidth=2)
        self.canvas.draw_idle()

    def render_iteration_table(self, func_str: str, history_list: List[dict], root: float, iterations: int, method_name: str = "Secant"):
        """Renders a detailed iteration table showing method progression.

        Args:
            func_str: The function string for the title
            history_list: List of iteration history dictionaries
            root: The final root value
            iterations: Number of iterations performed
            method_name: Display name for the method
        """
        sep_frame = ctk.CTkFrame(self.log_scroll_frame, fg_color="transparent")
        sep_frame.pack(fill="x", padx=10, pady=(15, 10))
        sep_line = ctk.CTkFrame(sep_frame, fg_color="#000000", height=2)
        sep_line.pack(fill="x")

        title_text = (
            f"Approximate root of the equation {func_str} using {method_name} method "
            f"is {root:.4f} (After {iterations} iterations)"
        )
        title_frame = ctk.CTkFrame(self.log_scroll_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=10, pady=(5, 15))

        title_label = ctk.CTkLabel(
            title_frame,
            text=title_text,
            font=ctk.CTkFont(family="Space Grotesk", size=13, weight="bold"),
            text_color="#000000",
            wraplength=self._wrap_length - 20
        )
        title_label.pack(anchor="w")

        table_frame = ctk.CTkFrame(self.log_scroll_frame, fg_color="transparent")
        table_frame.pack(fill="x", padx=10, pady=(0, 10))

        header_bg = "#FFFF00"
        row_bg_normal = "#F8F8F8"
        row_bg_alt = "#FFFFFF"
        border_color = "#000000"

        method_key = (method_name or "").lower()
        if "bisection" in method_key:
            headers = ["n", "a", "b", "mid", "f(mid)", "error"]
        else:
            headers = ["n", "x0", "f(x0)", "x1", "f(x1)", "x2", "f(x2)", "Update"]

        header_frame = ctk.CTkFrame(table_frame, fg_color=header_bg, border_width=2, border_color=border_color, corner_radius=0)
        header_frame.pack(fill="x", pady=(0, 0))

        for header in headers:
            col_frame = ctk.CTkFrame(header_frame, fg_color=header_bg, corner_radius=0)
            col_frame.pack(side="left", fill="both", expand=True, padx=1, pady=1)

            label = ctk.CTkLabel(
                col_frame,
                text=header,
                font=ctk.CTkFont(family="Space Mono", size=11, weight="bold"),
                text_color="#000000"
            )
            label.pack(pady=4, padx=4)

        if "bisection" in method_key:
            row_num = 1
            for step in history_list:
                if step.get("is_mid") is False:
                    continue

                a_val = step.get("a")
                b_val = step.get("b")
                mid_val = step.get("x_n")
                f_mid_val = step.get("f(x_n)")
                err_val = step.get("error")

                if a_val is None or b_val is None or mid_val is None or f_mid_val is None:
                    continue

                row_bg = row_bg_alt if row_num % 2 == 0 else row_bg_normal
                data_frame = ctk.CTkFrame(table_frame, fg_color=row_bg, border_width=1, border_color=border_color, corner_radius=0)
                data_frame.pack(fill="x", pady=(0, 0))

                row_data = [
                    str(row_num),
                    f"{a_val:.4f}",
                    f"{b_val:.4f}",
                    f"{mid_val:.4f}",
                    f"{f_mid_val:.4f}",
                    f"{err_val:.6f}" if err_val is not None else "--",
                ]

                for cell_data in row_data:
                    col_frame = ctk.CTkFrame(data_frame, fg_color=row_bg, corner_radius=0)
                    col_frame.pack(side="left", fill="both", expand=True, padx=1, pady=1)

                    label = ctk.CTkLabel(
                        col_frame,
                        text=cell_data,
                        font=ctk.CTkFont(family="Space Mono", size=10),
                        text_color="#000000",
                        justify="center"
                    )
                    label.pack(pady=3, padx=3)

                row_num += 1
        else:
            row_num = 1
            for i in range(len(history_list) - 2):
                if i + 2 < len(history_list):
                    x0_entry = history_list[i]
                    x1_entry = history_list[i + 1]
                    x2_entry = history_list[i + 2]

                    x0_val = x0_entry['x_n']
                    f_x0_val = x0_entry['f(x_n)']
                    x1_val = x1_entry['x_n']
                    f_x1_val = x1_entry['f(x_n)']
                    x2_val = x2_entry['x_n']
                    f_x2_val = x2_entry['f(x_n)']

                    row_bg = row_bg_alt if row_num % 2 == 0 else row_bg_normal
                    data_frame = ctk.CTkFrame(table_frame, fg_color=row_bg, border_width=1, border_color=border_color, corner_radius=0)
                    data_frame.pack(fill="x", pady=(0, 0))

                    row_data = [
                        str(row_num),
                        f"{x0_val:.4f}",
                        f"{f_x0_val:.4f}",
                        f"{x1_val:.4f}",
                        f"{f_x1_val:.4f}",
                        f"{x2_val:.4f}",
                        f"{f_x2_val:.4f}",
                        "x0 = x1\nx1 = x2"
                    ]

                    for cell_data in row_data:
                        col_frame = ctk.CTkFrame(data_frame, fg_color=row_bg, corner_radius=0)
                        col_frame.pack(side="left", fill="both", expand=True, padx=1, pady=1)

                        label = ctk.CTkLabel(
                            col_frame,
                            text=cell_data,
                            font=ctk.CTkFont(family="Space Mono", size=10),
                            text_color="#000000",
                            justify="center"
                        )
                        label.pack(pady=3, padx=3)

                    row_num += 1

    def draw_graph(self, x_curve: list, y_curve: list, history: list):
        self.ax.clear()
        
        # Brutalist thick grid
        self.ax.grid(True, color="#000000", linewidth=1, linestyle="-")
        
        # Main pop-art cyan curve
        self.ax.plot(x_curve, y_curve, color="#00FFFF", linewidth=4, label="$f(x)$", zorder=3)
        self.ax.axhline(0, color="#000000", linewidth=3, zorder=2) # X-axis
        
        # Plot iteration points with massive markers
        if history:
            x_points = [step['x_n'] for step in history]
            y_points = [step['f(x_n)'] for step in history]
            
            # Initial guesses
            self.ax.scatter(x_points[:2], y_points[:2], color="#FFFF00", edgecolors="#000000", linewidths=2, s=150, zorder=5, label="INITIAL")
            
            # intermediate points
            if len(x_points) > 2:
                 self.ax.scatter(x_points[2:-1], y_points[2:-1], color="#000000", s=60, marker="x", linewidths=3, zorder=5, label="STEPS")
            
            # Final point
            final_color = "#00FFFF" if (history[-1].get('error') or 1) < 1 else "#FF00FF"
            self.ax.scatter([x_points[-1]], [y_points[-1]], color=final_color, edgecolors="#000000", linewidths=3, s=250, zorder=6, label="TARGET")
            
        # Brutalist legend
        self.ax.legend(facecolor="#FFFFFF", edgecolor="#000000", labelcolor="#000000", prop={'family': 'Space Mono', 'weight': 'bold'})
        self.figure.tight_layout()
        self.canvas.draw_idle()
