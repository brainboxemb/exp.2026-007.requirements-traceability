# Authoring fixture — native MyST/Sphinx-Needs

Source authority:
`brainboxemb/2026-010-01.meta.event-timing-software@15f15c751d054f6a6af5e3478f5f9a85d046712c`

This is the control case where engineering objects are authored directly as
Sphinx-Needs directives.

```{uc} Start and prepare a TimingNode
:id: UC-001
:related_to: TimingNode, CommandHandler
:derived_to: SI01-REQ-003, SI01-REQ-020, SI01-REQ-021, SI01-REQ-022
:verified_by: VC-ST1-001

**Goal:** bring one configured `TimingNode` into a known usable state.

**Primary actor:** operator or automated startup policy.

**Preconditions:**

- SI-01 has loaded and validated configuration;
- the target instance exists;
- required local state has been restored or an explicit restore fault is visible.

**Main flow:**

1. The actor selects/addresses a TimingNode.
2. SI-01 reports current instance and subsystem status.
3. Required devices are started according to configuration/policy.
4. The instance becomes ready for the operator to open when prerequisites are satisfied.

**Alternative/failure flows:**

- a required device does not initialise;
- required reference data is unavailable/stale;
- persistence/restore is unhealthy.
```

```{uc} Run multiple TimingNodes in one process
:id: UC-014
:related_to: TimingNode, CommandHandler
:derived_to: SI01-REQ-003
:verified_by: VC-ST1-001

**Goal:** host multiple independently addressed TimingNodes while preserving
independent lifecycle, state and `TimingNodeId`-scoped streams.

**Primary actor:** configuration/test/operator tooling.

**Main flow:**

1. Settings describe several independently addressed `TimingNode` objects.
2. Each instance receives its own logical serialized state boundary.
3. Deployment configuration routes origins to applicable `TimingNodeId` targets.
4. Runtime-wide infrastructure may be shared without sharing mutable instance state.
5. Public interfaces can address each instance explicitly.
```

```{arch} TimingNode
:id: TimingNode
:related_to: CommandHandler
:allocated_from: SI01-REQ-003, SI01-REQ-020, SI01-REQ-021, SI01-REQ-022

A `TimingNode` is the primary independently addressed operational/domain
aggregate inside SI-01.
```

```{arch} CommandHandler
:id: CommandHandler
:related_to: TimingNode
:allocated_from: SI01-REQ-030, SI01-REQ-031

`CommandHandler` is the shared entry point for presentation requests.
```

```{req} Authoritative current status snapshot
:id: SI01-REQ-020
:derived_from: UC-001
:allocated_to: TimingNode, IF03-REQ-004
:verified_by: VC-ST1-001

The application shall expose one authoritative current status snapshot.
```

```{ifreq} Status query
:id: IF03-REQ-004
:derived_from: SI01-REQ-020
:related_to: CommandHandler
:verified_by: VC-ST1-001

The Remote API shall provide the current status query.
```

```{vc} Query and resynchronise first-executable status
:id: VC-ST1-001
:verifies: SI01-REQ-003, SI01-REQ-020, IF03-REQ-004

Start SI-01 with synthetic configuration, query version/status, connect and
reconnect the event stream, and verify the current state can be reconstructed.
```
