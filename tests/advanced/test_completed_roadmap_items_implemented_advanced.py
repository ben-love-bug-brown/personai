import json
from pathlib import Path

from src.api.nlp_service import create_app


ROOT = Path("/home/workspace/personai")
ROADMAP_JSON = ROOT / "data" / "roadmap.json"


def _completed_tasks_with_files():
    data = json.loads(ROADMAP_JSON.read_text())
    tasks = []
    for phase in data.get("phases", []):
        for task in phase.get("tasks", []):
            if task.get("status") == "completed":
                tasks.append(task)
    return tasks


def test_all_completed_roadmap_tasks_with_local_files_exist():
    tasks = _completed_tasks_with_files()
    missing = []

    for task in tasks:
        file_ref = task.get("file")
        if not file_ref or file_ref == "zo.space route":
            continue
        path = ROOT / file_ref
        if not path.exists():
            missing.append(file_ref)

    assert missing == []


def test_nlp_service_exposes_expected_phase3_routes():
    app = create_app()
    routes = {(r.method, r.resource.canonical) for r in app.router.routes()}

    expected = {
        ("POST", "/chat"),
        ("GET", "/status"),
        ("GET", "/history"),
        ("GET", "/roadmap"),
        ("POST", "/improve"),
        ("GET", "/health"),
    }
    assert expected.issubset(routes)


def test_status_contract_for_web_api_proxy_is_string_state_with_running_flag():
    source = (ROOT / "src" / "api" / "nlp_service.py").read_text()
    assert "'status': 'active' if running else 'stopped'" in source
    assert "'running': running" in source
