# Sphinx-Needs comparison

## Candidate

This comparison uses:

- Sphinx `9.1.0`;
- Sphinx-Needs `8.5.0`;
- MyST Parser `5.1.0`;
- Graphviz for the focused `needflow`.

The versions are pinned in
`candidates/sphinx-needs/requirements.txt`.

## Comparison method

The candidate must represent the same eight event-timing-derived objects as the
dependency-free graph baseline and preserve the same relationship meaning.

The MyST source is:

`candidates/sphinx-needs/source/index.md`

Sphinx-Needs configuration/schema rules are kept separate from the authored
fixture:

- `conf.py` — object types, link types and output behavior;
- `schemas.json` — declarative relationship/coverage validation.

## What is being tested

### Markdown authoring

The source uses ordinary MyST fenced directives with explicit IDs, source
metadata and typed relation options.

This is more embedded tool syntax than the JSON-sidecar baseline, but it has one
important property to evaluate: the engineering object and its relations live
beside the explanatory Markdown rather than in a separate data file.

### Validation

Sphinx-Needs schema validation is used to express the same rules that the
baseline implemented in Python:

- software requirements derive from at least one use case;
- software requirements allocate to interface/architecture elements;
- software requirements have verification coverage;
- interface requirements derive from software requirements;
- interface requirements allocate to architecture elements;
- interface requirements have verification coverage;
- architecture `related_to` targets are architecture elements.

The workflow also creates a deliberate unknown ID (`UC-404`) and requires the
strict Sphinx build to fail.

### Generated data

The HTML build also generates reproducible `needs.json`.

A small verification script checks:

- exact expected object IDs;
- outgoing relations;
- automatically generated backlinks;
- authoritative source metadata.

### Focused graph

The MyST source includes a `needflow` rooted at `SI01-REQ-020`, direction
`both`, depth `1`, using the same four relation families as the baseline.

The generated graph is retained with the HTML artifact for visual inspection.

## Result to record after CI

After qualification, update this document with:

- exact workflow run;
- generated artifact observations;
- authored/configuration line counts;
- installed dependency footprint;
- concrete functionality obtained without custom code;
- usability/readability costs;
- remaining gaps for the desired Book / Portal / Object / Focused Graph /
  Workspace experience.

This comparison is evidence for Experiment 007, not a production adoption
decision.
