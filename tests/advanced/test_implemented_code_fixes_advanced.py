from src.self_improving.executor import ImprovementAction, SelfImprovementExecutor
from src.planning.loop import MainLoop


def test_executor_apply_action_fails_when_old_snippet_not_found(tmp_path):
    target = tmp_path / "sample.py"
    target.write_text("x = 1\n")

    executor = SelfImprovementExecutor()
    action = ImprovementAction(
        id="a1",
        file_path=str(target),
        description="replace missing snippet",
        old_code="y = 2",
        new_code="y = 3",
        reason="safety",
        priority=1.0,
    )

    ok = executor.apply_action(action)

    assert ok is False
    assert action.status == "failed"
    assert "not found" in action.reason.lower()
    assert target.read_text() == "x = 1\n"


def test_executor_apply_action_replaces_only_first_occurrence(tmp_path):
    target = tmp_path / "sample.py"
    target.write_text("print('a')\nprint('a')\n")

    executor = SelfImprovementExecutor()
    action = ImprovementAction(
        id="a2",
        file_path=str(target),
        description="replace first",
        old_code="print('a')",
        new_code="print('b')",
        reason="safety",
        priority=1.0,
    )

    ok = executor.apply_action(action)

    assert ok is True
    assert target.read_text() == "print('b')\nprint('a')\n"


def test_main_loop_file_uses_logger_not_print_statements():
    import src.planning.loop as loop_module

    source = open(loop_module.__file__, "r", encoding="utf-8").read()
    assert "logger = logging.getLogger(__name__)" in source
    assert "print(" not in source
