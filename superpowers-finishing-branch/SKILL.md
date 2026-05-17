---
name: superpowers-finishing-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - presents structured options for merge, PR, or cleanup.
---

# Superpowers Finishing Branch

## Overview

Guide development completion through clear options: verify tests → present options → execute choice → cleanup.

**Start by announcing:** "I'm using the finishing-a-development-branch skill to complete this work."

## OpenClaw Adaptation Notes

Superpowers original uses git worktree for isolated workspaces, cleaning up worktrees when done. In OpenClaw:
- Use git branch for isolation
- Clean up feature branches on completion or keep for future use
- Working directory is the isolated environment, no extra cleanup needed

## Flow

### Step 1: Verify Tests

**Before presenting options, verify tests pass:**

```bash
# Run project test suite
npm test / pytest / cargo test / go test ./...
```

**If tests fail:**
```
Tests failed (<N> failures). Must fix before proceeding:

[show failures]

Cannot continue to merge/PR until tests pass.
```

Stop. Do not proceed to Step 2.

**If tests pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main
git merge-base HEAD master
```

Or ask: "This branch forks from main — correct?"

### Step 3: Present Options

Present these 4 options:

```
Implementation complete. What would you like to do?

1. Merge back to local <base-branch>
2. Push and create Pull Request
3. Keep branch (handle later)
4. Discard this work

Which option?
```

**Don't add explanations** — keep options concise.

### Step 4: Execute Choice

#### Option 1: Local Merge

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify post-merge tests
<test command>

# If tests pass
git branch -d <feature-branch>
```

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "..."
# or manually create and provide URL
```

#### Option 3: Keep

Report: `Branch <name> kept. Workspace remains at <path>.`

**Don't do extra cleanup.**

#### Option 4: Discard

**First confirm:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

## Quick Reference

| Option | Merge | Push | Keep Branch | Cleanup |
|--------|-------|------|-------------|---------|
| 1. Local merge | Yes | - | - | Yes |
| 2. Create PR | - | Yes | Yes | - |
| 3. Keep | - | - | Yes | - |
| 4. Discard | - | - | - | Yes (force) |

## Common Mistakes

**Skipping test verification**
- Problem: Merge bad code, create failing PR
- Fix: Always verify tests before presenting options

**Open-ended questions**
- Problem: "What next?" → vague
- Fix: Present exact 4 structured options

**Option 4 without confirmation**
- Problem: Accidental work deletion
- Fix: Require "discard" confirmation for option 4
