from src.self_improving.executor import SelfImprovementExecutor


def test_detect_issues_finds_bare_except_but_skips_self_improving_path():
    ex = SelfImprovementExecutor()
    code = "try:\n    x = 1\nexcept:\n    pass\n"

    issues = ex._detect_issues(code, "/tmp/sample.py")
    descriptions = [i["description"] for i in issues]

    assert any("Bare except" in d for d in descriptions)
    assert any("Empty except block" in d for d in descriptions)

    skipped = ex._detect_issues(code, "/home/workspace/personai/src/self_improving/runner.py")
    assert skipped == []
