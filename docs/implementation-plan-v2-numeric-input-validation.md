# NeuroSolve Implementation Plan v2: Numeric Input Guard and Invalid-State Feedback

- Version: `v2`
- Date: `2026-05-14`
- Status: `ready-for-dev`
- Baseline: `docs/implementation-plan-v1-numeric-input-validation.md`
- Improvement terms applied: refine, clarify, sequence, prioritize, operationalize, de-risk, verify

## Goal

Make the sidebar numeric inputs safer and easier to use by preventing non-numeric text from surviving in `X0 / A`, `X1 / B`, and `MAX ITER.`, and by turning the affected field red when invalid input is detected.

The existing solver flow should stay intact for valid input. The global bad-input banner in `MainContentFrame` should remain as a fallback, not the only warning.

## Why v2 Exists

v1 identified the right problem and the right files. v2 tightens the plan so it is easier to implement, test, and review:

- It clarifies exactly what each field accepts.
- It sequences the work so the safest pieces come first.
- It adds a de-risked fallback path so the controller still protects the solver.
- It separates the UI filter from the solve-time safety net.
- It makes the validation rules testable instead of burying them inside widget code.

## Clarified Input Rules

| Field | Allowed input | Rejected input | Notes |
| --- | --- | --- | --- |
| `X0 / A` | signed decimal numbers | letters, spaces, repeated dots, symbols, scientific notation | allow a leading minus so negative guesses still work |
| `X1 / B` | signed decimal numbers | letters, spaces, repeated dots, symbols, scientific notation | same rule as `X0 / A` |
| `MAX ITER.` | whole numbers only | decimals, signs, letters, spaces, symbols | integer-only because iteration count must be discrete |
| `TOLERANCE` | unchanged in v2 | unchanged in v2 | keep scientific notation support here because the solver already uses it |

Examples:

- Allowed for `X0 / A` and `X1 / B`: `1`, `-2`, `3.5`, `0.125`
- Rejected for `X0 / A` and `X1 / B`: `abc`, `1..2`, `2-3`, `1e-3`
- Allowed for `MAX ITER.`: `1`, `50`, `100`
- Rejected for `MAX ITER.`: `-1`, `3.5`, `10a`

## Scope

In scope:

- `src/ui/components/sidebar.py`
- `src/ui/app.py`
- `tests/` for helper-level validation coverage
- `docs/test-plan-v1.md` only if we want to add a brief reviewer-facing note later

Out of scope:

- Solver math changes
- Method dispatch changes
- Graph rendering changes
- `TOLERANCE` behavior changes
- Global output styling changes outside the existing fallback banner

## Implementation Sequence

1. **Operationalize the rules in a pure helper layer.**
   - Add small validation helpers that can be tested without launching the UI.
   - Prefer a simple validator module or equivalent pure functions over embedding all logic inside widget callbacks.
   - Keep the helpers focused on three jobs:
     - sanitize input text
     - validate final field value
     - classify invalid state for red-border feedback

2. **Refine `SidebarFrame` so each numeric field can show state.**
   - Extend the sidebar field construction so the wrapper frame and entry widget are both retained.
   - Store the border-bearing frame for each field, because that is what should turn red.
   - Keep the current brutalist composition unchanged unless the state styling needs a small wrapper adjustment.

3. **Sequence live filtering before submit-time fallback.**
   - Attach keypress or validation callbacks to `X0 / A`, `X1 / B`, and `MAX ITER.`.
   - Prevent invalid characters from staying in the field when the user types or pastes them.
   - If a value is incomplete but still on the path to a valid number, allow the user to finish typing instead of blocking too early.
   - Mark the field red when the committed content is invalid.

4. **Keep the controller as the safety net.**
   - Re-check the numeric fields in `NeuroSolveApp.run_solver()` before conversion.
   - If anything slips past the UI filter, stop the solve and route the user to the existing bad-input flow.
   - This de-risks the feature because a buggy callback cannot send broken data into the solver.

5. **Reset styling on clear and on dev fillers.**
   - `clear_inputs()` should remove text and return all numeric fields to the default black border.
   - Dev-only filler helpers should also restore the clean state after inserting sample values.
   - Any future validation state should be easy to clear from one shared helper.

6. **Verify the behavior with testable helpers plus manual UI smoke checks.**
   - Add unit tests for the pure validation helpers first.
   - Add controller-level tests only if the helper layer makes them cheap and stable.
   - Use manual UI verification for the red border behavior, because the project does not currently have automated visual tests.

## File Plan

