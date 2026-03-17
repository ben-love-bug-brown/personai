from src.self_improving.main import KeepDiscardManager, ImprovementResult, AutonomousScheduler, create_self_improver


def _result(metric_after: float, status: str = "keep") -> ImprovementResult:
    return ImprovementResult(
        modification="m",
        metric_name="test_pass_rate",
        metric_before=0.0,
        metric_after=metric_after,
        status=status,
        timestamp=0.0,
        duration_seconds=0.0,
    )


def test_keep_discard_keeps_only_meaningful_improvements():
    manager = KeepDiscardManager()

    assert manager.evaluate(_result(0.50), threshold=0.01) == "keep"
    assert manager.evaluate(_result(0.53), threshold=0.01) == "keep"
    assert manager.best_result.metric_after == 0.53

    assert manager.evaluate(_result(0.51), threshold=0.01) == "discard"
    assert manager.best_result.metric_after == 0.53


def test_keep_discard_discards_crash_results():
    manager = KeepDiscardManager()
    assert manager.evaluate(_result(0.50), threshold=0.01) == "keep"
    assert manager.evaluate(_result(0.99, status="crash"), threshold=0.01) == "discard"
    assert manager.best_result.metric_after == 0.50


def test_autonomous_scheduler_run_cycle_gracefully_handles_missing_advisor_module():
    improver = create_self_improver()
    scheduler = AutonomousScheduler(improver)
    scheduler.max_experiments_per_cycle = 2

    result = scheduler.run_cycle()

    assert result["cycle"] == 1
    assert len(result["experiments"]) == 2
    for exp in result["experiments"]:
        assert exp["status"] == "proposed"
        assert "suggestion" in exp
