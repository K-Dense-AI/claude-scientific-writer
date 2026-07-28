# Safe Formatting for Reports and Manuscripts

## Content before presentation

The former LaTeX style and demonstration report were removed. They could turn
plausible-looking placeholder findings into a polished PDF. This version uses
format-neutral Markdown and JSON/CSV registries so incompleteness remains visible.

Do not format a draft as submission-ready while any verification gate is incomplete.
Visual polish is not evidence.

## Workflow

1. Create a local scaffold.
2. Draft and verify content in Markdown.
3. Run manifest, claim, reference, consistency, authorship, coverage, and lint checks.
4. Obtain accountable human approval.
5. Copy the verified content into the current venue template.
6. Re-run checks that remain applicable and inspect the rendered output manually.

For a journal or conference, use its current author instructions and official template.
For an institutional report or thesis, use the institution's controlled template.

## Fail-closed placeholder policy

Permitted draft markers are intentionally conspicuous, such as `[[TODO:...]]`. The
language linter treats them as errors. Never replace an unresolved marker with generic
boilerplate, a guessed number, a fabricated statement, or an invented citation.

Keep:

- `submission_ready` false;
- the draft banner visible;
- missing declaration statuses explicit;
- human and confidentiality gates incomplete;

until the underlying records are verified.

## Headings and navigation

- Use a single title and logical heading levels.
- Preserve heading order when converting formats.
- Include lists of tables or figures only when useful or required.
- Use stable internal labels for tables, figures, appendices, and supplements.
- Ensure generated bookmarks and reading order match the visible structure.

## Typography and layout

- Use the venue's prescribed font, spacing, margins, page size, and line numbering.
- Do not use color, weight, or position as the only carrier of meaning.
- Keep equations, symbols, units, subscripts, and superscripts intact through
  conversion.
- Check widows, orphans, clipped content, broken links, and misplaced floats manually.

## Tables, figures, and accessibility

Follow `figures_tables.md`. Verify alt text, captions, provenance, permissions, color
independence, reading order, label legibility, and final-size rendering. Do not create a
decorative visual simply to make a report appear complete.

## References and declarations

References must render from verified metadata. After conversion, inspect identifier
links, special characters, author order, and citation order.

Declarations must come from validated records. A style template must never supply a
default ethics approval, consent statement, funding source, conflict statement, author
contribution, data or code promise, or AI disclosure.

## Archival handoff

Retain:

- the verified Markdown source;
- the structured registries;
- the exact venue template version;
- conversion instructions and software versions;
- the final rendered file;
- validator outputs and human approval record.

Do not archive sensitive source documents alongside a public manuscript package unless
authorization, consent, law, contracts, and policy permit it.
