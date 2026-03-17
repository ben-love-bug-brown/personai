import asyncio

from src.core.controller import PersonAIController
from src.core.state import AgentState


def test_controller_initialize_sets_system_flags_and_state_idle():
    controller = PersonAIController()
    asyncio.run(controller.initialize())

    state = controller.state.get_all()
    assert state.get("revenue_initialized") is True
    assert state.get("improver_initialized") is True
    assert state.get("agent_state") == AgentState.IDLE
