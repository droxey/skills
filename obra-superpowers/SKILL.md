---
name: obra-superpowers
description: Use automatically for coding, building, debugging, refactoring, code review, or multi-step software work. Applies the Obra Superpowers methodology: clarify goals, write a short spec, plan small TDD-oriented tasks, execute deliberately, verify with evidence, and finish cleanly.
created_at: '2026-05-18T14:57:00+00:00'
updated_at: '2026-05-18T14:57:00+00:00'
---

# Obra Superpowers

A formal Nebula skill for applying the Obra Superpowers software development methodology automatically during engineering work.

## Use this skill when

Use this skill automatically when the user asks for any of the following:

- Build, implement, modify, refactor, or debug code.
- Create a feature, fix a bug, or change project behavior.
- Review code, prepare a branch, open a PR, or finish development work.
- Execute a multi-step technical task where careless changes could create regressions.
- Investigate failing tests, broken deployments, unexpected behavior, or production issues.
- Coordinate implementation across multiple independent files, tasks, repositories, or agents.

Do not use this skill for purely conversational, writing-only, or simple factual questions unless the answer turns into software implementation work.

## Core rule

Do not jump straight into code for non-trivial engineering tasks. First understand what the user is trying to accomplish, then move through design, planning, execution, review, and verification.

For tiny, obvious edits, keep the workflow lightweight, but still verify the result.

## Default workflow

1. **Clarify the objective**
   - Restate the desired outcome.
   - Identify constraints, affected systems, acceptance criteria, and anything that must not change.
   - Ask only blocking questions. If the path is obvious, proceed with reasonable assumptions.

2. **Write a short spec**
   - Capture the intended behavior, scope, non-goals, and acceptance criteria.
   - Keep it chunked and easy to review.
   - For ambiguous or risky work, get user confirmation before implementation.

3. **Create an implementation plan**
   - Break the work into small, reviewable tasks.
   - Prefer tasks that can be completed and verified independently.
   - Emphasize YAGNI, DRY, and true red-green-refactor TDD where tests are practical.
   - Include exact files, tests, commands, and expected outcomes when making a written plan.

4. **Run a quick risk review**
   - What could fail in production?
   - What dependency or state assumption is weakest?
   - What signal would show a regression?
   - How can the change be rolled back quickly?

5. **Execute task-by-task**
   - Prefer test-first for risky logic changes.
   - Make the smallest change that satisfies the current task.
   - Avoid unrelated refactors or opportunistic improvements.
   - Use isolated branches/workspaces when changing repositories.

6. **Review before claiming done**
   - Check the implementation against the spec.
   - Check code quality: naming, boundaries, duplication, error handling, and test coverage.
   - If using subagents, review their work for both spec compliance and code quality before continuing.

7. **Verify with evidence**
   - Run the relevant tests, linters, builds, or smoke checks.
   - Do not say "fixed", "done", or "passing" without verification output or a clear explanation of why verification could not be run.
   - If verification fails, diagnose the cause before changing code again.

8. **Finish cleanly**
   - Summarize what changed, how it was verified, and any follow-up risks.
   - For git work, show the current branch/status and preserve user changes.
   - Do not merge, delete branches, or discard work without explicit confirmation.

## Skill routing

When a more specific Superpowers skill is available, use it for that phase:

- **Brainstorming/design**: before implementing new features or unclear changes.
- **Writing plans**: after a spec exists and before multi-step implementation.
- **TDD**: before writing behavior-changing code.
- **Systematic debugging**: when tests fail, bugs appear, or behavior is unexplained.
- **Parallel agents**: when independent investigations can run concurrently.
- **Subagent development**: when a written plan has independent implementation tasks.
- **Requesting code review**: before integration or PR creation.
- **Receiving code review**: when review feedback arrives.
- **Verification before completion**: before claiming work is done.
- **Finishing a development branch**: after implementation and verification are complete.

If those specific skills are not installed, apply the relevant section of this skill directly.

## Red flags

Slow down and apply the full workflow if you notice any of these conditions:

- The task touches auth, payments, data deletion, migrations, cron, deployment, secrets, or infrastructure.
- The change spans multiple files or repositories.
- The user says something is broken but the root cause is not known.
- Tests are failing for an unclear reason.
- You are tempted to say "probably", "should work", or "looks fixed" without running verification.
- You are about to refactor unrelated code.
- You are about to skip tests because the change seems small.

## Lightweight mode

If the user asks for speed, or the change is truly tiny:

1. State the minimal plan in one sentence.
2. Make the smallest safe change.
3. Run the narrowest useful verification.
4. Summarize briefly.

Do not use lightweight mode for risky production-impacting work.

## Output expectations

Keep user-visible updates concise:

- Lead with the current outcome.
- Mention only useful process details.
- Report verification honestly.
- If blocked, say exactly what is needed to continue.
