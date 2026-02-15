# humanlog

One-line logging + progress for humans.  
Works in terminals, CI, and Jupyter — no setup, no configuration.

```python
from humanlog import log

log.step("Downloading data")
...
log.done(rows=120_000)

log.info("Cleaning finished")
log.warn("Missing values detected", cols=3)
```

## Why humanlog?

Most logging tools are either:

- too low-level (stdlib logging),
- too heavy (structured logging frameworks),
- or great at one thing (progress bars) but awkward for everything else.

`humanlog` is opinionated and small:

- readable output
- automatic timing
- graceful behavior everywhere
- zero configuration

It’s for applications, scripts, CLIs, and data workflows.

## Install

```bash
pip install humanlog
```

Python 3.9+ (no dependencies).

## The core idea

### Steps feel like steps

```python
log.step("Training model")
train()
log.done(loss=0.031)
```

Output (terminal):

```text
→ Training model …
✓ Training model (loss=0.031, time=2.41s)
```

No manual timers. No formatting. No state.

### Informational messages

```python
log.info("Loading dataset", rows=120_000)
log.warn("Missing values detected", cols=3)
log.error("Failed to connect to database")
```

Output:

```text
[12:40:03] ℹ Loading dataset (rows=120000)
[12:40:04] ⚠ Missing values detected (cols=3)
[12:40:05] ✖ Failed to connect to database
```

## Works everywhere

### Terminal (TTY)

- Animated steps
- Clean overwrite
- Human-friendly symbols

### CI (GitHub Actions, GitLab, etc.)

- No carriage-return garbage
- Timestamped, line-by-line logs

### Jupyter notebooks

- No broken progress bars
- Clean output cells

`humanlog` automatically detects where it’s running and adapts.

Set `HUMANLOG_NO_ANIMATE=1` (or `NO_COLOR=1`) to force non-animated output.

## Zero configuration

No handlers.  
No log levels to wire up.  
No global logging side effects.

Just import and go.

## API

### `log.step(message: str)`

Start a timed step.

You can also use it as a context manager to auto-complete the step:

```python
with log.step("Training model"):
    train()
```

### `log.done(**info)`

Finish the current step and print timing + optional key/value info.

### `log.info(message: str, **info)`

Print an informational message.

### `log.warn(message: str, **info)`

Print a warning (to stderr).

### `log.error(message: str, **info)`

Print an error (to stderr).

Key/value info is always optional and rendered inline:

```python
log.info("Loaded batch", batch=3, rows=1024)
```

## Example: a real script

```python
from humanlog import log

log.step("Downloading data")
download()
log.done(rows=120_000)

log.step("Cleaning data")
clean()
log.done(dropped=341)

log.step("Training model")
train()
log.done(epochs=10, loss=0.031)

log.info("All done")
```

Readable. Intentional. Calm.

## Non-goals (by design)

`humanlog` is not:

- a replacement for structured logging
- a metrics system
- a tracing framework
- a progress-bar DSL

If you need JSON logs or OpenTelemetry, use those tools.

If you want pleasant, readable output, use `humanlog`.

## Roadmap (likely, but optional)

- `log.track(iterable, label="Processing")`
- optional Rich-powered rendering
- stdlib logging bridge (opt-in)

The core will stay small.

## Philosophy

`humanlog` optimizes for:

- clarity over flexibility
- defaults over configuration
- humans over machines

Logs are for people first.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for local setup and quality checks.

## License

MIT
