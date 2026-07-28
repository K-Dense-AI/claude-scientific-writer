#!/usr/bin/env python3
"""Build a hashed local-image inventory with final effective DPI."""

from __future__ import annotations

import argparse
import sys
import warnings
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from _common import CliError, emit_json, resolve_local_asset
from _manifest import ASSET_SUFFIXES, load_and_validate_manifest

MAX_IMAGE_PIXELS = 100_000_000


def _pillow_version() -> str:
    try:
        return version("Pillow")
    except PackageNotFoundError:
        return "unknown"


def _read_image(path: Path) -> dict[str, Any]:
    try:
        from PIL import Image
    except ImportError as exc:
        raise CliError(
            "Pillow is required for image inspection; install the exact pin with "
            "`uv pip install \"Pillow==12.3.0\"`"
        ) from exc
    Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                width, height = image.size
                image_format = image.format
                mode = image.mode
                frames = int(getattr(image, "n_frames", 1))
                image.load()
                has_icc_profile = bool(image.info.get("icc_profile"))
                has_alpha = "A" in image.getbands()
                exif_entry_count = len(image.getexif())
                text_keys = sorted(
                    str(key) for key in getattr(image, "text", {}).keys()
                )
                metadata_keys = sorted(str(key) for key in image.info)
    except (OSError, SyntaxError, Image.DecompressionBombError) as exc:
        raise CliError(f"cannot safely decode image {path}: {exc}") from exc
    except Image.DecompressionBombWarning as exc:
        raise CliError(f"image exceeds the pixel safety policy: {path}") from exc
    if image_format not in {"PNG", "JPEG"}:
        raise CliError(f"image format must be PNG or JPEG: {path}")
    if frames != 1:
        raise CliError(f"animated or multi-frame images are forbidden: {path}")
    if mode not in {"RGB", "RGBA", "L", "LA"}:
        raise CliError(
            f"image mode {mode!r} requires conversion and author review: {path}"
        )
    return {
        "format": image_format,
        "mode": mode,
        "width_px": width,
        "height_px": height,
        "frames": frames,
        "has_alpha": has_alpha,
        "has_icc_profile": has_icc_profile,
        "exif_entry_count": exif_entry_count,
        "embedded_text_keys": text_keys,
        "metadata_keys": metadata_keys,
    }


def build_inventory(
    manifest_path: Path,
    document: dict[str, Any],
    validation: dict[str, Any],
) -> dict[str, Any]:
    assets = {asset["id"]: asset for asset in document["assets"]}
    placements: dict[str, list[dict[str, Any]]] = {
        asset_id: [] for asset_id in assets
    }
    scale = float(validation["physical_output"]["print_scale"])
    minimum_dpi = float(document["quality"]["minimum_raster_dpi_final"])
    issues: list[dict[str, Any]] = []
    image_records: list[dict[str, Any]] = []

    for element in document["elements"]:
        if element["type"] == "image":
            placements[element["asset_id"]].append(element)

    for asset_id, asset in assets.items():
        path = resolve_local_asset(
            manifest_path,
            asset["path"],
            suffixes=ASSET_SUFFIXES,
        )
        metadata = _read_image(path)
        suspicious_metadata = sorted(
            {
                key
                for key in metadata["metadata_keys"]
                if any(
                    marker in key.lower()
                    for marker in (
                        "comment",
                        "description",
                        "exif",
                        "iptc",
                        "photoshop",
                        "software",
                        "xmp",
                        "xml",
                    )
                )
            }
            | set(metadata["embedded_text_keys"])
        )
        if metadata["exif_entry_count"] or suspicious_metadata:
            issues.append(
                {
                    "code": "HIDDEN_IMAGE_METADATA",
                    "asset_id": asset_id,
                    "message": (
                        "image contains EXIF or textual/application metadata; "
                        "flatten and strip it in an author-reviewed offline workflow, "
                        "then rehash and reapprove the asset"
                    ),
                    "exif_entry_count": metadata["exif_entry_count"],
                    "metadata_keys": suspicious_metadata,
                }
            )
        asset_placements: list[dict[str, Any]] = []
        for element in placements[asset_id]:
            box_width = float(element["width_in"])
            box_height = float(element["height_in"])
            fit_scale = min(
                box_width / int(metadata["width_px"]),
                box_height / int(metadata["height_px"]),
            )
            design_width = int(metadata["width_px"]) * fit_scale
            design_height = int(metadata["height_px"]) * fit_scale
            final_width = design_width * scale
            final_height = design_height * scale
            dpi_x = int(metadata["width_px"]) / final_width
            dpi_y = int(metadata["height_px"]) / final_height
            effective_dpi = min(dpi_x, dpi_y)
            placement = {
                "element_id": element["id"],
                "box_width_in_design": box_width,
                "box_height_in_design": box_height,
                "placed_width_in_design": design_width,
                "placed_height_in_design": design_height,
                "placed_width_in_final": final_width,
                "placed_height_in_final": final_height,
                "effective_dpi_x_final": dpi_x,
                "effective_dpi_y_final": dpi_y,
                "minimum_effective_dpi_final": effective_dpi,
                "pass": effective_dpi + 1e-6 >= minimum_dpi,
            }
            if not placement["pass"]:
                issues.append(
                    {
                        "code": "EFFECTIVE_DPI_TOO_LOW",
                        "asset_id": asset_id,
                        "element_id": element["id"],
                        "message": (
                            f"{effective_dpi:.1f} DPI is below the manifest's "
                            f"{minimum_dpi:.1f} DPI final-output requirement"
                        ),
                    }
                )
            if asset["role"] == "qr_code":
                placement["qr_manual_check"] = (
                    "Test this rendered QR code on the final proof with multiple "
                    "devices; the exact fallback URL is separate visible text."
                )
            asset_placements.append(placement)
        image_records.append(
            {
                "id": asset_id,
                "relative_path": asset["path"],
                "sha256": asset["sha256"],
                "source_id": asset["source_id"],
                "license": asset["license"],
                "provenance": asset["provenance"],
                "role": asset["role"],
                "alt_text": asset["alt_text"],
                "metadata": metadata,
                "placements": asset_placements,
            }
        )
    return {
        "schema_version": "1.0",
        "manifest": {
            "path": str(manifest_path),
            "content_sha256": validation["content_sha256"],
        },
        "pass": not issues,
        "pillow_version": _pillow_version(),
        "pixel_safety_limit": MAX_IMAGE_PIXELS,
        "minimum_raster_dpi_final": minimum_dpi,
        "minimum_raster_dpi_basis": {
            "kind": document["quality"]["raster_dpi_basis"],
            "source_id": document["quality"]["raster_dpi_source_id"],
        },
        "images": image_records,
        "issues": issues,
        "notice": (
            "Effective DPI is pixels divided by placed inches at final physical "
            "output, not file metadata DPI. Inspect the printer proof for resampling, "
            "compression, color conversion, and QR reliability."
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Fully decode approved local PNG/JPEG assets, report hashes, provenance, "
            "permission, and metadata, and calculate effective DPI at final physical "
            "placement. No network or image generation is used."
        )
    )
    parser.add_argument("manifest", help="approved local poster manifest JSON")
    parser.add_argument("--output", help="optional new JSON asset-manifest path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        manifest_path, document, validation = load_and_validate_manifest(
            args.manifest,
            verify_assets=True,
            require_approval=True,
        )
        report = build_inventory(manifest_path, document, validation)
        emit_json(report, output=args.output)
        return 0 if report["pass"] else 1
    except CliError as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
