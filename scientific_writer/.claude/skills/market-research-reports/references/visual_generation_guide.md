# Evidence-Led Tables and Visuals

Visuals are optional. Add one only when it answers an analytical question more
clearly than prose or a small table. Do not generate a fixed count, create
decorative cover imagery by default, or call another skill or external image
service.

## Required data contract

Before creating a chart, define:

- claim IDs the visual supports;
- input source IDs and calculation ID;
- geography, population, and coverage;
- observed/estimated/forecast status;
- period and retrieval cutoff;
- currency, base year, and price basis;
- stock/flow/count/share/rate/price/index;
- units and denominator;
- taxonomy and version;
- revision status;
- suppression, missing values, and material limitations.

Build visuals from the validated local data, never from an image prompt that
contains unsupported numbers.

## Choose the smallest useful display

| Analytical question | Preferred display |
|---|---|
| Exact values and metadata | Table |
| Change over ordered time | Line or point chart |
| Category comparison | Ordered dot or bar chart |
| Composition with few categories | Stacked bar |
| Distribution | Histogram, box plot, or interval plot |
| Scenario uncertainty over time | Directly labeled range/ribbon plus paths |
| Top-down vs bottom-up reconciliation | Side-by-side bridge or comparison table |
| Feature availability | Evidence-linked matrix |
| Relationship between two quantities | Scatterplot with units and caveats |
| Process or value chain | Simple flow diagram based on verified entities |

Avoid pie/donut charts for many categories, dual axes, 3-D effects, area scaling
without explanation, radar charts for precise comparison, and unlabeled
quadrant scores.

## Historical and forecast data

- Separate observed and forecast periods with a clear boundary.
- Use different line styles as well as color.
- Label scenarios as conditional; do not label the outer paths as a confidence
  interval.
- Show revisions or vintage when they materially change the historical path.
- Do not splice incompatible series without a break marker and explanation.
- If a historical source ends before the forecast base year, identify the
  bridge estimate.

## TAM/SAM/SOM

Prefer a table or nested bar chart to concentric circles because area can imply
precision and proportionality poorly.

Show:

- top-down and bottom-up TAM separately;
- SAM filters and retained share;
- SOM capture share and horizon;
- downside/base/upside values;
- reconciliation gap;
- denominator and coverage keys;
- sensitivity to principal assumptions.

The caption must say that outputs are conditional scenarios.

## Competitive evidence

### Feature matrix

Use statuses `yes`, `partial`, `no`, `unknown`, and `not-applicable`. Each cell
must map to source IDs and a common product scope, geography, and as-of date.
Do not treat `unknown` as `no`.

### Market shares

Use bars rather than a crowded pie. State:

- relevant product/geographic scope;
- share metric and denominator;
- period;
- unknown/residual share;
- whether values are reported, estimated, or calculated;
- source IDs for numerator and total.

If scope uncertainty is material, show alternate definitions instead of one
authoritative-looking chart.

### Positioning maps

Use only with measurable, defined axes. Publish the scoring rule, evidence per
point, treatment of unknown values, and sensitivity to axis choice. Do not place
firms based on impression alone.

## Survey evidence

Display weighted estimates only with:

- unweighted sample base;
- target population and frame;
- field dates and mode;
- weighting statement;
- appropriate uncertainty or an explicit reason it is unavailable;
- wording or instrument link;
- non-probability label where applicable.

Do not imply that overlapping intervals prove equivalence or that nonoverlap is
the only test of a meaningful difference.

## Regulatory timelines

Distinguish:

- announced or consulted;
- enacted/adopted;
- effective;
- stayed, repealed, or superseded.

Use the official publication and effective dates, not a news article date.

## Accessibility

- Do not rely on color alone.
- Use direct labels where possible.
- Ensure meaningful reading order and alt text.
- Keep text legible at final output size.
- Use patterns or line styles for scenarios.
- Avoid red/green-only encodings.
- Provide the underlying table or data file.

## Caption template

```text
[What the display shows]. Geography: [scope]. Period: [period].
Measure: [unit, denominator, stock/flow]. Currency/base: [if applicable].
Observed through [date]; conditional scenarios thereafter.
Sources: [S-...]. Calculation: [CALC-...]. Retrieval cutoff: [date].
Limitations: [material caveat].
```

## Visual audit

- Every plotted value is reproducible from a local table.
- All source and calculation IDs exist.
- Units, denominators, dates, and price bases are visible.
- Axis starts, scales, truncation, and sorting do not mislead.
- Missing/suppressed values are not rendered as zero.
- Forecast and historical data are visibly distinct.
- Rounding is consistent with evidence precision.
- The visual works in grayscale and with screen readers.
- The report does not require any figure to be considered complete.
