from __future__ import annotations

import os
import sys


def is_ci() -> bool:
    """Return True when running in a known CI environment."""
    return any(
        key in os.environ
        for key in (
            "CI",
            "GITHUB_ACTIONS",
            "GITLAB_CI",
            "BUILDKITE",
        )
    )


def is_tty() -> bool:
    """Return True when stdout behaves like a TTY."""
    return sys.stdout.isatty()


def is_dumb_terminal() -> bool:
    """Return True when the current terminal does not support cursor control."""
    return os.environ.get("TERM", "").lower() == "dumb"


def can_animate() -> bool:
    """Return True when single-line animation is safe and readable."""
    return is_tty() and not is_ci() and not is_dumb_terminal()
