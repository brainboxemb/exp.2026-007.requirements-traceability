# Sphinx-Needs comparison

## Candidate

This comparison uses:

- Sphinx `9.1.0`;
- Sphinx-Needs `8.5.0`;
- MyST Parser `5.1.0`;
- Graphviz for the built-in `needflow`.

The versions are pinned in
`candidates/sphinx-needs/requirements.txt`.

Status: **qualified as a strong traceability/model/export candidate; built-in
needflow does not define the explorer's exact depth semantics.**

Qualification run:
[`36342679350`](https://github.com/brainboxemb/exp.2026-007.requirements-traceability/actions/runs/36342679350)

## Comparison method

The candidate represents the same eight event-timing-derived objects as the
dependency-free graph baseline:

- `UC-001`;
- `UC-008`;
- `SI01-REQ-003`;
- `SI01-REQ-020`;
- `IF03-REQ-004`;
- `TimingNode`;
- `CommandHandler`;
- `VC-ST1-001`.

The intended relationship meaning remains the same:

- upstream source;
- interface/architecture allocation;
- verification coverage;
- architecture relation.

The MyST fixture is
`candidates/sphinx-needs/source/index.md`.

Configuration is split from authored engineering content:

- `conf.py` — need types, link types, custom fields and output behavior;
- `schemas.json` — declarative type/coverage validation.

## Authoring result

The authored fixture is comparable in size to the minimal JSON baseline:

| Source | Lines |
| --- | ---: |
| MyST fixture | 112 |
| Minimal JSON fixture | 108 |

The difference is therefore not primarily fixture size.

The MyST form keeps each engineering object, its explanatory text and its
outgoing relationships together. That is attractive for project documentation,
but it introduces Sphinx/MyST directive syntax directly into authored Markdown.

For example, a requirement carries explicit metadata such as:

```text
:req:
:id:
:derived_from:
:allocated_to:
:verified_by:
```

This remains readable, but it is more tool-aware than the current event-timing
Markdown.

## Canonical relationship rule

The first implementation exposed an important modelling rule.

Initially the same conceptual relationship was authored twice:

```text
SI01-REQ-020
  allocated_to -> IF03-REQ-004

IF03-REQ-004
  derived_from -> SI01-REQ-020
```

That duplicates one traceability fact and can drift.

The qualified model now authors the relationship once:

```text
SI01-REQ-020
  allocated_to -> IF03-REQ-004
```

Sphinx-Needs generates `allocated_to_back` on `IF03-REQ-004`. Schema
validation uses `network_back` when the inverse direction is needed.

**Experiment rule:** author a canonical relationship once; derive inverse views
and validation from backlinks.

## Validation result

Sphinx-Needs schema/network validation expresses the baseline rules
declaratively rather than in project-owned Python graph code.

The qualified schema checks include:

- software requirements derive from at least one use case;
- requirement `derived_from` targets are use cases;
- software requirements allocate to an interface requirement or architecture
  element;
- software requirements have verification coverage;
- interface requirements have an upstream software requirement through the
  generated allocation backlink;
- interface requirements allocate to an architecture element;
- interface requirements have verification coverage;
- architecture `related_to` targets are architecture elements.

The positive build reports zero schema warnings.

The workflow also changes the `SI01-REQ-020` source link to `UC-404` and
requires a strict `sphinx-build -W` to fail. The retained negative evidence
contains both the missing-target link diagnostic and schema-network violation.

This is a material advantage over maintaining equivalent semantic checks as
custom Python code.

## Export and backlinks

The normal HTML build generates reproducible `needs.json`.

The qualification checks prove that it contains:

- exactly the eight expected object IDs;
- typed outgoing relationships;
- generated incoming/backlink fields;
- authoritative source URL + anchor metadata.

The export is usable independently of Sphinx's HTML renderer, making it a good
candidate interchange boundary for:

- CI checks;
- `tool.eng-docs` integration;
- object/backlink views;
- a later portal/explorer.

The qualified `needs.json` is about 15 kB for the eight-object fixture.

## Built-in focused graph result

The source contains a built-in `needflow` with:

```text
root_id        SI01-REQ-020
root_direction both
root_depth     1
```

Experiment 007 defines depth 1 as the shortest-path one-hop neighborhood.

Expected nodes are:

```text
SI01-REQ-020
UC-001
UC-008
IF03-REQ-004
TimingNode
VC-ST1-001
```

Sphinx-Needs 8.5.0 renders:

```text
SI01-REQ-020
UC-001
UC-008
TimingNode
VC-ST1-001
```

`IF03-REQ-004` is omitted even though it is a direct
`SI01-REQ-020 -> allocated_to -> IF03-REQ-004` target.

This is retained as
`needflow-depth-observation.json`.

Current upstream Sphinx-Needs source explicitly documents this behavior in its
needflow graph model as a compatibility-preserved traversal characteristic:
`filter_by_tree` walks depth-first, first visit wins, and `root_depth` can
therefore depend on traversal order.

Upstream source:
[`sphinx_needs/directives/needflow/_model.py`](https://github.com/useblocks/sphinx-needs/blob/58bcb59d861da95f2aca79f343e8bae6ec5c1250/packages/sphinx-needs/src/sphinx_needs/directives/needflow/_model.py)

The experiment does **not** redefine its explorer semantics to match this
behavior.

## Exact focused query from needs.json

A small experiment-owned breadth-first query consumes `needs.json` and applies
the desired semantics:

- incoming + outgoing;
- selected link types;
- shortest graph distance;
- depth 1.

It produces exactly the same six-object neighborhood as the dependency-free
baseline, including `IF03-REQ-004`, while excluding second-hop
`CommandHandler` and unrelated `SI01-REQ-003`.

Retained output:
`focus-SI01-REQ-020.json`.

This supports a useful responsibility split:

```text
Sphinx-Needs
  -> authored object/link model
  -> validation
  -> backlinks
  -> needs.json

needs.json
  -> exact explorer query semantics
  -> object views
  -> focused graph
  -> workspace UI
```

The built-in `needflow` can still be useful for documentation diagrams, but it
should not define the interactive explorer's graph-distance contract.

## Implementation footprint

The comparison is intentionally not reduced to a single score.

### Minimal graph baseline

- graph/CLI implementation: ~357 lines;
- qualification tests: ~104 lines;
- authored JSON fixture: ~108 lines;
- workflow: ~40 lines;
- Python runtime dependencies: **0**;
- retained graph evidence: roughly **2 kB**.

### Sphinx-Needs candidate

Current experiment sources:

- authored MyST fixture: ~112 lines;
- Sphinx configuration: ~114 lines;
- declarative schemas: ~213 lines;
- export/focused-query/observation qualification code: small experiment-owned
  helpers;
- pinned top-level packages: 3 plus Graphviz system package.

The qualified environment contains **34 Python packages** after dependency
resolution.

The retained Sphinx evidence artifact is about **4.35 MB** because it contains
the HTML site, static assets, generated graph, `needs.json`, negative-build
evidence and dependency capture.

This is substantially heavier than the custom graph baseline, but the comparison
is not like-for-like output size: Sphinx also generates a complete HTML
documentation surface, table, anchors and visualization.

## Capability comparison

| Capability | Minimal graph | Sphinx-Needs |
| --- | --- | --- |
| Stable project IDs | yes | yes |
| Typed relations | custom code | configuration |
| Broken link detection | custom code | built in |
| Generated backlinks | custom code | built in |
| Coverage/type rules | Python | declarative schema/network validation |
| Machine-readable export | custom JSON | reproducible `needs.json` |
| HTML/deep links | no | built in |
| Traceability table | no | built in |
| Relationship diagram | no | built-in `needflow` |
| Exact shortest-depth focused query | yes | small query over `needs.json` needed |
| Runtime dependency footprint | minimal | substantial |
| Tool syntax in authored prose | none in Markdown | MyST/Sphinx-Needs directives |

## Current conclusion

Sphinx-Needs is a **strong candidate for the engineering relationship model,
validation and interchange layer**.

The PoP does not support making it the owner of the complete documentation
experience.

The stronger architecture emerging from the experiment is:

```text
project engineering Markdown
        |
        +-- Sphinx-Needs annotations / bounded metadata
        |
        v
Sphinx-Needs model + validation
        |
        v
needs.json
        |
        +--> documentation views
        +--> tool.eng-docs integration
        +--> thin explorer
              - object view
              - exact focused graph
              - side-by-side workspace
```

Two questions remain before a production direction can be selected:

1. can the existing event-timing Markdown adopt the required metadata without
   making normal GitHub authoring/review unpleasant?
2. can a good portal/explorer consume the exported graph while preserving the
   current architecture book as a first-class view?

The next PoP should therefore focus on the **portal/explorer experience**, not on
inventing another traceability engine.

This comparison remains Experiment 007 evidence and is not a production adoption
decision.
