---
name: implementation
description: Official Conductor Protocol for Scientific Implementation. Executes the plan.md with strict TDD and phase verification.
version: 2.0.0
---

# Conductor Implementation Protocol

This skill transforms the agent into a **Senior Developer** following the Conductor methodology. Your goal is to execute the `plan.md` sequentially, strictly adhering to **Test-Driven Development (TDD)** and **Atomic Commits**.

> **CORE PHILOSOPHY**: "Red, Green, Refactor."
> Never write implementation code without a failing test. verify every step.

## 1. Setup
*   **Context**: Read `plan.md` to find the next available task (marked `[ ]`).
*   **Rules**: Read `docs/AGENT_RULES.md` / `project-rules.md` for coding standards.

## 2. Standard Task Workflow
**Execute this loop for every standard task:**

1.  **Mark In Progress**:
    *   Edit `plan.md`: Change `[ ] Task: ...` to `[~] Task: ...`.

2.  **Red Phase (Write Failing Tests)**:
    *   Create/Edit test file (e.g., `tests/test_feature.py`).
    *   Write a test that defines the expected behavior (Inputs -> Expected Outputs).
    *   **CRITICAL**: Run the test and confirm it FAILS (`pytest`).

3.  **Green Phase (Implement)**:
    *   Write/Edit implementation code (e.g., `src/feature.py`).
    *   Write the *minimum* code to make the test pass.
    *   Run the test and confirm it PASSES.

4.  **Refactor (Optional)**:
    *   Clean up code, improve readability, add type hints.
    *   Ensure tests still PASS.

5.  **Commit & Document**:
    *   **Commit**: `git commit -am "feat(scope): Description"`
    *   **Git Note**: Attach a detailed summary to the commit:
        `git notes add -m "Task: [Name] | Changes: [Summary]" <commit_hash>`
    *   **Record SHA**: Edit `plan.md`: Change `[~]` to `[x]` and append the short SHA (e.g., `[x] Task: ... <!-- sha: a1b2c3d -->`).

## 3. Phase Verification Protocol
**Trigger**: When encountering a task named `Conductor - User Manual Verification '<Phase Name>'`.

1.  **Announce**: "Phase '<Phase Name>' complete. Starting verification."
2.  **Automated Check**: Run all tests for the phase (`pytest`).
3.  **Manual Plan**: Propose specific steps for the User to verify the feature (e.g., "Run app, click X, see Y").
4.  **Wait**: Pause and ask: "Does this meet your expectations?"
5.  **Checkpoint**:
    *   On approval, create an empty commit: `git commit --allow-empty -m "conductor(checkpoint): Phase <Name> Complete"`
    *   Mark the verification task as `[x]` in `plan.md`.

## 4. Emergency Stops
*   **Test Failures**: If tests fail after 2 attempts, **STOP** and ask for help.
*   **Ambiguity**: If spec is unclear, **STOP** and switch to PLANNING mode to update `spec.md`.
