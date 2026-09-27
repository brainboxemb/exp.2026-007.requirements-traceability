# Event-timing reference slice

## Purpose

Experiment 007 uses a bounded slice of the real event-timing documentation so
candidate tooling is tested against actual engineering structure without copying
the whole project.

Reference repository:

`brainboxemb/2026-010-01.meta.event-timing-software`

The reference remains read-only during the first PoP.

## Reference chain A — status

Use the existing first-executable status chain:

```text
UC-001 / UC-008
       |
       v
SI01-REQ-020
       |
       v
IF03-REQ-004
       |
       v
VC-ST1-001
```

Useful source locations:

- `docs/04-UC-system-use-cases.md`;
- `docs/20-01-SRD-timing-application-requirements.md`;
- `docs/40-01-IDD-application-control-status.md`.

This case proves typed links across use case, software-item requirement,
interface requirement and verification.

## Reference chain B — architecture object

Use `TimingNode` as the first architecture object.

It appears as a central domain aggregate in the SI-01 architecture and has
relationships to:

- UC-001 and other operational use cases;
- SI01-REQ-003 and status requirements;
- `TimingNodeId`;
- `CommandHandler`/presentation target resolution;
- I/O routing and backend message handling;
- verification scenarios.

The candidate object model should provide one generated view of those
relationships without inventing a second TimingNode definition.

Useful source:

- `docs/31-01-SAD-timing-application-architecture.md`;
- `docs/31-01-SDD-02-java-component-design.md`.

## Reference chain C — clickable architecture

Use Figure SI01-01 / the layered architecture as the navigation fixture.

The experiment should eventually prove:

1. a diagram node carries an engineering object ID;
2. the generated SVG/HTML exposes a link or selection event;
3. selecting `TimingNode` opens its generated object context;
4. the reader can navigate onward to one related requirement and verification
   case.

Do not change the production diagram merely for the first experimental fixture.
A reduced experiment-owned diagram is sufficient until the interaction shape is
qualified.

## Minimum object fixture

The first executable fixture can stay small:

| Object | Type |
| --- | --- |
| UC-001 | use-case |
| UC-008 | use-case |
| SI01-REQ-003 | requirement |
| SI01-REQ-020 | requirement |
| IF03-REQ-004 | interface-requirement |
| TimingNode | architecture-element |
| CommandHandler | architecture-element |
| VC-ST1-001 | verification-case |

Add objects only when a qualification question needs them.

## Minimum relationships

The fixture should exercise at least:

- `derived_from` / `source`;
- `allocated_to`;
- `defines_interface` or equivalent interface allocation;
- `verified_by`;
- architecture containment/association where useful.

Relationship names are not production conventions yet. The PoP may refine them.

## Evidence to retain

For each candidate implementation retain:

- authored fixture source;
- normalized/exported graph;
- validation output for passing fixture;
- deliberately failing duplicate/unknown-link cases;
- rendered object view;
- focused graph around one selected object;
- portal/deep-link example when that phase starts.

The final comparison should measure authoring impact as well as generated
capability.
