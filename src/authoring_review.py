"""Generate human-reviewable authoring comparison pages."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from src.authoring import authoring_stats


def copy_with_title(source: Path, target: Path, title: str) -> None:
    lines = source.read_text(encoding="utf-8").splitlines()
    if lines and lines[0].startswith("# "):
        lines[0] = f"# {title}"
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def graph_page(graph: dict) -> str:
    lines = [
        "# Normalized engineering graph",
        "",
        "Compact metadata and sidecar authoring must produce the same semantics.",
        "",
        f"**Objects:** {len(graph['objects'])}",
        "",
        "| ID | Type | Outgoing | Incoming |",
        "| --- | --- | ---: | ---: |",
    ]
    for obj in graph["objects"]:
        lines.append(
            f"| {obj['id']} | {obj['type']} | "
            f"{len(obj.get('relations', []))} | {len(obj.get('incoming', []))} |"
        )
    lines.extend(
        [
            "",
            "## Real-source findings",
            "",
            "- UC-001, UC-008 and UC-014 are first-class use-case objects.",
            "- SAD-TESTABILITY and SVP-ST-1 are traceable document-section sources.",
            "- requirement backlinks are generated rather than authored twice.",
            "- current SI01/IF03 titles need explicit stable anchors because they are bold text rather than Markdown headings.",
            "",
        ]
    )
    return "\n".join(lines)


def generate(
    compact: Path,
    sidecar_markdown: Path,
    sidecar_metadata: Path,
    native: Path,
    normalized_graph: Path,
    output: Path,
) -> None:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    compact_stats = authoring_stats(compact, mode="compact")
    sidecar_stats = authoring_stats(sidecar_markdown, mode="sidecar")
    native_lines = len(native.read_text(encoding="utf-8").splitlines())
    sidecar_metadata_lines = len(
        sidecar_metadata.read_text(encoding="utf-8").splitlines()
    )

    index = f"""# Step 05 — Real Markdown authoring

This review compares three ways to connect normal engineering documentation to
the Experiment 007 graph.

## What to judge

Look at this as an engineer reviewing normal project documentation:

- can you still read the use case without mentally parsing tooling syntax?
- is relation metadata close enough to the owning text to stay correct?
- can one relation be authored once and get backlinks automatically?
- do stable deep links exist for the selected object?
- would this remain maintainable as the document set grows?

## Candidates

| Candidate | Main characteristic | Review |
| --- | --- | --- |
| Compact metadata | normal Markdown plus hidden metadata beside the owning object | [open rendered document](compact.md) |
| Sidecar | normal Markdown plus separate JSON relation file | [open rendered document](sidecar.md) · [open metadata](sidecar-metadata.md) |
| Native MyST | engineering prose wrapped in Sphinx-Needs directives | [open normal-renderer view](native-myst.md) |

## Measured source size

| Candidate | Document lines | Metadata/extra lines | Objects |
| --- | ---: | ---: | ---: |
| Compact metadata | {compact_stats['total_lines']} | {compact_stats['metadata_lines']} hidden metadata lines | {compact_stats['object_count']} |
| Sidecar | {sidecar_stats['total_lines']} | {sidecar_metadata_lines} sidecar JSON lines | {sidecar_stats['object_count']} |
| Native MyST | {native_lines} | directive syntax is interleaved with prose | 19 |

Both compact and sidecar require **9 explicit anchor lines** for current
SI01/IF03 objects that otherwise have no object-level Markdown heading anchor.

## Graph result

[Open the normalized engineering graph summary](graph.md).

The qualification also checks that compact and sidecar produce identical object
types, titles, outgoing relations and generated backlinks.
"""

    (output / "index.md").write_text(index, encoding="utf-8")
    copy_with_title(compact, output / "compact.md", "Compact metadata — rendered document")
    copy_with_title(sidecar_markdown, output / "sidecar.md", "Sidecar — rendered document")
    copy_with_title(native, output / "native-myst.md", "Native MyST — normal Markdown renderer")

    metadata_text = sidecar_metadata.read_text(encoding="utf-8")
    (output / "sidecar-metadata.md").write_text(
        "# Sidecar metadata\n\n"
        "This separate file must stay synchronized with the Markdown document.\n\n"
        "~~~json\n" + metadata_text + "~~~\n",
        encoding="utf-8",
    )

    graph = json.loads(normalized_graph.read_text(encoding="utf-8"))
    (output / "graph.md").write_text(graph_page(graph), encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("compact")
    result.add_argument("sidecar_markdown")
    result.add_argument("sidecar_metadata")
    result.add_argument("native")
    result.add_argument("normalized_graph")
    result.add_argument("output")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    generate(
        Path(args.compact),
        Path(args.sidecar_markdown),
        Path(args.sidecar_metadata),
        Path(args.native),
        Path(args.normalized_graph),
        Path(args.output),
    )
    print(f"generated authoring review source: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
