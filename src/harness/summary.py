import json
from pathlib import Path

def main():
    idx = Path("runs/index.json")
    if not idx.exists():
        raise SystemExit("No runs/index.json found. Run: harness run")

    data = json.loads(idx.read_text(encoding="utf-8"))
    runs = data.get("runs", [])
    if not runs:
        raise SystemExit("index.json has no runs. Run: harness run")

    last = runs[-5:]  # last 5 runs
    print("Last runs (most recent last):")
    for r in last:
        print(f"- {r['run_id']}  score={r['passed']}/{r['total']}  model={r['model']}")

    avg = sum(r["score"] for r in last) / len(last)
    print(f"\nAvg (last {len(last)}): {avg:.3f}")

if __name__ == "__main__":
    main()
