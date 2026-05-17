---
name: superpowers-overview
description: Use when starting any development work or when unsure which superpowers development skill to use - provides entry point and navigation to the full superpowers skill suite.
---

# Superpowers Development Methodology — OpenClaw Port

## What This Is

Superpowers is a **structured development methodology** designed for AI coding agents, with the core principle:
> Agents should not jump straight to writing code, but should first understand requirements → design solutions → make plans → TDD implementation → review code → finish up.

This skill suite ports Superpowers to the OpenClaw Agent Runtime, adapted for OpenClaw's tool model.

## Skill Suite (9 skills)

### Getting Started

| Skill | When to Use | What It Does |
|-------|-------------|--------------|
| **`superpowers-overview`** (this one) | Not sure where to start | View full suite overview and entry points |
| **`superpowers-brainstorming`** | Before building new features/changes | Explore requirements, propose solutions, get approval |
| **`superpowers-writing-plans`** | Have a design, need concrete implementation plan | Write small-grained task plans |

### Execution

| Skill | When to Use | What It Does |
|-------|-------------|--------------|
| **`superpowers-isolated-workspace`** | Before starting implementation | Create isolated git branch, establish clean baseline |
| **`superpowers-subagent-dev`** | Have implementation plan, tasks are independent | Dispatch subagents per task, two-phase review |
| **`superpowers-parallel-agents`** | Multiple independent problems to handle in parallel | Dispatch parallel subagents working concurrently |
| **`superpowers-tdd`** | Before writing any implementation code | Enforce RED-GREEN-REFACTOR cycle |
| **`superpowers-executing-plans`** | Execute plan tasks sequentially in current session | Execute in batches with review checkpoints |

### Quality Assurance

| Skill | When to Use | What It Does |
|-------|-------------|--------------|
| **`superpowers-verification`** | Before claiming anything "done"/"passed" | Enforce evidence-first, must run verification commands |
| **`superpowers-systematic-debugging`** | Hit bugs/test failures/unexpected behavior | Four-phase debugging: root cause → pattern → hypothesis → fix |
| **`superpowers-requesting-code-review`** | After tasks/major features/before merges | Dispatch review to catch issues |
| **`superpowers-receiving-code-review`** | When receiving code review feedback | Verify before implementing, reasoned pushback |
| **`superpowers-finishing-branch`** | Implementation done, tests pass, ready to wrap up | Present merge/PR/keep/discard options |

## Development Flow

```
User requests new feature
        │
        ▼
┌───────────────────────────┐
│ superpowers-brainstorming │
│ Explore requirements +    │
│ design solution           │
└───────────┬───────────────┘
            │ Owner approves design
            ▼
┌───────────────────────────────┐
│ superpowers-isolated-workspace │
│ Create isolated branch +      │
│ clean baseline                 │
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────┐
│ superpowers-writing-plans │
│ Write implementation plan │
│ (task checklist)          │
└───────────┬───────────────┘
            │
            ▼
    ┌───────┴───────┐
    │  Choose mode   │
    └───────┬───────┘
            │
    ┌───────┴───────────────┐
    │                       │
    ▼                       ▼
┌────────────────┐  ┌─────────────────────┐
│ subagent-dev   │  │ executing-plans     │
│ (recommended)   │  │ (sequential in      │
│ dispatch per    │  │  current session)   │
│ task + review   │  │ execute in batches  │
└───────┬────────┘  └──────────┬──────────┘
        │                     │
        └─────────┬───────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │superpowers-finishing│
        │-branch              │
        │ merge/PR/keep/      │
        │ discard             │
        └─────────────────────┘
```

## Daily Use Decisions

**"I want to build feature X"**
→ `superpowers-brainstorming` → `superpowers-writing-plans` → `superpowers-subagent-dev`

**"I need to fix a bug"**
→ `superpowers-systematic-debugging` → `superpowers-tdd` → `superpowers-verification`

**"There are 3 independent test failures"**
→ `superpowers-parallel-agents` → investigate each in parallel → integrate

**"Code is written, ready to commit"**
→ `superpowers-verification` → `superpowers-requesting-code-review` → `superpowers-finishing-branch`

## Core Principles

1. **Design before implementation** — Don't jump to code
2. **Evidence before claims** — Don't say fixed, run verification
3. **Root cause before fix** — Don't guess, debug
4. **Test before code** — TDD, not after-the-fact tests
5. **Review before integration** — Catch issues early

## OpenClaw Adaptation Notes

Compared to Superpowers original:

| Dimension | Original | OpenClaw Adaptation |
|-----------|----------|---------------------|
| Isolation | git worktree | git branch + directory |
| Skill loading | Skill tool | Read SKILL.md file, semantic trigger |
| Subagent | Task cascade | `sessions_spawn` independent sessions |
| Todo management | TodoWrite tool | Inline checklist |
| Context passing | Template injection | Session history + filesystem |

## Relationship with AGENTS.md

Superpowers skill suite **complements** rather than **replaces** AGENTS.md:
- AGENTS.md = who I am, my workspace, my memory system
- Superpowers = structured development process and engineering quality standards
- Both work together: first understand who you are, then use the right methods to work

## ClawHub Publishing Status

All 13 skills published to ClawHub:

| Skill | ClawHub Slug | Version | Notes |
|-------|-------------|---------|-------|
| superpowers-overview | `superpowers-overview` | 1.0.0 | Entry overview |
| superpowers-tdd | `superpowers-tdd` | 1.0.0 | TDD cycle |
| superpowers-verification | `superpowers-verification` | 1.0.0 | Evidence first |
| superpowers-systematic-debugging | `superpowers-systematic-debugging` | 1.0.0 | Systematic debugging |
| superpowers-brainstorming | `superpowers-brainstorming` | 1.0.0 | Design process |
| superpowers-writing-plans | `superpowers-writing-plans` | 1.0.1 | Implementation plans |
| superpowers-subagent-dev | `superpowers-subagent-dev` | 1.0.1 | Sub-agent coordination |
| superpowers-finishing-branch | `superpowers-finishing-branch` | 1.0.1 | Branch completion |
| superpowers-isolated-workspace | `superpowers-isolated-workspace` | 1.0.1 | Isolated workspace |
| superpowers-parallel-agents | `superpowers-parallel-agents` | 1.0.1 | Parallel agents |
| superpowers-receiving-code-review | `openclaw-receiving-code-review` | 1.0.0 | Original slug taken, uses openclaw- prefix |
| superpowers-requesting-code-review | `openclaw-requesting-code-review` | 1.0.0 | Original slug taken, uses openclaw- prefix |
| superpowers-executing-plans | `openclaw-executing-plans` | 1.0.0 | Original slug taken, uses openclaw- prefix |
