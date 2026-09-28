"""Compare current compact authoring with native MyST/Sphinx-Needs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ANCHOR_RE = re.compile(r'^<a id="([^"]+)"></a>$')
ENG_RE = re.compile(r'^<!-- eng (\{.*\}) -->$')
ENG_REL_RE = re.compile(r'^<!-- eng-rel (\{.*\}) -->$')
OBJECT_ID_RE = re.compile(r'^\s*object_id:\s*([A-Za-z0-9_-]+)\s*$')
RELATIONS = ("derived_from", "satisfies", "verifies")
TYPE_MAP = {
    "uc": "use-case",
    "req": "requirement",
    "ifreq": "interface-requirement",
    "arch": "architecture-element",
    "vc": "verification-case",
}
EXPECTED_IDS = {
    "UC-001", "UC-008", "UC-014",
    "SI01-REQ-003", "SI01-REQ-020", "SI01-REQ-021", "SI01-REQ-022",
    "SI01-REQ-030", "SI01-REQ-031",
    "IF03-REQ-001", "IF03-REQ-002", "IF03-REQ-004",
    "TimingNode", "CommandHandler", "Conductor", "RemoteApi", "VC-ST1-001",
}


class AuthoringV2Error(ValueError):
    pass


def _relations(owner, metadata):
    rows = []
    relation_map = metadata.get("relations", {})
    if not isinstance(relation_map, dict):
        raise AuthoringV2Error(f"{owner}: relations must be an object")
    for relation_type, targets in relation_map.items():
        if relation_type not in RELATIONS:
            raise AuthoringV2Error(f"{owner}: unsupported relation {relation_type}")
        if not isinstance(targets, list) or not all(isinstance(x, str) and x for x in targets):
            raise AuthoringV2Error(f"{owner}: {relation_type} must be a list of ids")
        rows.extend((owner, relation_type, target) for target in targets)
    return rows


def _normalize(objects, relations):
    if set(objects) != EXPECTED_IDS:
        raise AuthoringV2Error(f"object ids differ: {sorted(objects)}")
    allowed = {
        "derived_from": {
            ("requirement", "use-case"),
            ("requirement", "requirement"),
            ("interface-requirement", "requirement"),
        },
        "satisfies": {
            ("architecture-element", "requirement"),
            ("architecture-element", "interface-requirement"),
        },
        "verifies": {
            ("verification-case", "requirement"),
            ("verification-case", "interface-requirement"),
        },
    }
    normalized = []
    for owner, relation_type, target in relations:
        if target not in objects:
            raise AuthoringV2Error(f"{owner}: unknown {relation_type} target {target}")
        pair = (objects[owner], objects[target])
        if pair not in allowed[relation_type]:
            raise AuthoringV2Error(
                f"{owner}: {relation_type} disallows {pair[0]} -> {pair[1]}"
            )
        normalized.append({"from": owner, "type": relation_type, "to": target})
    normalized.sort(key=lambda item: (item["from"], item["type"], item["to"]))
    if len(normalized) != 34:
        raise AuthoringV2Error(f"expected 34 relations, got {len(normalized)}")
    return {
        "objects": [{"id": key, "type": objects[key]} for key in sorted(objects)],
        "relations": normalized,
    }


def compact_signature(markdown: Path, diagram: Path):
    objects = {}
    relations = []
    extensions = []
    current_anchor = None
    for line_number, line in enumerate(
        markdown.read_text(encoding="utf-8").splitlines(), 1
    ):
        stripped = line.strip()
        match = ANCHOR_RE.fullmatch(stripped)
        if match:
            current_anchor = match.group(1)
            continue
        match = ENG_RE.fullmatch(stripped)
        if match:
            if current_anchor is None:
                raise AuthoringV2Error(f"{markdown}:{line_number}: eng without anchor")
            metadata = json.loads(match.group(1))
            objects[current_anchor] = metadata["type"]
            relations.extend(_relations(current_anchor, metadata))
            continue
        match = ENG_REL_RE.fullmatch(stripped)
        if match:
            metadata = json.loads(match.group(1))
            extensions.append((metadata["id"], metadata))

    for line in diagram.read_text(encoding="utf-8").splitlines():
        match = OBJECT_ID_RE.fullmatch(line)
        if match:
            objects[match.group(1)] = "architecture-element"

    for owner, metadata in extensions:
        if owner not in objects:
            raise AuthoringV2Error(f"eng-rel owner does not exist: {owner}")
        relations.extend(_relations(owner, metadata))

    return _normalize(objects, relations)


def needs_signature(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    current = data["current_version"]
    needs = data["versions"][current]["needs"]
    objects = {}
    relations = []
    for object_id, need in needs.items():
        objects[object_id] = TYPE_MAP[need["type"]]
        for relation_type in RELATIONS:
            relations.extend(
                (object_id, relation_type, target)
                for target in need.get(relation_type, [])
            )

    result = _normalize(objects, relations)

    if "TimingNode" not in needs["SI01-REQ-020"].get("satisfies_back", []):
        raise AuthoringV2Error("missing generated TimingNode satisfies backlink")
    if "VC-ST1-001" not in needs["SI01-REQ-020"].get("verifies_back", []):
        raise AuthoringV2Error("missing generated VC-ST1-001 verifies backlink")
    if "SI01-REQ-020" not in needs["UC-001"].get("derived_from_back", []):
        raise AuthoringV2Error("missing generated UC-001 derived_from backlink")

    return result


def metrics(compact: Path, native: Path):
    compact_lines = compact.read_text(encoding="utf-8").splitlines()
    native_lines = native.read_text(encoding="utf-8").splitlines()
    fence = chr(96) * 3 + "{"
    return {
        "compact": {
            "total_lines": len(compact_lines),
            "explicit_anchor_lines": sum(
                bool(ANCHOR_RE.fullmatch(line.strip())) for line in compact_lines
            ),
            "hidden_metadata_lines": sum(
                bool(
                    ENG_RE.fullmatch(line.strip())
                    or ENG_REL_RE.fullmatch(line.strip())
                )
                for line in compact_lines
            ),
        },
        "native_myst": {
            "total_lines": len(native_lines),
            "directive_open_lines": sum(
                line.startswith(fence) for line in native_lines
            ),
            "id_option_lines": sum(line.startswith(":id:") for line in native_lines),
            "relation_option_lines": sum(
                any(line.startswith(f":{relation}:") for relation in RELATIONS)
                for line in native_lines
            ),
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("compact")
    parser.add_argument("diagram")
    parser.add_argument("native_needs")
    parser.add_argument("native_source")
    parser.add_argument("output")
    args = parser.parse_args(argv)

    compact_graph = compact_signature(Path(args.compact), Path(args.diagram))
    native_graph = needs_signature(Path(args.native_needs))
    if compact_graph != native_graph:
        raise AuthoringV2Error("compact and native MyST semantics differ")

    result = {
        "schema_version": 1,
        "object_count": 17,
        "relation_count": 34,
        "semantic_match": True,
        "metrics": metrics(Path(args.compact), Path(args.native_source)),
        "graph": compact_graph,
    }
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("authoring v2: 17 objects / 34 relations / semantics equal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
