# Candidate architecture and tools

## Current conclusion

The first research pass does not support choosing one documentation product for
all responsibilities.

A more promising architecture separates:

1. authored engineering source;
2. normalized engineering-object/relationship data;
3. validation;
4. document/book assembly;
5. portal rendering;
6. interactive exploration.

Conceptually:

```text
Markdown + diagram YAML + small relationship metadata
                       |
                       v
              engineering graph
              objects + relations
                       |
          +------------+-------------+
          |            |             |
          v            v             v
      validation      book         portal
                                      |
                                      v
                                  explorer
```

The important experimental contract is the engineering graph, not the choice of
site generator.

## Sphinx-Needs

Current Sphinx-Needs is a strong candidate for the **relationship/traceability
engine**.

Relevant current capabilities include:

- typed need objects and links;
- warnings/errors for unknown links and configuration problems;
- constraints and filtering;
- tables and multiple relationship visualizations;
- focused `needflow` traversal from a `root_id` with direction/depth controls;
- reproducible `needs.json` export including a schema;
- import of external need data.

This is very close to the traceability capability Experiment 007 needs.

Potential mismatch:

- native Sphinx-Needs authoring places Sphinx/MyST/reStructuredText concepts
  directly in source;
- adopting it as the whole documentation framework may impose more syntax and
  build ownership than the current Markdown + `tool.eng-docs` model needs;
- its generated graph/table views do not by themselves provide the desired
  side-by-side engineering workspace.

Therefore the first Sphinx-Needs PoP, if selected, should test **two boundaries**:

1. native need authoring;
2. Sphinx-Needs as a graph/validation engine fed from a thinner project-owned
   representation.

Official references:

- https://sphinx-needs.readthedocs.io/en/stable/
- https://sphinx-needs.readthedocs.io/en/stable/builders.html
- https://sphinx-needs.readthedocs.io/en/stable/directives/needflow.html

## Material for MkDocs

Material for MkDocs is a strong candidate for the **portal/reading experience**.

Relevant current capabilities include:

- hierarchical navigation and tabs;
- breadcrumbs/anchor tracking;
- fast instant navigation;
- search;
- extensive Markdown support/customization;
- instant previews for internal header links, helping the reader inspect related
  documentation without fully leaving the current context;
- custom JavaScript/CSS support suitable for a later engineering-object panel.

It does not provide the engineering traceability model by itself.

That is an advantage if responsibilities remain separated: it can consume pages,
anchors and generated object data without becoming the owner of requirements.

A likely experiment shape is:

```text
project Markdown
      +
generated object pages / graph.json
      |
      v
Material portal
      +
small custom explorer panel
```

Official reference:

- https://squidfunk.github.io/mkdocs-material/setup/setting-up-navigation/

## Structurizr

Structurizr is a strong architectural reference and possible architecture-view
component.

Its core model explicitly separates **elements/relationships** from **views**.
Current DSL views include system landscape/context, container, component,
filtered, dynamic, deployment and custom views.

That “one model, several views” principle aligns strongly with Experiment 007.

Structurizr also supports supplementary Markdown/AsciiDoc documentation, but its
own documentation notes that a dedicated external documentation tool can be a
better fit when full control over documentation rendering is needed.

Therefore Structurizr is currently more interesting as:

- a reference for engineering model/view separation;
- a possible architecture-model/view integration candidate;

than as the one portal for all requirements/use-case/verification documentation.

Official references:

- https://docs.structurizr.com/dsl/language
- https://docs.structurizr.com/ui/documentation/

## Antora

Antora is a useful reference for **multi-repository and versioned documentation
assembly**.

Its component-version model can aggregate content belonging to one documentation
component from multiple sources and provides component/page version navigation.

That becomes attractive if BrainboxEmb later wants a large versioned
documentation portal spanning many repository families.

Current mismatch for this experiment:

- Antora is strongly AsciiDoc/component-layout oriented;
- the event-timing source is currently Markdown-first;
- it does not itself solve the engineering object/traceability model;
- adopting it now would introduce a large source-layout/content-format decision
  before the smaller interaction model is qualified.

Keep Antora as a reference for future multi-repository/version behavior rather
than the first PoP implementation.

Official references:

- https://docs.antora.org/antora/latest/component-version/
- https://docs.antora.org/antora/latest/navigation/

## Custom thin explorer

The desired Object/Focused Graph/Workspace views are specific enough that a
small custom browser layer may be simpler than forcing one documentation system
to provide them.

That does **not** imply building a complete custom documentation generator.

Possible boundary:

```text
engineering-graph.json
        |
        +--> generated object pages
        |
        +--> static browser component
             - selected object
             - backlinks
             - local graph
             - source links
             - optional second panel
```

This layer can remain small if search, Markdown rendering, navigation and normal
page layout are delegated to an established portal such as Material for MkDocs.

## Candidate responsibility split

| Responsibility | Current strongest direction |
| --- | --- |
| Authoritative prose | Existing project Markdown |
| Book assembly | Existing `tool.eng-docs` assembly |
| Trace graph / validation | Sphinx-Needs candidate vs thin project-independent graph engine |
| Portal | Material for MkDocs candidate |
| Architecture view principle | Existing `tool.eng-docs` diagrams + Structurizr ideas |
| Object/focused graph/workspace | Thin generated/custom explorer |
| Multi-repo/version model | Defer; learn from Antora |

This is a research direction, not a production decision.

## First implementation decision to qualify

The next PoP should not start by building a whole portal.

First qualify the smallest central contract:

```text
small readable source fixture
        |
        v
engineering graph
        |
        +--> validate IDs/links/coverage
        +--> object JSON
        +--> focused relation query
        +--> stable source URLs/anchors
```

Then render the same fixture through a minimal portal.

This sequence reveals whether Sphinx-Needs can sit behind the desired source
boundary or whether a smaller generic graph extractor is cleaner.
