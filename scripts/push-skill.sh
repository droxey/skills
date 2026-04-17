#!/usr/bin/env bash
set -euo pipefail

SKILL_PATH=""
BASE_BRANCH="main"
BRANCH_PREFIX="codex/skill-sync"
MESSAGE=""
APPLY=0
PUSH=0
OPEN_PR=0

usage() {
  cat <<USAGE
Usage: scripts/push-skill.sh --skill <path> [options]

Options:
  --skill <path>      Skill directory path (required)
  --base <branch>     Base branch (default: main)
  --branch-prefix <p> Branch prefix (default: codex/skill-sync)
  --message <msg>     Commit message (default auto-generated)
  --apply             Create branch + commit (default dry-run)
  --push              Push branch (requires --apply)
  --open-pr           Create PR via gh CLI (requires --push)
  -h, --help          Show help
USAGE
}

log() { printf '[push-skill] %s\n' "$*"; }
err() { printf '[push-skill][error] %s\n' "$*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skill) SKILL_PATH="$2"; shift 2 ;;
    --base) BASE_BRANCH="$2"; shift 2 ;;
    --branch-prefix) BRANCH_PREFIX="$2"; shift 2 ;;
    --message) MESSAGE="$2"; shift 2 ;;
    --apply) APPLY=1; shift ;;
    --push) PUSH=1; shift ;;
    --open-pr) OPEN_PR=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) err "Unknown argument: $1" ;;
  esac
done

[[ -n "$SKILL_PATH" ]] || err "--skill is required"
[[ -d "$SKILL_PATH" ]] || err "Skill path not found: $SKILL_PATH"
[[ -f "$SKILL_PATH/SKILL.md" ]] || err "Expected SKILL.md in $SKILL_PATH"

if [[ "$OPEN_PR" -eq 1 && "$PUSH" -eq 0 ]]; then
  err "--open-pr requires --push"
fi
if [[ "$PUSH" -eq 1 && "$APPLY" -eq 0 ]]; then
  err "--push requires --apply"
fi

STAMP="$(date -u +%Y%m%d-%H%M%S)"
BRANCH_NAME="${BRANCH_PREFIX}/${STAMP}"
if [[ -z "$MESSAGE" ]]; then
  MESSAGE="Update skill: $(basename "$SKILL_PATH")"
fi

FILES=("$SKILL_PATH")
[[ -f "skills-manifest.json" ]] && FILES+=("skills-manifest.json")

log "Plan branch=$BRANCH_NAME base=$BASE_BRANCH"
log "Plan commit message=$MESSAGE"
log "Plan files=${FILES[*]}"

if [[ "$APPLY" -eq 0 ]]; then
  log "Dry-run only. Re-run with --apply to commit."
  exit 0
fi

git fetch origin "$BASE_BRANCH"
git switch "$BASE_BRANCH"
git pull --ff-only origin "$BASE_BRANCH"
git switch -c "$BRANCH_NAME"
git add "${FILES[@]}"

if git diff --cached --quiet; then
  err "No staged changes after add; nothing to commit"
fi

git commit -m "$MESSAGE"

if [[ "$PUSH" -eq 1 ]]; then
  git push -u origin "$BRANCH_NAME"
  log "Pushed branch $BRANCH_NAME"
fi

if [[ "$OPEN_PR" -eq 1 ]]; then
  command -v gh >/dev/null || err "gh CLI is required for --open-pr"
  gh pr create --base "$BASE_BRANCH" --head "$BRANCH_NAME" --title "$MESSAGE" --body "Automated skill update from Codex pipeline."
  log "PR opened"
fi
