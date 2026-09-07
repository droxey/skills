# Skill Maturity Standard

This repository treats every skill as a small product and hardens it one level at a
time, following the incremental methodology from
[Building agent skills incrementally](https://alexhans.github.io/posts/series/evals/building-agent-skills-incrementally.html).
A skill earns a maturity level only when it meets every requirement of the lower
levels; a skill that has not yet been hardened sits at Level 0.

The reference implementation is `product-reverse-engineering/`: it is the Level 3
exemplar with a pinned `references/` contract, a deterministic router, machine-readable
`tests/` cases with unit tests, and a typed `agents/` interface.

## Levels

### Level 0 - Intent

A skill that is clear enough to use correctly. All first-party skills must reach at
least this level.

- States a single clear purpose.
- Names its inputs and outputs explicitly.
- Ships at least one concrete example.
- Defines "good enough" (success criteria) so an agent can tell when to stop.

### Level 1 - Determinism

The stable, mechanical parts of the skill are encoded so runs reproduce.

- Stable mechanical steps are moved into a script or tool instead of prose.
- Structured output (a schema, JSON/JSONL/YAML contract, or typed CLI output).
- Tool input/output is logged so a run can be replayed or audited.

### Level 2 - Stability

Behaviour is locked down with tests before it drifts or regresses.

- Unit tests cover the tooling, plus minimal golden and edge cases.
- A failing test is treated as a blocked change, not a soft warning.

### Level 3 - Safety and Scale

The skill is safe to run against production-scale or high-impact targets.

- Least privilege: minimal scope, read-only unless a write is required, no secrets.
- Human approval is required before consequential actions (purchase, publish, delete).
- Security evals cover the guardrails; observability makes decisions auditable.

## Required SKILL.md contract

Every first-party `SKILL.md` must carry, in its YAML frontmatter:

- `name` - the skill slug (non-empty).
- `description` - one sentence starting with `Use when` (non-empty).
- `maturity` - an integer `0`-`3` stating the level this skill has reached.

The body must contain one section for each capability of its declared level. The
validator accepts both the canonical heading and the aliases below, so a section is
recognized by intent even when an older skill uses a different word. New skills should
use the canonical heading.

| Capability | Canonical heading | Accepted aliases |
|---|---|---|
| Purpose | `## Purpose` | `Core rule`, `Intent`, `What it does`, `What this does` |
| Inputs | `## Inputs` | `Preflight`, `Runtime model`, `What it needs`, `Input` |
| Outputs | `## Outputs` | `What this skill produces`, `What it produces`, `Handoff`, `Produces`, `Artifacts` |
| Example | `## Example` | `Examples`, `Worked example`, `Example invocation`, `Example run` |
| Success criteria | `## Success criteria` | `Definition of done`, `Validation standard`, `Done when`, `Good enough`, `Acceptance criteria` |
| Maturity | `## Maturity` | `Maturity level`, `Maturity note` |

Level 1 and above add structural requirements the validator verifies against the skill
directory:

- Level 1: a runnable script (`.py`/`.sh`/`.js`/`.ts`) or a structured output file
  (`.json`/`.jsonl`/`.yaml`/`.yml`) anywhere under the skill directory.
- Level 2: a `tests/` directory containing at least one unit-test file
  (`test_*.py`/`*_test.py`).
- Level 3: an `agents/` interface directory or an explicit safety section
  (`## Guardrails`, `## Safety`, `## Security`, `## Authorization`, `## Ethics`,
  `## Approval`).

## Validating

Run the deterministic validator and its tests before landing a skill change:

```bash
python3 tools/validate_skills.py
python3 -m unittest tools.test_validate_skills
```

`tools/validate_skills.py` uses only the Python standard library and makes no network
or model calls. It scans every top-level first-party `SKILL.md`, checks the frontmatter
and required sections above, and reports each skill's declared and substantiated
maturity level. A non-zero exit code means a skill is missing a required section or is
declared at a level its structure does not substantiate.
