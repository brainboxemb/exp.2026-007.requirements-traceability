"""Generate human review HTML for Experiment 007 authoring v2."""

from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path
import shutil


CSS = """
body { font-family: system-ui, sans-serif; margin: 0; background: #f6f7f9; color: #1f2937; }
main { max-width: 1500px; margin: 0 auto; padding: 32px; }
h1, h2 { color: #111827; }
.cards { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: start; }
.card { background: white; border: 1px solid #d1d5db; border-radius: 10px; padding: 18px; min-width: 0; }
pre { overflow-x: auto; background: #111827; color: #f9fafb; padding: 14px; border-radius: 8px; font-size: 13px; }
table { border-collapse: collapse; background: white; width: 100%; margin: 16px 0 28px; }
th, td { border: 1px solid #d1d5db; padding: 9px 12px; text-align: left; vertical-align: top; }
.note { background: #fff7ed; border-left: 4px solid #f97316; padding: 12px 16px; }
.ok { background: #ecfdf5; border-left: 4px solid #10b981; padding: 12px 16px; }
a { color: #2563eb; }
code { background: #eef2ff; padding: 1px 4px; border-radius: 4px; }
"""


def copy_tree(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("comparison")
    parser.add_argument("compact")
    parser.add_argument("native")
    parser.add_argument("native_html")
    parser.add_argument("output")
    args = parser.parse_args()

    comparison = json.loads(Path(args.comparison).read_text(encoding="utf-8"))
    compact = Path(args.compact).read_text(encoding="utf-8")
    native = Path(args.native).read_text(encoding="utf-8")
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    compact_metrics = comparison["metrics"]["compact"]
    native_metrics = comparison["metrics"]["native_myst"]

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Experiment 007 authoring v2</title>
<style>{CSS}</style>
</head>
<body>
<main>
<h1>Experiment 007 — authoring v2 requalification</h1>

<div class="ok">
<strong>Engineering semantics match.</strong>
Both source forms normalize to {comparison["object_count"]} objects and
{comparison["relation_count"]} outgoing relations. Sphinx-Needs also generated
the representative inverse backlinks checked by the experiment.
</div>

<h2>Why this comparison exists</h2>
<p>The production canary proved traceability behaviour, but its source form
requires explicit HTML anchors plus hidden object/relation metadata. This
experiment re-opens the authoring decision and compares that real production
shape with native MyST/Sphinx-Needs using the corrected ownership model:</p>
<ul>
<li>requirements own <code>derived_from</code>;</li>
<li>design owns <code>satisfies</code>;</li>
<li>verification owns <code>verifies</code>.</li>
</ul>

<h2>Source measurements</h2>
<table>
<tr><th>Measure</th><th>Current compact production shape</th><th>Native MyST / Sphinx-Needs</th></tr>
<tr><td>Total source lines</td><td>{compact_metrics["total_lines"]}</td><td>{native_metrics["total_lines"]}</td></tr>
<tr><td>Explicit HTML anchor lines</td><td>{compact_metrics["explicit_anchor_lines"]}</td><td>0</td></tr>
<tr><td>Hidden object/relation metadata lines</td><td>{compact_metrics["hidden_metadata_lines"]}</td><td>0</td></tr>
<tr><td>Directive object openings</td><td>0</td><td>{native_metrics["directive_open_lines"]}</td></tr>
<tr><td>Explicit ID option lines</td><td>ID is split across normal source constructs</td><td>{native_metrics["id_option_lines"]}</td></tr>
<tr><td>Visible relation option lines</td><td>relations are hidden in comments</td><td>{native_metrics["relation_option_lines"]}</td></tr>
</table>

<div class="note">
<strong>Do not choose on line count alone.</strong>
The key question is which source an engineer can understand, edit and review
with the least duplicated bookkeeping.
</div>

<h2>Source you actually maintain</h2>
<div class="cards">
<section class="card">
<h2>Current compact production shape</h2>
<p>Normal Markdown stays pleasant when rendered, but identity/type/relation
information is split between headings, anchors, hidden comments and diagram
identity.</p>
<pre>{escape(compact)}</pre>
</section>

<section class="card">
<h2>Native MyST / Sphinx-Needs</h2>
<p>The directive is itself the engineering object. Its ID and authored
relations are visible options of that object.</p>
<p><a href="native/index.html">Open the Sphinx-rendered native document</a></p>
<pre>{escape(native)}</pre>
</section>
</div>

<h2>Review questions</h2>
<ul>
<li>Which source form would you prefer to review in a pull request?</li>
<li>Is the fenced MyST source on GitHub an acceptable trade-off for removing
custom anchors and hidden JSON?</li>
<li>Should stable IDs, typed links and backlinks be owned directly by
Sphinx-Needs?</li>
<li>If native Needs is selected, should production tooling consume the exported
Needs graph instead of parsing a second custom metadata language?</li>
</ul>
</main>
</body>
</html>
"""

    (output / "index.html").write_text(page, encoding="utf-8")
    copy_tree(Path(args.native_html), output / "native")
    (output / "comparison.json").write_text(
        json.dumps(comparison, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"generated authoring-v2 review: {output / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
