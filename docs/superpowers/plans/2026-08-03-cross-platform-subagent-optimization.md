# Cross-Platform Subagent Optimization Plan

**Date:** 2026-08-03

**Status:** Implemented with Nebula-first compatibility

**Scope:** The two tracked skills: `dani-roxberrys-teaching-voice` and `product-reverse-engineering`

## Implementation outcome

The implementation follows the plan with these Nebula-specific corrections:

- Nebula installs one `SKILL.md`, so every runtime rule is self-contained. Bundled repository references remain maintainer documentation only.
- Nebula's orchestrator performs automatic delegation to available workspace agents. Skills request bounded, independent work semantically and do not assume spawn, join, message, or cancel tool names.
- Each skill documents its `@skill:<name>` invocation while still allowing Nebula to select it automatically.
- Delegation is limited to three independent, read-only units, one owner per artifact, parent review, minimal context, and a serial fallback.
- Shared agents can act through their owner's connected accounts, and Nebula's safety gate is off by default. The skills therefore keep credentials and consequential actions out of worker handoffs and retain explicit approval gates regardless of platform settings.

Compatibility is enforced by `tests/test_nebula_skill_contract.py`; the product router's existing contract tests also require its safety and dependency gates to remain in the uploadable entry file.

## Goal

Make every tracked skill able to delegate independent work to subagents on any agent platform that exposes a delegation capability, while preserving correct behavior on platforms that do not.

## Constraints

- Keep instructions platform-neutral. Describe capabilities such as spawn, message, join, and cancel instead of naming vendor tools.
- Do not require delegation for trivial, sequential, stateful, destructive, credential-bearing, or tightly coupled work.
- Preserve each skill's output order, safety gates, review points, and source-of-truth rules.
- Treat subagent output as untrusted draft material. The parent agent owns integration, verification, and the final answer.
- Bound fan-out and give every worker a concrete deliverable, isolated inputs, and a stop condition.
- Fall back to the existing serial workflow when delegation is unavailable or would cost more than it saves.
- Change and validate one skill at a time. Do not combine the two migrations in one implementation change.

## Repository review

- Git tracks two `SKILL.md` files, although `skills-manifest.json` lists many catalog entries whose folders are absent from this checkout. This plan therefore covers tracked skills only; absent catalog entries need restoration or a separate source-of-truth decision before they can be reviewed.
- `dani-roxberrys-teaching-voice` has separable generation and audit work, but its examples → slides → notes order creates dependencies that must remain serial between stages.
- `product-reverse-engineering` already routes atomic phases and requires reviewed handoffs. Parallel execution must not bypass its authorization, dependency, provenance, license, or rights gates.
- Existing product-router tests provide a strong regression baseline. The teaching-voice skill has no automated contract tests yet.

## Best-practice delegation contract

Add the same concise semantic contract to each skill, adapted to its workflow:

1. **Detect capability:** Use subagents only when the runtime can start isolated workers and collect their results. Otherwise continue serially without degrading the deliverable.
2. **Find a safe cut:** Delegate only independent, read-only work with explicit inputs and output schemas. Keep ordering-sensitive synthesis with the parent.
3. **Minimize context:** Pass only task-local sources, constraints, destination paths, and acceptance criteria. Never pass secrets, credentials, session material, or unrelated private data.
4. **Set ownership:** Assign one owner per artifact. Do not let multiple workers edit the same file.
5. **Bound concurrency:** Default to at most three workers and reduce that limit when the platform or task has tighter constraints.
6. **Join before synthesis:** Wait for required workers, review their artifacts, resolve conflicts, and verify claims before advancing a gate or publishing output.
7. **Fail safely:** Retry once only when useful; otherwise complete the unit in the parent or mark it blocked. Never silently omit a required artifact.
8. **Record provenance:** Note delegated unit, inputs, worker result, review status, and any parent corrections in the run summary.

This capability-based language is portable across platforms and avoids brittle tool-name instructions. It also prevents the common anti-pattern of spawning workers merely because the runtime supports them.

## Approach

### Phase 1 — Add an executable delegation contract

**Task:** Establish repository-level tests before modifying either skill.

**Files:**

- Create `tests/test_subagent_contract.py`.

**Checks:**

- Enumerate tracked `SKILL.md` files rather than trusting absent manifest paths.
- Require each skill to state capability detection, serial fallback, bounded concurrency, parent review, and no shared-file ownership.
- Require domain-specific invariants: teaching asset order for the teaching skill; gated, reviewed phase handoffs for the router.
- Keep assertions semantic enough to allow clear wording improvements without pinning entire paragraphs.

