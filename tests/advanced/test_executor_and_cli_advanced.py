from types import SimpleNamespace

from click.testing import CliRunner

from src.cli.main import cli
from src.self_improving.executor import SelfImprovementExecutor


def test_executor_runs_project_tests_directory(monkeypatch):
    executor = SelfImprovementExecutor()

    captured = {}

    def fake_run(cmd, cwd, capture_output, text, timeout):
        captured["cmd"] = cmd
        captured["cwd"] = cwd
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr("src.self_improving.executor.subprocess.run", fake_run)

    result = executor._run_tests()

    assert result["passed"] is True
    assert captured["cwd"] == "/home/workspace/personai"
    assert captured["cmd"][:4] == ["python", "-m", "pytest", "/home/workspace/personai/tests"]


def _stub_orchestrator():
    class StubOrchestrator:
        def get_status(self):
            return {
                "total_revenue": 123.45,
                "enabled_models": 1,
                "total_models": 2,
                "models": {
                    "automation_agency": {
                        "enabled": True,
                        "status": "active",
                        "total_revenue": 120.00,
                        "allocation": 20.0,
                    },
                    "micro_saas": {
                        "enabled": False,
                        "status": "idle",
                        "total_revenue": 3.45,
                        "allocation": 0.0,
                    },
                },
            }

        def execute_all(self):
            return [
                SimpleNamespace(model="automation_agency", amount=12.0, success=True, error=None),
                SimpleNamespace(model="micro_saas", amount=0.0, success=False, error="disabled"),
            ]

        def get_report(self):
            return SimpleNamespace(
                timestamp=SimpleNamespace(isoformat=lambda: "2026-03-17T18:00:00"),
                total_revenue=123.45,
                active_models=1,
                summary={"ok": True},
            )

    return StubOrchestrator()


def test_cli_status_revenue_and_report_commands(monkeypatch):
    monkeypatch.setattr("src.cli.main.create_orchestrator", _stub_orchestrator)
    runner = CliRunner()

    status = runner.invoke(cli, ["status"])
    assert status.exit_code == 0
    assert "PersonAI Status" in status.output
    assert "Total Revenue: $123.45" in status.output

    revenue = runner.invoke(cli, ["revenue"])
    assert revenue.exit_code == 0
    assert "Revenue Generation Results" in revenue.output
    assert "automation_agency: $12.00" in revenue.output

    report = runner.invoke(cli, ["report"])
    assert report.exit_code == 0
    assert "Revenue Report" in report.output
    assert "Total Revenue: $123.45" in report.output
