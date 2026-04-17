---
name: codespace-operator
description: Choose the lightest viable GitHub development surface, prefer Codespaces when runtime access is needed, and produce a safe validated execution plan for mobile/web chat workflows.
allowed-tools: GitHub, browser, terminal, codespaces, gh, claude_remote_control
---

# Purpose

Use GitHub Codespaces as the default cloud dev runtime when a task needs command execution, build/test, preview servers, or a reproducible environment from phone or web chat.

# When to use

Use this skill when the user wants any of the following:
- work on a repo from phone or browser
- run code, tests, builds, generators, or preview apps remotely
- continue coding through ChatGPT or Claude without a local IDE
- decide between GitHub app, github.dev, Codespaces, or Claude Remote Control
- standardize a repo for Codespaces readiness

Do not use this skill when the task is pure explanation, repo reading, or tiny text edits with no runtime need.

# Goals

1. Pick the lightest viable workspace mode.
2. Avoid unnecessary Codespace startup.
3. Default to safe, restart-friendly execution.
4. Return proof: commands, files changed, tests, preview URL, unresolved edges.

# Workspace modes

## github_app
Use for repo understanding, search, file reading, PR review, and planning.

## github_dev
Use for small edits when no terminal, build, or preview is needed.

## codespace_browser
Use when terminal access or a reproducible environment is needed from phone/web.

## codespace_cli
Use when `gh codespace` or scripted control is available.

## claude_remote_control
Use only when an active Claude Code session already exists and needs continuation on another device.

# Selection rules

Choose `github_app` if all are true:
- no commands required
- no install/build/test required
- no preview required

Choose `github_dev` if all are true:
- edit is small
- environment fidelity is not important
- no terminal work is required

Choose `codespace_browser` if any are true:
- terminal commands required
- package install required
- tests or builds required
- app preview required
- environment consistency matters
- multi-file refactor is likely

Choose `codespace_cli` if any are true:
- scripted create/resume/rebuild is needed
- port operations are needed
- SSH or file copy is needed
- machine type changes are needed

Choose `claude_remote_control` only if:
- user is already in Claude Code
- a remote session exists
- continuation matters more than environment creation

# Required inspection

Before proposing edits, inspect for:
- `.devcontainer/devcontainer.json`
- package manager and runtime files
- known app ports
- required secrets
- setup/bootstrap commands
- default branch and target ref

If `.devcontainer/devcontainer.json` is missing, say so explicitly and propose the minimum viable config instead of pretending Codespaces is ready.

# Defaults

- private forwarded ports by default
- branch isolation for non-trivial work
- dry-run first when relevant
- no destructive git actions
- no secret values in chat
- prefer prebuild recommendation if startup is slow
- assume Codespaces can stop idly; make steps restart-safe

# Output format

Return exactly these sections:

## Workspace Mode
One of: `github_app` | `github_dev` | `codespace_browser` | `codespace_cli` | `claude_remote_control`

## Why This Mode
1-3 short bullets.

## Preconditions
- repo
- target ref
- required secrets
- required ports
- machine size
- codespaces readiness

## Dry Run
Numbered commands or UI actions only.

## Execute
Numbered commands or UI actions only.

## Validate
Numbered commands or checks only.

## Proof
- commands run
- files changed
- tests passed/failed
- preview URL if any

## Risks / Unverified Edges
Short bullets only.

# Validation checklist

Use only checks that fit the repo:

## Environment
```bash
pwd
git status --short --branch
command -v git node npm pnpm python go cargo java
printenv | grep -E 'CODESPACE|GITHUB'
```

## Secrets presence
```bash
test -n "$OPENAI_API_KEY" && echo OPENAI_API_KEY=set || echo OPENAI_API_KEY=missing
```

## Common app checks
```bash
npm test
npm run build
pytest -q
go test ./...
curl -I http://127.0.0.1:3000
```

Never claim completion without reporting actual results.

# Repo hardening suggestions

Recommend only when needed:
- add `.devcontainer/devcontainer.json`
- declare expected forwarded ports
- move setup into `postCreateCommand`
- document required Codespaces secrets
- enable prebuilds if startup is slow

# Response style

- be terse
- prefer bullets over prose
- avoid restating the user request
- avoid generic Codespaces explanation unless it changes the decision
- optimize for minimum tokens and fast agent parsing
