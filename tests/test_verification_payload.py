from src.solvers.bisection_method import solve_bisection_method
from src.solvers.secant_method import solve_secant_method
from src.ui.app import NeuroSolveApp
from src.ui.components.main_content import MainContentFrame
from src.utils.verification import format_verification_block


def test_secant_success_includes_structured_verification_payload():
    result = solve_secant_method(lambda x: x**2 - 4.0, x0=1.0, x1=3.0, tol=1e-5)

    verification = result["verification"]
    assert verification["schema_version"] == "verification.v1"
    assert verification["status"] == "success"
    assert verification["can_export"] is True
    assert isinstance(verification["checks"], list)
    assert any(check["label"] == "Residual |f(x*)|" for check in verification["checks"])
    assert any(check["label"] == "Step Size |Δx|" for check in verification["checks"])


def test_bisection_non_converged_still_reports_verification_evidence():
    result = solve_bisection_method(lambda x: x**3 - 2.0, a=1.0, b=2.0, tol=1e-12, max_iter=2)

    verification = result["verification"]
    assert result["converged"] is False
    assert verification["status"] == "warning"
    assert any(check["label"] == "Residual |f(mid)|" for check in verification["checks"])
    assert any(check["label"] == "Bracket Width" for check in verification["checks"])


def test_invalid_interval_has_no_trustworthy_estimate_verification_summary():
    result = solve_bisection_method(lambda x: x**2 + 1.0, a=-1.0, b=1.0)

    verification = result["verification"]
    assert result["root"] is None
    assert verification["status"] == "warning"
    assert "no trustworthy estimate exists" in verification["summary"].lower()


def test_initial_evaluation_failure_has_no_estimate_verification_summary():
    def bad_func(x):
        if x > 2.0:
            raise ValueError("Domain error simulated")
        return x

    result = solve_secant_method(bad_func, x0=1.0, x1=3.0)

    verification = result["verification"]
    assert result["root"] is None
    assert verification["status"] == "warning"
    assert "no trustworthy estimate exists" in verification["summary"].lower()


def test_format_verification_block_includes_textual_status_and_checks():
    payload = {
        "schema_version": "verification.v1",
        "status": "warning",
        "summary": "Residual is small but max iterations were reached.",
        "checks": [
            {"label": "Residual |f(x*)|", "value": 1.2e-06, "detail": "Computed at final estimate x*=1.4142."},
            {"label": "Step Size |Δx|", "value": 0.004, "detail": "Latest step remains above tolerance."},
        ],
        "can_export": True,
    }

    text = format_verification_block(payload)
    assert "Status: WARNING" in text
    assert "Residual |f(x*)|: 1.2e-06" in text
    assert "Latest step remains above tolerance." in text
    assert "Export Ready: Yes" in text


class _DummyWidget:
    def __init__(self):
        self.calls = []

    def configure(self, **kwargs):
        self.calls.append(kwargs)


def test_main_content_success_uses_structured_verification_payload():
    frame = object.__new__(MainContentFrame)
    trail = []
    frame.add_step = lambda heading, content, style="normal": trail.append((heading, content, style))
    frame.result_frame = _DummyWidget()
    frame.result_value = _DummyWidget()
    frame.result_status = _DummyWidget()

    verification = {
        "schema_version": "verification.v1",
        "status": "success",
        "summary": "Residual and step-size checks passed.",
        "checks": [{"label": "Residual |f(x*)|", "value": 0.0, "detail": "Exact root."}],
        "can_export": True,
    }
    MainContentFrame.update_success(frame, root=2.0, iterations=4, verification=verification)

    verification_steps = [entry for entry in trail if entry[0] == "VERIFICATION"]
    assert len(verification_steps) == 1
    assert "Residual and step-size checks passed." in verification_steps[0][1]
    assert "Status: SUCCESS" in verification_steps[0][1]


def test_main_content_warning_uses_structured_verification_payload():
    frame = object.__new__(MainContentFrame)
    trail = []
    frame.add_step = lambda heading, content, style="normal": trail.append((heading, content, style))
    frame.result_frame = _DummyWidget()
    frame.result_value = _DummyWidget()
    frame.result_status = _DummyWidget()

    verification = {
        "schema_version": "verification.v1",
        "status": "warning",
        "summary": "No trustworthy estimate exists for this run.",
        "checks": [{"label": "Estimate Available", "value": False, "detail": "Endpoint check failed."}],
        "can_export": True,
    }
    MainContentFrame.update_error(
        frame,
        message="Invalid interval: f(a) and f(b) must have opposite signs.",
        root_so_far=None,
        total_iters=0,
        message_level="warning",
        verification=verification,
    )

    verification_steps = [entry for entry in trail if entry[0] == "VERIFICATION"]
    assert len(verification_steps) == 1
    assert "No trustworthy estimate exists for this run." in verification_steps[0][1]
    assert "Status: WARNING" in verification_steps[0][1]


class _DummyMainContent:
    def __init__(self):
        self.draw_calls = []

    def draw_graph(self, x_curve, y_curve, history):
        self.draw_calls.append((x_curve, y_curve, history))


def test_generate_and_draw_graph_ignores_stale_solve_session():
    app = object.__new__(NeuroSolveApp)
    app._active_solve_session = 2
    app.main_content = _DummyMainContent()

    result = {"history": [{"x_n": 1.0}, {"x_n": 2.0}]}
    NeuroSolveApp._NeuroSolveApp__generate_and_draw_graph(
        app,
        func=lambda x: x**2 - 4.0,
        x0=1.0,
        x1=3.0,
        result=result,
        solve_session_id=1,
    )

    assert app.main_content.draw_calls == []


def test_generate_and_draw_graph_renders_for_active_solve_session():
    app = object.__new__(NeuroSolveApp)
    app._active_solve_session = 3
    app.main_content = _DummyMainContent()

    result = {"history": [{"x_n": 1.0}, {"x_n": 2.0}]}
    NeuroSolveApp._NeuroSolveApp__generate_and_draw_graph(
        app,
        func=lambda x: x**2 - 4.0,
        x0=1.0,
        x1=3.0,
        result=result,
        solve_session_id=3,
    )

    assert len(app.main_content.draw_calls) == 1
