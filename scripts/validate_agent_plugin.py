#!/usr/bin/env python3
"""Validate plugin directories against the Agent Plugins specification.

Specifications
--------------
Agent Plugins 1.0.0 : https://agent-plugins.org/specification
Agent Skills        : https://agentskills.io/specification

The checker is dependency-free and offline. Manifest and MCP documents are
validated against the vendored canonical schemas in
``scripts/schemas/agent-plugins/<version>/`` with a small JSON Schema subset
evaluator, then the semantic rules the schemas cannot express (§4 package
boundaries, §6 component discovery, §7 component types, §8 client extensions,
§9 placeholder expansion) are applied on top.

Supporting a new Agent Plugins version means dropping its schemas into a new
``scripts/schemas/agent-plugins/<version>/`` directory; nothing here hardcodes
1.0.0. Per §5.2 clients must never fetch a schema over the network while
loading a plugin, so the vendored copies are the only source consulted.

Usage
-----
    python scripts/validate_agent_plugin.py                 # repo root + bundled payloads
    python scripts/validate_agent_plugin.py path/to/plugin  # explicit roots
    python scripts/validate_agent_plugin.py --strict        # warnings fail too
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Union
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = Path(__file__).resolve().parent / "schemas" / "agent-plugins"

MANIFEST_NAME = "plugin.json"
MCP_NAME = "mcp.json"
SKILLS_DIR_NAME = "skills"
SKILL_FILE_NAME = "SKILL.md"

# Roots checked when no path argument is given: the repository itself plus the
# payload copies shipped inside the Python package, under either the Claude or
# the vendor-neutral directory name.
DEFAULT_ROOTS = [
    REPO_ROOT,
    REPO_ROOT / ".claude",
    REPO_ROOT / ".agents",
    REPO_ROOT / "scientific_writer" / ".claude",
    REPO_ROOT / "scientific_writer" / ".agents",
]

# Agent Skills specification frontmatter limits.
SKILL_NAME_PATTERN = re.compile(r"^(?!.*--)[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
MAX_SKILL_NAME_LENGTH = 64
MAX_SKILL_DESCRIPTION_LENGTH = 1024
MAX_SKILL_COMPATIBILITY_LENGTH = 500
SKILL_FRONTMATTER_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}

# §8: client extension namespaces are reverse-domain identifiers.
EXTENSION_NAMESPACE_PATTERN = re.compile(r"^[a-z0-9-]+(?:\.[a-z0-9-]+)+$")

# §9.2: the only placeholders a client expands.
PLACEHOLDER_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
EXPANDED_PLACEHOLDERS = {"PLUGIN_ROOT", "PLUGIN_DATA"}

Frontmatter = dict[str, Union[str, dict[str, str]]]


@dataclass(frozen=True)
class Diagnostic:
    """A single conformance finding.

    Attributes
    ----------
    level : str
        One of ``"error"``, ``"warning"``, or ``"info"``. Errors mean a
        conforming client would reject the plugin or skip the component;
        warnings mean the client recovers but the package is not what the author
        probably intended; info records what a client would actually load.
    location : str
        Path or JSON pointer the finding applies to, relative to the plugin root.
    message : str
        Human-readable description, citing the relevant specification section.
    """

    level: str
    location: str
    message: str

    def render(self) -> str:
        """Return the one-line console representation of the finding."""
        mark = "✗" if self.level == "error" else "!"
        return f"  {mark} {self.location}: {self.message}"


def error(location: str, message: str) -> Diagnostic:
    """Build an error-level diagnostic."""
    return Diagnostic("error", location, message)


def warning(location: str, message: str) -> Diagnostic:
    """Build a warning-level diagnostic."""
    return Diagnostic("warning", location, message)


# ---------------------------------------------------------------------------
# JSON Schema (draft 2020-12) subset evaluator
# ---------------------------------------------------------------------------
# Only the keywords used by the canonical Agent Plugins schemas are supported:
# type, const, enum, not, minLength, maxLength, pattern, properties, required,
# additionalProperties, propertyNames, items, oneOf, and local $ref/$defs.

JSON_TYPES: dict[str, Any] = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "number": (int, float),
    "integer": int,
    "null": type(None),
}


def _resolve_ref(ref: str, root_schema: dict[str, Any]) -> dict[str, Any]:
    """Resolve a local JSON pointer reference such as ``#/$defs/server``."""
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported non-local $ref: {ref}")
    node: Any = root_schema
    for token in ref[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        node = node[token]
    return node


def _type_matches(instance: Any, expected: str) -> bool:
    """Return whether an instance matches a single JSON Schema type name."""
    if expected == "boolean":
        return isinstance(instance, bool)
    if expected in {"number", "integer"} and isinstance(instance, bool):
        return False
    return isinstance(instance, JSON_TYPES[expected])


def validate_against_schema(
    instance: Any,
    schema: Any,
    root_schema: dict[str, Any],
    pointer: str = "",
) -> list[str]:
    """Validate an instance against a schema subset, returning failure messages.

    Parameters
    ----------
    instance : Any
        Decoded JSON value under test.
    schema : Any
        Schema (or subschema) to apply. ``True``/``False`` schemas are honored.
    root_schema : dict
        The document the schema came from, used to resolve local ``$ref``.
    pointer : str
        JSON pointer of ``instance`` within the document, for messages.

    Returns
    -------
    list of str
        One message per violation; empty when the instance conforms.
    """
    where = pointer or "(root)"
    if schema is True:
        return []
    if schema is False:
        return [f"{where}: value is not allowed here"]
    if "$ref" in schema:
        return validate_against_schema(instance, _resolve_ref(schema["$ref"], root_schema), root_schema, pointer)

    problems: list[str] = []

    if "type" in schema:
        expected = schema["type"]
        names = [expected] if isinstance(expected, str) else list(expected)
        if not any(_type_matches(instance, name) for name in names):
            return [f"{where}: expected type {' or '.join(names)}"]

    if "const" in schema and instance != schema["const"]:
        problems.append(f"{where}: must equal {json.dumps(schema['const'])}")

    if "enum" in schema and instance not in schema["enum"]:
        problems.append(f"{where}: must be one of {json.dumps(schema['enum'])}")

    if "not" in schema and not validate_against_schema(instance, schema["not"], root_schema, pointer):
        problems.append(f"{where}: value is excluded by the schema")

    if "oneOf" in schema:
        attempts = [
            validate_against_schema(instance, option, root_schema, pointer) for option in schema["oneOf"]
        ]
        matched = sum(1 for failures in attempts if not failures)
        if matched != 1:
            titles = [option.get("title", "variant") for option in schema["oneOf"]]
            problems.append(
                f"{where}: must match exactly one of [{', '.join(titles)}] (matched {matched})"
            )
            if matched == 0:
                # Surface the closest variant's failures so the author sees the
                # actual problem rather than only the oneOf summary.
                problems += min(attempts, key=len)

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            problems.append(f"{where}: shorter than {schema['minLength']} character(s)")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            problems.append(f"{where}: longer than {schema['maxLength']} character(s)")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            problems.append(f"{where}: does not match {schema['pattern']}")

    if isinstance(instance, list) and "items" in schema:
        for index, item in enumerate(instance):
            problems += validate_against_schema(item, schema["items"], root_schema, f"{pointer}/{index}")

    if isinstance(instance, dict):
        problems += _validate_object(instance, schema, root_schema, pointer)

    return problems


def _validate_object(
    instance: dict[str, Any],
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    pointer: str,
) -> list[str]:
    """Apply the object-specific keywords of the supported schema subset."""
    where = pointer or "(root)"
    problems: list[str] = []
    properties = schema.get("properties", {})

    for required in schema.get("required", []):
        if required not in instance:
            problems.append(f"{where}: missing required field {required!r}")

    for key, value in instance.items():
        child = f"{pointer}/{key}"
        if "propertyNames" in schema and validate_against_schema(
            key, schema["propertyNames"], root_schema, child
        ):
            problems.append(f"{child}: property name is not allowed here")
        if key in properties:
            problems += validate_against_schema(value, properties[key], root_schema, child)
            continue
        extra = schema.get("additionalProperties", True)
        if extra is False:
            problems.append(f"{child}: unknown field")
        else:
            problems += validate_against_schema(value, extra, root_schema, child)

    return problems


def load_vendored_schema(canonical_id: str) -> tuple[str, dict[str, Any]]:
    """Map a canonical ``$schema`` identifier onto a vendored schema document.

    Parameters
    ----------
    canonical_id : str
        The ``$schema`` value declared by a plugin document.

    Returns
    -------
    tuple of (str, dict)
        The Agent Plugins version and the decoded schema.

    Raises
    ------
    ValueError
        If the identifier is malformed or the version is not vendored here.
    """
    parsed = urlparse(canonical_id)
    parts = Path(parsed.path).parts
    if parsed.scheme != "https" or parsed.netloc != "agent-plugins.org" or len(parts) != 4:
        raise ValueError(f"not a canonical Agent Plugins schema identifier: {canonical_id!r}")
    _, version, filename = parts[1], parts[2], parts[3]
    path = SCHEMA_DIR / version / filename
    if not path.is_file():
        available = sorted(p.name for p in SCHEMA_DIR.iterdir() if p.is_dir())
        raise ValueError(
            f"unsupported Agent Plugins version {version!r} "
            f"(vendored schemas: {', '.join(available) or 'none'})"
        )
    return version, json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Agent Skills frontmatter
# ---------------------------------------------------------------------------


def _unquote(value: str) -> str:
    """Strip matching YAML quotes from a scalar and unescape its contents."""
    value = value.strip()
    if len(value) < 2 or value[0] != value[-1] or value[0] not in "\"'":
        return value
    inner = value[1:-1]
    if value[0] == "'":
        return inner.replace("''", "'")
    out: list[str] = []
    index = 0
    while index < len(inner):
        char = inner[index]
        if char == "\\" and index + 1 < len(inner):
            following = inner[index + 1]
            out.append({"n": "\n", "t": "\t", "r": "\r"}.get(following, following))
            index += 2
            continue
        out.append(char)
        index += 1
    return "".join(out)


def parse_frontmatter(text: str) -> tuple[Frontmatter, list[str]]:
    """Parse SKILL.md YAML frontmatter into top-level scalars and nested maps.

    A full YAML parser is deliberately avoided so the checker stays
    dependency-free; the Agent Skills frontmatter schema is a flat mapping of
    scalars plus the ``metadata`` map, which this covers.

    Returns
    -------
    tuple of (dict, list of str)
        The parsed fields and any structural parse problems.
    """
    if not text.startswith("---"):
        return {}, ["file does not begin with a YAML frontmatter block"]
    end = text.find("\n---", 3)
    if end == -1:
        return {}, ["frontmatter block is not terminated by '---'"]

    fields: Frontmatter = {}
    problems: list[str] = []
    current_map: Union[dict[str, str], None] = None

    for raw in text[3:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indented = raw[:1].isspace()
        if ":" not in raw:
            problems.append(f"unparsable frontmatter line: {raw.strip()!r}")
            continue
        key, _, value = raw.partition(":")
        key = key.strip()
        value = _unquote(value)
        if indented:
            if current_map is None:
                problems.append(f"indented frontmatter line outside a mapping: {raw.strip()!r}")
                continue
            current_map[key] = value
            continue
        if value == "":
            current_map = {}
            fields[key] = current_map
        else:
            current_map = None
            fields[key] = value

    return fields, problems


def validate_skill(skill_dir: Path, location: str) -> list[Diagnostic]:
    """Validate one discovered skill against the Agent Skills specification."""
    diagnostics: list[Diagnostic] = []
    skill_md = skill_dir / SKILL_FILE_NAME
    fields, problems = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    diagnostics += [error(location, problem) for problem in problems]
    if not fields:
        return diagnostics

    for key in sorted(set(fields) - SKILL_FRONTMATTER_FIELDS):
        diagnostics.append(
            warning(location, f"frontmatter field {key!r} is not defined by the Agent Skills specification")
        )

    name = fields.get("name")
    if not isinstance(name, str) or not name:
        diagnostics.append(error(location, "frontmatter is missing the required 'name' field"))
    else:
        if len(name) > MAX_SKILL_NAME_LENGTH:
            diagnostics.append(error(location, f"name is longer than {MAX_SKILL_NAME_LENGTH} characters"))
        if not SKILL_NAME_PATTERN.match(name):
            diagnostics.append(
                error(
                    location,
                    f"name {name!r} must be lowercase alphanumeric with single hyphens, "
                    "and must not start or end with a hyphen",
                )
            )
        if name != skill_dir.name:
            diagnostics.append(
                error(location, f"name {name!r} does not match its directory {skill_dir.name!r}")
            )

    description = fields.get("description")
    if not isinstance(description, str) or not description.strip():
        diagnostics.append(error(location, "frontmatter is missing a non-empty 'description' field"))
    elif len(description) > MAX_SKILL_DESCRIPTION_LENGTH:
        diagnostics.append(
            error(
                location,
                f"description is {len(description)} characters "
                f"(maximum {MAX_SKILL_DESCRIPTION_LENGTH})",
            )
        )

    compatibility = fields.get("compatibility")
    if isinstance(compatibility, str) and len(compatibility) > MAX_SKILL_COMPATIBILITY_LENGTH:
        diagnostics.append(
            error(
                location,
                f"compatibility is {len(compatibility)} characters "
                f"(maximum {MAX_SKILL_COMPATIBILITY_LENGTH})",
            )
        )

    metadata = fields.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        diagnostics.append(error(location, "metadata must be a mapping of string keys to string values"))

    for scalar in ("license", "compatibility", "allowed-tools"):
        if scalar in fields and not isinstance(fields[scalar], str):
            diagnostics.append(error(location, f"{scalar} must be a string"))

    return diagnostics


# ---------------------------------------------------------------------------
# Package model, discovery, and component checks
# ---------------------------------------------------------------------------


def _escapes_root(path: Path, root: Path) -> bool:
    """Return whether a filesystem-resolved path leaves the resolved plugin root (§4.1)."""
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return True
    return False


def _check_relative_path(value: str, root: Path, location: str, field: str) -> list[Diagnostic]:
    """Validate a plugin-relative path field: ``./``-prefixed and contained (§4.1)."""
    if not value.startswith("./"):
        return [error(location, f"{field} {value!r} must be a plugin-relative path beginning with './'")]
    if _escapes_root(root / value[2:], root):
        return [error(location, f"{field} {value!r} resolves outside the plugin root")]
    return []


def _check_placeholders(values: Iterable[tuple[str, str]], location: str) -> list[Diagnostic]:
    """Warn about ``${...}`` placeholders no client is required to expand (§9.2)."""
    diagnostics = []
    for field, value in values:
        for name in PLACEHOLDER_PATTERN.findall(value):
            if name not in EXPANDED_PLACEHOLDERS:
                diagnostics.append(
                    warning(
                        location,
                        f"{field} references ${{{name}}}, which clients do not expand; "
                        "only ${PLUGIN_ROOT} and ${PLUGIN_DATA} are substituted",
                    )
                )
    return diagnostics


def check_manifest(root: Path) -> tuple[list[Diagnostic], bool]:
    """Validate ``plugin.json`` (§5).

    Returns
    -------
    tuple of (list of Diagnostic, bool)
        Findings, and whether the manifest is loadable enough for a client to
        continue on to component discovery.
    """
    manifest_path = root / MANIFEST_NAME
    if not manifest_path.exists():
        return [error(MANIFEST_NAME, "manifest is missing; every plugin MUST have plugin.json at its root")], False
    if not manifest_path.is_file():
        return [error(MANIFEST_NAME, "manifest is not a regular file")], False
    if _escapes_root(manifest_path, root):
        return [error(MANIFEST_NAME, "manifest resolves outside the plugin root")], False

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [error(MANIFEST_NAME, f"manifest is not valid JSON: {exc}")], False
    if not isinstance(manifest, dict):
        return [error(MANIFEST_NAME, "manifest must contain a top-level JSON object")], False

    declared = manifest.get("$schema")
    if not isinstance(declared, str) or not declared:
        return [error(MANIFEST_NAME, "manifest is missing the required '$schema' field")], False
    try:
        version, schema = load_vendored_schema(declared)
    except ValueError as exc:
        return [error(MANIFEST_NAME, str(exc))], False

    diagnostics: list[Diagnostic] = []
    extensions = manifest.get("extensions")
    checked = dict(manifest)

    # §5.2: unknown top-level fields and a non-object 'extensions' are reported
    # and ignored rather than rejected, so they are separated from fatal
    # schema violations before the schema runs.
    for key in sorted(set(manifest) - set(schema.get("properties", {}))):
        diagnostics.append(warning(MANIFEST_NAME, f"unknown top-level field {key!r} is ignored by clients"))
        checked.pop(key)
    if "extensions" in checked and not isinstance(extensions, dict):
        diagnostics.append(warning(MANIFEST_NAME, "'extensions' is not an object and is ignored by clients"))
        checked.pop("extensions")

    fatal = [error(MANIFEST_NAME, problem) for problem in validate_against_schema(checked, schema, schema)]
    if fatal:
        return diagnostics + fatal, False

    # §8: extension namespaces are reverse-domain identifiers with object values.
    if isinstance(extensions, dict):
        for namespace in sorted(extensions):
            if not EXTENSION_NAMESPACE_PATTERN.match(namespace):
                diagnostics.append(
                    warning(
                        MANIFEST_NAME,
                        f"extension namespace {namespace!r} is not a reverse-domain identifier",
                    )
                )
            directory = root / namespace
            if directory.exists() and not directory.is_dir():
                diagnostics.append(
                    error(namespace, "client extension namespace exists but is not a directory")
                )

    diagnostics.append(
        Diagnostic("info", MANIFEST_NAME, f"targets Agent Plugins {version} as {manifest['name']!r}")
    )
    return diagnostics, True


def check_skills(root: Path) -> list[Diagnostic]:
    """Discover and validate the ``skills/`` component (§6, §7.1)."""
    skills_dir = root / SKILLS_DIR_NAME
    if not skills_dir.exists():
        return []
    if not skills_dir.is_dir():
        return [error(SKILLS_DIR_NAME, "exists but is not a directory; the skills component is invalid")]

    diagnostics: list[Diagnostic] = []
    discovered = 0
    for child in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        relative = f"{SKILLS_DIR_NAME}/{child.name}"
        skill_md = child / SKILL_FILE_NAME
        if not skill_md.is_file():
            # §7.1: only immediate children are scanned, so nested SKILL.md
            # files in a bundle directory are never discovered.
            nested = sorted(p.parent.name for p in child.glob(f"*/{SKILL_FILE_NAME}"))
            detail = f"; nested skills are not discovered: {', '.join(nested)}" if nested else ""
            diagnostics.append(
                warning(relative, f"no {SKILL_FILE_NAME}, so this directory is not loaded as a skill{detail}")
            )
            continue
        if _escapes_root(skill_md, root):
            diagnostics.append(error(relative, f"{SKILL_FILE_NAME} resolves outside the plugin root"))
            continue
        discovered += 1
        diagnostics += validate_skill(child, f"{relative}/{SKILL_FILE_NAME}")

    diagnostics.append(Diagnostic("info", SKILLS_DIR_NAME, f"{discovered} skill(s) discoverable"))
    return diagnostics


def check_mcp(root: Path) -> list[Diagnostic]:
    """Validate the optional ``mcp.json`` component (§6, §7.2, §9)."""
    mcp_path = root / MCP_NAME
    if not mcp_path.exists():
        return []
    if not mcp_path.is_file():
        return [error(MCP_NAME, "exists but is not a regular file; the MCP component is invalid")]

    try:
        document = json.loads(mcp_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [error(MCP_NAME, f"not valid JSON: {exc}")]
    if not isinstance(document, dict):
        return [error(MCP_NAME, "must contain a top-level JSON object")]

    declared = document.get("$schema")
    if not isinstance(declared, str) or not declared:
        return [error(MCP_NAME, "missing the required '$schema' field")]
    try:
        _, schema = load_vendored_schema(declared)
    except ValueError as exc:
        return [error(MCP_NAME, str(exc))]

    diagnostics = [error(MCP_NAME, problem) for problem in validate_against_schema(document, schema, schema)]
    if diagnostics:
        return diagnostics

    servers = document.get("mcpServers", {})
    for name in sorted(servers):
        server = servers[name]
        location = f"{MCP_NAME}#{name}"
        if server.get("type") != "stdio":
            continue
        command = server["command"]
        if command.startswith("./"):
            diagnostics += _check_relative_path(command, root, location, "command")
        elif "/" in command or "\\" in command:
            diagnostics.append(
                error(location, f"command {command!r} must be a bare executable token or a './' path")
            )
        cwd = server.get("cwd")
        if isinstance(cwd, str) and cwd.startswith("./"):
            diagnostics += _check_relative_path(cwd, root, location, "cwd")
        candidates = [("command", command)]
        candidates += [("args", value) for value in server.get("args", [])]
        candidates += [(f"env.{key}", value) for key, value in sorted(server.get("env", {}).items())]
        diagnostics += _check_placeholders(candidates, location)

    diagnostics.append(Diagnostic("info", MCP_NAME, f"{len(servers)} MCP server(s) declared"))
    return diagnostics


def validate_plugin(root: Path) -> list[Diagnostic]:
    """Run every Agent Plugins conformance check against one plugin root."""
    if not root.is_dir():
        return [error(str(root), "plugin root is not a directory")]
    diagnostics, loadable = check_manifest(root)
    if not loadable:
        # §5.3: a client rejects the plugin outright and discovers nothing.
        return diagnostics
    return diagnostics + check_skills(root) + check_mcp(root)


def main() -> int:
    """Validate the requested plugin roots and report findings."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "roots",
        nargs="*",
        type=Path,
        help="plugin root directories (defaults to the repository and its bundled payloads)",
    )
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--quiet", action="store_true", help="only print findings and the final verdict")
    args = parser.parse_args()

    roots = args.roots or [root for root in DEFAULT_ROOTS if (root / MANIFEST_NAME).exists()]
    if not roots:
        print(f"No plugin roots found (looked for {MANIFEST_NAME} in the repository and bundled payloads).")
        return 1

    failures = 0
    for root in roots:
        label = _display(root)
        diagnostics = validate_plugin(root)
        errors = [d for d in diagnostics if d.level == "error"]
        warnings = [d for d in diagnostics if d.level == "warning"]
        infos = [d for d in diagnostics if d.level == "info"]

        print(f"{label}")
        for diagnostic in errors + warnings:
            print(diagnostic.render())
        if not args.quiet:
            for diagnostic in infos:
                print(f"  · {diagnostic.location}: {diagnostic.message}")
        if errors or (args.strict and warnings):
            failures += 1
            print(f"  → FAILED ({len(errors)} error(s), {len(warnings)} warning(s))")
        else:
            print(f"  → conforms to Agent Plugins ({len(warnings)} warning(s))")

    if failures:
        print(f"\n{failures} plugin root(s) failed Agent Plugins validation.")
        return 1
    print("\nAll plugin roots conform to the Agent Plugins specification.")
    return 0


def _display(path: Path) -> str:
    """Render a path relative to the repository root when possible."""
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(REPO_ROOT)) or "."
    except ValueError:
        return str(resolved)


if __name__ == "__main__":
    sys.exit(main())
