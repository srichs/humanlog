from __future__ import annotations

import time
from typing import Any


def format_kv(**kwargs: Any) -> str:
    """Render key/value metadata suffix for log lines."""
    if not kwargs:
        return ""
    parts = [f"{k}={v}" for k, v in kwargs.items()]
    return " (" + ", ".join(parts) + ")"


def timestamp() -> str:
    """Return a compact local timestamp."""
    return time.strftime("%H:%M:%S")
