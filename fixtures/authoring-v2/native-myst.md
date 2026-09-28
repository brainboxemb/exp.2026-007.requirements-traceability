# Authoring v2 — native MyST/Sphinx-Needs

Reference authority:
\`brainboxemb/2026-010-01.meta.event-timing-software@a855e66f6ecb325ab77139745ef50a5c6b7acc17\`

\`\`\`{uc} Start and prepare a TimingNode
:id: UC-001

Bring one configured TimingNode into a known usable state.
\`\`\`

\`\`\`{uc} Operate SI-01 through a desktop GUI
:id: UC-008

Operate and observe SI-01 through the Remote API.
\`\`\`

\`\`\`{uc} Run multiple TimingNodes in one process
:id: UC-014

Host multiple independently addressed TimingNodes in one SI-01 process.
\`\`\`

\`\`\`{req} Minimal TimingNode composition
:id: SI01-REQ-003
:derived_from: UC-001, UC-014

The first executable shall support at least one configured TimingNode.
\`\`\`

\`\`\`{req} Authoritative current status snapshot
:id: SI01-REQ-020
:derived_from: UC-001, UC-008

SI-01 shall maintain an authoritative current application status model.
\`\`\`

\`\`\`{req} Minimum first-executable status content
:id: SI01-REQ-021
:derived_from: UC-001, UC-008

The first-executable status shall expose the minimum required identity,
lifecycle and error information.
\`\`\`

\`\`\`{req} Equivalent status semantics across first interfaces
:id: SI01-REQ-022
:derived_from: UC-008

The first interfaces shall derive status from the same application semantics.
\`\`\`

\`\`\`{req} Shared application behaviour
:id: SI01-REQ-030

Transport adapters shall invoke shared application commands and queries.
\`\`\`

\`\`\`{req} Externally testable executable
:id: SI01-REQ-031

SI-01 shall support ST-1 as a separate process through its public interface.
\`\`\`

\`\`\`{ifreq} Shared semantics
:id: IF03-REQ-001
:derived_from: SI01-REQ-022, SI01-REQ-030

IF-03 shall reuse the same application semantics as other first interfaces.
\`\`\`

\`\`\`{ifreq} Remote-host operation
:id: IF03-REQ-002
:derived_from: SI01-REQ-031

IF-03 shall support operation from a separate host or process.
\`\`\`

\`\`\`{ifreq} Status query
:id: IF03-REQ-004
:derived_from: SI01-REQ-020, SI01-REQ-021, SI01-REQ-022

IF-03 shall provide a machine-consumable current status query.
\`\`\`

\`\`\`{arch} TimingNode
:id: TimingNode
:satisfies: SI01-REQ-003, SI01-REQ-020, SI01-REQ-021

TimingNode is the primary independently addressed operational/domain aggregate.
\`\`\`

\`\`\`{arch} CommandHandler
:id: CommandHandler
:satisfies: SI01-REQ-022, SI01-REQ-030, SI01-REQ-031, IF03-REQ-001, IF03-REQ-004

CommandHandler is the shared entry point for presentation requests.
\`\`\`

\`\`\`{arch} Conductor
:id: Conductor

Conductor coordinates application-wide lifecycle and active TimingNodes.
\`\`\`

\`\`\`{arch} RemoteApi
:id: RemoteApi
:satisfies: SI01-REQ-031, IF03-REQ-001, IF03-REQ-002, IF03-REQ-004

RemoteApi is the programmable HTTP/WebSocket presentation component.
\`\`\`

\`\`\`{vc} Query and resynchronise first-executable status
:id: VC-ST1-001
:verifies: SI01-REQ-003, SI01-REQ-020, SI01-REQ-021, SI01-REQ-022, SI01-REQ-030, SI01-REQ-031, IF03-REQ-001, IF03-REQ-002, IF03-REQ-004

Start SI-01 with synthetic configuration and verify version/status plus reconnect
behaviour through the public application interface.
\`\`\`
