from harness.judge import _try_parse_json


def test_try_parse_json_accepts_direct_json():
    parsed = _try_parse_json('{"overall": 5, "rationale": "ok"}')
    assert parsed == {"overall": 5, "rationale": "ok"}


def test_try_parse_json_extracts_wrapped_object():
    parsed = _try_parse_json('Judge result follows:\n{"overall": 4, "rationale": "solid"}\nThanks')
    assert parsed == {"overall": 4, "rationale": "solid"}


def test_try_parse_json_returns_none_for_invalid_text():
    assert _try_parse_json("not json at all") is None
