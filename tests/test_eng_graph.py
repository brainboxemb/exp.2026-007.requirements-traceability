import copy
import json
import unittest
from pathlib import Path

from src.eng_graph import GraphError, focus_graph, normalize_graph, validate_graph


FIXTURE = Path("fixtures/reference/event-timing-graph.json")


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def object_by_id(data, object_id):
    return next(obj for obj in data["objects"] if obj["id"] == object_id)


class EngineeringGraphTests(unittest.TestCase):
    def test_graph_01_valid_reference_graph(self):
        data = load_fixture()
        by_id = validate_graph(data)
        self.assertEqual(8, len(by_id))

    def test_graph_02_duplicate_ids_are_rejected(self):
        data = load_fixture()
        data["objects"].append(copy.deepcopy(data["objects"][0]))
        with self.assertRaisesRegex(GraphError, "duplicate engineering id: UC-001"):
            validate_graph(data)

    def test_graph_03_unknown_targets_are_rejected(self):
        data = load_fixture()
        requirement = object_by_id(data, "SI01-REQ-020")
        requirement["relations"][0]["target"] = "UC-404"
        with self.assertRaisesRegex(GraphError, "targets unknown id 'UC-404'"):
            validate_graph(data)

    def test_graph_04_invalid_type_combination_is_rejected(self):
        data = load_fixture()
        use_case = object_by_id(data, "UC-001")
        use_case["relations"].append(
            {"type": "verified_by", "target": "VC-ST1-001"}
        )
        with self.assertRaisesRegex(GraphError, "is not allowed from 'use-case'"):
            validate_graph(data)

    def test_graph_05_requirement_coverage_is_checked(self):
        data = load_fixture()
        requirement = object_by_id(data, "SI01-REQ-003")
        requirement["relations"] = [
            relation
            for relation in requirement["relations"]
            if relation["type"] != "source"
        ]
        with self.assertRaisesRegex(GraphError, "requirement has no upstream source"):
            validate_graph(data)

    def test_graph_06_backlinks_are_generated(self):
        normalized = normalize_graph(load_fixture())
        use_case = object_by_id(normalized, "UC-001")
        incoming = {
            (relation["type"], relation["source"])
            for relation in use_case["incoming"]
        }
        self.assertIn(("source", "SI01-REQ-003"), incoming)
        self.assertIn(("source", "SI01-REQ-020"), incoming)

    def test_graph_07_focused_traversal_is_bounded(self):
        normalized = normalize_graph(load_fixture())
        focused = focus_graph(
            normalized,
            "SI01-REQ-020",
            depth=1,
            direction="both",
        )
        ids = {obj["id"] for obj in focused["objects"]}
        self.assertEqual(
            {
                "SI01-REQ-020",
                "UC-001",
                "UC-008",
                "IF03-REQ-004",
                "TimingNode",
                "VC-ST1-001",
            },
            ids,
        )
        self.assertNotIn("CommandHandler", ids)

    def test_graph_08_export_retains_provenance_and_generator(self):
        normalized = normalize_graph(load_fixture())
        self.assertEqual(
            "brainboxemb/2026-010-01.meta.event-timing-software",
            normalized["provenance"]["source_repository"],
        )
        self.assertEqual(
            "exp-007-minimal-engineering-graph",
            normalized["generator"]["name"],
        )


if __name__ == "__main__":
    unittest.main()
