---
name: generate-image
description: Generate or edit images with AI models through the OpenRouter Image API (Gemini, FLUX, Seedream, Recraft, GPT-Image). Use for photos, illustrations, artwork, concept art, visual assets, logos, and image editing or compositing from reference images. For flowcharts, circuits, pathways, and other technical diagrams, use the scientific-schematics skill instead.
license: MIT
compatibility: Requires Python 3.9+ and network access to openrouter.ai. The bundled script uses only the standard library. Image generation requires the OPENROUTER_API_KEY credential and bills per request; listing models does not. Targets the OpenRouter Image API (POST /api/v1/images) as documented on 2026-07-26.
allowed-tools: Read Write Edit Bash
metadata:
  version: "2.0"
  skill-author: K-Dense Inc.
  last-reviewed: "2026-07-26"
  openclaw:
    primaryEnv: OPENROUTER_API_KEY
    envVars:
      - name: OPENROUTER_API_KEY
        required: true
        description: OpenRouter API key used for image generation.
---

# Generate Image

Generate and edit images through OpenRouter's Image API, which reaches Gemini, FLUX, Seedream,
Recraft, GPT-Image, and roughly thirty other models behind one request shape.

## When to use

**Use this skill for:** photos and photorealistic images, illustrations and artwork, concept art,
presentation and poster visuals, logos and vector marks, image editing, and compositing from
reference images.

**Use `scientific-schematics` instead for:** flowcharts, circuit diagrams, biological pathways,
system architecture diagrams, CONSORT diagrams, and other technical schematics.

## API key

Generation requires an OpenRouter key. The script resolves it in this order:

1. `--api-key`
2. the `OPENROUTER_API_KEY` environment variable
3. `OPENROUTER_API_KEY=` in a `.env` file, searching the working directory upward

If none is present the script exits with setup instructions. Keys: https://openrouter.ai/keys

`--list-models` needs no key.

## Quick start

```bash
# Generate
python scripts/generate_image.py "A beautiful sunset over mountains"

# Edit an existing image
python scripts/generate_image.py "Make the sky purple" -i photo.jpg -o edited.png
```

Output defaults to `generated_image.<ext>`, where the extension follows the media type the model
returned. The per-request cost is printed from `usage.cost`.

## Choosing a model

Default: `google/gemini-3.1-flash-image`.

| Need | Model |
| --- | --- |
| General quality, prompt adherence | `google/gemini-3.1-flash-image` |
| Highest Gemini tier | `google/gemini-3-pro-image` |
| Photoreal control, reproducible seeds | `black-forest-labs/flux.2-pro` |
| Cheap iteration | `black-forest-labs/flux.2-klein-4b` |
| Several images per request | `bytedance-seed/seedream-4.5`, `openai/gpt-image-2` |
| Vector / SVG output | `recraft/recraft-v4-vector` |
| Transparent background | `openai/gpt-image-2` with `--background transparent` |

`references/models.md` carries the full catalogue with per-model parameter support. The live
listing is authoritative:

```bash
python scripts/generate_image.py --list-models
```

## Parameter support varies by model

This is the main thing to get right. Models advertise different parameter sets, and **sending a
parameter a model does not support is rejected, not ignored**. The script omits every flag you do
not pass, so pass only what the target model accepts.

- `--resolution` (`512`, `1K`, `2K`, `4K`) — Gemini, Seedream, Riverflow, Krea, Grok. **Not FLUX.**
- `--output-format` — FLUX and Riverflow 2.5. **Not Gemini.**
- `--quality`, `--background`, `--output-compression` — the OpenAI family.
- `--seed` — FLUX, Seedream, Krea. **Not Gemini, not OpenAI.**
- `--aspect-ratio` — nearly all models, but the allowed enum differs.
- `--n` — capped per model: 1 for Gemini and FLUX, 6 for Recraft, 10 for Seedream and OpenAI.

On an HTTP 400 the script prints OpenRouter's message and points at `--list-models`.

## Editing and reference images

`-i/--input` is repeatable and accepts local paths, HTTP(S) URLs, or data URLs. Local files are
base64-encoded and sent as `input_references`.

```bash
# Single-image edit
python scripts/generate_image.py "Add sunglasses to the person" -i portrait.png

# Composite several references
python scripts/generate_image.py "Blend these two styles" -i style_a.png -i style_b.jpg -o blend.png

# Reference an image already on the web
python scripts/generate_image.py "Restyle as a watercolor" -i https://example.com/photo.jpg
```

