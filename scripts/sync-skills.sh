#!/usr/bin/env bash
set -euo pipefail

MANIFEST="skills-manifest.json"
DEST="${CODEX_HOME:-$HOME/.codex}/skills"
APPLY=0
CHANNEL=""

usage() {
  cat <<USAGE
Usage: scripts/sync-skills.sh [options]

Options:
  --manifest <file>   Manifest path (default: skills-manifest.json)
  --dest <dir>        Install dir (default: \$CODEX_HOME/skills or ~/.codex/skills)
  --channel <name>    Require channel match
  --apply             Apply changes (default is dry-run)
  -h, --help          Show help
USAGE
}

log() { printf '[sync] %s\n' "$*"; }
err() { printf '[sync][error] %s\n' "$*" >&2; exit 1; }

# Clone without assuming the ref is a branch so the manifest can pin tags or commits too.
clone_manifest_repo() {
  local repo_url="$1"
  local ref="$2"
  local destination="$3"

  git clone --no-checkout --filter=blob:none --sparse "$repo_url" "$destination" >/dev/null
  (
    cd "$destination"
    git fetch origin "$ref" >/dev/null
    git checkout --detach FETCH_HEAD >/dev/null
  )
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --manifest) MANIFEST="$2"; shift 2 ;;
    --dest) DEST="$2"; shift 2 ;;
    --channel) CHANNEL="$2"; shift 2 ;;
    --apply) APPLY=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) err "Unknown argument: $1" ;;
  esac
done

command -v git >/dev/null || err "git is required"
command -v python3 >/dev/null || err "python3 is required"
command -v sha256sum >/dev/null || err "sha256sum is required"
[[ -f "$MANIFEST" ]] || err "Manifest not found: $MANIFEST"

readarray -t META < <(python3 - "$MANIFEST" <<'PY'
import json, sys
m = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
print(m.get('repo', ''))
print(m.get('repo_url', ''))
print(m.get('ref', 'main'))
print(m.get('channel', ''))
valid = [s for s in m.get('skills', []) if s.get('name', '').strip() and s.get('path', '').strip()]
print(len(valid))
PY
)

REPO="${META[0]}"
REPO_URL="${META[1]}"
REF="${META[2]}"
MANIFEST_CHANNEL="${META[3]}"
COUNT="${META[4]}"

[[ -n "$REPO" ]] || err "Manifest 'repo' is required"
[[ "$COUNT" -gt 0 ]] || err "Manifest 'skills' must not be empty"
if [[ -z "$REPO_URL" ]]; then
  REPO_URL="https://github.com/${REPO}.git"
fi
if [[ -n "$CHANNEL" && "$CHANNEL" != "$MANIFEST_CHANNEL" ]]; then
  err "Channel mismatch requested=$CHANNEL manifest=$MANIFEST_CHANNEL"
fi

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

log "Fetching ${REPO}@${REF}"
clone_manifest_repo "$REPO_URL" "$REF" "$TMPDIR/repo"

PATHS=()
while IFS= read -r line; do
  PATHS+=("$line")
done < <(python3 - "$MANIFEST" <<'PY'
import json, sys
m = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
for s in m.get('skills', []):
    p = s.get('path', '').strip()
    if p:
        print(p)
PY
)

( cd "$TMPDIR/repo" && git sparse-checkout set --no-cone "${PATHS[@]}" ) >/dev/null

mkdir -p "$DEST"
UPDATED=0
UNCHANGED=0
FAILED=0

while IFS=$'\t' read -r NAME PATH_IN_REPO; do
  SRC="$TMPDIR/repo/$PATH_IN_REPO"
  SRC_SKILL="$SRC/SKILL.md"
  TARGET="$DEST/$NAME"
  MARKER="$TARGET/.skills-sync-source"

  if [[ ! -f "$SRC_SKILL" ]]; then
    log "FAIL $NAME missing SKILL.md at $PATH_IN_REPO"
    FAILED=$((FAILED + 1))
    continue
  fi

  SRC_HASH="$(sha256sum "$SRC_SKILL" | awk '{print $1}')"
  PREV_HASH=""
  if [[ -f "$MARKER" ]]; then
    PREV_HASH="$(awk -F'=' '/^skill_md_sha256=/{print $2}' "$MARKER" | tr -d '[:space:]')"
  fi

  if [[ -d "$TARGET" && "$PREV_HASH" == "$SRC_HASH" ]]; then
    log "UNCHANGED $NAME"
    UNCHANGED=$((UNCHANGED + 1))
    continue
  fi

  if [[ "$APPLY" -eq 0 ]]; then
    log "PLAN $NAME -> $TARGET"
    UPDATED=$((UPDATED + 1))
    continue
  fi

  TS="$(date -u +%Y%m%dT%H%M%SZ)"
  if [[ -d "$TARGET" ]]; then
    BACKUP="$DEST/${NAME}.bak.${TS}"
    mv "$TARGET" "$BACKUP"
    log "BACKUP $NAME -> $BACKUP"
  fi

  cp -a "$SRC" "$TARGET"
  cat > "$MARKER" <<MARKER
repo=$REPO
ref=$REF
path=$PATH_IN_REPO
skill_dir_sha256=$SRC_HASH
installed_at=$TS
MARKER
  log "UPDATED $NAME"
  UPDATED=$((UPDATED + 1))
done < <(python3 - "$MANIFEST" <<'PY'
import json, sys
m = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
for s in m.get('skills', []):
    n = s.get('name', '').strip()
    p = s.get('path', '').strip()
    if n and p:
        print(f"{n}\t{p}")
PY
)

MODE="DRY_RUN"
[[ "$APPLY" -eq 1 ]] && MODE="APPLY"
log "Summary mode=$MODE updated_or_planned=$UPDATED unchanged=$UNCHANGED failed=$FAILED"
[[ "$FAILED" -eq 0 ]] || exit 2
