from typing import Optional


def classify_solver_message(message: Optional[str]) -> str:
    """Classify legacy solver error text when explicit severity is unavailable."""
    normalized = (message or "").strip().lower()
    if not normalized:
        return "error"

    warning_markers = (
        "failed to converge",
        "invalid interval",
        "division by zero",
        "calculation error at x=",
        "error evaluating function at initial guesses",
        "error evaluating function at interval endpoints",
    )
    return "warning" if any(marker in normalized for marker in warning_markers) else "error"


def resolve_message_level(explicit_level: Optional[str], message: Optional[str]) -> str:
    """Prefer explicit solver severity metadata, then fallback to legacy text matching."""
    normalized_level = (explicit_level or "").strip().lower()
    if normalized_level in {"warning", "error"}:
        return normalized_level
    return classify_solver_message(message)


def format_log_title(title: str, style: str) -> str:
    """Add explicit text markers for styles where color alone is insufficient."""
    base = (title or "").upper()
    if style == "warning":
        return f"[WARNING] {base}"
    return base
