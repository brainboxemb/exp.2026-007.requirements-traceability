import json
import sys
from pathlib import Path


EXPECTED_IDS = {
    "UC-001",
    "UC-008",
    "SI01-REQ-003",
    "SI01-REQ-020",
    "IF03-REQ-004",
    "TimingNode",
    "CommandHandler",
    "VC-ST1-001",
}

EXPECTED_FOCUS = {
    "SI01-REQ-020",
    "UC-001",
    "UC-008",
    "IF03-REQ-004",
    "TimingNode",
    "VC-ST1-001",
}


def require(path: Path) -> Path:
    if not path.exists():
        raise AssertionError(f"missing expected portal output: {path}")
    return path


def main(root: str) -> int:
    root_path = Path(root)
    docs = root_path / "docs"
    site = root_path / "site"

    graph = json.loads(
        require(docs / "assets" / "engineering-graph.json").read_text(
            encoding="utf-8"
        )
    )
    actual_ids = set(graph["objects"])
    if actual_ids != EXPECTED_IDS:
        raise AssertionError(
            f"portal object ids differ: expected={sorted(EXPECTED_IDS)} "
            f"actual={sorted(actual_ids)}"
        )

    focus = graph["focus_depth_1"]["SI01-REQ-020"]
    focus_ids = set(focus["objects"])
    if focus_ids != EXPECTED_FOCUS:
        raise AssertionError(
            f"portal one-hop focus differs: expected={sorted(EXPECTED_FOCUS)} "
            f"actual={sorted(focus_ids)}"
        )
    if "CommandHandler" in focus_ids or "SI01-REQ-003" in focus_ids:
        raise AssertionError("portal depth-1 focus contains a second-hop object")

    for object_id in EXPECTED_IDS:
        page = require(site / "objects" / object_id / "index.html")
        content = page.read_text(encoding="utf-8")
        if object_id not in content:
            raise AssertionError(f"{object_id}: generated object page lost its id")

    requirement_page = (
        site / "objects" / "SI01-REQ-020" / "index.html"
    ).read_text(encoding="utf-8")
    for related_id in (
        "UC-001",
        "UC-008",
        "IF03-REQ-004",
        "TimingNode",
        "VC-ST1-001",
    ):
        if related_id not in requirement_page:
            raise AssertionError(
                f"SI01-REQ-020 page is missing relation context {related_id}"
            )

    explorer = require(site / "explorer" / "index.html").read_text(
        encoding="utf-8"
    )
    for marker in (
        'data-eng-explorer',
        'data-eng-detail',
        'data-object-id="TimingNode"',
        'data-object-id="CommandHandler"',
        'data-object-id="IF03-REQ-004"',
        'id="eng-graph-data"',
    ):
        if marker not in explorer:
            raise AssertionError(f"explorer is missing marker: {marker}")

    book = require(site / "book" / "index.html").read_text(encoding="utf-8")
    if "architecture-book.md" not in book:
        raise AssertionError("Book view does not link the architecture book")

    search = json.loads(
        require(site / "search" / "search_index.json").read_text(
            encoding="utf-8"
        )
    )
    search_text = json.dumps(search)
    for object_id in EXPECTED_IDS:
        if object_id not in search_text:
            raise AssertionError(f"search index does not contain {object_id}")

    require(site / "assets" / "javascripts" / "explorer.js")
    require(site / "assets" / "stylesheets" / "explorer.css")

    print(
        "verified Material portal: 8 object pages, searchable static site, "
        "clickable workspace markers and exact one-hop graph data"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
