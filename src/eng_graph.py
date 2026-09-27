"""Minimal engineering-graph Proof of Principle for Experiment 007."""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from typing import Any, Iterable


TOOL_NAME = "exp-007-minimal-engineering-graph"
TOOL_VERSION = "0.1"

OBJECT_TYPES = {
    "use-case",
    "requirement",
    "interface-requirement",
    "architecture-element",
    "verification-case",
}

RELATION_RULES = {
    "source": {
        ("requirement", "use-case"),
        ("interface-requirement", "requirement"),
    },
    "allocated_to": {
        ("requirement", "architecture-element"),
        ("requirement", "interface-requirement"),
        ("interface-requirement", "architecture-element"),
    },
    "verified_by": {
        ("requirement", "verification-case"),
        ("interface-requirement", "verification-case"),
    },
    "related_to": {
        ("architecture-element", "architecture-element"),
    },
}


class GraphError(ValueError):
    """Raised when authored engineering-graph data is invalid."""


def load_graph(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise GraphError("graph root must be an object")
    return data


def _require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GraphError(f"{label} must be a non-empty string")
    return value


def validate_graph(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if data.get("schema_version") != 1:
        raise GraphError("schema_version must be 1")

    provenance = data.get("provenance")
    if not isinstance(provenance, dict):
        raise GraphError("provenance must be an object")
    _require_text(provenance.get("source_repository"), "provenance.source_repository")
    _require_text(provenance.get("source_revision"), "provenance.source_revision")

    objects = data.get("objects")
    if not isinstance(objects, list):
        raise GraphError("objects must be a list")

    by_id: dict[str, dict[str, Any]] = {}
    for index, obj in enumerate(objects):
        if not isinstance(obj, dict):
            raise GraphError(f"objects[{index}] must be an object")

        object_id = _require_text(obj.get("id"), f"objects[{index}].id")
        if object_id in by_id:
            raise GraphError(f"duplicate engineering id: {object_id}")

        object_type = _require_text(obj.get("type"), f"{object_id}.type")
        if object_type not in OBJECT_TYPES:
            raise GraphError(f"{object_id}: unsupported object type {object_type!r}")

        _require_text(obj.get("title"), f"{object_id}.title")

        source = obj.get("source")
        if not isinstance(source, dict):
            raise GraphError(f"{object_id}.source must be an object")
        _require_text(source.get("url"), f"{object_id}.source.url")
        _require_text(source.get("anchor"), f"{object_id}.source.anchor")

        relations = obj.get("relations", [])
        if not isinstance(relations, list):
            raise GraphError(f"{object_id}.relations must be a list")

        by_id[object_id] = obj

    for object_id, obj in by_id.items():
        source_type = obj["type"]
        for index, relation in enumerate(obj.get("relations", [])):
            if not isinstance(relation, dict):
                raise GraphError(f"{object_id}.relations[{index}] must be an object")

            relation_type = _require_text(
                relation.get("type"), f"{object_id}.relations[{index}].type"
            )
            target_id = _require_text(
                relation.get("target"), f"{object_id}.relations[{index}].target"
            )

            if relation_type not in RELATION_RULES:
                raise GraphError(
                    f"{object_id}: unsupported relation type {relation_type!r}"
                )
            if target_id not in by_id:
                raise GraphError(
                    f"{object_id}: relation {relation_type!r} targets unknown id "
                    f"{target_id!r}"
                )

            target_type = by_id[target_id]["type"]
            if (source_type, target_type) not in RELATION_RULES[relation_type]:
                raise GraphError(
                    f"{object_id}: relation {relation_type!r} is not allowed from "
                    f"{source_type!r} to {target_type!r} ({target_id})"
                )

    for object_id, obj in by_id.items():
        if obj["type"] != "requirement":
            continue

        relation_types = {r["type"] for r in obj.get("relations", [])}
        if "source" not in relation_types:
            raise GraphError(f"{object_id}: requirement has no upstream source")
        if "allocated_to" not in relation_types:
            raise GraphError(f"{object_id}: requirement has no allocation")
        if obj.get("verification_required", True) and "verified_by" not in relation_types:
            raise GraphError(
                f"{object_id}: requirement in verification baseline has no verification"
            )

    return by_id


def normalize_graph(data: dict[str, Any]) -> dict[str, Any]:
    by_id = validate_graph(data)
    incoming: dict[str, list[dict[str, str]]] = {
        object_id: [] for object_id in by_id
    }

    for source_id, obj in by_id.items():
        for relation in obj.get("relations", []):
            incoming[relation["target"]].append(
                {"type": relation["type"], "source": source_id}
            )

    normalized_objects = []
    for object_id in sorted(by_id):
        obj = by_id[object_id]
        normalized = {
            key: value
            for key, value in obj.items()
            if key not in {"relations", "incoming"}
        }
        normalized["relations"] = sorted(
            (
                {"type": relation["type"], "target": relation["target"]}
                for relation in obj.get("relations", [])
            ),
            key=lambda item: (item["type"], item["target"]),
        )
        normalized["incoming"] = sorted(
            incoming[object_id],
            key=lambda item: (item["type"], item["source"]),
        )
        normalized_objects.append(normalized)

    return {
        "schema_version": data["schema_version"],
        "generator": {"name": TOOL_NAME, "version": TOOL_VERSION},
        "provenance": data["provenance"],
        "objects": normalized_objects,
    }


def _relation_filter(
    relation_type: str, allowed: set[str] | None
) -> bool:
    return allowed is None or relation_type in allowed


def focus_graph(
    normalized: dict[str, Any],
    root_id: str,
    *,
    depth: int = 1,
    direction: str = "both",
    relation_types: Iterable[str] | None = None,
) -> dict[str, Any]:
    if depth < 0:
        raise GraphError("focus depth must be >= 0")
    if direction not in {"incoming", "outgoing", "both"}:
        raise GraphError("focus direction must be incoming, outgoing or both")

    objects = {obj["id"]: obj for obj in normalized["objects"]}
    if root_id not in objects:
        raise GraphError(f"focus root is unknown: {root_id}")

    allowed = set(relation_types) if relation_types is not None else None
    selected = {root_id}
    edges: set[tuple[str, str, str]] = set()
    queue: deque[tuple[str, int]] = deque([(root_id, 0)])
    visited_depth: dict[str, int] = {root_id: 0}

    while queue:
        current_id, current_depth = queue.popleft()
        if current_depth >= depth:
            continue

        current = objects[current_id]
        neighbors: list[tuple[str, str, str]] = []

        if direction in {"outgoing", "both"}:
            for relation in current.get("relations", []):
                if _relation_filter(relation["type"], allowed):
                    neighbors.append(
                        (current_id, relation["type"], relation["target"])
                    )

        if direction in {"incoming", "both"}:
            for relation in current.get("incoming", []):
                if _relation_filter(relation["type"], allowed):
                    neighbors.append(
                        (relation["source"], relation["type"], current_id)
                    )

        for source_id, relation_type, target_id in neighbors:
            edges.add((source_id, relation_type, target_id))
            neighbor_id = target_id if source_id == current_id else source_id
            selected.add(neighbor_id)
            next_depth = current_depth + 1
            if visited_depth.get(neighbor_id, next_depth + 1) > next_depth:
                visited_depth[neighbor_id] = next_depth
                queue.append((neighbor_id, next_depth))

    focused_objects = []
    for object_id in sorted(selected):
        obj = objects[object_id]
        focused_objects.append(
            {
                "id": obj["id"],
                "type": obj["type"],
                "title": obj["title"],
                "source": obj["source"],
            }
        )

    return {
        "schema_version": normalized["schema_version"],
        "generator": normalized["generator"],
        "provenance": normalized["provenance"],
        "focus": {
            "root": root_id,
            "depth": depth,
            "direction": direction,
            "relation_types": sorted(allowed) if allowed is not None else None,
        },
        "objects": focused_objects,
        "edges": [
            {"source": source, "type": relation_type, "target": target}
            for source, relation_type, target in sorted(edges)
        ],
    }


def write_json(data: dict[str, Any], path: str | Path) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=False)
        handle.write("\n")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate authored graph")
    validate.add_argument("input")

    export = subparsers.add_parser(
        "export", help="validate and export normalized graph with backlinks"
    )
    export.add_argument("input")
    export.add_argument("output")

    focus = subparsers.add_parser(
        "focus", help="export a bounded relationship neighborhood"
    )
    focus.add_argument("input")
    focus.add_argument("root")
    focus.add_argument("output")
    focus.add_argument("--depth", type=int, default=1)
    focus.add_argument(
        "--direction",
        choices=("incoming", "outgoing", "both"),
        default="both",
    )
    focus.add_argument(
        "--relation",
        action="append",
        dest="relations",
        help="limit traversal to one relation type; repeat as needed",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        authored = load_graph(args.input)
        if args.command == "validate":
            by_id = validate_graph(authored)
            print(f"valid engineering graph: {len(by_id)} objects")
            return 0

        normalized = normalize_graph(authored)
        if args.command == "export":
            write_json(normalized, args.output)
            print(f"wrote normalized graph: {args.output}")
            return 0

        focused = focus_graph(
            normalized,
            args.root,
            depth=args.depth,
            direction=args.direction,
            relation_types=args.relations,
        )
        write_json(focused, args.output)
        print(f"wrote focused graph: {args.output}")
        return 0
    except (GraphError, json.JSONDecodeError, OSError) as exc:
        parser.exit(2, f"error: {exc}\n")

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
