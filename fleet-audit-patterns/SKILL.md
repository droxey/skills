---
name: fleet-audit-patterns
description: Use when auditing a fleet of agents for toolkit overlap, duplication, and coverage gaps.
  on 2+ agents), orphan agents (no goals or disabled), superset/subset relationships
  suggesting merges, and agents with minimal unique value.'
created_at: '2026-05-15T02:59:37.055072+00:00'
updated_at: '2026-05-15T02:59:37.055072+00:00'
maturity: 0
---

# Fleet Audit Patterns

## What to check every audit

1. **Toolkit overlap** — When 2+ agents share the same core toolkit (e.g. both have `builtin:code` + `builtin:web-scraping`), flag for merge review. BUT: toolkit overlap alone is not sufficient. "model-scout" (AI model research) and "manifestor" (Human Design teaching) share the same `builtin:code` + `builtin:web-scraping` pair but serve entirely different domains — no merge value. Always cross-check agent descriptions, goals, and domain before recommending a merge.
2. **Orphan agents** — Agents with zero goals or that are disabled. Recommend retirement.
3. **Superset/subset relationships** — If one agent's toolkits are a strict superset of another's, suggest merging the subset into the superset.
4. **Minimal unique value** — An agent with only `builtin:code` and no distinctive API connections or domain expertise may not justify its own agent slot.
5. **Stale goals** — Goals that are vague, out of date, or clearly no longer relevant.

## When to recommend vs. when to act

- **Recommend** — When changes would benefit from user input (merge two agents, retire an agent). Surface via action-watchdog.
- **Act** — When something is clearly wrong (an agent has broken toolkits, no goals, or is a duplicate). Update the agent directly.

## Trigger naming convention
- Use format: `[Frequency] Short Description` — e.g. `Weekly Fleet Audit`

## Delivery
- Audit findings go to the user's preferred delivery channel (default: email if the trigger's steps include it).
- For recurring triggers, the thread post IS the delivery — only add email/Slack steps when the user explicitly requested out-of-band delivery.

## Maturity

Level 0 - Intent. Substantiated by the written contract only; no runnable asset or tests yet.

## Purpose

Run a consistent fleet audit covering overlap, duplication, and gaps.

## Inputs

The agent roster and each agent's toolkits, prompts, and usage.

## Outputs

An audit report listing overlaps, gaps, and consolidation recommendations.

## Example

Compare all agents' toolkits and flag any pair with redundant coverage plus any capability nobody owns.

## Success criteria

Every overlap, gap, and redundant-toolkit case in the fleet is named with a recommendation.