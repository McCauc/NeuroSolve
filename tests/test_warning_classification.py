from src.utils.warning_classification import (
    classify_solver_message,
    format_log_title,
    resolve_message_level,
)


def test_classify_solver_message_flags_handled_solver_failures_as_warning():
    assert classify_solver_message("Failed to converge after 5 iterations.") == "warning"
    assert classify_solver_message("Invalid interval: f(a) and f(b) must have opposite signs.") == "warning"
    assert classify_solver_message("Division by zero (secant line is horizontal).") == "warning"


def test_classify_solver_message_keeps_unknown_messages_as_error():
    assert classify_solver_message("Totally unexpected backend fault") == "error"
    assert classify_solver_message("") == "error"


def test_warning_title_uses_text_marker_not_color_only():
    assert format_log_title("Summary", "warning").startswith("[WARNING] ")
    assert format_log_title("Summary", "error") == "SUMMARY"


def test_explicit_message_level_wins_over_text_matching():
    assert resolve_message_level("warning", "Any future wording is fine.") == "warning"
    assert resolve_message_level("error", "Failed to converge after 5 iterations.") == "error"


def test_message_level_falls_back_to_legacy_text_when_missing():
    assert resolve_message_level(None, "Failed to converge after 5 iterations.") == "warning"
    assert resolve_message_level("", "totally unknown issue") == "error"
