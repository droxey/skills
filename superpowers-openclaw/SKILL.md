---
name: superpowers-openclaw
description: Complete Superpowers methodology for OpenClaw. A 12-skill collection that enforces design-before-code, TDD, systematic debugging, verification, and structured development workflows.
---

# SuperpowersOpen

Superpowers methodology — complete skill collection for the OpenClaw platform. 12 skills working together to form an end-to-end rigorous development workflow.

## How This Collection Works

This is a **skill collection**. The root SKILL.md acts as the manifest. Individual skills live in subdirectories and are auto-discovered by OpenClaw via their `description` fields.

## Skills

### Entry Point
- **using-superpowers-open** — Tool mapping, trigger coordination, instruction priority (always active)

### Workflow Chain
- **brainstorming** — Design-first: no code before design approval
- **writing-plans** — Decompose designs into bite-sized implementation tasks
- **executing-plans** — Load plan, execute tasks inline, verify completion
- **finishing-a-development-branch** — Structured merge/PR/keep/discard workflow

### Practice Disciplines
- **test-driven-development** — RED-GREEN-REFACTOR: test first, watch it fail, minimal code
- **systematic-debugging** — 4-phase debugging: root cause → pattern → hypothesis → fix
- **verification-before-completion** — Evidence before claims, always
- **receiving-code-review** — Verify before implementing, no performative agreement
- **requesting-code-review** — 5-dimension self-review checklist
- **writing-skills** — TDD methodology applied to skill documentation
- **using-git-worktrees** — Isolated git worktree workspaces

## Installation

```bash
cp -r superpowers-open ~/.openclaw/skills/
```

Restart OpenClaw Gateway. All 12 skills are auto-discovered.

## Requirements

- OpenClaw (any version supporting SKILL.md format)
- No additional dependencies

## License

MIT-0

## Credits

Adapted from [obra/superpowers](https://github.com/obra/superpowers) methodology.
