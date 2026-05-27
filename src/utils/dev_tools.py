import random

from src.utils.parsing import parse_math_expr


def _gen_polynomial() -> dict:
    """Generates a random polynomial equation (quadratic or cubic) with smart bounds."""
    degree = random.choice([2, 3])
    
    if degree == 2:
        a = random.choice([-1, 1]) * random.randint(1, 5)
        b = random.choice([-1, 1]) * random.randint(0, 10)
        c = random.choice([-1, 1]) * random.randint(1, 20)
        
        parts = [f"{a}*x**2"]
        if b != 0:
            sign = "+" if b > 0 else "-"
            parts.append(f"{sign} {abs(b)}*x")
        sign = "+" if c > 0 else "-"
        parts.append(f"{sign} {abs(c)}")
        func = " ".join(parts)
    else:
        a = random.choice([-1, 1]) * random.randint(1, 3)
        b = random.choice([-1, 1]) * random.randint(0, 5)
        c = random.choice([-1, 1]) * random.randint(1, 15)
        
        parts = [f"{a}*x**3"]
        if b != 0:
            sign = "+" if b > 0 else "-"
            parts.append(f"{sign} {abs(b)}*x")
        sign = "+" if c > 0 else "-"
        parts.append(f"{sign} {abs(c)}")
        func = " ".join(parts)
    
    x0 = round(random.uniform(-5.0, 5.0), 2)
    x1 = round(x0 + random.choice([-1, 1]) * random.uniform(0.5, 3.0), 2)
    
    return {"func": func, "x0": str(x0), "x1": str(x1)}


def _gen_trigonometric() -> dict:
    """Generates a random trigonometric equation with smart bounds."""
    trig_fn = random.choice(["sin", "cos"])  # tan excluded: asymptotes at ±π/2 cause inf
    a = random.randint(1, 5)
    c = round(random.uniform(0.1, 2.0), 2)
    sign = random.choice(["+", "-"])
    
    func = f"{a}*{trig_fn}(x) {sign} {c}"
    
    # Trig functions are periodic, so keep bounds within [-pi, pi] range
    x0 = round(random.uniform(-3.0, 3.0), 2)
    x1 = round(x0 + random.choice([-1, 1]) * random.uniform(0.3, 2.0), 2)
    
    return {"func": func, "x0": str(x0), "x1": str(x1)}


def _gen_exponential() -> dict:
    """Generates a random exponential equation with smart bounds."""
    c = random.randint(1, 10)
    variant = random.choice(["sub", "add_x"])
    
    if variant == "sub":
        func = f"exp(x) - {c}"
    else:
        func = f"x*exp(-x) - {round(random.uniform(0.1, 0.5), 2)}"
    
    x0 = round(random.uniform(-1.0, 3.0), 2)
    x1 = round(x0 + random.choice([-1, 1]) * random.uniform(0.5, 2.0), 2)
    
    return {"func": func, "x0": str(x0), "x1": str(x1)}


def _gen_mixed() -> dict:
    """Generates a mixed-type equation (e.g., x*sin(x), x^2 - cos(x))."""
    templates = [
        lambda: f"x*sin(x) - {random.randint(1, 5)}",
        lambda: f"x**2 - cos(x) - {random.randint(1, 5)}",
        lambda: f"exp(-x) - x + {random.randint(1, 3)}",
        lambda: f"x**2 - sin(x) - {random.randint(2, 8)}",
        lambda: f"log(x + {random.randint(1, 3)}) - {round(random.uniform(0.5, 2.5), 2)}",
    ]
    
    func = random.choice(templates)()
    # Clamp x0 to positive domain for log templates
    if "log" in func:
        x0 = round(random.uniform(0.5, 4.0), 2)
    else:
        x0 = round(random.uniform(0.1, 4.0), 2)
    x1 = round(x0 + random.choice([-1, 1]) * random.uniform(0.5, 2.5), 2)
    if "log" in func and x1 < 0.1:
        x1 = round(random.uniform(0.5, 3.0), 2)
    
    return {"func": func, "x0": str(x0), "x1": str(x1)}


def _try_find_bracket(func_str: str, attempts: int = 30) -> tuple[float, float] | None:
    """Attempts to find an interval [a, b] such that f(a) and f(b) have opposite signs."""
    try:
        func = parse_math_expr(func_str)
    except Exception:
        return None

    for _ in range(attempts):
        center = random.uniform(-3.0, 3.0)
        span = random.uniform(0.5, 4.0)
        a = round(center - span, 2)
        b = round(center + span, 2)
        if a == b:
            continue
        if a > b:
            a, b = b, a
        try:
            f_a = func(a)
            f_b = func(b)
        except Exception:
            continue
        if f_a == 0.0:
            return a, a
        if f_b == 0.0:
            return b, b
        if f_a * f_b < 0.0:
            return a, b

    return None


def get_random_test_case(method: str = "Secant") -> dict:
    """
    Dynamically generates a random, mathematically valid test case
    for the Secant Method with varied equation types and smart bounds.
    DEV ONLY: To be removed before production.
    """
    generator = random.choice([_gen_polynomial, _gen_trigonometric, _gen_exponential, _gen_mixed])
    case = generator()

    if method.strip().lower() == "bisection":
        bracket = _try_find_bracket(case["func"])
        if bracket is not None:
            a, b = bracket
            case["x0"] = str(a)
            case["x1"] = str(b)
    
    # Smart tolerance and iteration limits
    case["tol"] = random.choice(["1e-4", "1e-5", "1e-6", "1e-8"])
    case["max_iter"] = random.choice(["20", "30", "50"])
    
    return case


def get_invalid_test_case() -> dict:
    """
    Returns a dictionary containing explicitly invalid data.
    Used for demonstrating the Week 2 Input Validation UI features.
    """
    test_cases = [
        {
            "func": "x**2 & 4",  # Bad character '&'
            "x0": "1.0",
            "x1": "3.0",
            "tol": "1e-6",
            "max_iter": "100"
        },
        {
            "func": "y**2 - 4",  # Wrong variable 'y' instead of 'x'
            "x0": "1.0",
            "x1": "3.0",
            "tol": "1e-6",
            "max_iter": "100"
        },
        {
            "func": "x**2 - 4",
            "x0": "One", # String instead of float
            "x1": "3.0",
            "tol": "1e-6",
            "max_iter": "100"
        },
        {
            "func": "x**2 - 4",
            "x0": "1.0",
            "x1": "3.0",
            "tol": "-1e-6", # Negative tolerance
            "max_iter": "100"
        },
        {
            "func": "x**3 - 8", 
            "x0": "1.5",
            "x1": "Two", # String instead of float
            "tol": "1e-5",
            "max_iter": "50"
        },
        {
            "func": "sin(x) + #invalid", # Bad syntax with '#'
            "x0": "0.1",
            "x1": "1.5",
            "tol": "1e-6",
            "max_iter": "100"
        },
        {
            "func": "x**2 + 5",
            "x0": "1.0",
            "x1": "2.0",
            "tol": "1e-6",
            "max_iter": "A hundred" # String instead of int
        },
        {
            "func": "5", # Horizontal line (will fail math division by zero during solve, testing solver robustness)
            "x0": "1.0",
            "x1": "2.0",
            "tol": "1e-6",
            "max_iter": "100"
        }
    ]
    
    return random.choice(test_cases)
