# Authoring fixture — native MyST/Sphinx-Needs

Reference authority:
`brainboxemb/2026-010-01.meta.event-timing-software@15f15c751d054f6a6af5e3478f5f9a85d046712c`

This is the control case where engineering objects and relations are authored
directly as Sphinx-Needs directives.

```{uc} Start and prepare a TimingNode
:id: UC-001

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

```{uc} Operate SI-01 through a desktop GUI
:id: UC-008

**Goal:** operate/observe a timing application through the Remote API.

**Primary actor:** operator.

**Main flow:**

1. SI-02 connects through the application-control/status interface.
2. It retrieves current application/instance/subsystem state.
3. The operator performs permitted commands.
4. SI-02 shows command outcome and connectivity/status explicitly.
```

```{uc} Run multiple TimingNodes in one process
:id: UC-014

**Goal:** host multiple independently addressed TimingNodes while preserving
independent lifecycle, state and `TimingNodeId`-scoped streams.
```

```{docsec} Testability and failure/recovery architecture
:id: SAD-TESTABILITY

The architecture keeps business behaviour testable behind shared boundaries and
replaceable adapters.
```

```{docsec} Application behaviour profile
:id: SVP-ST-1

ST-1 verifies a real SI-01 process through its public application interface.
```

```{arch} TimingNode
:id: TimingNode
:related_to: CommandHandler, Conductor

Primary independently addressed operational/domain aggregate inside SI-01.
```

```{arch} CommandHandler
:id: CommandHandler
:related_to: RemoteApi

Shared presentation/application command and query boundary.
```

```{arch} Conductor
:id: Conductor
:related_to: TimingNode

Application-level composition/lifecycle coordination.
```

```{arch} RemoteApi
:id: RemoteApi
:related_to: CommandHandler

IF-03 HTTP/JSON/WebSocket presentation component.
```

```{req} Minimal TimingNode composition
:id: SI01-REQ-003
:derived_from: UC-001, UC-014
:allocated_to: TimingNode
:verified_by: VC-ST1-001

The first executable shall support at least one configured TimingNode.
```

```{req} Authoritative current status snapshot
:id: SI01-REQ-020
:derived_from: UC-001, UC-008
:allocated_to: TimingNode, IF03-REQ-004
:verified_by: VC-ST1-001

SI-01 shall maintain an authoritative current application status model.
```

```{req} Minimum first-executable status content
:id: SI01-REQ-021
:derived_from: UC-001, UC-008
:allocated_to: TimingNode, IF03-REQ-004
:verified_by: VC-ST1-001

The first-executable status shall expose the minimum identity/lifecycle/error
information required by the first slice.
```

```{req} Equivalent status semantics across first interfaces
:id: SI01-REQ-022
:derived_from: UC-008
:allocated_to: CommandHandler, IF03-REQ-001, IF03-REQ-004
:verified_by: VC-ST1-001

The first interfaces shall derive status from the same application semantics.
```

```{req} Shared application behaviour
:id: SI01-REQ-030
:derived_from: SAD-TESTABILITY
:allocated_to: CommandHandler
:verified_by: VC-ST1-001

Transport adapters shall invoke shared application commands/queries.
```

```{req} Externally testable executable
:id: SI01-REQ-031
:derived_from: SAD-TESTABILITY, SVP-ST-1
:allocated_to: CommandHandler, RemoteApi, IF03-REQ-002
:verified_by: VC-ST1-001

SI-01 shall support ST-1 as a separate process through its public interface.
```

```{ifreq} Shared semantics
:id: IF03-REQ-001
:derived_from: SI01-REQ-022, SI01-REQ-030
:allocated_to: CommandHandler, RemoteApi
:verified_by: VC-ST1-001

IF-03 shall reuse the same application semantics as other first interfaces.
```

```{ifreq} Remote-host operation
:id: IF03-REQ-002
:derived_from: SI01-REQ-031
:allocated_to: RemoteApi
:verified_by: VC-ST1-001

IF-03 shall support operation from a separate host/process.
```

```{ifreq} Status query
:id: IF03-REQ-004
:derived_from: SI01-REQ-020, SI01-REQ-021, SI01-REQ-022
:allocated_to: RemoteApi, CommandHandler
:verified_by: VC-ST1-001

IF-03 shall provide a machine-consumable current status query.
```

```{vc} Query and resynchronise first-executable status
:id: VC-ST1-001

Start SI-01 with synthetic configuration, query version/status, connect and
reconnect the event stream, and verify current state can be reconstructed.
```
