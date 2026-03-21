# NeuroSolve: Educational Numerical Analysis Module

NeuroSolve is an educational desktop application that solves non-linear equations using numerical methods like the Secant Method. By providing a step-by-step algorithmic trail and real-time interactive graphing, it bridges the gap between black-box calculators and mathematical theory, helping students visualize exactly how iterations converge or fail.

## Supported Sample Problems
The application is designed to support the following real-world computational problems:
1. **Finding roots of complex polynomials** (e.g., $f(x) = x^3 - 2x - 5$) where deriving exact algebraic analytical solutions is tedious or impossible.
2. **Solving transcendental equations** involving trigonometric or exponential functions (e.g., $f(x) = \sin(x) - \frac{1}{2}$ or $e^x - 3$) which cannot be solved via standard algebra.
3. **Analyzing algorithmic failure states** (e.g., horizontal tangents causing division-by-zero, or divergent initial guesses) to educate users on the mathematical limitations and boundary conditions of numerical methods.

## Features
*   **Native Desktop UI:** Built from the ground up using `CustomTkinter` for a lightning-fast, premium look without the overhead of web browsers.
*   **Educational Trail Panel:** Translates complex mathematical Python iterations into plain-english step-by-step explanations.
*   **Asynchronous Graphing:** Leverages `matplotlib` for native, threaded graph rendering that doesn't freeze the main User Interface.

## Setup Instructions

1.  **Install Python 3.10+**
2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage
Run the application via the provided batch script:
```bash
.\run
```
*(Alternatively, run `python -m src.ui.app`)*
