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

## Week 9 Additive Verification Reference

- Story `1.12` adds structured solver verification payloads and every-run verification rendering for successful and handled warning outcomes.
- Use this command to run all Week 9 automated checks:

```powershell
pytest tests/test_verification_payload.py tests/test_secant.py tests/test_bisection.py tests/test_warning_classification.py
```

### V1 - Secant Success Payload Contract (Automated)

- Type: Automated (`pytest`)
- Source: `tests/test_verification_payload.py::test_secant_success_includes_structured_verification_payload`
- Coverage:
  - verification payload exists
  - schema marker `verification.v1`
  - success status + export flag
  - concrete checks (`Residual |f(x*)|`, `Step Size |Δx|`)

### V2 - Bisection Non-Converged Verification Evidence (Automated)

- Type: Automated (`pytest`)
- Source: `tests/test_verification_payload.py::test_bisection_non_converged_still_reports_verification_evidence`
- Coverage:
  - handled warning/non-converged still returns verification
  - checks include residual and bracket-width evidence

### V3 - No-Estimate Fallback: Invalid Interval (Automated)

- Type: Automated (`pytest`)
- Source: `tests/test_verification_payload.py::test_invalid_interval_has_no_trustworthy_estimate_verification_summary`
- Coverage:
  - root-less outcome returns verification warning state
  - summary explicitly states no trustworthy estimate exists

### V4 - No-Estimate Fallback: Endpoint Evaluation Failure (Automated)

- Type: Automated (`pytest`)
- Source: `tests/test_verification_payload.py::test_initial_evaluation_failure_has_no_estimate_verification_summary`
- Coverage:
  - handled warning from secant initialization failure returns no-estimate verification summary

### V5 - Shared Contract Compatibility (Automated)

- Type: Automated (`pytest`)
- Source:
  - `tests/test_secant.py::test_secant_failure_contract_keys`
  - `tests/test_bisection.py::test_bisection_invalid_interval_failure_contract_keys`
- Coverage:
  - shared solver/history keys remain intact after additive verification payload changes

### V6 - Text-First Verification Messaging + Export Traceability (Automated)

- Type: Automated (`pytest`)
- Source: `tests/test_verification_payload.py::test_format_verification_block_includes_textual_status_and_checks`
- Coverage:
  - textual status marker (`Status: WARNING`) not color-only
  - structured checks render from payload content
  - export/reporting traceability via `can_export` -> `Export Ready: Yes`

### V7 - Trail Visibility Smoke Check: Successful Solve (Manual)

- Type: Manual
- Steps:
  1. Launch app: `.\run.bat` or `python -m src.ui.app`
  2. Solve `x**2 - 4` with method `Secant`, valid parameters
  3. Confirm trail includes a dedicated `VERIFICATION` block after solve
- Expected:
  - verification block is visible
  - status/summary/check lines are textual and readable

### V8 - Trail Visibility Smoke Check: Handled Warning (Manual)

- Type: Manual
- Steps:
  1. Launch app
  2. Use Bisection with invalid interval (example: `x**2 + 1`, `a=-1`, `b=1`)
  3. Confirm warning result still includes a dedicated `VERIFICATION` block
- Expected:
  - warning path shows verification content
  - summary states uncertainty / no trustworthy estimate when applicable

## Week 10 Additive Export Reference

- Story `1.4` adds local solution-trail report export for TXT, HTML, and PDF.
- Use this command to run the export-specific automated checks:

```powershell
pytest tests/test_report_export.py
```

### E1 - Report Model Metadata and Section Order (Automated)

- Type: Automated (`pytest`)
- Source: `tests/test_report_export.py::test_report_model_has_header_metadata_and_required_section_order`
- Coverage:
  - header includes project name, version, milestone, timestamp, method, inputs, root, convergence state, iterations, and outcome summary
  - report sections render in the order `GIVEN`, `METHOD`, `STEPS`, `FINAL`, `VERIFICATION`, `SUMMARY`
  - verification text reuses the shared verification formatter output

### E2 - Method-Specific Input Labels (Automated)

- Type: Automated (`pytest`)
- Source: `tests/test_report_export.py::test_report_model_uses_method_specific_bisection_labels`
- Coverage:
  - Bisection reports `a` and `b`
  - Secant-oriented labels are not guessed into Bisection reports

### E3 - TXT, HTML, and PDF Writers (Automated)

- Type: Automated (`pytest`)
- Source: `tests/test_report_export.py::test_write_report_outputs_txt_html_and_pdf`
- Coverage:
  - TXT preserves readable report sections
  - HTML emits semantic headings and preformatted section content
  - PDF writes a local `%PDF` file through `fpdf2`

### E4 - Export Error and Snapshot Guardrails (Automated)

- Type: Automated (`pytest`)
- Source:
  - `tests/test_report_export.py::test_write_report_rejects_unsupported_format`
  - `tests/test_report_export.py::test_stale_export_snapshot_cannot_replace_active_context`
- Coverage:
  - unsupported formats fail clearly
  - stale solve callbacks cannot overwrite the active export snapshot

### E5 - Manual Export Smoke Check

- Type: Manual
- Steps:
  1. Launch app: `.\run.bat` or `python -m src.ui.app`
  2. Complete a valid solve with method `Secant`
  3. Click the download button in the algorithmic log header
  4. Export one report each as TXT, HTML, and PDF
  5. Repeat with a handled warning outcome such as invalid Bisection interval
- Expected:
  - picker shows TXT, HTML, and PDF options
  - file extension matches the selected format
  - report content matches the active run and includes verification or the explicit unavailable/fallback text
  - no-solve, validation-failure, and fatal-error states keep export disabled

## Pass Criteria

- Automated tests in this plan pass.
- Manual checks for About/Help and screenshot readiness pass.
- Documentation and UI labels remain consistent with `v0.1.0` and `Week 7 Midterm Build`.
