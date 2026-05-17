---
name: superpowers-isolated-workspace
description: Use when starting feature work that needs isolation from current workspace - creates isolated git branches with clean setup and safety verification.
---

# Superpowers Isolated Workspace

## Overview

Create an isolated git branch environment for new feature work. In OpenClaw, git branches are more stable and reliable for isolation than worktrees.

**Core principle:** Systematic directory selection + safety verification = reliable isolation.

**Start by announcing:** "I'm using the isolated-workspace skill to set up an isolated work environment."

## Directory Selection Flow

Check in priority order:

### 1. Check Existing Directories

```bash
# Check in priority order
ls -d .isolated 2>/dev/null || ls -d worktrees 2>/dev/null || ls -d .worktrees 2>/dev/null
```

**If found:** Use that directory.

### 2. Check AGENTS.md or Project Docs

```bash
grep -i "workspace.*director\|worktree.*director\|isolated.*path" AGENTS.md 2>/dev/null
```

**If preference specified:** Use without asking.

### 3. Ask Owner

If no directory and no preference specified:

```
No isolated workspace directory found. Where to create?

1. .isolated/ (in-project, hidden)
2. ~/.openclaw/workspace-<project-name>/ (global location)

Which?
```

## Safety Verification

### For In-Project Directories

**Must verify directory is not tracked before creating branch:**

```bash
# Check if directory is gitignored
git check-ignore -q .isolated 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**If not ignored:**

Fix immediately:
1. Add to .gitignore
2. Commit change
3. Continue creating isolated branch

## Creation Steps

### 1. Detect Project Name

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. Create Feature Branch

```bash
# Determine branch name
BRANCH_NAME="feature/<feature-name>"

# Create new branch from current
git checkout -b "$BRANCH_NAME"

# Confirm on correct branch
git branch --show-current
```

### 3. Run Project Setup

Auto-detect and run appropriate setup:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then pip install -e .; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. Verify Clean Baseline

Run tests to ensure clean starting point:

```bash
# Use project-appropriate test command
npm test / pytest / cargo test / go test ./...
```

**If tests fail:** Report failures, ask whether to continue or investigate.

**If tests pass:** Report ready.

### 5. Report Location

```
Isolated branch ready: $BRANCH_NAME
Tests passed (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.isolated/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.isolated/` |
| None exist | Check AGENTS.md → ask owner |
| Directory not ignored | Add to .gitignore + commit |
| Baseline tests fail | Report failure + ask |
| No package.json | Skip dependency install |

## Common Mistakes

**Skipping ignore verification**
- Problem: Workspace content tracked, polluting git status
- Fix: Always use `git check-ignore` before creating in-project directory

**Assuming directory location**
- Problem: Causes inconsistency, violates project convention
- Fix: Follow priority: existing > AGENTS.md > ask

**Starting without confirmation**
- Problem: Can't distinguish new bugs from existing issues
- Fix: Report failure, get explicit permission before continuing

**Hardcoded setup commands**
- Problem: Fails on projects using different tools
- Fix: Auto-detect from project files (package.json, etc.)

## Integration with Brainstorming

```
User requests new feature
  → brainstorming skill (explore design)
  → Owner approves design
  → isolated-workspace (create isolated branch) ← current skill
  → writing-plans (write implementation plan)
  → subagent-dev or sequential execution
  → finishing-branch (complete and cleanup)
```

## OpenClaw Environment Notes

In OpenClaw (WSL):
- `git worktree` command available but not fully compatible with OpenClaw session model
- Using `git branch` + independent working directory is more stable
- Branch naming convention: `feature/<name>` / `fix/<name>` / `refactor/<name>`
- After completion, use `finishing-branch` skill for merge/PR/cleanup
