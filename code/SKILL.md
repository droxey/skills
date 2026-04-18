---
name: code
description: "Structured workflow for writing or refactoring code with an AI agent: discuss, iterate on a plan, capture a spec, implement tests-first, manually verify behavior, review with another pass, run mutation testing, and update docs/artifacts. Use when building non-trivial code changes where quality gates and regression resistance matter."
---

# Code

Use this workflow to deliver reliable code changes without depending on special frameworks.

## Do Not Use For

- Docs-only edits (typos, formatting, wording-only README updates).
- Translation, summarization, or general writing tasks with no code change.
- One-off snippet/Q&A requests that do not need plan/spec/test/verify gates.
- Narrow debugging asks when the user only wants a quick hypothesis or fix.

## Core Flow

1. **Discuss the change with an agent**
   - Clarify scope, constraints, and non-goals.
   - Surface unknowns and risks before coding.

2. **Iterate on the implementation plan**
   - Produce a step-by-step plan.
   - Review and revise until the plan is concrete enough to execute.

3. **Write the spec**
   - Capture acceptance criteria, edge cases, and out-of-scope items.
   - Use the spec as the source of truth while implementing.

4. **Implement tests first, then code**
   - Add or update tests that encode the spec.
   - Implement the minimum code needed to satisfy tests.

5. **Manually verify behavior**
   - Exercise key user paths and edge cases outside automated tests.
   - Confirm real-world behavior matches the spec.

6. **Review and mutate**
   - Run a review pass (second agent, manual review, or both).
   - Perform mutation testing: introduce plausible bugs and confirm tests fail.
   - Strengthen tests for any mutant that survives.

7. **Update docs and artifacts**
   - Update READMEs, runbooks, changelogs, or design docs impacted by the change.
   - Keep operational and onboarding docs aligned with implementation.

8. **Close out**
   - Confirm acceptance criteria are met.
   - Summarize what changed, how it was verified, and remaining risks.

## Mutation Testing Playbook (LLM-assisted)

Use this lightweight loop when a mutation framework is unavailable:

1. Pick 3-10 high-risk behaviors from the spec.
2. Ask an agent to create one plausible bug per behavior (off-by-one, wrong branch, skipped validation, stale state, etc.).
3. Apply one mutation at a time.
4. Run the test suite.
5. If tests pass, treat the mutant as a coverage gap; add/improve tests.
6. Re-run until tests fail for the mutant.
7. Revert the mutation and proceed to the next one.

Prefer deterministic, easy-to-revert mutations. Do not batch many mutants together.

## Scoring and Evidence Gate

Use this gate before marking work complete.

### Mutation Testing Threshold

- Treat changes as **medium/large** when they modify production logic across multiple files, control-flow branches, or externally visible behavior.
- Run at least **5 mutants** across high-risk behaviors for medium/large changes.
- Require a **mutant kill rate >= 80%** before closeout.
- For surviving mutants, either:
  - add tests until the mutant is killed, or
  - document why the survivor is acceptable and what follow-up is required.

### Required Evidence Template

Record this block in the final report:

```text
Mutation Testing Evidence
- Spec areas targeted:
- Mutants introduced (id + bug type + location):
- Mutants killed:
- Mutants survived:
- Kill rate (%):
- Tests added/updated:
- Justified survivors and follow-ups:
```

## Scaling Guidance

- **Trivial change**: compress steps 1-3 into a short plan and brief spec.
- **Medium change**: execute every step once.
- **Large change**: split into milestones, each with its own plan/spec/test/verify/review cycle.

## Output Checklist

For each completed task, produce:

- Final spec (or spec diff).
- Test evidence (what ran, what passed/failed).
- Manual verification notes.
- Mutation testing notes (mutants tried and outcomes).
- Documentation/artifact updates.
- Residual risks and follow-ups.
