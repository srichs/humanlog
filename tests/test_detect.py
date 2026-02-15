import humanlog.detect as detect


def test_is_ci_when_known_ci_var_present(monkeypatch) -> None:
    monkeypatch.setenv("CI", "1")
    assert detect.is_ci() is True


def test_is_ci_false_when_no_ci_vars(monkeypatch) -> None:
    for key in (
        "CI",
        "GITHUB_ACTIONS",
        "GITLAB_CI",
        "BUILDKITE",
        "CIRCLECI",
        "JENKINS_URL",
        "TF_BUILD",
    ):
        monkeypatch.delenv(key, raising=False)
    assert detect.is_ci() is False


def test_is_ci_false_for_falsey_ci_value(monkeypatch) -> None:
    monkeypatch.setenv("CI", "0")
    assert detect.is_ci() is False


def test_is_ci_when_other_supported_provider_var_present(monkeypatch) -> None:
    monkeypatch.setenv("CIRCLECI", "true")
    assert detect.is_ci() is True


def test_is_ci_true_when_provider_var_present_even_if_ci_falsey(monkeypatch) -> None:
    monkeypatch.setenv("CI", "0")
    monkeypatch.setenv("GITHUB_ACTIONS", "1")
    assert detect.is_ci() is True


def test_can_animate_depends_on_tty_and_ci(monkeypatch) -> None:
    monkeypatch.setattr(detect, "is_tty", lambda: True)
    monkeypatch.setattr(detect, "is_ci", lambda: False)
    monkeypatch.setattr(detect, "is_dumb_terminal", lambda: False)
    monkeypatch.setattr(detect, "is_animation_disabled", lambda: False)
    assert detect.can_animate() is True

    monkeypatch.setattr(detect, "is_ci", lambda: True)
    assert detect.can_animate() is False


def test_can_animate_false_for_dumb_terminal(monkeypatch) -> None:
    monkeypatch.setattr(detect, "is_tty", lambda: True)
    monkeypatch.setattr(detect, "is_ci", lambda: False)
    monkeypatch.setattr(detect, "is_dumb_terminal", lambda: True)
    monkeypatch.setattr(detect, "is_animation_disabled", lambda: False)
    assert detect.can_animate() is False


def test_can_animate_false_when_disabled_by_env(monkeypatch) -> None:
    monkeypatch.setattr(detect, "is_tty", lambda: True)
    monkeypatch.setattr(detect, "is_ci", lambda: False)
    monkeypatch.setattr(detect, "is_dumb_terminal", lambda: False)
    monkeypatch.setattr(detect, "is_animation_disabled", lambda: True)
    assert detect.can_animate() is False


def test_is_animation_disabled(monkeypatch) -> None:
    monkeypatch.delenv("HUMANLOG_NO_ANIMATE", raising=False)
    monkeypatch.delenv("NO_COLOR", raising=False)
    assert detect.is_animation_disabled() is False

    monkeypatch.setenv("NO_COLOR", "1")
    assert detect.is_animation_disabled() is True


def test_is_animation_disabled_false_for_falsey_values(monkeypatch) -> None:
    monkeypatch.setenv("HUMANLOG_NO_ANIMATE", "false")
    monkeypatch.setenv("NO_COLOR", "0")
    assert detect.is_animation_disabled() is False
