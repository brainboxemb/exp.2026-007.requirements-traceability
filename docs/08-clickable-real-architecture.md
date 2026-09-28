# Clickable real architecture and richer use-case navigation

## Scope

Experiment 007 Step 06 qualifies whether the real SI-01 architecture diagram can
act as a navigation surface for the same engineering objects used by
requirements, use cases and verification.

The reference project is pinned to:

`brainboxemb/2026-010-01.meta.event-timing-software@d6f629093e865a7fc33c9adbaaad7e66a5510751`

The current diagram generator owner was inspected at:

`brainboxemb/tool.eng-docs@82510d4e70ed7ece35936ffdd67cdaa55e0accaf`

Primary technical qualification run:

`36437219540`

Retained human-review artifact:

`navigation-review-output` — artifact `10975669725`

Exact qualified source head:

`5190b1ed1381fdcb2a02418abfb384857c78ff70`

## Real inputs

The Step-06 review fixture was refreshed on 28 September 2026 to the current
event-timing `main` architecture rather than a daily tag. The available
`daily/20260924*` tags predate the latest architecture work, including
ApplicationBootstrap, backend-message routing/Web multiplicity and runtime
logging/live diagnostics.

The matching generated diagram is pinned from `prod/docs` commit
`dafd1c784451456793f3f322f400e4d4e781a23d`.

The PoP mirrors only the reference material needed for navigation:

- the real `docs/_diagrams/layered-architecture.yaml`;
- the generated real `layered-architecture.svg`;
- the real system use-case document;
- the SI-01 SRD;
- the IF-03 IDD / verification content;
- the Step-05 normalized engineering graph.

The production event-timing repository is not modified by this experiment.

## Finding 1 — diagram-local identity and engineering identity are different

The current diagram language already requires a local node ID.

For example, the real diagram uses a node identity such as:

```yaml
- id: timing-node-root
  label: TimingNode
```

That local ID is useful for:

- edge routing;
- grouping;
- diagram layout;
- Draw.io generation.

It is not necessarily the canonical engineering-object identity.

The engineering graph already owns:

```text
TimingNode
```

The PoP therefore adds one optional semantic field beside the real node:

```yaml
- id: timing-node-root
  object_id: TimingNode
  label: TimingNode
```

This is preferable to overloading the diagram-local `id`.

It also avoids a separate portal-side mapping such as:

```text
"TimingNode box" -> "TimingNode engineering object"
```

The diagram source itself declares which engineering object it represents.

## Finding 2 — the current SVG renderer drops node identity

At the inspected `tool.eng-docs` revision, node IDs are used in the diagram
model and in Draw.io output, but the SVG renderer emits ordinary rectangles,
glyphs and text without preserving the node ID on a containing SVG element.

That means the browser cannot currently answer:

> Which engineering object produced this rectangle?

The PoP proves that only a small additional contract is required.

Experiment output carries:

```html
<g
  class="engineering-hit"
  data-engineering-id="TimingNode"
  role="button"
  tabindex="0">
  ...
</g>
```

For the experiment this is implemented as an overlay on the existing generated
SVG so the production renderer does not need to be changed prematurely.

A production implementation in `tool.eng-docs` should preferably preserve the
identity directly on/wrapping the rendered node rather than recreate an overlay
after rendering.

## Finding 3 — diagram identity validates against the engineering graph

The Step-06 generator rejects a diagram `object_id` when:

- the ID does not exist in the engineering graph;
- the object exists but is not an architecture element;
- the same engineering identity is assigned more than once in the qualified
  diagram scope.

The qualified real diagram exposes:

- `TimingNode`;
- `CommandHandler`;
- `Conductor`;
- `RemoteApi`.

The test deliberately changes `TimingNode` to `MissingTimingNode` and
requires generation to fail.

This is important because a clickable diagram must not silently create a second,
independent identity namespace.

## Finding 4 — architecture to use-case navigation can be derived

The diagram does not contain a hand-authored list of related use cases.

For `TimingNode`, the navigation model follows the existing engineering graph:

