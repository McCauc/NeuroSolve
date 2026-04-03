import pytest

from src.solvers.secant_method import solve_secant_method
from src.solvers.bisection_method import solve_bisection_method
from src.utils.solver_dispatch import get_solver_for_method


def test_dispatch_secant():
    assert get_solver_for_method("Secant") is solve_secant_method


def test_dispatch_bisection():
    assert get_solver_for_method("Bisection") is solve_bisection_method


def test_dispatch_invalid_method():
    with pytest.raises(ValueError):
        get_solver_for_method("UnknownMethod")


def test_dispatch_normalizes_whitespace_and_label_variants():
    assert get_solver_for_method("  secant method  ") is solve_secant_method
    assert get_solver_for_method("\nBisection Method\t") is solve_bisection_method
