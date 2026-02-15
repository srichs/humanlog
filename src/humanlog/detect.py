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

_ANIMATION_DISABLED_ENV_VARS = (
    "HUMANLOG_NO_ANIMATE",
    "NO_COLOR",
)

_FALSEY_ENV_VALUES = {"", "0", "false", "no", "off"}


def _is_enabled_env_flag(value: str | None) -> bool:
    """Return True when an environment value should be treated as enabled."""
    if value is None:
        return False
    return value.strip().lower() not in _FALSEY_ENV_VALUES


def is_ci() -> bool:
    """Return True when running in a known CI environment."""
    env = os.environ

    return any(_is_enabled_env_flag(env.get(key)) for key in _CI_ENV_VARS)


def is_tty() -> bool:
    """Return True when stdout behaves like a TTY."""
    stream = getattr(sys, "stdout", None)
    isatty = getattr(stream, "isatty", None)
    if not callable(isatty):
        return False

    try:
        return bool(isatty())
    except (OSError, ValueError):
        # Some stream wrappers can raise when the descriptor is unavailable.
        return False


def is_dumb_terminal() -> bool:
    """Return True when the current terminal does not support cursor control."""
    term = os.environ.get("TERM", "").strip().lower()
    return term == "" or term == "dumb" or term.startswith("dumb-")


def is_animation_disabled() -> bool:
    """Return True when environment configuration explicitly disables animation."""
    env = os.environ
    return any(
        _is_enabled_env_flag(env.get(var)) for var in _ANIMATION_DISABLED_ENV_VARS
    )


def can_animate() -> bool:
    """Return True when single-line animation is safe and readable."""
    return (
        is_tty()
        and not is_ci()
        and not is_dumb_terminal()
        and not is_animation_disabled()
    )
