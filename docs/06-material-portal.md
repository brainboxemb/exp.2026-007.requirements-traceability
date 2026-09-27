# Material portal and workspace PoP

## Candidate

The first reader-facing portal candidate is Material for MkDocs `9.7.7`.

Status: **qualified for the bounded Experiment 007 portal/workspace slice**.

Primary qualification run:
`36343762003`

Exact source:
`853f70f568e86deda6e0eea50b71a70110d6cd14`

The candidate is intentionally evaluated **after** the engineering graph and
Sphinx-Needs export boundary were qualified.

The portal does not parse project requirements itself.

## Pipeline

The qualified PoP keeps the responsibilities explicit:

~~~text
MyST reference fixture
    |
    v
Sphinx-Needs validation
    |
    | needs builder only
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
~~~

The Sphinx step uses the `needs` builder only. The portal therefore consumes
the traceability/model export without using Sphinx HTML or Graphviz as its
frontend.

This successfully proves that the relation model and the reader-facing portal
can remain separate responsibilities.

## Qualified views

### Portal

Material provides the normal documentation-site concerns:

- search;
- explicit hierarchical navigation;
- breadcrumbs/navigation path;
- instant navigation;
- instant prefetching;
- instant previews;
- stable static URLs;
- static HTML generation.

The generated engineering object pages remain searchable but are deliberately
kept out of the primary navigation. The main navigation therefore remains
compact:

~~~text
Portal
Architecture book
Engineering explorer
Objects
  Engineering object index
~~~

This matters for scale: a portal with hundreds of engineering objects should not
turn every generated object into a permanent left-navigation entry.

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

The qualification script proves all eight pages exist and remain present in the
Material search index.

### Workspace

The explorer is a two-pane view:

~~~text
architecture + object context | selected object
                              | relations
                              | one-hop context
                              | source/object links
~~~

The left-hand architecture slice is generated from object IDs and their
relationships. Selecting an architecture node or relation/object chip updates
the right-hand detail panel without replacing the architecture context.

On narrow screens the panes stack.

The first browser screenshot exposed two useful UX problems:

- Material's default content width left too much unused horizontal space;
- a fixed SVG minimum height made the small architecture fixture appear tiny.

The qualified version therefore:

- widens the Material content grid;
- puts architecture before the object selector;
- lets the SVG scale naturally;
- keeps generated object pages out of primary navigation.

Human inspection of the second retained screenshot shows a substantially clearer
workspace: architecture context remains visible on the left while the selected
`TimingNode` details and traceability context remain visible on the right.

### Browser execution

The qualification does not stop at static HTML checks.

CI serves the generated static site and runs a real headless Chrome session
against:

`/explorer/?object=TimingNode`

The browser gate verifies that JavaScript initialization produces:

- the selected `TimingNode` detail;
- the `One-hop context` section;
- the `Open object page` action.

CI also retains a 1600×1000 screenshot:
`explorer-TimingNode.png`.

This proves the workspace behavior executes in the rendered portal, rather than
only existing as unexercised HTML/JavaScript source.

### Focus semantics

The portal generator consumes Sphinx-Needs backlinks and computes breadth-first
shortest-path depth.

`SI01-REQ-020` at depth 1 contains exactly:

- `SI01-REQ-020`;
- `UC-001`;
- `UC-008`;
- `IF03-REQ-004`;
- `TimingNode`;
- `VC-ST1-001`.

It does not include `CommandHandler` or `SI01-REQ-003`.

This deliberately preserves the Experiment 007 explorer contract rather than
inheriting the built-in `needflow root_depth` traversal behavior.

## Book boundary

The portal has an **Architecture book** destination that links to the existing
event-timing architecture book.

The PoP does not move book assembly into MkDocs.

This is an important qualified design boundary:

~~~text
tool.eng-docs / project assembly
        -> coherent Book view

needs.json + Material portal
        -> search / object / explorer views
~~~

The book and portal therefore complement each other rather than competing for
source ownership.

## Static-output evidence

The qualified retained artifact is `material-portal-evidence`.

For run `36343762003`:

- compressed CI artifact: about **0.85 MB**;
- generated static site: **63 files**, about **2.77 MB** uncompressed;
- generated explorer HTML: about **25 kB**;
- generated `SI01-REQ-020` object page: about **18 kB**;
- search index: about **11 kB**;
- normalized explorer graph: about **11 kB**;
- selected-object depth-1 graph: under **1 kB**;
- retained browser screenshot: about **132 kB**.

The complete combined Sphinx + Material Python environment contains **52
installed packages**.

The result is still ordinary static HTML/CSS/JavaScript suitable for a Pages-like
publication model.

## Custom implementation cost

Material solves the generic portal concerns well, but the engineering explorer is
intentionally domain-specific interaction and therefore requires a thin custom
layer.

Current experiment source size:

| Part | Approximate source lines |
| --- | ---: |
| portal generator | 460 |
| explorer JavaScript | 170 |
| explorer CSS | 167 |
| Material configuration | 46 |
| portal qualification tests | 120 |
| portal CI workflow | 120 |

The largest custom part is currently the portal generator. It handles several
responsibilities together for the PoP:

- normalize Sphinx-Needs export;
- compute focused graphs;
- generate object pages;
- generate the experiment architecture fixture;
- generate workspace data.

That is acceptable for an experiment, but a production design should avoid
simply moving this file unchanged into every project. Generic graph/view
generation would need one reusable owner, most likely `tool.eng-docs` if a
later migration adopts this architecture.

## Current conclusion

Material for MkDocs is a **strong portal candidate** for Experiment 007.

The PoP supports this responsibility split:

~~~text
project engineering source
        |
        v
Sphinx-Needs
  model / validation / backlinks
        |
        v
needs.json
        |
        +----------------------+
        |                      |
        v                      v
tool.eng-docs Book        Material portal
                             |
                             +--> search/navigation
                             +--> generated object pages
                             +--> thin explorer/workspace
~~~

The result is cleaner than trying to make either Sphinx or MkDocs own every
documentation responsibility.

Material is doing what it is good at: presentation, navigation and search.
Sphinx-Needs is doing what it is good at: engineering relationships,
validation and export. The existing book remains independent.

## Remaining questions

The next uncertainty is no longer which traceability engine or portal framework
to try.

The important remaining questions are closer to the **real authored
documentation**:

1. how should the current event-timing Markdown express stable objects and
   relations without becoming noisy MyST boilerplate?
2. how can the real SI-01 architecture diagrams expose object IDs so they become
   clickable portal surfaces without creating a parallel mapping?
3. how should richer use cases expose scenario/actor/failure/requirement/
   verification relationships?
4. how much side-by-side context remains useful when a real use case or
   architecture section is substantially larger than this eight-object fixture?
5. which generic generation responsibilities belong in `tool.eng-docs` if
   production adoption is selected?

The next PoP should therefore test a **larger, realistic authored use-case +
architecture slice and its authoring ergonomics**, not start another general
tool tournament.

This remains Experiment 007 evidence and is not a production adoption decision.
