import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


EXPECTED_NODE_IDS = {
    "SI01-REQ-020",
    "UC-001",
    "UC-008",
    "IF03-REQ-004",
    "TimingNode",
    "VC-ST1-001",
}


def read_nodes(html_dir: Path) -> set[str]:
    images = sorted((html_dir / "_images").glob("needflow-*.svg"))
    if len(images) != 1:
        raise AssertionError(
            f"expected exactly one generated needflow SVG, found {len(images)}"
        )

    root = ET.parse(images[0]).getroot()
    nodes = set()

    for element in root.iter():
        if not element.tag.endswith("g"):
            continue
        if element.attrib.get("class") != "node":
            continue
        for child in element:
            if child.tag.endswith("title") and child.text:
                nodes.add(child.text)
                break

    return nodes


def main(html_dir: str, output: str) -> int:
    actual = read_nodes(Path(html_dir))
    missing = sorted(EXPECTED_NODE_IDS - actual)
    extra = sorted(actual - EXPECTED_NODE_IDS)

    report = {
        "root": "SI01-REQ-020",
        "requested_depth": 1,
        "expected_shortest_path_nodes": sorted(EXPECTED_NODE_IDS),
        "needflow_nodes": sorted(actual),
        "missing": missing,
        "extra": extra,
        "matches_shortest_path_semantics": not missing and not extra,
        "observation": (
            "Sphinx-Needs needflow root_depth uses depth-first traversal where "
            "first visit wins; this can omit a directly connected node when the "
            "same node is reached first through a deeper path."
        ),
    }

    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if report["matches_shortest_path_semantics"]:
        print("built-in needflow currently matches shortest-path depth semantics")
    else:
        print(
            "recorded built-in needflow depth limitation: "
            f"missing={missing} extra={extra}"
        )

    # This inspection step records candidate behaviour. It deliberately does
    # not redefine Experiment 007's focused-graph semantics to match needflow.
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
