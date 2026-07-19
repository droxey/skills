#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: install.sh [--force] TARGET_SKILLS_DIRECTORY

Installs the reasoning-router skill into:
  TARGET_SKILLS_DIRECTORY/reasoning-router

--force preserves any existing installation as a timestamped backup before replacing it.
USAGE
}

force=0
if [[ "${1:-}" == "--force" ]]; then
  force=1
  shift
fi

if [[ $# -ne 1 ]]; then
  usage >&2
  exit 2
fi

target_root=$1
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source_root=$(cd -- "$script_dir/.." && pwd)
destination="$target_root/reasoning-router"

for required in SKILL.md README.md scripts/select_reasoning.py scripts/__init__.py; do
  if [[ ! -f "$source_root/$required" ]]; then
    printf 'Missing required source file: %s\n' "$source_root/$required" >&2
    exit 1
  fi
done

mkdir -p -- "$target_root"
staging=$(mktemp -d "$target_root/.reasoning-router.install.XXXXXX")
cleanup() {
  rm -rf -- "$staging"
}
trap cleanup EXIT

mkdir -p -- "$staging/scripts"
cp -- "$source_root/SKILL.md" "$staging/SKILL.md"
cp -- "$source_root/README.md" "$staging/README.md"
cp -- "$source_root/scripts/select_reasoning.py" "$staging/scripts/select_reasoning.py"
cp -- "$source_root/scripts/__init__.py" "$staging/scripts/__init__.py"
chmod +x -- "$staging/scripts/select_reasoning.py"

if [[ -e "$destination" ]]; then
  if [[ $force -ne 1 ]]; then
    printf 'Destination already exists: %s\nUse --force to preserve it as a backup and replace it.\n' "$destination" >&2
    exit 1
  fi
  timestamp=$(date -u +%Y%m%dT%H%M%SZ)
  backup="$target_root/reasoning-router.backup.$timestamp"
  mv -- "$destination" "$backup"
  printf 'Preserved previous installation: %s\n' "$backup"
fi

mv -- "$staging" "$destination"
trap - EXIT
printf 'Installed reasoning-router: %s\n' "$destination"
