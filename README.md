# exp.2026-007.requirements-traceability

Experiment for interactive engineering documentation, traceability, architecture
navigation and verification.

Status: **active — target experience and candidate architecture first**

Cross-project coordination:
[brainboxemb.meta Experiment 007](https://github.com/brainboxemb/brainboxemb.meta/tree/feature/issue-167-requirements-traceability-experiment/experiments/007-requirements-traceability)

Current experiment issue:
[#1 — Define target engineering-documentation experience and evaluate candidate architecture](https://github.com/brainboxemb/exp.2026-007.requirements-traceability/issues/1)

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
5. implement a bounded technology PoP only after the target and candidate split
   are clear;
6. qualify the selected shape with reproducible cases and retained evidence;
7. hand production mechanisms to the proper owner only after the experiment
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
