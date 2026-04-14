# AGENTS

## What this skill is for

`markdown-mode-router` chooses the correct markdown strategy before a file is written or reformatted.

It routes to:

- `teaching` for course artifacts
- `general` for every other markdown file

## Install shape

Keep these files together:

- `SKILL.md`
- `strategies.md`
- `prompts.md`
- `AGENTS.md`

Expose the folder to whatever shared skill library your agent environment already loads.

## Environment notes

### ChatGPT web/app

Make the folder available in your synced skills library, then invoke it by name in the prompt.

### Codex web/cli

Place the folder in the skill set your Codex environment already reads, then call `markdown-mode-router` directly in the task prompt.

### Claude Code web/app

Add the folder to the reusable skills location you already expose to Claude Code, then invoke it by folder name.

### Claude Code CLI

Copy or symlink the folder into your CLI skill directory, then invoke it with the same prompt shape.

## Copy/paste prompts

### Auto-route a file

```md
Use markdown-mode-router.
repo: OWNER/REPO
file: path/to/file.md
goal: choose the correct markdown strategy and format the file
```

### Force non-course rules

```md
Use markdown-mode-router.
repo: OWNER/REPO
file: notes/relocation.md
force_mode: general
goal: apply the Apple Notes-derived markdown structure
```

### Preserve teaching rules

```md
Use markdown-mode-router.
repo: ACS-4999-AI-Engineering
file: lessons/week-03/plan.md
goal: keep teaching formatting and avoid non-course defaults
```

## Decision summary

- repo starts with `ACS` -> `teaching`
- lesson plan, lab, tip, assignment, slides, speaker notes, or quiz -> `teaching`
- everything else -> `general`

## Critical general-mode rule

Only add a TOC when both are true:

- exactly 1 H2 exists
- at least 2 H3 headings exist

When present, the TOC links the H2 and leaves H3 bullets unlinked.
