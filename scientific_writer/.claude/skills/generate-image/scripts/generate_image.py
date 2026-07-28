#!/usr/bin/env python3
"""
Generate and edit images through the OpenRouter Image API (POST /api/v1/images).

The Image API is model-agnostic: the same request shape reaches Gemini, FLUX,
Seedream, Recraft, GPT-Image, and the rest of the image catalogue. Responses
carry base64 payloads in ``data[].b64_json`` alongside the concrete
``media_type``, so the output extension follows what the model actually
returned rather than an assumption.

Reference images (image-to-image and editing) go in ``input_references`` as
HTTP(S) URLs or base64 data URLs.

Only the standard library is required.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API_BASE = "https://openrouter.ai/api/v1"
IMAGES_URL = f"{API_BASE}/images"
MODELS_URL = f"{API_BASE}/images/models"

DEFAULT_MODEL = "google/gemini-3.1-flash-image"

# media_type -> file extension. Vector-capable models return image/svg+xml.
EXTENSIONS = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "image/svg+xml": ".svg",
}

# Local file extension -> MIME type, for encoding reference images.
INPUT_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


class ApiError(RuntimeError):
    """An error surfaced by the OpenRouter API or the transport beneath it."""


def find_api_key(explicit: str | None = None) -> str:
    """Resolve the API key from --api-key, the environment, then any .env file."""
    if explicit:
        return explicit

    from_env = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if from_env:
        return from_env

    cwd = Path.cwd()
    for directory in [cwd, *cwd.parents]:
        env_file = directory / ".env"
        if not env_file.is_file():
            continue
        try:
            content = env_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for raw in content.splitlines():
            line = raw.strip()
            if line.startswith("#") or "=" not in line:
                continue
            name, _, value = line.partition("=")
            if name.strip() == "OPENROUTER_API_KEY":
                value = value.strip().strip('"').strip("'")
                if value:
                    return value

    raise ApiError(
        "OPENROUTER_API_KEY not found.\n"
        "  export OPENROUTER_API_KEY=your-key\n"
        "  or add OPENROUTER_API_KEY=your-key to a .env file\n"
        "  or pass --api-key\n"
        "Keys: https://openrouter.ai/keys"
    )


def encode_reference(source: str) -> str:
    """Return an image reference as a URL the API accepts.

    HTTP(S) URLs and existing data URLs pass through; local paths are read and
    encoded as base64 data URLs.
    """
    if source.startswith(("http://", "https://", "data:")):
        return source

    path = Path(source)
    if not path.is_file():
        raise ApiError(f"Reference image not found: {source}")

    mime = INPUT_MIME.get(path.suffix.lower())
    if mime is None:
        supported = ", ".join(sorted(INPUT_MIME))
        raise ApiError(
            f"Unsupported reference image type '{path.suffix}' ({source}). "
            f"Supported: {supported}"
        )

    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def request_json(url: str, api_key: str | None, payload: dict | None, timeout: float) -> Any:
    """POST (or GET when payload is None) and decode the JSON response."""
    headers = {"Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        detail = body
        try:
            parsed = json.loads(body)
            detail = parsed.get("error", {}).get("message") or body
        except (json.JSONDecodeError, AttributeError):
            pass
        hint = ""
        if exc.code == 400:
            hint = (
                "\nParameter support varies by model. Check what this model accepts:\n"
                "  python generate_image.py --list-models"
            )
        raise ApiError(f"OpenRouter returned HTTP {exc.code}: {detail}{hint}") from exc
    except urllib.error.URLError as exc:
        raise ApiError(f"Could not reach OpenRouter: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise ApiError(f"OpenRouter returned a non-JSON response: {exc}") from exc


def build_payload(args: argparse.Namespace) -> dict:
    """Assemble the request body, omitting every parameter the caller left unset.

    Omission matters: models advertise different parameter sets, and sending one
    a model does not support is rejected rather than ignored.
    """
    payload: dict[str, Any] = {"model": args.model, "prompt": args.prompt}

    optional = {
        "n": args.n,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "size": args.size,
        "quality": args.quality,
        "output_format": args.output_format,
        "background": args.background,
        "output_compression": args.output_compression,
        "seed": args.seed,
    }
    payload.update({key: value for key, value in optional.items() if value is not None})

    if args.input:
        payload["input_references"] = [
            {"type": "image_url", "image_url": {"url": encode_reference(src)}}
            for src in args.input
        ]

    return payload


def output_paths(requested: str | None, media_type: str, count: int) -> list[Path]:
    """Choose filenames for the returned images.

    The extension follows the model's media_type unless the caller named a file
    explicitly, in which case their choice is kept and a mismatch is reported.
    """
    extension = EXTENSIONS.get(media_type, ".png")

    if requested is None:
        stem, suffix = Path("generated_image"), extension
    else:
        given = Path(requested)
        stem, suffix = given.with_suffix(""), given.suffix or extension
        if given.suffix and given.suffix.lower() != extension:
            print(
                f"Note: model returned {media_type} but --output ends in "
                f"'{given.suffix}'; writing the returned bytes under that name.",
                file=sys.stderr,
            )

    if count == 1:
        return [stem.with_suffix(suffix)]
    return [stem.parent / f"{stem.name}_{i + 1}{suffix}" for i in range(count)]


def save_images(result: dict, requested_output: str | None) -> list[Path]:
    """Decode data[].b64_json into files and return the paths written."""
    items = result.get("data")
    if not items:
        raise ApiError(
            "Response contained no images.\n"
            f"Raw response: {json.dumps(result, indent=2)[:800]}"
        )

    first_media = items[0].get("media_type", "image/png")
    paths = output_paths(requested_output, first_media, len(items))
    written: list[Path] = []

    for item, path in zip(items, paths):
        payload = item.get("b64_json")
        if not payload:
            print(f"Skipping an entry with no b64_json: {list(item)}", file=sys.stderr)
            continue
        if "," in payload and payload.startswith("data:"):
            payload = payload.split(",", 1)[1]
        if str(path.parent) not in ("", "."):
            path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(base64.b64decode(payload))
        written.append(path)

    if not written:
        raise ApiError("Response carried image entries but none contained data.")
    return written


def list_models(timeout: float) -> int:
    """Print the image catalogue with each model's supported parameters."""
    result = request_json(MODELS_URL, None, None, timeout)
    models = result.get("data", [])
    if not models:
        print("No models returned.", file=sys.stderr)
        return 1

    print(f"{len(models)} image models available\n")
    for model in sorted(models, key=lambda m: m.get("id", "")):
        params = model.get("supported_parameters") or {}
        n_spec = params.get("n") or {}
        refs = params.get("input_references") or {}
        print(f"{model.get('id', '?')}")
        print(
            f"    images/request: up to {n_spec.get('max', 1)}"
            f" | reference images: up to {refs.get('max', 0)}"
            f" | streaming: {'yes' if model.get('supports_streaming') else 'no'}"
        )
        if params:
            print(f"    parameters: {', '.join(sorted(params))}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate or edit images via the OpenRouter Image API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate with the default model
  python generate_image.py "A beautiful sunset over mountains"

  # Pick a model and shape
  python generate_image.py "A cat in space" -m black-forest-labs/flux.2-pro --aspect-ratio 16:9

  # Edit an existing image
  python generate_image.py "Make the sky purple" -i photo.jpg -o edited.png

  # Composite from several references (model-dependent limit)
  python generate_image.py "Blend these styles" -i a.png -i b.png -o blended.png

  # Vector output
  python generate_image.py "Minimal fox logo" -m recraft/recraft-v4-vector -o logo.svg

  # Inspect the catalogue and per-model parameter support
  python generate_image.py --list-models
""",
    )

    parser.add_argument("prompt", nargs="?", help="Description of the image, or the edit to apply")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL,
                        help=f"Model slug (default: {DEFAULT_MODEL})")
    parser.add_argument("--output", "-o",
                        help="Output path; extension defaults to the returned media type")
    parser.add_argument("--input", "-i", action="append", metavar="IMAGE",
                        help="Reference image: local path, HTTP(S) URL, or data URL. Repeatable.")
    parser.add_argument("--n", type=int, help="Number of images (model-dependent maximum)")
    parser.add_argument("--aspect-ratio", help="e.g. 1:1, 16:9, 9:16, 4:3, 3:2, 21:9")
    parser.add_argument("--resolution", help="Tier: 512, 1K, 2K, 4K")
    parser.add_argument("--size", help='Explicit pixels, e.g. "2048x2048"')
    parser.add_argument("--quality", choices=["auto", "low", "medium", "high"])
    parser.add_argument("--output-format", choices=["png", "jpeg", "webp", "svg"])
    parser.add_argument("--background", choices=["auto", "transparent", "opaque"])
    parser.add_argument("--output-compression", type=int, metavar="0-100",
                        help="Compression for webp/jpeg output")
    parser.add_argument("--seed", type=int, help="Seed for deterministic output, where supported")
    parser.add_argument("--api-key", help="Overrides OPENROUTER_API_KEY and any .env file")
    parser.add_argument("--timeout", type=float, default=300.0,
                        help="Request timeout in seconds (default: 300)")
    parser.add_argument("--list-models", action="store_true",
                        help="List image models and their supported parameters, then exit")

    args = parser.parse_args(argv)

    try:
        if args.list_models:
            return list_models(args.timeout)

        if not args.prompt:
            parser.error("a prompt is required unless --list-models is given")

        api_key = find_api_key(args.api_key)
        payload = build_payload(args)

        action = "Editing" if args.input else "Generating"
        print(f"{action} with {args.model}")
        print(f"Prompt: {args.prompt}")
        if args.input:
            print(f"References: {', '.join(args.input)}")

        result = request_json(IMAGES_URL, api_key, payload, args.timeout)
        written = save_images(result, args.output)

        for path in written:
            print(f"Saved {path}")

        cost = (result.get("usage") or {}).get("cost")
        if cost is not None:
            print(f"Cost: ${cost}")
        return 0

    except ApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
