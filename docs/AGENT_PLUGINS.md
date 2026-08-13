# Agent Plugins Support

Scientific Writer ships as a conformant [Agent Plugins](https://agent-plugins.org/) 1.0.0 package,
so its skills load in any client that implements the standard — not just Claude Code.

Agent Plugins is a vendor-neutral package format governed by a Technical Steering Committee with
maintainers from Amazon, Cursor, Microsoft, OpenAI, and Vercel. It defines a fixed directory layout
for two portable component types, [Agent Skills](https://agentskills.io/specification) and MCP
servers, while leaving distribution, installation, permissions, and UX to each client.

## What this repository provides

| Path | Role |
|------|------|
| `plugin.json` | Agent Plugins 1.0.0 manifest at the plugin root (required by §5) |
| `skills/` | 26 discoverable skills, each a directory with `SKILL.md` (§7.1) |
| `mcp.json` | Not present — this plugin ships no MCP servers, which §6.2 explicitly permits |
| `.claude/`, `scientific_writer/.claude/` | Bundled payload copies, each a loadable plugin root of its own |
| `.claude-plugin/marketplace.json` | Claude Code marketplace metadata (client-specific, outside the portable format) |

The manifest declares its target specification version through `$schema`, which is how a client
selects its validation rules:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "claude-scientific-writer",
  "version": "2.19.0"
}
```

`plugin.json` is the source of truth; `scripts/sync_skills.py` mirrors it byte-for-byte into the two
payload directories, and `scripts/bump_version.py` keeps its `version` aligned with `pyproject.toml`,
`scientific_writer/__init__.py`, and `.claude-plugin/marketplace.json`.

## Using the plugin from an Agent Plugins client

Point your client at any of these roots:

```bash
# From a checkout
git clone https://github.com/K-Dense-AI/claude-scientific-writer.git

# From the published Python package — the installed payload is itself a plugin root
pip install scientific-writer
python -c "import scientific_writer, pathlib; print(pathlib.Path(scientific_writer.__file__).parent / '.claude')"
```

Skills that shell out to the bundled scripts need the runtime dependencies described in the
[README prerequisites](../README.md#prerequisites) — a LaTeX distribution, `parallel-cli`
authentication, and optionally `OPENROUTER_API_KEY` for image generation.

## Validating conformance

`scripts/validate_agent_plugin.py` checks any plugin root against the specification. It is
dependency-free and never touches the network: the canonical schemas are vendored under
`scripts/schemas/agent-plugins/<version>/`, as §5.2 requires of clients ("Clients MUST NOT retrieve a
schema while loading a plugin").

```bash
# Validate this repository and its bundled payloads (what CI runs)
uv run python scripts/validate_agent_plugin.py

# Validate someone else's plugin
uv run python scripts/validate_agent_plugin.py ../their-plugin

# Fail on warnings too
uv run python scripts/validate_agent_plugin.py --strict
```

It reports three levels:

- **errors** — a conforming client would reject the plugin or skip the component (missing manifest,
  unsupported spec version, invalid `name`, a `SKILL.md` whose frontmatter breaks the Agent Skills
  spec, an MCP `command` that escapes the plugin root).
- **warnings** — the client recovers, but the package probably is not what the author intended
  (unknown top-level manifest fields, a non-object `extensions`, a `skills/` subdirectory with no
  `SKILL.md`, a `${...}` placeholder no client expands).
- **info** — what a client would actually load, e.g. `skills: 22 skill(s) discoverable`.

Supporting a future specification version means dropping its schemas into a new
`scripts/schemas/agent-plugins/<version>/` directory; nothing in the checker hardcodes 1.0.0.

### Keep every skill an immediate child of `skills/`

§7.1 is explicit that "Clients MUST NOT recursively search deeper descendants for additional
skills". A skill nested two levels down is invisible to every Agent Plugins client, and to Claude
Code as well.

This bit the `docx`, `pdf`, `pptx`, and `xlsx` skills, which the vendoring step used to rewrite into
a local `document-skills/` bundle through the `destination` field in `skills.lock.json`. Upstream
always published them as top-level skills; the nesting was introduced here. The destinations are now
flat, so all 26 skills are discoverable. If you add a skill to `skills.lock.json`, keep its
`destination` a single path segment — `scripts/validate_agent_plugin.py` reports any directory under
`skills/` that has no `SKILL.md`, and names the nested skills it is hiding.

## Client extensions

Section 8 of the specification reserves reverse-domain namespaces for client-specific behavior: data
under `extensions` in `plugin.json`, files in a matching top-level directory.

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "claude-scientific-writer",
  "extensions": {
    "com.example.client": { "setting": true }
  }
}
```

This plugin declares no extensions. A namespace should be owned by the client that defines its
semantics, and the Claude-specific pieces here — `commands/` and `.claude-plugin/marketplace.json` —
already live where Claude Code looks for them. Clients ignore namespaces they do not implement, so
adding one later is backward compatible.

## MCP servers

If this plugin ever ships an MCP server, it goes in `mcp.json` at the plugin root:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "example": {
      "type": "stdio",
      "command": "./bin/server",
      "args": ["--data", "${PLUGIN_DATA}"],
      "cwd": "${PLUGIN_ROOT}"
    }
  }
}
```

The validator already covers this file: transport selection (`stdio`, `streamable-http`, `sse`),
`./`-prefixed paths that stay inside the plugin root, the reserved `PLUGIN_ROOT` / `PLUGIN_DATA`
environment names, and placeholders no client expands.

## AGENTS.md and `.agents/`

The same portability goal applies to project instructions and agent directories:

- **`AGENTS.md`** at the repository root is a generated, byte-identical mirror of `CLAUDE.md`,
  regenerated by `scripts/sync_skills.py` so the two can never drift.
- **`/claude-scientific-writer:scientific-writer-init`** writes both `CLAUDE.md` and `AGENTS.md`
  into a user's project, from `templates/CLAUDE.scientific-writer.md` and
  `templates/AGENTS.scientific-writer.md`.
- **`load_system_instructions()`** searches `.claude/` then `.agents/` for `WRITER.md`, `AGENTS.md`,
  and `CLAUDE.md`, then falls back to `AGENTS.md` and `CLAUDE.md` at the project root.
- **`setup_claude_skills()`** always installs the bundled payload into `.claude/` (the Claude Agent
  SDK discovers skills there) and additionally refreshes `.agents/` when the project already has one,
  so projects on the vendor-neutral layout get the same skills without every other project growing
  an unexpected directory.

## References

- [Agent Plugins specification](https://agent-plugins.org/specification)
- [Agent Plugins JSON schemas](https://agent-plugins.org/schemas)
- [Agent Skills specification](https://agentskills.io/specification)
- [Specification repository and governance](https://github.com/agentplugins/agent-plugins-spec)
