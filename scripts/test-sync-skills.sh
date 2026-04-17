#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
SYNC_SCRIPT="$ROOT_DIR/scripts/sync-skills.sh"

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

SOURCE_REPO="$WORKDIR/source-repo"
DEST_DIR="$WORKDIR/dest"
COMMIT_V1=""

git init --initial-branch=main "$SOURCE_REPO" >/dev/null
cd "$SOURCE_REPO"
git config user.name "Sync Skills Test"
git config user.email "sync-skills-test@example.com"

mkdir demo-skill
cat > demo-skill/SKILL.md <<'EOF'
# demo skill v1
EOF
git add demo-skill/SKILL.md
git commit -m "demo skill v1" >/dev/null
COMMIT_V1="$(git rev-parse HEAD)"

cat > demo-skill/SKILL.md <<'EOF'
# demo skill v2
EOF
git add demo-skill/SKILL.md
git commit -m "demo skill v2" >/dev/null

cat > "$WORKDIR/manifest-branch.json" <<EOF
{
  "repo": "local/test",
  "repo_url": "file://$SOURCE_REPO",
  "ref": "main",
  "skills": [
    { "name": "demo-skill", "path": "demo-skill" }
  ]
}
EOF

cat > "$WORKDIR/manifest-sha.json" <<EOF
{
  "repo": "local/test",
  "repo_url": "file://$SOURCE_REPO",
  "ref": "$COMMIT_V1",
  "skills": [
    { "name": "demo-skill", "path": "demo-skill" }
  ]
}
EOF

BRANCH_LOG="$WORKDIR/branch.log"
SHA_LOG="$WORKDIR/sha.log"

bash "$SYNC_SCRIPT" --manifest "$WORKDIR/manifest-branch.json" --dest "$DEST_DIR/branch" >"$BRANCH_LOG"
grep -F "PLAN demo-skill -> $DEST_DIR/branch/demo-skill" "$BRANCH_LOG" >/dev/null
[[ ! -e "$DEST_DIR/branch/demo-skill" ]]

bash "$SYNC_SCRIPT" --manifest "$WORKDIR/manifest-sha.json" --dest "$DEST_DIR/sha" --apply >"$SHA_LOG"
grep -F "UPDATED demo-skill" "$SHA_LOG" >/dev/null
grep -F "# demo skill v1" "$DEST_DIR/sha/demo-skill/SKILL.md" >/dev/null
grep -Fx "ref=$COMMIT_V1" "$DEST_DIR/sha/demo-skill/.skills-sync-source" >/dev/null
