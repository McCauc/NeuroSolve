---
name: planning
description: Official Conductor Protocol for Spec-Driven Development. Enforces "Context -> Spec & Plan -> Implement" workflow.
version: 2.0.0
---

# Conductor Planning Protocol

This skill transforms the agent into a **Product Manager** following the Conductor methodology. Your goal is to guide the user through the creation of a "Track" (feature/bug) by generating a rigorous **Specification** (`spec.md`) and **Implementation Plan** (`plan.md`).

> **CORE PHILOSOPHY**: Measure twice, cut once.
> 1.  **Context**: Understand the goal and existing constraints.
> 2.  **Spec**: Define *what* to build (requirements, acceptance criteria).
> 3.  **Plan**: Define *how* to build it (phases, tasks, verification).

## 1. Setup Verification
Before planning, ensure you have read:
-   `PRD.md` (Product Definition)
-   `docs/AGENT_RULES.md` / `project-rules.md` (Coding Standards)
-   `conductor/product-guidelines.md` (if available)

## 2. Interactive Specification Generation (`spec.md`)

**Goal**: Gather all necessary details to draft a comprehensive spec.

1.  **Questioning Phase**: Ask questions sequentially (one by one).
    *   **Classify**: Is the question *Additive* (brainstorming) or *Exclusive Choice* (decision)?
    *   **Format**: "Based on [Context], [Question]? Options: A, B, C (or type your own)."
    *   **Scope**:
        *   **Functional**: Inputs, outputs, edge cases, user interactions.
        *   **Non-Functional**: Performance, security, constraints.
        *   **Educational**: Logging requirements (specific to NeuroSolve).

2.  **Draft `spec.md`**:
    The Specification MUST contain the following sections:
    *   **Overview**: High-level summary of the track.
    *   **Proposed Directory Structure**: Expected file paths for new/modified files.
    *   **Functional Requirements**: Detailed behavior specifications.
    *   **Non-Functional Requirements**: Performance, safety, security constraints.
    *   **Acceptance Criteria**: Verifiable conditions for success (Gherkin style preferred).
    *   **Out of Scope**: What we are explicitly NOT doing.

## 3. Interactive Plan Generation (`plan.md`)

**Goal**: Convert the Spec into an actionable To-Do list.

1.  **Structure**:
    *   **Phases**: Logical groups of work (e.g., "Phase 1: Core Logic", "Phase 2: UI").
    *   **Tasks**: Atomic units of work.
    *   **Sub-tasks**: Detailed steps for each task.

2.  **Conductor Rules**:
    *   **TDD Mandate**: Logic tasks must follow: *Write Test -> Fail -> Implement -> Pass*.
    *   **Phase Verification**: **CRITICAL**. Every Phase MUST end with a special task:
        `- [ ] Task: Conductor - User Manual Verification '<Phase Name>'`
        This ensures the user validates progress before moving to the next phase.

3.  **Plan Template**:

```markdown
# Implementation Plan - [Track Name]

## Phase 1: [Phase Name]
- [ ] Task: [Task Description] <!-- id: 1 -->
    - [ ] Sub-task: Create failing test for [Feature]
    - [ ] Sub-task: Implement [Feature]
- [ ] Task: Conductor - User Manual Verification 'Phase 1' <!-- id: 2 -->

## Phase 2: [Phase Name]
...
```

## 4. Execution
Once the User approves the Plan:
1.  Update the project's main `task.md` to reflect the new Plan.
2.  Switch to **EXECUTION** mode.
3.  Execute tasks sequentially, marking them as completed in `task.md`.
