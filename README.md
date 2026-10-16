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
Windows. It validates the catalog; Skill Sync manages distribution separately.
The validator checks all skill contracts. Tests cover the validator, hardening
helpers, routing evaluator, trigger evaluator, and the two Nebula-specific skills;
they do not prove every skill's live behavior.

The maintenance commands `python tools/harden_skills.py` and
`python tools/finalize_skills.py` rewrite skill files. Run them only when changing
the catalog, then inspect the diff and rerun validation.

### Skill Sync

Whenever adding a skill, install it and sync its validated package to
[Skill Sync](https://skillsync.com/docs/skills). Use the `skl` CLI; sign in with
`skl login` when required. Preview each upload, then upload privately:

```bash
skl skills upload /absolute/path/to/skill --dry-run
skl skills upload /absolute/path/to/skill
```

Verify the remote skill's files and report any blocked sync as incomplete. Remote
uploads are private by default. Preserve source attribution and licenses, and do
not overwrite a conflicting skill or publish it publicly without authorization.

`skl skills sync` compares workspace skills; with a name it pulls that skill and
never uploads. `skl sync` uploads conversation history and is outside this workflow.
Skillshare is a different product. The former script-based sync workflow is retired.

### Use this repository with any agent harness

[![Last updated](https://img.shields.io/github/last-commit/droxey/skills?label=last%20updated)](https://github.com/droxey/skills/commits/main)
[![Skills](https://img.shields.io/badge/skills-40-blue)](#skills)

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
- [drive-motivation](drive-motivation/SKILL.md)
- [essence](essence/SKILL.md)
- [essence-commit](essence-commit/SKILL.md)
- [essence-doc](essence-doc/SKILL.md)
- [essence-pr](essence-pr/SKILL.md)
- [fleet-audit-patterns](fleet-audit-patterns/SKILL.md)
- [gamification](gamification/SKILL.md)
- [gamification-loops](gamification-loops/SKILL.md)
- [go-defensive](go-defensive/SKILL.md)
- [hooked-ux](hooked-ux/SKILL.md)
- [humanize](humanize/SKILL.md)
- [improve](improve/SKILL.md)
- [intake-implementation-workflow](intake-implementation-workflow/SKILL.md)
- [ios-rendering-protocol](ios-rendering-protocol/SKILL.md)
- [linkedin-lead-gen-outreach](linkedin-lead-gen-outreach/SKILL.md)
- [markdown-mode-router](markdown-mode-router/SKILL.md)
- [meeting-to-action](meeting-to-action/SKILL.md)
- [microinteractions](microinteractions/SKILL.md)
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

The imported design skills preserve their upstream license in `UPSTREAM_LICENSE.txt`
and source commit, original file hashes, and local contract adaptations in `UPSTREAM.json`.
