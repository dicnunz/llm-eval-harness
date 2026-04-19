import json
from pathlib import Path
from typing import Any


def _score_value(run: dict[str, Any]) -> float:
    if "score" in run:
        return float(run["score"])
    total = max(1, int(run["total"]))
    return float(run["passed"]) / total


def _score_percent(run: dict[str, Any]) -> str:
    total = int(run["total"])
    if total == 0:
        return "0.0%"
    return f"{(int(run['passed']) / total) * 100:.1f}%"


def _format_run(run: dict[str, Any]) -> str:
    pack_name = run.get("pack_name")
    pack_part = f"  pack={pack_name}" if pack_name else ""
    return (
        f"- {run['run_id']}  score={run['passed']}/{run['total']} ({_score_percent(run)})  "
        f"model={run['model']}{pack_part}"
    )


def render_summary(runs: list[dict[str, Any]], limit: int = 5) -> str:
    if not runs:
        raise ValueError("No runs available.")

    window = runs[-limit:]
    latest = window[-1]
    best = max(window, key=lambda run: (_score_value(run), run["run_id"]))
    avg = sum(_score_value(run) for run in window) / len(window)

    lines = ["Recent runs (most recent last):"]
    lines.extend(_format_run(run) for run in window)
    lines.extend(
        [
            "",
            f"Latest: {latest['run_id']}  score={latest['passed']}/{latest['total']} ({_score_percent(latest)})",
            f"Best (last {len(window)}): {best['run_id']}  score={best['passed']}/{best['total']} ({_score_percent(best)})",
            f"Avg (last {len(window)}): {avg:.3f}",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    index_path = Path("runs/index.json")
    if not index_path.exists():
        raise SystemExit("No runs/index.json found. Run: harness run")

    data = json.loads(index_path.read_text(encoding="utf-8"))
    runs = data.get("runs", [])
    if not runs:
        raise SystemExit("index.json has no runs. Run: harness run")

    print(render_summary(runs))


if __name__ == "__main__":
    main()
