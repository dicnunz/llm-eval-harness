import json
from pathlib import Path

def load_latest_run():
    runs = sorted(Path("runs").glob("run_*.json"))
    if not runs:
        raise SystemExit("No runs found in ./runs. Run: python src/run_eval.py")
    return runs[-1]

def main():
    run_path = load_latest_run()
    data = json.loads(run_path.read_text(encoding="utf-8"))

    passed = data["summary"]["passed"]
    total = data["summary"]["total"]
    model = data["model"]
    run_id = data["run_id"]

    lines = []
    lines.append(f"# LLM Eval Report")
    lines.append(f"- Run: `{run_id}`")
    lines.append(f"- Model: `{model}`")
    lines.append(f"- Score: **{passed}/{total}**")
    lines.append("")
    lines.append("## Results")

    for r in data["results"]:
        status = "✅ PASS" if r["pass"] else "❌ FAIL"
        lines.append(f"### {r['task_id']} — {status}")
        lines.append(f"**Type:** `{r['type']}`")
        lines.append(f"**Prompt:** {r['prompt']}")
        lines.append(f"**Output:** `{r['output']}`")
        if not r["pass"]:
            lines.append(f"**Detail:** `{r['detail']}`")
        lines.append("")

    out_md = Path("runs") / f"report_{run_id}.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote: {out_md}")

if __name__ == "__main__":
    main()
