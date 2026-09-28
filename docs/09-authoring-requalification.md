# Authoring requalification after production canary

Status: **active experiment follow-up**

Tracking issue: [#20](https://github.com/brainboxemb/exp.2026-007.requirements-traceability/issues/20)

## Why this follow-up exists

The original Experiment 007 qualified three source-authoring shapes and selected
compact adjacent metadata as the best fit at that time.

Migration 013 then exercised that direction in the real event-timing
documentation. The production canary proved several useful things:

- stable engineering identity is useful;
- relationships should be authored once;
- inverse/backlink views should be generated;
- relation ownership should follow engineering work:
  - requirements own `derived_from`;
  - design owns `satisfies`;
  - verification owns `verifies`;
- a human view of authored versus generated relations is useful.

It also exposed an authoring problem.

A current requirement can require separate source constructs for:

1. an explicit HTML anchor;
2. the normal requirement ID/title;
3. a hidden object-type/relationship comment.

For example:

```md
<a id="SI01-REQ-003"></a>
**SI01-REQ-003 — Minimal TimingNode composition**

<!-- eng {"type":"requirement","relations":{"derived_from":["UC-001","UC-014"]}} -->
```

That is valid and machine-readable, but it repeats information and hides the
relationship input that an engineer is expected to maintain.

## Re-opened question

Native MyST/Sphinx-Needs was already technically qualified by the original
experiment. Its earlier "poor default production authoring fit" conclusion was
an experiment finding based mainly on direct GitHub rendering, not an explicit
production decision.

This follow-up therefore asks again:

> Is native MyST/Sphinx-Needs now a better authoritative source form than the
> custom compact metadata syntax, given what the production canary taught us?

## Same engineering meaning

The comparison uses the current event-timing production slice at:

`a855e66f6ecb325ab77139745ef50a5c6b7acc17`

It contains 17 objects and 34 authored outgoing relations.

The comparison must preserve exactly that meaning. It is not allowed to make
native MyST look simpler by changing the graph.

## Candidate A — current compact production shape

This is represented by:

- `fixtures/authoring-v2/current-compact.md`;
- `fixtures/authoring-v2/current-diagram.yaml`.

It reproduces the current anchor + hidden `eng` / `eng-rel` convention and
diagram-owned architecture identity.

## Candidate B — native MyST/Sphinx-Needs

This is represented by:

- `fixtures/authoring-v2/native-myst.md`;
- `candidates/authoring-native-v2/conf.py`;
- `candidates/authoring-native-v2/schemas.json`.

The engineering object is authored as one directive, for example:

```text
{req} Minimal TimingNode composition
:id: SI01-REQ-003
:derived_from: UC-001, UC-014

The first executable shall support at least one configured TimingNode.
```

(The real source uses the normal MyST fenced-directive markers around that
content.)

Sphinx-Needs owns:

- object type/directive;
- stable object ID;
- typed outgoing relations;
- generated inverse/backlinks;
- machine-readable `needs.json`;
- rendered object anchors.

## Qualification

The `Authoring v2 requalification` workflow checks:

- both source forms normalize to the same 17 objects / 34 relations;
- representative inverse backlinks are generated;
- unknown relation targets fail;
- invalid relation source/target types fail;
- native MyST builds a normal reader-facing Sphinx HTML view;
- a retained human review compares the actual maintained source side by side.

## Decision boundary

This document does not yet select a winner.

Migration 013 and the unreleased `tool.eng-docs v0.4.0` graph boundary remain
blocked on the authoring decision.

If native MyST is selected, the next design question is whether
`tool.eng-docs` should stop owning a separate Markdown metadata parser and
instead consume/normalize the Sphinx-Needs export boundary.

If compact metadata remains preferred, the production syntax still needs to be
made smaller so ID/type/anchor information is not redundantly authored.
