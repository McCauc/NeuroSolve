from typing import Callable

from src.solvers.secant_method import solve_secant_method
from src.solvers.bisection_method import solve_bisection_method


def get_solver_for_method(method_name: str) -> Callable:
    """
    Returns the solver function for the given method label.

    Args:
        method_name: Display label such as "Secant" or "Bisection".

    Returns:
        Callable: Solver function matching the method.

    Raises:
        ValueError: If the method is unknown.
    """
    normalized = (method_name or "").strip().lower()
    if normalized in {"secant", "secant method"}:
        return solve_secant_method
    if normalized in {"bisection", "bisection method"}:
        return solve_bisection_method
    raise ValueError(f"Unknown method: {method_name}")
