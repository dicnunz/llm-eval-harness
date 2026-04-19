![tests](https://github.com/dicnunz/llm-eval-harness/actions/workflows/tests.yml/badge.svg)

# llm-eval-harness

Tiny reproducible local-LLM evals over any OpenAI-compatible API.

This repo exists for one narrow job: quickly sanity-check a local model server, save the run as real artifacts, and keep a lightweight score history while you swap models, prompts, or serving stacks.

## Why this exists

Most local-LLM testing is still ad hoc:
- a few manual prompts
- no saved evidence
- no easy before/after comparison
- no small gate before changing model weights or server config

`llm-eval-harness` makes that loop repeatable without turning it into a heavyweight benchmark project.

## Use it when

Use this repo when you want to:
- compare local models behind LM Studio or another OpenAI-compatible server
- run a tiny eval gate before changing prompts, quantizations, or serving config
- keep JSON plus Markdown artifacts you can inspect later
- prove a local model still handles output shape, simple correctness, and refusal basics

Do not use it when you need large benchmark suites, distributed eval infra, or research-grade leaderboards.

## What it does

- runs small JSON-defined eval packs
- talks to any OpenAI-compatible `/v1` endpoint
- writes machine-readable run data plus a human-readable Markdown report
- keeps a rolling `runs/index.json` history for quick trend checks
- supports exact match, JSON parse, keyword constraints, refusal heuristics, and model-as-judge scoring

## Quickstart

### 1) Start a local OpenAI-compatible server

LM Studio works out of the box:
- LM Studio
- Local Server
- Start Server

Default base URL: `http://localhost:1234/v1`

### 2) Install

```bash
git clone https://github.com/dicnunz/llm-eval-harness.git
cd llm-eval-harness
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 3) List the bundled packs

```bash
harness packs
```

Expected shape:

```text
Available eval packs:
- evals/basic.json | basic | 6 tasks | Starter pack for correctness, structure, and refusal checks.
- evals/release_gate.json | release-gate | 5 tasks | Tiny pre-change gate for local model swaps and server config changes.
```

### 4) Run a local eval

```bash
harness run --base-url http://localhost:1234/v1 --model openai/gpt-oss-20b
```

Or run the tighter release gate:

```bash
harness run --pack evals/release_gate.json --model openai/gpt-oss-20b
```

Artifacts written to `runs/`:

```text
runs/
  index.json
  run_<timestamp>.json
  report_<timestamp>.md
```

### 5) Check recent history

```bash
harness summary
```

Example output:

```text
Recent runs (most recent last):
- 20260418-210101  score=5/5 (100.0%)  model=openai/gpt-oss-20b  pack=release-gate
- 20260418-210422  score=4/5 (80.0%)  model=qwen2.5:7b  pack=release-gate

Latest: 20260418-210422  score=4/5 (80.0%)
Best (last 2): 20260418-210101  score=5/5 (100.0%)
Avg (last 2): 0.900
```

## Example report artifact

Generated Markdown reports are meant to be readable enough to share or inspect quickly:

```md
# Local LLM Eval Report

## Run
- Run ID: `20260418-210101`
- Model: `openai/gpt-oss-20b`
- Base URL: `http://localhost:1234/v1`
- Pack: `release-gate`
- Pack File: `evals/release_gate.json`
- Score: **5/5** (100.0%)

## Scorecard
| Task | Type | Result |
| --- | --- | --- |
| `reply_exactly_ready` | `exact_match` | **PASS** |
| `json_contract` | `json_parse` | **PASS** |
```

## Built-in packs

`evals/basic.json`
- broad starter pack
- exact match, JSON shape, arithmetic, instruction following, refusal, judge scoring

`evals/release_gate.json`
- tighter pre-change gate for local iteration
- useful before switching model, prompt wrapper, or OpenAI-compatible server settings

## Pack format

Eval packs are plain JSON with a `tasks` array:

```json
{
  "name": "my-pack",
  "description": "Short description.",
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

Supported task types:
- `exact_match`
- `json_parse`
- `contains`
- `refusal_check`
- `judge`

## Reliability story

This repo is intentionally small, but it is not hand-wavy:
- pack validation fails fast on malformed JSON or missing task fields
- model calls run with `temperature=0` for stable eval prompts
- judge parsing retries once and falls back to a structured error payload
- CLI flow, report writing, summary formatting, and pack loading are covered by tests
- GitHub Actions runs the test suite on every push and pull request

## Development

```bash
python -m compileall src
pytest -q
```

## License

MIT
