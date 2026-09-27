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


def main(html_dir: str) -> int:
    images = sorted((Path(html_dir) / "_images").glob("needflow-*.svg"))
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

    if nodes != EXPECTED_NODE_IDS:
        raise AssertionError(
            f"focused graph differs from one-hop baseline: "
            f"expected={sorted(EXPECTED_NODE_IDS)} actual={sorted(nodes)}"
        )

    if "CommandHandler" in nodes or "SI01-REQ-003" in nodes:
        raise AssertionError("focused graph leaked a second-hop/unrelated object")

    print(
        "verified focused Sphinx-Needs graph: "
        + ", ".join(sorted(nodes))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
