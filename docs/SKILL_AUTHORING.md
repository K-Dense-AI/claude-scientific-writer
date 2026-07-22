# Skill Authoring Guide

This guide explains how to contribute a skill through the canonical [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) repository and then include its pinned upstream version in Scientific Writer. For general contribution workflow (tests, lint, PRs), see [CONTRIBUTING.md](../CONTRIBUTING.md).

## Where Skills Live

The **canonical source of truth** is the `skills/` tree in [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills). This repository vendors a selected, reproducible snapshot at the revision recorded in `skills.lock.json`.

The following three directories are generated and must never be edited directly:

- `skills/` (Claude Code plugin payload)
- `.claude/skills/` (CLI and local-development mirror)
- `scientific_writer/.claude/skills/` (Python package mirror)

After an upstream skill change is released, pin and vendor that release:

```bash
python3 scripts/sync_skills.py --update-ref v2.55.0
```

CI verifies the pinned content hashes and both mirrors, without a network request, using `python3 scripts/sync_skills.py --check`.

## Directory Layout

Each skill is authored in the upstream repository as a directory under `skills/` containing a `SKILL.md` file and optional supporting subdirectories:

```
skills/
└── my-skill-name/
    ├── SKILL.md          # Required: frontmatter + instructions
    ├── references/       # Optional: in-depth reference documents (.md)
    ├── scripts/          # Optional: helper scripts invoked via Bash
    └── assets/           # Optional: templates, examples, style files
```

Keep `SKILL.md` focused on *how the agent should act*; move long background material into `references/` and point to it from `SKILL.md` so the agent loads it only when needed.

## SKILL.md Frontmatter

Every `SKILL.md` starts with YAML frontmatter:

```yaml
---
name: my-skill-name
description: What the skill does and when to use it. This skill should be used when the user asks for X, Y, or Z.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---
```

Field reference:

| Field | Required | Format | Notes |
|-------|----------|--------|-------|
| `name` | Yes | Lowercase, hyphen-separated | Must match the directory name |
| `description` | Yes | 1-3 sentences | States what the skill does **and when it should trigger**. This is what the agent reads to decide whether to load the skill, so include concrete trigger phrases ("Use when...", "This skill should be used when...") |
| `allowed-tools` | Yes | Space-separated string, e.g. `Read Write Edit Bash` | Not a YAML list. Restricts which tools the agent may call while the skill is active |
| `license` | Yes | e.g. `MIT license` | License for the skill content |
| `metadata.skill-author` | Yes | `K-Dense Inc.` | Author attribution for skills contributed to this repository |
| `compatibility` | No | Free text | Runtime requirements, e.g. required CLIs or environment variables |

A common mistake is writing `allowed-tools: [Read, Write, Edit, Bash]` (list style); the convention in this repository is the space-separated string `allowed-tools: Read Write Edit Bash`.

## Writing the Skill Body

Below the frontmatter, write the instructions the agent follows when the skill is active. Guidelines:

- **Start with an Overview** describing the skill's purpose in a short paragraph.
- **Give a concrete workflow**: numbered steps the agent should follow, including exact commands for any scripts in `scripts/`.
- **Show usage examples**: example user prompts and the expected behavior.
- **State environment requirements explicitly** (e.g., "requires `PARALLEL_API_KEY`") and describe fallback behavior when a dependency is missing.
- **Reference supporting files by relative path** (e.g., `references/citation_styles.md`) so the agent can read them on demand.

## Registering the Skill

After a new skill is merged upstream, add it to `skills.lock.json` so the sync script selects it. Then register its generated local destination in `.claude-plugin/marketplace.json`, which defines the `claude-scientific-writer` plugin:

```json
"skills": [
  "./skills/citation-management",
  "./skills/my-skill-name",
  ...
]
```

A selected skill that is not listed in `marketplace.json` will not be available to plugin users.

## Full Workflow Checklist

1. Create or update `skills/my-skill-name/` in `K-Dense-AI/scientific-agent-skills`.
2. Follow that repository's contribution, metadata-versioning, validation, and security-scanning requirements.
3. Merge and release the upstream change.
4. Add the upstream skill and its local destination to `skills.lock.json`, then register the destination in `.claude-plugin/marketplace.json`.
5. Run `python3 scripts/sync_skills.py --update-ref <upstream-tag-or-commit>` to refresh all generated snapshots and hashes.
6. Verify with `python3 scripts/sync_skills.py --check`.
7. Test locally: reinstall the plugin from a test marketplace (see [DEVELOPMENT.md](DEVELOPMENT.md#plugin-development)) and confirm the skill appears when you ask "What skills are available?".
8. Add a section describing the skill to [docs/SKILLS.md](SKILLS.md) if it is user-facing.

## Minimum Quality Bar

Before opening a pull request, a new skill should meet all of the following:

- **Triggers correctly**: the `description` is specific enough that the agent activates the skill for its intended requests and not for unrelated ones.
- **Self-contained**: all scripts run with the project's declared dependencies; any extra requirements are documented in the frontmatter (`compatibility`) and the skill body.
- **Working examples**: every command shown in `SKILL.md` has been executed successfully from a clean checkout.
- **No secrets or personal paths**: no API keys, usernames, or absolute paths from your machine.
- **Consistent voice**: instructions are written as directives to the agent, matching the style of existing skills.
- **Pinned snapshot and mirrors in sync**: `python3 scripts/sync_skills.py --check` passes.

## See Also

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution workflow
- [DEVELOPMENT.md](DEVELOPMENT.md) - Architecture and plugin development
- [SKILLS.md](SKILLS.md) - Documentation of existing skills
