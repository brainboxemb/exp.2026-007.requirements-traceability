# Authoring fixture — compact metadata

Reference authority:
`brainboxemb/2026-010-01.meta.event-timing-software@15f15c751d054f6a6af5e3478f5f9a85d046712c`

This variant keeps normal Markdown visible. A stable anchor is explicit where the
current production source has no heading anchor, and one hidden `eng` metadata
block immediately follows the owning object title.

## UC-001 — Start and prepare a TimingNode

<!-- eng
{"type":"use-case"}
-->

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

<!-- eng
{"type":"use-case"}
-->

**Goal:** operate/observe a timing application through the Remote API.

**Primary actor:** operator.

**Main flow:**

1. SI-02 connects through the system-defined application-control/status interface.
2. It retrieves current application/instance/subsystem state.
3. The operator performs permitted commands.
4. SI-02 shows command outcome and live/stale/disconnected status explicitly.
5. Timing state remains in SI-01 rather than being stored only in the GUI.

## UC-014 — Run multiple TimingNodes in one process

<!-- eng
{"type":"use-case"}
-->

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

<!-- eng
{"type":"document-section"}
-->

The SI-01 architecture keeps business behaviour testable behind shared
application/domain boundaries and replaceable adapters.

## SVP-ST-1 — Application behaviour profile

<!-- eng
{"type":"document-section"}
-->

ST-1 verifies a real SI-01 application process through its public application
interface while external devices/backoffice may use deterministic stubs.

## TimingNode

<!-- eng
{"type":"architecture-element","relations":{"related_to":["CommandHandler","Conductor"]}}
-->

A `TimingNode` is the primary independently addressed operational/domain
aggregate inside SI-01. One application process may host one or more TimingNodes.

## CommandHandler

<!-- eng
{"type":"architecture-element","relations":{"related_to":["RemoteApi"]}}
-->

`CommandHandler` is the shared entry point for presentation requests and keeps
presentation interfaces from reaching directly into domain internals.

## Conductor

<!-- eng
{"type":"architecture-element","relations":{"related_to":["TimingNode"]}}
-->

`Conductor` owns application-level composition/lifecycle coordination.

## RemoteApi

<!-- eng
{"type":"architecture-element","relations":{"related_to":["CommandHandler"]}}
-->

`RemoteApi` is the IF-03 presentation component for HTTP/JSON/WebSocket
application control and status.

<a id="SI01-REQ-003"></a>
**SI01-REQ-003 — Minimal TimingNode composition**

<!-- eng
{"type":"requirement","relations":{"source":["UC-001","UC-014"],"allocated_to":["TimingNode"],"verified_by":["VC-ST1-001"]}}
-->

The first executable shall support configuration of at least one `TimingNode`
with a stable `TimingNodeId` that can be represented in application status.

<a id="SI01-REQ-020"></a>
**SI01-REQ-020 — Authoritative current status snapshot**

<!-- eng
{"type":"requirement","relations":{"source":["UC-001","UC-008"],"allocated_to":["TimingNode","IF03-REQ-004"],"verified_by":["VC-ST1-001"]}}
-->

SI-01 shall maintain an authoritative current application status model that is
separate from log output.

<a id="SI01-REQ-021"></a>
**SI01-REQ-021 — Minimum first-executable status content**

<!-- eng
{"type":"requirement","relations":{"source":["UC-001","UC-008"],"allocated_to":["TimingNode","IF03-REQ-004"],"verified_by":["VC-ST1-001"]}}
-->

The first-executable status shall expose enough information to determine
application/build identity, application state, configured TimingNode IDs,
minimal lifecycle state and explicit degraded/error information.

<a id="SI01-REQ-022"></a>
**SI01-REQ-022 — Equivalent status semantics across first interfaces**

<!-- eng
{"type":"requirement","relations":{"source":["UC-008"],"allocated_to":["CommandHandler","IF03-REQ-001","IF03-REQ-004"],"verified_by":["VC-ST1-001"]}}
-->

Local console, remote-shell and IF-03 status representations shall be derived
from the same application status semantics.

<a id="SI01-REQ-030"></a>
**SI01-REQ-030 — Shared application behaviour**

<!-- eng
{"type":"requirement","relations":{"source":["SAD-TESTABILITY"],"allocated_to":["CommandHandler"],"verified_by":["VC-ST1-001"]}}
-->

Transport-specific adapters shall invoke shared SI-01 application
commands/queries rather than implementing independent copies of behaviour.

<a id="SI01-REQ-031"></a>
**SI01-REQ-031 — Externally testable executable**

<!-- eng
{"type":"requirement","relations":{"source":["SAD-TESTABILITY","SVP-ST-1"],"allocated_to":["CommandHandler","RemoteApi","IF03-REQ-002"],"verified_by":["VC-ST1-001"]}}
-->

The produced SI-01 application shall support ST-1 verification as a separate
running process through its public application interface.

<a id="IF03-REQ-001"></a>
**IF03-REQ-001 — Shared semantics**

<!-- eng
{"type":"interface-requirement","relations":{"source":["SI01-REQ-022","SI01-REQ-030"],"allocated_to":["CommandHandler","RemoteApi"],"verified_by":["VC-ST1-001"]}}
-->

IF-03 shall reuse the same application semantics as the other first interfaces.

<a id="IF03-REQ-002"></a>
**IF03-REQ-002 — Remote-host operation**

<!-- eng
{"type":"interface-requirement","relations":{"source":["SI01-REQ-031"],"allocated_to":["RemoteApi"],"verified_by":["VC-ST1-001"]}}
-->

IF-03 shall support operation from a separate host/process.

<a id="IF03-REQ-004"></a>
**IF03-REQ-004 — Status query**

<!-- eng
{"type":"interface-requirement","relations":{"source":["SI01-REQ-020","SI01-REQ-021","SI01-REQ-022"],"allocated_to":["RemoteApi","CommandHandler"],"verified_by":["VC-ST1-001"]}}
-->

IF-03 shall provide a machine-consumable current status query.

## VC-ST1-001 — Query and resynchronise first-executable status

<!-- eng
{"type":"verification-case"}
-->

Start SI-01 with synthetic configuration, query version/status, connect and
reconnect the event stream, and verify that current state can be reconstructed.
