# Authoring fixture — sidecar metadata

Reference authority:
`brainboxemb/2026-010-01.meta.event-timing-software@15f15c751d054f6a6af5e3478f5f9a85d046712c`

This variant keeps engineering relations outside the Markdown in a sidecar file.
Stable anchors remain in the Markdown because sidecar metadata alone cannot make
the authoritative source directly addressable.

## UC-001 — Start and prepare a TimingNode


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
4. The instance becomes ready for the operator to open when required prerequisites are satisfied.

**Alternative/failure flows:**

- a required device does not initialise;
- required reference data is unavailable/stale;
- persistence/restore is unhealthy;
- network/backoffice is unavailable while local operation may still remain possible.

## UC-008 — Operate SI-01 through a desktop GUI


**Goal:** operate/observe a timing application through the Remote API.

**Primary actor:** operator.

**Main flow:**

1. SI-02 connects through the system-defined application-control/status interface.
2. It retrieves current application/instance/subsystem state.
3. The operator performs permitted commands.
4. SI-02 shows command outcome and live/stale/disconnected status explicitly.
5. Timing state remains in SI-01 rather than being stored only in the GUI.

## UC-014 — Run multiple TimingNodes in one process


**Goal:** host multiple independently addressed TimingNodes while preserving
independent lifecycle, state and `TimingNodeId`-scoped streams.

**Primary actor:** configuration/test/operator tooling.

**Main flow:**

1. Settings describe several independently addressed `TimingNode` objects.
2. Each instance receives its own logical serialized state boundary.
3. Deployment configuration routes origins to applicable `TimingNodeId` targets.
4. Runtime-wide infrastructure may be shared without sharing mutable instance state.
5. Public interfaces can address each instance explicitly.

## SAD-TESTABILITY — Testability and failure/recovery architecture


The SI-01 architecture keeps business behaviour testable behind shared
application/domain boundaries and replaceable adapters.

## SVP-ST-1 — Application behaviour profile


ST-1 verifies a real SI-01 application process through its public application
interface while external devices/backoffice may use deterministic stubs.

## TimingNode


A `TimingNode` is the primary independently addressed operational/domain
aggregate inside SI-01. One application process may host one or more TimingNodes.

## CommandHandler


`CommandHandler` is the shared entry point for presentation requests and keeps
presentation interfaces from reaching directly into domain internals.

## Conductor


`Conductor` owns application-level composition/lifecycle coordination.

## RemoteApi


`RemoteApi` is the IF-03 presentation component for HTTP/JSON/WebSocket
application control and status.

<a id="SI01-REQ-003"></a>
**SI01-REQ-003 — Minimal TimingNode composition**


The first executable shall support configuration of at least one `TimingNode`
with a stable `TimingNodeId` that can be represented in application status.

<a id="SI01-REQ-020"></a>
**SI01-REQ-020 — Authoritative current status snapshot**


SI-01 shall maintain an authoritative current application status model that is
separate from log output.

<a id="SI01-REQ-021"></a>
**SI01-REQ-021 — Minimum first-executable status content**


The first-executable status shall expose enough information to determine
application/build identity, application state, configured TimingNode IDs,
minimal lifecycle state and explicit degraded/error information.

<a id="SI01-REQ-022"></a>
**SI01-REQ-022 — Equivalent status semantics across first interfaces**


Local console, remote-shell and IF-03 status representations shall be derived
from the same application status semantics.

<a id="SI01-REQ-030"></a>
**SI01-REQ-030 — Shared application behaviour**


Transport-specific adapters shall invoke shared SI-01 application
commands/queries rather than implementing independent copies of behaviour.

<a id="SI01-REQ-031"></a>
**SI01-REQ-031 — Externally testable executable**


The produced SI-01 application shall support ST-1 verification as a separate
running process through its public application interface.

<a id="IF03-REQ-001"></a>
**IF03-REQ-001 — Shared semantics**


IF-03 shall reuse the same application semantics as the other first interfaces.

<a id="IF03-REQ-002"></a>
**IF03-REQ-002 — Remote-host operation**


IF-03 shall support operation from a separate host/process.

<a id="IF03-REQ-004"></a>
**IF03-REQ-004 — Status query**


IF-03 shall provide a machine-consumable current status query.

## VC-ST1-001 — Query and resynchronise first-executable status


Start SI-01 with synthetic configuration, query version/status, connect and
reconnect the event stream, and verify that current state can be reconstructed.
