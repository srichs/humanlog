import humanlog.detect as detect


def test_is_ci_when_known_ci_var_present(monkeypatch) -> None:
    monkeypatch.setenv("CI", "1")
    assert detect.is_ci() is True


def test_is_ci_false_when_no_ci_vars(monkeypatch) -> None:
    for key in ("CI", "GITHUB_ACTIONS", "GITLAB_CI", "BUILDKITE"):
        monkeypatch.delenv(key, raising=False)
    assert detect.is_ci() is False


def test_can_animate_depends_on_tty_and_ci(monkeypatch) -> None:
    monkeypatch.setattr(detect, "is_tty", lambda: True)
    monkeypatch.setattr(detect, "is_ci", lambda: False)
    assert detect.can_animate() is True

    monkeypatch.setattr(detect, "is_ci", lambda: True)
    assert detect.can_animate() is False
