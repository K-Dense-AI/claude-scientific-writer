# PPTX package security

## Threat model

A presentation can be more than visible slide XML. A package can contain VBA,
ActiveX, OLE objects, embedded files, external relationships, linked images, malformed
XML, duplicate/traversing ZIP names, or highly compressed payloads.

Do not open an untrusted presentation or template to see whether it is safe. Opening
is execution by a complex Office application and is outside these scripts.

This skill:

- generates from a built-in blank `python-pptx` presentation only;
- accepts no external template;
- accepts no `.pptm`, `.potx`, `.potm`, `.ppsx`, `.ppsm`, legacy `.ppt`, or
  arbitrary office package;
- inspects `.pptx` as a bounded one-slide generated-poster ZIP/XML profile without
  extraction;
- rejects every external relationship, even an ordinary hyperlink;
- uses visible QR fallback text instead of creating external hyperlinks.

## Package facts

[ECMA-376](https://ecma-international.org/publications-and-standards/standards/ecma-376/)
defines Office Open XML vocabularies, representation, and packaging.
[ISO/IEC 29500-2:2021](https://www.iso.org/standard/77818.html) defines Open
Packaging Conventions, which combine parts and relationships into one package.

The inspector expects a standard macro-free PresentationML package with at least:

- `[Content_Types].xml`
- `_rels/.rels`
- `ppt/presentation.xml`
- `ppt/_rels/presentation.xml.rels`
- exactly one slide part and one matching slide relationship.

It requires the standard macro-free presentation main content type. It resolves
internal relationship targets against package parts.

[Microsoft's supported-format list](https://support.microsoft.com/en-us/office/file-formats-that-are-supported-in-powerpoint-252c6fa0-a4bc-41be-ac82-b77c9773f9dc)
identifies `.pptm` as a macro-enabled presentation containing VBA code. A `.pptx`
extension alone is not sufficient assurance, so the inspector also checks content
types, relationships, and package part names.

## Rejected active and embedded content

The inspector rejects:

- VBA/macro-enabled content types and `vbaProject` parts;
- `.pptm` and every non-`.pptx` extension;
- `ppt/activeX`, control properties, custom UI, and related relationships;
- OLE object relationships and markup;
- `ppt/embeddings` and package relationships;
- external-link package areas;
- audio, video, linked media, timing, transitions, embedded fonts, 3D models, and
  other parts outside the static generated-poster profile;
- notes, comments, custom properties, web extensions, and interactive hyperlink/action
  markup outside the one-slide poster profile;
- package signatures, because generation changes the package and never preserves an
  unverified signature;
- executable/script/binary suffixes.

[Microsoft's Open XML OLE object documentation](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.oleobject?view=openxml-3.0.1)
shows that PresentationML OLE objects can be embedded or linked. Neither is needed for
a static poster and both are rejected.

## External relationships

An OPC relationship can target an internal package part or an external resource.
Microsoft's
[OPC target-mode documentation](https://learn.microsoft.com/en-us/windows/win32/api/msopc/nf-msopc-iopcrelationship-gettargetmode)
distinguishes the two. The strict policy rejects any relationship with
`TargetMode="External"`.

This includes:

- remote or linked images;
- ordinary web hyperlinks;
- linked OLE objects or workbooks;
- external media or data.

The policy is intentionally stricter than PowerPoint's feature set. The visible
poster may contain an `https://` URL as plain text, and a local QR image may encode
that URL, but the PPTX does not create a clickable external relationship.

Internal targets are normalized relative to the source part, must remain inside the
package, and must exist.

## ZIP preflight

The inspector reads the central directory before selected XML:

- input file limit: 512 MiB;
- central-directory limit: 64 MiB;
- member limit: 4,096;
- single uncompressed member limit: 128 MiB;
- total uncompressed limit: 1 GiB;
- compression-ratio limit: 100:1;
- allowed methods: stored or deflated;
- no encrypted members;
- no symbolic-link members;
- no absolute, traversing, backslash, duplicate, or case-colliding names.
- no multi-disk or ZIP64 package in this strict bounded profile.
- no package part outside the exact generated-poster path allowlist.
- PNG/JPEG media suffixes must match their byte signatures and streams must pass ZIP
  CRC validation.

These are defensive local policy limits, not ECMA/ISO or PowerPoint product limits.
Adjusting them is a security decision and requires new tests.

The ZIP footer is read directly before Python's `ZipFile` constructs its member list.
Declared member count and central-directory size are therefore bounded before the
library materializes attacker-controlled entries.

The code never calls `ZipFile.extract` or `extractall`. Python's
[`zipfile` documentation](https://docs.python.org/3/library/zipfile.html) warns
that callers must prevent archive members from escaping the destination; not
extracting removes that path entirely.

## XML handling

Every bounded XML part and every relationship part is parsed. The strict generated
profile requires UTF-8 XML; NUL, document-type, and entity declarations are rejected
before parsing, including attempts to hide declarations in another encoding. Content types,
relationship roots/IDs/target modes, the one-slide relationship, and internal target
existence are checked explicitly.

The inspector does not:

- resolve external entities;
- execute macros or scripts;
- activate OLE/ActiveX;
- follow links;
- render slides;
- invoke PowerPoint, LibreOffice, or a shell command;
- deserialize arbitrary Python objects.

## Alt text markup

The generator writes each approved picture description to PresentationML nonvisual
drawing properties (`p:cNvPr` `descr`). Microsoft's
[NonVisualDrawingProperties documentation](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.nonvisualdrawingproperties?view=openxml-3.0.1)
describes this element and its drawing description property.

The inspector counts pictures with nonempty descriptions. Presence is not semantic
quality; review alt text in PowerPoint.

The generator also uses the visible poster title as the native slide-title placeholder
and writes the manifest language on text runs. The inspector reports title count and
missing run-language metadata. These structural fields still require PowerPoint,
screen-reader, and exported-PDF review. Longer descriptions remain approved native
text elements in reading order rather than hidden package attachments.

## Safe generation sequence

1. Validate strict local JSON, requirements, sources, approval hash, and asset hashes.
2. Decode bounded local images with exact-pinned Pillow and reject EXIF/XMP/comments
   or embedded text/application metadata.
3. Create a new presentation with exact-pinned `python-pptx` and its exact-pinned
   `lxml` dependency; never load a user template.
4. Remove the built-in template's inert binary printer-settings part and normalize
   ZIP timestamps.
5. Inspect the cleaned generated package.
6. Copy the package while adding approved picture descriptions and text language.
7. Inspect the patched package again.
8. Run layout/font/image/palette audits.
9. Publish to a new destination without replacement.

The temporary files are private and in the destination directory. Final publication
uses a same-filesystem hard link that fails if the destination already exists.

## Untrusted inputs

For a third-party PPTX:

```bash
python -B scripts/inspect_pptx.py untrusted.pptx
```

If it reports a finding, quarantine or discard the file. Do not open it to remediate.

Even a clean report is not an antivirus verdict. The checker recognizes a deliberately
small package profile; it cannot prove that every Office parser vulnerability or
malicious payload is absent. Apply organizational malware scanning, sandboxing,
Office Protected View, patching, and provenance controls as required.

Do not use an inspected third-party file as a generator template. This skill has no
template-input feature.

## Residual technical limits

- Standard ZIP/XML validation is not full ECMA-376 schema validation.
- Standalone package inspection checks image signatures/CRC, not image decoder
  safety. Generation separately performs bounded, exact-pinned Pillow decoding.
- It does not render text, equations, fonts, transparency, or color.
- It cannot certify accessibility, scientific accuracy, or print readiness.
- It intentionally rejects safe but unnecessary features such as hyperlinks and
  embedded files.
- Password-protected/encrypted packages are rejected rather than decrypted.

These limits are design boundaries, not invitations to bypass the checks.
