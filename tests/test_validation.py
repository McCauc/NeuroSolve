import pytest
from src.utils.parsing import parse_math_expr

class TestInputValidation:
    """
    Test suite fulfilling the Week 2 Requirement: 'At least 3 invalid input tests documented'.
    These tests ensure that our parsing logic explicitly catches bad inputs before mathematical execution.
    """

    def test_invalid_characters_rejected(self):
        """Test #1: Ensures symbols outside of the allowed mathematical subset throw errors."""
        invalid_expr = "x**2 & 4"
        with pytest.raises(ValueError) as exc:
            parse_math_expr(invalid_expr)
        assert "Invalid characters detected" in str(exc.value)

    def test_unknown_variables_rejected(self):
        """Test #2: Ensures equations utilizing variables other than 'x' are rejected."""
        # Our app strictly operates on single-variable equations regarding x
        invalid_expr = "y**2 - 4"
        with pytest.raises(ValueError) as exc:
            parse_math_expr(invalid_expr)
        assert "Expression can only contain the variable 'x'" in str(exc.value)

    def test_malformed_syntax_rejected(self):
        """Test #3: Ensures mathematically unparseable syntax throws errors."""
        invalid_expr = "x**2 - - * 4"
        with pytest.raises(ValueError) as exc:
            parse_math_expr(invalid_expr)
        assert "Invalid mathematical expression" in str(exc.value)
