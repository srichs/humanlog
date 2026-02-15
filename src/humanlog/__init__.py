"""humanlog: one-line progress + logging for humans."""

from .core import NiceLog

__all__ = ["NiceLog", "log"]

log = NiceLog()
