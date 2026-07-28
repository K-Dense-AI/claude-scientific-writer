# Source-bound poster content

## Non-negotiable rule

The generator renders approved manifest content. It does not research, infer, draft,
summarize, complete, or "improve" scientific claims. Never invent poster text,
citations, data, statistics, author details, affiliations, funding statements, image
licenses, or QR destinations.

If an exact source or author approval is missing, stop. Keep the manifest in `draft`
status. Do not replace missing material with plausible prose.

## Build an evidence packet first

Ask the author for the local, authoritative material needed for this poster:

- accepted abstract or author-approved summary;
- exact title, author order, affiliations, contact details, and identifiers;
- final tables, figures, captions, units, sample sizes, statistics, and uncertainty;
- bibliography or exact publication identifiers;
- funding, conflict, ethics, registration, data, and code statements where applicable;
- optional local logos and images plus provenance and ownership/license/permission
  records;
- organizer poster instructions and printer specifications;
- exact QR destination and the visible fallback URL/text.

Record each item as a `sources[]` entry with a unique ID. A locator can be a DOI,
stable URL, local controlled-record identifier, figure/table number, page/section,
or dated author instruction. The scripts never dereference it.

`author_verified: true` means a human author checked that source record. It does not
mean an agent found a plausible web page.

## Exact source IDs

Every text or image element has `source_ids`. These IDs must exactly match records in
`sources[]`; fuzzy title matching is forbidden.

Use the smallest defensible source set:

- a title/author element can cite the accepted-submission or author-roster record;
- a result sentence should cite the exact table, figure, analysis output, or
  publication location supporting it;
- a figure should cite its data/figure provenance and its asset-license record;
- a conference dimension should cite the organizer's current instruction;
- a printer constraint should cite the current quote, specification, or written
  confirmation.

The validator rejects unknown and unused source IDs. This catches misspellings and
stale records instead of guessing what the author meant.

## Content selection is author-controlled

There is no universal section list, word count, visual percentage, number of figures,
or citation count. Use the organizer's requirements and the research story.

A useful author review asks:

1. What question should a viewer understand?
2. Which exact result supports the take-home message?
3. Which method detail is necessary to interpret that result?
4. Which limitation prevents overstatement?
5. What action or follow-up should the viewer take?

Possible sections include context, objective, methods, results, limitations,
conclusions, references, acknowledgments, and contact information. Include only those
that are supported and appropriate. Clinical, qualitative, engineering, humanities,
and computational posters often need different structures.

## Preserve scientific meaning

For each candidate edit:

- preserve direction, magnitude, units, denominators, uncertainty, and qualifiers;
- distinguish observed association from causation;
- retain negative/null results when necessary to prevent a misleading summary;
- keep population, intervention, comparator, endpoint, and time frame where relevant;
- do not convert a model metric into a clinical or practical claim;
- do not add significance language that the source does not support;
- do not remove limitations that materially change interpretation;
- define acronyms for the intended audience;
- keep citation labels synchronized with the exact bibliography.

An agent may propose shorter wording, but the author must approve the exact resulting
text and renew the manifest content hash.

## Figures and data

Figures are optional. Use author-supplied local assets or assets generated separately
from exact author data in a reviewed workflow. This skill makes no network or model
calls. Do not create substitute data, redraw values from memory, or ask an image model
to depict scientific results.

Before approval, verify:

- values, labels, units, error definitions, sample sizes, and statistical notation;
- category order, axes, scales, transformations, baselines, and truncation;
- correspondence between caption and plotted data;
- direct labels or a clear legend;
- redundant encoding beyond color;
- asset hash, source ID, exact provenance, license/permission, and concise alt text;
- a source-bound native long description when alt text and adjacent prose are
  insufficient for a complex figure;
- final effective DPI for raster assets.

If a chart must be regenerated, regenerate it from the author's exact data using a
separate, reviewed analysis workflow. Record the tool/version or controlled workflow,
input source IDs, date, human reviewer, and permission to use the output. Then add the
resulting local image and provenance to the manifest.

## Citations and references

Copy citations only from the author's verified bibliography or primary source record.
Never fabricate missing metadata. Keep identifiers exact, including DOI capitalization
and version/date where those distinguish records.

Space pressure does not justify an ambiguous citation. If the organizer permits a
short display form, keep a stable identifier and provide an exact accessible full-list
destination. The visible poster still needs enough information for a viewer to
identify the source without relying solely on a QR code.

## QR codes

A QR image is only a local asset. The scripts do not generate it, resolve it, follow
it, or create a hyperlink.

For every QR asset:

- record one exact `https://` target in `asset.qr_target`;
- provide a separate text element with role `qr_fallback`;
- include that exact URL verbatim in the fallback text;
- cite the same source record from the image and fallback text;
- write alt text that states the QR code's purpose and destination;
- test the exported and printed code manually on multiple devices.

Do not use a QR code as the only way to access essential poster content.

## Approval binding

Approval is content-specific:

1. Complete the manifest with local assets and all exact source IDs.
2. Keep `approval.status` as `draft`.
3. Run the validator with `--print-content-hash`.
4. Give the exact manifest and reported hash to the approving author.
5. After approval, set `status`, `approved_by`, `approved_at`, and
   `content_sha256`.
6. Run normal validation and generation.

Any change outside `approval` changes the canonical hash. The validator then refuses
generation until an author approves the new hash.

## Placeholder policy

The bundled template intentionally contains replacement tokens, false confirmations,
and draft approval. It must fail validation.

The validator rejects common placeholder forms such as TODO, TBD, Lorem ipsum,
REPLACE_ME, generic bracketed fields, and unresolved template labels. Do not weaken
this policy to make a draft generate. Replace every field with reviewed content or
stop.

## Final content review

Before release, the presenting/corresponding author should compare the poster against
the original evidence packet and check:

- title, author order, affiliations, correspondence, and funding;
- every claim, number, unit, citation, image, and caption;
- methods and limitations needed for valid interpretation;
- consistency between poster text and figures;
- accessibility text, visible QR fallbacks, and meaningful contact information;
- conference and printer compliance;
- the final manifest hash and generated PPTX hash.

An automated pass never substitutes for scientific sign-off.
