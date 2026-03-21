from typing import Callable, Dict, Any, List

def solve_secant_method(func: Callable[[float], float], x0: float, x1: float, tol: float = 1e-6, max_iter: int = 100) -> Dict[str, Any]:
    """
    Finds the root of a function using the Secant Method algorithm.
    
    Formula: x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))
    
    Args:
        func: The standard Python function f(x).
        x0: First initial guess.
        x1: Second initial guess.
        tol: Tolerance for convergence (checks absolute difference between successive guesses).
        max_iter: Maximum number of iterations to prevent infinite loops.
        
    Returns:
        dict: A dictionary containing:
            - "root": float | None, The approximate solution if found
            - "converged": bool, Whether convergence was achieved
            - "iterations": int, Number of steps taken
            - "history": List[dict], Iteration history for the UI log (includes an 'explanation' string)
            - "error_msg": str | None, Error message if failed
    """
    
    history: List[Dict[str, Any]] = []
    
    try:
        f_x0 = func(x0)
        f_x1 = func(x1)
    except Exception as e:
        return {
            "root": None,
            "converged": False,
            "iterations": 0,
            "history": history,
            "error_msg": f"Error evaluating function at initial guesses: {str(e)}"
        }

    # Log initial guesses
    history.append({
        "n": 0, "x_n": x0, "f(x_n)": f_x0, "error": None,
        "explanation": f"Initialization: We evaluate our first guess, giving f({x0:g}) = {f_x0:g}."
    })
    history.append({
        "n": 1, "x_n": x1, "f(x_n)": f_x1, "error": abs(x1 - x0),
        "explanation": f"Initialization: We evaluate our second guess, giving f({x1:g}) = {f_x1:g}."
    })
    
    # If the second guess happens to be an exact root immediately
    if abs(f_x1) == 0.0 or abs(x1 - x0) < tol:
        history.append({
            "n": 1, "x_n": x1, "f(x_n)": f_x1, "error": 0.0,
            "explanation": "Process completed: Initial guess is an exact root or within tolerance."
        })
        return {
            "root": x1,
            "converged": True,
            "iterations": 1,
            "history": history,
            "error_msg": None
        }

    current_x0 = x0
    current_x1 = x1
    current_f0 = f_x0
    current_f1 = f_x1
    
    for i in range(2, max_iter + 2):
        # STRESS TEST FINDING: Explicitly catch ZeroDivisionError
        denominator = current_f1 - current_f0
        if abs(denominator) == 0.0:
            history.append({
                "n": i, "x_n": current_x1, "f(x_n)": current_f1, "error": None,
                "explanation": "Process stopped: Division by zero encountered. The secant line became horizontal."
            })
            return {
                "root": current_x1, # Return best guess so far
                "converged": False,
                "iterations": i - 1,
                "history": history,
                "error_msg": "Division by zero (secant line is horizontal)."
            }
            
        # Secant method formula
        x_next = current_x1 - current_f1 * (current_x1 - current_x0) / denominator
        
        try:
            f_next = func(x_next)
        except Exception as e:
            history.append({
                "n": i, "x_n": x_next, "f(x_n)": None, "error": None,
                "explanation": f"Process stopped: Mathematical domain error encountered during evaluation: {str(e)}"
            })
            return {
                "root": x_next,
                "converged": False,
                "iterations": i,
                "history": history,
                "error_msg": f"Calculation error at x={x_next}: {str(e)}"
            }
            
        error_val = abs(x_next - current_x1)
        explanation = (
            f"Using points x_{i-2}={current_x0:g} and x_{i-1}={current_x1:g}, "
            f"we use the secant line to approximate the next root at x_{i}={x_next:g}. "
            f"Evaluating the function yields f({x_next:g}) = {f_next:g}."
        )
        history.append({"n": i, "x_n": x_next, "f(x_n)": f_next, "error": error_val, "explanation": explanation})
        
        # Check convergence criteria
        # We check both the step size and the function value being close to 0
        if error_val < tol or abs(f_next) == 0.0:
            history.append({
                "n": i, "x_n": x_next, "f(x_n)": f_next, "error": error_val,
                "explanation": f"Process completed: Residual error is within tolerance ({tol}). Root found!"
            })
            return {
                "root": x_next,
                "converged": True,
                "iterations": i,
                "history": history,
                "error_msg": None
            }
            
        # Update variables for next iteration
        current_x0 = current_x1
        current_f0 = current_f1
        current_x1 = x_next
        current_f1 = f_next
        
    # If loop finishes without returning, max_iter was reached
    history.append({
        "n": max_iter, "x_n": current_x1, "f(x_n)": current_f1, "error": abs(current_x1 - current_x0),
        "explanation": f"Process stopped: Maximum iterations ({max_iter}) reached without meeting tolerance criteria."
    })
    return {
        "root": current_x1,
        "converged": False,
        "iterations": max_iter,
        "history": history,
        "error_msg": f"Failed to converge after {max_iter} iterations."
    }
