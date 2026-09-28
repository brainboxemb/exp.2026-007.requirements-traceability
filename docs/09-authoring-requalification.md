# Authoring requalification after production canary

Status: **complete — native MyST/Sphinx-Needs selected for graph-exposed authoring**

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

## Qualification result

Authoring-v2 run `36459941403` is green on exact PR head
`40fbfa7eb7ed3f69bf922319ef0efc048ca71f99`.

The two candidates represent exactly the same engineering meaning:

- 17 engineering objects;
- 34 authored outgoing relations;
- generated `derived_from_back`, `satisfies_back` and `verifies_back`;
- identical relation ownership.

The negative qualification also proved that native Sphinx-Needs rejects:

- unknown relation targets;
- invalid relation source/target type combinations.

Measured maintained source is comparable in size:

| Measure | Current compact | Native MyST |
| --- | ---: | ---: |
| Total lines | 122 | 119 |
| Explicit HTML anchor lines | 13 | 0 |
| Hidden metadata lines | 16 | 0 |
| Need directives | 0 | 17 |
| Explicit ID options | split across source constructs | 17 |
| Visible relation options | hidden in JSON | 11 |

Human review of the generated native HTML also confirms that a requirement view
naturally combines its authored upstream relation with generated downstream
context. For example `SI01-REQ-020` shows:

- `derived from UC-001 / UC-008`;
- `satisfied by TimingNode`;
- `verified by VC-ST1-001`.

Only the first relation is authored by the requirement.

## Decision

**Select native MyST/Sphinx-Needs as the authoritative authoring form for
graph-exposed engineering objects.**

The authoring contract is:

1. ordinary narrative remains normal Markdown/MyST;
2. a graph-exposed engineering object is authored once as a typed Needs
   directive such as `uc`, `req`, `ifreq`, `arch` or `vc`;
3. the directive owns the stable engineering ID;
4. each object authors only its own outgoing engineering relations;
5. inverse/backlink relations are generated by Sphinx-Needs;
6. typed relation rules are consumer-owned Sphinx-Needs schema/configuration;
7. `needs.json` is the machine-readable source graph boundary;
8. diagram `object_id` values reference an existing engineering ID; they do
   not define a second engineering object.

For architecture this means the design text/Need owns, for example,
`TimingNode`; the diagram node's `object_id: TimingNode` is a navigation
reference to that same object.

## Accepted trade-off

GitHub does not render MyST fenced directives as Sphinx-Needs cards. In direct
GitHub source review the directive remains visible as fenced source.

That trade-off is accepted because:

- the actual maintained relationship input is visible rather than hidden;
- ID/type/relation metadata is no longer split across custom anchors and hidden
  JSON;
- the source remains readable as plain text;
- the generated engineering Book remains a first-class human review output;
- Sphinx-Needs already provides anchors, backlinks, validation and machine
  export that would otherwise require custom production code.

## Production consequence

Migration 013 may now resume Step 4 with a changed reusable boundary.

`tool.eng-docs` should **not** own a second custom Markdown/hidden-JSON parser
for the same engineering object model.

Instead, Step 4 should use Sphinx-Needs as the authoring/relationship engine and
treat its exported `needs.json` as input to any smaller normalized graph,
portal, diagram cross-validation or other reusable views that BrainboxEmb still
needs.

The already-merged but unreleased `tool.eng-docs v0.4.0` graph implementation
must therefore be revised before release.
