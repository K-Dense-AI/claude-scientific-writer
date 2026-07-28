#!/usr/bin/env python3
"""Bounded, non-executing PPTX package inspection and layout analysis."""

from __future__ import annotations

import posixpath
import re
import shutil
import stat
import struct
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

from _common import (
    EMU_PER_INCH,
    MAX_INPUT_BYTES,
    CliError,
    checked_input_file,
)

REPORT_SCHEMA_VERSION = "1.0"
MAX_MEMBERS = 4_096
MAX_TOTAL_UNCOMPRESSED = 1024 * 1024 * 1024
MAX_MEMBER_UNCOMPRESSED = 128 * 1024 * 1024
MAX_XML_BYTES = 8 * 1024 * 1024
MAX_COMPRESSION_RATIO = 100.0
MAX_CENTRAL_DIRECTORY_BYTES = 64 * 1024 * 1024
DETERMINISTIC_ZIP_DATETIME = (1980, 1, 1, 0, 0, 0)

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

STANDARD_PRESENTATION_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument.presentationml."
    "presentation.main+xml"
)
REQUIRED_PARTS = {
    "[Content_Types].xml",
    "_rels/.rels",
    "ppt/_rels/presentation.xml.rels",
    "ppt/presentation.xml",
}
FORBIDDEN_PREFIXES = (
    "_xmlsignatures/",
    "customxml/",
    "customui/",
    "ppt/activex/",
    "ppt/comments/",
    "ppt/ctrlprops/",
    "ppt/embeddings/",
    "ppt/externallinks/",
    "ppt/fonts/",
    "ppt/model3d/",
    "ppt/notesmasters/",
    "ppt/notesslides/",
    "ppt/persons/",
    "ppt/vba/",
    "ppt/webextensions/",
    "webextensions/",
)
FORBIDDEN_RELATIONSHIP_MARKERS = (
    "activex",
    "attachedtemplate",
    "control",
    "customui",
    "externallink",
    "relationships/hyperlink",
    "notesmaster",
    "notesslide",
    "oleobject",
    "person",
    "relationships/package",
    "relationships/audio",
    "relationships/media",
    "relationships/video",
    "webextension",
    "vbaproject",
)
FORBIDDEN_CONTENT_TYPE_MARKERS = (
    "activex",
    "macroenabled",
    "oleobject",
    "vba",
    "vnd.ms-package",
)
FORBIDDEN_BINARY_SUFFIXES = {
    ".7z",
    ".app",
    ".applescript",
    ".bat",
    ".bin",
    ".class",
    ".cmd",
    ".com",
    ".doc",
    ".docm",
    ".docx",
    ".dll",
    ".dylib",
    ".exe",
    ".hta",
    ".htm",
    ".html",
    ".jar",
    ".js",
    ".lnk",
    ".msi",
    ".pdf",
    ".ppt",
    ".pptm",
    ".pptx",
    ".ps1",
    ".py",
    ".rar",
    ".rb",
    ".sh",
    ".so",
    ".svg",
    ".vbs",
    ".xls",
    ".xlsm",
    ".xlsx",
    ".zip",
}
ALLOWED_CONTENT_TYPES = {
    "application/vnd.openxmlformats-package.core-properties+xml",
    "application/vnd.openxmlformats-package.relationships+xml",
    "application/vnd.openxmlformats-officedocument.extended-properties+xml",
    "application/vnd.openxmlformats-officedocument.presentationml.presProps+xml",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml",
    "application/vnd.openxmlformats-officedocument.presentationml.slide+xml",
    "application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml",
    "application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml",
    "application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml",
    "application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml",
    "application/vnd.openxmlformats-officedocument.theme+xml",
    "application/xml",
    "image/jpeg",
    "image/png",
}
ALLOWED_PART_PATTERNS = tuple(
    re.compile(pattern)
    for pattern in (
        r"\[Content_Types\]\.xml",
        r"_rels/\.rels",
        r"docProps/(?:app|core)\.xml",
        r"docProps/thumbnail\.jpeg",
        r"ppt/(?:presentation|presProps|tableStyles|viewProps)\.xml",
        r"ppt/_rels/presentation\.xml\.rels",
        r"ppt/theme/theme[1-9][0-9]*\.xml",
        r"ppt/slideMasters/slideMaster[1-9][0-9]*\.xml",
        r"ppt/slideMasters/_rels/slideMaster[1-9][0-9]*\.xml\.rels",
        r"ppt/slideLayouts/slideLayout[1-9][0-9]*\.xml",
        r"ppt/slideLayouts/_rels/slideLayout[1-9][0-9]*\.xml\.rels",
        r"ppt/slides/slide[1-9][0-9]*\.xml",
        r"ppt/slides/_rels/slide[1-9][0-9]*\.xml\.rels",
        r"ppt/media/image[1-9][0-9]*\.(?:jpeg|jpg|png)",
        r"ppt/printerSettings/printerSettings[1-9][0-9]*\.bin",
    )
)


def _finding(code: str, message: str, *, location: str | None = None) -> dict[str, Any]:
    record: dict[str, Any] = {"code": code, "message": message}
    if location is not None:
        record["location"] = location
    return record


def _allowed_generated_part(name: str) -> bool:
    """Return whether a part belongs to the strict generated-poster profile."""
    return any(pattern.fullmatch(name) for pattern in ALLOWED_PART_PATTERNS)


