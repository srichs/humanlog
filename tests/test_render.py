from humanlog.render import format_kv, timestamp


def test_format_kv_empty() -> None:
    assert format_kv() == ""


def test_format_kv_with_values() -> None:
    assert format_kv(user="alice", count=2) == " (user=alice, count=2)"


def test_format_kv_quotes_ambiguous_string_values() -> None:
    assert (
        format_kv(path="/tmp/my file", detail="a,b", status="")
        == ' (path="/tmp/my file", detail="a,b", status="")'
    )


def test_timestamp_shape() -> None:
    value = timestamp()
    assert len(value) == 8
    assert value[2] == ":"
    assert value[5] == ":"
