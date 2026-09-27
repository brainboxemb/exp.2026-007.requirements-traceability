# Target engineering-documentation experience

## Purpose

Experiment 007 is not primarily a search for a requirements database.

The target is an engineering-documentation system that makes a growing software
system easier to understand from several directions without giving up the
benefits of a coherent linear document.

The event-timing project is the first realistic reference because it already has:

- a generated architecture book;
- system use cases;
- software-item requirements;
- software architecture and detailed design;
- interface definitions;
- verification planning and concrete verification cases;
- stable identifiers for many of those objects.

The problem is therefore not a lack of documentation. The problem is making the
relationships between those documents and engineering objects visible and easy
to navigate.

## Principle: one knowledge base, several views

The same engineering meaning should be reusable through several views:

```text
                         engineering knowledge
                                  |
          +-----------------------+-----------------------+
          |                       |                       |
          v                       v                       v
     Book / PDF               Portal                Explorer
   ordered narrative      find and navigate     inspect relationships
          |                       |                       |
          +-----------------------+-----------------------+
                                  |
                            validation / CI
```

A view must not become a second manually maintained source of the same
requirement, use case or architecture decision.

## View 1 — Book

The book remains a first-class output.

It should support:

- deliberate reading order;
- architectural narrative;
- long-form explanation;
- diagrams in context;
- review as one substantial document;
- printable/PDF output where useful;
- stable section anchors.

The current event-timing architecture book is a good example of why this view is
worth preserving.

The book is not expected to be the fastest way to answer every cross-document
question.

## View 2 — Portal

The portal optimizes finding and moving through documentation.

It should provide:

- full-text search;
- hierarchical navigation;
- breadcrumbs;
- stable URLs and anchors;
- fast transitions between related pages;
- contextual previews where practical;
- links back to the larger book/narrative context.

The portal should be generated from the same authoritative source set used by
the book.

## View 3 — Clickable architecture

Architecture diagrams should become navigation surfaces rather than only images.

A diagram element such as `TimingNode`, `CommandHandler` or `IF-03` should
be able to carry a stable engineering-object identity.

Selecting it should allow navigation to:

- its definition;
- the document/section that owns that definition;
- related requirements;
- related use cases;
- related interfaces;
- related verification.

The diagram itself does not become the owner of those relationships.

## View 4 — Engineering object

A generated object view answers:

> What do we know about this one engineering thing?

Example:

```text
TimingNode
  type: architecture component
  defined in: SAD
  related use cases: UC-001, UC-014, ...
  allocated requirements: SI01-REQ-...
  related interfaces: ...
  verified by: ...
  appears in diagrams: SI01-01, SI01-03, ...
```

The object view is generated from links/metadata. It is not a new hand-authored
TimingNode document.

Object types in the initial model may include:

- use case;
- requirement;
- interface/interface requirement;
- architecture element;
- design element;
- verification case;
- document/section;
- implementation/evidence reference.

The experiment should keep this type system as small as the reference cases
allow.

## View 5 — Focused graph

A global graph of every engineering object is expected to become unreadable.

The useful graph starts from one selected object and shows a bounded local
neighborhood.

For example:

```text
UC-001
   |
   v
SI01-REQ-020
   |
   +------> IF03-REQ-004
   |
   +------> TimingNode/status model
   |
   +------> VC-ST1-001
```

The reader should be able to:

- choose relationship types;
- choose incoming/outgoing/both directions;
- limit traversal depth;
- expand one object at a time;
- navigate from a node to its object view or authoritative source.

This is closer to the desired “multi-dimensional” documentation experience than
one static traceability matrix.

## View 6 — Workspace

Engineering work often requires comparing several contexts at once.

The long-term user experience should therefore support a workspace-like view
where two or more panels can remain visible, for example:

```text
+--------------------------+------------------------------+
| Architecture diagram     | Selected object              |
|                          | TimingNode                   |
| [TimingNode selected]    | requirements / use cases /  |
|                          | verification / source links  |
+--------------------------+------------------------------+
| optional focused graph / related document              |
+---------------------------------------------------------+
```

The experiment does not require a literal 3D renderer. The requirement is
multi-dimensional navigation without repeatedly losing context.

A useful first implementation may be a two-pane responsive web UI.

## View 7 — Traceability and CI

The relationship model must also support non-visual checks.

Candidate checks include:

- duplicate engineering IDs;
- references to unknown IDs;
- relationships to incompatible object types;
- requirements without an upstream source;
- requirements without an applicable design/interface allocation;
- requirements in a verification baseline without verification coverage;
- verification cases with no linked requirement/behaviour;
- stale links to removed/renamed objects.

These checks should work without requiring a human to inspect a generated
matrix.

## Navigation example

A representative navigation sequence should feel natural:

```text
architecture book
    |
    | click TimingNode in Figure SI01-01
    v
TimingNode object view
    |
    | show incoming requirements
    v
SI01-REQ-020
    |
    | inspect interface allocation
    v
IF03-REQ-004
    |
    | inspect verification
    v
VC-ST1-001
    |
    | open authoritative source section
    v
IDD verification case
```

At every step the reader should be able to return to the architecture context or
open the related information beside it.

## Authoring experience

The authoring experience matters as much as the resulting site.

Desired properties:

- ordinary Markdown remains pleasant to read and review on GitHub;
- stable engineering IDs are explicit;
- relationships are close enough to their source that they do not silently
  drift;
- generated views do not require duplicate prose;
- adding one relationship should not require editing several matrices;
- tool-specific syntax should remain bounded;
- the model should be exportable as ordinary machine-readable data.

## What this experiment is not

Experiment 007 is not initially:

- a replacement of all event-timing Markdown with Sphinx/MyST;
- a literal 3D visualization project;
- a generic corporate developer portal;
- a complete MBSE/ALM system;
- a requirement to make every sentence an addressable object;
- a migration of production documentation.

The first goal is to find the smallest architecture that materially improves
understanding and traceability.
