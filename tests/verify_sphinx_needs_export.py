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


def main(path: str) -> int:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    current_version = data["current_version"]
    version_data = data["versions"][current_version]
    needs = version_data["needs"]

    actual_ids = set(needs)
    if actual_ids != EXPECTED_IDS:
        raise AssertionError(
            f"unexpected needs ids: expected={sorted(EXPECTED_IDS)} "
            f"actual={sorted(actual_ids)}"
        )

    status_req = needs["SI01-REQ-020"]
    if set(status_req["derived_from"]) != {"UC-001", "UC-008"}:
        raise AssertionError("SI01-REQ-020 derived_from links differ from baseline")
    if set(status_req["allocated_to"]) != {"IF03-REQ-004", "TimingNode"}:
        raise AssertionError("SI01-REQ-020 allocations differ from baseline")
    if set(status_req["verified_by"]) != {"VC-ST1-001"}:
        raise AssertionError("SI01-REQ-020 verification differs from baseline")

    uc1 = needs["UC-001"]
    if not {"SI01-REQ-003", "SI01-REQ-020"}.issubset(
        set(uc1["derived_from_back"])
    ):
        raise AssertionError("generated derived_from backlinks are incomplete")

    ifreq = needs["IF03-REQ-004"]
    if "SI01-REQ-020" not in set(ifreq["allocated_to_back"]):
        raise AssertionError("generated allocation backlink is missing")

    verification = needs["VC-ST1-001"]
    if not {"SI01-REQ-003", "SI01-REQ-020", "IF03-REQ-004"}.issubset(
        set(verification["verified_by_back"])
    ):
        raise AssertionError("generated verification backlinks are incomplete")

    if not status_req.get("origin_url") or not status_req.get("origin_anchor"):
        raise AssertionError("authoritative source metadata missing from export")

    print(
        "verified Sphinx-Needs export: "
        f"{len(needs)} objects, typed links and generated backlinks"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
