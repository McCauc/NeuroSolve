from typing import Callable, Dict, Any, List


def solve_bisection_method(
    func: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-6,
    max_iter: int = 100
) -> Dict[str, Any]:
    """
    Finds the root of a function using the Bisection Method algorithm.

    Args:
        func: The standard Python function f(x).
        a: Lower bound of the interval.
        b: Upper bound of the interval.
        tol: Tolerance for convergence (checks interval width and |f(mid)|).
        max_iter: Maximum number of iterations to prevent infinite loops.

    Returns:
        dict: A dictionary containing:
            - "root": float | None, The approximate solution if found
            - "converged": bool, Whether convergence was achieved
            - "iterations": int, Number of steps taken
            - "history": List[dict], Iteration history for the UI log
            - "error_msg": str | None, Error message if failed
            - "method": str, Method label for UI rendering
    """
    history: List[Dict[str, Any]] = []

    try:
        f_a = func(a)
        f_b = func(b)
    except Exception as e:
        return {
            "root": None,
            "converged": False,
            "iterations": 0,
            "history": history,
            "error_msg": f"Error evaluating function at interval endpoints: {str(e)}",
            "method": "Bisection",
            "message_level": "warning",
        }

    history.append({
        "n": 0, "x_n": a, "f(x_n)": f_a, "error": None, "a": a, "b": b, "is_mid": False,
        "explanation": f"Initialization: Evaluate interval start a={a:g}, giving f(a)={f_a:g}."
    })
    history.append({
        "n": 1, "x_n": b, "f(x_n)": f_b, "error": abs(b - a), "a": a, "b": b, "is_mid": False,
        "explanation": f"Initialization: Evaluate interval end b={b:g}, giving f(b)={f_b:g}."
    })

    if f_a == 0.0:
        history.append({
            "n": 1, "x_n": a, "f(x_n)": f_a, "error": 0.0, "a": a, "b": b, "is_mid": True,
            "explanation": "Process completed: Interval start is an exact root."
        })
        return {
            "root": a,
            "converged": True,
            "iterations": 1,
            "history": history,
            "error_msg": None,
            "method": "Bisection",
            "message_level": "success",
        }

    if f_b == 0.0:
        history.append({
            "n": 1, "x_n": b, "f(x_n)": f_b, "error": 0.0, "a": a, "b": b, "is_mid": True,
            "explanation": "Process completed: Interval end is an exact root."
        })
        return {
            "root": b,
            "converged": True,
            "iterations": 1,
            "history": history,
            "error_msg": None,
            "method": "Bisection",
            "message_level": "success",
        }

    if f_a * f_b > 0.0:
        history.append({
            "n": 2, "x_n": a, "f(x_n)": f_a, "error": None, "a": a, "b": b, "is_mid": False,
            "explanation": "Process stopped: Interval does not bracket a root (f(a) and f(b) have the same sign)."
        })
        return {
            "root": None,
            "converged": False,
            "iterations": 0,
            "history": history,
            "error_msg": "Invalid interval: f(a) and f(b) must have opposite signs.",
            "method": "Bisection",
            "message_level": "warning",
        }

    left = a
    right = b
    f_left = f_a
    f_right = f_b

    for i in range(1, max_iter + 1):
        mid = (left + right) / 2.0
        try:
            f_mid = func(mid)
        except Exception as e:
            history.append({
                "n": i + 1, "x_n": mid, "f(x_n)": float("nan"), "error": None, "a": left, "b": right, "is_mid": True,
                "explanation": f"Process stopped: Mathematical domain error at mid={mid:g}: {str(e)}"
            })
            return {
                "root": mid,
                "converged": False,
                "iterations": i,
                "history": history,
                "error_msg": f"Calculation error at x={mid}: {str(e)}",
                "method": "Bisection",
                "message_level": "warning",
            }

        error_val = abs(right - left) / 2.0
        history.append({
            "n": i + 1,
            "x_n": mid,
            "f(x_n)": f_mid,
            "error": error_val,
            "a": left,
            "b": right,
            "is_mid": True,
            "explanation": (
                f"Iteration {i}: Midpoint m={mid:g} with f(m)={f_mid:g}. "
                "Choose the sub-interval that still brackets the root."
            )
        })

        if abs(f_mid) == 0.0 or error_val < tol:
            history.append({
                "n": i + 1, "x_n": mid, "f(x_n)": f_mid, "error": error_val, "a": left, "b": right, "is_mid": True,
                "explanation": f"Process completed: Residual error is within tolerance ({tol}). Root found!"
            })
            return {
                "root": mid,
                "converged": True,
                "iterations": i + 1,
                "history": history,
                "error_msg": None,
                "method": "Bisection",
                "message_level": "success",
            }

        if f_left * f_mid < 0.0:
            right = mid
            f_right = f_mid
        else:
            left = mid
            f_left = f_mid

    history.append({
        "n": max_iter, "x_n": (left + right) / 2.0, "f(x_n)": func((left + right) / 2.0),
        "error": abs(right - left) / 2.0, "a": left, "b": right, "is_mid": True,
        "explanation": f"Process stopped: Maximum iterations ({max_iter}) reached without meeting tolerance criteria."
    })
    return {
        "root": (left + right) / 2.0,
        "converged": False,
        "iterations": max_iter,
        "history": history,
        "error_msg": f"Failed to converge after {max_iter} iterations.",
        "method": "Bisection",
        "message_level": "warning",
    }
