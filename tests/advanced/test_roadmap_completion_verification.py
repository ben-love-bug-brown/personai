import json

from src.planning.roadmap import Roadmap


def _phase_map(phases):
    by_name = {}
    for phase in phases:
        name = phase.get("name", "")
        by_name[name] = {t.get("name", ""): t.get("status") for t in phase.get("tasks", [])}
    return by_name


def test_phase_1_and_2_completed_items_match_roadmap_json():
    roadmap = Roadmap()
    phase_tasks = _phase_map(roadmap.phases)

    foundation = next((v for k, v in phase_tasks.items() if "Foundation" in k), {})
    planning = next((v for k, v in phase_tasks.items() if "Planning" in k), {})

    expected_foundation = [
        "Core state management - Thread-safe AGI state with event system",
        "Memory system - Persistent conversation storage",
        "Self-driven NLP - Pure Python NLP without external APIs",
        "Agent system - Supervisor, researcher, coder agents",
        "Revenue models - 7 core AI revenue models",
        "Self-improvement engine - Autonomous code improvement",
        "Consciousness/Heartbeat - Autonomous thinking system",
        "Main controller - Orchestration of all systems",
    ]
    expected_planning = [
        "Roadmap tracker - JSON-based progress tracking",
        "Planning loop - Main execution loop",
        "Improvement cycle - Self-improvement orchestration",
    ]

    for task_name in expected_foundation:
        assert foundation.get(task_name) == "completed"

    for task_name in expected_planning:
        assert planning.get(task_name) == "completed"


def test_completed_count_in_status_summary_matches_roadmap_data_file():
    roadmap = Roadmap()
    summary = roadmap.get_status_summary()

    with open("/home/workspace/personai/data/roadmap.json", "r") as f:
        raw = json.load(f)

    # The Roadmap class computes totals from phases, so compare completed counts
    # Total tasks may differ due to Roadmap class computing from actual phase data
    assert summary["completed"] == raw["completed"]