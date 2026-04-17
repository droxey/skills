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
[[ -f "$MANIFEST" ]] || err "Manifest not found: $MANIFEST"

# Deterministic SHA-256 of a file or directory tree, sorted by relative path.
sha256_path() {
  python3 - "$1" <<'PY'
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

root = Path(sys.argv[1])
digest = hashlib.sha256()

def update_field(tag: bytes, value: bytes) -> None:
    digest.update(tag)
    digest.update(len(value).to_bytes(8, "big"))
    digest.update(value)

if root.is_file():
    update_field(b"T", b"F")
    update_field(b"P", root.name.encode("utf-8"))
    digest.update(b"S")
    digest.update(root.stat().st_size.to_bytes(8, "big"))
    with root.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
else:
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        if path.is_dir():
            update_field(b"T", b"D")
            update_field(b"P", rel.encode("utf-8"))
            continue
        update_field(b"T", b"F")
        update_field(b"P", rel.encode("utf-8"))
        digest.update(b"S")
        digest.update(path.stat().st_size.to_bytes(8, "big"))
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                digest.update(chunk)

print(digest.hexdigest())
PY
}

META=()
while IFS= read -r line; do
  META+=("$line")
done < <(python3 - "$MANIFEST" <<'PY'
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
if [[ "$REF" =~ ^[0-9a-fA-F]{40}$ ]]; then
  # Full commit SHA: --branch doesn't accept SHAs; clone default then detach
  git clone --filter=blob:none --sparse "$REPO_URL" "$TMPDIR/repo" >/dev/null 2>&1
  ( cd "$TMPDIR/repo" && git checkout --detach "$REF" ) >/dev/null 2>&1
else
  # Branch or tag: shallow clone with --branch
  git clone --depth 1 --branch "$REF" --filter=blob:none --sparse "$REPO_URL" "$TMPDIR/repo" >/dev/null 2>&1
fi

mapfile -t PATHS < <(python3 - "$MANIFEST" <<'PY'
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

  SRC_HASH="$(sha256_path "$SRC")"
  PREV_HASH=""
  PREV_REPO=""
  PREV_REF=""
  PREV_PATH=""
  if [[ -f "$MARKER" ]]; then
    PREV_HASH="$(awk -F'=' '/^skill_dir_sha256=/{print $2}' "$MARKER" | tr -d '[:space:]')"
    PREV_REPO="$(awk -F'=' '/^repo=/{print substr($0, index($0, "=") + 1)}' "$MARKER" | tr -d '\r')"
    PREV_REF="$(awk -F'=' '/^ref=/{print substr($0, index($0, "=") + 1)}' "$MARKER" | tr -d '\r')"
    PREV_PATH="$(awk -F'=' '/^path=/{print substr($0, index($0, "=") + 1)}' "$MARKER" | tr -d '\r')"
  fi

  if [[ -d "$TARGET" && "$PREV_HASH" == "$SRC_HASH" && "$PREV_REPO" == "$REPO" && "$PREV_REF" == "$REF" && "$PREV_PATH" == "$PATH_IN_REPO" ]]; then
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
