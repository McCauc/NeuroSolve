from pathlib import Path

import pytest

from src.ui.app import NeuroSolveApp
from src.ui.app_metadata import APP_MILESTONE, APP_NAME, APP_VERSION
from src.utils.report_export import (
    ExportError,
    build_default_report_filename,
    build_report_model,
    normalize_export_format,
    write_report,
)


def _sample_context(**overrides):
    context = {
        "expr_str": "x**2 - 4",
        "method_label": "Secant",
        "input_values": {"x0": 1.0, "x1": 3.0, "tol": 1e-5, "max_iter": 50},
        "result": {
            "root": 2.0,
            "converged": True,
            "iterations": 5,
            "history": [
                {"n": 0, "x_n": 1.0, "f(x_n)": -3.0, "error": None, "explanation": "First estimate."},
                {"n": 1, "x_n": 3.0, "f(x_n)": 5.0, "error": None, "explanation": "Second estimate."},
                {"n": 2, "x_n": 2.0, "f(x_n)": 0.0, "error": 0.0, "explanation": "Root estimate."},
            ],
            "error_msg": "",
        },
        "verification": {
            "schema_version": "verification.v1",
            "status": "success",
            "summary": "Residual and step-size checks passed.",
            "checks": [{"label": "Residual |f(x*)|", "value": 0.0, "detail": "Exact root."}],
            "can_export": True,
        },
        "timestamp": "2026-04-30T12:00:00+00:00",
        "outcome_state": "success",
        "outcome_summary": "The Root Finder protocol successfully converged.",
        "export_enabled": True,
    }
    context.update(overrides)
    return context


def test_report_model_has_header_metadata_and_required_section_order():
    model = build_report_model(_sample_context())

    assert model["header"]["project_name"] == APP_NAME
    assert model["header"]["version"] == APP_VERSION
    assert model["header"]["milestone"] == APP_MILESTONE
    assert model["header"]["method"] == "Secant"
    assert [section["heading"] for section in model["sections"]] == [
        "GIVEN",
        "METHOD",
        "STEPS",
        "FINAL",
        "VERIFICATION",
        "SUMMARY",
    ]
    verification = next(section for section in model["sections"] if section["heading"] == "VERIFICATION")
    assert "Residual and step-size checks passed." in verification["content"]
    assert "Export Ready: Yes" in verification["content"]


def test_report_model_uses_method_specific_bisection_labels():
    model = build_report_model(
        _sample_context(
            method_label="Bisection",
            input_values={"a": 1.0, "b": 3.0, "tol": 1e-5, "max_iter": 50},
        )
    )

    given = next(section for section in model["sections"] if section["heading"] == "GIVEN")
    assert "a = 1.0" in given["content"]
    assert "b = 3.0" in given["content"]
    assert "x0" not in given["content"]


def test_report_model_says_when_verification_is_missing():
    model = build_report_model(_sample_context(verification=None))

    verification = next(section for section in model["sections"] if section["heading"] == "VERIFICATION")
    assert "Verification data unavailable." in verification["content"]
    assert "Export Ready: No" in verification["content"]


def test_default_filename_and_format_normalization_are_consistent():
    context = _sample_context(timestamp="2026-04-30T12:13:14+00:00")

    assert normalize_export_format("TXT") == "txt"
    assert build_default_report_filename(context, "html") == "neurosolve-secant-20260430-121314.html"
    with pytest.raises(ExportError):
        normalize_export_format("docx")


def test_write_report_outputs_txt_html_and_pdf(tmp_path):
    model = build_report_model(_sample_context())

    txt_path = tmp_path / "report.txt"
    html_path = tmp_path / "report.html"
    pdf_path = tmp_path / "report.pdf"

    write_report(model, txt_path, "txt")
    write_report(model, html_path, "html")
    write_report(model, pdf_path, "pdf")

    assert "GIVEN" in txt_path.read_text(encoding="utf-8")
    assert "<h2>VERIFICATION</h2>" in html_path.read_text(encoding="utf-8")
    assert pdf_path.read_bytes().startswith(b"%PDF")
    pdf_text = pdf_path.read_bytes().decode("latin-1", errors="ignore")
    assert "Version:" in pdf_text
    assert "GIVEN" in pdf_text
    assert "VERIFICATION" in pdf_text


def test_write_report_rejects_unsupported_format(tmp_path):
    model = build_report_model(_sample_context())

    with pytest.raises(ExportError):
        write_report(model, tmp_path / "report.docx", "docx")


def test_missing_context_fails_clearly():
    with pytest.raises(ExportError, match="No solve context"):
        build_report_model(None)


def test_stale_export_snapshot_cannot_replace_active_context():
    app = object.__new__(NeuroSolveApp)
    app._active_solve_session = 2
    app._export_snapshot = {"expr_str": "fresh"}

    NeuroSolveApp._store_export_snapshot_if_current(app, 1, {"expr_str": "stale"})

    assert app._export_snapshot == {"expr_str": "fresh"}


def test_current_export_snapshot_replaces_active_context():
    app = object.__new__(NeuroSolveApp)
    app._active_solve_session = 2
    app._export_snapshot = None

    NeuroSolveApp._store_export_snapshot_if_current(app, 2, {"expr_str": "fresh"})

    assert app._export_snapshot == {"expr_str": "fresh"}


class _DummyMainContent:
    def __init__(self):
        self.messages = []

    def log_export_status(self, message, style="normal"):
        self.messages.append((message, style))


def test_export_success_logs_and_shows_messagebox(monkeypatch, tmp_path):
    app = object.__new__(NeuroSolveApp)
    app.main_content = _DummyMainContent()
    shown = []
    final_path = tmp_path / "report.pdf"

    monkeypatch.setattr(
        "src.ui.app.messagebox.showinfo",
        lambda title, message, parent=None: shown.append((title, message, parent)),
    )

    NeuroSolveApp._handle_export_success(app, final_path)

    assert app.main_content.messages == [(f"Export successful. Report saved: {final_path}", "success")]
    assert shown == [
        (
            "Export Successful",
            f"Solution trail report saved successfully:\n{final_path}",
            app,
        )
    ]
