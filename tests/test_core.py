import humanlog.core as core


def test_info_closes_active_step_and_prints_info(monkeypatch, capsys) -> None:
    logger = core.NiceLog()
    times = iter([10.0, 12.5])

    monkeypatch.setattr(core, "can_animate", lambda: False)
    monkeypatch.setattr(core, "timestamp", lambda: "09:30:00")
    monkeypatch.setattr(core.time, "perf_counter", lambda: next(times))

    logger.step("download")
    logger.info("ready", items=3)

    out = capsys.readouterr().out.strip().splitlines()
    assert out == [
        "[09:30:00] → download",
        "[09:30:00] ✓ download (time=2.50s)",
        "[09:30:00] ℹ ready (items=3)",
    ]


def test_warn_and_error_write_to_stderr(monkeypatch, capsys) -> None:
    logger = core.NiceLog()
    monkeypatch.setattr(core, "timestamp", lambda: "09:30:00")

    logger.warn("slow", retry=1)
    logger.error("failed", code=500)

    err = capsys.readouterr().err.strip().splitlines()
    assert err == [
        "[09:30:00] ⚠ slow (retry=1)",
        "[09:30:00] ✖ failed (code=500)",
    ]


def test_done_without_step_is_noop(capsys) -> None:
    logger = core.NiceLog()
    logger.done()
    assert capsys.readouterr().out == ""