def _preflight_zip_directory(path: Path) -> list[dict[str, Any]]:
    """Bound the central directory before ZipFile materializes all members."""
    findings: list[dict[str, Any]] = []
    file_size = path.stat().st_size
    if file_size < 22:
        return [_finding("NOT_ZIP", "file is too short to contain a ZIP directory")]
    with path.open("rb") as handle:
        if handle.read(4) != b"PK\x03\x04":
            return [_finding("NOT_ZIP", "file does not begin with a ZIP local header")]
        tail_size = min(file_size, 65_557)
        handle.seek(file_size - tail_size)
        tail = handle.read(tail_size)
    marker = b"PK\x05\x06"
    index = tail.rfind(marker)
    if index < 0 or index + 22 > len(tail):
        return [_finding("ZIP_DIRECTORY_INVALID", "end-of-central-directory not found")]
    try:
        (
            signature,
            disk_number,
            central_disk,
            entries_on_disk,
            total_entries,
            central_size,
            central_offset,
            comment_length,
        ) = struct.unpack_from("<4s4H2LH", tail, index)
    except struct.error as exc:
        return [_finding("ZIP_DIRECTORY_INVALID", str(exc))]
    if signature != marker:
        findings.append(
            _finding("ZIP_DIRECTORY_INVALID", "invalid central-directory signature")
        )
    eocd_offset = file_size - tail_size + index
    if eocd_offset + 22 + comment_length != file_size:
        findings.append(
            _finding(
                "ZIP_DIRECTORY_INVALID",
                "central-directory comment length or trailing bytes are invalid",
            )
        )
    if (
        disk_number != 0
        or central_disk != 0
        or entries_on_disk != total_entries
    ):
        findings.append(
            _finding("ZIP_MULTIDISK", "multi-disk ZIP packages are forbidden")
        )
    if (
        total_entries == 0xFFFF
        or central_size == 0xFFFFFFFF
        or central_offset == 0xFFFFFFFF
    ):
        findings.append(
            _finding(
                "ZIP64_DIRECTORY",
                "ZIP64 central directories are outside the strict PPTX profile",
            )
        )
        return findings
    if total_entries > MAX_MEMBERS:
        findings.append(
            _finding(
                "ZIP_MEMBER_LIMIT",
                f"package declares {total_entries} members; limit is {MAX_MEMBERS}",
            )
        )
    if central_size > MAX_CENTRAL_DIRECTORY_BYTES:
        findings.append(
            _finding(
                "ZIP_DIRECTORY_SIZE",
                f"central directory is {central_size} bytes; limit is "
                f"{MAX_CENTRAL_DIRECTORY_BYTES}",
            )
        )
    if central_offset + central_size != eocd_offset:
        findings.append(
            _finding(
                "ZIP_DIRECTORY_INVALID",
                "central-directory offset/size does not end at the ZIP footer",
            )
        )
    return findings


def _unsafe_xml(text: str) -> bool:
    upper = text.upper()
    return "<!DOCTYPE" in upper or "<!ENTITY" in upper


def _parse_xml(raw: bytes, *, location: str) -> ET.Element:
    if len(raw) > MAX_XML_BYTES:
        raise CliError(
            f"XML part {location} is {len(raw)} bytes; limit is {MAX_XML_BYTES}"
        )
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise CliError(
            f"XML part {location} must be UTF-8 in the strict generated profile"
        ) from exc
    if "\x00" in text:
        raise CliError(f"NUL is forbidden in XML part {location}")
    if _unsafe_xml(text):
        raise CliError(f"DTD or entity declaration is forbidden in {location}")
    try:
        return ET.fromstring(text)
    except ET.ParseError as exc:
        raise CliError(f"malformed XML in {location}: {exc}") from exc


def _relationship_source_directory(rels_name: str) -> str:
    if rels_name == "_rels/.rels":
        return ""
    marker = "/_rels/"
    if marker not in rels_name or not rels_name.endswith(".rels"):
        raise CliError(f"invalid relationship part name: {rels_name}")
    prefix, leaf = rels_name.split(marker, 1)
    source_leaf = leaf[: -len(".rels")]
    return posixpath.dirname(f"{prefix}/{source_leaf}")


def _resolve_internal_target(rels_name: str, target: str) -> str:
    if not target or "\x00" in target or "\\" in target:
        raise CliError(f"unsafe internal relationship target in {rels_name}: {target!r}")
    if target.startswith("/") or "%" in target or "?" in target or "#" in target:
        raise CliError(
            f"unsupported internal relationship target in {rels_name}: {target!r}"
        )
    base = _relationship_source_directory(rels_name)
    normalized = posixpath.normpath(posixpath.join(base, target))
    if normalized in {"", ".", ".."} or normalized.startswith("../"):
        raise CliError(
            f"relationship target escapes the package in {rels_name}: {target!r}"
        )
    return normalized


