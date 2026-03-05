import pytest
import math
from src.solvers.secant_method import solve_secant_method

def test_secant_basic_convergence():
    """Test standard convergence on a simple polynomial x^2 - 4"""
    # Root is exactly 2.0
    func = lambda x: x**2 - 4.0
    
    result = solve_secant_method(func, x0=1.0, x1=3.0, tol=1e-5)
    
    assert result["converged"] is True
    assert math.isclose(result["root"], 2.0, abs_tol=1e-5)
    assert result["error_msg"] is None
    assert len(result["history"]) > 2

def test_secant_division_by_zero():
    """Test algorithm safely catches horizontal secant lines without crashing"""
    # A horizontal line f(x) = 5
    func = lambda x: 5.0
    
    result = solve_secant_method(func, x0=1.0, x1=2.0)
    
    assert result["converged"] is False
    assert result["error_msg"] == "Division by zero (secant line is horizontal)."
    
def test_secant_max_iterations():
    """Test algorithm gracefully stops after max_iter when failing to converge"""
    # A function that takes some time to converge starting from far away
    # Setting max_iter ridiculously low to force an early exit
    func = lambda x: x**3 - 5.0
    
    result = solve_secant_method(func, x0=100.0, x1=99.0, max_iter=3)
    
    assert result["converged"] is False
    assert result["iterations"] == 3
    assert "Failed to converge after 3 iterations" in result["error_msg"]

def test_secant_immediate_success():
    """Test behavior when the initial guess is exactly right"""
    func = lambda x: x - 5.0
    
    result = solve_secant_method(func, x0=0.0, x1=5.0)
    
    assert result["converged"] is True
    assert result["iterations"] == 1
    assert result["root"] == 5.0
    
def test_secant_exception_handling():
    """Test behavior when the internal function raises an exception"""
    def bad_func(x):
        if x > 2.0:
            raise ValueError("Domain error simulated")
        return x
        
    result = solve_secant_method(bad_func, x0=1.0, x1=3.0)
    
    assert result["converged"] is False
    assert "Error evaluating function" in result["error_msg"]
