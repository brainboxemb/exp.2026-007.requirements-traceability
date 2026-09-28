import json
import re
import tempfile
import unittest
from pathlib import Path

try:
    import markdown  # noqa: F401
    import yaml  # noqa: F401
    from src.navigation import (
        NavigationError,
        build_navigation_model,
        generate_site,
    )
    HAS_NAVIGATION_DEPS = True
except ModuleNotFoundError:
    HAS_NAVIGATION_DEPS = False
    NavigationError = ValueError
    build_navigation_model = None
    generate_site = None


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "navigation"
AUTHORING = ROOT / "fixtures" / "authoring"
ASSETS = ROOT / "candidates" / "navigation-review" / "assets"


@unittest.skipUnless(
    HAS_NAVIGATION_DEPS,
    "navigation qualification dependencies are installed only in the Step 06 workflow",
)
class NavigationModelTest(unittest.TestCase):
    def build(self):
        return build_navigation_model(
            compact_markdown=AUTHORING / "compact-metadata.md",
            compact_reference=AUTHORING / "reference.json",
            diagram_yaml=FIXTURE / "layered-architecture.yaml",
            base_svg=FIXTURE / "layered-architecture.base.svg",
            fixture_reference=FIXTURE / "reference.json",
            source_dir=FIXTURE / "source",
        )

    def test_real_diagram_ids_resolve_directly_to_graph_objects(self):
        model, svg = self.build()

        self.assertEqual(
            {"TimingNode", "CommandHandler", "Conductor", "RemoteApi"},
            set(model["diagram_identity"]),
        )
        for object_id in model["diagram_identity"]:
            self.assertEqual(
                "architecture-element",
                model["objects"][object_id]["type"],
            )
            self.assertIn(
                f'data-engineering-id="{object_id}"',
                svg,
            )

    def test_timing_node_reaches_real_use_cases_through_requirements(self):
        model, _ = self.build()
        context = model["architecture_context"]["TimingNode"]

        self.assertIn("UC-001", context["use_cases"])
        self.assertIn("UC-014", context["use_cases"])
        self.assertIn("SI01-REQ-003", context["requirements"])
        self.assertIn("SI01-REQ-020", context["requirements"])
        self.assertIn("VC-ST1-001", context["verification"])

    def test_uc001_keeps_architecture_context(self):
        model, _ = self.build()
        context = model["use_case_context"]["UC-001"]

        self.assertIn("TimingNode", context["architecture"])
        self.assertIn("SI01-REQ-003", context["requirements"])
        self.assertIn("SI01-REQ-020", context["requirements"])
        self.assertIn("VC-ST1-001", context["verification"])
        self.assertIn("Main flow", model["use_case_html"]["UC-001"])

    def test_real_source_links_expose_anchor_limitation(self):
        model, _ = self.build()

        uc = model["source_index"]["UC-001"]
        self.assertTrue(uc["stable_anchor"])
        self.assertIn("#uc-001-", uc["url"])

        req = model["source_index"]["SI01-REQ-020"]
        self.assertFalse(req["stable_anchor"])
        self.assertIn("#L", req["url"])

    def test_unknown_diagram_object_id_fails_close_to_source(self):
        text = (FIXTURE / "layered-architecture.yaml").read_text(encoding="utf-8")
        broken = text.replace(
            "object_id: TimingNode",
            "object_id: MissingTimingNode",
            1,
        )

        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "broken.yaml"
            path.write_text(broken, encoding="utf-8")

            with self.assertRaisesRegex(
                NavigationError,
                r"diagram object_id 'MissingTimingNode' does not exist",
            ):
                build_navigation_model(
                    compact_markdown=AUTHORING / "compact-metadata.md",
                    compact_reference=AUTHORING / "reference.json",
                    diagram_yaml=path,
                    base_svg=FIXTURE / "layered-architecture.base.svg",
                    fixture_reference=FIXTURE / "reference.json",
                    source_dir=FIXTURE / "source",
                )

    def test_generated_page_embeds_parseable_navigation_data(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "site"
            generate_site(
                output,
                compact_markdown=AUTHORING / "compact-metadata.md",
                compact_reference=AUTHORING / "reference.json",
                diagram_yaml=FIXTURE / "layered-architecture.yaml",
                base_svg=FIXTURE / "layered-architecture.base.svg",
                fixture_reference=FIXTURE / "reference.json",
                source_dir=FIXTURE / "source",
                assets_dir=ASSETS,
            )

            html = (output / "index.html").read_text(encoding="utf-8")
            match = re.search(
                r'<script id="navigation-data" type="application/json">(.*?)</script>',
                html,
                flags=re.DOTALL,
            )
            self.assertIsNotNone(match)
            data = json.loads(match.group(1))
            self.assertIn("TimingNode", data["diagram_identity"])
            self.assertIn("UC-001", data["use_case_html"])
            self.assertIn('data-zoom="fit"', html)
            self.assertIn('data-zoom="125"', html)


if __name__ == "__main__":
    unittest.main()
