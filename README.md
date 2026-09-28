# exp.2026-007.requirements-traceability

Experiment for interactive engineering documentation, traceability, architecture
navigation and verification.

Status: **active — clickable real architecture and richer use-case navigation**

Cross-project coordination:
[brainboxemb.meta Experiment 007](https://github.com/brainboxemb/brainboxemb.meta/tree/feature/issue-167-requirements-traceability-experiment/experiments/007-requirements-traceability)

Current experiment issue:
[#15 — Qualify clickable real architecture and richer use-case navigation](https://github.com/brainboxemb/exp.2026-007.requirements-traceability/issues/15)

Human review site:
[Experiment 007 GitHub Pages](https://brainboxemb.github.io/exp.2026-007.requirements-traceability/)

Reference project:
[`2026-010-01.meta.event-timing-software`](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software)

## Question

How can BrainboxEmb engineering documentation become easier to understand and
navigate while keeping the useful linear engineering book?

Requirements traceability is part of that question, but not the whole question.

The experiment starts from the desired user experience:

```text
                         engineering knowledge
                                  |
       +--------------------------+--------------------------+
       |                          |                          |
       v                          v                          v
  readable book             documentation portal       engineering explorer
  ordered narrative         search/navigation          object/relationship views
       |                          |                          |
       +--------------------------+--------------------------+
                                  |
                           traceability checks
```

The first phase deliberately does **not** select Sphinx-Needs or another tool in
advance.

## Desired views

The experiment evaluates a documentation system that can provide:

- a coherent **Book** view for reading, review and printable output;
- a **Portal** with search, breadcrumbs, stable deep links and fast navigation;
- **clickable architecture** where diagram elements lead to engineering objects;
- generated **Object** views for components, use cases, requirements, interfaces
  and verification cases;
- a **Focused graph** around a selected object instead of one unreadable global
  dependency graph;
- a **Workspace** where related views can remain visible side-by-side;
- machine-checkable **Traceability** rules and coverage.

These are views on one engineering knowledge model, not independent copies of
the same information.

## Work sequence

1. [Target experience](docs/00-target-experience.md)
2. [Evaluation criteria](docs/01-evaluation-criteria.md)
3. [Candidate architecture and tools](docs/02-candidate-architecture.md)
4. [Event-timing reference slice](docs/03-reference-slice.md)
5. [Minimal engineering graph](docs/04-minimal-engineering-graph.md)
6. [Sphinx-Needs comparison](docs/05-sphinx-needs-comparison.md)
7. [Material portal/workspace](docs/06-material-portal.md)
8. [Real Markdown authoring](docs/07-real-markdown-authoring.md)
9. qualify clickable real architecture/use-case navigation and the reusable
   production owner boundary;
10. decide whether the experiment has enough evidence for a production-adoption
    proposal or needs one final bounded PoP;
11. hand production mechanisms to the proper owner only after the experiment
    supports that decision.

## Ownership

This repository owns the experimental fixtures, implementations, qualification
cases and evidence.

`brainboxemb.meta` owns cross-project sequencing and the final production
handoff decision.

The event-timing coordination repository remains owner of its project meaning,
requirements, architecture and verification content.

A reusable production mechanism may later belong in `tool.eng-docs`, but that
is a result to prove rather than an assumption of the experiment.
