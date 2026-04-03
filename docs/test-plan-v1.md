# NeuroSolve Test Plan v1

- Version: `v0.1.0`
- Milestone: `Week 7 Midterm Build`
- Date: `2026-04-01`
- Team: Rejay Buta, John Cedrick Delgado, Carlo Jose Anyayahan

## Purpose

This plan documents concrete verification for the current Week 7 runnable package. It includes both automated and manual tests, clearly labeled.

## Environment

- OS: Windows (PowerShell)
- Python: 3.10+ (known working: 3.11.9)
- Install command:

```powershell
pip install -r requirements.txt
```

## Test Cases

### T1 - Secant Convergence (Automated)

- Type: Automated (`pytest`)
- Source: `tests/test_secant.py::test_secant_basic_convergence`
- Preconditions:
  - Dependencies installed
- Steps:
  1. Run `pytest tests/test_secant.py::test_secant_basic_convergence`
- Expected Outcome:
  - Test passes.
  - Solver converges for `x**2 - 4` with root near `2.0`.
  - Returned result includes expected success state and history entries.

### T2 - Bisection Invalid Bracket Handling (Automated)

- Type: Automated (`pytest`)
- Source: `tests/test_bisection.py::test_bisection_invalid_interval`
- Preconditions:
  - Dependencies installed
- Steps:
  1. Run `pytest tests/test_bisection.py::test_bisection_invalid_interval`
- Expected Outcome:
  - Test passes.
  - Solver returns `converged=False`.
  - Clear invalid interval error is present.

### T3 - Method Dispatch Selection (Automated)

- Type: Automated (`pytest`)
- Source: `tests/test_dispatch.py`
- Preconditions:
  - Dependencies installed
- Steps:
  1. Run `pytest tests/test_dispatch.py`
- Expected Outcome:
  - Test passes.
  - `"Secant"` maps to secant solver.
  - `"Bisection"` maps to bisection solver.
  - Unknown method raises `ValueError`.

### T4 - Input Validation Rejects Unsupported Expressions (Automated)

- Type: Automated (`pytest`)
- Source: `tests/test_validation.py`
- Preconditions:
  - Dependencies installed
- Steps:
  1. Run `pytest tests/test_validation.py`
- Expected Outcome:
  - Test passes.
  - Invalid characters are rejected.
  - Unknown variables (not `x`) are rejected.
  - Malformed math syntax is rejected.

### T5 - About/Help Content Visibility (Manual)

- Type: Manual
- Preconditions:
  - App launches successfully
- Steps:
  1. Start the app with `.\run.bat` or `python -m src.ui.app`.
  2. Click the Help button in the top-right header.
  3. Inspect the About/Help surface.
- Expected Outcome:
  - A non-crashing About/Help UI appears.
  - It displays:
    - Project name: `NeuroSolve`
    - Version: `v0.1.0`
    - Milestone label: `Week 7 Midterm Build`
    - Team members:
      - Rejay Buta
      - John Cedrick Delgado
      - Carlo Jose Anyayahan

### T6 - Screenshot Readiness with Visible Trail (Manual)

- Type: Manual
- Preconditions:
  - App launches successfully
- Steps:
  1. Start the app.
  2. Use a deterministic solve example (for example, function `x**2 - 4` with valid inputs).
  3. Run Calculate and wait for the solution trail/log to populate.
  4. Capture at least one screenshot where the trail is clearly visible.
  5. Save the capture to `docs/screenshots/week7/`.
- Expected Outcome:
  - At least one screenshot exists in `docs/screenshots/week7/`.
  - Screenshot shows current UI and populated solution trail.
  - Screenshot is not stored only in `archive/images/`.

## Full Suite Regression Command

```powershell
pytest tests
```

Expected result: all tests pass with no regressions.

## Week 8 Additive Robustness Reference

- For Week 8 robustness inventory and edge-case traceability, see:
  - `docs/week8-robustness-report.md`
- This Week 7 test plan remains historically accurate for the midterm package and is not rewritten as a future-state Week 8 artifact.

## Pass Criteria

- Automated tests in this plan pass.
- Manual checks for About/Help and screenshot readiness pass.
- Documentation and UI labels remain consistent with `v0.1.0` and `Week 7 Midterm Build`.
