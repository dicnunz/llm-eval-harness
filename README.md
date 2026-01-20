![tests](https://github.com/dicnunz/llm-eval-harness/actions/workflows/tests.yml/badge.svg)

# llm-eval-harness

A tiny, reproducible evaluation harness for **local LLMs** served through an **OpenAI-compatible API** (tested with LM Studio).

It runs a small task pack, saves results to `runs/` as JSON + Markdown, and tracks score history.

## Why this project
This repo demonstrates I can:
- integrate with OpenAI-compatible APIs (local model servers like LM Studio)
- design reproducible evals (JSON + markdown reports, run history)
- add safety/behavior checks and model-as-judge scoring
- ship an installable CLI with tests + CI

## Requirements
- Python 3.10+
- LM Studio running a local server (OpenAI-compatible)

## Quickstart

### 1) Start LM Studio server
In LM Studio: **Local Server → Start Server** (default `http://localhost:1234/v1`)

### 2) Install
```bash
git clone https://github.com/dicnunz/llm-eval-harness.git
cd llm-eval-harness
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3) Run an eval
```bash
harness run --base-url http://localhost:1234/v1 --model openai/gpt-oss-20b
```

### Eval packs
Run the default pack or choose a specific one:
```bash
harness run --pack evals/basic.json
```

To write a new pack, create a JSON file with a `tasks` array. Each task needs
`id`, `type`, and `prompt`, plus any type-specific fields:
```json
{
  "name": "my-pack",
  "description": "Short description of the pack.",
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

Outputs:
- `runs/run_<timestamp>.json` (machine-readable)
- `runs/report_<timestamp>.md` (human-readable)
- `runs/index.json` (history)

### 4) View recent scores
```bash
harness summary
```

## Development
Run the unit tests locally:
```bash
python -m compileall src
pytest -q
```

## What it evaluates (current pack)
- Exact-match instruction following
- JSON formatting correctness
- Simple arithmetic
- Keyword inclusion constraints
- Safety/refusal behavior
- Model-as-judge quality scoring (rubric)

## Notes
- The default model name is `openai/gpt-oss-20b`, but you can pass any model id that your local server exposes.

## License
MIT
