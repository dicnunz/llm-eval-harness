import json
from pathlib import Path

import pytest

from harness.cli import PackValidationError, load_pack


def test_load_pack_success():
    pack = load_pack(Path("evals/basic.json"))
    assert pack["tasks"]
    assert any(task["type"] == "judge" for task in pack["tasks"])


def test_load_pack_missing_fields(tmp_path):
    invalid_pack = {
        "tasks": [
            {"id": "missing_prompt", "type": "exact_match", "expected": "OK"},
        ]
    }
    pack_path = tmp_path / "invalid.json"
    pack_path.write_text(json.dumps(invalid_pack), encoding="utf-8")

    with pytest.raises(PackValidationError, match="missing required field"):
        load_pack(pack_path)
