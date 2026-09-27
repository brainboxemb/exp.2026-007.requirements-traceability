# Minimal engineering-graph PoP

## Purpose

This PoP establishes the smallest executable contract needed for Experiment 007
before evaluating Sphinx-Needs on the same problem.

It is intentionally **not** a production-tool proposal.

The implementation uses only the Python standard library and a small JSON
fixture. That makes its implementation/authoring cost a useful baseline.

## Authored model

The reference fixture is:

`fixtures/reference/event-timing-graph.json`

It contains eight real event-timing-derived engineering objects:

- `UC-001`;
- `UC-008`;
- `SI01-REQ-003`;
- `SI01-REQ-020`;
- `IF03-REQ-004`;
- `TimingNode`;
- `CommandHandler`;
- `VC-ST1-001`.

Each authored object carries:

```text
id
type
title
authoritative source URL + anchor
outgoing typed relations
optional verification-baseline flag
```

Backlinks are never authored twice. They are derived in normalized output.

## Current relation vocabulary

The first PoP deliberately keeps the vocabulary small:

| Relation | Meaning in this fixture |
| --- | --- |
| `source` | upstream use case/requirement source |
| `allocated_to` | design/interface/architecture allocation |
| `verified_by` | verification coverage |
| `related_to` | architecture association used only where needed |

Allowed source/target type combinations are explicitly validated.

These names are experimental and are not yet BrainboxEmb production conventions.

## Qualification cases

Issue #3 defines GRAPH-01 through GRAPH-08.

The automated test suite proves:

- valid reference model;
- duplicate-ID rejection;
- unknown-target rejection;
- relation/type compatibility;
- requirement coverage;
- derived backlinks;
- bounded focused traversal;
- provenance/generator retention.

## Commands

Validate:

```text
python -m src.eng_graph validate fixtures/reference/event-timing-graph.json
```

Export normalized graph with backlinks:

```text
python -m src.eng_graph export \
  fixtures/reference/event-timing-graph.json \
  bld/engineering-graph.json
```

Export the one-hop context around `SI01-REQ-020`:

```text
python -m src.eng_graph focus \
  fixtures/reference/event-timing-graph.json \
  SI01-REQ-020 \
  bld/focus-SI01-REQ-020.json \
  --depth 1 --direction both
```

## What this baseline should teach us

The important measurement is not just whether Python can model a graph.

We want to learn:

- how much authored metadata the useful relationships require;
- whether the relation vocabulary remains understandable;
- whether useful validation needs much custom code;
- whether normalized JSON is a clean boundary for portal/explorer views;
- which features Sphinx-Needs provides that would otherwise require meaningful
  maintenance here.

The next candidate comparison should use this same eight-object fixture and the
same qualification questions.

## Qualification result

The first CI qualification is green:

- workflow run: `36341893252`;
- all GRAPH-01 through GRAPH-08 unit/qualification cases passed;
- retained artifact: `engineering-graph-evidence`;
- artifact contains:
  - `engineering-graph.json` — normalized graph with generated backlinks;
  - `focus-SI01-REQ-020.json` — one-hop incoming/outgoing neighborhood.

The focused output contains `SI01-REQ-020` plus its direct use-case,
interface, architecture and verification context. `CommandHandler` is
correctly absent at depth 1 because it is one additional hop beyond
`IF03-REQ-004`/`TimingNode`.

### Baseline implementation size

The first baseline is intentionally small but not free:

- core graph/CLI implementation: about 357 source lines;
- qualification tests: about 104 source lines;
- reference fixture: about 108 JSON lines;
- workflow: about 40 lines;
- external Python runtime dependencies: **none**.

These counts are comparison evidence, not production size targets.

### Limitations exposed by the baseline

The baseline also makes several costs visible:

- JSON authoring is explicit and comparatively verbose;
- relationship/type rules are currently hard-coded in Python;
- there is no Markdown extraction or inline authoring model;
- there is no generated HTML/table/diagram view yet;
- source anchors are manually supplied;
- cross-repository import/version handling is not implemented;
- object types and relation vocabulary are experiment-owned code.

This is useful evidence. A larger framework such as Sphinx-Needs should justify
its additional machinery by reducing these costs or providing materially useful
capabilities without damaging the desired Markdown-first authoring experience.
