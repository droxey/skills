# Agent Run: Nebula Subagent Compatibility

## Goal

Implement safe subagent use in every checked-out skill and make each uploadable `SKILL.md` self-contained and compatible with Nebula.

## Initial status

- Branch `work` was clean at `7f67304`.
- The checkout contains two skill definitions: `dani-roxberrys-teaching-voice/SKILL.md` and `product-reverse-engineering/SKILL.md`.
- The latest commit contained a plan and run record but no skill implementation.

## Plan

1. Read repository instructions, skill-creator guidance, current skills, supporting references, fixtures, and tests.
2. Inventory and read every page in Nebula's public documentation sitemap.
3. Write failing compatibility tests before modifying skills.
4. Add Nebula-aware, platform-portable delegation while preserving teaching order and router safety gates.
5. Validate skills, run the full suite and Git checks, audit the diff, commit, and create a pull request.

## Nebula documentation audit

- Fetched `https://docs.nebula.gg/sitemap.xml`; it listed 55 URLs.
- Fetched all 55 URLs successfully with HTTP 200 and extracted their reader-visible content: 222,070 characters total.
- Cross-checked the crawl against `https://docs.nebula.gg/llms.txt` and read the complete machine-readable corpus at `https://docs.nebula.gg/llms-full.txt` (6,256 lines; 41,039 words; 284,107 bytes).
- Nebula skills are single `SKILL.md` files installed by upload, direct URL, or registry. They can be scoped to Nebula or one agent, selected automatically, invoked as `@skill:<name>`, and appear as slash commands.
- Nebula's personal orchestrator coordinates and automatically delegates to available specialized agents. The public docs do not expose a skill-level spawn/join/cancel API, so the implementation uses semantic delegation instructions rather than vendor tool names.
- Threads hold shared context and files; thread attachments remain thread-scoped. Shared agents run through their owner's connected accounts. Connections and workspace visibility therefore constrain delegation.
- The safety gate pauses risky actions only when enabled and is off by default. Skill-level authorization and approval rules remain mandatory.

## Changes

- Added repository-wide tests for Nebula frontmatter, single-file self-containment, invocation, delegation, bounded fan-out, artifact ownership, parent review, serial fallback, sensitive context, and consequential actions.
- Added a delegation contract and safe generation/audit fan-out to the teaching skill while preserving `examples.md → slides.md → speaker-notes.md`.
- Made the product router self-contained by embedding its pinned dependency registry and added safe evidence partitioning without parallelizing phases or weakening gates.
- Updated the prior plan with the implemented Nebula-specific decisions.

## Validation

- The new compatibility suite failed in five tests before implementation, proving the missing behavior.
- `pytest -q` passed: 24 tests.
- Both `quick_validate.py` checks passed: `Skill is valid!`.
- `python -m compileall -q product-reverse-engineering/tests tests` passed.
- The documentation audit check passed for 55/55 sitemap pages and the 6,256-line `llms-full.txt` corpus.
- `git diff --check` passed.
- The unused/commented-out code scan found no `TODO`, `FIXME`, `XXX`, `HACK`, or commented-out Python statements.

## Risks and unverified edges

- Compatibility covers the 55 public pages advertised by Nebula's sitemap on 2026-08-03. Authenticated, unpublished, or deployment-specific behavior was not available for inspection.
- Nebula decides which workspace agent receives delegated work; skills cannot guarantee a particular agent exists or is accessible. The serial fallback preserves completion when no suitable delegate is available.
- The pinned external skill records were not refreshed in this change. Existing fail-closed dependency and license gates remain in force.

## Rollback

Revert the implementation commit. This restores the prior serial-only skill behavior and plan-only documentation.

## Commit and pull request

Commit and pull-request metadata are created after this record is finalized.
