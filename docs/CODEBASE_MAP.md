# NeuroSolve Codebase Map

## Project Root
- `GEMINI.md`: **The Law**. Primary context and rules.
- `_bmad-output/planning-artifacts/prd.md`: Active Product Requirements Document for planning.
- `README.md`: General overview.

## Documentation (`docs/`)
- `AGENT_RULES.md`: Coding standards and best practices.
- `CODEBASE_MAP.md`: This file (Project Index).

## Agent Brain (`.agent/`)
- `skills/`: Specialized workflows.
    - `planning/SKILL.md`: Protocol for Spec & Plan.
    - `implementation/SKILL.md`: Protocol for TDD & Code.
    - `code-review/SKILL.md`: Protocol for Auditing.
    - `codebase-investigator/SKILL.md`: Protocol for Debugging.

## Source Code (`src/`)

### Solvers (`src/solvers/`)
*Mathematical logic only. No UI code allowed here.*
- `secant_method.py`: Core logic for Secant Method root finding.

### User Interface (`src/ui/`)
*CustomTkinter code only. No complex mathematical logic allowed here.*
- `app.py`: Main controller orchestrating the CustomTkinter components.
- `components/`: Modular UI widgets.
    - `sidebar.py`: Handles parameter collection and user input.
    - `main_content.py`: Handles graphic display and algorithm logging.

### Utilities (`src/utils/`)
*Shared helpers.*
- `parsing.py`: Secure mathematical expression parsing.
- `dev_tools.py`: Developer-only utilities (e.g., random test case generator).

## Tests (`tests/`)
*Mirror of `src/` structure.*
- `test_secant.py`: Unit tests for the Secant Method solver.
- `test_parsing.py`: Unit tests for secure expression parsing.