| File | Planned change |
| --- | --- |
| `src/ui/components/sidebar.py` | add numeric field validation hooks, field state helpers, and red-border styling support |
| `src/ui/app.py` | add final solve-time numeric validation before `float()` / `int()` conversion |
| `tests/test_*` | add helper tests for numeric sanitizing and validation rules |
| `docs/test-plan-v1.md` | optional short cross-reference if we want reviewer-facing coverage notes |

## Acceptance Criteria

- [ ] Typing or pasting letters into `X0 / A`, `X1 / B`, or `MAX ITER.` does not leave those invalid characters in the field.
- [ ] `X0 / A` and `X1 / B` accept signed decimal input such as `1`, `-2`, and `3.5`.
- [ ] `MAX ITER.` accepts whole numbers only.
- [ ] Invalid numeric content turns the affected field border red until the value is corrected or cleared.
- [ ] Clearing the sidebar resets all numeric fields to the normal black-border style.
- [ ] The controller still blocks bad values even if a validation callback fails.
- [ ] Valid secant and bisection runs behave exactly as before.
- [ ] `TOLERANCE` keeps its current behavior and is not broken by the numeric guard work.

## Verification Plan

- Run the full regression suite:
  - `pytest tests`
- Run any new validation-helper tests directly if they are added:
  - `pytest tests/test_*validation*`
- Manual smoke test:
  - launch the app
  - type letters into `X0 / A`, `X1 / B`, and `MAX ITER.`
  - confirm the fields reject or sanitize the invalid text
  - paste invalid text into each field
  - confirm the invalid field turns red
  - enter valid numeric values
  - confirm the red state clears
  - click `Clear`
  - confirm all numeric fields return to the default appearance
- Dev-mode smoke test:
  - use the existing invalid-input filler path to confirm the warning state is easy to see during debugging

## Risks And Mitigations

- Tk validation callbacks can be inconsistent for paste events.
  - Mitigation: keep a submit-time fallback in `run_solver()`.
- The border belongs to the wrapper frame, not the entry widget itself.
  - Mitigation: keep a stable reference to the wrapper frame for each numeric field.
- Negative values matter for `X0 / A` and `X1 / B`.
  - Mitigation: allow a leading minus in those two fields, but keep `MAX ITER.` integer-only.
- The output banner already provides a global failure state.
  - Mitigation: leave it in place so the UI still warns the user even if a field-state update fails.

## Rollback / Fallback

- If live filtering proves flaky, keep the solve-time validator and simplify the UI layer to red-on-submit only.
- If red border styling is unstable on a platform, reuse the same validation helpers but fall back to the existing output error banner for the visible warning.
- If the stricter signed-decimal rule is later considered too narrow, expand the validator in a separate follow-up so the current plan stays reviewable and low-risk.

## Week 12 - Testing & QA Output

### Testing Checklist Completed

- [x] `tests/test_numeric_validation.py::test_normalize_numeric_text_strips_outer_whitespace`
- [x] `tests/test_numeric_validation.py::test_float_partial_states_are_allowed_while_typing`
- [x] `tests/test_numeric_validation.py::test_float_final_state_rejects_scientific_notation_and_letters`
- [x] `tests/test_numeric_validation.py::test_int_partial_states_are_allowed_while_typing`
- [x] `tests/test_numeric_validation.py::test_int_final_state_requires_whole_numbers_only`
- [x] `tests/test_dispatch.py::test_dispatch_normalizes_whitespace_and_label_variants`
- [x] `tests/test_bisection.py::test_bisection_basic_convergence`
- [x] `tests/test_bisection.py::test_bisection_invalid_interval`
- [x] `tests/test_secant.py::test_secant_basic_convergence`
- [x] `tests/test_secant.py::test_secant_division_by_zero`
- [x] `tests/test_warning_classification.py::test_classify_solver_message_flags_handled_solver_failures_as_warning`
- [x] `tests/test_verification_payload.py::test_secant_success_includes_structured_verification_payload`
- [x] `tests/test_report_export.py::test_report_model_has_header_metadata_and_required_section_order`
- [x] `tests/test_app_metadata.py::test_app_identity_bundle_values`

### Regression Tests Re-run

- `pytest -q tests/test_app_metadata.py tests/test_dispatch.py tests/test_bisection.py tests/test_secant.py tests/test_numeric_validation.py tests/test_warning_classification.py`
  - Result: `27 passed`
- `pytest -q`
  - Result: `83 passed`

### Notes

- The bug list + fixes summary is intentionally omitted here because another teammate is handling that section.
- Manual UI smoke checks for the red border behavior are still worth doing separately on `X0 / A`, `X1 / B`, and `MAX ITER.` because this repo does not have automated visual tests.
