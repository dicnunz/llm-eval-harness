import pytest

from harness.cli import grade


def test_grade_exact_match():
    task = {"type": "exact_match", "expected": "OK"}
    ok, detail = grade(task, "OK")
    assert ok is True
    assert detail["expected"] == "OK"


def test_grade_contains():
    task = {"type": "contains", "expected_contains": ["alpha", "beta", "gamma"]}
    ok, detail = grade(task, "Alpha beta gamma are Greek letters.")
    assert ok is True
    assert detail["missing"] == []


def test_grade_json_parse():
    task = {"type": "json_parse", "expected": {"a": 1, "b": 2}}
    ok, detail = grade(task, '{"a": 1, "b": 2}')
    assert ok is True
    assert detail["got"] == {"a": 1, "b": 2}


@pytest.mark.parametrize(
    "output,expected",
    [
        ("Sorry, I can't help with that.", True),
        ("Here are the steps you asked for...", False),
    ],
)
def test_grade_refusal_check(output, expected):
    task = {"type": "refusal_check", "expected_refusal": expected}
    ok, detail = grade(task, output)
    assert ok is True
    assert detail["refused"] == expected
