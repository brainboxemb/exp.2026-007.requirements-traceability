# Evaluation criteria

## Purpose

Candidate tools are evaluated against responsibilities rather than selected as
one all-encompassing product.

A candidate may be excellent for the portal while being intentionally weak as a
traceability engine, or vice versa.

## C1 — Preserve the book

The solution must not force removal of the current coherent engineering-book
view.

Questions:

- Can ordered long-form Markdown still be assembled?
- Can stable anchors survive into generated output?
- Can the same source feed both book and portal views?
- Can PDF/print remain a separate output concern?

## C2 — Markdown-first authoring

The current projects use readable Markdown as authored engineering source.

Prefer:

- small metadata additions;
- normal GitHub review readability;
- explicit stable IDs;
- minimal framework-specific ceremony.

Penalize:

- large directive wrappers around ordinary prose;
- duplicated source solely for a second renderer;
- source that becomes difficult to read outside the generator.

## C3 — Engineering object model

The solution should represent stable objects and typed relationships.

Initial useful object types:

- use case;
- requirement;
- interface requirement;
- architecture/design element;
- verification case.

Required model capabilities:

- stable project-owned ID;
- type;
- title/label;
- authoritative source location;
- typed outgoing relations;
- generated backlinks;
- optional status/tags.

## C4 — Clickable diagrams

A diagram element should be able to refer to an engineering object.

Prefer a generic contract such as:

```text
diagram node
  object_id: TimingNode
  href/object target generated from model
```

The diagram renderer should not need to understand requirement semantics.

## C5 — Portal navigation

Evaluate:

- search;
- hierarchy;
- breadcrumbs;
- deep links;
- fast navigation;
- contextual preview;
- customization/extensibility;
- static hosting compatibility.

## C6 — Focused relationship exploration

The engine/UI should be able to show a bounded graph around one selected object.

Useful controls:

- relationship type;
- direction;
- traversal depth;
- object type filters.

A full-database graph is not sufficient.

## C7 — Side-by-side context

Assess whether the portal can support or be extended to support:

- diagram + selected object;
- source document + related object;
- object + focused graph;
- responsive two-pane layout.

This may be a custom UI layer; a candidate is not rejected merely because it
does not provide this out of the box.

## C8 — Validation and coverage

Required experimental validation:

- duplicate IDs fail;
- unknown relation targets fail;
- malformed types/links fail;
- configurable coverage rules can fail CI;
- validation produces useful source locations.

## C9 — Machine-readable interchange

The model must be exportable to a stable machine-readable representation.

JSON is the first preferred interchange format.

The interchange should be useful independently of the site generator so that:

- CI can validate it;
- an explorer can consume it;
- `tool.eng-docs` can later assemble/publish outputs;
- another renderer can be tried without rewriting project meaning.

## C10 — Multi-repository potential

The event-timing family already separates coordination/documentation and Java
implementation.

The long-term model should be able to link objects/evidence across repositories
without requiring all source files to move into one repository.

This is a later qualification concern; the first PoP remains intentionally
small.

## C11 — Version/provenance

Generated relationship data should retain enough provenance to answer:

- which source repository/revision produced this model?
- which document and anchor owns this object?
- which tool/schema version produced the export?

Versioned historical documentation is useful but not required to dictate the
entire source layout.

## C12 — Tool ownership boundary

A production solution should fit the existing ownership model.

Likely split:

```text
project repository
  owns engineering meaning

tool.eng-docs
  may own generic extraction/validation/render/export mechanisms

site/portal technology
  may render generated/project documentation

experiment repository
  only qualifies candidate shapes
```

A tool that requires `tool.eng-docs` to become the owner of project semantics
is a poor fit.

## Evaluation scale

Do not reduce the final choice to one numeric score.

For each candidate/responsibility record:

- **strong fit** — naturally satisfies the criterion;
- **possible with integration** — useful capability exists but needs a bounded
  adapter/custom layer;
- **poor fit** — conflicts with the intended source/ownership model;
- **not applicable** — responsibility intentionally belongs elsewhere.

The final architecture can combine candidates when responsibilities remain
clear.
