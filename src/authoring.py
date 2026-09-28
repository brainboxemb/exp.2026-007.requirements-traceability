"""Extract Experiment 007 engineering objects from readable Markdown fixtures."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from src.eng_graph import GraphError, normalize_graph, validate_graph, write_json


class AuthoringError(ValueError):
    """Raised when a Markdown authoring fixture is malformed."""


HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
ANCHOR_RE = re.compile(r'^<a\s+id="([^"]+)"\s*></a>\s*$')
BOLD_TITLE_RE = re.compile(r"^\*\*(.+?)\*\*\s*$")
META_RE = re.compile(r"<!--\s*eng\s*\n(.*?)\n-->", re.DOTALL)

EXPERIMENT_REPO = "brainboxemb/exp.2026-007.requirements-traceability"


def github_slug(title: str) -> str:
    """Approximate GitHub's Markdown heading slug for the experiment fixtures."""
    value = title.strip().lower()
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    value = value.replace(" ", "-")
    return value


def split_identity(title: str) -> tuple[str, str]:
    if " — " in title:
        object_id, label = title.split(" — ", 1)
        return object_id.strip(), label.strip()
    value = title.strip()
    return value, value


def _marker_lines(lines: list[str]) -> list[dict[str, Any]]:
    markers: list[dict[str, Any]] = []
    index = 0
    while index < len(lines):
        line = lines[index]

        heading = HEADING_RE.match(line)
        if heading:
            raw_title = heading.group(1).strip()
            object_id, title = split_identity(raw_title)
            markers.append(
                {
                    "start": index,
                    "title_line": index,
                    "id": object_id,
                    "title": title,
                    "anchor": github_slug(raw_title),
                }
            )
            index += 1
            continue

        anchor = ANCHOR_RE.match(line)
        if anchor and index + 1 < len(lines):
            bold = BOLD_TITLE_RE.match(lines[index + 1])
            if bold:
                raw_title = bold.group(1).strip()
                object_id, title = split_identity(raw_title)
                if anchor.group(1) != object_id:
                    raise AuthoringError(
                        f"line {index + 1}: anchor {anchor.group(1)!r} does not "
                        f"match object id {object_id!r}"
                    )
                markers.append(
                    {
                        "start": index,
                        "title_line": index + 1,
                        "id": object_id,
                        "title": title,
                        "anchor": anchor.group(1),
                    }
                )
                index += 2
                continue

        index += 1

    return markers


def _metadata_from_section(
    section: str,
    *,
    path: Path,
    line_number: int,
) -> tuple[dict[str, Any], str]:
    matches = list(META_RE.finditer(section))
    if len(matches) != 1:
        raise AuthoringError(
            f"{path}:{line_number}: expected exactly one hidden eng metadata block"
        )
    raw = matches[0].group(1)
    try:
        metadata = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AuthoringError(
            f"{path}:{line_number}: invalid eng metadata JSON: {exc.msg}"
        ) from exc
    if not isinstance(metadata, dict):
        raise AuthoringError(
            f"{path}:{line_number}: eng metadata must be a JSON object"
        )
    visible = (section[: matches[0].start()] + section[matches[0].end() :]).strip()
    return metadata, visible


