#!/usr/bin/env sh
set -eu

CODEX_HOME_VALUE="${CODEX_HOME:-$HOME/.codex}"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SKILL_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
DEST_DIR="$CODEX_HOME_VALUE/skills/codex-visuals"

FORCE=0
if [ "${1:-}" = "--force" ]; then
  FORCE=1
fi

mkdir -p "$CODEX_HOME_VALUE/skills"

if [ -e "$DEST_DIR" ]; then
  if [ "$FORCE" -ne 1 ]; then
    echo "Destination already exists: $DEST_DIR" >&2
    echo "Re-run with --force to replace it." >&2
    exit 1
  fi
  rm -rf "$DEST_DIR"
fi

cp -R "$SKILL_ROOT" "$DEST_DIR"
echo "Installed codex-visuals to $DEST_DIR"
echo "Restart Codex to pick up the updated skill."
