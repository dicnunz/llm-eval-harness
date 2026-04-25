import argparse
import json
from pathlib import Path

import pytest

from harness import cli
from harness.cli import PackValidationError, cmd_packs, cmd_validate, load_pack


def test_load_pack_success():
    pack = load_pack(Path("evals/basic.json"))
    assert pack["tasks"]
    assert pack["name"] == "basic"
    assert any(task["type"] == "judge" for task in pack["tasks"])


def test_load_release_gate_pack_success():
    pack = load_pack(Path("evals/release_gate.json"))
    assert pack["name"] == "release-gate"
    assert len(pack["tasks"]) == 5


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


def test_cmd_packs_prints_metadata(tmp_path, monkeypatch, capsys):
    alpha = tmp_path / "alpha.json"
    beta = tmp_path / "beta.json"

    alpha.write_text(
        json.dumps(
            {
                "name": "alpha",
                "description": "Alpha pack.",
                "tasks": [{"id": "ok", "type": "exact_match", "prompt": "Reply with OK", "expected": "OK"}],
            }
        ),
        encoding="utf-8",
    )
    beta.write_text(
        json.dumps(
            {
                "name": "beta",
                "description": "Beta pack.",
                "tasks": [{"id": "json", "type": "json_parse", "prompt": "Return JSON", "expected": {}}],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(cli, "EVALS_DIR", tmp_path)
    cmd_packs(argparse.Namespace())

    out = capsys.readouterr().out
    assert "Available eval packs:" in out
    assert "alpha.json | alpha | 1 tasks | Alpha pack." in out
    assert "beta.json | beta | 1 tasks | Beta pack." in out


def test_cmd_validate_checks_every_pack(tmp_path, monkeypatch, capsys):
    pack = tmp_path / "alpha.json"
    pack.write_text(
        json.dumps(
            {
                "name": "alpha",
                "tasks": [{"id": "ok", "type": "exact_match", "prompt": "Reply with OK", "expected": "OK"}],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(cli, "EVALS_DIR", tmp_path)
    cmd_validate(argparse.Namespace(pack=None))

    out = capsys.readouterr().out
    assert "valid: " in out
    assert "Validated 1 pack(s)." in out
