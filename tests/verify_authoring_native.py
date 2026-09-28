import json
import sys
from pathlib import Path


EXPECTED_IDS = {
    "UC-001",
    "UC-008",
    "UC-014",
    "SAD-TESTABILITY",
    "SVP-ST-1",
    "TimingNode",
    "CommandHandler",
    "Conductor",
    "RemoteApi",
    "SI01-REQ-003",
    "SI01-REQ-020",
    "SI01-REQ-021",
    "SI01-REQ-022",
    "SI01-REQ-030",
    "SI01-REQ-031",
    "IF03-REQ-001",
    "IF03-REQ-002",
    "IF03-REQ-004",
    "VC-ST1-001",
}


def main(path: str) -> int:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    current = data["current_version"]
    needs = data["versions"][current]["needs"]

    actual = set(needs)
    if actual != EXPECTED_IDS:
        raise AssertionError(
            f"native authoring ids differ: expected={sorted(EXPECTED_IDS)} "
            f"actual={sorted(actual)}"
        )

    if needs["SAD-TESTABILITY"]["type"] != "docsec":
        raise AssertionError("SAD-TESTABILITY is not represented as document section")
    if needs["SVP-ST-1"]["type"] != "docsec":
        raise AssertionError("SVP-ST-1 is not represented as document section")

    req030 = needs["SI01-REQ-030"]
    if req030["derived_from"] != ["SAD-TESTABILITY"]:
        raise AssertionError("SI01-REQ-030 lost its real SAD upstream source")

    req031_sources = set(needs["SI01-REQ-031"]["derived_from"])
    if req031_sources != {"SAD-TESTABILITY", "SVP-ST-1"}:
        raise AssertionError("SI01-REQ-031 lost SAD/SVP upstream sources")

    if set(needs["SI01-REQ-020"]["derived_from"]) != {"UC-001", "UC-008"}:
        raise AssertionError("SI01-REQ-020 source links differ")

    if set(needs["IF03-REQ-004"]["derived_from"]) != {
        "SI01-REQ-020",
        "SI01-REQ-021",
        "SI01-REQ-022",
    }:
        raise AssertionError("IF03-REQ-004 upstream requirement links differ")

    if "SI01-REQ-003" not in needs["UC-014"]["derived_from_back"]:
        raise AssertionError("UC-014 did not receive generated requirement backlink")

    print(
        "verified native MyST authoring: 19 objects, real use-case/document-section "
        "sources, allocations, verification and generated backlinks"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
