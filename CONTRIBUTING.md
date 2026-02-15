# Contributing to humanlog

Thanks for your interest in contributing to `humanlog`.

## Development setup

1. Create and activate a virtual environment.
2. Install development dependencies:

```bash
pip install -e .[dev]
```

## Common commands

```bash
ruff check .
black --check .
mypy src
pytest
```

## Style guidelines

- Keep the API small and readable.
- Prefer behavior that works consistently in TTY, CI, and notebooks.
- Add tests for any behavior changes.

## Pull requests

- Keep PRs focused and small.
- Update docs (`README.md` / `docs/`) when API behavior changes.
- Ensure checks pass before requesting review.
