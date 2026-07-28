# Evidence Model and Citation Integrity

This model makes a report auditable at claim level. A bibliography is necessary
but insufficient: each material claim must map to the exact source records,
calculation, and assumptions that support it.

## Statement classes

Label every material statement as one of:

1. **Quantitative fact** — a value directly represented by a cited source.
2. **Quantitative estimate** — a source's or analyst's uncertain estimate.
3. **Qualitative fact** — an attributable event, policy, feature, or statement.
4. **Calculation** — deterministic transformation of cited inputs.
5. **Forecast** — conditional future path based on stated assumptions.
6. **Opinion** — attributed respondent or analyst judgment.
7. **Recommendation** — decision advice derived from findings and objectives.

Do not rewrite an estimate as a fact, a scenario as a prediction, an interview
theme as prevalence, or a recommendation as an evidence claim.

## Source record

Give each source a stable ID such as `S-001`. Record:

- title, publisher/author, URL or persistent identifier;
- source type and original data producer;
- publication date and retrieval date;
- archived local snapshot path, if legally permitted;
- geography and covered population;
- currency, base year, and nominal/real/current/constant/chained basis;
- stock, flow, count, share, rate, price, index, or mixed measure;
- unit and denominator;
- industry/product taxonomy and version;
- preliminary/revised/final/vintage/current status;
- collection or estimation method;
- survey frame, mode, sample, weighting, and response information when relevant;
- limitations, suppression, imputation, breaks, and known revisions;
- license, terms, and attribution requirements.

For an aggregator, record both the delivery platform and original producer. For
example, a FRED series should retain its original agency/source metadata; FRED
availability does not erase third-party rights or methodology.

## Claim record

Give each claim a stable ID such as `C-014`. Record:

- exact claim text;
- statement class;
- one or more source IDs;
- report location;
- as-of date and geography;
- currency/base year/price basis, measure type, unit, and denominator;
- taxonomy and version;
- revision status;
- calculation ID and assumption IDs where applicable;
- a calibrated confidence label and reasons;
- limitations or conflicts material to interpretation.

One citation at the end of a paragraph does not automatically support every
sentence in the paragraph. Split compound claims when different sources support
different components.

## Source hierarchy

Use fitness for the claim, not prestige alone. A practical default:

1. primary law, regulator decision, official filing, or official statistic;
2. original company filing or attributable first-party operating disclosure;
3. transparent survey or study with inspectable methods;
4. peer-reviewed or institutional research using identifiable primary data;
5. industry association data with disclosed coverage and methods;
6. reputable secondary synthesis;
7. paid market estimate with inspectable scope/method and lawful access;
8. news or commentary for leads and attributable events, not unsupported size
   estimates.

The best source can differ by claim. A company filing is authoritative about
reported company revenue but not automatically about total market size. An
official industry total may be authoritative but too broad for the product
market being studied.

## Conflicting evidence

Never choose the most convenient number silently.

1. Compare definitions, period, geography, currency, price basis, unit,
   denominator, taxonomy, sample, and revision vintage.
2. Determine whether values are genuinely conflicting or merely different
   measures.
3. Prefer the source closest to the primary observation and fit to the claim.
4. If both remain plausible, retain a range or parallel estimates.
5. Document the conflict, decision rule, and sensitivity to the choice.
6. Do not average incompatible estimates.

## Revisions and vintages

- Record retrieval date for every online source.
- Record a dataset vintage or release identifier when available.
- Preserve the original input snapshot or checksum when terms permit.
- Mark preliminary data and expected revisions.
- On refresh, compare new and prior values; do not overwrite silently.
- Use archived/vintage systems where needed for reproducibility.
- For sources that expose only the latest version, preserve the retrieved file
  and state that historical versions are not supplied by the API.

## Calculation lineage

Each calculation record should identify:

- formula and calculation ID;
- exact input fields and source IDs;
- exclusions and coverage keys;
- conversions, exchange-rate source/date, and deflator/index;
- rounding policy;
- intermediate values;
- output unit and denominator;
- assumptions and sensitivity values;
- software/script version or command used.

Do not cite a calculated result as if it appeared verbatim in a source.

## Source integrity failures to avoid

- fabricated citations, URLs, access dates, quotes, or paid figures;
- citing a search-result snippet instead of the underlying source;
- citation laundering through an aggregator or secondary article;
- using a source outside its geographic, temporal, or definitional scope;
- omitting a correction, restatement, or revision;
- attributing a denominator from one source to a numerator from another without
  reconciliation;
- claiming that multiple citations are independent when they reproduce one
  underlying estimate;
- treating absence of public evidence as evidence of absence.

## Minimum audit

Before release:

1. validate the source ledger;
2. audit every factual, estimate, calculation, and forecast claim;
3. resolve missing source IDs;
4. review unused sources and citation clusters;
5. spot-check every headline number against the archived source;
6. reproduce market-size and forecast outputs from local inputs;
7. rerun unit/currency/base-year consistency checks;
8. retain unresolved conflicts and limitations in the report.
