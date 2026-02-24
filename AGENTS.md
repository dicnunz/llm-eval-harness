# AGENTS.md

## Purpose
Guidelines for contributors and automation agents working in this repository.

## Non-negotiable rules
- Preserve evaluator behavior unless a change is explicitly requested and justified.
- Keep outputs reproducible: avoid hidden randomness, keep scoring logic explicit, and preserve artifact schema compatibility.
- Do not make fake benchmark claims or imply publication-scale evaluation coverage.
- Favor simple interfaces (`harness` CLI, JSON packs) and explicit file outputs (`runs/*.json`, `runs/*.md`, `runs/index.json`).

## Implementation expectations
- Keep eval pack contracts strict (`id`, `type`, `prompt`, and type-specific fields).
- Prefer additive, backwards-compatible changes to task grading and report formats.
- Update tests when behavior changes; otherwise keep tests green without weakening assertions.
- Keep docs concrete and truthful about what the harness does and does not measure.
