# Poster design and accessibility principles

## Requirements outrank conventions

There is no universal poster size, orientation, grid, body font, margin, image DPI,
word count, or number of columns. Confirm the current organizer and printer rules,
record exact source IDs, and design against those constraints.

Use generic advice only as a labeled project heuristic. Do not transform a heuristic
into a conference or accessibility requirement.

## Visual hierarchy

Make the research question, key result, and interpretation easy to locate without
forcing every poster into one visual style.

- Use a small, consistent set of text roles.
- Prefer left-aligned body text for left-to-right languages unless language or design
  requirements indicate otherwise.
- Keep related evidence, caption, and interpretation spatially grouped.
- Use spacing, alignment, size, and weight before adding decorative effects.
- Avoid unexplained icons, dense backgrounds, and text over uncontrolled imagery.
- Do not rely on a predicted "eye pattern"; confirm the actual reading order.

The generated PPTX uses fixed font sizes and disables text auto-shrink. A visual check
is still required because the XML package does not reveal font substitution or
rendered overflow.

## Font size means final-output size

PowerPoint stores point sizes on the PPTX canvas. When the printer scales the canvas,
the physical text scales too:

`final point size = design point size × physical artboard width / canvas width`

Use the same ratio on height; unequal ratios are prohibited.

Microsoft's PowerPoint accessibility guidance recommends 18 pt or larger for ordinary
slides. That is a [Microsoft slide recommendation](https://support.microsoft.com/en-us/office/make-your-powerpoint-presentations-accessible-to-people-with-disabilities-6f7772b2-2f33-4bd2-8ca7-dae3b2b3ef25),
not a universal poster minimum. Poster viewing distance, typeface, substrate, lighting,
audience, and organizer rules can require larger text.

The manifest therefore requires:

- a final-output minimum;
- a basis labeled `heuristic`, `source_specific`,
  `conference_requirement`, or `printer_requirement`;
- an exact source ID for every non-heuristic basis.

Test a reduced-scale print and the full-size proof under expected viewing conditions.

## Font availability and substitution

A typeface name in PresentationML is a request, not proof that the font is installed,
licensed for embedding, or rendered identically by another workstation. Microsoft's
[font-embedding guidance](https://support.microsoft.com/en-us/office/benefits-of-embedding-custom-fonts-cb3982aa-ea76-4323-b008-86670f222dbc)
notes that embedding can preserve layout but that not every font permits it and that
embedding only used characters limits editing.

The generator does not install or embed fonts. Before release:

- use fonts licensed for the intended authoring, sharing, embedding, and print use;
- confirm every declared face is installed on the review/export workstation;
- inspect substitutions, missing glyphs, equations, and line wrapping in PowerPoint;
- decide with the printer whether embedding is appropriate and permitted;
- inspect the actual exported PDF's font records and rendered glyphs.

## Text contrast

[WCAG 2.2 SC 1.4.3](https://www.w3.org/TR/WCAG22/#contrast-minimum) specifies:

- 4.5:1 for normal text;
- 3:1 for large text, defined as at least 18 pt, or at least 14 pt and bold.

WCAG is written for web content. This skill uses its sRGB contrast mathematics and
thresholds as an explicit design target for poster/PPTX color pairs; a passing ratio
does not by itself establish that a physical poster or exported PDF conforms to WCAG.
Print conversion, transparency, gradients, images behind text, paper, glare, and
lighting require manual review and proofing.

The manifest declares each foreground/background pair and its usage. Text elements
must reference a declared pair. The validator rejects a pair below its declared
threshold.

## Non-text contrast and color redundancy

[WCAG 2.2 SC 1.4.11](https://www.w3.org/TR/WCAG22/#non-text-contrast) uses 3:1
against adjacent colors for graphical parts required to understand content.
[SC 1.4.1](https://www.w3.org/TR/WCAG22/#use-of-color) says color must not be
the only visual means of conveying information.

For plots and diagrams:

- directly label important series and regions when practical;
- combine color with shape, marker, pattern, line style, position, or text;
- retain meaningful distinctions in grayscale;
- avoid assigning semantic meaning to a hue without another cue;
- check the rendered figure, not just the palette's color list.

The palette checker reports exact pair ratios and heuristic grayscale L* separation.
It explicitly does not certify color-vision accessibility.

## Choosing palettes

[ColorBrewer](https://colorbrewer2.org/) separates qualitative, sequential, and
diverging schemes and provides filters for colorblind-safe, print-friendly, and
photocopy-safe options. Its palettes were designed for maps; use the data-type logic,
then test the actual poster figure and background.

[Paul Tol's colour-scheme technical note](https://sronpersonalpages.nl/~pault/data/colourschemes.pdf)
provides schemes intended to remain clear for color-blind readers. Choose a scheme
for its documented purpose and supported category count. Do not assume every color
in a named scheme has sufficient text or line contrast against white.

Palette provenance does not replace contrast checks, redundant encodings, color-vision
simulation, or print proofing.

## Alt text and native text

Microsoft says visuals need concise alternative text describing their purpose and
important content. See
[Make PowerPoint presentations accessible](https://support.microsoft.com/en-us/office/make-your-powerpoint-presentations-accessible-to-people-with-disabilities-6f7772b2-2f33-4bd2-8ca7-dae3b2b3ef25).

This generator requires approved alt text for every local picture and writes it to
the standard PresentationML nonvisual drawing description. The technical inspector
checks that the description exists. It also supports a source-bound native text
element as a long description for a complex figure.

Alt text still needs human review:

- describe the purpose and essential conclusion, not every pixel;
- avoid repeating adjacent text verbatim;
- do not begin with redundant phrases such as "image of";
- include essential values and relationships when they are not available in nearby
  native text;
- keep important words as native PowerPoint text rather than only inside a raster
  image.

When concise alt text and adjacent prose do not communicate a figure's essential
relationships, values, uncertainty, and conclusion, set
`long_description_element_id` to an approved native body/caption/other text element.
It must follow the image in reading order and cite every source used by the image.
The structural check cannot determine whether the long description is scientifically
or semantically complete.

An XML attribute being present does not prove that the description is accurate.

## Reading order

Screen readers use an object's reading order, which can differ from its visual
position. Microsoft recommends the Accessibility Checker and Reading Order pane.

The manifest requires the visible title first, then contiguous `reading_order` values.
The generator uses a native title placeholder, adds remaining shapes in that order,
and writes explicit language on text runs. This is only a deterministic starting
point. In the final PowerPoint:

1. run Review > Check Accessibility;
2. inspect the Reading Order pane;
3. verify every object name and sequence;
4. navigate with a keyboard;
5. test with a screen reader.

Groups, charts, SmartArt, decorative objects, and exported PDF tags need separate
manual review. The strict generator intentionally limits its shape set to native text
boxes and local pictures.

## QR codes and links

A QR code is not an accessibility substitute.

- Include the exact destination URL as visible native text.
- Use meaningful surrounding language that describes the destination.
- Add alt text to the QR image.
- Keep the fallback text in logical reading order.
- Test the final exported/printed code with multiple devices.
- Do not put essential content only behind the QR destination.

The generator does not create a clickable external relationship. This allows the
package inspector to reject all external relationships consistently.

## Raster quality

File metadata DPI does not determine poster quality. Use effective DPI:

`effective DPI = source pixels / final placed inches`

Calculate it independently for width and height at the final physical output. The
asset inventory reports the lower value. The threshold must be labeled as a heuristic
or tied to the exact organizer/printer/source rule.

PowerPoint can compress inserted pictures. Microsoft documents High fidelity and
per-document "Do not compress images in file" settings. Review those settings in the
actual export application, then inspect the PDF and proof for resampling; the source
PPTX effective-DPI calculation does not prove export resolution.

Vector artwork may be preferable for line art, but this strict generator accepts only
bounded local PNG/JPEG assets. If vector content is required, convert it through an
author-reviewed, offline workflow and verify the rasterized result and text
accessibility; do not silently substitute or redraw scientific content.

## Audio, video, and linked media

PowerPoint supports audio and video, including formats and linked-file workflows that
vary by version. None is needed for a static printed poster. The strict manifest and
package profile therefore allow only local PNG/JPEG still images and reject audio,
video, linked media, transitions, timing, and other interactive content. Put optional
external material behind a visible, verified URL/QR fallback rather than embedding or
linking media in the PPTX.

## Manual accessibility gate

Before release:

- run PowerPoint's Accessibility Checker;
- verify reading order and object names;
- review every alt text and native long description;
- test screen-reader and keyboard navigation;
- inspect text contrast, non-text contrast, and redundant encoding;
- review reduced-scale and full-size proofs;
- verify exported PDF tags and reading order;
- test visible fallback links and QR codes;
- get author and accessibility-reviewer sign-off.

Automation finds technical defects. It cannot certify accessibility or scientific
accuracy.
