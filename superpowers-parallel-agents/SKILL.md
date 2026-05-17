---
name: superpowers-parallel-agents
description: Use when facing 2 or more independent tasks that can be worked on without shared state - dispatches parallel subagents using sessions_spawn for concurrent independent work.
---

# Superpowers Parallel Agents

## Overview

When facing 2+ independent tasks, assign them to specialized parallel subagents that work concurrently. OpenClaw uses `sessions_spawn` to create independent sessions for parallel dispatch.

**Core principle:** One agent per independent problem domain, let them work concurrently.

## OpenClaw Adaptation

Superpowers original uses Claude Code's `Task` tool for concurrent dispatch. OpenClaw uses `sessions_spawn`:
- `sessions_spawn(mode="run")` — One-shot tasks, concurrent execution
- `sessions_spawn(mode="session")` — Persistent sessions, multi-turn interaction
- Main session coordinates, subagent results aggregated via session history or filesystem

## Usage Conditions

```
Multiple failures/independent tasks?
  → Are they independent? (different root causes, no shared state)?
    → Can they work in parallel?
      → Use parallel-agents (this skill)
    → Sequential is better?
      → Use systematic-debugging individually
  → Need comprehensive context understanding?
    → Single agent handles all
```

**Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems independently broken
- Each problem can be understood without understanding context of others
- No shared state between investigations

**Don't use when:**
- Failures are related (fixing one might fix others)
- Need to understand full system state
- Agents would interfere (editing same file, sharing resources)

## Flow

### 1. Identify Independent Problem Domains

Group by problem:
- Test file A: Tool approval flow
- Test file B: Batch completion behavior
- Test file C: Abort functionality

Each domain independent — fixing tool approval doesn't affect abort tests.

### 2. Create Focused Tasks for Each Agent

Each agent gets:
- **Clear scope:** One test file or subsystem
- **Clear goal:** Make these tests pass / fix this bug
- **Constraints:** Don't change other code
- **Expected output:** Summary of findings and fixes

### 3. Parallel Dispatch

Use `sessions_spawn` to dispatch all agents simultaneously:

```javascript
// OpenClaw: sessions_spawn parallel dispatch
sessions_spawn({
  task: "Fix 3 failing tests in src/agents/agent-tool-abort.test.ts...",
  runtime: "subagent",
  mode: "run",
  cwd: "/path/to/project"
})
sessions_spawn({
  task: "Fix 2 failing tests in src/batch/completion.test.ts...",
  runtime: "subagent",
  mode: "run",
  cwd: "/path/to/project"
})
sessions_spawn({
  task: "Fix 1 failing test in src/tools/race-conditions.test.ts...",
  runtime: "subagent",
  mode: "run",
  cwd: "/path/to/project"
})
```

### 4. Review and Integrate

When agents return:
- Read each summary
- Verify fixes don't conflict
- Run full test suite
- Integrate all changes

## Agent Prompt Structure

Good agent prompts:
1. **Focused** — One clear problem domain
2. **Self-contained** — All context needed to understand the problem
3. **Specific output** — What should the agent return?

```markdown
Fix 3 failing tests in src/agents/agent-tool-abort.test.ts:

1. "should abort tool with partial output capture" - expects 'interrupted at' in message
2. "should handle mixed completed and aborted tools" - fast tool aborted instead of completed
3. "should properly track pendingToolCount" - expects 3 results but gets 0

These are timing/race condition issues. Your task:

1. Read test file, understand what each test verifies
2. Identify root cause — timing issue or actual bug?
3. Fix:
   - Replace arbitrary timeouts with event-based waiting
   - Fix bugs in abort implementation if found
   - Adjust test expectations if testing changed behavior

Don't just add timeouts — find the real issue.

Return: What you found, what you fixed.
```

## Common Mistakes

**Scope too broad:** "Fix all tests" — agent gets lost
**Specific:** "Fix agent-tool-abort.test.ts" — focused scope

**No context:** "Fix race condition" — agent doesn't know where
**With context:** Paste error messages and test names

**No constraints:** Agent might refactor everything
**With constraints:** "Don't change other code" or "Fix tests only"

**Vague output:** "Fixed" — don't know what changed
**Specific output:** "Return root cause and change summary"

## When Not to Use

**Related failures:** Fix one might fix others — investigate together first
**Needs full context:** Understanding requires seeing whole system
**Exploratory debugging:** Don't know what's broken yet
**Shared state:** Agents would interfere (same file, same resource)

## Key Benefits

1. **Parallelization** — Multiple investigations happen simultaneously
2. **Focus** — Each agent has narrow scope, less context to track
3. **Independence** — Agents don't interfere with each other
4. **Speed** — 3 problems solved in time of 1

## Verification

After agents return:
1. **Review each summary** — Understand what changed
2. **Check for conflicts** — Did agents edit same code?
3. **Run full suite** — Verify all fixes work together
4. **Spot check** — Agents can make systematic errors
