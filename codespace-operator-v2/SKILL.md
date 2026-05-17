---
name: Codespace Operator
description: Select the lightest GitHub workspace mode, prefer Codespaces only when runtime is needed, and return a validated mobile/web execution plan.
allowed-tools: GitHub, github.dev, Codespaces, gh, browser, terminal, claude_remote_control
---

# Use when
- user wants repo work from phone or browser
- commands, builds, tests, generators, or preview servers are needed
- user needs a reproducible cloud dev environment
- user wants to choose between GitHub app, github.dev, Codespaces, or Claude Remote Control
- repo needs Codespaces readiness review

# Skip when
- task is explanation only
- task is repo reading only
- tiny edit needs no runtime

# Modes
- `github_app`: read/search/review only
- `github_dev`: small edit, no terminal
- `codespace_browser`: runtime needed from web/mobile
- `codespace_cli`: `gh codespace` or scripted control needed
- `claude_remote_control`: existing Claude Code session must continue on another device

# Selection
Choose `github_app` if all are true:
- no commands
- no install/build/test
- no preview

Choose `github_dev` if all are true:
- edit is small
- no terminal
- environment fidelity is unimportant

Choose `codespace_browser` if any are true:
- terminal commands needed
- install/build/test needed
- preview server needed
- multi-file refactor likely
- reproducibility matters

Choose `codespace_cli` if any are true:
- create/resume/rebuild must be scripted
- ports must be managed from CLI
- SSH, logs, copy, or machine changes are needed

Choose `claude_remote_control` only if:
- user is already using Claude Code
- live session exists
- continuation is more important than new environment setup

# Required inspection
Inspect before proposing execution:
- `.devcontainer/devcontainer.json`
- runtime/package manager files
- setup/bootstrap commands
- required secrets
- expected app ports
- default branch and target ref

If `.devcontainer/devcontainer.json` is missing, say so directly and propose the minimum viable config.

# Current constraints that matter
- browser-based Codespaces exists and is suitable for phone/web continuation
- `gh codespace` supports create, stop, delete, rebuild, SSH, logs, file copy, ports, and machine-type changes
- forwarded ports are private by default
- private port auth cookies expire after 3 hours
- default idle timeout is 30 minutes unless changed or restricted by policy
- prebuilds are worth recommending when startup is slow

# Defaults
- private ports by default
- branch isolation for non-trivial work
- dry-run first
- no destructive git actions
- no secret values in chat
- restart-safe steps
- recommend prebuilds only when startup cost is material

# Output
Return exactly:

## Workspace Mode
`github_app` | `github_dev` | `codespace_browser` | `codespace_cli` | `claude_remote_control`

## Why This Mode
2-4 short bullets.

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

# Validation snippets
Use only what fits the repo.

```bash
pwd
git status --short --branch
command -v git node npm pnpm python go cargo java
printenv | grep -E 'CODESPACE|GITHUB'
```

```bash
test -n "$OPENAI_API_KEY" && echo OPENAI_API_KEY=set || echo OPENAI_API_KEY=missing
```

```bash
npm test
npm run build
pytest -q
go test ./...
curl -I http://127.0.0.1:3000
```

Never report completion without actual results.

# Response style
- terse
- execution-first
- low-token
- easy to scan
- no generic Codespaces primer unless it changes the decision
