---
name: superpowers-subagent-dev
description: Use when executing implementation plans with independent tasks - coordinates task execution by dispatching subagents per task with verification checkpoints and two-phase review.
---

# Superpowers Subagent Development

## Overview

Execute plans by dispatching independent subagents per task, with two-phase review after each task: first spec compliance review, then code quality review.

**Why subagents:** Delegate tasks to specialized agents with isolated context. By precisely crafting instructions and context, you ensure they stay focused and succeed. Subagents should not inherit session history — construct exactly what they need.

**Core principle:** Fresh subagent per task + two-phase review (spec compliance → code quality)

## OpenClaw Adaptation

Superpowers original is designed for Claude Code's Task/subagent cascade model. OpenClaw uses `sessions_spawn` to create independent sessions, without native cascading.

**OpenClaw adaptation:**
- Main agent acts as controller, coordinating all work
- Use `sessions_spawn(mode="run")` to dispatch one-shot task subagents
- Subagent results passed through session history or filesystem
- Reviews executed inline in main session (or spawn independent review sessions)
- Complex review tasks use `sessions_spawn`

## Usage Conditions

```
Have implementation plan?
  → Tasks mostly independent?
    → Work in current session?
      → Use subagent-dev (this skill)
    → Parallel independent sessions?
      → Use sessions_spawn parallel dispatch
  → Manual execution or brainstorm first
```

## Flow

### Per Task

1. **Read plan, extract all tasks**
   - Read plan file once
   - Extract all tasks with full text and context
   - Create task list

2. **Dispatch implementer subagent**
   ```
   Use sessions_spawn:
   - mode: "run" (one-shot task)
   - task: full task text + context
   - cwd: project directory
   ```

3. **Handle subagent questions**
   - If subagent asks → answer, provide context
   - Re-dispatch or continue

4. **Subagent implements, tests, commits, self-reviews**
   - Implementer completes work
   - Runs tests
   - Commits
   - Self-reviews

5. **Spec compliance review (main session inline or spawn)**
   - Check implementation meets spec in plan
   - Issues found → feedback to implementer → re-review
   - Passed → continue

6. **Code quality review**
   - Check code quality: DRY, naming, test design
   - Issues found → fix
   - Passed → continue

7. **Mark task complete, continue to next**

### After Tasks

All tasks complete:
- Do final code review
- Call `superpowers-finishing-branch` to complete work

## Model Selection

Use weakest model that can handle the task, saving cost and increasing speed:

| Task Type | Example | Model |
|-----------|---------|-------|
| Mechanical implementation | Isolated functions, clear spec, 1-2 files | Fast cheap model |
| Integration and judgment | Multi-file coordination, pattern matching, debugging | Standard model |
| Architecture design and review | Requires design judgment or broad codebase understanding | Strongest model |

## Handling Subagent Status

Subagents report one of four statuses. Handle appropriately:

**DONE:** Continue to spec compliance review.

**DONE_WITH_CONCERNS:** Implementer completed but flagged concerns. Read concerns before proceeding. If concerns involve correctness or scope, resolve before review.

**NEEDS_CONTEXT:** Implementer needs information not provided. Supply missing context and re-dispatch.

**BLOCKED:** Implementer cannot complete task. Evaluate blockage:
1. If context issue, provide more context and re-dispatch with same model
2. If task needs more reasoning, re-dispatch with stronger model
3. If task too large, break into smaller pieces
4. If plan itself is wrong, escalate to owner

**Never** ignore escalations or force same-model retry without changes.

## Red Flags

**Never:**
- Start implementation on main/master branch (without owner explicit approval)
- Skip reviews (spec compliance or code quality)
- Continue with unfixed issues
- Dispatch multiple implementer subagents simultaneously (conflicts)
- Let subagent read plan file (provide full text directly)
- Skip scene-setting context (subagent needs to understand where task fits)
- Ignore subagent questions (answer before letting them continue)
- Accept "close enough" spec compliance (review finds issues = not done)
- Skip review loop (review finds issues = implementer fixes = re-review)
- Let implementer self-review substitute for actual review (both needed)
- **Start code quality review before spec compliance passes** (wrong order)
- Continue to next task with open issues

## Integration

**Required workflow skills:**
- `superpowers-writing-plans` — Creates plans this skill executes
- `superpowers-finishing-branch` — Wrap-up after all tasks complete
- `superpowers-tdd` — Subagents follow TDD per task

**Alternative workflows:**
- `sessions_spawn` parallel dispatch — For parallel investigation of independent problems
- Sequential execution — Execute tasks in batches within main session
