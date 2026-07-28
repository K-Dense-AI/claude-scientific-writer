# Source ledger

Research cutoff: **2026-07-24**. Recheck live organizer, printer, package, and
application guidance before production use.

This ledger records the upstream basis for skill behavior. It is not a poster's
scientific bibliography.

Method: targeted `parallel-cli search` and `parallel-cli extract` queries restricted
to the official domains cited below, followed by cross-checking canonical pages.
Retrieval dates are stated where a page exposed no publication/update date.

## Microsoft PowerPoint

### Poster-specific product guidance

- [Microsoft Create poster templates for PowerPoint](https://create.microsoft.com/en-us/templates/posters)
  (official Microsoft Create).
  - Describes editable PowerPoint poster/flyer templates and saving, printing, or
    sending the result as PDF.

Skill impact: confirms PowerPoint as a supported poster authoring format, but does
not establish research-poster dimensions or printer requirements. This strict
generator does not ingest downloaded templates or use the page's AI design features.

### Slide dimensions and scaling

- [Change the size of your PowerPoint slides](https://support.microsoft.com/en-us/office/change-the-size-of-your-powerpoint-slides-040a811c-be43-40b9-8d04-0de5ed79987e)
  (Microsoft Support; checked 2026-07-24; no publication date exposed).
  - Custom width/height each range from 1 to 56 inches.
  - Units can be inches, centimeters, or pixels; PowerPoint converts them.
  - All slides in a presentation have the same size.
  - Maximize can cause content not to fit; Ensure Fit can make content smaller.

Skill impact: enforce 1–56 inches, one slide, exact aspect ratio, explicit physical
scale, and no reuse/resizing of existing content.

### Export

- [Export a presentation](https://support.microsoft.com/en-us/powerpoint/export-a-presentation)
  (Microsoft Support; checked 2026-07-24).
  - Standard is the option for publishing online and printing; Minimum size
    prioritizes a smaller file.

Skill impact: provide a manual export plan and require independent PDF/print checks.
The scripts do not invoke Office or an alternative converter.

### Accessibility

- [Make your PowerPoint presentations accessible to people with disabilities](https://support.microsoft.com/en-us/office/make-your-powerpoint-presentations-accessible-to-people-with-disabilities-6f7772b2-2f33-4bd2-8ca7-dae3b2b3ef25)
  (Microsoft Support; checked 2026-07-24).
  - Use Accessibility Checker and Reading Order pane.
  - Add alt text to visuals.
  - Do not use color alone.
  - Use sufficient text/background contrast.
  - Use meaningful hyperlink text.
  - Test with a screen reader.
  - Recommends 18 pt or larger for ordinary slides.

- [Rules for the Accessibility Checker](https://support.microsoft.com/en-us/accessibility/office-accessibility/rules-for-the-accessibility-checker)
  (Microsoft Support).
  - Includes missing alt text and logical reading order checks.

- [PowerPoint PDF Accessibility](https://learn.microsoft.com/en-us/office/pdf/powerpoint/powerpointpdfaccessibility)
  (Microsoft Learn; last updated 2026-05-12).
  - Documents tagged-PDF behavior and applicable PowerPoint versions/channels.

Skill impact: automate only structural checks; require final Accessibility Checker,
reading-order, screen-reader, and exported-PDF review. The 18 pt recommendation is
identified as slide-specific, not a universal poster minimum.

### Fonts, pictures, and media

- [Benefits of embedding custom fonts](https://support.microsoft.com/en-us/office/benefits-of-embedding-custom-fonts-cb3982aa-ea76-4323-b008-86670f222dbc)
  (Microsoft Support; published 2026-05-04 in the extracted result).
  - Embedding can preserve layout, styling, and characters when a recipient lacks a
    font, but not all fonts permit embedding.
  - Embedding only used characters limits later editing; embedding all characters is
    the PowerPoint option intended for editing by others.

- [Change the default resolution for inserting pictures in Office](https://support.microsoft.com/en-us/office/change-the-default-resolution-for-inserting-pictures-in-office-f4aca5b4-6332-48c6-9488-bf5e0094a7d2)
  and [Turn off picture compression](https://support.microsoft.com/en-us/office/turn-off-picture-compression-81a6b603-0266-4451-b08e-fc1bf58da658)
  (Microsoft Support; checked 2026-07-24).
  - Microsoft documents High fidelity/minimal compression and a per-document option
    not to compress images.

- [Video and audio file formats supported in PowerPoint](https://support.microsoft.com/en-us/office/video-and-audio-file-formats-supported-in-powerpoint-d8b12450-26db-4c7b-a5c1-593d3418fb59)
  (Microsoft Support; checked 2026-07-24).
  - PowerPoint supports several audio/video formats and notes deprecations beginning
    in version 2505 for older formats.

Skill impact: the generator records font names but does not install or embed fonts;
availability, embedding rights, substitution, and the exported PDF are checked
manually. It accepts only fully decoded local PNG/JPEG still images, reports effective
DPI, and excludes every audio/video or linked-media feature from its package profile.

### Color API

- [PowerPoint ColorFormat.RGB property](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.colorformat.rgb)
  (Microsoft Learn).

Skill impact: author opaque sRGB colors, label PowerPoint as an RGB workflow, and
block claims of CMYK readiness until printer-approved conversion/proof.

### File formats and macros

- [File formats supported in PowerPoint](https://support.microsoft.com/en-us/office/file-formats-that-are-supported-in-powerpoint-252c6fa0-a4bc-41be-ac82-b77c9773f9dc)
  (Microsoft Support).
  - Identifies `.pptm` as a VBA-containing macro-enabled presentation.

- [Save a presentation that contains VBA macros](https://support.microsoft.com/en-us/office/save-a-presentation-that-contains-vba-macros-e6010530-f899-49a9-9fa5-78338a1c2580)
  (Microsoft Support).
  - Macro-bearing presentations require macro-enabled extensions such as `.pptm`.

Skill impact: accept/generate only `.pptx`, then inspect content types and package
parts rather than trusting the extension alone.

## Office Open XML and packaging

- [ECMA-376](https://ecma-international.org/publications-and-standards/standards/ecma-376/)
  (Ecma International).
  - Defines Office Open XML vocabularies, document representation, and packaging.

- [ISO/IEC 29500-2:2021](https://www.iso.org/standard/77818.html)
  (ISO).
  - Defines Open Packaging Conventions for combining parts and relationships.

- [Open XML SDK overview](https://learn.microsoft.com/en-us/office/open-xml/open-xml-sdk)
  (Microsoft Learn).
  - Connects the SDK and file formats to ECMA-376 and ISO/IEC 29500.

- [IOpcRelationship::GetTargetMode](https://learn.microsoft.com/en-us/windows/win32/api/msopc/nf-msopc-iopcrelationship-gettargetmode)
  (Microsoft Learn).
  - Distinguishes internal package-part targets from external targets.

- [PowerPoint `.pptx` extensions to Office Open XML](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-pptx/efd8bb2d-d888-4e2e-af25-cad476730c9f)
  (Microsoft Open Specifications; published protocol revision shown as 2024-08-20
  during research).

- [PresentationML OLE Object](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.oleobject?view=openxml-3.0.1)
  (Microsoft Learn / ISO schema remarks).
  - OLE objects can contain embedded or linked objects/controls.

- [Presentation NonVisualDrawingProperties](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.nonvisualdrawingproperties?view=openxml-3.0.1)
  (Microsoft Learn / ISO schema remarks).
  - `p:cNvPr` stores nonvisual properties including the drawing description used
    for picture alt text.

Skill impact: bounded ZIP/XML inspection, relationship target/mode checks, rejection
of embedded/active/external content, and standard alt-description markup.

## Python package APIs and versions

### python-pptx

- [python-pptx on PyPI](https://pypi.org/project/python-pptx/)
  - Current stable at cutoff: **1.0.2**, released 2024-08-07.
  - Requires Python 3.8 or later.
  - Described as creating, reading, and updating PowerPoint 2007+ `.pptx` files.

- [python-pptx v1.0.2 repository tag](https://github.com/scanny/python-pptx/tree/v1.0.2)
  (official GitHub repository).
  - GitHub had tags through v1.0.2; the GitHub Releases list returned no published
    releases during the 2026-07-23 check. PyPI release history is therefore the
    version authority used here.

- [Presentation API](https://python-pptx.readthedocs.io/en/latest/api/presentation.html)
  - `Presentation()`, `save`, `slide_width`, and `slide_height`; dimensions are EMU.

- [Shapes API](https://python-pptx.readthedocs.io/en/latest/api/shapes.html)
  - `add_textbox`, `add_picture`, and explicit shape position/size.

- [Text API](https://python-pptx.readthedocs.io/en/latest/api/text.html)
  - Font sizes and text-frame behavior.

Skill impact: exact pin `python-pptx==1.0.2`; use only documented creation, slide,
shape, text, color, and core-property APIs. Alt descriptions are added afterward
using standard PresentationML because the public python-pptx API does not expose a
complete poster accessibility workflow.

### Pillow

- [Pillow on PyPI](https://pypi.org/project/pillow/)
  - Current stable at cutoff: **12.3.0**, released 2026-07-01.
  - Requires Python 3.10 or later.

- [Pillow documentation](https://pillow.readthedocs.io/)
  (documentation identified itself as 12.3.0 at cutoff).

Skill impact: exact pin `Pillow==12.3.0`; bounded verification of local PNG/JPEG
dimensions, mode, frames, and effective DPI. Heavy imports remain lazy so every
CLI's help works without optional packages.

### lxml

- [lxml on PyPI](https://pypi.org/project/lxml/)
  - Current stable at cutoff: **6.1.1**, released 2026-05-18.
  - Requires Python 3.8 or later.
  - The 6.1.1 release includes security-related fixes in bundled XML/XSLT libraries.

Skill impact: exact transitive pin `lxml==6.1.1` for `python-pptx` generation.
The dependency-free inspector still uses bounded standard-library XML parsing and
rejects DTD/entity declarations before parsing.

## Accessibility standards

- [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)
  (W3C Recommendation, 2024-12-12).
  - SC 1.4.1: do not use color as the only visual means of conveying information.
  - SC 1.4.3: 4.5:1 for normal text; 3:1 for large text.
  - Large text: at least 18 pt, or at least 14 pt and bold.
  - SC 1.4.11: 3:1 for graphical parts required to understand content.

Skill impact: exact sRGB contrast calculations with usage-specific thresholds and
mandatory redundant encoding. WCAG is used as a declared design target; no claim is
made that a physical poster or PPTX is a conforming web page.

## Palette authorities

- [ColorBrewer 2](https://colorbrewer2.org/)
  (Penn State/Cynthia Brewer project).
  - Distinguishes qualitative, sequential, and diverging schemes.
  - Offers colorblind-safe, print-friendly, and photocopy-safe filters.

- [Paul Tol, Colour Schemes, issue 3.2](https://sronpersonalpages.nl/~pault/data/colourschemes.pdf)
  (SRON/EPS/TN/09-002, 2021-08-18).
  - Documents clear colour schemes intended to work for colour-blind readers and
    gives scheme-specific values/order.

Skill impact: explain scheme selection and caveats. No bundled palette is represented
as universally accessible; rendered contrast and redundant encoding remain required.

## Conference examples — not universal rules

- [CSCW 2026 posters](https://cscw.acm.org/2026/posters.html)
  (official event page checked 2026-07-24; its explicit 2026 important dates include
  a 2026-07-10 camera-ready deadline).
  - Allocated 48 × 48 inches; recommended no side over 45 inches, allowed up to
    47 inches; stated A0 or A1 could be acceptable.

- [IEEE DSC 2025 poster instructions](https://attend.ieee.org/dsc-2025/call-for-posters/)
  (official organizer page).
  - Required the physical poster to fit A1 space: 84.1 × 59.4 cm.

Skill impact: use these only to demonstrate variation. The validator requires the
actual event's confirmed rule and exact source ID.

## Secure standard-library APIs

- [Python `zipfile`](https://docs.python.org/3/library/zipfile.html)
- [Python `xml.etree.ElementTree`](https://docs.python.org/3/library/xml.etree.elementtree.html)
- [Python `json`](https://docs.python.org/3/library/json.html)

Skill impact: no archive extraction; strict duplicate/non-finite JSON handling;
bounded XML parts; DTD/entity rejection; no network, shell invocation, dynamic code
execution, or arbitrary object deserialization.
