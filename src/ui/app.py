import customtkinter as ctk
import sys
import time
from typing import Optional
import math
import numpy as np
import warnings
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import threading
from tkinter import filedialog, messagebox

# Suppress matplotlib font warnings for missing fonts (graceful fallback is built-in)
warnings.filterwarnings('ignore')

from src.utils.parsing import parse_math_expr
from src.utils.numeric_validation import normalize_numeric_text
from src.utils.solver_dispatch import get_solver_for_method
from src.ui.components.header import HeaderFrame
from src.ui.components.about_help_dialog import AboutHelpDialog
from src.ui.components.export_dialog import ExportFormatDialog
from src.ui.components.sidebar import SidebarFrame
from src.ui.components.main_content import MainContentFrame
from src.utils.report_export import (
    ExportError,
    build_default_report_filename,
    build_report_model,
    write_report,
)
from src.utils.warning_classification import resolve_message_level

# Configure appearance (We override defaults manually for Brutalism)
ctk.set_appearance_mode("light") # Pastel brutalism works best on light base
ctk.set_default_color_theme("blue") # We will override widget colors manually

class NeuroSolveApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.about_help_dialog: Optional[AboutHelpDialog] = None
        self.export_dialog: Optional[ExportFormatDialog] = None
        self._active_solve_session = 0
        self._export_snapshot = None

        # Window configuration
        self.title("NeuroSolve - Brutalist Control Deck")
        self.geometry("1400x850")  # Larger default to fit horizontal strip
        self.minsize(1100, 700)
        self.configure(fg_color="#F8F5F8") # Off-white brutalist background from HTML reference
        
        # Main Grid Layout: Top-Down Split
        # Row 0: Header (White, Logo, Settings)
        # Row 1: Header Border (Black)
        # Row 2: Command Strip (Mint Green, Inputs)
        # Row 3: Command Strip Border (Black)
        # Row 4: Content Area (Splits into Graph and Log)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)              # Expandable map area
        self.grid_columnconfigure(0, weight=3)           # Graph column
        self.grid_columnconfigure(1, weight=2)           # Log column

        # Initialize Header (Will bind dev tools after command strip is created)
        self.header = HeaderFrame(self)
        self.header.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)
        self.header.set_help_callback(self.open_about_help)
        
        # Header Bottom Border
        self.header_border = ctk.CTkFrame(self, fg_color="#000000", height=3, corner_radius=0)
        self.header_border.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

        # Initialize Command Strip (previously sidebar) across the middle
        self.command_strip = SidebarFrame(
            self, 
            calculate_callback=self.run_solver,
            clear_callback=self.clear_inputs
        )
        self.command_strip.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

        # Bind Dev Tools from Command Strip to Header Labels
        self.header.bind_dev_tools(
            self.command_strip._dev_fill_random_inputs,
            self.command_strip._dev_fill_invalid_inputs
        )

        # Keep header method badge in sync with UI selection
        self.header.set_method_badge(self.command_strip.method_var.get())
        self.command_strip.method_var.trace_add(
            "write",
            lambda *_: self.header.set_method_badge(self.command_strip.method_var.get()),
        )
        
        # Command Strip Bottom Border
        self.command_strip_border = ctk.CTkFrame(self, fg_color="#000000", height=3, corner_radius=0)
        self.command_strip_border.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

        # Initialize Main Content (Graph & Log) underneath
        self.main_content = MainContentFrame(self, export_callback=self.open_export_picker)
        self.main_content.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=20, pady=(10, 20))

    def open_about_help(self):
        """Opens the About/Help dialog and reuses an existing window if already open."""
        if self.about_help_dialog and self.about_help_dialog.winfo_exists():
            self.about_help_dialog.lift()
            self.about_help_dialog.focus_force()
            return

        self.about_help_dialog = AboutHelpDialog(self, on_close=self._on_about_help_closed)

    def _on_about_help_closed(self):
        self.about_help_dialog = None

    def clear_inputs(self):
        """Clears all inputs and resets the UI"""
        self.command_strip.clear_inputs()
        self._export_snapshot = None
        self.main_content.reset_view()

    def open_export_picker(self):
        """Open the export format picker when a trustworthy solve snapshot exists."""
        if not self._export_snapshot or not self._export_snapshot.get("export_enabled"):
            self.main_content.log_export_status(
                "Export is unavailable until the current run has a completed solve or handled warning.",
                style="warning",
            )
            self.main_content.set_export_enabled(False)
            return

        if self.export_dialog and self.export_dialog.winfo_exists():
            self.export_dialog.lift()
            self.export_dialog.focus_force()
            return

        self.export_dialog = ExportFormatDialog(
            self,
            on_select=self._start_export_flow,
            on_close=self._on_export_dialog_closed,
        )

    def _on_export_dialog_closed(self):
        self.export_dialog = None

    def _start_export_flow(self, format_name: str):
        try:
            default_name = build_default_report_filename(self._export_snapshot, format_name)
        except ExportError as exc:
            self.main_content.log_export_status(str(exc), style="error")
            return

        extension = f".{format_name}"
        filetypes = [
            (f"{format_name.upper()} report", f"*{extension}"),
            ("All files", "*.*"),
        ]
        save_path = filedialog.asksaveasfilename(
            parent=self,
            title=f"Save {format_name.upper()} Report",
            initialfile=default_name,
            defaultextension=extension,
            filetypes=filetypes,
        )
        if not save_path:
            self.main_content.log_export_status("Export canceled.", style="warning")
            return

        snapshot = deepcopy(self._export_snapshot)
        self.main_content.log_export_status(f"Exporting {format_name.upper()} report...", style="code")
        worker = threading.Thread(
            target=self._export_report_worker,
            args=(snapshot, Path(save_path), format_name),
            daemon=True,
        )
        worker.start()

    def _export_report_worker(self, snapshot, save_path: Path, format_name: str):
        try:
            model = build_report_model(snapshot)
            final_path = write_report(model, save_path, format_name)
        except ExportError as exc:
            message = str(exc)
            self.after(0, lambda: self.main_content.log_export_status(message, style="error"))
        except Exception as exc:
            message = f"Export failed: {exc}"
            self.after(0, lambda: self.main_content.log_export_status(message, style="error"))
        else:
            self.after(0, lambda: self._handle_export_success(final_path))

    def _handle_export_success(self, final_path: Path):
        self.main_content.log_export_status(f"Export successful. Report saved: {final_path}", style="success")
        messagebox.showinfo(
            "Export Successful",
            f"Solution trail report saved successfully:\n{final_path}",
            parent=self,
        )

    def _store_export_snapshot_if_current(self, solve_session_id: int, snapshot):
        if solve_session_id == self._active_solve_session:
            self._export_snapshot = snapshot

    def run_solver(self):
        """
        Orchestrates the entire computation pipeline.
        
        This method acts as the controller:
        1. Retrieves raw inputs from the UI.
        2. Validates domain requirements and updates the status labels.
        3. Parses the mathematical function string into an executable lambda.
        4. Invokes the selected mathematical solver.
        5. Formats the text log output.
        6. Defers the heavy matplotlib graph rendering to prevent UI freezing.
        """
        inputs = self.command_strip.get_inputs()
        method_name = (inputs.get("method") or "Secant").strip() or "Secant"
        method_key = method_name.lower()
        left_name = "a" if "bisection" in method_key else "x0"
        right_name = "b" if "bisection" in method_key else "x1"

        # Reflect selection in UI header immediately (even before solve completes)
        self.header.set_method_badge(method_name)
        
        # 1. Validate required fields
        expr_str = inputs["func"].strip()
        if not expr_str:
            self._export_snapshot = None
            self.main_content.set_export_enabled(False)
            self.main_content.log_input_error("Function f(x) is required. Please enter a function.")
            return
            
        try:
            # Validate and parse numerical inputs
            if not inputs["x0"].strip():
                self._export_snapshot = None
                self.main_content.set_export_enabled(False)
                self.main_content.log_input_error(f"Input '{left_name}' is required.")
                return
            if not inputs["x1"].strip():
                self._export_snapshot = None
                self.main_content.set_export_enabled(False)
                self.main_content.log_input_error(f"Input '{right_name}' is required.")
                return
            if not inputs["tol"].strip():
                self._export_snapshot = None
                self.main_content.set_export_enabled(False)
                self.main_content.log_input_error("Tolerance (ε) is required.")
                return
            if not inputs["max_iter"].strip():
                self._export_snapshot = None
                self.main_content.set_export_enabled(False)
                self.main_content.log_input_error("Max Iterations is required.")
                return

            numeric_valid, numeric_errors = self.command_strip.validate_numeric_inputs()
            if not numeric_valid:
                self._export_snapshot = None
                self.main_content.set_export_enabled(False)
                self.main_content.log_input_error("\n".join(numeric_errors))
                return

            x0 = float(normalize_numeric_text(inputs["x0"]))
            x1 = float(normalize_numeric_text(inputs["x1"]))
            try:
                tol = float(normalize_numeric_text(inputs["tol"]))
            except ValueError:
                self._export_snapshot = None
                self.main_content.set_export_enabled(False)
                self.main_content.log_input_error("Tolerance (ε) must be a valid decimal number.")
                return
            max_iter = int(normalize_numeric_text(inputs["max_iter"]))

            # Tie async callbacks to this solve request so stale prior runs
            # cannot overwrite newer UI state.
            self._active_solve_session += 1
            solve_session_id = self._active_solve_session
            self._export_snapshot = None
            self.main_content.set_export_enabled(False)

            # Architectural Override: UI responsiveness before math
            # update_idletasks forces the UI to render the "Calculating..." status 
            # before the heavy math blocking the main thread begins
            label_left = left_name
            label_right = right_name
            self.main_content.set_computing_status(expr_str, x0, x1, tol, method_name, label_left, label_right)
            self.update_idletasks()

            # 2. Safely parse string into a numerical evaluating lambda using SymPy
            callable_func = parse_math_expr(expr_str)
            self.main_content._append_log("> VALIDATION: PASS (Equation syntax and domains are clean)", style="code")

            # 3. Execute Solver
            try:
                solver_fn = get_solver_for_method(method_name)
            except ValueError as e:
                self._export_snapshot = None
                self.main_content.set_export_enabled(False)
                self.main_content.log_input_error(str(e))
                return

            result = solver_fn(callable_func, x0, x1, tol, max_iter)
            result.setdefault("method", method_name)
            result_message_level = resolve_message_level(result.get("message_level"), result.get("error_msg"))
            export_enabled = bool(result.get("converged")) or result_message_level == "warning"
            outcome_summary = self._build_outcome_summary(result, result_message_level)
            input_values = {
                label_left: x0,
                label_right: x1,
                "tol": tol,
                "max_iter": max_iter,
            }
            snapshot = {
                "expr_str": expr_str,
                "method_label": method_name,
                "input_values": input_values,
                "result": deepcopy(result),
                "verification": deepcopy(result.get("verification")),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "outcome_state": "success" if result.get("converged") else result_message_level,
                "outcome_summary": outcome_summary,
                "export_enabled": export_enabled,
            }
            self._store_export_snapshot_if_current(solve_session_id, snapshot)

            # 3. Render Step-by-Step History Log to "Trail Panel"
            self.main_content.render_log_history(result['history'])
            
            # 4. Render Iteration Table
            if result['history'] and result.get('root') is not None:
                self.main_content.render_iteration_table(expr_str, result['history'], result['root'], result['iterations'], result.get("method", method_name))
            
            # 5. Handle Outcome and update main Result & Status UI
            if result['converged']:
                self.main_content.update_success(
                    result['root'],
                    result['iterations'],
                    result.get("verification"),
                )
            else:
                self.main_content.update_error(
                    result['error_msg'],
                    result['root'],
                    result['iterations'],
                    result.get("message_level"),
                    result.get("verification"),
                )
            self.main_content.set_export_enabled(export_enabled)

            # 6. ASYNC GRAPH RENDERING
            # Plot generation is heavy. Using `self.after` lets the Tk mainloop draw
            # the text results BEFORE freezing exactly once to draw the Matplotlib graph.
            self.after(50, lambda: self.__generate_and_draw_graph(callable_func, x0, x1, result, solve_session_id))
                
        except ValueError as e:
             self._export_snapshot = None
             self.main_content.set_export_enabled(False)
             self.main_content.log_input_error(str(e))
        except Exception as e:
             self._export_snapshot = None
             self.main_content.set_export_enabled(False)
             self.main_content.log_unexpected_error(str(e))

    def _build_outcome_summary(self, result, message_level: str) -> str:
        if result.get("converged"):
            return (
                "The Root Finder protocol successfully converged to the root "
                f"after {result.get('iterations', 0)} mathematical steps."
            )
        message = str(result.get("error_msg") or "").strip()
        if message_level == "warning":
            return f"Calculation completed with a handled warning.\n{message}".strip()
        return f"Calculation halted due to algorithmic failure.\n{message}".strip()

    def __generate_and_draw_graph(self, func, x0, x1, result, solve_session_id):
        """
        Calculates the data points for plotting and passes RAW ARRAY DATA 
        to the Dumb UI component. This satisfies the Architectual Override.
        """
        try:
            if solve_session_id != self._active_solve_session:
                return

            history = result.get('history', [])
            
            # Smart padding for domain
            if history:
                all_x = [step['x_n'] for step in history] + [x0, x1]
                min_x = min(all_x)
                max_x = max(all_x)
            else:
                min_x, max_x = min(x0, x1), max(x0, x1)

            # Pad 20% on each side
            pad = (max_x - min_x) * 0.2
            if pad == 0: pad = 1.0
            
            x_min = min_x - pad
            x_max = max_x + pad

            # Generate 200 linspace points
            x_curve = np.linspace(x_min, x_max, 200).tolist()
            
            # Evaluate using a loop to avoid NumPy TypeCasting Crashes
            # and gracefully handle Math Domain errors (e.g. sqrt(-1))
            y_curve = []
            for x in x_curve:
                try:
                    y = func(x)
                    # Complex checks
                    if isinstance(y, complex):
                        y_curve.append(math.nan)
                    else:
                        y_curve.append(y)
                except Exception:
                    y_curve.append(math.nan)
            
            # Delegate to Dumb UI
            self.main_content.draw_graph(x_curve, y_curve, history)
            
        except Exception as e:
             print(f"Error drawing graph: {e}")

if __name__ == "__main__":
    app = NeuroSolveApp()
    app.mainloop()
