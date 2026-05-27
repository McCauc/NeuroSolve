from src.utils.numeric_validation import is_numeric_text_valid, normalize_numeric_text


def test_normalize_numeric_text_strips_outer_whitespace():
    assert normalize_numeric_text("  12.5  ") == "12.5"


def test_float_partial_states_are_allowed_while_typing():
    assert is_numeric_text_valid("", "float", final=False)
    assert is_numeric_text_valid("-", "float", final=False)
    assert is_numeric_text_valid(".", "float", final=False)
    assert is_numeric_text_valid("-.", "float", final=False)
    assert is_numeric_text_valid("1.", "float", final=False)
    assert is_numeric_text_valid("-3.5", "float", final=False)
    assert not is_numeric_text_valid(" 1.5", "float", final=False)


def test_float_final_state_rejects_scientific_notation_and_letters():
    assert is_numeric_text_valid("1.5", "float", final=True)
    assert is_numeric_text_valid("-2", "float", final=True)
    assert not is_numeric_text_valid(" 1.5", "float", final=True)
    assert not is_numeric_text_valid("1e-3", "float", final=True)
    assert not is_numeric_text_valid("abc", "float", final=True)
    assert not is_numeric_text_valid("1..2", "float", final=True)


def test_int_partial_states_are_allowed_while_typing():
    assert is_numeric_text_valid("", "int", final=False)
    assert is_numeric_text_valid("0", "int", final=False)
    assert is_numeric_text_valid("123", "int", final=False)
    assert not is_numeric_text_valid("-1", "int", final=False)
    assert not is_numeric_text_valid("3.5", "int", final=False)
    assert not is_numeric_text_valid(" 123", "int", final=False)


def test_int_final_state_requires_whole_numbers_only():
    assert is_numeric_text_valid("0", "int", final=True)
    assert is_numeric_text_valid("100", "int", final=True)
    assert not is_numeric_text_valid(" 100", "int", final=True)
    assert not is_numeric_text_valid("", "int", final=True)
    assert not is_numeric_text_valid("-1", "int", final=True)
    assert not is_numeric_text_valid("10a", "int", final=True)
