import json
import tempfile
import unittest
from pathlib import Path

from src.authoring import (
    AuthoringError,
    authoring_stats,
    extract_markdown,
    semantic_signature,
)
from src.eng_graph import normalize_graph


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "authoring"
REFERENCE = FIXTURE / "reference.json"


class AuthoringFixtureTest(unittest.TestCase):
    def compact(self):
        return normalize_graph(
            extract_markdown(
                FIXTURE / "compact-metadata.md",
                REFERENCE,
                mode="compact",
            )
        )

    def sidecar(self):
        return normalize_graph(
            extract_markdown(
                FIXTURE / "sidecar-content.md",
                REFERENCE,
                mode="sidecar",
                sidecar_path=FIXTURE / "sidecar-metadata.json",
            )
        )

    def test_compact_and_sidecar_have_identical_semantics(self):
        compact = self.compact()
        sidecar = self.sidecar()

        self.assertEqual(19, len(compact["objects"]))
        self.assertEqual(
            semantic_signature(compact),
            semantic_signature(sidecar),
        )

    def test_real_source_document_sections_are_valid_upstream_sources(self):
        objects = {obj["id"]: obj for obj in self.compact()["objects"]}

        req030 = objects["SI01-REQ-030"]
        self.assertIn(
            {"type": "source", "target": "SAD-TESTABILITY"},
            req030["relations"],
        )

        req031 = objects["SI01-REQ-031"]
        self.assertIn(
            {"type": "source", "target": "SAD-TESTABILITY"},
            req031["relations"],
        )
        self.assertIn(
            {"type": "source", "target": "SVP-ST-1"},
            req031["relations"],
        )

    def test_use_cases_receive_generated_requirement_backlinks(self):
        objects = {obj["id"]: obj for obj in self.compact()["objects"]}

        uc001_sources = {
            item["source"]
            for item in objects["UC-001"]["incoming"]
            if item["type"] == "source"
        }
        self.assertEqual(
            {"SI01-REQ-003", "SI01-REQ-020", "SI01-REQ-021"},
            uc001_sources,
        )

        uc014_sources = {
            item["source"]
            for item in objects["UC-014"]["incoming"]
            if item["type"] == "source"
        }
        self.assertEqual({"SI01-REQ-003"}, uc014_sources)

    def test_requirement_objects_have_explicit_stable_anchors(self):
        objects = {obj["id"]: obj for obj in self.compact()["objects"]}
        for object_id in (
            "SI01-REQ-003",
            "SI01-REQ-020",
            "SI01-REQ-021",
            "SI01-REQ-022",
            "SI01-REQ-030",
            "SI01-REQ-031",
            "IF03-REQ-001",
            "IF03-REQ-002",
            "IF03-REQ-004",
        ):
            self.assertEqual(object_id, objects[object_id]["source"]["anchor"])

    def test_unknown_target_reports_the_source_fixture(self):
        original = (FIXTURE / "compact-metadata.md").read_text(encoding="utf-8")
        broken = original.replace(
            '"allocated_to":["TimingNode"]',
            '"allocated_to":["MissingTimingNode"]',
            1,
        )

        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "broken.md"
            path.write_text(broken, encoding="utf-8")
            with self.assertRaisesRegex(
                AuthoringError,
                r"broken\.md: SI01-REQ-003: relation 'allocated_to' targets unknown id",
            ):
                extract_markdown(path, REFERENCE, mode="compact")

    def test_authoring_cost_is_measurable(self):
        compact = authoring_stats(FIXTURE / "compact-metadata.md", mode="compact")
        sidecar = authoring_stats(FIXTURE / "sidecar-content.md", mode="sidecar")

        self.assertEqual(19, compact["object_count"])
        self.assertEqual(19, sidecar["object_count"])
        self.assertGreater(compact["metadata_lines"], 19)
        self.assertEqual(9, compact["explicit_anchor_lines"])
        self.assertEqual(9, sidecar["explicit_anchor_lines"])


if __name__ == "__main__":
    unittest.main()
