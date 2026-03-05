import sympy as sp
import re
from typing import Callable

def parse_math_expr(expr_str: str) -> Callable:
    """
    Safely parses a mathematical string into a Python callable function using SymPy.
    
    Args:
        expr_str (str): The mathematical expression as a string (e.g., "x**2 - 4").
        
    Returns:
        Callable: A Python function that takes a float `x` and returns a float.
        
    Raises:
        ValueError: If the expression is invalid or cannot be parsed.
    """
    try:
        # Pre-flight security check: Strictly allow only alphanumeric, basic math operators, and whitespace
        if not re.match(r'^[a-zA-Z0-9\.\+\-\*\/\(\)\s]+$', expr_str):
            raise ValueError("Invalid characters detected. Only standard mathematical expressions allowed.")

        # Define the symbol 'x' explicitly as required by project rules
        x = sp.Symbol('x')
        
        # Parse the string into a SymPy expression
        # sympify is safely isolated, passing our regex validation
        expr = sp.sympify(expr_str)
        
        # Ensure the expression actually contains 'x' or is a valid constant
        if not expr.free_symbols.issubset({x}):
            raise ValueError(f"Expression can only contain the variable 'x'. Found: {expr.free_symbols}")
            
        # Convert the SymPy expression into a fast NumPy-compatible lambda function
        num_func = sp.lambdify(x, expr, modules=['numpy', 'math'])
        
        # Wrap it to ensure it returns standard Python floats instead of NumPy scalars
        # to prevent CustomTkinter serialization/rendering issues
        def wrapper_func(val: float) -> float:
            # We explicitly cast to float here to ensure standard types
            return float(num_func(val))
            
        return wrapper_func
        
    except sp.SympifyError as e:
        raise ValueError(f"Invalid mathematical expression: '{expr_str}'. Details: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to parse expression '{expr_str}'. Error: {str(e)}")
