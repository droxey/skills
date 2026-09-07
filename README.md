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
