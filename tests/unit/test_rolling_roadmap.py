import json

from src.self_improving.roadmap import RollingRoadmap


def test_roadmap_loads_existing_items(tmp_path):
    data_file = tmp_path / "roadmap_progress.json"
    data_file.write_text(
        json.dumps(
            {
                "cycles_completed": 3,
                "improvements_made": 5,
                "items": [
                    {
                        "id": "a",
                        "phase": "Self-Improvement",
                        "task": "Fix x",
                        "status": "completed",
                        "priority": 9,
                        "completed_at": "2026-03-17T10:00:00",
                        "notes": "done",
                        "blockers": [],
                        "dependencies": [],
                    },
                    {
                        "id": "b",
                        "phase": "Quality Assurance",
                        "task": "Write tests",
                        "status": "pending",
                        "priority": 8,
                    },
                ],
            }
        )
    )

    roadmap = RollingRoadmap(data_path=str(data_file))

    assert roadmap.cycles_completed == 3
    assert roadmap.improvements_made == 5
    assert len(roadmap.items) == 2
    assert roadmap.items[0].id == "a"
    assert roadmap.items[1].task == "Write tests"


def test_get_next_items_returns_highest_priority_pending(tmp_path):
    data_file = tmp_path / "roadmap_progress.json"
    roadmap = RollingRoadmap(data_path=str(data_file))

    roadmap.add_item("Phase", "p1", priority=1)
    roadmap.add_item("Phase", "p2", priority=10)
    roadmap.add_item("Phase", "p3", priority=5)

    next_items = roadmap.get_next_items(limit=2)
    assert [i.task for i in next_items] == ["p2", "p3"]
