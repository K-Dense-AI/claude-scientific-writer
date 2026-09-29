#!/usr/bin/env python3
"""
Generate and edit images through the OpenRouter Image API (POST /api/v1/images).

The Image API is model-agnostic: the same request shape reaches Gemini,
Seedream, Recraft, GPT-Image, Riverflow, and the rest of the image catalogue.
Responses carry base64 payloads in ``data[].b64_json`` alongside the concrete
``media_type``, so the output extension follows what the model actually
returned rather than an assumption.

Reference images (image-to-image and editing) go in ``input_references`` as
HTTP(S) URLs or base64 data URLs.

Parameter support is per-model and an unsupported parameter is rejected rather
than ignored, so every generation is preceded by a free metadata lookup that
validates the request locally before anything is billed (``--no-preflight``
skips it). Only the standard library is required.
"""

from __future__ import annotations

import argparse
import base64
import difflib
import json
import os
import sys
import time
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

# Suffixes that name the same format, so `-o out.jpeg` for an image/jpeg
# response is not reported as a mismatch.
SUFFIX_ALIASES = {
    ".jpg": {".jpg", ".jpeg"},
    ".jpeg": {".jpg", ".jpeg"},
    ".svg": {".svg", ".svgz"},
}

# Local file extension -> MIME type, for encoding reference images.
INPUT_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

# Request parameters that carry a per-model capability spec. `model`, `prompt`,
# and `input_references` are handled separately.
VALIDATED_PARAMETERS = (
    "n",
    "aspect_ratio",
    "resolution",
    "quality",
    "output_format",
    "background",
    "output_compression",
    "seed",
)

RETRY_STATUS = frozenset({429, 500, 502, 503, 504})

# Ceiling for an image the response asks us to download rather than inlining.
# A 4K PNG is a few tens of megabytes; anything past this is not an image we want.
MAX_DOWNLOAD_BYTES = 64 * 1024 * 1024

# Families outside this skill's documented set. They stay visible in
# --list-models and --model-info, which mirror the live catalogue, but are not
# offered as suggestions when a parameter is unsupported.
UNSUGGESTED_PREFIXES = ("black-forest-labs/",)


class ApiError(RuntimeError):
    """An error surfaced by the OpenRouter API or the transport beneath it."""


class RequestRejected(ApiError):
    """The request cannot succeed as built, caught before it is billed."""


def find_api_key(explicit: str | None = None) -> str:
    """Resolve the API key from --api-key, the environment, then any .env file.

    The .env scan walks up from the working directory and finally checks the
    script's own directory, so running from anywhere inside a project picks up
    the key at its root. Only the standard library is used: python-dotenv is a
    common omission, and a missing optional dependency should not read as a
    missing credential.
    """
    if explicit:
        return explicit

    from_env = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if from_env:
        return from_env

    cwd = Path.cwd()
    for directory in [cwd, *cwd.parents, Path(__file__).resolve().parent]:
        env_file = directory / ".env"
        if not env_file.is_file():
            continue
        try:
            content = env_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for raw in content.splitlines():
            line = raw.strip()
            if line.startswith("export "):
                line = line[len("export "):].strip()
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