**Exit criteria:** The new tests fail for missing delegation contracts while all existing tests retain their baseline result.

### Phase 2 — Optimize `dani-roxberrys-teaching-voice`

**Task:** Add safe delegation around its dependency chain without changing lesson authority.

**Files:**

- Modify `dani-roxberrys-teaching-voice/SKILL.md`.

**Delegation design:**

- Keep the parent responsible for normalizing objectives and freezing the lesson brief.
- Optionally fan out independent example candidates by objective; the parent reviews and merges them into `examples.md`.
- Generate `slides.md` only after examples are accepted, then generate `speaker-notes.md` only after slides are accepted.
- After all required assets exist, run privacy, drift, and voice audits in parallel because they are read-only checks over stable artifacts.
- Give each audit a structured finding format: severity, artifact, location, evidence, and proposed correction.
- Keep final corrections and release approval with the parent.

**Tests:**

- Run the repository contract suite.
- Validate the skill with `quick_validate.py`.
- Forward-test once with delegation available and once with a simulated no-delegation runtime; compare required artifacts and ordering.

**Rollback:** Revert this skill's single implementation commit. The original serial workflow remains the fallback throughout.

### Phase 3 — Optimize `product-reverse-engineering`

**Task:** Permit parallel evidence work only inside a selected, authorized phase.

**Files:**

- Modify `product-reverse-engineering/SKILL.md`.
- Modify `product-reverse-engineering/references/routing-contract.md` only if the detailed handoff schema no longer fits compactly in `SKILL.md`.
- Extend existing router cases and tests.

**Delegation design:**

- Keep route selection, authorization, dependency verification, and phase gating with the parent.
- Do not parallelize different pipeline phases; complete and review one phase before the next.
- After a route passes its gates, allow workers to inspect independent evidence partitions, such as separate public pages or distinct repository subsystems.
- Preserve destination-native workflows. The router may recommend delegation but must not fabricate support when the destination or platform lacks it.
- Require evidence labels and source locations in every worker handoff.
- Prohibit workers from authenticating, executing binaries, changing permissions, purchasing, publishing, or performing other consequential actions.
- Have the parent deduplicate observations, reconcile contradictions, apply rights and privacy gates, and approve the phase handoff.

**Tests:**

- Extend routing cases for safe fan-out, unavailable-subagent fallback, phase-order preservation, conflicting worker evidence, and prohibited consequential actions.
- Run all router unit and contract tests.
- Validate the skill with `quick_validate.py`.
- Forward-test a compound request and verify that phases remain serial even when evidence collection within a phase is parallel.

**Rollback:** Revert this skill's single implementation commit. Existing routing and safety tests remain the acceptance baseline.

### Phase 4 — Catalog reconciliation follow-up

**Task:** Do not edit absent skills. Open a separate decision item to either restore the manifest-listed skill folders or mark the manifest as an inventory of external/unavailable skills.

After that decision, apply Phases 1–3 to each restored skill in separate, reviewable changes. Do not weaken the tracked-file test to claim coverage for files that are not present.

## Validation matrix

| Scenario | Expected behavior |
|---|---|
| No delegation capability | Run the original serial workflow and produce the same required artifacts. |
| One independent unit | Keep it in the parent unless delegation has a clear quality or latency benefit. |
| Several independent, read-only units | Delegate with unique artifact ownership and a concurrency cap. |
| Ordered stages | Parallelize only within a stage; join and review before the next stage. |
| Worker failure | Retry once if useful, then recover serially or report a visible block. |
| Conflicting findings | Parent resolves from source evidence; do not majority-vote. |
| Sensitive or consequential action | Keep with the parent and enforce the skill's existing gate. |

## Risks and mitigations

- **Instruction bloat:** Keep the common contract short and move domain detail into existing workflow sections.
- **Platform incompatibility:** Specify capabilities and fallbacks, not tool calls or platform names.
- **Higher cost on small tasks:** Require a benefit check and bounded fan-out.
- **Context leakage:** Pass minimal task-local context and exclude sensitive material.
- **Inconsistent artifacts:** Use one owner per artifact and parent-only integration.
- **Safety-gate bypass:** Make routing, authorization, reviewed handoffs, and final approval non-delegable.
- **False catalog coverage:** Define current scope from tracked skill files and explicitly defer absent manifest entries.

## Recommended commit sequence

1. `test: define cross-platform subagent contract`
2. `feat: add safe teaching asset delegation`
3. `feat: add gated product analysis delegation`
4. Separate catalog reconciliation commits only after the source-of-truth decision

Each implementation commit should be independently revertible and leave the serial path operational.
