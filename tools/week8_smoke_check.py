"""Week 8 scripted smoke checks for controller-safe robustness verification."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Callable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.parsing import parse_math_expr
from src.utils.solver_dispatch import get_solver_for_method


REQUIRED_RESULT_KEYS = {"method", "root", "converged", "iterations", "history", "error_msg", "message_level"}


def _assert_result_contract(result: dict) -> None:
    assert REQUIRED_RESULT_KEYS <= set(result.keys()), "Result contract keys missing"


def _run_case(name: str, case: Callable[[], None]) -> bool:
    try:
        case()
        print(f"[PASS] {name}")
        return True
    except Exception as exc:  # pragma: no cover - smoke-script surface area
        print(f"[FAIL] {name}: {exc}")
        return False


def case_success_secant() -> None:
    solver = get_solver_for_method("Secant")
    func = parse_math_expr("x**2 - 4")
    result = solver(func, 1.0, 3.0, 1e-6, 100)
    _assert_result_contract(result)
    assert result["converged"] is True
    assert abs(result["root"] - 2.0) < 1e-4


def case_handled_invalid_bracket() -> None:
    solver = get_solver_for_method("Bisection")
    func = parse_math_expr("x**2 + 1")
    result = solver(func, -1.0, 1.0, 1e-6, 100)
    _assert_result_contract(result)
    assert result["converged"] is False
    assert "Invalid interval" in (result["error_msg"] or "")


def case_handled_non_convergence() -> None:
    solver = get_solver_for_method("Secant")
    func = parse_math_expr("x**3 - 5")
    result = solver(func, 100.0, 99.0, 1e-12, 3)
    _assert_result_contract(result)
    assert result["converged"] is False
    assert "Failed to converge after 3 iterations" in (result["error_msg"] or "")


def main() -> int:
    results = [
        _run_case("successful solve path", case_success_secant),
        _run_case("handled invalid bracket path", case_handled_invalid_bracket),
        _run_case("handled non-convergent path", case_handled_non_convergence),
    ]
    if all(results):
        print("\nWeek 8 smoke checks completed without crashes.")
        return 0
    print("\nWeek 8 smoke checks detected failures.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
