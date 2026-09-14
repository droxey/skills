# Agent Run: Cross-Platform Subagent Plan

## Goal

Produce a safe, implementation-ready plan to optimize every skill present in this checkout for cross-platform subagent use.

## Repository review

- Read the conversation instructions and repository `AGENTS.md`.
- Read root `README.md`, `CLAUDE.md`, `settings.json`, and `skills-manifest.json`.
- Read both tracked skill definitions.
- Reviewed existing plans, run logs, router references, fixtures, and tests.
- Found no prototype, mockup, diagram, or roadmap files.
- Read the system `skill-creator` guidance for updating skills.

## Existing git status

`git status --short --branch` returned a clean `work` branch before changes.

## Task chosen

Add one planning document and this required run record. Do not modify skill behavior in a planning-only request.

This is the smallest safe task because the requested optimization spans multiple skills, changes orchestration semantics, and needs explicit fallback and safety contracts before implementation.

## Best practices

- Use capability-based delegation language instead of vendor-specific tool names.
- Delegate independent, read-only units with isolated inputs and explicit outputs.
- Keep the parent responsible for gates, integration, verification, and final delivery.
- Bound concurrency and preserve a serial fallback.
- Use one artifact owner to avoid concurrent-write conflicts.
- Test delegation-enabled and delegation-unavailable behavior.

## Strategy

1. Scope current coverage to tracked `SKILL.md` files.
2. Define a shared semantic contract and tests.
3. Plan one implementation change per skill.
4. Preserve teaching generation order and router phase gates.
5. Defer absent manifest entries until their source of truth is resolved.

## Files changed

- Added `docs/superpowers/plans/2026-08-03-cross-platform-subagent-optimization.md`.
- Added `docs/agent-runs/2026-08-03-1657-cross-platform-subagent-plan.md`.

## Commands run and results

- `find .. -name AGENTS.md -print` — passed; found only the repository instructions.
- `rg --files -g '!node_modules'` — passed; inventoried repository files.
- `git status --short --branch` — passed; clean baseline on `work`.
- `git log -5 --oneline --decorate` — passed; reviewed recent history.
- `cat`/`find`/`rg` review commands — passed; reviewed root docs, skills, plans, references, fixtures, and tests.
- `cat /opt/codex/skills/.system/skill-creator/SKILL.md` — passed; reviewed skill-update best practices.
- `pytest -q` — passed at baseline: 19 tests passed.
- `git diff --check` — passed with no whitespace errors.
- `python3 /opt/codex/skills/.system/skill-creator/scripts/quick_validate.py dani-roxberrys-teaching-voice` — unavailable because the environment lacks the `yaml` Python module; no existing skill files were changed.
- `python3 /opt/codex/skills/.system/skill-creator/scripts/quick_validate.py product-reverse-engineering` — unavailable for the same environment limitation; no existing skill files were changed.

## Diff summary

Documentation only: one implementation plan plus one audit record. No skill, dependency, configuration, generated file, or lockfile changed.

## Assumptions

- “Every skill in this repo” means skill folders present and tracked in this checkout, not manifest entries whose folders are absent.
- “On any platform” means platform-neutral capability detection with a serial fallback, not identical vendor APIs.
- Subagents should improve independent work, not be forced onto tasks where coordination costs or safety risks outweigh the benefit.

## Risks

- The manifest/check-out mismatch can make repository-wide coverage appear broader than it is.
- A blanket subagent mandate could increase cost and reduce quality; the plan therefore uses conditional delegation.
- Forward tests cannot be completed until implementation exists.

## Rollback

Revert the planning commit; no runtime behavior is affected.

## Commit/push status

Commit is requested and will follow final validation. Pull-request metadata will be recorded after the commit. No push is possible because no remote is configured.
