from __future__ import annotations

from typing import Any, Dict, List, Optional


VERIFICATION_SCHEMA_VERSION = "verification.v1"


def build_verification_payload(
    status: str,
    summary: str,
    checks: List[Dict[str, Any]],
    can_export: bool = True,
) -> Dict[str, Any]:
    """Create a stable, serializable verification payload for solver/UI contracts."""
    normalized_status = (status or "").strip().lower()
    if normalized_status not in {"success", "warning", "error"}:
        normalized_status = "warning"

    sanitized_checks: List[Dict[str, Any]] = []
    for check in checks or []:
        sanitized_checks.append(
            {
                "label": str(check.get("label", "")).strip() or "Check",
                "value": _to_serializable_scalar(check.get("value")),
                "detail": str(check.get("detail", "")).strip(),
            }
        )

    return {
        "schema_version": VERIFICATION_SCHEMA_VERSION,
        "status": normalized_status,
        "summary": str(summary or "").strip(),
        "checks": sanitized_checks,
        "can_export": bool(can_export),
    }


def format_verification_block(payload: Optional[Dict[str, Any]]) -> str:
    """Format verification payload into UI-friendly plain text (no color-only meaning)."""
    if not isinstance(payload, dict):
        return "Status: WARNING\nVerification data unavailable.\nExport Ready: No"

    status = str(payload.get("status", "warning")).strip().upper() or "WARNING"
    summary = str(payload.get("summary", "")).strip() or "No verification summary was provided."
    checks = payload.get("checks") if isinstance(payload.get("checks"), list) else []
    can_export = bool(payload.get("can_export"))

    lines: List[str] = [f"Status: {status}", summary]
    for check in checks:
        label = str(check.get("label", "Check")).strip() or "Check"
        value = _format_value(check.get("value"))
        detail = str(check.get("detail", "")).strip()
        if detail:
            lines.append(f"- {label}: {value} ({detail})")
        else:
            lines.append(f"- {label}: {value}")

    lines.append(f"Export Ready: {'Yes' if can_export else 'No'}")
    return "\n".join(lines)


def _to_serializable_scalar(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, bool, int, float)):
        return value
    try:
        return float(value)
    except (TypeError, ValueError):
        return str(value)


def _format_value(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, float):
        return f"{value:.6g}"
    if value is None:
        return "n/a"
    return str(value)
