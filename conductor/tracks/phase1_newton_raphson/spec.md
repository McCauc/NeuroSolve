# Track: Phase 1 - Newton-Raphson Solver

---

## 1. Specification

### 1.1 Overview
Implement the Newton-Raphson root-finding algorithm with a streamlined Streamlit UI. This track focuses on core numerical accuracy, safety (no `eval`), and educational transparency.

### 1.2 Functional Requirements
1.  **Input Handling**:
    *   Start Page: Application loads with default example ($x^2 - 2$).
    *   User inputs: Function string $f(x)$, Start point $x_0$, Tolerance $\epsilon$.
    *   Validation: Reject unsafe strings (e.g., `import os`) immediately.
2.  **Solver Logic**:
    *   Algorithm: $x_{n+1} = x_n - f(x_n)/f'(x_n)$.
    *   Derivatives: Computed symbolically using SymPy.
    *   Stopping Criteria: stop when $|f(x)| < \epsilon$ OR $|\Delta x| < \epsilon$ OR $n \ge max\_iter$.
3.  **Output Display**:
    *   **Graph**: Interactive Plotly line chart showing function curve and iteration markers.
    *   **Log**: Table showing iteration history $(n, x_n, f(x_n), f'(x_n), error)$.
    *   **Status**: Clear message on convergence success or failure reason.

### 1.3 Non-Functional Requirements (Safety & Robustness)
1.  **Security**: Strict whitelist for math parsing. No `eval` on raw input.
2.  **Robustness**: Handle `ZeroDivisionError` (flat derivative) gracefully with user-friendly error.
3.  **Performance**: Solver must timeout or hit max iterations (e.g., 100) to prevent infinite loops.

### 1.4 Acceptance Criteria
- [ ] **AC1**: User can input `sin(x) - 0.5` and find root $\approx 0.523$.
- [ ] **AC2**: Inputting `import os` raises a "Invalid Input" error, not a system crash.
- [ ] **AC3**: Solver handles $f(x)=x^2+1$ (no root) by reaching max iterations and reporting "Failed to converge".
- [ ] **AC4**: Steps table matches manual calculation for $x^2-4$ at $x_0=1$.

### 1.5 Proposed Directory Structure
*   `src/solvers/newton_raphson.py`: Core solver logic and `NewtonRaphsonSolver` class.
*   `src/utils/parsing.py`: Secure math expression parsing utility.
*   `src/ui/app.py`: Streamlit application entry point.
*   `tests/test_newton.py`: Unit tests for solver logic.
*   `tests/test_parsing.py`: Unit tests for parsing safety.
