from __future__ import annotations

import os
import sys


_CI_ENV_VARS = (
    "CI",
    "GITHUB_ACTIONS",
    "GITLAB_CI",
    "BUILDKITE",
    "CIRCLECI",
    "JENKINS_URL",
    "TF_BUILD",
)


def is_ci() -> bool:
    """Return True when running in a known CI environment."""
    return any(key in os.environ for key in _CI_ENV_VARS)


def is_tty() -> bool:
    """Return True when stdout behaves like a TTY."""
    stream = getattr(sys, "stdout", None)
    isatty = getattr(stream, "isatty", None)
    return bool(callable(isatty) and isatty())


def is_dumb_terminal() -> bool:
    """Return True when the current terminal does not support cursor control."""
    return os.environ.get("TERM", "").lower() == "dumb"


def is_animation_disabled() -> bool:
    """Return True when environment configuration explicitly disables animation."""
    disabled_vars = {"HUMANLOG_NO_ANIMATE", "NO_COLOR"}
    return any(var in os.environ for var in disabled_vars)


def can_animate() -> bool:
    """Return True when single-line animation is safe and readable."""
    return all(
        (
            is_tty(),
            not is_ci(),
            not is_dumb_terminal(),
            not is_animation_disabled(),
        )
    )
