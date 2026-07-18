# Reasoning Router

A portable agent skill for selecting the **lowest sufficient GPT-5.6 reasoning mode** for a task.

The policy distinguishes three different kinds of capability:

- **Reasoning effort:** Medium, High, Extra High, and Max.
- **Model judgment:** Pro uses the higher-capability Pro option where available.
- **Parallel execution:** Ultra coordinates multiple independent workstreams where supported.

These are not interchangeable. A harder task does not automatically require Pro, and a large task does not automatically require Ultra.

## Rules

1. Classify the task before substantive work.
2. Select the lowest mode likely to complete it correctly.
3. Prefer **High to create** and **Extra High to audit**.
4. Use **Max** only for one exceptionally entangled reasoning problem.
5. Use **Pro** when the problem frame or consequential judgment is the main risk.
6. Use **Ultra** only when at least three independent workstreams can proceed in parallel.
7. Reassess after failed verification, contradictory evidence, or a material change in scope.
8. Respect an explicit user-selected mode.
9. Inspect the current surface before claiming a mode is available.
10. Apply an explicit fallback when the preferred mode is unavailable.

## Decision signals

| Signal | Lower effort | Higher effort |
|---|---|---|
| Scope | One bounded deliverable | Cross-component system or broad program |
| Uncertainty | Solution shape is known | Architecture or framing is unresolved |
| Consequence | Easy to reverse | Expensive, risky, or difficult to reverse |
| Verification | Local check | Audit, proof, or adversarial validation |
| Entanglement | Few independent constraints | Many tightly coupled constraints |
| Judgment | Execute inside a known frame | Decide whether the frame itself is correct |
| Parallelism | One coherent problem | Several independent workstreams |

## Mode guide

### Medium

Use for bounded, familiar work with straightforward verification.

Examples:

- Rewrite one paragraph under explicit constraints.
- Summarize a supplied document.
- Implement a small function with existing tests.
- Update one configuration entry and run a local check.

Do not move to High merely because the output is long.

### High

Use for multi-step synthesis, architecture, cross-component work, or meaningful debugging.

Examples:

- Compare two frameworks for a defined production system.
- Sequence a multi-part course or training program.
- Diagnose a failure spanning an API, worker, and database.
- Design shared configuration across several compatible tools.

High is the normal default for substantive engineering and planning.

### Extra High

Use when the work requires audit-quality reasoning, difficult verification, or careful reconciliation of subtle constraints.

Examples:

- Audit whether a benchmark measures its stated construct.
- Review an infrastructure bootstrap for idempotency and rollback.
- Perform a security, authorization, concurrency, or data-integrity review.
- Reconcile a design review with an existing implementation.

A useful pattern is **High to build, Extra High to challenge**.

### Max

Use for the deepest possible reasoning on one coherent problem when the active surface supports it.

Examples:

- Prove the cause of an intermittent distributed-state failure.
- Produce an exhaustive failure analysis after earlier attempts were inconclusive.
- Migrate configuration across incompatible systems without losing state.
- Establish whether a complex evaluation methodology is logically valid.

Max is not a substitute for parallel agents. When the task splits cleanly, use Ultra instead.

### Pro

Use when stronger judgment matters more than simply reasoning longer inside the current frame.

Examples:

- Decide whether a foundational architecture should exist in its proposed form.
- Determine whether the stated product problem is the real problem.
- Adjudicate conflicting technical, organizational, and product evidence.
- Approve a consequential security or data-governance design.

Use Extra High when the frame is known and the primary need is rigorous review. Use Pro when the frame itself may be wrong.

### Ultra

Use when several independent specialist tracks can run concurrently and then be synthesized.

Examples:

- Audit multiple repositories in parallel.
- Compare a broad technology ecosystem across architecture, operations, security, and cost.
- Review a system through independent backend, frontend, accessibility, testing, and deployment tracks.
- Research several market, technical, and implementation questions concurrently.

Ultra is not “more Max.” Max deepens one line of reasoning; Ultra coordinates multiple lines of work.

## Boundary rules

### Medium versus High

Use Medium when the solution shape is already known. Use High when the solution shape must be discovered or reconciled across components.

### High versus Extra High

Use High to produce a design or implementation. Use Extra High to audit assumptions, search for failure modes, or validate difficult claims.

### Extra High versus Max

Use Extra High for most demanding professional work. Use Max only when one problem is exceptionally entangled, proof is required, or Extra High has already been insufficient.

### Max versus Pro

Use Max when the frame is accepted and the task is a very hard reasoning problem. Use Pro when deciding whether the frame, premise, or foundational choice is correct.

### Pro versus Ultra

Use Pro for one difficult cohesive judgment. Use Ultra for multiple independent investigations requiring synthesis.

## Availability and fallbacks

The skill separates the **desired conceptual mode** from the **selected available mode**.

| Desired | Fallback order |
|---|---|
| Ultra | Ultra → Pro → Extra High → High → Medium |
| Pro | Pro → Extra High → High → Medium |
| Max | Max → Extra High → High → Medium |
| Extra High | Extra High → High → Medium |
| High | High → Medium |
| Medium | Medium |

Always inspect the current product surface because plan, workspace, and rollout availability can change.

## Use the deterministic selector

The skill can route directly from the policy. The included script is useful for tests, automation, or ambiguous cases.

```bash
python scripts/select_reasoning.py \
  --scope cross-component \
  --uncertainty high \
  --consequence high \
  --verification proof \
  --entanglement exceptional \
  --repeated-failure \
  --available medium,high,extra-high,max,pro,ultra
```

Example result:

```json
{
  "desired": "max",
  "fallback_used": false,
  "selected": "max"
}
```

Run the built-in checks:

```bash
python scripts/select_reasoning.py --self-test
pytest -q
```

## Installation

Install into any compatible global skills directory:

```bash
./scripts/install.sh ~/.codex/skills
```

Or provide an explicit runtime directory:

```bash
./scripts/install.sh /path/to/global/skills
```

The installed path is `<target>/reasoning-router/`.

To make invocation mandatory in an agent harness, add this global instruction:

```markdown
Before every substantive task, load and follow the `reasoning-router` skill to select the lowest sufficient available reasoning mode.
```

## Common mistakes

| Mistake | Correction |
|---|---|
| “This is important, so use Pro.” | Importance alone does not imply framing risk or a need for a stronger model. |
| “This is large, so use Ultra.” | Ultra requires independent workstreams, not just size. |
| “Max is always better than Extra High.” | Max costs more time and is justified only by exceptional single-problem entanglement. |
| “Pro is just the next effort level.” | Pro changes the model capability; it is not merely more reasoning effort. |
| “The requested mode exists everywhere.” | Inspect the active product surface and apply a documented fallback. |
