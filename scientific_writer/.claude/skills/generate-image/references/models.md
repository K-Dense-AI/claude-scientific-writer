# OpenRouter image model reference

Snapshot of `GET https://openrouter.ai/api/v1/images/models`, taken 2026-07-26 (38 models).
The catalogue moves; re-read it rather than trusting this table:

```bash
python scripts/generate_image.py --list-models
```

No API key is needed to list models.

## Capability table

`refs` is the maximum number of `input_references` accepted; `n` is images per request.

| Model | n | refs | stream | Parameters |
| --- | --- | --- | --- | --- |
| `google/gemini-3.1-flash-image` | 1 | 14 | no | aspect_ratio, resolution, n, input_references |
| `google/gemini-3.1-flash-image-preview` | 1 | 14 | no | aspect_ratio, resolution, n, input_references |
| `google/gemini-3.1-flash-lite-image` | 1 | 14 | no | aspect_ratio, resolution, n, input_references |
| `google/gemini-3-pro-image` | 1 | 14 | no | aspect_ratio, resolution, n, input_references |
| `google/gemini-3-pro-image-preview` | 1 | 14 | no | aspect_ratio, resolution, n, input_references |
| `google/gemini-2.5-flash-image` | 1 | 3 | no | aspect_ratio, n, input_references |
| `black-forest-labs/flux.2-pro` | 1 | 8 | no | aspect_ratio, output_format, seed, n, input_references |
| `black-forest-labs/flux.2-max` | 1 | 8 | no | aspect_ratio, output_format, seed, n, input_references |
| `black-forest-labs/flux.2-flex` | 1 | 8 | no | aspect_ratio, output_format, seed, n, input_references |
| `black-forest-labs/flux.2-klein-4b` | 1 | 4 | no | aspect_ratio, output_format, seed, n, input_references |
| `bytedance-seed/seedream-4.5` | 10 | 14 | no | aspect_ratio, resolution, seed, n, input_references |
| `openai/gpt-image-2` | 10 | 16 | yes | aspect_ratio, background, quality, output_compression, n, input_references |
| `openai/gpt-image-1` | 10 | 16 | yes | aspect_ratio, background, quality, output_compression, n, input_references |
| `openai/gpt-image-1-mini` | 10 | 16 | yes | aspect_ratio, background, quality, output_compression, n, input_references |
| `openai/gpt-5.4-image-2` | 10 | 16 | yes | background, quality, output_compression, n, input_references |
| `openai/gpt-5-image` | 10 | 16 | yes | background, quality, output_compression, n, input_references |
| `openai/gpt-5-image-mini` | 10 | 16 | yes | background, quality, output_compression, n, input_references |
| `recraft/recraft-v4.1-pro` | 6 | 1 | no | aspect_ratio, n, input_references |
| `recraft/recraft-v4.1` | 6 | 1 | no | aspect_ratio, n, input_references |
| `recraft/recraft-v4.1-vector` | 6 | 1 | no | aspect_ratio, n, input_references |
| `recraft/recraft-v4.1-pro-vector` | 6 | 1 | no | aspect_ratio, n, input_references |
| `recraft/recraft-v4.1-utility` | 6 | 1 | no | aspect_ratio, n, input_references |
| `recraft/recraft-v4.1-utility-pro` | 6 | 1 | no | aspect_ratio, n, input_references |
| `recraft/recraft-v4-pro` | 6 | 1 | no | aspect_ratio, n, input_references |
| `recraft/recraft-v4` | 6 | 1 | no | aspect_ratio, n, input_references |
| `recraft/recraft-v4-vector` | 6 | 1 | no | aspect_ratio, n, input_references |
| `recraft/recraft-v4-pro-vector` | 6 | 1 | no | aspect_ratio, n, input_references |
| `recraft/recraft-v3` | 6 | 1 | no | aspect_ratio, n, input_references |
| `sourceful/riverflow-v2.5-pro` | 1 | 10 | no | aspect_ratio, background, output_format, resolution, n, input_references |
| `sourceful/riverflow-v2.5-fast` | 1 | 4 | no | aspect_ratio, background, output_format, resolution, n, input_references |
| `sourceful/riverflow-v2-pro` | 1 | 10 | no | aspect_ratio, resolution, n, input_references |
| `sourceful/riverflow-v2-fast` | 1 | 4 | no | aspect_ratio, resolution, n, input_references |
| `microsoft/mai-image-2.5-pro` | 1 | 1 | no | aspect_ratio, n, input_references |
| `microsoft/mai-image-2.5` | 1 | 1 | no | aspect_ratio, n, input_references |
| `krea/krea-2-large` | — | 1 | no | aspect_ratio, resolution, seed, input_references |
| `krea/krea-2-medium` | — | 1 | no | aspect_ratio, resolution, seed, input_references |
| `krea/krea-2-medium-turbo` | — | 1 | no | aspect_ratio, resolution, seed, input_references |
| `x-ai/grok-imagine-image-quality` | 1 | 3 | no | aspect_ratio, resolution, n, input_references |

## Reading the parameter columns

Parameters are not universal, and an unsupported one is **rejected, not ignored**:

- `resolution` (`512`, `1K`, `2K`, `4K`) — Gemini, Seedream, Riverflow, Krea, Grok. Not FLUX.
- `output_format` — FLUX (`png`, `jpeg`) and Riverflow 2.5. Gemini does not take it.
- `quality`, `background`, `output_compression` — the OpenAI family (`background` also on Riverflow 2.5).
- `seed` — FLUX, Seedream, Krea. Not Gemini, not OpenAI.
- `aspect_ratio` — nearly everything, but the enum differs. FLUX 2 Pro accepts
  `1:1, 4:3, 3:4, 3:2, 2:3, 16:9, 9:16, 21:9, auto`.

Per-model detail, including provider-specific passthrough parameters and pricing:

```bash
curl -s https://openrouter.ai/api/v1/images/models/black-forest-labs/flux.2-pro/endpoints
```

FLUX 2 Pro, for example, allows `steps`, `guidance`, and `safety_tolerance` as passthrough
parameters and bills $0.03 per output megapixel.

## Choosing a model

- **General quality, prompt adherence** — `google/gemini-3.1-flash-image` (skill default), or
  `google/gemini-3-pro-image` for the higher tier.
- **Photoreal and artistic control, seeded reproducibility** — `black-forest-labs/flux.2-pro`.
- **Cheap iteration** — `black-forest-labs/flux.2-klein-4b`, `google/gemini-3.1-flash-lite-image`.
- **Batches** — `bytedance-seed/seedream-4.5` or the OpenAI family (up to 10 per request).
- **True vector output (SVG)** — `recraft/recraft-v4-vector`, `recraft/recraft-v4.1-vector`, and
  the `-pro-vector` variants. These return `media_type: image/svg+xml`.
- **Transparent backgrounds** — the OpenAI family via `--background transparent`.
- **Heavy multi-reference compositing** — OpenAI (16 references), Gemini and Seedream (14).

## Provider routing

The Image API accepts the same `provider` block as chat completions — `provider.only`,
`provider.order`, `provider.ignore`, `provider.sort` (`price`, `throughput`, `latency`), and
`provider.allow_fallbacks`. The bundled script does not expose these; send a direct request when
routing control matters.

## Billing

Image billing is all-or-nothing: a generation either completes and is billed in full, or fails and
is not billed. Partial preview frames delivered during streaming are not charged separately.
Per-request cost comes back in `usage.cost`, which the script prints.
