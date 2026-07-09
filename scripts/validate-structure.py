#!/usr/bin/env python3
from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


manifest_path = ROOT / ".claude-plugin" / "plugin.json"
if not manifest_path.exists():
    fail("missing .claude-plugin/plugin.json")

manifest = json.loads(manifest_path.read_text())
skills = manifest.get("skills")
if not isinstance(skills, list) or not skills:
    fail(".claude-plugin/plugin.json must contain a non-empty skills array")

for rel in skills:
    skill_dir = (ROOT / rel).resolve()
    if not str(skill_dir).startswith(str(ROOT)):
        fail(f"skill path escapes repository: {rel}")

    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        fail(f"missing {skill_file.relative_to(ROOT)}")

    text = skill_file.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail(f"{skill_file.relative_to(ROOT)} is missing YAML frontmatter")

    frontmatter = match.group(1)
    for field in ("name", "description"):
        if not re.search(rf"^{field}:\s*.+$", frontmatter, re.M):
            fail(f"{skill_file.relative_to(ROOT)} is missing {field}")

    name = re.search(r"^name:\s*(.+)$", frontmatter, re.M).group(1).strip()
    if name != skill_dir.name:
        fail(f"{skill_file.relative_to(ROOT)} name is {name}, expected {skill_dir.name}")

print(f"OK: {len(skills)} skills listed and valid")
