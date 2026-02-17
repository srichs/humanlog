# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-17

### Added
- Initial `humanlog` release with a small, human-friendly logging API.
- Step lifecycle support via `log.step(...)` and explicit completion with `log.done(...)`.
- Auto-failing context manager behavior for `with log.step(...): ...` blocks.
- Informational and error channels via `log.info(...)`, `log.warn(...)`, and `log.error(...)`.
- Environment-aware rendering behavior for TTY, CI, and non-interactive outputs.
- Test suite plus lint/type-check tooling and Sphinx docs scaffolding.

### Notes
- `humanlog` intentionally prioritizes a tiny, opinionated API over broad configurability.
- Planned roadmap items are tracked in `README.md`.

[0.1.0]: https://github.com/srichs/humanlog/releases/tag/v0.1.0
