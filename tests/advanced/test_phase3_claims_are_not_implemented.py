from pathlib import Path

from src.planning.roadmap import Roadmap


def _phase3_tasks(roadmap):
    phase3 = next((p for p in roadmap.phases if "Web UI & API" in p.get("name", "")), None)
    return {t.get("name", ""): t.get("status") for t in (phase3 or {}).get("tasks", [])}


def test_phase3_completed_claims_do_not_match_project_reality():
    roadmap = Roadmap()
    phase3 = _phase3_tasks(roadmap)

    for status in phase3.values():
        assert status == "completed"

    root = Path("/home/workspace/personai")

    # Web chat interface file in repo is not present (README points to zo.space URL only)
    assert not (root / "src" / "web").exists()

    # REST API full CRUD claim is not true with current nlp_service endpoints
    # implemented: chat/status/history/roadmap/improve/health (no CRUD resources)
    nlp_service = (root / "src" / "api" / "nlp_service.py").read_text()
    assert "add_post('/chat'" in nlp_service
    assert "add_get('/status'" in nlp_service
    assert "add_get('/history'" in nlp_service
    assert "add_get('/roadmap'" in nlp_service
    assert "add_post('/improve'" in nlp_service
    assert "add_get('/health'" in nlp_service

    # No service manager implementation in repository source
    service_related = list(root.glob("src/**/service*.py"))
    assert service_related == []

    # No restart endpoint/button implementation in the local project code
    assert "restart" not in nlp_service
