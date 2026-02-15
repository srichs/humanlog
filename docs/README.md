# Building documentation

This project supports two documentation workflows:

## pydoc

Generate built-in Python HTML docs for the package:

```bash
python -m pydoc -w humanlog
```

This creates `humanlog.html` in the current directory.

## Sphinx

Install docs dependencies, then build HTML docs:

```bash
python -m pip install -e .[dev]
sphinx-build -b html docs docs/_build/html
```

Open `docs/_build/html/index.html` in your browser.
