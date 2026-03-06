# NeuroSolve: Educational Numerical Analysis Application - Detailed Project Documentation

## Project Overview

**NeuroSolve** is an educational desktop application designed to teach and demonstrate numerical methods for solving non-linear equations. The application focuses specifically on the **Secant Method**, a root-finding algorithm that iteratively approximates solutions to equations where analytical solutions are impossible or impractical.

The application bridges the gap between theoretical mathematics and practical computation by providing real-time visual feedback, step-by-step algorithmic trails, and interactive graphing in a user-friendly desktop interface.

### Project Purpose
- **Educational Focus**: Help students understand how numerical methods work through visualization and explanation
- **Interactive Learning**: Provide immediate graphical feedback showing function curves and convergence points
- **Error Handling**: Educate users about algorithm failure states and limitations (divergence, division by zero, etc.)
- **Real-world Application**: Demonstrate solutions to complex equations from multiple domains (polynomials, transcendental functions, exponential equations)

---

## Technical Architecture

### Technology Stack

#### Backend/Mathematical Computing
- **Python 3.10+**: Primary programming language
- **NumPy 1.24.0+**: Numerical computing and array operations
- **SymPy 1.12+**: Symbolic mathematics for safe expression parsing and evaluation
- **Matplotlib 3.8.0+**: Scientific plotting and visualization

#### Frontend/User Interface
- **CustomTkinter 5.2.0+**: Modern, native-looking desktop UI framework (wrapper around Tkinter with enhanced styling)
- **Pillow 10.0.0+**: Image processing for UI assets

#### Testing & Quality Assurance
- **Pytest 7.0.0+**: Unit testing framework

### Project Structure

```
COSC-110_(PROJECT)/
├── README.md                          # Quick start guide
├── requirements.txt                   # Python dependencies
├── run.bat                           # Windows batch script to launch application
├── detailed.md                       # This comprehensive documentation
│
├── src/                              # Source code directory
│   ├── solvers/                      # Mathematical solver implementations
│   │   └── secant_method.py         # Core Secant Method algorithm
│   │
│   ├── ui/                           # User interface components
│   │   ├── app.py                   # Main application controller
│   │   └── components/              # Modular UI components
│   │       ├── header.py            # Application header/title bar
│   │       ├── sidebar.py           # Parameter input panel
│   │       ├── main_content.py      # Graph and logging display
│   │       └── __init__.py
│   │
│   └── utils/                        # Utility functions
│       ├── parsing.py               # Safe mathematical expression parsing
│       └── dev_tools.py             # Developer utilities
│
├── tests/                            # Unit tests
│   ├── test_secant.py               # Tests for Secant Method
│   └── test_validation.py           # Tests for input validation
│
├── docs/                             # Documentation
│   ├── CODEBASE_MAP.md              # Project structure reference
│   └── customtkinter_guide.md       # UI framework documentation
│
├── assets/                           # Images and media files
└── data/                            # Data storage directory
```

---

## Core Components & Functionality

### 1. Mathematical Solver: Secant Method (`src/solvers/secant_method.py`)

#### Algorithm Description
The **Secant Method** is a numerical root-finding algorithm that uses two initial approximations to iteratively find where a function crosses zero.

**Mathematical Formula:**
$$x_{n+1} = x_n - f(x_n) \cdot \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$$

#### Key Characteristics
- **Requires 2 initial guesses** (x₀ and x₁) instead of Newton's method's 1
- **Derivative-free**: Does not require computing f'(x), making it more practical
- **Superlinear convergence**: Faster than bisection but slower than Newton's method
- **No derivative requirement**: Useful when f'(x) is difficult or impossible to compute

#### Implementation Details
- Accepts a callable function, two initial guesses, tolerance threshold, and maximum iterations
- Returns a dictionary containing:
  - **root**: The approximate solution (float or None)
  - **converged**: Boolean indicating success
  - **iterations**: Number of steps performed
  - **history**: List of detailed step-by-step data for UI logging
  - **error_msg**: Description of any error encountered

#### Failure Modes & Error Handling
The implementation detects and handles:
- **Division by zero**: When the secant line is horizontal (f(x_n) - f(x_{n-1}) = 0)
- **Maximum iterations exceeded**: When algorithm doesn't converge in time
- **Function evaluation errors**: Invalid domain values or undefined operations
- **Divergence**: When initial guesses lead away from solutions

### 2. User Interface System (`src/ui/`)

