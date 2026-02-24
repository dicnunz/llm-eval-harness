# 60-Second Recruiter Demo

## Goal
Show a practical local LLM evaluation loop with explicit artifacts.

## Script (about 60 seconds)
1. Open `README.md` and point to the one-line project pitch and problem statement.
2. Run `harness packs` to show discoverable eval packs.
3. Run one eval:
   `harness run --base-url http://localhost:11434/v1 --model llama3.2 --api-key ollama`
4. Open the new `runs/run_<timestamp>.json` and call out machine-readable fields (`summary`, per-task `detail`).
5. Open `runs/report_<timestamp>.md` and show pass/fail readability for humans.
6. Run `harness summary` to show trend/history from `runs/index.json`.
7. Close with: this is a local, reproducible comparison harness for iterative model testing.

## What to emphasize
- Reproducible task pack input.
- Concrete JSON + Markdown outputs.
- Honest scope: small harness, not a large benchmark platform.
