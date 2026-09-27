# Material portal and workspace PoP

## Candidate

The first reader-facing portal candidate is Material for MkDocs `9.7.7`.

The candidate is intentionally evaluated **after** the engineering graph and
Sphinx-Needs export boundary were qualified.

The portal does not parse project requirements itself.

## Pipeline

The PoP keeps the responsibilities explicit:

```text
MyST reference fixture
    |
    v
Sphinx-Needs validation
    |
    v
needs.json
    |
    v
small portal generator
    |
    +--> generated object Markdown
    +--> normalized explorer JSON
    +--> clickable architecture/workspace page
    |
    v
Material for MkDocs
    |
    v
static HTML site
```

The Sphinx step uses the `needs` builder only. The portal therefore consumes
the traceability/model export without using Sphinx HTML as its frontend.

## Views under qualification

### Portal

Material provides the normal documentation-site concerns:

- search;
- navigation;
- breadcrumbs/navigation path;
- instant navigation;
- instant prefetching;
- instant previews;
- static HTML generation.

### Generated object pages

Every engineering object in the eight-object reference slice gets one generated
page containing:

- ID/type/title;
- the engineering text carried by the graph;
- authoritative source link;
- outgoing relations;
- generated incoming/backlink relations;
- exact one-hop context;
- a link back to the explorer while preserving selected-object identity.

These pages are output, not a second source.

### Workspace

The explorer is a two-pane view:

```text
reference objects + architecture | selected object
                                  | relations
                                  | one-hop context
                                  | source/object links
```

The left-hand architecture slice is generated from object IDs and their
relationships. Selecting an architecture node or relation/object chip updates
the right-hand detail panel without replacing the architecture context.

On narrow screens the panes stack.

### Focus semantics

The portal generator consumes Sphinx-Needs backlinks and computes breadth-first
shortest-path depth.

`SI01-REQ-020` at depth 1 must contain exactly:

- `SI01-REQ-020`;
- `UC-001`;
- `UC-008`;
- `IF03-REQ-004`;
- `TimingNode`;
- `VC-ST1-001`.

It must not include `CommandHandler` or `SI01-REQ-003`.

This deliberately preserves the Experiment 007 explorer contract rather than
inheriting the built-in `needflow root_depth` traversal behavior.

## Book boundary

The portal has a Book destination that links to the existing event-timing
architecture book.

The PoP does not move book assembly into MkDocs. This keeps the useful
top-to-bottom engineering narrative separate from portal/explorer rendering.

## Result to record after CI

After qualification retain:

- exact workflow run;
- static site artifact;
- generated object/focus evidence;
- portal dependency footprint;
- amount of custom Python/JavaScript/CSS required;
- navigation/search observations;
- whether the two-pane workspace is a useful basis for the requested
  multi-dimensional documentation experience;
- remaining gaps before testing against a larger real documentation slice.

This is Experiment 007 evidence, not a production adoption decision.
