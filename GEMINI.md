# NeuroSolve Context & Rules (GEMINI.md)

This file serves as the primary context anchor for the AI Agent (Gemini). It consolidates project identity, critical rules, and skill triggers.

## 1. Project Identity
**NeuroSolve** is a Scientific/Numerical computation application.
**Goal**: Educational transparency. We explain the *method*, not just the answer.

## 2. Tech Stack
- **Core**: Python 3.x
- **Numerical**: NumPy (Vectorized operations required)
- **Symbolic**: SymPy (Use expression trees, NOT regex strings)
- **UI**: CustomTkinter (Desktop Native, strict separation from solver logic)

## 3. Law of the Agent
> **Strict Adherence Required. Deviations will be rejected.**

1.  **No Code Without Plan**: You must have an approved `plan.md` before writing implementation code.
2.  **TDD Mandate**: Write failing tests (Red) -> Implement (Green) -> Refactor.
3.  **Math Rigor**:
    -   Validate domains (e.g., division by zero).
    -   Handle non-convergence gracefully.
    -   Never hallucinate convergence; report errors honestly.
4.  **User Verification**: Stop at all "Verification" tasks. Do not proceed without user approval.

## 4. Skill Triggers
Use these skills to guide your workflow:

-   **Start New Feature** -> Read `.agent/skills/planning/SKILL.md`
-   **Write Code** -> Read `.agent/skills/implementation/SKILL.md`
-   **Review Code** -> Read `.agent/skills/code-review/SKILL.md`
-   **Debug/Explore** -> Read `.agent/skills/codebase-investigator/SKILL.md`

## 5. Documentation Map
-   **Detailed Rules**: `docs/AGENT_RULES.md`
-   **Product Spec**: `PRD.md`


## 6. Critical Instruction
**ALWAYS** prefer retrieval-led reasoning. If you are unsure about a library (NumPy/SymPy) or a math concept, use the `context7` tools or `mcp_exa` search tools to verify before guessing.

## 7. Context Maintenance Protocol
> **Instruction to Agent**: You must maintain this file as the project evolves.

1.  **New Tech**: If you add a dependency (e.g., `pandas`) to `requirements.txt`, you **MUST** update Section 2 (Tech Stack).
2.  **New Skills**: If you create a new skill file in `.agent/skills/`, you **MUST** update Section 4 (Skill Triggers).
3.  **New Files**: If you create a new file in `src/` or `tests/`, you **MUST** add it to `docs/CODEBASE_MAP.md`.
4.  **Rule Changes**: If a user rule changes (e.g., "Allow regex"), you **MUST** update Section 3 (Law of the Agent).

