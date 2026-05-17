---
name: superpowers-writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code - guides writing comprehensive implementation plans with bite-sized tasks.
---

# Superpowers Writing Plans

## Overview

Write comprehensive implementation plans assuming the executor has zero codebase context and questionable taste. Document everything they need to know: which files to modify per task, what code, which tests and docs may need checking, how to test. Produce a complete plan as small-grained tasks. DRY. YAGNI. TDD. Frequent commits.

Assume the executor is a skilled developer but knows almost nothing about our toolset or problem domain. Assume they're not great at test design.

**Start by announcing:** "I'm using the writing-plans skill to create an implementation plan."

**Context:** This should run in a dedicated working directory (created by the brainstorming skill).

**Save plan to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`

## Scope Check

If the spec covers multiple independent subsystems, it should already be decomposed into sub-project specs at the brainstorming stage. If not, suggest decomposition into independent plans — one per subsystem. Each plan should produce working, testable software.

## File Structure

Before defining tasks, map which files will be created or modified, and what each file is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- Code you can fit in your head you reason about best, and edit most reliably. Prefer smaller, focused files over large do-everything files.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow existing patterns. If the codebase uses large files, don't unilaterally refactor — but if files being modified are already uncomfortably large, including a split in the plan is reasonable.

This structure guides task decomposition. Each task should produce meaningful changes that can be understood independently.

## Small-Grained Tasks

**Each step is one action (2-5 minutes):**
- "Write failing test" — one step
- "Run to verify it fails" — one step
- "Write minimal code to make test pass" — one step
- "Run to verify test passes" — one step
- "Commit" — one step

## Plan Document Header

**Every plan must start with this header:**

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence describing what's being built]

**Architecture:** [2-3 sentences describing approach]

**Tech Stack:** [Key technologies and libraries]

---
```

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL, error "function not defined"

- [ ] **Step 3: Write minimal implementation code**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## No Placeholders

Every step must contain the actual content the executor needs. The following are **plan failures** — never write:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling"/"Add validation"/"Handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to task N" (repeat code — executor may read tasks sequentially)
- Steps describing what to do without showing how (code steps must have code blocks)
- References to types, functions, or methods not defined in any task

## Self-Review

After writing the full plan, look at the spec with fresh eyes and check the plan:

**1. Spec coverage:** Go through each spec section/requirement. Can you point to a task that implements it? List any gaps.

**2. Placeholder scan:** Search the plan for red flags — any pattern from the "No Placeholders" section above. Fix them.

**3. Type consistency:** Are types, method signatures, and property names consistent between earlier and later tasks? `clearLayers()` in Task 3 and `clearFullLayers()` in Task 7 is a bug.

Find issues, fix inline. No need to re-review — fix and continue. If a spec requirement has no task, add one.

## Working Directory Notes (OpenClaw Adaptation)

Superpowers original uses git worktree for isolated workspaces. In OpenClaw:
- Use git branch to create feature branches
- Work on the branch, merge or PR when done
- Keep working directory clean, isolated from main

**Workflow:**
```bash
# Create feature branch from current
git checkout -b feature/<feature-name>

# Implement (per plan tasks)
# ...

# When done
git checkout main && git merge feature/<feature-name>
```

## Execution Handoff

After saving the plan, offer execution choices:

**"Plan written and saved to `docs/superpowers/plans/<filename>.md`. Two execution options:**

**1. Sub-agent driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Sequential execution** — Execute tasks in batches in current session, with review checkpoints

**Which do you prefer?"**

**If sub-agent driven chosen:**
- Requires `superpowers-subagent-dev` skill
- Fresh subagent per task + two-phase review

**If sequential execution chosen:**
- Execute in order per plan tasks in current session
- Run verification after each task
- Call `superpowers-finishing-branch` on completion for cleanup
