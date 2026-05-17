---
name: musexmachine-mcp-codex-env
description: Create and validate a Codex-ready development environment for the GitHub repository musexmachine/mcp with safe defaults, deterministic setup steps, and explicit verification output.
---

# Purpose

Set up a reproducible Codex environment for `musexmachine/mcp` with minimal risk and clear proof of readiness.

Use this skill when the user asks to create, fix, or verify a Codex/devcontainer/Codespaces environment for this repo.

# Goal

Deliver a working environment that can:
- clone and open the repository
- install dependencies
- run baseline checks/tests
- expose the MCP service locally (if defined by the repo)

# Constraints

- Inspect source first; do not guess runtime, package manager, or startup commands.
- Prefer idempotent commands.
- Use dry-run style checks before mutating when relevant.
- Keep secrets out of logs and chat output.
- Make the smallest change needed for environment readiness.

# Required inspection

Inspect in this order before proposing changes:
1. `.devcontainer/devcontainer.json`
2. `README*`, `docs/*`, and setup scripts
3. runtime manifests (`package.json`, `pyproject.toml`, `requirements*.txt`, `Dockerfile`, etc.)
4. test and lint scripts
5. expected ports/env vars

If the repo is inaccessible (private/no auth), report that explicitly and return a bootstrap plan with exact commands the user can run once authenticated.

# Environment build workflow

## 1) Preflight (no mutation)

Run:

```bash
pwd
git status --short --branch
command -v git gh node npm pnpm yarn python python3 uv pipx docker
```

Check remote visibility safely:

```bash
git ls-remote https://github.com/musexmachine/mcp.git
```

If this fails due to auth, stop mutation and return a credential-ready path.

## 2) Clone + bootstrap

Use a clean workspace directory and branch-isolated workflow:

```bash
mkdir -p "$HOME/workspaces"
cd "$HOME/workspaces"
git clone https://github.com/musexmachine/mcp.git
cd mcp
git checkout -b chore/codex-env-setup
```

Then follow repo-native setup (examples only; choose based on actual files):

- Node: `npm ci` or `pnpm install --frozen-lockfile`
- Python: `uv sync` or `python -m venv .venv && pip install -r requirements.txt`

## 3) Codex/devcontainer readiness

If `.devcontainer/devcontainer.json` exists:
- verify `features`, `postCreateCommand`, and forwarded ports
- only patch missing essentials

If missing, create a minimum viable config with:
- detected runtime toolchain
- deterministic install command
- non-public/default-private port assumptions
- clear comments for required secrets (names only)

## 4) Validate

Run only checks the repo defines:

```bash
# examples; choose what exists
npm test
npm run build
pytest -q
```

For service startup, run repo-native command and validate local HTTP/socket health if documented.

## 5) Proof output contract

Always return:
- commands actually run
- files created/changed
- checks passed/failed
- unresolved risks/unverified edges

Never claim completion without command output evidence.

# Fallback: private repo / no credentials

If repository access fails:
1. report exact failing command and error
2. pick an authenticated path:
   - if `gh` is available: `gh auth login` then `gh repo clone musexmachine/mcp`
   - if `gh` is missing but Git auth is configured (SSH agent or credential helper): `git clone git@github.com:musexmachine/mcp.git` or `git clone https://github.com/musexmachine/mcp.git`
   - otherwise, return a short setup plan (install `gh` or configure Git with PAT/SSH) without guessing secrets
3. rerun the inspection/build/validate workflow after a successful clone
4. mark environment status as **blocked on repo access** when cloning still fails
