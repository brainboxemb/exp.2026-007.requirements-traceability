# Authoring fixture — sidecar metadata

Source authority: `brainboxemb/2026-010-01.meta.event-timing-software@15f15c751d054f6a6af5e3478f5f9a85d046712c`

This variant keeps the visible Markdown completely free of engineering metadata.

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
4. The instance becomes ready for the operator to open when prerequisites are satisfied.

**Alternative/failure flows:**

- a required device does not initialise;
- required reference data is unavailable/stale;
- persistence/restore is unhealthy;
- network/backoffice is unavailable while local operation may still remain possible.

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

## TimingNode

A `TimingNode` is the primary independently addressed operational/domain
aggregate inside SI-01.

## CommandHandler

`CommandHandler` is the shared entry point for presentation requests.

## SI01-REQ-020 — Authoritative current status snapshot

The application shall expose one authoritative current status snapshot.

## IF03-REQ-004 — Status query

The Remote API shall provide the current status query.

## VC-ST1-001 — Query and resynchronise first-executable status

Start SI-01 with synthetic configuration, query version/status, connect and
reconnect the event stream, and verify the current state can be reconstructed.
