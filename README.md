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


## musexmachine-mcp-codex-env

Source: `musexmachine/mcp`

Sample prompt:
```text
Use the musexmachine-mcp-codex-env skill to create and validate a Codex-ready environment for musexmachine/mcp.
```

## code

Source: `hacker-news-comment (workflow pattern)`

Sample prompt:
```text
Use the code skill to execute a refactor with plan iteration, spec-first thinking, tests-first implementation, manual verification, review, mutation testing, and docs updates.
```

## reasoning-router

Source: `reasoning-router/`

Sample prompt:
```text
Use the reasoning-router skill before beginning the task to select the lowest sufficient available reasoning mode.
```

## product-reverse-engineering

Source: `product-reverse-engineering/`

Sample prompt:
```text
Use $product-reverse-engineering to route this product analysis or rebuilding request to the correct specialist with the required safety gates and reviewed handoffs.
```

## skill-maturity

Every first-party skill declares a `maturity` level in its `SKILL.md` frontmatter and carries the required Purpose, Inputs, Outputs, Example, Success criteria, and Maturity sections. Levels: `0` Intent, `1` Determinism (script/structured asset), `2` Stability (unit tests), `3` Safety and Scale (agents/ interface or safety section). See `docs/skill-maturity-standard.md`.

Validate and harden the library:

```bash
python3 tools/validate_skills.py          # strict check of a skill directory's frontmatter + sections
python3 tools/harden_skills.py            # batch-add maturity + required sections to live first-party skills
python3 tools/finalize_skills.py          # harden the essence meta-skills and sweep-validate all skills
python3 -m unittest tools.test_validate_skills
```

### Use this repository with any agent harness

[![Last updated](https://img.shields.io/github/last-commit/droxey/skills?label=last%20updated)](https://github.com/droxey/skills/commits/main)
[![Skills](https://img.shields.io/badge/skills-34-blue)](#skills)

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
