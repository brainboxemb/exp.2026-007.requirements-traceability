"""Generate the Experiment 007 Material portal from Sphinx-Needs needs.json."""

from __future__ import annotations

import argparse
import html
import json
import shutil
from collections import deque
from pathlib import Path
from typing import Any


LINK_TYPES = (
    "derived_from",
    "allocated_to",
    "verified_by",
    "related_to",
)

TYPE_LABELS = {
    "uc": "Use case",
    "req": "Requirement",
    "ifreq": "Interface requirement",
    "arch": "Architecture element",
    "vc": "Verification case",
}

ARCHITECTURE_OBJECTS = (
    "IF03-REQ-004",
    "CommandHandler",
    "TimingNode",
)

REFERENCE_FOCUS_ROOT = "SI01-REQ-020"


class PortalError(ValueError):
    """Raised when portal input cannot satisfy the generated view contract."""


def load_needs(path: str | Path) -> dict[str, dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    current_version = data.get("current_version")
    versions = data.get("versions", {})
    if current_version not in versions:
        raise PortalError("needs.json has no current version payload")

    needs = versions[current_version].get("needs")
    if not isinstance(needs, dict):
        raise PortalError("needs.json current version has no needs object")
    return needs


def normalize_needs(needs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    objects: dict[str, dict[str, Any]] = {}

    for object_id, need in needs.items():
        object_type = need.get("type")
        if object_type not in TYPE_LABELS:
            raise PortalError(
                f"{object_id}: unsupported portal object type {object_type!r}"
            )

        outgoing = []
        incoming = []
        for link_type in LINK_TYPES:
            for target in need.get(link_type, []) or []:
                if target in needs:
                    outgoing.append({"type": link_type, "target": target})
            for source in need.get(f"{link_type}_back", []) or []:
                if source in needs:
                    incoming.append({"type": link_type, "source": source})

        objects[object_id] = {
            "id": object_id,
            "type": object_type,
            "type_label": TYPE_LABELS[object_type],
            "title": need.get("title") or object_id,
            "content": (need.get("content") or "").strip(),
            "origin_url": need.get("origin_url"),
            "origin_anchor": need.get("origin_anchor"),
            "outgoing": sorted(
                outgoing, key=lambda item: (item["type"], item["target"])
            ),
            "incoming": sorted(
                incoming, key=lambda item: (item["type"], item["source"])
            ),
        }

    focus_depth_1 = {
        object_id: focus_graph(objects, object_id, depth=1, direction="both")
        for object_id in objects
    }

    return {
        "schema_version": 1,
        "default_object": REFERENCE_FOCUS_ROOT,
        "link_types": list(LINK_TYPES),
        "objects": objects,
        "focus_depth_1": focus_depth_1,
    }


def focus_graph(
    objects: dict[str, dict[str, Any]],
    root_id: str,
    *,
    depth: int,
    direction: str,
) -> dict[str, Any]:
    if root_id not in objects:
        raise PortalError(f"unknown focus root: {root_id}")
    if depth < 0:
        raise PortalError("focus depth must be >= 0")
    if direction not in {"incoming", "outgoing", "both"}:
        raise PortalError("focus direction must be incoming, outgoing or both")

    selected = {root_id}
    edges: set[tuple[str, str, str]] = set()
    queue: deque[tuple[str, int]] = deque([(root_id, 0)])
    visited_depth = {root_id: 0}

    while queue:
        current_id, current_depth = queue.popleft()
        if current_depth >= depth:
            continue

        current = objects[current_id]
        neighbors: list[tuple[str, str, str]] = []

        if direction in {"outgoing", "both"}:
            for relation in current["outgoing"]:
                neighbors.append(
                    (current_id, relation["type"], relation["target"])
                )

        if direction in {"incoming", "both"}:
            for relation in current["incoming"]:
                neighbors.append(
                    (relation["source"], relation["type"], current_id)
                )

        for source, relation_type, target in neighbors:
            edges.add((source, relation_type, target))
            neighbor = target if source == current_id else source
            selected.add(neighbor)
            next_depth = current_depth + 1
            if visited_depth.get(neighbor, next_depth + 1) > next_depth:
                visited_depth[neighbor] = next_depth
                queue.append((neighbor, next_depth))

    return {
        "root": root_id,
        "depth": depth,
        "direction": direction,
        "objects": sorted(selected),
        "edges": [
            {"source": source, "type": relation_type, "target": target}
            for source, relation_type, target in sorted(edges)
        ],
    }


def _object_link(object_id: str) -> str:
    return f"{object_id}.md"


def _source_url(obj: dict[str, Any]) -> str | None:
    url = obj.get("origin_url")
    anchor = obj.get("origin_anchor")
    if not url:
        return None
    return f"{url}#{anchor}" if anchor else url


def render_object_page(obj: dict[str, Any], graph: dict[str, Any]) -> str:
    lines = [
        f"# {obj['id']} — {obj['title']}",
        "",
        f"**Type:** {obj['type_label']}  ",
    ]

    source_url = _source_url(obj)
    if source_url:
        lines.append(f"**Authority:** [open source section]({source_url})  ")

    lines.extend(
        [
            f"**Explorer:** [open with context](../explorer.md?object={obj['id']})",
            "",
        ]
    )

    if obj["content"]:
        lines.extend(["## Definition", "", obj["content"], ""])

    lines.extend(["## Outgoing relationships", ""])
    if obj["outgoing"]:
        lines.extend(
            [
                "| Relation | Target |",
                "| --- | --- |",
            ]
        )
        for relation in obj["outgoing"]:
            target = graph["objects"][relation["target"]]
            lines.append(
                f"| {relation['type']} | "
                f"[{target['id']} — {target['title']}]({_object_link(target['id'])}) |"
            )
    else:
        lines.append("None in this reference slice.")

    lines.extend(["", "## Incoming relationships", ""])
    if obj["incoming"]:
        lines.extend(
            [
                "| Relation | Source |",
                "| --- | --- |",
            ]
        )
        for relation in obj["incoming"]:
            source = graph["objects"][relation["source"]]
            lines.append(
                f"| {relation['type']} | "
                f"[{source['id']} — {source['title']}]({_object_link(source['id'])}) |"
            )
    else:
        lines.append("None in this reference slice.")

    focus = graph["focus_depth_1"][obj["id"]]
    lines.extend(
        [
            "",
            "## One-hop context",
            "",
            "Exact shortest-path depth 1 over incoming and outgoing traceability links.",
            "",
        ]
    )
    for related_id in focus["objects"]:
        if related_id == obj["id"]:
            continue
        related = graph["objects"][related_id]
        lines.append(
            f"- [{related['id']} — {related['title']}]({_object_link(related_id)})"
        )

    lines.append("")
    return "\n".join(lines)


def render_object_index(graph: dict[str, Any]) -> str:
    lines = [
        "# Engineering object index",
        "",
        "Generated from needs.json; no object descriptions are maintained here.",
        "",
        "| ID | Type | Title |",
        "| --- | --- | --- |",
    ]
    for object_id in sorted(graph["objects"]):
        obj = graph["objects"][object_id]
        lines.append(
            f"| [{object_id}]({_object_link(object_id)}) "
            f"| {obj['type_label']} | {obj['title']} |"
        )
    lines.append("")
    return "\n".join(lines)


def _architecture_edges(graph: dict[str, Any]) -> list[dict[str, str]]:
    selected = set(ARCHITECTURE_OBJECTS)
    edges = []
    for source_id in ARCHITECTURE_OBJECTS:
        source = graph["objects"][source_id]
        for relation in source["outgoing"]:
            if relation["target"] in selected:
                edges.append(
                    {
                        "source": source_id,
                        "type": relation["type"],
                        "target": relation["target"],
                    }
                )
    return edges


def render_architecture_svg(graph: dict[str, Any]) -> str:
    positions = {
        "IF03-REQ-004": (30, 80),
        "CommandHandler": (300, 80),
        "TimingNode": (570, 80),
    }
    width = 190
    height = 86

    for object_id in ARCHITECTURE_OBJECTS:
        if object_id not in graph["objects"]:
            raise PortalError(f"architecture object is absent: {object_id}")

    parts = [
        '<svg class="eng-architecture" viewBox="0 0 790 250" '
        'role="img" aria-label="Clickable engineering architecture slice">',
        '<defs><marker id="eng-arrow" markerWidth="8" markerHeight="8" '
        'refX="7" refY="3" orient="auto" markerUnits="strokeWidth">'
        '<path d="M0,0 L0,6 L8,3 z" '
        'fill="var(--md-default-fg-color--lighter)" /></marker></defs>',
    ]

    for edge in _architecture_edges(graph):
        sx, sy = positions[edge["source"]]
        tx, ty = positions[edge["target"]]
        if sx < tx:
            x1, x2 = sx + width, tx
        else:
            x1, x2 = sx, tx + width
        y1 = sy + height / 2
        y2 = ty + height / 2
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 - 8
        parts.append(
            f'<line class="eng-edge" x1="{x1}" y1="{y1}" '
            f'x2="{x2}" y2="{y2}" marker-end="url(#eng-arrow)" />'
        )
        parts.append(
            f'<text class="eng-edge-label" x="{mx}" y="{my}" '
            f'text-anchor="middle">{html.escape(edge["type"])}</text>'
        )

    for object_id in ARCHITECTURE_OBJECTS:
        obj = graph["objects"][object_id]
        x, y = positions[object_id]
        title = html.escape(obj["title"])
        object_text = html.escape(object_id)
        parts.extend(
            [
                f'<g class="eng-node" data-object-id="{html.escape(object_id)}" '
                'role="button" tabindex="0">',
                f'<rect x="{x}" y="{y}" width="{width}" height="{height}" />',
                f'<text x="{x + 14}" y="{y + 31}">{object_text}</text>',
                f'<text x="{x + 14}" y="{y + 57}">{title}</text>',
                "</g>",
            ]
        )

    parts.append("</svg>")
    return "\n".join(parts)


def render_explorer(graph: dict[str, Any]) -> str:
    chips = []
    for object_id in sorted(graph["objects"]):
        chips.append(
            f'<button class="eng-object-chip" type="button" '
            f'data-object-id="{html.escape(object_id)}">'
            f'{html.escape(object_id)}</button>'
        )

    graph_json = json.dumps(graph, separators=(",", ":")).replace("</", "<\\/")
    return f"""# Engineering explorer

Keep the engineering context visible while inspecting one object. The object
details, backlinks and one-hop context below are generated from the same
needs.json used by traceability validation.

<div class="eng-workspace" data-eng-explorer>
  <section class="eng-context">
    <h2>Reference objects</h2>
    <div class="eng-object-picker">
      {"".join(chips)}
    </div>
    <h2>Clickable architecture slice</h2>
    {render_architecture_svg(graph)}
    <p>
      The diagram labels and relationships are resolved from engineering object
      IDs. Click a node without leaving this architecture context.
    </p>
  </section>
  <aside class="eng-detail" data-eng-detail aria-live="polite">
    Select an engineering object.
  </aside>
</div>

<script id="eng-graph-data" type="application/json">{graph_json}</script>
"""


def generate(needs_json: Path, candidate_dir: Path, output_dir: Path) -> None:
    needs = load_needs(needs_json)
    graph = normalize_needs(needs)

    if REFERENCE_FOCUS_ROOT not in graph["objects"]:
        raise PortalError(f"reference focus root is absent: {REFERENCE_FOCUS_ROOT}")

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    pages_dir = candidate_dir / "pages"
    assets_dir = candidate_dir / "assets"
    shutil.copytree(pages_dir, output_dir, dirs_exist_ok=True)
    shutil.copytree(assets_dir, output_dir / "assets", dirs_exist_ok=True)

    objects_dir = output_dir / "objects"
    objects_dir.mkdir(parents=True)
    (objects_dir / "index.md").write_text(
        render_object_index(graph), encoding="utf-8"
    )
    for object_id, obj in graph["objects"].items():
        (objects_dir / f"{object_id}.md").write_text(
            render_object_page(obj, graph),
            encoding="utf-8",
        )

    (output_dir / "explorer.md").write_text(
        render_explorer(graph), encoding="utf-8"
    )

    assets_out = output_dir / "assets"
    (assets_out / "engineering-graph.json").write_text(
        json.dumps(graph, indent=2) + "\n",
        encoding="utf-8",
    )
    (assets_out / f"focus-{REFERENCE_FOCUS_ROOT}.json").write_text(
        json.dumps(graph["focus_depth_1"][REFERENCE_FOCUS_ROOT], indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"generated Material portal source: {len(graph['objects'])} objects "
        f"into {output_dir}"
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    generate_parser = sub.add_parser("generate")
    generate_parser.add_argument("needs_json")
    generate_parser.add_argument("candidate_dir")
    generate_parser.add_argument("output_dir")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "generate":
        generate(
            Path(args.needs_json),
            Path(args.candidate_dir),
            Path(args.output_dir),
        )
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