def _sidecar_metadata(path: Path) -> dict[str, dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AuthoringError(f"{path}: cannot read sidecar metadata: {exc}") from exc

    if data.get("schema_version") != 1:
        raise AuthoringError(f"{path}: schema_version must be 1")
    objects = data.get("objects")
    if not isinstance(objects, dict):
        raise AuthoringError(f"{path}: objects must be an object")
    return objects


def _relations(metadata: dict[str, Any], object_id: str) -> list[dict[str, str]]:
    relation_map = metadata.get("relations", {})
    if relation_map is None:
        relation_map = {}
    if not isinstance(relation_map, dict):
        raise AuthoringError(f"{object_id}: relations must be an object")

    relations: list[dict[str, str]] = []
    for relation_type, targets in relation_map.items():
        if not isinstance(targets, list) or not all(
            isinstance(target, str) and target for target in targets
        ):
            raise AuthoringError(
                f"{object_id}: relation {relation_type!r} must be a list of ids"
            )
        for target in targets:
            relations.append({"type": relation_type, "target": target})
    return relations


def load_reference(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AuthoringError(f"{source}: cannot read reference metadata: {exc}") from exc

    for key in ("source_repository", "source_revision"):
        if not isinstance(data.get(key), str) or not data[key]:
            raise AuthoringError(f"{source}: missing {key}")
    return data


def extract_markdown(
    markdown_path: str | Path,
    reference_path: str | Path,
    *,
    mode: str,
    sidecar_path: str | Path | None = None,
) -> dict[str, Any]:
    if mode not in {"compact", "sidecar"}:
        raise AuthoringError("mode must be compact or sidecar")

    path = Path(markdown_path)
    reference = load_reference(reference_path)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    markers = _marker_lines(lines)
    if not markers:
        raise AuthoringError(f"{path}: no engineering object markers found")

    sidecar: dict[str, dict[str, Any]] | None = None
    if mode == "sidecar":
        if sidecar_path is None:
            raise AuthoringError("sidecar mode requires sidecar metadata")
        sidecar = _sidecar_metadata(Path(sidecar_path))

    objects: list[dict[str, Any]] = []
    seen: set[str] = set()

    for position, marker in enumerate(markers):
        object_id = marker["id"]
        if object_id in seen:
            raise AuthoringError(
                f"{path}:{marker['title_line'] + 1}: duplicate object id {object_id}"
            )
        seen.add(object_id)

        end = markers[position + 1]["start"] if position + 1 < len(markers) else len(lines)
        body_start = marker["title_line"] + 1
        section = "\n".join(lines[body_start:end]).strip()

        if mode == "compact":
            metadata, visible = _metadata_from_section(
                section,
                path=path,
                line_number=marker["title_line"] + 1,
            )
        else:
            assert sidecar is not None
            if object_id not in sidecar:
                raise AuthoringError(
                    f"{path}:{marker['title_line'] + 1}: sidecar has no metadata "
                    f"for {object_id}"
                )
            metadata = sidecar[object_id]
            visible = section.strip()

        object_type = metadata.get("type")
        if not isinstance(object_type, str) or not object_type:
            raise AuthoringError(
                f"{path}:{marker['title_line'] + 1}: {object_id} has no type"
            )

        source_url = (
            f"https://github.com/{EXPERIMENT_REPO}/blob/main/"
            f"{path.as_posix()}#{marker['anchor']}"
        )
        objects.append(
            {
                "id": object_id,
                "type": object_type,
                "title": marker["title"],
                "content": visible,
                "source": {
                    "url": source_url,
                    "anchor": marker["anchor"],
                },
                "relations": _relations(metadata, object_id),
            }
        )

    if sidecar is not None:
        extra = sorted(set(sidecar) - seen)
        if extra:
            raise AuthoringError(
                f"{sidecar_path}: metadata contains objects not present in Markdown: "
                + ", ".join(extra)
            )

    authored = {
        "schema_version": 1,
        "provenance": {
            "source_repository": reference["source_repository"],
            "source_revision": reference["source_revision"],
            "authoring_fixture": path.as_posix(),
            "authoring_mode": mode,
        },
        "objects": objects,
    }

    try:
        validate_graph(authored)
    except GraphError as exc:
        raise AuthoringError(f"{path}: {exc}") from exc
    return authored


def semantic_signature(normalized: dict[str, Any]) -> dict[str, Any]:
    """Return source-location-independent graph semantics for authoring comparison."""
    result: list[dict[str, Any]] = []
    for obj in normalized["objects"]:
        result.append(
            {
                "id": obj["id"],
                "type": obj["type"],
                "title": obj["title"],
                "relations": obj.get("relations", []),
                "incoming": obj.get("incoming", []),
            }
        )
    return {"objects": result}


def authoring_stats(path: str | Path, *, mode: str) -> dict[str, int]:
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()
    stats = {
        "total_lines": len(lines),
        "object_count": len(_marker_lines(lines)),
        "explicit_anchor_lines": sum(1 for line in lines if ANCHOR_RE.match(line)),
    }
    if mode == "compact":
        metadata_lines = 0
        in_metadata = False
        for line in lines:
            if line.strip().startswith("<!-- eng"):
                in_metadata = True
            if in_metadata:
                metadata_lines += 1
            if in_metadata and line.strip() == "-->":
                in_metadata = False
        stats["metadata_lines"] = metadata_lines
    return stats


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    extract = sub.add_parser("extract", help="extract and validate authored Markdown")
    extract.add_argument("markdown")
    extract.add_argument("reference")
    extract.add_argument("output")
    extract.add_argument("--mode", choices=("compact", "sidecar"), required=True)
    extract.add_argument("--sidecar")

    compare = sub.add_parser("compare", help="compare compact and sidecar semantics")
    compare.add_argument("compact")
    compare.add_argument("sidecar_markdown")
    compare.add_argument("sidecar_metadata")
    compare.add_argument("reference")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "extract":
            authored = extract_markdown(
                args.markdown,
                args.reference,
                mode=args.mode,
                sidecar_path=args.sidecar,
            )
            normalized = normalize_graph(authored)
            write_json(normalized, args.output)
            print(
                f"extracted {len(normalized['objects'])} engineering objects "
                f"from {args.markdown}"
            )
            return 0

        compact = normalize_graph(
            extract_markdown(args.compact, args.reference, mode="compact")
        )
        sidecar = normalize_graph(
            extract_markdown(
                args.sidecar_markdown,
                args.reference,
                mode="sidecar",
                sidecar_path=args.sidecar_metadata,
            )
        )
        if semantic_signature(compact) != semantic_signature(sidecar):
            raise AuthoringError(
                "compact and sidecar authoring do not produce the same semantics"
            )

        result = {
            "object_count": len(compact["objects"]),
            "semantic_match": True,
            "compact": authoring_stats(args.compact, mode="compact"),
            "sidecar_markdown": authoring_stats(args.sidecar_markdown, mode="sidecar"),
            "sidecar_metadata_lines": len(
                Path(args.sidecar_metadata).read_text(encoding="utf-8").splitlines()
            ),
        }
        print(json.dumps(result, indent=2))
        return 0
    except (AuthoringError, GraphError, OSError, json.JSONDecodeError) as exc:
        parser.exit(2, f"error: {exc}\n")

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
