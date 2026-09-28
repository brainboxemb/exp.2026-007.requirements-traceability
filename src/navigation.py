"""Generate the Step 06 clickable real-architecture review site."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import markdown
import yaml

from src.authoring import extract_markdown
from src.eng_graph import normalize_graph


SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

USE_CASE_HEADING = re.compile(r"^##\s+(UC-\d+)\s+—\s+(.+?)\s*$")
BOLD_OBJECT = re.compile(r"^\*\*((?:SI01|IF03)-REQ-\d+)\s+—\s+(.+?)\*\*\s*$")
VC_HEADING = re.compile(r"^###\s+(VC-[A-Za-z0-9-]+)\s+—\s+(.+?)\s*$")
NODE_ID_LINE = re.compile(r"^- id:\s+([A-Za-z0-9_.-]+)\s*$")


class NavigationError(ValueError):
    """Raised when navigation fixture data is inconsistent."""


def github_heading_slug(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    return value.replace(" ", "-")


def github_blob_url(repo: str, revision: str, path: str, fragment: str = "") -> str:
    url = f"https://github.com/{repo}/blob/{revision}/{path}"
    return url + fragment


def _line_url(repo: str, revision: str, path: str, start: int, end: int | None = None) -> str:
    fragment = f"#L{start}" if end is None or end == start else f"#L{start}-L{end}"
    return github_blob_url(repo, revision, path, fragment)


def parse_markdown_objects(
    path: Path,
    *,
    source_repo: str,
    source_revision: str,
    source_path: str,
) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    markers: list[dict[str, Any]] = []

    for index, line in enumerate(lines):
        uc = USE_CASE_HEADING.match(line)
        if uc:
            markers.append(
                {
                    "id": uc.group(1),
                    "title": uc.group(2),
                    "type": "use-case",
                    "line": index,
                    "heading": line.removeprefix("## ").strip(),
                    "stable_anchor": True,
                }
            )
            continue

        req = BOLD_OBJECT.match(line)
        if req:
            markers.append(
                {
                    "id": req.group(1),
                    "title": req.group(2),
                    "type": "requirement" if req.group(1).startswith("SI01") else "interface-requirement",
                    "line": index,
                    "stable_anchor": False,
                }
            )
            continue

        vc = VC_HEADING.match(line)
        if vc:
            markers.append(
                {
                    "id": vc.group(1),
                    "title": vc.group(2),
                    "type": "verification-case",
                    "line": index,
                    "heading": line.removeprefix("### ").strip(),
                    "stable_anchor": True,
                }
            )

    result: dict[str, dict[str, Any]] = {}
    rendered: dict[str, str] = {}

    for position, marker in enumerate(markers):
        start = marker["line"]
        end = markers[position + 1]["line"] - 1 if position + 1 < len(markers) else len(lines) - 1

        if marker["stable_anchor"]:
            anchor = github_heading_slug(marker["heading"])
            url = github_blob_url(source_repo, source_revision, source_path, f"#{anchor}")
        else:
            anchor = None
            url = _line_url(source_repo, source_revision, source_path, start + 1, min(end + 1, start + 20))

        result[marker["id"]] = {
            "repository": source_repo,
            "revision": source_revision,
            "path": source_path,
            "line": start + 1,
            "anchor": anchor,
            "stable_anchor": marker["stable_anchor"],
            "url": url,
        }

        if marker["type"] == "use-case":
            section = "\n".join(lines[start : end + 1])
            rendered[marker["id"]] = markdown.markdown(
                section,
                extensions=["tables", "fenced_code"],
            )

    return result, rendered


def parse_diagram(
    path: Path,
    *,
    source_repo: str,
    source_revision: str,
    source_path: str,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise NavigationError("diagram root must be an object")

    source_lines = path.read_text(encoding="utf-8").splitlines()
    original_line = 0
    node_source_line: dict[str, int] = {}
    for line in source_lines:
        if re.match(r"^\s+object_id:\s+", line):
            continue
        original_line += 1
        node = NODE_ID_LINE.match(line)
        if node:
            node_source_line[node.group(1)] = original_line

    identity: dict[str, dict[str, Any]] = {}
    for node in data.get("nodes", []):
        object_id = node.get("object_id")
        if not object_id:
            continue
        if object_id in identity:
            raise NavigationError(f"duplicate diagram object_id: {object_id}")
        node_id = node["id"]
        identity[object_id] = {
            "node_id": node_id,
            "label": node["label"],
            "layout": node["layout"],
            "source": {
                "repository": source_repo,
                "revision": source_revision,
                "path": source_path,
                "line": node_source_line[node_id],
                "stable_anchor": False,
                "anchor": None,
                "url": _line_url(
                    source_repo,
                    source_revision,
                    source_path,
                    node_source_line[node_id],
                    node_source_line[node_id] + 8,
                ),
            },
        }

    return data, identity


def add_svg_identity_overlays(svg_path: Path, identities: dict[str, dict[str, Any]]) -> str:
    tree = ET.parse(svg_path)
    root = tree.getroot()
    overlays = ET.SubElement(root, f"{{{SVG_NS}}}g", {"id": "engineering-identity-overlays"})

    for object_id, entry in identities.items():
        r = entry["layout"]
        group = ET.SubElement(
            overlays,
            f"{{{SVG_NS}}}g",
            {
                "class": "engineering-hit",
                "data-engineering-id": object_id,
                "role": "button",
                "tabindex": "0",
                "aria-label": f"Open {object_id}",
            },
        )
        title = ET.SubElement(group, f"{{{SVG_NS}}}title")
        title.text = f"Open {entry['label']} ({object_id})"
        ET.SubElement(
            group,
            f"{{{SVG_NS}}}rect",
            {
                "x": str(r["x"]),
                "y": str(r["y"]),
                "width": str(r["w"]),
                "height": str(r["h"]),
                "rx": "8",
                "ry": "8",
                "class": "engineering-hit-target",
            },
        )

    return ET.tostring(root, encoding="unicode")


def graph_index(normalized: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {obj["id"]: obj for obj in normalized["objects"]}


def related_requirements(objects: dict[str, dict[str, Any]], architecture_id: str) -> list[str]:
    result = []
    for obj in objects.values():
        if obj["type"] not in {"requirement", "interface-requirement"}:
            continue
        if any(
            rel["type"] == "allocated_to" and rel["target"] == architecture_id
            for rel in obj.get("relations", [])
        ):
            result.append(obj["id"])
    return sorted(result)


def use_cases_for_architecture(objects: dict[str, dict[str, Any]], architecture_id: str) -> list[str]:
    result: set[str] = set()
    for req_id in related_requirements(objects, architecture_id):
        req = objects[req_id]
        for rel in req.get("relations", []):
            if rel["type"] == "source" and rel["target"] in objects:
                target = objects[rel["target"]]
                if target["type"] == "use-case":
                    result.add(target["id"])
    return sorted(result)


def architecture_for_use_case(objects: dict[str, dict[str, Any]], use_case_id: str) -> list[str]:
    result: set[str] = set()
    for incoming in objects[use_case_id].get("incoming", []):
        if incoming["type"] != "source":
            continue
        req = objects[incoming["source"]]
        for rel in req.get("relations", []):
            if rel["type"] != "allocated_to" or rel["target"] not in objects:
                continue
            target = objects[rel["target"]]
            if target["type"] == "architecture-element":
                result.add(target["id"])
    return sorted(result)


def verification_for_requirements(objects: dict[str, dict[str, Any]], requirement_ids: list[str]) -> list[str]:
    result: set[str] = set()
    for req_id in requirement_ids:
        for rel in objects[req_id].get("relations", []):
            if rel["type"] == "verified_by":
                result.add(rel["target"])
    return sorted(result)


def build_navigation_model(
    *,
    compact_markdown: Path,
    compact_reference: Path,
    diagram_yaml: Path,
    base_svg: Path,
    fixture_reference: Path,
    source_dir: Path,
) -> tuple[dict[str, Any], str]:
    authored = extract_markdown(
        compact_markdown,
        compact_reference,
        mode="compact",
    )
    normalized = normalize_graph(authored)
    objects = graph_index(normalized)

    reference = json.loads(fixture_reference.read_text(encoding="utf-8"))
    source_repo = reference["source_repository"]
    source_revision = reference["source_revision"]

    source_index: dict[str, dict[str, Any]] = {}
    use_case_html: dict[str, str] = {}

    for filename, source_path in (
        ("04-UC-system-use-cases.md", "docs/04-UC-system-use-cases.md"),
        ("20-01-SRD-timing-application-requirements.md", "docs/20-01-SRD-timing-application-requirements.md"),
        ("40-01-IDD-application-control-status.md", "docs/40-01-IDD-application-control-status.md"),
    ):
        index, rendered = parse_markdown_objects(
            source_dir / filename,
            source_repo=source_repo,
            source_revision=source_revision,
            source_path=source_path,
        )
        source_index.update(index)
        use_case_html.update(rendered)

    _, diagram_identity = parse_diagram(
        diagram_yaml,
        source_repo=source_repo,
        source_revision=source_revision,
        source_path=reference["diagram_source"],
    )

    for object_id, entry in diagram_identity.items():
        if object_id not in objects:
            raise NavigationError(
                f"diagram object_id {object_id!r} does not exist in engineering graph"
            )
        if objects[object_id]["type"] != "architecture-element":
            raise NavigationError(
                f"diagram object_id {object_id!r} is not an architecture element"
            )
        source_index[object_id] = entry["source"]

    for object_id in ("UC-001", "UC-008", "UC-014"):
        if object_id not in use_case_html:
            raise NavigationError(f"real use-case narrative missing: {object_id}")

    architecture_context: dict[str, Any] = {}
    for object_id in diagram_identity:
        reqs = related_requirements(objects, object_id)
        architecture_context[object_id] = {
            "requirements": reqs,
            "use_cases": use_cases_for_architecture(objects, object_id),
            "verification": verification_for_requirements(objects, reqs),
        }

    use_case_context: dict[str, Any] = {}
    for object_id in ("UC-001", "UC-008", "UC-014"):
        reqs = sorted(
            incoming["source"]
            for incoming in objects[object_id].get("incoming", [])
            if incoming["type"] == "source"
            and objects[incoming["source"]]["type"] == "requirement"
        )
        use_case_context[object_id] = {
            "requirements": reqs,
            "architecture": architecture_for_use_case(objects, object_id),
            "verification": verification_for_requirements(objects, reqs),
        }

    model = {
        "reference": reference,
        "objects": objects,
        "diagram_identity": diagram_identity,
        "source_index": source_index,
        "use_case_html": use_case_html,
        "architecture_context": architecture_context,
        "use_case_context": use_case_context,
    }
    svg = add_svg_identity_overlays(base_svg, diagram_identity)
    return model, svg


def generate_site(
    output: Path,
    *,
    compact_markdown: Path,
    compact_reference: Path,
    diagram_yaml: Path,
    base_svg: Path,
    fixture_reference: Path,
    source_dir: Path,
    assets_dir: Path,
) -> dict[str, Any]:
    model, svg = build_navigation_model(
        compact_markdown=compact_markdown,
        compact_reference=compact_reference,
        diagram_yaml=diagram_yaml,
        base_svg=base_svg,
        fixture_reference=fixture_reference,
        source_dir=source_dir,
    )

    if output.exists():
        shutil.rmtree(output)
    (output / "assets").mkdir(parents=True)
    shutil.copy2(assets_dir / "navigation.css", output / "assets" / "navigation.css")
    shutil.copy2(assets_dir / "navigation.js", output / "assets" / "navigation.js")

    html_page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Step 06 — Clickable real architecture</title>
  <link rel="stylesheet" href="assets/navigation.css">
</head>
<body>
  <header class="topbar">
    <div>
      <p class="eyebrow">Experiment 007 · Step 06</p>
      <h1>Clickable real architecture + richer use cases</h1>
    </div>
    <p class="hint">Click TimingNode, CommandHandler, Conductor or RemoteApi in the real SI-01 diagram.</p>
  </header>
  <main class="workspace">
    <section class="architecture-pane">
      <div class="pane-head">
        <div>
          <h2>Figure SI01-01</h2>
          <p>Real event-timing layered architecture at <code>{html.escape(model['reference']['source_revision'][:12])}</code></p>
        </div>
        <div class="zoom-controls" aria-label="Diagram zoom">
          <button type="button" data-zoom="0.78">Fit</button>
          <button type="button" data-zoom="1">100%</button>
          <button type="button" data-zoom="1.25">125%</button>
        </div>
      </div>
      <div class="diagram-scroll">
        <div class="diagram-stage" data-zoom-stage>
          {svg}
        </div>
      </div>
    </section>
    <aside class="inspector-pane">
      <div id="inspector" class="inspector">
        <p class="empty">Select an architecture object to explore its use cases, requirements and verification without leaving the diagram.</p>
      </div>
    </aside>
  </main>
  <script id="navigation-data" type="application/json">{html.escape(json.dumps(model))}</script>
  <script src="assets/navigation.js"></script>
</body>
</html>
"""
    (output / "index.html").write_text(html_page, encoding="utf-8")
    (output / "navigation-model.json").write_text(
        json.dumps(model, indent=2) + "\n",
        encoding="utf-8",
    )
    return model


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("output")
    result.add_argument("--compact", default="fixtures/authoring/compact-metadata.md")
    result.add_argument("--compact-reference", default="fixtures/authoring/reference.json")
    result.add_argument("--diagram", default="fixtures/navigation/layered-architecture.yaml")
    result.add_argument("--svg", default="fixtures/navigation/layered-architecture.base.svg")
    result.add_argument("--reference", default="fixtures/navigation/reference.json")
    result.add_argument("--source-dir", default="fixtures/navigation/source")
    result.add_argument("--assets-dir", default="candidates/navigation-review/assets")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    model = generate_site(
        Path(args.output),
        compact_markdown=Path(args.compact),
        compact_reference=Path(args.compact_reference),
        diagram_yaml=Path(args.diagram),
        base_svg=Path(args.svg),
        fixture_reference=Path(args.reference),
        source_dir=Path(args.source_dir),
        assets_dir=Path(args.assets_dir),
    )
    print(
        "generated clickable architecture review: "
        f"{len(model['diagram_identity'])} clickable diagram objects"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
