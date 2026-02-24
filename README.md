![tests](https://github.com/dicnunz/llm-eval-harness/actions/workflows/tests.yml/badge.svg)

# llm-eval-harness

“Runs locally with Ollama — deployable in Replit in one click.”

A practical evaluation harness for comparing local LLM behavior through an OpenAI-compatible API.

## Problem it solves
When trying local models, it is easy to rely on ad-hoc prompts and subjective impressions. This project gives you a repeatable check: run a fixed task pack, score outputs consistently, and keep run history in files you can inspect and diff.

This is intentionally small-scope: a local comparison harness, not a published benchmark platform.

## How it compares local LLM outputs
`harness run` executes each task in an eval pack (`evals/*.json`) against one model endpoint and grades outputs by task type:

- `exact_match`: strict string match
- `json_parse`: JSON parse + exact object match
- `contains`: required keywords present
- `refusal_check`: lightweight refusal heuristic
- `judge`: model-as-judge rubric score (1-5 dimensions)

Runs are deterministic where possible (`temperature=0`) and recorded as explicit artifacts.

## Expected inputs and outputs
### Inputs
- Eval pack JSON file (default: `evals/basic.json`)
- Model endpoint info (`--base-url`, `--model`, optional `--api-key`)

Minimal pack structure:

```json
{
  "name": "basic",
  "description": "Starter eval pack",
  "tasks": [
    {
      "id": "exact_string",
      "type": "exact_match",
      "prompt": "Reply with exactly: OK",
      "expected": "OK"
    }
  ]
}
```

### Outputs
Each run writes artifacts to `runs/`:

- `run_<timestamp>.json`: machine-readable per-task results
- `report_<timestamp>.md`: human-readable report
- `index.json`: rolling run history and scores

Sample artifacts are in `examples/sample_run.json` and `examples/sample_report.md`.

## Local setup
Requirements:

- Python 3.10+
- Ollama running locally (or any OpenAI-compatible local server)

```bash
git clone https://github.com/dicnunz/llm-eval-harness.git
cd llm-eval-harness
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start Ollama separately, then run:

```bash
harness run \
  --base-url http://localhost:11434/v1 \
  --model llama3.2 \
  --api-key ollama
```

## Example run
List available packs:

```bash
harness packs
```

Run default pack:

```bash
harness run --base-url http://localhost:11434/v1 --model llama3.2 --api-key ollama
```

View recent score trend:

```bash
harness summary
```

## How to interpret results
- Start with `summary.passed / summary.total` in `run_*.json` for a quick pass rate.
- Open `report_*.md` to inspect each task’s prompt, output, and failure details.
- Use `runs/index.json` to compare runs over time (model changes, prompt-pack updates, regressions).
- Treat `judge` scores as a heuristic signal, not ground truth.

## Replit deployment
This repo now includes minimal Replit config for one-click launch:

- `.replit`
- `replit.nix`
- `requirements.txt`

### Exact steps
1. Import the GitHub repo into Replit.
2. Click **Run** once. Replit installs dependencies and runs `harness packs`.
3. To execute an eval from the Replit shell, run:

```bash
harness run --base-url "$BASE_URL" --model "$MODEL" --api-key "$API_KEY"
```

4. Set `BASE_URL`, `MODEL`, and `API_KEY` in Replit Secrets (or inline in the command). The endpoint must be reachable from Replit.

Notes:
- Replit hosts the harness runner; the model server can be Ollama/OpenAI-compatible anywhere reachable by URL.
- If no model endpoint is reachable, `harness run` will fail while `harness packs` and docs still work.

## Development
```bash
python -m compileall src
pytest -q
```

## License
MIT