Reference limits differ: 16 for OpenAI, 14 for Gemini and Seedream, 8 for FLUX, 1 for Recraft and
MAI. Accepted local formats: PNG, JPEG, GIF, WebP.

## Worked examples

```bash
# Wide hero image for a poster
python scripts/generate_image.py \
  "Laboratory with modern equipment, photorealistic, well-lit" \
  -m black-forest-labs/flux.2-pro --aspect-ratio 21:9 -o poster/hero.png

# Conceptual figure for a manuscript
python scripts/generate_image.py \
  "Microscopic view of cancer cells attacked by immunotherapy agents, scientific illustration" \
  --resolution 2K -o figures/immunotherapy_concept.png

# Vector logo
python scripts/generate_image.py \
  "Minimal geometric fox logo, two colors" \
  -m recraft/recraft-v4-vector -o assets/logo.svg

# Slide background with a transparent alpha channel
python scripts/generate_image.py \
  "Abstract molecular pattern, subtle, blue and white" \
  -m openai/gpt-image-2 --background transparent -o slides/bg.png

# Four variations in one request
python scripts/generate_image.py \
  "Stylized neuron network illustration" \
  -m bytedance-seed/seedream-4.5 --n 4 -o variations.png
# -> variations_1.png ... variations_4.png

# Reproducible output
python scripts/generate_image.py "A cat astronaut" \
  -m black-forest-labs/flux.2-pro --seed 42
```

## Script parameters

| Flag | Purpose |
| --- | --- |
| `prompt` | Image description, or the edit to apply (required unless `--list-models`) |
| `-m`, `--model` | Model slug (default `google/gemini-3.1-flash-image`) |
| `-o`, `--output` | Output path; extension defaults to the returned media type |
| `-i`, `--input` | Reference image — path, URL, or data URL. Repeatable |
| `--n` | Images per request, model-capped |
| `--aspect-ratio` | `1:1`, `16:9`, `9:16`, `4:3`, `3:2`, `21:9`, … |
| `--resolution` | `512`, `1K`, `2K`, `4K` |
| `--size` | Explicit pixels, e.g. `2048x2048` |
| `--quality` | `auto`, `low`, `medium`, `high` |
| `--output-format` | `png`, `jpeg`, `webp`, `svg` |
| `--background` | `auto`, `transparent`, `opaque` |
| `--output-compression` | 0–100, for WebP/JPEG |
| `--seed` | Deterministic output where supported |
| `--api-key` | Overrides the environment and `.env` |
| `--timeout` | Request timeout, seconds (default 300) |
| `--list-models` | Print the catalogue with parameter support, then exit |

## API shape

For direct requests without the script:

```bash
curl -s https://openrouter.ai/api/v1/images \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-3.1-flash-image",
    "prompt": "A red bicycle against a white wall",
    "aspect_ratio": "16:9"
  }'
```

Response:

```json
{
  "created": 1748372400,
  "data": [{ "b64_json": "<base64>", "media_type": "image/png" }],
  "usage": { "prompt_tokens": 0, "completion_tokens": 4175, "total_tokens": 4175, "cost": 0.04 }
}
```

`b64_json` is raw base64, **not** a data URL. `media_type` reflects the real format, so honour it
when naming files — vector models return `image/svg+xml`.

Streaming (`"stream": true`) emits `image_generation.partial_image`, `image_generation.completed`,
and `error` events, terminating with `data: [DONE]`. Only the OpenAI models support it, and the
bundled script does not use it.

Billing is all-or-nothing: a generation is either completed and billed in full, or it fails and is
not billed. Streaming preview frames are not charged separately.

## Notes and caveats

- Generation is a paid API call. Prefer a cheap model while iterating on a prompt.
- Generation takes roughly 5–60 seconds depending on model and resolution.
- Reference images are uploaded to OpenRouter. Do not send unpublished or sensitive data.
- Never hardcode the API key. Keep it in the environment or an ignored `.env`.
- Prompt specifically when editing: "change the sky to sunset colours" beats "edit the sky".

## Related skills

- `scientific-schematics` — technical diagrams, flowcharts, circuits, pathways
- `scientific-slides` — presentations that embed generated visuals
- `latex-posters` — posters that embed hero images
