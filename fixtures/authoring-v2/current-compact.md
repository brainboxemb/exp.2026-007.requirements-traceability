# Authoring v2 — current compact production shape

Reference authority:
`brainboxemb/2026-010-01.meta.event-timing-software@a855e66f6ecb325ab77139745ef50a5c6b7acc17`

This fixture retains the current production authoring mechanism on the bounded
17-object / 34-relation slice.

<a id="UC-001"></a>
## UC-001 — Start and prepare a TimingNode

<!-- eng {"type":"use-case"} -->

Bring one configured TimingNode into a known usable state.

<a id="UC-008"></a>
## UC-008 — Operate SI-01 through a desktop GUI

<!-- eng {"type":"use-case"} -->

Operate and observe SI-01 through the Remote API.

<a id="UC-014"></a>
## UC-014 — Run multiple TimingNodes in one process

<!-- eng {"type":"use-case"} -->

Host multiple independently addressed TimingNodes in one SI-01 process.

<a id="SI01-REQ-003"></a>
**SI01-REQ-003 — Minimal TimingNode composition**

<!-- eng {"type":"requirement","relations":{"derived_from":["UC-001","UC-014"]}} -->

The first executable shall support at least one configured TimingNode.

<a id="SI01-REQ-020"></a>
**SI01-REQ-020 — Authoritative current status snapshot**

<!-- eng {"type":"requirement","relations":{"derived_from":["UC-001","UC-008"]}} -->

SI-01 shall maintain an authoritative current application status model.

<a id="SI01-REQ-021"></a>
**SI01-REQ-021 — Minimum first-executable status content**

<!-- eng {"type":"requirement","relations":{"derived_from":["UC-001","UC-008"]}} -->

The first-executable status shall expose the minimum required identity,
lifecycle and error information.

<a id="SI01-REQ-022"></a>
**SI01-REQ-022 — Equivalent status semantics across first interfaces**

<!-- eng {"type":"requirement","relations":{"derived_from":["UC-008"]}} -->

The first interfaces shall derive status from the same application semantics.

<a id="SI01-REQ-030"></a>
**SI01-REQ-030 — Shared application behaviour**

<!-- eng {"type":"requirement"} -->

Transport adapters shall invoke shared application commands and queries.

<a id="SI01-REQ-031"></a>
**SI01-REQ-031 — Externally testable executable**

<!-- eng {"type":"requirement"} -->

SI-01 shall support ST-1 as a separate process through its public interface.

<a id="IF03-REQ-001"></a>
**IF03-REQ-001 — Shared semantics**

<!-- eng {"type":"interface-requirement","relations":{"derived_from":["SI01-REQ-022","SI01-REQ-030"]}} -->

IF-03 shall reuse the same application semantics as other first interfaces.

<a id="IF03-REQ-002"></a>
**IF03-REQ-002 — Remote-host operation**

<!-- eng {"type":"interface-requirement","relations":{"derived_from":["SI01-REQ-031"]}} -->

IF-03 shall support operation from a separate host or process.

<a id="IF03-REQ-004"></a>
**IF03-REQ-004 — Status query**

<!-- eng {"type":"interface-requirement","relations":{"derived_from":["SI01-REQ-020","SI01-REQ-021","SI01-REQ-022"]}} -->

IF-03 shall provide a machine-consumable current status query.

## TimingNode design

<!-- eng-rel {"id":"TimingNode","relations":{"satisfies":["SI01-REQ-003","SI01-REQ-020","SI01-REQ-021"]}} -->

TimingNode is the primary independently addressed operational/domain aggregate.

## CommandHandler design

<!-- eng-rel {"id":"CommandHandler","relations":{"satisfies":["SI01-REQ-022","SI01-REQ-030","SI01-REQ-031","IF03-REQ-001","IF03-REQ-004"]}} -->

CommandHandler is the shared entry point for presentation requests.

## Conductor design

Conductor coordinates application-wide lifecycle and active TimingNodes.

## RemoteApi design

<!-- eng-rel {"id":"RemoteApi","relations":{"satisfies":["SI01-REQ-031","IF03-REQ-001","IF03-REQ-002","IF03-REQ-004"]}} -->

RemoteApi is the programmable HTTP/WebSocket presentation component.

<a id="VC-ST1-001"></a>
### VC-ST1-001 — Query and resynchronise first-executable status

<!-- eng {"type":"verification-case","relations":{"verifies":["SI01-REQ-003","SI01-REQ-020","SI01-REQ-021","SI01-REQ-022","SI01-REQ-030","SI01-REQ-031","IF03-REQ-001","IF03-REQ-002","IF03-REQ-004"]}} -->

Start SI-01 with synthetic configuration and verify version/status plus reconnect
behaviour through the public application interface.