def request_bytes(
    url: str,
    api_key: str | None,
    payload: dict | None,
    timeout: float,
    retries: int = 2,
    accept: str = "application/json",
    max_bytes: int | None = None,
) -> bytes:
    """POST (or GET when payload is None), retrying transient failures.

    Rate limits and 5xx responses are retried with exponential backoff, honouring
    Retry-After when the server sends it. A 4xx other than 429 is final: the
    request itself is wrong, so repeating it only wastes time.
    """
    headers = {"Accept": accept}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    attempt = 0
    while True:
        req = urllib.request.Request(url, data=data, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if max_bytes is None:
                    return resp.read()
                body = resp.read(max_bytes + 1)
                if len(body) > max_bytes:
                    raise ApiError(f"Refusing a response larger than {max_bytes} bytes: {url}")
                return body
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            retryable = exc.code in RETRY_STATUS
            if retryable and attempt < retries:
                delay = retry_delay(exc.headers.get("Retry-After"), attempt)
                print(
                    f"HTTP {exc.code} from OpenRouter; retrying in {delay:.0f}s "
                    f"({attempt + 1}/{retries})",
                    file=sys.stderr,
                )
                time.sleep(delay)
                attempt += 1
                continue
            raise ApiError(f"OpenRouter returned HTTP {exc.code}: {error_detail(exc.code, body)}") from exc
        except urllib.error.URLError as exc:
            if attempt < retries:
                delay = retry_delay(None, attempt)
                print(
                    f"Could not reach OpenRouter ({exc.reason}); retrying in {delay:.0f}s "
                    f"({attempt + 1}/{retries})",
                    file=sys.stderr,
                )
                time.sleep(delay)
                attempt += 1
                continue
            raise ApiError(f"Could not reach OpenRouter: {exc.reason}") from exc


def retry_delay(retry_after: str | None, attempt: int) -> float:
    """Seconds to wait before the next attempt: Retry-After, else backoff."""
    if retry_after:
        try:
            return max(1.0, min(60.0, float(retry_after)))
        except ValueError:
            pass
    return float(2 ** attempt)


def error_detail(status: int, body: str) -> str:
    """Extract the API's error message and add a hint for the usual causes."""
    detail = body
    try:
        parsed = json.loads(body)
        detail = parsed.get("error", {}).get("message") or body
    except (json.JSONDecodeError, AttributeError):
        pass

    hint = ""
    if status == 400:
        hint = (
            "\nParameter support and allowed values are per-model. Inspect this model:\n"
            "  python generate_image.py --model-info MODEL"
        )
    elif status in (401, 403):
        hint = (
            "\nCheck the key and its credit balance: https://openrouter.ai/keys\n"
            "A 403 can also be a content-policy refusal — rephrase the prompt."
        )
    return f"{detail}{hint}"


def request_json(url: str, api_key: str | None, payload: dict | None, timeout: float,
                 retries: int = 2) -> Any:
    """POST or GET and decode the JSON response."""
    raw = request_bytes(url, api_key, payload, timeout, retries)
    try:
        return json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ApiError(f"OpenRouter returned a non-JSON response: {exc}") from exc


def fetch_catalogue(timeout: float, retries: int = 2) -> dict[str, dict]:
    """Return the image catalogue keyed by model id. Needs no API key."""
    result = request_json(MODELS_URL, None, None, timeout, retries)
    return {m["id"]: m for m in result.get("data", []) if m.get("id")}


def describe_spec(spec: dict) -> str:
    """Render one capability spec as the values or range it permits."""
    if not isinstance(spec, dict):
        return "supported"
    if spec.get("type") == "enum":
        return ", ".join(str(v) for v in spec.get("values", []))
    if spec.get("type") == "range":
        return f"{spec.get('min', '?')}-{spec.get('max', '?')}"
    return "supported"


def spec_problem(name: str, value: Any, spec: dict) -> str | None:
    """Return a message if `value` violates `spec`, else None."""
    if not isinstance(spec, dict):
        return None
    kind = spec.get("type")
    if kind == "enum":
        allowed = [str(v) for v in spec.get("values", [])]
        if allowed and str(value) not in allowed:
            return f"{name}={value} is not allowed; this model accepts: {', '.join(allowed)}"
    elif kind == "range":
        low, high = spec.get("min"), spec.get("max")
        if isinstance(value, (int, float)):
            if low is not None and value < low:
                return f"{name}={value} is below this model's minimum of {low}"
            if high is not None and value > high:
                return f"{name}={value} exceeds this model's maximum of {high}"
    return None


def models_supporting(catalogue: dict[str, dict], parameter: str, value: Any = None) -> list[str]:
    """Model ids that accept `parameter`, and `value` for it when given."""
    matches = []
    for model_id, model in catalogue.items():
        spec = (model.get("supported_parameters") or {}).get(parameter)
        if spec is None:
            continue
        if value is not None and spec_problem(parameter, value, spec):
            continue
        matches.append(model_id)
    suggestable = [m for m in matches if not m.startswith(UNSUGGESTED_PREFIXES)]
    return sorted(suggestable or matches)


def preflight(payload: dict, catalogue: dict[str, dict]) -> None:
    """Validate the request against the model's advertised capabilities.

    Every problem found here would otherwise be an HTTP 400 after the round
    trip, or -- worse -- a silently wrong request. Errors are collected so one
    run reports all of them.
    """
    model_id = payload["model"]
    model = catalogue.get(model_id)
    if model is None:
        close = difflib.get_close_matches(model_id, sorted(catalogue), n=3, cutoff=0.4)
        suggestion = f" Did you mean: {', '.join(close)}?" if close else ""
        raise RequestRejected(
            f"'{model_id}' is not in the OpenRouter image catalogue.{suggestion}\n"
            "  python generate_image.py --list-models"
        )

    supported = model.get("supported_parameters") or {}
    problems: list[str] = []

    for name in VALIDATED_PARAMETERS:
        if name not in payload:
            continue
        spec = supported.get(name)
        if spec is None:
            others = models_supporting(catalogue, name, payload[name])
            alternatives = f"\n    Models that accept it: {', '.join(others[:6])}" if others else ""
            problems.append(
                f"{name} is not supported by {model_id}"
                f" (it accepts: {', '.join(sorted(supported)) or 'nothing but model and prompt'})"
                f"{alternatives}"
            )
            continue
        issue = spec_problem(name, payload[name], spec)
        if issue:
            problems.append(issue)

    references = payload.get("input_references") or []
    if references:
        spec = supported.get("input_references")
        if spec is None:
            problems.append(f"{model_id} does not accept reference images")
        else:
            maximum = spec.get("max", 0) if isinstance(spec, dict) else 0
            if maximum and len(references) > maximum:
                problems.append(
                    f"{len(references)} reference images given; {model_id} accepts at most {maximum}"
                )

    if problems:
        listed = "\n  - ".join(problems)
        raise RequestRejected(
            f"Request rejected before billing ({len(problems)} problem"
            f"{'s' if len(problems) > 1 else ''}):\n  - {listed}\n"
            f"Inspect the model: python generate_image.py --model-info {model_id}\n"
            "Bypass this check with --no-preflight."
        )


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


def redacted_payload(payload: dict) -> dict:
    """Copy the payload with base64 reference blobs shortened, for printing."""
    shown = dict(payload)
    references = shown.get("input_references")
    if references:
        trimmed = []
        for ref in references:
            url = ((ref.get("image_url") or {}).get("url")) or ""
            if url.startswith("data:") and len(url) > 80:
                head = url.split(",", 1)[0]
                url = f"{head},<{len(url)} chars of base64>"
            trimmed.append({"type": ref.get("type"), "image_url": {"url": url}})
        shown["input_references"] = trimmed
    return shown


def acceptable_suffixes(media_type: str) -> set[str]:
    """Suffixes that correctly name `media_type`, including spelling variants."""
    extension = EXTENSIONS.get(normalise_media_type(media_type), ".png")
    return SUFFIX_ALIASES.get(extension, {extension})


def normalise_media_type(media_type: str) -> str:
    """Strip parameters and case from a media type: 'IMAGE/PNG; x=1' -> 'image/png'."""
    return media_type.split(";", 1)[0].strip().lower()


def output_paths(requested: str | None, media_type: str, count: int) -> list[Path]:
    """Choose filenames for the returned images.

    The extension follows the model's media_type unless the caller named a file
    explicitly, in which case their choice is kept and a real mismatch -- not a
    mere spelling variant -- is reported.
    """
    extension = EXTENSIONS.get(normalise_media_type(media_type), ".png")

    if requested is None:
        stem, suffix = Path("generated_image"), extension
    else:
        given = Path(requested)
        stem, suffix = given.with_suffix(""), given.suffix or extension
        if given.suffix and given.suffix.lower() not in acceptable_suffixes(media_type):
            print(
                f"Note: model returned {media_type} but --output ends in "
                f"'{given.suffix}'; writing the returned bytes under that name.",
                file=sys.stderr,
            )

    if count == 1:
        return [stem.with_suffix(suffix)]
    return [stem.parent / f"{stem.name}_{i + 1}{suffix}" for i in range(count)]


def image_bytes(item: dict, timeout: float) -> bytes | None:
    """Decode one response entry, downloading it if it arrived as a URL."""
    payload = item.get("b64_json")
    if payload:
        if payload.startswith("data:") and "," in payload:
            payload = payload.split(",", 1)[1]
        return base64.b64decode(payload)

    url = item.get("url")
    if not url:
        return None

    # The documented response inlines base64, so this branch only runs if a
    # provider hands back a link instead. The URL comes from the response rather
    # than from the caller, so require HTTPS and cap what we are willing to read.
    if not url.startswith("https://"):
        raise ApiError(f"Refusing to fetch a non-HTTPS image URL from the response: {url}")
    return request_bytes(
        url, None, None, timeout, retries=1, accept="image/*", max_bytes=MAX_DOWNLOAD_BYTES
    )


def save_images(result: dict, requested_output: str | None, timeout: float = 60.0) -> list[Path]:
    """Decode data[] into files and return the paths written."""
    items = result.get("data")
    if not items:
        raise ApiError(
            "Response contained no images.\n"
            f"Raw response: {json.dumps(result, indent=2)[:800]}"
        )

    decoded: list[tuple[dict, bytes]] = []
    for item in items:
        content = image_bytes(item, timeout)
        if content is None:
            print(f"Skipping an entry with no image data: {list(item)}", file=sys.stderr)
            continue
        decoded.append((item, content))

    if not decoded:
        raise ApiError("Response carried image entries but none contained data.")

    # Numbering is assigned after skipping empty entries so the written files
    # are always _1.._n with no gaps.
    first_media = decoded[0][0].get("media_type", "image/png")
    paths = output_paths(requested_output, first_media, len(decoded))
    written: list[Path] = []

    for (_, content), path in zip(decoded, paths):
        if str(path.parent) not in ("", "."):
            path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        written.append(path)

    return written


def format_cost(cost: Any) -> str:
    """Render a USD amount in decimal, never scientific notation."""
    if not isinstance(cost, (int, float)):
        return str(cost)
    return f"{cost:.8f}".rstrip("0").rstrip(".") or "0"


def format_pricing(pricing: list[dict] | None) -> list[str]:
    """Render an endpoint's pricing entries as readable lines."""
    if not pricing:
        return ["    pricing: not published for this model"]
    lines = []
    for entry in pricing:
        variant = f" ({entry['variant']})" if entry.get("variant") else ""
        lines.append(
            f"    pricing: ${format_cost(entry.get('cost_usd'))} per {entry.get('unit', '?')}"
            f" of {entry.get('billable', '?')}{variant}"
        )
    return lines


def cost_lines(usage: dict) -> list[str]:
    """Report what the request cost, including the BYOK case.

    On a bring-your-own-key account OpenRouter reports ``usage.cost`` as 0
    because the upstream provider bills directly; the real figure is in
    ``cost_details.upstream_inference_cost``. Printing only ``cost`` there would
    claim a paid generation was free.
    """
    cost = usage.get("cost")
    upstream = (usage.get("cost_details") or {}).get("upstream_inference_cost")

    lines = []
    if cost:
        lines.append(f"Cost: ${format_cost(cost)}")
    elif upstream:
        lines.append(f"Cost: ${format_cost(upstream)} billed upstream (BYOK key)")
    elif cost is not None:
        lines.append("Cost: $0 reported")

    image_tokens = (usage.get("completion_tokens_details") or {}).get("image_tokens")
    if image_tokens:
        lines.append(f"Image tokens: {image_tokens}")
    return lines


def print_model(model: dict) -> None:
    """Print one catalogue entry with its per-parameter allowed values."""
    params = model.get("supported_parameters") or {}
    n_spec = params.get("n") or {}
    refs = params.get("input_references") or {}
    print(model.get("id", "?"))
    per_request = f"up to {n_spec.get('max', 1)}" if n_spec else "1 (n not accepted)"
    print(
        f"    images/request: {per_request}"
        f" | reference images: up to {refs.get('max', 0)}"
        f" | streaming: {'yes' if model.get('supports_streaming') else 'no'}"
    )
    for name in sorted(params):
        if name in ("n", "input_references"):
            continue
        print(f"    {name}: {describe_spec(params[name])}")


def list_models(timeout: float, substring: str = "") -> int:
    """Print the image catalogue with each model's parameters and their values."""
    catalogue = fetch_catalogue(timeout)
    if not catalogue:
        print("No models returned.", file=sys.stderr)
        return 1

    selected = [m for mid, m in sorted(catalogue.items()) if substring.lower() in mid.lower()]
    if not selected:
        print(f"No image model id contains '{substring}'.", file=sys.stderr)
        return 1

    scope = f" matching '{substring}'" if substring else ""
    print(f"{len(selected)} image models available{scope}\n")
    for model in selected:
        print_model(model)
    return 0


def model_info(model_id: str, timeout: float) -> int:
    """Print one model's allowed values, passthrough parameters, and pricing."""
    catalogue = fetch_catalogue(timeout)
    if model_id not in catalogue:
        close = difflib.get_close_matches(model_id, sorted(catalogue), n=3, cutoff=0.4)
        hint = f" Did you mean: {', '.join(close)}?" if close else ""
        print(f"'{model_id}' is not in the image catalogue.{hint}", file=sys.stderr)
        return 1

    print_model(catalogue[model_id])
    result = request_json(f"{MODELS_URL}/{model_id}/endpoints", None, None, timeout)
    for endpoint in result.get("endpoints", []):
        print(f"    provider: {endpoint.get('provider_name', '?')}")
        for line in format_pricing(endpoint.get("pricing")):
            print(line)
        passthrough = endpoint.get("allowed_passthrough_parameters") or []
        if passthrough:
            print(f"    passthrough (direct API only): {', '.join(passthrough)}")
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
  python generate_image.py "A cat in space" -m google/gemini-3-pro-image --aspect-ratio 16:9

  # Edit an existing image
  python generate_image.py "Make the sky purple" -i photo.jpg -o edited.png

  # Composite from several references (model-dependent limit)
  python generate_image.py "Blend these styles" -i a.png -i b.png -o blended.png

  # Vector output
  python generate_image.py "Minimal fox logo" -m recraft/recraft-v4-vector -o logo.svg

  # Validate the request and print the payload without generating or billing
  python generate_image.py "A cat astronaut" --resolution 4K --dry-run

  # Inspect the catalogue, or one model's allowed values and pricing
  python generate_image.py --list-models gemini
  python generate_image.py --model-info openai/gpt-image-1
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
    parser.add_argument("--aspect-ratio", help="e.g. 1:1, 16:9, 9:16, 4:3 (enum differs per model)")
    parser.add_argument("--resolution", help="Tier: 512, 1K, 2K, 4K (support differs per model)")
    parser.add_argument("--quality", choices=["auto", "low", "medium", "high"])
    parser.add_argument("--output-format", choices=["png", "jpeg", "webp"])
    parser.add_argument("--background", choices=["auto", "transparent", "opaque"])
    parser.add_argument("--output-compression", type=int, metavar="0-100",
                        help="Compression for webp/jpeg output")
    parser.add_argument("--seed", type=int, help="Seed for deterministic output, where supported")
    parser.add_argument("--api-key", help="Overrides OPENROUTER_API_KEY and any .env file")
    parser.add_argument("--timeout", type=float, default=300.0,
                        help="Request timeout in seconds (default: 300)")
    parser.add_argument("--retries", type=int, default=2, metavar="N",
                        help="Retries for rate limits and 5xx responses (default: 2)")
    parser.add_argument("--no-preflight", action="store_true",
                        help="Skip the free capability check before the billed request")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate and print the request, then exit without generating")
    parser.add_argument("--list-models", nargs="?", const="", metavar="SUBSTRING",
                        help="List image models and their allowed values, then exit")
    parser.add_argument("--model-info", metavar="MODEL",
                        help="Print one model's allowed values and pricing, then exit")

    args = parser.parse_args(argv)

    try:
        if args.list_models is not None:
            return list_models(args.timeout, args.list_models)

        if args.model_info:
            return model_info(args.model_info, args.timeout)

        if not args.prompt:
            parser.error("a prompt is required unless --list-models or --model-info is given")

        if args.output_compression is not None and not 0 <= args.output_compression <= 100:
            parser.error("--output-compression must be between 0 and 100")
        if args.n is not None and args.n < 1:
            parser.error("--n must be at least 1")

        payload = build_payload(args)

        if not args.no_preflight:
            try:
                catalogue = fetch_catalogue(args.timeout, args.retries)
            except ApiError as exc:
                # Fail open: an unreachable metadata endpoint should not block a
                # request the API itself may well accept.
                print(f"Skipping the capability check ({exc}).", file=sys.stderr)
            else:
                preflight(payload, catalogue)

        if args.dry_run:
            print(f"POST {IMAGES_URL}")
            print(json.dumps(redacted_payload(payload), indent=2))
            print("Dry run: nothing generated, nothing billed.")
            return 0

        api_key = find_api_key(args.api_key)

        action = "Editing" if args.input else "Generating"
        print(f"{action} with {args.model}")
        print(f"Prompt: {args.prompt}")
        if args.input:
            print(f"References: {', '.join(args.input)}")

        result = request_json(IMAGES_URL, api_key, payload, args.timeout, args.retries)
        written = save_images(result, args.output, args.timeout)

        for path in written:
            print(f"Saved {path}")

        for line in cost_lines(result.get("usage") or {}):
            print(line)
        print("Open the image and check it before using it.")
        return 0

    except ApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
