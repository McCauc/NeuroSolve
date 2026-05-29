# NeuroSolve

NeuroSolve is a Windows-first desktop learning app for numerical root finding. It is designed for coursework and demonstrations where users need to see both the final answer and the step-by-step trail behind it.

This repository currently represents the Week 7 midterm package release.

- Official version: `v0.1.0`
- Milestone label: `Week 7 Midterm Build`
- Team members: Rejay Buta, John Cedrick Delgado, Carlo Jose Anyayahan

## Current Implemented Scope

The current runnable build includes:

- Method selection between Secant and Bisection
- Input validation for function and numeric parameters
- Step-by-step algorithmic log / solution trail
- Graph rendering for solve output
- Method-aware iteration table rendering
- Local TXT, HTML, and PDF solution-trail report export
- Automated tests for parsing, solver behavior, and dispatch

## Not Yet Implemented in This Build

To keep this README accurate for the current codebase:

- AI assistant and chat explanation workflow are not part of the current runnable UI

## Requirements

- Python `3.10+` (known working in project context: `3.11.9`)
- Windows + PowerShell for the default local workflow

Project dependencies are installed from:

- [`requirements.txt`](requirements.txt)

## Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run the App

Option 1 (recommended in this repo):

```powershell
.\run.bat
```

Option 2 (module entrypoint):

```powershell
python -m src.ui.app
```

## Run Tests

```powershell
pytest tests
```

## Project Structure

- `src/solvers/` - numerical methods and solver logic
- `src/ui/` - CustomTkinter desktop interface
- `src/utils/` - shared utilities (parsing, report export, helpers)
- `tests/` - automated tests
- `docs/` - supporting documentation and Week 7 artifacts

## Test Plan

- Test Plan v1: [`docs/test-plan-v1.md`](docs/test-plan-v1.md)

## Notes for Reviewers

- This release focuses on the local solver-first workflow.
- Core usage does not require accounts or internet access.
- Documentation intentionally avoids claiming future features as already shipped.
