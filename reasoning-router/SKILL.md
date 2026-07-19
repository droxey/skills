---
name: reasoning-router
description: Use when beginning any task to choose the lowest sufficient GPT-5.6 reasoning level or execution mode, especially when complexity, consequence, verification depth, framing uncertainty, prior failure, or parallel work may change the correct choice.
---

# Reasoning Router

## Core rule

Select the **lowest sufficient available mode**. Classify the task before substantive action, then reassess after new evidence, failed verification, or contradictory results.

An explicit user-selected mode is authoritative. Never claim to activate a mode the current product surface does not expose.

## Classify the task

Assess seven observable signals:

1. **Scope:** bounded, multi-step, cross-component, or broad program.
2. **Uncertainty:** known solution shape versus unresolved architecture or framing.
3. **Consequence:** cost of a wrong answer or change.
4. **Verification:** easy check, multi-step validation, audit, or proof.
5. **Entanglement:** number of tightly coupled constraints in one problem.
6. **Judgment:** whether choosing the right frame matters more than reasoning longer inside a fixed frame.
7. **Parallelism:** number of genuinely independent workstreams.

## Decision order

| Choose | When | Generic example |
|---|---|---|
| **Ultra** | Three or more independent workstreams need coordinated synthesis. | Review backend, frontend, security, testing, and operations in parallel. |
| **Pro** | Consequential judgment or problem framing dominates. | Decide whether a foundational architecture solves the right problem. |
| **Max** | One exceptionally entangled problem requires proof, exhaustive failure analysis, or recovery after Extra High was insufficient. | Prove the cause of an intermittent distributed-state failure. |
| **Extra High** | Audit-quality work, high consequence, difficult verification, security/concurrency analysis, or subtle interacting constraints. | Audit a benchmark methodology or authorization design. |
| **High** | Complex multi-step work, architecture, cross-component debugging, or meaningful synthesis. | Compare two frameworks for a defined production system. |
| **Medium** | Bounded, familiar work with straightforward verification. | Rewrite one section or implement a small tested function. |

Apply the table top-down. Ultra is about parallel work, Pro is about stronger judgment, and Max is about deeper single-problem reasoning.

## Availability fallbacks

Inspect the active picker, API, or workspace configuration.

- Ultra unavailable → Pro; otherwise Extra High and manually divide the work.
- Max unavailable → Extra High.
- Pro unavailable → Extra High and note the judgment limitation when material.
- Extra High unavailable → High.
- High unavailable → Medium.

Standard ChatGPT and Work/Codex surfaces may expose different options. Availability changes by plan, workspace, and rollout.

## Escalation rules

Escalate one level when verification fails for a reasoning-related cause, material constraints conflict, or the current framing becomes uncertain. Do not escalate merely because the task is important, long, or verbose.

## Red flags

- Choosing Pro as a prestige label.
- Choosing Ultra for one tightly coupled problem.
- Choosing Max when several independent tracks should be parallelized.
- Starting at the highest mode without testing whether a lower mode is sufficient.
- Silently substituting an unavailable mode.

When uncertain, run `python scripts/select_reasoning.py --help` from this skill directory.
