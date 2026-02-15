from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from typing import Any, Literal, Optional

from .detect import can_animate
from .render import format_kv, timestamp


@dataclass
class _Step:
    label: str
    start: float
    animated: bool


class _StepContext:
    """Context manager that closes the active step on block exit.

    Args:
        logger: The :class:`HumanLog` instance that opened the current step and
            should be finalized when the context exits.
    """

    def __init__(self, logger: "HumanLog") -> None:
        self._logger = logger

    def __enter__(self) -> "HumanLog":
        return self._logger

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> Literal[False]:
        if exc_type is None:
            self._logger.done()
        else:
            details = {"error": exc_type.__name__}
            message = str(exc)
            if message:
                details["message"] = message
            self._logger.fail(**details)
        return False


class HumanLog:
    """A tiny logger focused on clean, human-readable progress output."""

    def __init__(self) -> None:
        self._current_step: Optional[_Step] = None

    def step(self, msg: str) -> _StepContext:
        """Start a named step and return a context manager that auto-completes it.

        Args:
            msg: Human-readable description for the unit of work being started.
                The same label is reused when rendering completion output.
        """
        self._end_step_if_any()
        animated = can_animate()
        self._current_step = _Step(
            label=msg, start=time.perf_counter(), animated=animated
        )

        if animated:
            print(f"→ {msg} …", end="", flush=True)
        else:
            print(f"[{timestamp()}] → {msg}", flush=True)

        return _StepContext(self)

    def done(self, **info: Any) -> None:
        """Finish the active step and render elapsed duration.

        Args:
            **info: Optional metadata emitted as key/value pairs in the final
                log line (for example ``items=10`` or ``path="out.txt"``).
        """
        self._complete_step(symbol="✓", **info)

    def fail(self, **info: Any) -> None:
        """Finish the active step as failed and render elapsed duration.

        Args:
            **info: Optional metadata emitted as key/value pairs in the failure
                log line to provide extra debugging context.
        """
        self._complete_step(symbol="✖", **info)

    def _complete_step(self, symbol: str, **info: Any) -> None:
        if not self._current_step:
            return

        elapsed = time.perf_counter() - self._current_step.start
        label = self._current_step.label
        animated = self._current_step.animated
        self._current_step = None

        details = {**info, "time": f"{elapsed:.2f}s"}
        suffix = format_kv(**details)

        if animated:
            print(f"\r{symbol} {label}{suffix}", flush=True)
        else:
            print(f"[{timestamp()}] {symbol} {label}{suffix}", flush=True)

    def info(self, msg: str, **info: Any) -> None:
        """Write an info message and auto-close any pending step.

        Args:
            msg: Main message text shown after the info symbol.
            **info: Optional structured metadata rendered as key/value pairs.
        """
        self._end_step_if_any()
        print(f"[{timestamp()}] ℹ {msg}{format_kv(**info)}", flush=True)

    def warn(self, msg: str, **info: Any) -> None:
        """Write a warning message to stderr.

        Args:
            msg: Main warning text shown after the warning symbol.
            **info: Optional structured metadata rendered as key/value pairs.
        """
        self._end_step_if_any()
        print(
            f"[{timestamp()}] ⚠ {msg}{format_kv(**info)}",
            file=sys.stderr,
            flush=True,
        )

    def error(self, msg: str, **info: Any) -> None:
        """Write an error message to stderr.

        Args:
            msg: Main error text shown after the error symbol.
            **info: Optional structured metadata rendered as key/value pairs.
        """
        self._end_step_if_any()
        print(
            f"[{timestamp()}] ✖ {msg}{format_kv(**info)}",
            file=sys.stderr,
            flush=True,
        )

    def _end_step_if_any(self) -> None:
        if self._current_step:
            self.done()
