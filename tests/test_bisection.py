import math

from src.solvers.bisection_method import solve_bisection_method


def test_bisection_basic_convergence():
    func = lambda x: x**2 - 4.0
    result = solve_bisection_method(func, a=1.0, b=3.0, tol=1e-5)

    assert result["converged"] is True
    assert math.isclose(result["root"], 2.0, abs_tol=1e-4)
    assert result["error_msg"] is None
    assert len(result["history"]) > 0


def test_bisection_invalid_interval():
    func = lambda x: x**2 + 1.0
    result = solve_bisection_method(func, a=-1.0, b=1.0)

    assert result["converged"] is False
    assert result["root"] is None
    assert "Invalid interval" in result["error_msg"]


def test_bisection_max_iterations():
    func = lambda x: x**3 - 2.0
    result = solve_bisection_method(func, a=1.0, b=2.0, tol=1e-12, max_iter=2)

    assert result["converged"] is False
    assert result["iterations"] == 2
    assert "Failed to converge after 2 iterations" in result["error_msg"]


def test_bisection_exact_endpoint_root_marks_table_row():
    func = lambda x: x - 1.0
    result = solve_bisection_method(func, a=1.0, b=3.0)

    assert result["converged"] is True
    assert math.isclose(result["root"], 1.0, abs_tol=1e-12)
    assert any(step.get("is_mid") is True for step in result["history"])


def test_bisection_invalid_interval_failure_contract_keys():
    """Failure paths should preserve core history/result compatibility keys."""
    result = solve_bisection_method(lambda x: x**2 + 1.0, a=-1.0, b=1.0)

    assert result["converged"] is False
    assert result["method"] == "Bisection"
    assert {"root", "converged", "iterations", "history", "error_msg", "method", "message_level"} <= set(result.keys())
    assert result["message_level"] == "warning"
    assert len(result["history"]) >= 3
    assert {"n", "x_n", "f(x_n)", "error", "explanation"} <= set(result["history"][-1].keys())
