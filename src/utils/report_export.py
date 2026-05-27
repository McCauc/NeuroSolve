from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from html import escape
from pathlib import Path
import re
from typing import Any, Dict, Iterable, List, Mapping

from src.ui.app_metadata import APP_MILESTONE, APP_NAME, APP_VERSION
from src.utils.verification import format_verification_block


SUPPORTED_EXPORT_FORMATS = ("txt", "html", "pdf")
REPORT_SECTION_ORDER = ("GIVEN", "METHOD", "STEPS", "FINAL", "VERIFICATION", "SUMMARY")


class ExportError(RuntimeError):
    """Raised when a report export cannot be completed safely."""


def normalize_export_format(format_name: str) -> str:
    normalized = (format_name or "").strip().lower().lstrip(".")
    if normalized not in SUPPORTED_EXPORT_FORMATS:
        raise ExportError(f"Unsupported export format: {format_name or 'unknown'}")
    return normalized


def build_default_report_filename(context: Mapping[str, Any], format_name: str) -> str:
    extension = normalize_export_format(format_name)
    method = _slugify(str(context.get("method_label") or "solve"))
    timestamp = _parse_timestamp(context.get("timestamp"))
    return f"neurosolve-{method}-{timestamp.strftime('%Y%m%d-%H%M%S')}.{extension}"


def build_report_model(context: Mapping[str, Any]) -> Dict[str, Any]:
    """Convert a persisted solve context into a serializable report model."""
    if not isinstance(context, Mapping):
        raise ExportError("No solve context is available to export.")

    result = context.get("result") if isinstance(context.get("result"), Mapping) else {}
    verification = context.get("verification") if isinstance(context.get("verification"), Mapping) else None
    root = result.get("root")
    iterations = result.get("iterations", 0)
    converged = bool(result.get("converged"))
    outcome_summary = str(context.get("outcome_summary") or _default_outcome_summary(result)).strip()

    header = {
        "project_name": APP_NAME,
        "version": APP_VERSION,
        "milestone": APP_MILESTONE,
        "timestamp": _parse_timestamp(context.get("timestamp")).isoformat(),
        "method": str(context.get("method_label") or result.get("method") or "Unknown"),
        "inputs": deepcopy(context.get("input_values") or {}),
        "root": root,
        "convergence_state": "converged" if converged else "not converged",
        "iterations": iterations,
        "outcome_summary": outcome_summary,
    }

    sections = [
        {"heading": "GIVEN", "content": _format_given(context)},
        {"heading": "METHOD", "content": _format_method(header["method"])},
        {"heading": "STEPS", "content": _format_steps(result.get("history"))},
        {"heading": "FINAL", "content": _format_final(root, converged, iterations, result.get("error_msg"))},
        {"heading": "VERIFICATION", "content": format_verification_block(verification)},
        {"heading": "SUMMARY", "content": outcome_summary},
    ]

    return {"header": header, "sections": sections}


def write_report(model: Mapping[str, Any], file_path: str | Path, format_name: str) -> Path:
    extension = normalize_export_format(format_name)
    path = Path(file_path)
    if path.suffix.lower() != f".{extension}":
        path = path.with_suffix(f".{extension}")

    try:
        if extension == "txt":
            path.write_text(render_txt_report(model), encoding="utf-8")
        elif extension == "html":
            path.write_text(render_html_report(model), encoding="utf-8")
        elif extension == "pdf":
            _write_pdf_report(model, path)
    except OSError as exc:
        raise ExportError(f"Could not write report file: {exc}") from exc

    return path


def render_txt_report(model: Mapping[str, Any]) -> str:
    header = model.get("header", {})
    lines = [
        str(header.get("project_name", APP_NAME)),
        f"Version: {header.get('version', APP_VERSION)}",
        f"Milestone: {header.get('milestone', APP_MILESTONE)}",
        f"Timestamp: {header.get('timestamp', 'n/a')}",
        f"Method: {header.get('method', 'Unknown')}",
        f"Inputs: {_format_inputs(header.get('inputs'))}",
        f"Root: {_format_scalar(header.get('root'))}",
        f"Convergence State: {header.get('convergence_state', 'unknown')}",
        f"Iterations: {header.get('iterations', 0)}",
        f"Outcome Summary: {header.get('outcome_summary', '')}",
        "",
    ]
    for section in _ordered_sections(model.get("sections", [])):
        lines.extend([section["heading"], "-" * len(section["heading"]), section["content"], ""])
    return "\n".join(lines).rstrip() + "\n"


