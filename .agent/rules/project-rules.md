---
trigger: always_on
---

# AGENT RULES AND BEST PRACTICES

This document defines the rules and best practices for the **NeuroSolve** project. These guidelines must be followed by the AI Agent and human developers to ensure code quality, maintainability, and consistency.

## 1. General Philosophy
*   **Be a Tutor, Not Just a Calculator**: The primary goal is *educational transparency*. Every computation must be explainable.
*   **Code for Readability**: Code should be self-documenting. Use clear variable names (`x_current` instead of `x`).
*   **Documentation First**: Before implementing complex logic, document the expected behavior and inputs/outputs.
*   **Robustness**: All numerical methods must handle edge cases (e.g., division by zero, non-convergence) gracefully.

## 2. Project Structure & Standards
*   **Directory Layout**:
    *   `src/solvers/`: Contains the core numerical algorithms.
    *   `src/ui/`: Contains CustomTkinter GUI code.
    *   `src/utils/`: Shared utilities (parsing, formatting).
    *   `tests/`: Unit and integration tests.
*   **File Naming**: Use `snake_case` for Python files (e.g., `newton_raphson.py`).
*   **Type Hinting**: All functions **MUST** use Python type hints (Standard `typing` library).

## 3. Technology Stack & Rules

### A. NumPy (Numerical Computation)
*   **Vectorization**: Prefer vectorized operations over loops for performance.
    *   *Bad*: `[x**2 for x in data]`
    *   *Good*: `data**2` (where `data` is a NumPy array)
*   **Data Types**: Be explicit about data types when necessary (e.g., `dtype=np.float64` for high precision).
*   **Avoid Global Random State**: Use `rng = np.random.default_rng()` instead of `np.random.seed()`.

### B. SymPy (Symbolic Mathematics)
*   **Avoid String Manipulation for Logic**: Do not use regex on mathematical strings. Parse them into SymPy expressions immediately.
    *   *Bad*: `if "x^2" in expr_str:`
    *   *Good*: `if expr.has(x**2):`
*   **Explicit Symbols**: Define symbols explicitly or pass them as arguments to functions. Avoid implicit global symbols.
    *   *Why*: Prevents scope confusion and makes functions pure/testable.
*   **Use `sympify()` Carefully**: validate user input before passing it to `sympify()` to prevent arbitrary code execution (though less critical in a local app, still best practice).

### C. CustomTkinter (User Interface)
*   **Separation of Concerns**: Keep UI logic separate from solver logic.
    *   *Pattern*: The UI collects input -> calls a Solver function -> receives a Result object -> updates the UI labels/textboxes.
*   **State Management**: Store data in application class attributes (`self.history = []`).
*   **Component Structure**: Break down complex UI screens into modular widget building functions (e.g., `_create_sidebar()`, `_create_input_group()`).
*   **Neo-Brutalist Styling & Rendering Gotchas**:
    *   **Borders**: Use `ctk.CTkFrame` with `border_width` and `border_color` for reliable solid borders, rather than relying on nested absolute positioning.
    *   **Widget Default Sizes**: Be aware that widgets like `CTkEntry` have default widths (e.g., 140px). If placed inside strictly sized containers, they will silently force the parent to stretch and cause clipping of right-hand borders. Explicitly override `width=50` (or similar) when relying on `expand=True`.
    *   **Padding & Height Clipping**: In fixed-height containers (`height=X` with `pack_propagate(False)`), excessive vertical padding (`pady`) on child elements will cause the bottom of the child elements (including their borders) to be clipped silently without triggering errors.
    *   **Child Positioning over Borders (.place vs .pack)**: If a parent frame has a `border_width` defined, placing a child widget (like a `CTkLabel`) inside it using absolute `.place(relx=0.5, rely=0.5)` will cause the child's background to paint completely over the parent's borders. To respect parent borders, you must use `.pack(expand=True, fill="both", padx=border_size, pady=border_size)`.
    *   **The Sub-Pixel Bleed Glitch (Use `tk.Frame`)**: `CustomTkinter`'s internal `Canvas` engine cannot correctly anti-alias floating-point sizes when a layout manager expands a container. Setting `border_width` on dynamic components (like the main log log or dynamically placed buttons) will cause a 1px white/background bleed over the black border. **To fix shadows and borders completely:** 
        *   NEVER use `border_width=3` with `corner_radius=0` on dynamic expanding layouts. 
        *   INSTEAD, construct nested solid standard `tkinter.Frame` instances. A black `tk.Frame` acting as the shadow `place(x=6, y=6)`, a black `tk.Frame` acting as the border `place(x=0, y=0)`, and the content `CTkFrame` packed with `padx=3, pady=3` inside the border layer. Standard `tk.Frame` respects integer pixels perfectly and naturally prevents sub-pixel canvas bleed.
    *   **Fonts**: Custom external fonts (like "Space Grotesk") need to be properly installed on the system, otherwise `CTkFont` will silently fallback to a system default which can throw off your exact pixel measurements.

