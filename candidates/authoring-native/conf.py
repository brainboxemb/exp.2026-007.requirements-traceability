project = "Experiment 007 real authoring comparison"
version = "0.1"
release = version

extensions = [
    "myst_parser",
    "sphinx_needs",
]

master_doc = "index"
source_suffix = {".md": "markdown"}

needs_id_required = True
needs_id_regex = r"^[A-Za-z][A-Za-z0-9_-]*$"
needs_build_json = True
needs_reproducible_json = True
needs_json_remove_defaults = True

needs_types = [
    {"directive": "uc", "title": "Use Case", "prefix": "UC-", "color": "#BFD8D2", "style": "node"},
    {"directive": "req", "title": "Requirement", "prefix": "REQ-", "color": "#FEDCD2", "style": "node"},
    {"directive": "ifreq", "title": "Interface Requirement", "prefix": "IF-", "color": "#F6E5A8", "style": "node"},
    {"directive": "arch", "title": "Architecture Element", "prefix": "ARCH-", "color": "#D9EAF7", "style": "node"},
    {"directive": "vc", "title": "Verification Case", "prefix": "VC-", "color": "#D8E7C5", "style": "node"},
    {"directive": "docsec", "title": "Document Section", "prefix": "DOC-", "color": "#E7E7E7", "style": "node"},
]

needs_links = {
    "derived_from": {
        "description": "Upstream engineering source",
        "incoming": "is source for",
        "outgoing": "derived from",
        "copy": False,
        "allow_dead_links": False,
    },
    "allocated_to": {
        "description": "Design/interface/architecture allocation",
        "incoming": "receives allocation from",
        "outgoing": "allocated to",
        "copy": False,
        "allow_dead_links": False,
    },
    "verified_by": {
        "description": "Verification coverage",
        "incoming": "verifies",
        "outgoing": "verified by",
        "copy": False,
        "allow_dead_links": False,
    },
    "related_to": {
        "description": "Architecture relation",
        "incoming": "related from",
        "outgoing": "related to",
        "copy": False,
        "allow_dead_links": False,
    },
}

needs_schema_definitions_from_json = "schemas.json"
