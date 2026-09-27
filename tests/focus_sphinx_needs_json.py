import json
import sys
from collections import deque
from pathlib import Path


DEFAULT_LINK_TYPES = (
    "derived_from",
    "allocated_to",
    "verified_by",
    "related_to",
)


def load_needs(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    current = data["current_version"]
    return data["versions"][current]["needs"]


def focus(
    needs: dict,
    root_id: str,
    *,
    depth: int,
    direction: str,
    link_types: tuple[str, ...] = DEFAULT_LINK_TYPES,
) -> dict:
    if root_id not in needs:
        raise KeyError(f"unknown root id: {root_id}")
    if direction not in {"incoming", "outgoing", "both"}:
        raise ValueError("direction must be incoming, outgoing or both")
    if depth < 0:
        raise ValueError("depth must be >= 0")

    selected = {root_id}
    edges = set()
    queue = deque([(root_id, 0)])
    visited_depth = {root_id: 0}

    while queue:
        current_id, current_depth = queue.popleft()
        if current_depth >= depth:
            continue

        current = needs[current_id]
        neighbors = []

        if direction in {"outgoing", "both"}:
            for link_type in link_types:
                for target in current.get(link_type, []):
                    if target in needs:
                        neighbors.append((current_id, link_type, target))

        if direction in {"incoming", "both"}:
            for link_type in link_types:
                back_field = f"{link_type}_back"
                for source in current.get(back_field, []):
                    if source in needs:
                        neighbors.append((source, link_type, current_id))

        for source, link_type, target in neighbors:
            edges.add((source, link_type, target))
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
        "link_types": list(link_types),
        "objects": [
            {
                "id": object_id,
                "type": needs[object_id]["type"],
                "title": needs[object_id]["title"],
                "origin_url": needs[object_id].get("origin_url"),
                "origin_anchor": needs[object_id].get("origin_anchor"),
            }
            for object_id in sorted(selected)
        ],
        "edges": [
            {"source": source, "type": link_type, "target": target}
            for source, link_type, target in sorted(edges)
        ],
    }


def main(needs_json: str, output: str) -> int:
    needs = load_needs(Path(needs_json))
    result = focus(
        needs,
        "SI01-REQ-020",
        depth=1,
        direction="both",
    )

    expected = {
        "SI01-REQ-020",
        "UC-001",
        "UC-008",
        "IF03-REQ-004",
        "TimingNode",
        "VC-ST1-001",
    }
    actual = {obj["id"] for obj in result["objects"]}

    if actual != expected:
        raise AssertionError(
            f"focused needs.json query differs from baseline: "
            f"expected={sorted(expected)} actual={sorted(actual)}"
        )
    if "CommandHandler" in actual or "SI01-REQ-003" in actual:
        raise AssertionError("focused query leaked a second-hop/unrelated object")

    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("verified exact one-hop focused graph from needs.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
