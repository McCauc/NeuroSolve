"""
Tooltip utility for CustomTkinter widgets.
Displays informative messages on hover.
"""
import customtkinter as ctk
import tkinter as tk

class Tooltip:
    """
    Create a tooltip for a given widget.
    Shows on hover, hides when mouse leaves.
    """
    def __init__(self, widget, text: str, delay: int = 400):
        """
        Args:
            widget: The CTkWidget to attach tooltip to
            text: The tooltip message text
            delay: Delay in milliseconds before showing tooltip
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.after_id = None
        
        # Bind hover events
        self.widget.bind("<Enter>", self._schedule_tooltip, add="+")
        self.widget.bind("<Leave>", self._hide_tooltip, add="+")
    
    def _schedule_tooltip(self, event=None):
        """Schedule the tooltip to appear after delay."""
        self._hide_tooltip()
        self.after_id = self.widget.after(self.delay, self._show_tooltip)
    
    def _show_tooltip(self):
        """Display the tooltip window."""
        if self.tooltip_window is not None:
            return
        
        try:
            # Get widget position
            x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
            
            # Create tooltip window
            self.tooltip_window = ctk.CTkToplevel(self.widget)
            self.tooltip_window.wm_overrideredirect(True)
            self.tooltip_window.wm_geometry(f"+{x}+{y}")
            self.tooltip_window.attributes('-topmost', True)
            
            # Create label with tooltip text
            label = ctk.CTkLabel(
                self.tooltip_window,
                text=self.text,
                bg_color="#000000",
                fg_color="#C3C3BF",
                text_color="#000000",
                padx=8,
                pady=4,
                font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
                corner_radius=4
            )
            label.pack()
            
        except tk.TclError:
            # Widget was destroyed
            pass
    
    def _hide_tooltip(self, event=None):
        """Hide the tooltip window."""
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        
        if self.tooltip_window is not None:
            try:
                self.tooltip_window.destroy()
            except tk.TclError:
                pass
            self.tooltip_window = None