```text
TimingNode
   ^
   | allocated_to
   |
SI01 requirements
   ^
   | source
   |
UC-001 / UC-008 / UC-014
```

The qualified Step-06 model therefore derives real use-case context including:

- `UC-001`;
- `UC-014`.

It also exposes the allocated requirements and the verification reached through
those requirements.

The inverse direction works as well.

Opening `UC-001` derives architecture context through its generated requirement
backlinks and highlights the applicable diagram objects while keeping the real
use-case narrative visible.

No requirement-to-diagram or use-case-to-diagram matrix is authored separately.

## Finding 5 — the narrative remains the use-case authority

Step 06 renders the real multi-paragraph use-case section rather than replacing
it with structured fields.

The graph supplies navigation around the narrative:

```text
architecture
     |
     v
  UC-001
  narrative
     |
     +--> requirements
     +--> interfaces
     +--> verification
```

This confirms the Step-05 direction:

- goal, actors, preconditions, main flow and alternatives remain readable
  Markdown;
- compact metadata/graph relations support traversal;
- generated views assemble context instead of duplicating the narrative.

## Finding 6 — source-link quality still depends on stable anchors

The real use cases are Markdown headings and therefore have stable GitHub
section anchors.

For example, `UC-001` can link directly to its authoritative section.

The current SI01 and IF03 requirement titles are bold paragraphs rather than
headings. Step 06 therefore falls back to a pinned source-revision line range
for those objects.

The UI deliberately marks this distinction.

This is useful evidence for a later production authoring convention:

- every engineering object exposed through the graph should have a stable source
  target;
- heading anchors are sufficient where they already exist;
- non-heading requirement objects need a minimal explicit anchor convention.

## Qualified production boundary

The technical PoP supports the following owner split:

```text
project repository
  diagram YAML
    id: diagram-local identity
    object_id: optional engineering identity

  Markdown
    engineering object identity + relations
            |
            v
tool.eng-docs
  validate object_id shape
  preserve object_id into generated SVG
            |
            v
SVG + engineering graph
            |
            v
portal / workspace
  selection
  generated backlinks
  use-case context
  source navigation
```

The portal does not own project meaning and does not maintain a second
diagram-to-object map.

## Likely `tool.eng-docs` change

If production adoption is selected later, the smallest useful generic addition
appears to be:

1. allow optional `object_id` on diagram nodes (and only on groups if a real
   need is later proven);
2. validate the field as an opaque/stable semantic ID;
3. preserve it into SVG output, for example as
   `data-engineering-id="<object_id>"`;
4. optionally expose the same value in Draw.io metadata where useful;
5. keep graph-aware validation outside the pure diagram renderer unless the
   calling project supplies a graph/catalog explicitly.

The experiment does **not** recommend coupling `tool.eng-docs` directly to
Sphinx-Needs.

The useful generic contract is engineering identity, not a specific traceability
engine.

## Human-review status

Technical qualification is green.

The retained screenshots cover:

- `TimingNode` selected in the real SI-01 diagram;
- `UC-001` open while related architecture remains highlighted.

Human review on 28 September 2026 accepted the clickable real-architecture view
as useful and worth continuing toward production adoption. No additional
bounded UX PoP was requested.

The positive review specifically confirms the central Step-06 premise: the
architecture can remain visible as useful context while navigating into richer
engineering objects and real use-case narrative.

## Exit status

**Step 06 is accepted and Experiment 007 is qualified for production adoption.**

The experiment has sufficient evidence for the next cross-project track:

1. retain the experiment repository as evidence, human review surface and
   regression lab;
2. move generic diagram engineering-identity support to `tool.eng-docs`;
3. define the smallest production authoring/graph extraction convention without
   making native MyST the project source format;
4. pilot the production mechanism in the event-timing documentation while
   retaining the engineering book as a first-class output;
5. keep project-specific requirements, use cases, architecture and verification
   meaning in the project repository.

Production changes remain owned by the follow-on migration; this experiment does
not directly modify those owners.
