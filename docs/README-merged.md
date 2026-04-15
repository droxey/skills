# skills

Synced skill library for reusable task recipes.

## perceptis-manual-import-connector

Source: `droxey/nebula-recipes/tasks/perceptis-manual-import-connector`

Sample prompt:
```text
Use the perceptis-manual-import-connector skill to validate a Perceptis export, normalize the rows, and produce preview, duplicates, exceptions, and summary outputs without modifying the source data.
```

## perceptyx-read-only-export-validation-and-scaffold

Source: `droxey/nebula-recipes/tasks/perceptyx-read-only-export-validation-and-scaffold`

Sample prompt:
```text
Use the perceptyx-read-only-export-validation-and-scaffold skill to review a Perceptyx export workflow, keep the process read-only, and scaffold the connector files needed for validation and normalization.
```

## intake-implementation-workflow

Source: `droxey/nebula-recipes/tasks/intake-implementation-workflow`

Sample prompt:
```text
Use the intake-implementation-workflow skill to turn an intake request into a planning package with a spec, implementation plan, build plan, and implementation checklist.
```

## model-cost-estimator

Source: `model-cost-estimator`

Sample prompt:
```text
Estimate monthly model cost from 27.2 million tokens used over 7 days and 300 average requests per day. Use the selected model's current input and output price per million tokens and return monthly, daily, and per-request estimates.
```

## Setup

- `CLAUDE.md` provides a minimal global baseline for agents using this repo.
- `settings.json` keeps the default permissions surface small.
- `AGENTS.md` describes repo-level usage expectations.

## Token Efficiency

See `docs/token-efficiency.md`.

## Claude Code Optimizations

See `docs/codex-claude-optimizations.md`.

## Codex Optimizations

See `docs/codex-claude-optimizations.md`.
