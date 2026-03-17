from src.core.state import AgentState, StateManager


def test_state_manager_defaults_and_snapshot():
    state = StateManager()
    snap = state.snapshot()

    assert snap.agent_state == AgentState.IDLE
    assert snap.current_task is None
    assert snap.revenue_today == 0.0
    assert snap.improvements_made == 0


def test_add_goal_orders_by_priority_and_complete_goal():
    state = StateManager()
    state.add_goal("low", priority=1)
    state.add_goal("high", priority=10)

    goals = state.get("goals")
    assert goals[0]["goal"] == "high"
    assert goals[1]["goal"] == "low"

    state.complete_goal("high")
    goals = state.get("goals")
    high = next(g for g in goals if g["goal"] == "high")
    assert high["completed"] is True
    assert "completed_at" in high


def test_to_json_serializes_enum_and_datetime():
    state = StateManager()
    state.update("agent_state", AgentState.INITIALIZING)
    payload = state.to_json()

    assert '"agent_state": "initializing"' in payload
    assert '"uptime_start":' in payload
