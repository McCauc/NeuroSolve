# Product Requirement Document (PRD)

## Project Name: NeuroSolve - Numerical & Symbolic Computation Analyst

### 1. Overview
**NeuroSolve** is a desktop/web application designed to solve fundamental numerical and symbolic computation problems while providing a human-readable, step-by-step explanation of the process. It features an integrated AI Chat Assistant that can analyze the computed results and explain the methodology, acting as a tutor rather than a calculator.

### 2. Goals & Objectives
*   **Accuracy:** Perform computations using standard Python libraries (NumPy, SymPy) to ensure mathematical precision.
*   **Transparency:** Display the "thinking process" of the algorithm (iterations, errors, intermediate steps) in a readable log format.
*   **Educational Value:** Use AI to explain *why* a result occurred (e.g., "The error spiked here because the derivative was near zero"), not just *what* the result is.
*   **Usability:** Provide a clean, modern GUI for inputting equations and parameters.

### 3. Target Audience
*   Students of **COSC 110 (Numerical & Symbolic Computation)** who need to verify their manual calculations and understand algorithmic behavior.
*   Instructors demonstrating numerical methods in class.

### 4. Core Features
#### A. The Solver Engine (Python)
Based on standard COSC 110 curricula, the app will support the following modules:
1.  **Root Finding (Numerical):**
    *   **Bisection Method:** Good for visualizing bracketing.
    *   **Secant Method:** Standard root-finding method using secant lines.
    *   *Output:* Iteration table (n, x_n, f(x_n), error).
2.  **Linear Systems (Numerical):**
    *   **Gaussian Elimination:** Row reduction steps.
    *   *Implementation Note:* Must use a custom "Verbose Solver" class to print intermediate matrix states, as standard libraries (SciPy) skip steps.
    *   *Output:* Matrix state at each row operation.
3.  **Numerical Integration:**
    *   **Trapezoidal / Simpson's Rule:** Approximating area under curves.
    *   *Output:* Area sum calculation steps.

#### B. The User Interface (GUI)
*   **Input Panel:** Text fields for functions (e.g., `f(x) = x^2 - 4`), start points, and tolerances.
*   **Visualization:** Interactive plots (Matplotlib) showing the function curve and the algorithm's "path" (e.g., secant lines for Secant method).
*   **Step-by-Step Log:** A scrollable text area showing the exact algorithmic operations.
*   **Export:** Button to save the "Step-by-Step Log" and Final Result to a `.txt` or `.csv` file.

#### C. The AI Analyst
*   **Role:** The AI does **NOT** calculate the answer. It receives the *Log* from the Solver Engine.
*   **Capabilities:**
    *   "Explain this step": User highlights a log line; AI explains the math.
    *   "Analyze convergence": AI reads the error log and explains if it converged fast or slow.
    *   "What if": User asks "What if I changed the initial guess?", AI predicts the behavior (qualitatively).

### 5. Technical Architecture
*   **Language:** Python 3.10+
*   **UI Framework:** **CustomTkinter** (Desktop Native).
*   **Computation Libraries:**
    *   `NumPy`: Vectors, matrices, arrays.
    *   `Pandas`: Handling iteration tables and data export.
*   **AI Service:** OpenAI API / Google Gemini API (via API Key).

### 6. Success Metrics
*   **Correctness:** The Python solver matches standard WolframAlpha results.
*   **Clarity:** A non-technical user can understand the "Step-by-Step Log".
    *   **Performance:** UI remains responsive during calculations.
    *   **Safety:** Solvers must implement "Max Iterations" (e.g., 100) to prevent infinite loops on divergent functions.

### 7. Roadmap
1.  **Phase 1 (Prototype):** Implement Secant Method Solver with CLI logs.
2.  **Phase 2 (UI):** Wrap Phase 1 in the chosen GUI (CustomTkinter).
3.  **Phase 3 (Logging):** Format logs into a "Human Readable" exportable text file.
4.  **Phase 4 (AI):** Connect the AI Chat window to read the logs.
5.  **Phase 5 (Polish):** Add plots and additional solvers (Linear Algebra/Integration).
