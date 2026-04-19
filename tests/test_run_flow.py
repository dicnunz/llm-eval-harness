import argparse
import json

from harness import cli


class DummyClient:
    pass


def test_cmd_run_writes_json_report_and_index(tmp_path, monkeypatch, capsys):
    runs_dir = tmp_path / "runs"
    pack_path = tmp_path / "smoke.json"
    pack_path.write_text(
        json.dumps(
            {
                "name": "smoke",
                "description": "Small deterministic smoke pack.",
                "tasks": [
                    {
                        "id": "reply_exactly_ready",
                        "type": "exact_match",
                        "prompt": "Reply with exactly: READY",
                        "expected": "READY",
                    },
                    {
                        "id": "json_contract",
                        "type": "json_parse",
                        "prompt": "Return ONLY JSON with status=ready.",
                        "expected": {"status": "ready"},
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    responses = {
        "Reply with exactly: READY": "READY",
        "Return ONLY JSON with status=ready.": '{"status": "ready"}',
    }

    monkeypatch.setattr(cli, "RUNS_DIR", runs_dir)
    monkeypatch.setattr(cli, "OpenAI", lambda **kwargs: DummyClient())
    monkeypatch.setattr(cli, "chat", lambda client, model, prompt: responses[prompt])
    monkeypatch.setattr(cli.time, "strftime", lambda fmt: "20260418-210101")

    args = argparse.Namespace(
        base_url="http://localhost:1234/v1",
        model="test-model",
        api_key="lm-studio",
        pack=str(pack_path),
    )

    cli.cmd_run(args)

    out = capsys.readouterr().out
    assert "Running 2 tasks from smoke against test-model via http://localhost:1234/v1" in out
    assert "reply_exactly_ready: PASS" in out
    assert "json_contract: PASS" in out

    run_path = runs_dir / "run_20260418-210101.json"
    report_path = runs_dir / "report_20260418-210101.md"
    index_path = runs_dir / "index.json"

    assert run_path.exists()
    assert report_path.exists()
    assert index_path.exists()

    run_data = json.loads(run_path.read_text(encoding="utf-8"))
    assert run_data["pack"]["name"] == "smoke"
    assert run_data["summary"] == {"passed": 2, "total": 2}

    report = report_path.read_text(encoding="utf-8")
    assert "# Local LLM Eval Report" in report
    assert "| `reply_exactly_ready` | `exact_match` | **PASS** |" in report
    assert "Pack Description: Small deterministic smoke pack." in report

    index = json.loads(index_path.read_text(encoding="utf-8"))
    assert index["runs"][0]["pack_name"] == "smoke"
    assert index["runs"][0]["score"] == 1.0
