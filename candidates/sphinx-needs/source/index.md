# Event-timing reference slice — Sphinx-Needs

This is the same bounded engineering slice used by the dependency-free
Experiment 007 graph baseline.

The prose is intentionally small. The point of this source is to compare how
much relationship metadata must be authored and what Sphinx-Needs generates
from it.

## Use cases

```{uc} Start and prepare a TimingNode
:id: UC-001
:origin_url: https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/blob/main/docs/04-UC-system-use-cases.md
:origin_anchor: uc-001--start-and-prepare-a-timingnode

Bring one configured TimingNode into a usable operational state.
```

```{uc} Operate SI-01 through a desktop GUI
:id: UC-008
:origin_url: https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/blob/main/docs/04-UC-system-use-cases.md
:origin_anchor: uc-008--operate-si-01-through-a-desktop-gui

View status/data and execute permitted commands through the Remote API.
```

## Requirements

```{req} Minimal TimingNode composition
:id: SI01-REQ-003
:origin_url: https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/blob/main/docs/20-01-SRD-timing-application-requirements.md
:origin_anchor: si01-req-003--minimal-timingnode-composition
:derived_from: UC-001
:allocated_to: TimingNode
:verified_by: VC-ST1-001

Support configuration of at least one TimingNode with a stable TimingNodeId.
```

```{req} Authoritative current status snapshot
:id: SI01-REQ-020
:origin_url: https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/blob/main/docs/20-01-SRD-timing-application-requirements.md
:origin_anchor: si01-req-020--authoritative-current-status-snapshot
:derived_from: UC-001, UC-008
:allocated_to: IF03-REQ-004, TimingNode
:verified_by: VC-ST1-001

Expose one authoritative current application/TimingNode status snapshot.
```

## Interface requirement

```{ifreq} Status query
:id: IF03-REQ-004
:origin_url: https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/blob/main/docs/40-01-IDD-application-control-status.md
:origin_anchor: if03-req-004--status-query
:derived_from: SI01-REQ-020
:allocated_to: CommandHandler
:verified_by: VC-ST1-001

Provide the current status through the Remote API.
```

## Architecture

```{arch} TimingNode
:id: TimingNode
:origin_url: https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/blob/main/docs/31-01-SAD-timing-application-architecture.md
:origin_anchor: domain
:related_to: CommandHandler

Primary independently addressed operational/domain aggregate.
```

```{arch} CommandHandler
:id: CommandHandler
:origin_url: https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/blob/main/docs/31-01-SAD-timing-application-architecture.md
:origin_anchor: application

Shared presentation request boundary.
```

## Verification

```{vc} Query and resynchronise first-executable status
:id: VC-ST1-001
:origin_url: https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/blob/main/docs/40-01-IDD-application-control-status.md
:origin_anchor: vc-st1-001--query-and-resynchronise-first-executable-status

Exercise version/status query and reconnect/resynchronisation behavior.
```

## Traceability table

```{needtable} Reference slice
:columns: id;title;type;outgoing;incoming
:style: table
```

## Focused graph

The graph is deliberately rooted at the same object and depth as the custom
baseline.

```{needflow} SI01-REQ-020 one-hop context
:root_id: SI01-REQ-020
:root_direction: both
:root_depth: 1
:link_types: derived_from,allocated_to,verified_by,related_to
:show_link_names:
:engine: graphviz
```
