# Release process

This document describes the repeatable release flow for `humanlog`.

## Preconditions

- Work is merged to the default branch.
- Local checks are green.
- `CHANGELOG.md` has an entry for the release version.
- `pyproject.toml` has the correct `project.version`.

## 1) Create/activate a clean environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
python -m pip install build twine
```

## 2) Run quality gates

```bash
ruff check .
black --check .
mypy src
pytest
sphinx-build -b html docs docs/_build/html
```

## 3) Build artifacts

```bash
rm -rf dist/
python -m build
```

Expected artifacts:
- `dist/*.tar.gz` (sdist)
- `dist/*.whl` (wheel)

## 4) Validate package metadata and long description

```bash
twine check dist/*
```

## 5) Publish

### TestPyPI (recommended first)

```bash
twine upload --repository testpypi dist/*
```

Install smoke test:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ humanlog==<version>
python -c "from humanlog import log; log.info('smoke test')"
```

### PyPI

```bash
twine upload dist/*
```

## 6) Tag and GitHub release

```bash
git tag -a v<version> -m "humanlog v<version>"
git push origin v<version>
```

Then create a GitHub release:
- Title: `v<version>`
- Body: summarize changes from `CHANGELOG.md`

## 7) Post-release checks

- Verify `pip install humanlog==<version>` from PyPI.
- Verify import and a minimal runtime call.
- Confirm docs/release notes links are correct.