def _preflight_members(
    archive: zipfile.ZipFile,
) -> tuple[list[zipfile.ZipInfo], list[dict[str, Any]], set[str], int]:
    findings: list[dict[str, Any]] = []
    members = archive.infolist()
    if len(members) > MAX_MEMBERS:
        return (
            members,
            [
                _finding(
                    "ZIP_MEMBER_LIMIT",
                    f"package has {len(members)} members; limit is {MAX_MEMBERS}",
                )
            ],
            set(),
            0,
        )
    names: set[str] = set()
    casefold_names: set[str] = set()
    total_uncompressed = 0

    for info in members:
        name = info.filename
        location = name or "<empty>"
        if (
            not name
            or "\x00" in name
            or "\\" in name
            or ":" in name
            or "%" in name
        ):
            findings.append(
                _finding(
                    "ZIP_UNSAFE_NAME",
                    "empty, NUL, backslash, colon, or percent-encoded member name",
                    location=location,
                )
            )
            continue
        pure = PurePosixPath(name)
        if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
            findings.append(
                _finding("ZIP_TRAVERSAL", "absolute or traversing member path", location=name)
            )
        if name in names or name.casefold() in casefold_names:
            findings.append(
                _finding("ZIP_DUPLICATE_NAME", "duplicate or case-colliding member", location=name)
            )
        names.add(name)
        casefold_names.add(name.casefold())
        unix_mode = (info.external_attr >> 16) & 0o170000
        if unix_mode == stat.S_IFLNK:
            findings.append(
                _finding("ZIP_SYMLINK", "symbolic-link member is forbidden", location=name)
            )
        if info.flag_bits & 0x1:
            findings.append(
                _finding("ZIP_ENCRYPTED", "encrypted member is forbidden", location=name)
            )
        if info.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}:
            findings.append(
                _finding(
                    "ZIP_COMPRESSION_METHOD",
                    f"unsupported compression method {info.compress_type}",
                    location=name,
                )
            )
        total_uncompressed += info.file_size
        if total_uncompressed > MAX_TOTAL_UNCOMPRESSED:
            findings.append(
                _finding(
                    "ZIP_TOTAL_SIZE",
                    f"package expands beyond {MAX_TOTAL_UNCOMPRESSED} bytes",
                    location=name,
                )
            )
            return members, findings, names, total_uncompressed
        if info.file_size > MAX_MEMBER_UNCOMPRESSED:
            findings.append(
                _finding(
                    "ZIP_MEMBER_SIZE",
                    f"member expands to {info.file_size} bytes; "
                    f"limit is {MAX_MEMBER_UNCOMPRESSED}",
                    location=name,
                )
            )
            return members, findings, names, total_uncompressed
        if info.file_size:
            if info.compress_size == 0:
                ratio = float("inf")
            else:
                ratio = info.file_size / info.compress_size
            if ratio > MAX_COMPRESSION_RATIO:
                findings.append(
                    _finding(
                        "ZIP_COMPRESSION_RATIO",
                        f"compression ratio {ratio:.1f}:1 exceeds "
                        f"{MAX_COMPRESSION_RATIO:.1f}:1",
                        location=name,
                    )
                )
                return members, findings, names, total_uncompressed
        lowered = name.lower()
        if lowered.startswith(FORBIDDEN_PREFIXES):
            findings.append(
                _finding(
                    "FORBIDDEN_PACKAGE_PART",
                    "active, external, or embedded package area is forbidden",
                    location=name,
                )
            )
        if lowered == "docprops/custom.xml":
            findings.append(
                _finding(
                    "FORBIDDEN_CUSTOM_PROPERTIES",
                    "custom document properties are outside the strict poster profile",
                    location=name,
                )
            )
        if PurePosixPath(lowered).suffix in FORBIDDEN_BINARY_SUFFIXES:
            findings.append(
                _finding(
                    "FORBIDDEN_BINARY_PART",
                    "binary or executable package part is forbidden",
                    location=name,
                )
            )
        if not _allowed_generated_part(name):
            findings.append(
                _finding(
                    "UNKNOWN_PACKAGE_PART",
                    "part is outside the strict one-slide generated-poster profile",
                    location=name,
                )
            )
        if lowered.startswith("ppt/media/") and PurePosixPath(lowered).suffix not in {
            ".jpeg",
            ".jpg",
            ".png",
        }:
            findings.append(
                _finding(
                    "FORBIDDEN_MEDIA_PART",
                    "non-image media part is forbidden",
                    location=name,
                )
            )

    missing = sorted(REQUIRED_PARTS - names)
    if missing:
        findings.append(
            _finding(
                "MISSING_REQUIRED_PART",
                f"missing required package part(s): {', '.join(missing)}",
            )
        )
    return members, findings, names, total_uncompressed