#### Application Controller (`app.py`)
The main orchestrator that:
- Manages component lifecycle and interaction
- Coordinates data flow between UI and solver
- Handles asynchronous graph rendering to prevent UI freezing
- Implements error handling and user feedback

**Main Workflow:**
1. Retrieves user inputs (function string, initial values, parameters)
2. Validates all required fields
3. Parses mathematical expression into executable function
4. Invokes Secant Method solver
5. Renders iteration history as step-by-step log
6. Displays results (root value and convergence status)
7. Renders final results table showing all iterations
8. Generates and displays interactive matplotlib graph

#### Component: Header Frame (`components/header.py`)
- Application title and branding: "NeuroSolve - Brutalist Control Deck"
- Status logo/icon area
- Developer tools integration (secret shortcuts for testing)

#### Component: Sidebar Frame (`components/sidebar.py`)
**Input Control Panel** with fields for:
- **Function f(x)**: Mathematical expression string (e.g., "x**3 + 2*x**2 + x - 1")
- **Initial Guess 1 (x₀)**: First starting point for algorithm
- **Initial Guess 2 (x₁)**: Second starting point for algorithm
- **Tolerance (ε)**: Convergence criterion (typically 1e-6 for 6 decimal places)
- **Max Iterations**: Safety limit to prevent infinite loops (default: 100)

Features:
- Real-time input validation
- Developer modes (random filling for testing)
- Clear/Reset functionality
- Calculate button to execute solver

#### Component: Main Content Frame (`components/main_content.py`)
**Display Area** split into two sections:

**Left Panel (60% width):**
- **Result Status Box**: Large yellow badge showing:
  - Current status ("AWAITING INPUT", "CALCULATING...", or computed root value)
  - Iteration count and convergence message
- **Interactive Graph**: Matplotlib visualization showing:
  - Function curve in cyan
  - Initial guess points in yellow
  - Iteration approximation points in black
  - Final solution point (cyan if converged, magenta if failed)
  - Grid overlay with black borders

**Right Panel (40% width):**
- **Algorithmic Log**: Scrollable trail panel displaying:
  - Validation messages
  - Step-by-step iteration breakdown (each step labeled STEP 01, STEP 02, etc.)
  - Plain English explanations of each calculation
  - Mathematical data (x values, f(x) values, error metrics)
  - Final verification and summary messages
- **Download/Print Buttons**: Export functionality
- **Iteration Table**: Detailed summary table with all iteration data

### 3. Utility Functions (`src/utils/`)

#### Expression Parser (`parsing.py`)
Safely converts mathematical strings into executable Python functions.

**Security Features:**
- Regex validation: Only allows alphanumeric characters, operators (+, -, *, /), parentheses
- SymPy-based parsing: Prevents code injection
- Variable restriction: Only the variable 'x' is permitted
- Type safety: Converts NumPy scalars to standard Python floats

**Supported Function Syntax:**
- Polynomials: `x**2 - 4*x + 3`
- Trigonometric: `sin(x) - 0.5`, `cos(x) - x`
- Exponential: `exp(x) - 3`, `2**x - 10`
- Logarithmic: `log(x) - 2`
- Complex combinations: `x**3 + 2*x**2 + x - 1`

#### Developer Tools (`dev_tools.py`)
Utilities for testing and debugging:
- Random test case generation
- Input validation helpers
- Logging utilities

---

## User Interface Design

