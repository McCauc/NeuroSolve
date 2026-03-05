# CustomTkinter GUI Development Guide

This document summarizes the best practices, modern widget implementations, theming, and gotchas for using CustomTkinter in the NeuroSolve project.

## 1. Core Layout: CTkFrame and Grid Systems
For responsive designs, the `grid` geometry manager combined with `grid_columnconfigure` and `grid_rowconfigure` is the most efficient approach in CustomTkinter. `CTkFrame` should be used as the primary container.

### Best Practices for Responsive Grids
1.  **Configure Weights:** Always configure weights (e.g., `weight=1`) on the parent container's rows and columns that need to expand or shrink dynamically.
2.  **Sticky Padding:** Use the `sticky` parameter (`"nsew"`) to make widgets stretch and fill their allocated grid cells.
3.  **Nested Frames:** Use nested `CTkFrame` widgets to build complex layouts rather than complex single grids.

### Code Snippet: Responsive Grid Layout
```python
import customtkinter as ctk

app = ctk.CTk()
app.geometry("400x300")

# Configure a responsive grid on the main window
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=2) # Column 1 will take twice the space of 0
app.grid_rowconfigure(0, weight=1)

# Create Frames
left_frame = ctk.CTkFrame(app)
left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

right_frame = ctk.CTkFrame(app)
right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

app.mainloop()
```

---

## 2. Modern Widgets: Details and Attributes

### `CTkButton`
Modern button with hover effects and rounded corners.
*   **Key Attributes:** `text`, `command`, `corner_radius`, `fg_color`, `hover_color`, `text_color`, `image` (requires CTkImage).
*   **Snippet:**
    ```python
    btn = ctk.CTkButton(master=left_frame, text="Solve", corner_radius=8,
                        command=lambda: print("Solving..."))
    btn.pack(pady=20)
    ```

### `CTkEntry`
A single-line text input field.
*   **Key Attributes:** `placeholder_text`, `width`, `height`, `corner_radius`, `border_width`, `border_color`, `fg_color`, `text_color`.
*   **Snippet:**
    ```python
    entry = ctk.CTkEntry(master=right_frame, placeholder_text="Enter f(x)...", width=200)
    entry.pack(pady=20, padx=20)
    ```

### `CTkScrollableFrame`
A frame that automatically adds vertical/horizontal scrollbars when content exceeds its explicit size. Replaces complex Canvas+Frame scrolling hacks in standard Tkinter.
*   **Key Attributes:** `width`, `height`, `orientation` ("vertical" or "horizontal"), `label_text` (optional title), `scrollbar_button_color`, `scrollbar_button_hover_color`.
*   **Snippet:**
    ```python
    scroll_frame = ctk.CTkScrollableFrame(master=right_frame, width=200, height=150, label_text="Step Log")
    scroll_frame.pack(expand=True, fill="both", padx=20, pady=20)

    for i in range(10):
        ctk.CTkLabel(scroll_frame, text=f"Step {i}: x = {i*0.5}").pack(anchor="w")
    ```

---

## 3. Theming and Appearance Modes

CustomTkinter provides native support for Dark/Light mode switching and custom `.json` themes.

### Dynamically Switching Appearance Modes
CustomTkinter can follow the system theme automatically or be forced into "dark" or "light" mode.

```python
# Follow operating system theme (Default)
ctk.set_appearance_mode("System")

# Force specific modes
ctk.set_appearance_mode("Dark")
ctk.set_appearance_mode("Light")
```

### Applying Custom Color Themes (.json)
Instead of hardcoding colors on every widget, you can define a JSON theme file and load it at the start of the application.

```python
# Load a custom JSON theme file
# The JSON file defines colors as tuples: ["light_color", "dark_color"] or hex strings
ctk.set_default_color_theme("path/to/neurosolve_theme.json")

# Or use built-in themes:
# ctk.set_default_color_theme("dark-blue") # Options: "blue", "green", "dark-blue"
```

*Example structure of a custom theme JSON snippet:*
```json
{
  "CTkButton": {
    "fg_color": ["#3a7ebf", "#1f538d"],
    "hover_color": ["#325882", "#14375e"],
    "text_color": ["#DCE4EE", "#DCE4EE"]
  }
}
```

---

## 4. Best Practices and "Gotchas" (vs Standard Tkinter)

1.  **Widget Instantiation:** Always use `ctk.CTk...` widgets instead of standard `tk...` widgets (e.g., `CTkButton` vs `Button`, `CTkLabel` vs `Label`). Mixing them can cause visual glitches and break the dynamic dark/light mode switching.
2.  **Color Tuples:** Many color arguments in CustomTkinter accept a tuple `("light_color", "dark_color")`. The widget automatically uses the correct color based on the current Appearance Mode. If a single string is passed, it remains static across modes.
    *   *Example:* `fg_color=("#DDDDDD", "#222222")`
3.  **Images (`CTkImage`):** Standard `PhotoImage` can appear blurry, especially on HighDPI displays. use `ctk.CTkImage` combined with `PIL.Image` for crisp widget icons that scale correctly and can swap between dark/light modes.
    *   *Snippet:* `my_image = ctk.CTkImage(light_image=Image.open("icon_light.png"), dark_image=Image.open("icon_dark.png"), size=(20, 20))`
4.  **Avoid `.place()` over Borders:** As noted in the project rules, placing widgets using absolute (`.place()`) positioning inside a frame with a `border_width` will paint the child's background over the parent's border. Use `.pack()` or `.grid()` with appropriate `padx/pady` to respect borders.
5.  **Font Handling:** Use `ctk.CTkFont(family="FontName", size=14, weight="bold")`. If a custom font isn't installed system-wide, it will fail silently to the fallback font.
6.  **`bg_color` vs `fg_color`:** In CustomTkinter, `bg_color` controls the color *behind* the widget (visible at rounded corners). `fg_color` (foreground color) is the actual main solid color of the widget itself. To make a widget blend perfectly into a parent frame, `bg_color` is rarely needed; `fg_color` is what you want to change.
