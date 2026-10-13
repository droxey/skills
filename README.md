# skills

Synced skill library for reusable task recipes.

## intake-implementation-workflow

Source: `droxey/nebula-recipes/tasks/intake-implementation-workflow`

Sample prompt:
```text
Use the intake-implementation-workflow skill to turn an intake request into a planning package with a spec, implementation plan, build plan, and implementation checklist.
```


## code

Source: `hacker-news-comment (workflow pattern)`

Sample prompt:
```text
Use the code skill to execute a refactor with plan iteration, spec-first thinking, tests-first implementation, manual verification, review, mutation testing, and docs updates.
```

## product-reverse-engineering

Source: `product-reverse-engineering/`

Sample prompt:
```text
Use $product-reverse-engineering to route this product analysis or rebuilding request to the correct specialist with the required safety gates and reviewed handoffs.
```

## skill-maturity

Every first-party skill declares a `maturity` level in its `SKILL.md` frontmatter and carries the required Purpose, Inputs, Outputs, Example, Success criteria, and Maturity sections. Levels: `0` Intent, `1` Determinism (script/structured asset), `2` Stability (unit tests), `3` Safety and Scale (agents/ interface or safety section). See `docs/skill-maturity-standard.md`.

### Validation

From the repository root, using Python 3.12:

```bash
python -m pip install pytest==9.1.1
python tools/validate_skills.py
python -m pytest -q
```

CI runs these checks on pushes to `main` and pull requests on Linux, macOS, and
Windows. It validates the catalog; Skillshare manages distribution separately.
The validator checks all skill contracts. Tests cover the validator, hardening
helpers, routing evaluator, trigger evaluator, and the two Nebula-specific skills;
they do not prove every skill's live behavior.

The maintenance commands `python tools/harden_skills.py` and
`python tools/finalize_skills.py` rewrite skill files. Run them only when changing
the catalog, then inspect the diff and rerun validation.

### Skillshare

Use [Skillshare](https://github.com/runkids/skillshare) to manage skill distribution.
Inspect the configured source and targets before syncing; this repository does not
prescribe a global config or target paths. With Skillshare installed, these global
commands inspect configuration and preview changes:

```bash
skillshare status -g --json
skillshare diff -g --json
skillshare doctor -g --json
skillshare sync -g --dry-run
```

Use `-p` instead for a configured project. Check command help for your installed
version. A clean repository test run does not establish that local targets are
synced. The former script-based sync workflow has been retired.

### Use this repository with any agent harness

[![Last updated](https://img.shields.io/github/last-commit/droxey/skills?label=last%20updated)](https://github.com/droxey/skills/commits/main)
[![Skills](https://img.shields.io/badge/skills-35-blue)](#skills)

#### Kickoff prompt

```text
Use this repository as a library of reusable skills. Read the relevant
SKILL.md before starting, follow its instructions, and keep the task scoped
to the user's request. If no skill clearly applies, proceed without one.
```

#### Usage guide

1. Make this repository available to your harness by cloning it or adding it as a skills directory.
2. For each task, select the closest skill below and provide its `SKILL.md` to the agent as context.
3. Ask the agent to follow the skill, inspect the repository, and report validation results.

#### Skills

- [ah-devops-engineer](ah-devops-engineer/SKILL.md)
- [ai-writing-detection](ai-writing-detection/SKILL.md)
- [chrome-mcp-web-fallback](chrome-mcp-web-fallback/SKILL.md)
- [code](code/SKILL.md)
- [code-review](code-review/SKILL.md)
- [codespace-operator-v2](codespace-operator-v2/SKILL.md)
- [dani-roxberrys-teaching-voice](dani-roxberrys-teaching-voice/SKILL.md)
- [essence](essence/SKILL.md)
- [essence-commit](essence-commit/SKILL.md)
- [essence-doc](essence-doc/SKILL.md)
- [essence-pr](essence-pr/SKILL.md)
- [fleet-audit-patterns](fleet-audit-patterns/SKILL.md)
- [go-defensive](go-defensive/SKILL.md)
- [humanize](humanize/SKILL.md)
- [improve](improve/SKILL.md)
- [intake-implementation-workflow](intake-implementation-workflow/SKILL.md)
- [ios-rendering-protocol](ios-rendering-protocol/SKILL.md)
- [linkedin-lead-gen-outreach](linkedin-lead-gen-outreach/SKILL.md)
- [markdown-mode-router](markdown-mode-router/SKILL.md)
- [meeting-to-action](meeting-to-action/SKILL.md)
- [mobile-forensics](mobile-forensics/SKILL.md)
- [model-cost-estimator](model-cost-estimator/SKILL.md)
- [nextjs-nebula-miniapp](nextjs-nebula-miniapp/SKILL.md)
- [owasp-top-10](owasp-top-10/SKILL.md)
- [product-clone-research](product-clone-research/SKILL.md)
- [product-reverse-engineering](product-reverse-engineering/SKILL.md)
- [prompt-technique-router](prompt-technique-router/SKILL.md)
- [qmd](qmd/SKILL.md)
- [repo-settings-bootstrap](repo-settings-bootstrap/SKILL.md)
- [resume-ats-pdf-optimizer](resume-ats-pdf-optimizer/SKILL.md)
- [senior-devops](senior-devops/SKILL.md)
- [skill-router-v2](skill-router-v2/SKILL.md)
- [tdd-workflows-tdd-cycle](tdd-workflows-tdd-cycle/SKILL.md)
- [teaching-lesson-plan](teaching-lesson-plan/SKILL.md)
- [web-scraper](web-scraper/SKILL.md)