## 4. Coding Conventions

### Function Signatures
All solver functions must return a structured object (dictionary or class), NOT just the final result.
*   **Standard Return Format**:
    ```python
    {
        "root": float,          # The approximate solution
        "converged": bool,      # Did it find a solution?
        "iterations": int,      # Number of steps
        "history": List[dict],  # Step-by-step log (n, x, f(x), error)
        "error_msg": str|None   # If failed, why?
    }
    ```

### Docstrings
Use Google-style docstrings for all functions.
```python
def solve_bisection(func: Callable, a: float, b: float, tol: float = 1e-6) -> dict:
    """
    Finds the root of a function using the Bisection method.

    Args:
        func: The standard Python function f(x).
        a: Lower bound of the interval.
        b: Upper bound of the interval.
        tol: Tolerance for convergence.

    Returns:
        dict: A dictionary containing the root, convergence status, and iteration history.
    """
    pass
```

## 5. Tooling & Workflow (Added 2026)

### A. Dependencies
*   **Standardization**: All project dependencies must be listed in a `requirements.txt` file in the root directory.
*   **Pinning**: Versions should be pinned (e.g., `numpy==2.1.0`) to ensure reproducibility.

### B. Linting & Formatting
*   **Tool**: Use **Ruff** for both linting and formatting. It replaces `flake8`, `black`, and `isort`.
*   **Style**: Follow standard PEP 8.
*   **Configuration**: Maintain a `pyproject.toml` or `ruff.toml` for consistent settings.

### C. Testing
*   **Framework**: Use **pytest** for all unit and integration tests.
*   **UI Testing**: Decouple logic so that mathematical components can be tested entirely headless with pytest.
*   **Coverage**: Aim for high test coverage on solver logic.

## 6. Additional Rules for Stability & Maintenance

### A. Error Handling
*   **Explicit Exceptions**: Raise specific errors (e.g., `ValueError` for domain errors, `RuntimeError` for convergence failure) rather than generic `Exception`.
*   **User Feedback**: In the UI, catch known errors and display them using a dedicated status label with simpler language, not raw stack traces.

### B. Testing Strategy
*   **Unit Tests**: Every solver **MUST** have a corresponding test file in `tests/` (e.g., `tests/test_newton_raphson.py`).
*   **Regression Tests**: If a bug is found, add a test case that reproduces it before fixing.

### C. Git Commit Messages
*   **Format**: Use Conventional Commits:
    *   `feat: ...` for new features (e.g., `feat: add secant method solver`)
    *   `fix: ...` for bug fixes (e.g., `fix: handle division by zero in newton iteration`)
    *   `docs: ...` for documentation
    *   `refactor: ...` for code cleanup
    *   `test: ...` for adding/modifying tests

### D. UI Responsiveness
*   **Progress Indicators**: For any operation that might take time, update a status label to "Calculating..." and call `self.update_idletasks()` before starting the intensive task.

## 7. AI Interaction Rules (Meta-Rules)
*   **Context Awareness**: Before answering "Why?", read the *entire* relevant log history.
*   **No Hallucination**: If the log shows "Error", do not say "The calculation finished successfully". Reliability > Politeness.
*   **Step-by-Step Thinking**: When asked to implement a new feature:
    1.  Recall these rules.
    2.  Plan the structure.
    3.  Implement the Core Logic (Solver).
    4.  Implement the UI.
    5.  Verify with Tests.

THIS FILE SHOULD BE READ BY THE AGENT AT THE START OF COMPLEX TASKS TO REFRESH MEMORY.