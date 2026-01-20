import json
from pathlib import Path

RUNS_DIR = Path("runs")
INDEX_PATH = RUNS_DIR / "index.json"

def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    runs = sorted(RUNS_DIR.glob("run_*.json"))
    if not runs:
        raise SystemExit("No runs found. Run: python src/run_eval.py")

    latest = runs[-1]
    latest_data = json.loads(latest.read_text(encoding="utf-8"))

    index = load_json(INDEX_PATH, {"runs": []})
    existing_ids = {r["run_id"] for r in index["runs"]}

    if latest_data["run_id"] not in existing_ids:
        index["runs"].append({
            "run_id": latest_data["run_id"],
            "model": latest_data["model"],
            "base_url": latest_data["base_url"],
            "passed": latest_data["summary"]["passed"],
            "total": latest_data["summary"]["total"],
            "score": latest_data["summary"]["passed"] / max(1, latest_data["summary"]["total"]),
            "run_file": latest.name,
            "report_file": f"report_{latest_data['run_id']}.md",
        })

    # keep sorted by run_id (timestamp string)
    index["runs"] = sorted(index["runs"], key=lambda r: r["run_id"])

    INDEX_PATH.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"Updated: {INDEX_PATH}  (runs tracked: {len(index['runs'])})")

if __name__ == "__main__":
    main()
