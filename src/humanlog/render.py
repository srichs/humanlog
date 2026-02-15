from __future__ import annotations

import json
import time
from typing import Any


def _format_value(value: Any) -> str:
    """Format metadata values with lightweight quoting for readability."""
    if isinstance(value, str):
        if value == "" or any(ch.isspace() or ch in ",()=" for ch in value):
            return json.dumps(value)
        return value
    return str(value)


def format_kv(**kwargs: Any) -> str:
    """Render key/value metadata suffix for log lines."""
    if not kwargs:
        return ""
    parts = [f"{k}={_format_value(v)}" for k, v in kwargs.items()]
    return " (" + ", ".join(parts) + ")"


def timestamp() -> str:
    """Return a compact local timestamp."""
    return time.strftime("%H:%M:%S")
