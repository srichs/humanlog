from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from typing import Any, Optional

from .detect import can_animate
from .render import format_kv, timestamp


@dataclass
class _Step:
    label: str
    start: float


class NiceLog:
    """A tiny logger focused on clean, human-readable progress output."""

    def __init__(self) -> None:
        self._current_step: Optional[_Step] = None

    def step(self, msg: str) -> None:
        """Start a named step and render it immediately."""
        self._end_step_if_any()
        self._current_step = _Step(label=msg, start=time.perf_counter())

        if can_animate():
            print(f"→ {msg} …", end="", flush=True)
        else:
            print(f"[{timestamp()}] → {msg}")

    def done(self, **info: Any) -> None:
        """Finish the active step and render elapsed duration."""
        if not self._current_step:
            return

        elapsed = time.perf_counter() - self._current_step.start
        label = self._current_step.label
        self._current_step = None

        details = {**info, "time": f"{elapsed:.2f}s"}
        suffix = format_kv(**details)

        if can_animate():
            print(f"\r✓ {label}{suffix}")
        else:
            print(f"[{timestamp()}] ✓ {label}{suffix}")

    def info(self, msg: str, **info: Any) -> None:
        """Write an info message and auto-close any pending step."""
        self._end_step_if_any()
        print(f"[{timestamp()}] ℹ {msg}{format_kv(**info)}")

    def warn(self, msg: str, **info: Any) -> None:
        """Write a warning message to stderr."""
        self._end_step_if_any()
        print(f"[{timestamp()}] ⚠ {msg}{format_kv(**info)}", file=sys.stderr)

    def error(self, msg: str, **info: Any) -> None:
        """Write an error message to stderr."""
        self._end_step_if_any()
        print(f"[{timestamp()}] ✖ {msg}{format_kv(**info)}", file=sys.stderr)

    def _end_step_if_any(self) -> None:
        if self._current_step:
            self.done()
