# My Skills

Personal agent skills, using the same basic layout as `mattpocock/skills`.

## Install From GitHub

After pushing this repository, install it with:

```bash
npx skills@latest add promogit/skills
```

or:

```bash
npx skills@latest add https://github.com/promogit/skills
```

## Local Codex Install

From a local clone, copy every skill into Codex:

```bash
bash scripts/install-codex.sh
```

By default this installs into `${CODEX_HOME:-$HOME/.codex}/skills`.

## Validate

Before pushing:

```bash
python3 scripts/validate-structure.py
```

## Git Hook

Enable the versioned pre-commit hook once per clone:

```bash
git config core.hooksPath .githooks
```

It runs `python3 scripts/validate-structure.py` before each commit.

## Add A Skill

1. Create `skills/<category>/<skill-name>/SKILL.md`.
2. Put `name` and `description` in YAML frontmatter.
3. Add the folder path to `.claude-plugin/plugin.json`.
4. Add the skill name to `skills.sh.json` if you want it grouped on skills.sh.

Optional files such as `references/`, `scripts/`, and `assets/` live inside the individual skill folder.
