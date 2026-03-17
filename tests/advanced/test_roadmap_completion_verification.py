import json

from src.planning.roadmap import Roadmap


def _phase_map(phases):
    by_name = {}
    for phase in phases:
        name = phase.get("name", "")
        by_name[name] = {
            "by_name": {t.get("name", ""): t.get("status") for t in phase.get("tasks", [])},
            "by_id": {t.get("id", ""): t.get("status") for t in phase.get("tasks", [])},
        }
    return by_name


def _assert_task_completed(phase_payload, task_id: str, fallback_name: str):
    by_id = phase_payload.get("by_id", {})
    by_name = phase_payload.get("by_name", {})

    if task_id in by_id:
        assert by_id.get(task_id) == "completed"
        return

    assert by_name.get(fallback_name) == "completed"


def test_phase_1_and_2_completed_items_match_roadmap_json():
    roadmap = Roadmap()
    phase_tasks = _phase_map(roadmap.phases)

    foundation = next((v for k, v in phase_tasks.items() if "Foundation" in k), {})
    planning = next((v for k, v in phase_tasks.items() if "Planning" in k), {})

    expected_foundation = [
        ("core_state_management", "Core state management"),
        ("memory_system_persistent", "Memory system - Persistent conversation storage"),
        ("self_driven_nlp", "Self-driven NLP - Pure Python NLP without external APIs"),
        ("agent_system_supervisor", "Agent system - Supervisor, researcher, coder agents"),
        ("revenue_models_7", "Revenue models - 7 core AI revenue models"),
        ("self_improvement_engine", "Self-improvement engine - Autonomous code improvement"),
        ("consciousness_heartbeat", "Consciousness/Heartbeat - Autonomous thinking system"),
        ("controller_main", "Main controller - Orchestration of all systems"),
    ]
    expected_planning = [
        ("roadmap_tracker_json", "Roadmap tracker - JSON-based progress tracking"),
        ("planning_loop_main", "Planning loop - Main execution loop"),
        ("improvement_cycle_self", "Improvement cycle - Self-improvement orchestration"),
    ]

    for task_id, fallback_name in expected_foundation:
        _assert_task_completed(foundation, task_id, fallback_name)

    for task_id, fallback_name in expected_planning:
        _assert_task_completed(planning, task_id, fallback_name)


def test_completed_count_in_status_summary_matches_roadmap_data_file():
    roadmap = Roadmap()
    summary = roadmap.get_status_summary()

    with open("/home/workspace/personai/data/roadmap.json", "r") as f:
        raw = json.load(f)

    assert summary["completed"] == raw["completed"]