def _inspect_content_types(
    archive: zipfile.ZipFile,
    names: set[str],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if "[Content_Types].xml" not in names:
        return findings
    try:
        root = _parse_xml(
            archive.read("[Content_Types].xml"),
            location="[Content_Types].xml",
        )
    except (KeyError, OSError, RuntimeError, zipfile.BadZipFile, CliError) as exc:
        return [
            _finding(
                "CONTENT_TYPES_INVALID",
                str(exc),
                location="[Content_Types].xml",
            )
        ]
    if root.tag != f"{{{CT_NS}}}Types":
        findings.append(
            _finding(
                "CONTENT_TYPES_INVALID",
                "root element is not the OPC content-types element",
                location="[Content_Types].xml",
            )
        )
        return findings
    main_type = None
    seen_defaults: set[str] = set()
    seen_overrides: set[str] = set()
    for node in root:
        content_type = node.attrib.get("ContentType", "")
        lowered = content_type.lower()
        if node.tag not in {f"{{{CT_NS}}}Default", f"{{{CT_NS}}}Override"}:
            findings.append(
                _finding(
                    "CONTENT_TYPES_INVALID",
                    "unexpected element in content-types part",
                    location="[Content_Types].xml",
                )
            )
            continue
        if content_type not in ALLOWED_CONTENT_TYPES:
            findings.append(
                _finding(
                    "UNEXPECTED_CONTENT_TYPE",
                    f"content type is outside the strict profile: {content_type!r}",
                    location="[Content_Types].xml",
                )
            )
        if any(marker in lowered for marker in FORBIDDEN_CONTENT_TYPE_MARKERS):
            findings.append(
                _finding(
                    "FORBIDDEN_CONTENT_TYPE",
                    f"forbidden content type {content_type!r}",
                    location="[Content_Types].xml",
                )
            )
        if node.tag == f"{{{CT_NS}}}Default":
            extension = node.attrib.get("Extension", "")
            if (
                not extension
                or extension in seen_defaults
                or "/" in extension
                or "\\" in extension
                or "." in extension
            ):
                findings.append(
                    _finding(
                        "CONTENT_TYPES_INVALID",
                        f"invalid or duplicate default extension {extension!r}",
                        location="[Content_Types].xml",
                    )
                )
            seen_defaults.add(extension)
            continue
        part_name = node.attrib.get("PartName", "")
        normalized_part = part_name[1:] if part_name.startswith("/") else ""
        if (
            not normalized_part
            or normalized_part in seen_overrides
            or normalized_part not in names
        ):
            findings.append(
                _finding(
                    "CONTENT_TYPES_INVALID",
                    f"invalid, duplicate, or missing override part {part_name!r}",
                    location="[Content_Types].xml",
                )
            )
        seen_overrides.add(normalized_part)
        if (
            node.tag == f"{{{CT_NS}}}Override"
            and part_name == "/ppt/presentation.xml"
        ):
            main_type = content_type
    if main_type != STANDARD_PRESENTATION_CONTENT_TYPE:
        findings.append(
            _finding(
                "PRESENTATION_CONTENT_TYPE",
                "ppt/presentation.xml is not a standard macro-free PPTX main part",
                location="[Content_Types].xml",
            )
        )
    return findings


def _inspect_relationships(
    archive: zipfile.ZipFile,
    names: set[str],
) -> tuple[list[dict[str, Any]], int]:
    findings: list[dict[str, Any]] = []
    relationship_count = 0
    for rels_name in sorted(name for name in names if name.endswith(".rels")):
        try:
            root = _parse_xml(archive.read(rels_name), location=rels_name)
        except (KeyError, OSError, RuntimeError, zipfile.BadZipFile, CliError) as exc:
            findings.append(
                _finding("RELATIONSHIPS_INVALID", str(exc), location=rels_name)
            )
            continue
        if root.tag != f"{{{PKG_REL_NS}}}Relationships":
            findings.append(
                _finding(
                    "RELATIONSHIPS_INVALID",
                    "root element is not the OPC relationships element",
                    location=rels_name,
                )
            )
            continue
        seen_ids: set[str] = set()
        for relationship in root:
            if relationship.tag != f"{{{PKG_REL_NS}}}Relationship":
                findings.append(
                    _finding(
                        "RELATIONSHIPS_INVALID",
                        "unexpected element in relationship part",
                        location=rels_name,
                    )
                )
                continue
            relationship_count += 1
            relationship_id = relationship.attrib.get("Id", "")
            relationship_type = relationship.attrib.get("Type", "")
            target = relationship.attrib.get("Target", "")
            target_mode = relationship.attrib.get("TargetMode", "")
            if not relationship_id or relationship_id in seen_ids:
                findings.append(
                    _finding(
                        "RELATIONSHIPS_INVALID",
                        f"missing or duplicate relationship Id {relationship_id!r}",
                        location=rels_name,
                    )
                )
            seen_ids.add(relationship_id)
            if not relationship_type:
                findings.append(
                    _finding(
                        "RELATIONSHIPS_INVALID",
                        "relationship Type is required",
                        location=rels_name,
                    )
                )
            if target_mode == "External":
                code = (
                    "REMOTE_LINKED_IMAGE"
                    if relationship_type.lower().endswith("/image")
                    else "EXTERNAL_RELATIONSHIP"
                )
                findings.append(
                    _finding(
                        code,
                        f"external target is forbidden: {target!r}",
                        location=rels_name,
                    )
                )
                continue
            if target_mode not in {"", "Internal"}:
                findings.append(
                    _finding(
                        "RELATIONSHIP_TARGET_MODE_INVALID",
                        f"unsupported TargetMode {target_mode!r}",
                        location=rels_name,
                    )
                )
                continue
            type_lower = relationship_type.lower()
            if any(marker in type_lower for marker in FORBIDDEN_RELATIONSHIP_MARKERS):
                findings.append(
                    _finding(
                        "FORBIDDEN_RELATIONSHIP_TYPE",
                        f"forbidden relationship type {relationship_type!r}",
                        location=rels_name,
                    )
                )
            try:
                resolved = _resolve_internal_target(rels_name, target)
            except CliError as exc:
                findings.append(
                    _finding(
                        "RELATIONSHIP_TARGET_INVALID",
                        str(exc),
                        location=rels_name,
                    )
                )
                continue
            if resolved not in names:
                findings.append(
                    _finding(
                        "RELATIONSHIP_TARGET_MISSING",
                        f"internal target does not exist: {resolved!r}",
                        location=rels_name,
                    )
                )
    return findings, relationship_count


def _inspect_all_xml_parts(
    archive: zipfile.ZipFile,
    names: set[str],
) -> list[dict[str, Any]]:
    """Reject malformed or entity-bearing XML anywhere in the strict package."""
    findings: list[dict[str, Any]] = []
    for part_name in sorted(name for name in names if name.endswith(".xml")):
        try:
            _parse_xml(archive.read(part_name), location=part_name)
        except (KeyError, OSError, RuntimeError, zipfile.BadZipFile, CliError) as exc:
            findings.append(
                _finding("XML_PART_INVALID", str(exc), location=part_name)
            )
    return findings


def _inspect_one_slide_profile(
    archive: zipfile.ZipFile,
    names: set[str],
) -> list[dict[str, Any]]:
    """Require exactly one slide and one matching presentation relationship."""
    findings: list[dict[str, Any]] = []
    slide_names = sorted(
        name
        for name in names
        if name.startswith("ppt/slides/slide")
        and name.endswith(".xml")
        and "/_rels/" not in name
    )
    if len(slide_names) != 1:
        return [
            _finding(
                "SLIDE_COUNT",
                f"strict poster profile requires exactly one slide; found {len(slide_names)}",
                location="ppt/presentation.xml",
            )
        ]
    try:
        presentation = _parse_xml(
            archive.read("ppt/presentation.xml"),
            location="ppt/presentation.xml",
        )
        presentation_rels = _parse_xml(
            archive.read("ppt/_rels/presentation.xml.rels"),
            location="ppt/_rels/presentation.xml.rels",
        )
    except (KeyError, OSError, RuntimeError, zipfile.BadZipFile, CliError) as exc:
        return [
            _finding(
                "PRESENTATION_PROFILE_INVALID",
                str(exc),
                location="ppt/presentation.xml",
            )
        ]
    slide_ids = presentation.findall(
        f"./{{{P_NS}}}sldIdLst/{{{P_NS}}}sldId"
    )
    if len(slide_ids) != 1:
        findings.append(
            _finding(
                "SLIDE_ID_COUNT",
                f"presentation must declare exactly one slide Id; found {len(slide_ids)}",
                location="ppt/presentation.xml",
            )
        )
        return findings
    relationship_id = slide_ids[0].attrib.get(f"{{{R_NS}}}id", "")
    targets: dict[str, str] = {}
    for relationship in presentation_rels:
        if relationship.attrib.get("TargetMode", "") == "External":
            continue
        try:
            target = _resolve_internal_target(
                "ppt/_rels/presentation.xml.rels",
                relationship.attrib.get("Target", ""),
            )
        except CliError:
            continue
        targets[relationship.attrib.get("Id", "")] = target
    if targets.get(relationship_id) != slide_names[0]:
        findings.append(
            _finding(
                "SLIDE_RELATIONSHIP",
                "the declared slide Id does not resolve to the sole slide part",
                location="ppt/presentation.xml",
            )
        )
    return findings


def _inspect_image_payloads(
    archive: zipfile.ZipFile,
    names: set[str],
) -> list[dict[str, Any]]:
    """Check strict-profile image signatures and stream through CRC validation."""
    findings: list[dict[str, Any]] = []
    image_names = sorted(
        name
        for name in names
        if name.startswith("ppt/media/") or name == "docProps/thumbnail.jpeg"
    )
    for part_name in image_names:
        try:
            with archive.open(part_name, "r") as handle:
                prefix = handle.read(16)
                while handle.read(1024 * 1024):
                    pass
        except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
            findings.append(
                _finding("IMAGE_PART_INVALID", str(exc), location=part_name)
            )
            continue
        suffix = PurePosixPath(part_name).suffix.lower()
        signature_ok = (
            prefix.startswith(b"\x89PNG\r\n\x1a\n")
            if suffix == ".png"
            else prefix.startswith(b"\xff\xd8\xff")
        )
        if not signature_ok:
            findings.append(
                _finding(
                    "IMAGE_SIGNATURE",
                    "image bytes do not match the declared PNG/JPEG suffix",
                    location=part_name,
                )
            )
    return findings


def _inspect_slide_accessibility(
    archive: zipfile.ZipFile,
    names: set[str],
) -> dict[str, Any]:
    picture_count = 0
    pictures_with_alt_text = 0
    missing_alt: list[dict[str, str]] = []
    slide_title_count = 0
    text_run_count = 0
    text_runs_with_language = 0
    missing_language: list[dict[str, str]] = []
    slide_names = sorted(
        name
        for name in names
        if name.startswith("ppt/slides/slide")
        and name.endswith(".xml")
        and "/_rels/" not in name
    )
    for slide_name in slide_names:
        try:
            root = _parse_xml(archive.read(slide_name), location=slide_name)
        except (KeyError, OSError, RuntimeError, zipfile.BadZipFile, CliError):
            continue
        for shape in root.findall(f".//{{{P_NS}}}sp"):
            placeholder = shape.find(
                f"./{{{P_NS}}}nvSpPr/{{{P_NS}}}nvPr/{{{P_NS}}}ph"
            )
            if (
                placeholder is not None
                and placeholder.attrib.get("type") in {"title", "ctrTitle"}
                and "".join(
                    node.text or ""
                    for node in shape.findall(f".//{{{A_NS}}}t")
                ).strip()
            ):
                slide_title_count += 1
        for run_index, run in enumerate(root.findall(f".//{{{A_NS}}}r"), 1):
            text = run.find(f"./{{{A_NS}}}t")
            if text is None or not (text.text or ""):
                continue
            text_run_count += 1
            properties = run.find(f"./{{{A_NS}}}rPr")
            language = "" if properties is None else properties.attrib.get("lang", "")
            if language:
                text_runs_with_language += 1
            else:
                missing_language.append(
                    {"slide": slide_name, "run": str(run_index)}
                )
        for picture in root.findall(f".//{{{P_NS}}}pic"):
            picture_count += 1
            properties = picture.find(f"./{{{P_NS}}}nvPicPr/{{{P_NS}}}cNvPr")
            name = ""
            description = ""
            if properties is not None:
                name = properties.attrib.get("name", "")
                description = properties.attrib.get("descr", "").strip()
            if description:
                pictures_with_alt_text += 1
            else:
                missing_alt.append({"slide": slide_name, "name": name})
    return {
        "picture_count": picture_count,
        "pictures_with_alt_text": pictures_with_alt_text,
        "pictures_missing_alt_text": missing_alt,
        "slide_title_count": slide_title_count,
        "text_run_count": text_run_count,
        "text_runs_with_language": text_runs_with_language,
        "text_runs_missing_language": missing_language,
        "manual_check_required": (
            "PowerPoint Accessibility Checker, Reading Order pane, and a screen-reader "
            "test remain required; package inspection cannot establish accessibility."
        ),
    }


def _inspect_forbidden_markup(
    archive: zipfile.ZipFile,
    names: set[str],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for part_name in sorted(
        name
        for name in names
        if name.startswith("ppt/")
        and name.endswith(".xml")
        and "/_rels/" not in name
    ):
        try:
            root = _parse_xml(archive.read(part_name), location=part_name)
        except (KeyError, OSError, RuntimeError, zipfile.BadZipFile, CliError) as exc:
            findings.append(
                _finding("PRESENTATION_XML_INVALID", str(exc), location=part_name)
            )
            continue
        for node in root.iter():
            local = _local_name(node.tag).lower()
            namespace = node.tag.split("}", 1)[0].lower()
            if local in {
                "audio",
                "cmd",
                "control",
                "hlinkclick",
                "hlinkhover",
                "oleobj",
                "snd",
                "timing",
                "transition",
                "video",
            } or any(
                marker in namespace
                for marker in ("activex", "model3d", "webextension")
            ):
                findings.append(
                    _finding(
                        "FORBIDDEN_PRESENTATION_MARKUP",
                        f"active or embedded markup element {local!r} is forbidden",
                        location=part_name,
                    )
                )
                break
    return findings


def inspect_pptx(value: str | Path) -> dict[str, Any]:
    """Inspect a PPTX as ZIP/XML without opening it in PowerPoint or python-pptx."""
    path = checked_input_file(value, max_bytes=MAX_INPUT_BYTES)
    findings: list[dict[str, Any]] = []
    if path.suffix.lower() != ".pptx":
        findings.append(
            _finding(
                "FILE_EXTENSION",
                "only the macro-free .pptx extension is accepted; .pptm is rejected",
                location=str(path),
            )
        )
        return {
            "schema_version": REPORT_SCHEMA_VERSION,
            "path": str(path),
            "safe": False,
            "findings": findings,
        }
    findings.extend(_preflight_zip_directory(path))
    if findings:
        return {
            "schema_version": REPORT_SCHEMA_VERSION,
            "path": str(path),
            "safe": False,
            "findings": findings,
        }

    member_count = 0
    total_uncompressed = 0
    relationship_count = 0
    accessibility: dict[str, Any] = {
        "picture_count": 0,
        "pictures_with_alt_text": 0,
        "pictures_missing_alt_text": [],
        "slide_title_count": 0,
        "text_run_count": 0,
        "text_runs_with_language": 0,
        "text_runs_missing_language": [],
        "manual_check_required": True,
    }
    try:
        with zipfile.ZipFile(path, "r") as archive:
            members, member_findings, names, total_uncompressed = _preflight_members(
                archive
            )
            member_count = len(members)
            findings.extend(member_findings)
            if not member_findings:
                findings.extend(_inspect_content_types(archive, names))
                findings.extend(_inspect_all_xml_parts(archive, names))
                rel_findings, relationship_count = _inspect_relationships(
                    archive, names
                )
                findings.extend(rel_findings)
                findings.extend(_inspect_one_slide_profile(archive, names))
                findings.extend(_inspect_forbidden_markup(archive, names))
                findings.extend(_inspect_image_payloads(archive, names))
                accessibility = _inspect_slide_accessibility(archive, names)
    except (OSError, RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        findings.append(_finding("ZIP_READ_ERROR", str(exc)))

    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "path": str(path),
        "safe": not findings,
        "limits": {
            "max_archive_bytes": MAX_INPUT_BYTES,
            "max_members": MAX_MEMBERS,
            "max_central_directory_bytes": MAX_CENTRAL_DIRECTORY_BYTES,
            "max_member_uncompressed_bytes": MAX_MEMBER_UNCOMPRESSED,
            "max_total_uncompressed_bytes": MAX_TOTAL_UNCOMPRESSED,
            "max_compression_ratio": MAX_COMPRESSION_RATIO,
        },
        "package": {
            "member_count": member_count,
            "total_uncompressed_bytes": total_uncompressed,
            "relationship_count": relationship_count,
        },
        "accessibility": accessibility,
        "findings": findings,
        "inspection_method": (
            "Bounded ZIP central-directory and selected XML-part inspection only; "
            "members were not extracted and the presentation was not opened or executed."
        ),
    }


def require_safe_pptx(value: str | Path) -> dict[str, Any]:
    report = inspect_pptx(value)
    if not report["safe"]:
        codes = ", ".join(item["code"] for item in report["findings"])
        raise CliError(f"unsafe PPTX package ({codes})")
    return report


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _shape_transform(shape: ET.Element) -> tuple[int, int, int, int] | None:
    kind = _local_name(shape.tag)
    if kind == "graphicFrame":
        transform = shape.find(f"./{{{P_NS}}}xfrm")
    else:
        transform = shape.find(f"./{{{P_NS}}}spPr/{{{A_NS}}}xfrm")
    if transform is None:
        return None
    offset = transform.find(f"./{{{A_NS}}}off")
    extent = transform.find(f"./{{{A_NS}}}ext")
    if offset is None or extent is None:
        return None
    try:
        return (
            int(offset.attrib["x"]),
            int(offset.attrib["y"]),
            int(extent.attrib["cx"]),
            int(extent.attrib["cy"]),
        )
    except (KeyError, ValueError):
        return None


def _shape_name(shape: ET.Element) -> str:
    properties = shape.find(f".//{{{P_NS}}}cNvPr")
    return "" if properties is None else properties.attrib.get("name", "")


def _shape_text(shape: ET.Element) -> str:
    return "".join(
        node.text or "" for node in shape.findall(f".//{{{A_NS}}}t")
    ).strip()


def _font_sizes_pt(shape: ET.Element) -> list[float]:
    sizes: list[float] = []
    for tag in ("rPr", "defRPr", "endParaRPr"):
        for node in shape.findall(f".//{{{A_NS}}}{tag}"):
            raw = node.attrib.get("sz")
            if raw is None:
                continue
            try:
                sizes.append(int(raw) / 100.0)
            except ValueError:
                continue
    return sizes


def _intersection(
    first: tuple[int, int, int, int],
    second: tuple[int, int, int, int],
) -> tuple[int, int]:
    first_x, first_y, first_w, first_h = first
    second_x, second_y, second_w, second_h = second
    overlap_w = min(first_x + first_w, second_x + second_w) - max(
        first_x, second_x
    )
    overlap_h = min(first_y + first_h, second_y + second_h) - max(
        first_y, second_y
    )
    return max(0, overlap_w), max(0, overlap_h)


def analyze_layout(
    value: str | Path,
    *,
    print_scale: float = 1.0,
    minimum_font_pt_final: float = 18.0,
) -> dict[str, Any]:
    """Check direct slide shapes for bounds, overlap, and explicit font sizes."""
    if print_scale <= 0:
        raise CliError("print_scale must be greater than zero")
    if minimum_font_pt_final <= 0:
        raise CliError("minimum_font_pt_final must be greater than zero")
    package_report = require_safe_pptx(value)
    path = Path(package_report["path"])
    issues: list[dict[str, Any]] = []
    slides: list[dict[str, Any]] = []

    with zipfile.ZipFile(path, "r") as archive:
        presentation = _parse_xml(
            archive.read("ppt/presentation.xml"),
            location="ppt/presentation.xml",
        )
        slide_size = presentation.find(f"./{{{P_NS}}}sldSz")
        if slide_size is None:
            raise CliError("ppt/presentation.xml does not declare slide dimensions")
        try:
            slide_width = int(slide_size.attrib["cx"])
            slide_height = int(slide_size.attrib["cy"])
        except (KeyError, ValueError) as exc:
            raise CliError("invalid slide dimensions in ppt/presentation.xml") from exc

        slide_names = sorted(
            (
                name
                for name in archive.namelist()
                if name.startswith("ppt/slides/slide")
                and name.endswith(".xml")
                and "/_rels/" not in name
            ),
            key=lambda name: (
                len(PurePosixPath(name).stem),
                PurePosixPath(name).stem,
            ),
        )
        for slide_index, slide_name in enumerate(slide_names, 1):
            root = _parse_xml(archive.read(slide_name), location=slide_name)
            tree = root.find(f"./{{{P_NS}}}cSld/{{{P_NS}}}spTree")
            if tree is None:
                issues.append(
                    {
                        "code": "MISSING_SHAPE_TREE",
                        "slide": slide_index,
                        "message": "slide has no shape tree",
                    }
                )
                continue
            shapes: list[dict[str, Any]] = []
            for child in list(tree):
                kind = _local_name(child.tag)
                if kind not in {"sp", "pic", "graphicFrame", "cxnSp", "grpSp"}:
                    continue
                name = _shape_name(child)
                if kind == "grpSp":
                    issues.append(
                        {
                            "code": "GROUP_REQUIRES_MANUAL_REVIEW",
                            "slide": slide_index,
                            "shape": name,
                            "message": (
                                "group transforms are not flattened by this checker"
                            ),
                        }
                    )
                    continue
                box = _shape_transform(child)
                if box is None:
                    issues.append(
                        {
                            "code": "MISSING_TRANSFORM",
                            "slide": slide_index,
                            "shape": name,
                            "message": "shape position or size could not be read",
                        }
                    )
                    continue
                x, y, width, height = box
                text = _shape_text(child)
                sizes = _font_sizes_pt(child)
                shape_record = {
                    "reading_order": len(shapes) + 1,
                    "name": name,
                    "kind": kind,
                    "x_in": x / EMU_PER_INCH,
                    "y_in": y / EMU_PER_INCH,
                    "width_in": width / EMU_PER_INCH,
                    "height_in": height / EMU_PER_INCH,
                    "has_text": bool(text),
                    "_box": box,
                }
                shapes.append(shape_record)
                if x < 0 or y < 0 or x + width > slide_width or y + height > slide_height:
                    issues.append(
                        {
                            "code": "OUT_OF_BOUNDS",
                            "slide": slide_index,
                            "shape": name,
                            "message": "shape extends outside the slide canvas",
                        }
                    )
                if text:
                    if not sizes:
                        issues.append(
                            {
                                "code": "FONT_SIZE_UNSPECIFIED",
                                "slide": slide_index,
                                "shape": name,
                                "message": (
                                    "text has no explicit run/default font size; "
                                    "theme inheritance requires manual review"
                                ),
                            }
                        )
                    else:
                        minimum_design = min(sizes)
                        minimum_final = minimum_design * print_scale
                        shape_record["minimum_font_pt_design"] = minimum_design
                        shape_record["minimum_font_pt_final"] = minimum_final
                        if minimum_final + 1e-6 < minimum_font_pt_final:
                            issues.append(
                                {
                                    "code": "FONT_TOO_SMALL",
                                    "slide": slide_index,
                                    "shape": name,
                                    "message": (
                                        f"minimum final font {minimum_final:.2f} pt "
                                        f"is below {minimum_font_pt_final:.2f} pt"
                                    ),
                                }
                            )

            for first_index, first in enumerate(shapes):
                first_box = first["_box"]
                if first_box[2] <= 0 or first_box[3] <= 0:
                    continue
                for second in shapes[first_index + 1 :]:
                    second_box = second["_box"]
                    if second_box[2] <= 0 or second_box[3] <= 0:
                        continue
                    overlap_width, overlap_height = _intersection(
                        first_box, second_box
                    )
                    if overlap_width > 0 and overlap_height > 0:
                        overlap_area = overlap_width * overlap_height
                        smaller_area = min(
                            first_box[2] * first_box[3],
                            second_box[2] * second_box[3],
                        )
                        issues.append(
                            {
                                "code": "SHAPE_OVERLAP",
                                "slide": slide_index,
                                "shapes": [first["name"], second["name"]],
                                "overlap_fraction_of_smaller": (
                                    overlap_area / smaller_area
                                ),
                                "message": (
                                    "direct shape bounding boxes overlap; determine "
                                    "whether this is intentional"
                                ),
                            }
                        )
            for shape in shapes:
                shape.pop("_box", None)
            slides.append(
                {
                    "slide": slide_index,
                    "part": slide_name,
                    "shape_count": len(shapes),
                    "reading_order": [
                        {"order": shape["reading_order"], "name": shape["name"]}
                        for shape in shapes
                    ],
                    "shapes": shapes,
                }
            )

    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "path": str(path),
        "pass": not issues,
        "slide_size": {
            "width_in": slide_width / EMU_PER_INCH,
            "height_in": slide_height / EMU_PER_INCH,
        },
        "print_scale": print_scale,
        "minimum_font_pt_final": minimum_font_pt_final,
        "minimum_font_basis": (
            "Caller-supplied requirement or project heuristic; this value is not "
            "a universal poster standard."
        ),
        "slides": slides,
        "issues": issues,
        "manual_checks": [
            "Review text overflow in PowerPoint; XML bounds do not reveal rendered overflow.",
            "Confirm Reading Order pane order and test with a screen reader.",
            "Inspect intentional overlays, rotated objects, groups, charts, and SmartArt manually.",
        ],
    }


def strip_generated_printer_settings(source: Path, destination: Path) -> None:
    """Remove python-pptx's inert default printer-settings binary from new output."""
    with zipfile.ZipFile(source, "r") as input_archive:
        _, preflight_findings, _, _ = _preflight_members(input_archive)
        unexpected = [
            finding
            for finding in preflight_findings
            if not (
                finding["code"] == "FORBIDDEN_BINARY_PART"
                and str(finding.get("location", "")).startswith(
                    "ppt/printerSettings/"
                )
            )
        ]
        if unexpected:
            codes = ", ".join(finding["code"] for finding in unexpected)
            raise CliError(
                f"generated package has unexpected ZIP findings before cleanup: {codes}"
            )
        with zipfile.ZipFile(
            destination,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=6,
            allowZip64=True,
        ) as output_archive:
            for info in input_archive.infolist():
                if info.filename.startswith("ppt/printerSettings/"):
                    continue
                info.date_time = DETERMINISTIC_ZIP_DATETIME
                if info.filename == "[Content_Types].xml":
                    root = _parse_xml(
                        input_archive.read(info.filename),
                        location=info.filename,
                    )
                    for node in list(root):
                        if (
                            node.tag == f"{{{CT_NS}}}Default"
                            and node.attrib.get("Extension", "").lower() == "bin"
                            and node.attrib.get("ContentType", "").endswith(
                                ".printerSettings"
                            )
                        ):
                            root.remove(node)
                    output_archive.writestr(
                        info,
                        ET.tostring(
                            root,
                            encoding="utf-8",
                            xml_declaration=True,
                        ),
                    )
                    continue
                if info.filename.endswith(".rels"):
                    root = _parse_xml(
                        input_archive.read(info.filename),
                        location=info.filename,
                    )
                    changed = False
                    for relationship in list(root):
                        if relationship.attrib.get("Type", "").endswith(
                            "/printerSettings"
                        ):
                            root.remove(relationship)
                            changed = True
                    if changed:
                        output_archive.writestr(
                            info,
                            ET.tostring(
                                root,
                                encoding="utf-8",
                                xml_declaration=True,
                            ),
                        )
                        continue
                with input_archive.open(info, "r") as source_handle:
                    with output_archive.open(info, "w") as destination_handle:
                        shutil.copyfileobj(
                            source_handle,
                            destination_handle,
                            length=1024 * 1024,
                        )


def patch_accessibility_metadata(
    source: Path,
    destination: Path,
    *,
    alt_text_by_shape_name: dict[str, str],
    language: str,
) -> None:
    """Add picture descriptions and explicit run language to a generated PPTX."""
    require_safe_pptx(source)
    found: dict[str, int] = {name: 0 for name in alt_text_by_shape_name}
    with zipfile.ZipFile(source, "r") as input_archive:
        with zipfile.ZipFile(
            destination,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=6,
            allowZip64=True,
        ) as output_archive:
            for info in input_archive.infolist():
                info.date_time = DETERMINISTIC_ZIP_DATETIME
                if (
                    info.filename.startswith("ppt/slides/slide")
                    and info.filename.endswith(".xml")
                    and "/_rels/" not in info.filename
                ):
                    root = _parse_xml(
                        input_archive.read(info.filename),
                        location=info.filename,
                    )
                    changed = False
                    for picture in root.findall(f".//{{{P_NS}}}pic"):
                        properties = picture.find(
                            f"./{{{P_NS}}}nvPicPr/{{{P_NS}}}cNvPr"
                        )
                        if properties is None:
                            continue
                        name = properties.attrib.get("name", "")
                        if name not in alt_text_by_shape_name:
                            continue
                        properties.set("descr", alt_text_by_shape_name[name])
                        properties.set("title", name)
                        found[name] += 1
                        changed = True
                    for run in root.findall(f".//{{{A_NS}}}r"):
                        properties = run.find(f"./{{{A_NS}}}rPr")
                        if properties is None:
                            properties = ET.Element(f"{{{A_NS}}}rPr")
                            run.insert(0, properties)
                        if properties.attrib.get("lang") != language:
                            properties.set("lang", language)
                            changed = True
                    for tag in ("defRPr", "endParaRPr"):
                        for properties in root.findall(f".//{{{A_NS}}}{tag}"):
                            if properties.attrib.get("lang") != language:
                                properties.set("lang", language)
                                changed = True
                    payload = (
                        ET.tostring(
                            root,
                            encoding="utf-8",
                            xml_declaration=True,
                        )
                        if changed
                        else input_archive.read(info.filename)
                    )
                    output_archive.writestr(info, payload)
                    continue
                with input_archive.open(info, "r") as source_handle:
                    with output_archive.open(info, "w") as destination_handle:
                        shutil.copyfileobj(
                            source_handle,
                            destination_handle,
                            length=1024 * 1024,
                        )
    missing = [name for name, count in found.items() if count != 1]
    if missing:
        raise CliError(
            "could not apply alt text exactly once for shape(s): "
            + ", ".join(sorted(missing))
        )
