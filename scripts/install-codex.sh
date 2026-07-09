#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${CODEX_HOME:-"$HOME/.codex"}/skills"

mkdir -p "$DEST"

while IFS= read -r -d '' skill_file; do
  skill_dir="$(dirname "$skill_file")"
  skill_name="$(basename "$skill_dir")"
  mkdir -p "$DEST/$skill_name"
  cp -R "$skill_dir"/. "$DEST/$skill_name"/
  printf 'Installed %s -> %s\n' "$skill_name" "$DEST/$skill_name"
done < <(find "$ROOT/skills" -mindepth 3 -maxdepth 3 -name SKILL.md -print0)

printf '\nRestart Codex or start a new thread to pick up updated skills.\n'