### Design Philosophy: "Brutalist Control Deck"
The UI follows a neo-brutalist design aesthetic emphasizing:
- **Bold, stark elements**: Thick black borders, primary color blocks
- **Minimal decoration**: No gradients or rounded corners
- **High contrast**: Clear visual hierarchy using cyan (#00FFFF), magenta (#FF00FF), yellow (#FFFF00)
- **Functional beauty**: Every visual element serves a purpose

### Color Scheme
- **Background**: Off-white (#F8F5F8) - brutalist canvas
- **Success/Info**: Cyan (#00FFFF) - indicates convergence and active elements
- **Warnings/Errors**: Magenta (#FF00FF) - indicates failure or divergence
- **Emphasis**: Yellow (#FFFF00) - highlights headers and important data
- **Structure**: Black (#000000) - borders, grid lines, text

### Font Choices
- **Headers**: Space Grotesk (sans-serif, bold) - strong, geometric
- **Data/Code**: Space Mono (monospace) - precise, technical
- **Default fallback**: DejaVu Sans (when custom fonts unavailable)

---

## Data Flow & User Workflow

### Complete Usage Scenario

**Step 1: Input Configuration**
```
User enters equation:    x**3 + 2*x**2 + x - 1
User enters x₀:         0
User enters x₁:         1
User enters tolerance:  1e-4
User enters max_iter:   100
```

**Step 2: Validation**
- Application validates all fields are non-empty
- Parser checks equation syntax using regex and SymPy
- All parameters converted to correct numeric types

**Step 3: Execution**
```
Function: f(x) = x³ + 2x² + x - 1

Iteration 0: x₀ = 0,      f(0) = -1
Iteration 1: x₁ = 1,      f(1) = 3
Iteration 2: x₂ = 0.25,   f(0.25) = -0.6094
Iteration 3: x₃ = 0.3766, f(0.3766) = -0.2863
Iteration 4: x₄ = 0.4888, f(0.4888) = 0.0835
Iteration 5: x₅ = 0.4655, f(0.4655) = -0.0002

Convergence achieved after 5 iterations
Root ≈ 0.4655 (accurate to 4 decimal places)
```

**Step 4: Display Results**
- Status box shows root value (0.4655) in cyan box
- Log panel displays step-by-step breakdown
- Iteration table shows all calculation steps
- Graph plots function curve and points

**Step 5: Interpretation**
- Student can see how each iteration refined the approximation
- Graph visualizes convergence to x-intercept
- Error values show minimization over iterations
- Educational insights about algorithm behavior

---

## Testing & Quality Assurance

### Unit Tests (`tests/`)

#### `test_secant.py`
Tests for the core Secant Method implementation:
- Convergence on known roots (e.g., x² - 4 = 0 has root at x = 2)
- Divergence detection
- Division by zero handling
- Maximum iteration limits
- Tolerance thresholds

#### `test_validation.py`
Tests for input validation and error handling:
- Invalid expression syntax
- Missing required fields
- Out-of-range parameters
- Edge cases and boundary conditions

### Running Tests
```bash
pytest tests/                    # Run all tests
pytest tests/test_secant.py -v   # Run with verbose output
pytest tests/ --cov=src          # Generate coverage report
```

---

## Installation & Setup

### Prerequisites
- Windows, macOS, or Linux operating system
- Python 3.10 or higher
- pip (Python package manager)

### Installation Steps

**1. Create Virtual Environment:**
```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux
```

**2. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**Dependencies Summary:**
| Package | Version | Purpose |
|---------|---------|---------|
| NumPy | ≥1.24.0 | Numerical computing |
| SymPy | ≥1.12 | Symbolic mathematics |
| CustomTkinter | ≥5.2.0 | Modern UI framework |
| Matplotlib | ≥3.8.0 | Scientific plotting |
| Pytest | ≥7.0.0 | Unit testing |
| Pillow | ≥10.0.0 | Image handling |

**3. Run Application:**
```bash
.\run.bat                       # Windows (batch script)
python -m src.ui.app          # Cross-platform Python
```

---

## How It Works: Algorithm Walkthrough

### Example Problem: Find root of f(x) = x³ + 2x² + x - 1

### Theory
The Secant Method uses two points to approximate the tangent line (secant) and find where it crosses the x-axis:

1. Start with two guesses: x₀ and x₁
2. Evaluate function at both points: f(x₀) and f(x₁)
3. Find equation of secant line through (x₀, f(x₀)) and (x₁, f(x₁))
4. Calculate x-intercept of this line → x₂
5. Move forward: x₀ := x₁, x₁ := x₂
6. Repeat until convergence

### Mathematical Computation
```
Given: x₀ = 0, x₁ = 1

Step 2: f(x₀) = -1, f(x₁) = 3
Step 3: Secant line slope = [3 - (-1)] / [1 - 0] = 4
Step 4: x₂ = x₁ - f(x₁) × (x₁ - x₀) / [f(x₁) - f(x₀)]
       x₂ = 1 - 3 × (1 - 0) / (3 - (-1))
       x₂ = 1 - 3/4 = 0.25

Repeat process with x₀ = 1, x₁ = 0.25:
       f(0.25) = -0.6094
       x₃ = 0.25 - (-0.6094) × (0.25 - 1) / (-0.6094 - 3)
       x₃ ≈ 0.3766
```

### Convergence Visualization
The algorithm creates a sequence that spirals toward the root:
```
Iteration Sequence: [0, 1, 0.25, 0.3766, 0.4888, 0.4655, ...]
                          ↑ decreasing error
Error (|xₙ - xₙ₋₁|):  [1.0, 0.75, 0.1266, 0.1122, 0.0233, ...]
                          ↑ exponential decrease
```

---

## Advantages & Limitations

### Advantages
✓ **No derivative required**: Practical for complex functions  
✓ **Superlinear convergence**: Faster than bisection, nearly as fast as Newton  
✓ **Robust initial guesses**: Only needs two rough starting points  
✓ **Wide applicability**: Works for any continuous function  

### Limitations
✗ **Requires two initial guesses**: More setup than Newton's method  
✗ **Can diverge**: If initial guesses are too far from root  
✗ **Division by zero risk**: When secant line is horizontal  
✗ **Slower than Newton's method**: For smooth, well-behaved functions  
✗ **Can miss roots**: May converge to local maximum/minimum instead  

---

## Real-World Applications

The Secant Method solves equations that appear in:

### Engineering & Physics
- **Circuit Analysis**: Finding resonant frequencies in RLC circuits
- **Mechanics**: Calculating critical load buckling in columns
- **Thermodynamics**: Solving equations of state for gases

### Finance & Economics
- **Option Pricing**: Finding implied volatility in Black-Scholes model
- **NPV Calculations**: Finding internal rate of return (IRR)
- **Break-even Analysis**: Finding equilibrium prices

### Natural Sciences
- **Chemistry**: pH calculations from equilibrium expressions
- **Biology**: Solving logistic growth equations
- **Astronomy**: Orbital mechanics and Kepler's equation

### Computer Science
- **Graphics**: Ray-sphere intersection calculations
- **Optimization**: Finding extrema of cost functions
- **Signal Processing**: Finding zero-crossings in time series

---

## Comparison with Other Root-Finding Methods

| Method | Derivative Required | Convergence Speed | Robustness | Use When |
|--------|-------------------|-------------------|-----------|----------|
| **Bisection** | No | Slow (Linear) | Very Robust | You need guaranteed convergence |
| **Newton-Raphson** | Yes | Very Fast (Quadratic) | Can Diverge | f'(x) is easy to compute |
| **Secant** | No | Fast (Superlinear) | Good | You need speed without derivatives |
| **Regula Falsi** | No | Slow (Linear) | Very Robust | You want bisection's reliability with better speed |
| **Brent's Method** | No | Fast (Superlinear) | Very Robust | You want both speed and reliability |

---

## Educational Value & Learning Outcomes

### For Students Using This Application
Students can learn:
1. **Understanding iteration**: See how algorithms refine approximations step-by-step
2. **Convergence behavior**: Observe how error decreases exponentially
3. **Failure analysis**: Understand why algorithms fail with bad initial guesses
4. **Trade-offs**: Compare tolerance vs iteration count
5. **Visualization**: Bridge gap between abstract math and concrete graphs
6. **Problem-solving**: Apply method to diverse real-world equations

### Teaching Applications
- **Classroom demonstrations**: Live visualization of algorithm behavior
- **Student assignments**: Have students predict convergence before running
- **Error analysis**: Students investigate which equations are "hard" to solve
- **Algorithm comparison**: Run same problem with different initial guesses
- **Debugging skills**: Use failure messages to understand mathematical concepts

---

## Code Quality & Best Practices

### Architectural Principles
1. **Separation of Concerns**: 
   - Math logic isolated in `/solvers/`
   - UI code isolated in `/ui/`
   - Utilities in `/utils/`

2. **Type Safety**: 
   - All functions annotated with type hints
   - Input validation at boundaries
   - Explicit float conversions

3. **Error Handling**: 
   - Comprehensive try-catch blocks
   - Descriptive error messages
   - Graceful degradation

4. **Performance Optimization**:
   - Asynchronous graph rendering (prevents UI freezing)
   - Incremental UI updates (avoid redrawing everything)
   - Efficient numpy operations

5. **Security**:
   - Regex validation of user input
   - SymPy sandboxing for expression parsing
   - No dynamic code execution (eval/exec)

### Code Organization
- **DRY Principle**: Utility functions prevent code duplication
- **Single Responsibility**: Each class/function has one clear purpose
- **Readability**: Descriptive variable names, clear comments
- **Maintainability**: Well-documented functions and logical structure

---

## Future Enhancement Possibilities

### Algorithm Expansions
- [ ] Newton-Raphson Method
- [ ] Bisection Method
- [ ] Regula Falsi Method
- [ ] Brent's Method
- [ ] Multiple root finding

### UI Improvements
- [ ] Function gallery (pre-loaded famous equations)
- [ ] Animation of iteration process
- [ ] Comparison mode (run two methods side-by-side)
- [ ] 3D plotting for multivariable functions
- [ ] Export results to PDF/LaTeX

### Data Features
- [ ] Save and load session history
- [ ] Equation templates and examples
- [ ] Performance metrics and statistics
- [ ] Difficulty ratings for equations

### Interactive Learning
- [ ] Guided tutorials and walkthroughs
- [ ] Problem difficulty progression
- [ ] Hints and step-by-step guidance
- [ ] Quiz mode to test understanding

---

## Troubleshooting

### Common Issues

**Issue 1: "Font family 'Space Grotesk' not found"**
- *Cause*: Brutalist aesthetic fonts not installed on system
- *Solution*: Application automatically falls back to default fonts
- *Impact*: Minor - no functionality affected, just visual appearance

**Issue 2: Application freezes during graph rendering**
- *Cause*: Heavy matplotlib computation on main thread
- *Solution*: Application uses async rendering with `self.after()`
- *Status*: Fixed in current architecture

**Issue 3: "Division by zero" error**
- *Cause*: Initial guesses created horizontal secant line
- *Solution*: Try different initial values farther apart
- *Example*: Instead of x₀=0, x₁=0.1, try x₀=0, x₁=1

**Issue 4: Algorithm doesn't converge**
- *Cause*: Function oscillates or initial guesses far from root
- *Solution*: Increase max iterations or try different starting points
- *Tip*: Graph the function first to estimate root location

**Issue 5: Unexpected parsing error**
- *Cause*: Unsupported function notation or invalid syntax
- *Solution*: Use standard Python/SymPy notation
- *Valid examples*: `sin(x)`, `exp(x)`, `x**2` ← use `**` for powers

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 7+, macOS 10.13+, or Linux (Ubuntu 18.04+)
- **RAM**: 512 MB
- **Storage**: 200 MB (for Python + dependencies)
- **Python**: 3.10+ (64-bit recommended)

### Recommended Specifications
- **OS**: Windows 10+, macOS 11+, or modern Linux
- **RAM**: 2+ GB
- **Storage**: 1 GB
- **Python**: 3.11 or 3.12 (most recent stable)
- **Monitor**: 1920×1080+ for comfortable viewing

---

## File Descriptions

### Configuration Files
- **requirements.txt**: Exact versions of all Python dependencies
- **run.bat**: Windows batch script that activates venv and runs app
- **detailed.md**: This comprehensive documentation file

### Source Files

#### `src/solvers/secant_method.py` (130 lines)
Core mathematical algorithm. Pure Python, no external UI dependencies. Returns structured result dictionary for UI consumption.

#### `src/ui/app.py` (180 lines)
Main application controller. Orchestrates component lifecycle, validates inputs, calls solver, renders results. Uses asynchronous operations for responsive UI.

#### `src/ui/components/header.py` (60 lines)
Header component with title, logo, and developer tools integration.

#### `src/ui/components/sidebar.py` (150 lines)
Input control panel with 5 parameter fields and calculation button. Implements real-time validation and helper utilities.

#### `src/ui/components/main_content.py` (600 lines)
Display panel with graph, status box, and cylindrical logging. Includes iteration table rendering and mathematical visualization.

#### `src/utils/parsing.py` (50 lines)
Safe mathematical expression parser using regex validation and SymPy. Converts strings to callable functions.

#### `src/utils/dev_tools.py` (30 lines)
Developer utilities for testing (random data generation, input filling).

### Test Files
- **tests/test_secant.py**: Unit tests for core algorithm
- **tests/test_validation.py**: Tests for input sanitization

### Documentation
- **docs/CODEBASE_MAP.md**: Project structure reference
- **docs/customtkinter_guide.md**: UI framework reference

---

## Conclusion

NeuroSolve is a well-architected educational application that makes numerical methods accessible and understandable. By combining robust mathematical computation with modern, intuitive interface design, it serves as both a practical tool and a learning platform.

The project demonstrates professional software engineering practices including separation of concerns, comprehensive error handling, type safety, and security considerations—making it suitable as an educational example and portfolio piece for computer science education.

---

**Last Updated**: March 6, 2026  
**Project Status**: Fully Functional - Educational Release  
**Version**: 1.0  
**License**: Educational Use (Contact for specifics)
