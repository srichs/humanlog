"""humanlog: one-line progress + logging for humans."""

from .core import HumanLog

__all__ = ["HumanLog", "log"]

log = HumanLog()