def render_html_report(model: Mapping[str, Any]) -> str:
    header = model.get("header", {})
    rows = [
        ("Project", header.get("project_name", APP_NAME)),
        ("Version", header.get("version", APP_VERSION)),
        ("Milestone", header.get("milestone", APP_MILESTONE)),
        ("Timestamp", header.get("timestamp", "n/a")),
        ("Method", header.get("method", "Unknown")),
        ("Inputs", _format_inputs(header.get("inputs"))),
        ("Root", _format_scalar(header.get("root"))),
        ("Convergence State", header.get("convergence_state", "unknown")),
        ("Iterations", header.get("iterations", 0)),
        ("Outcome Summary", header.get("outcome_summary", "")),
    ]
    metadata = "\n".join(
        f"<tr><th>{escape(str(label))}</th><td>{escape(str(value))}</td></tr>" for label, value in rows
    )
    sections = "\n".join(
        f"<section><h2>{escape(section['heading'])}</h2><pre>{escape(section['content'])}</pre></section>"
        for section in _ordered_sections(model.get("sections", []))
    )
    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head><meta charset=\"utf-8\"><title>NeuroSolve Report</title>"
        "<style>body{font-family:Arial,sans-serif;line-height:1.45;max-width:900px;margin:32px auto;padding:0 20px;}"
        "table{border-collapse:collapse;width:100%;margin-bottom:24px;}th,td{border:1px solid #111;padding:8px;text-align:left;}"
        "pre{white-space:pre-wrap;background:#f7f7f7;border:1px solid #111;padding:12px;}</style></head>\n"
        f"<body><h1>{escape(str(header.get('project_name', APP_NAME)))} Solution Trail Report</h1>"
        f"<table>{metadata}</table>{sections}</body></html>\n"
    )


def _write_pdf_report(model: Mapping[str, Any], path: Path) -> None:
    try:
        from fpdf import FPDF
        from fpdf.enums import XPos, YPos
    except ImportError as exc:
        raise ExportError("PDF export requires fpdf2. Install requirements.txt and try again.") from exc

    pdf = FPDF()
    pdf.set_compression(False)
    pdf.set_margins(left=16, top=16, right=16)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(
        pdf.epw,
        10,
        "NeuroSolve Solution Trail Report",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    for line in render_txt_report(model).splitlines():
        safe_line = line.encode("latin-1", "replace").decode("latin-1") or " "
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(
            pdf.epw,
            6,
            safe_line,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
            wrapmode="CHAR",
        )
    pdf.output(str(path))


def _format_given(context: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            f"Function: f(x) = {context.get('expr_str', 'n/a')}",
            f"Inputs: {_format_inputs(context.get('input_values'))}",
        ]
    )


def _format_method(method: str) -> str:
    label = str(method or "Unknown").strip() or "Unknown"
    return f"{label}\nAlgorithm Initialized."


def _format_steps(history: Any) -> str:
    if not isinstance(history, list) or not history:
        return "No iteration history was recorded."

    lines: List[str] = []
    for index, step in enumerate(history, start=1):
        if not isinstance(step, Mapping):
            continue
        lines.append(f"STEP {index:02d}")
        explanation = str(step.get("explanation") or "No explanation provided.").strip()
        lines.append(explanation)
        lines.append(f"x_curr: {_format_scalar(step.get('x_n'))}")
        lines.append(f"f(x): {_format_scalar(step.get('f(x_n)'))}")
        lines.append(f"error: {_format_scalar(step.get('error'))}")
        lines.append("")
    return "\n".join(lines).rstrip()


def _format_final(root: Any, converged: bool, iterations: Any, error_msg: Any) -> str:
    if root is not None:
        prefix = "Root bounded" if converged else "Latest estimate"
        return f"{prefix} at x = {_format_scalar(root)} after {iterations} iterations."
    message = str(error_msg or "").strip()
    if message:
        return f"No final root was produced.\n{message}"
    return "No final root was produced."


def _default_outcome_summary(result: Mapping[str, Any]) -> str:
    if result.get("converged"):
        return f"The Root Finder protocol converged after {result.get('iterations', 0)} mathematical steps."
    message = str(result.get("error_msg") or "The run did not converge.").strip()
    return message


def _ordered_sections(sections: Iterable[Mapping[str, Any]]) -> List[Dict[str, str]]:
    by_heading = {str(section.get("heading", "")).upper(): section for section in sections if isinstance(section, Mapping)}
    ordered: List[Dict[str, str]] = []
    for heading in REPORT_SECTION_ORDER:
        section = by_heading.get(heading, {})
        ordered.append({"heading": heading, "content": str(section.get("content", "")).strip()})
    return ordered


def _format_inputs(inputs: Any) -> str:
    if not isinstance(inputs, Mapping) or not inputs:
        return "n/a"
    return " | ".join(f"{key} = {_format_scalar(value)}" for key, value in inputs.items())


def _format_scalar(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        if value.is_integer():
            return f"{value:.1f}"
        return f"{value:.8g}"
    return str(value)


def _parse_timestamp(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except ValueError:
            pass
    return datetime.now().astimezone()


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "solve"
