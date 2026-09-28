# Authoring fixture — compact metadata

Source authority: `brainboxemb/2026-010-01.meta.event-timing-software@15f15c751d054f6a6af5e3478f5f9a85d046712c`

This file deliberately keeps the visible engineering prose close to the current
event-timing Markdown. Engineering metadata is carried in hidden HTML comments
immediately below the owning heading.

## UC-001 — Start and prepare a TimingNode

<!-- eng
{
  "type": "use-case",
  "relations": {
    "related_to": ["TimingNode", "CommandHandler"],
    "derived_to": ["SI01-REQ-003", "SI01-REQ-020", "SI01-REQ-021", "SI01-REQ-022"],
    "verified_by": ["VC-ST1-001"]
  }
}
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
4. RFID equipment that is required for the instance goes through power-on and initialisation.
5. SI-01 reports individual device/subsystem readiness rather than hiding startup progress behind one boolean.
6. The instance becomes ready for the operator to open when required operational prerequisites are satisfied.

**Alternative/failure flows:**

- an RFID device does not boot or initialise;
- a CAN device is not discovered;
- required reference data is unavailable/stale;
- persistence/restore is unhealthy;
- network/backoffice is unavailable while local operation may still remain possible.

**Relevant interfaces:** IF-01/02/03, IF-07, IF-08, status model.

## UC-014 — Run multiple TimingNodes in one process

<!-- eng
{
  "type": "use-case",
  "relations": {
    "related_to": ["TimingNode", "CommandHandler"],
    "derived_to": ["SI01-REQ-003"],
    "verified_by": ["VC-ST1-001"]
  }
}
-->

**Goal:** host multiple independently addressed TimingNodes while preserving
independent lifecycle, state and `TimingNodeId`-scoped streams.

**Primary actor:** configuration/test/operator tooling.

**Main flow:**

1. Settings describe several independently addressed `TimingNode` objects and their location/timing node identity mappings.
2. Each instance receives its own logical serialized state boundary.
3. Deployment configuration routes each producer/asset/antenna origin to one or more applicable `TimingNodeId` targets without making those hardware objects children of the `TimingNode` software model.
4. Runtime-wide infrastructure may be shared without sharing mutable instance state.
5. Public interfaces can address each instance explicitly.

## TimingNode

<!-- eng
{
  "type": "architecture-element",
  "relations": {
    "related_to": ["CommandHandler"],
    "allocated_from": ["SI01-REQ-003", "SI01-REQ-020", "SI01-REQ-021", "SI01-REQ-022"]
  }
}
-->

A `TimingNode` is the primary independently addressed operational/domain
aggregate inside SI-01. One application process may host one or more TimingNodes.

## CommandHandler

<!-- eng
{
  "type": "architecture-element",
  "relations": {
    "related_to": ["TimingNode"],
    "allocated_from": ["SI01-REQ-030", "SI01-REQ-031"]
  }
}
-->

`CommandHandler` is the shared entry point for presentation requests and keeps
presentation interfaces from reaching directly into domain internals.

## SI01-REQ-020 — Authoritative current status snapshot

<!-- eng
{
  "type": "requirement",
  "relations": {
    "derived_from": ["UC-001"],
    "allocated_to": ["TimingNode", "IF03-REQ-004"],
    "verified_by": ["VC-ST1-001"]
  }
}
-->

The application shall expose one authoritative current status snapshot.

## IF03-REQ-004 — Status query

<!-- eng
{
  "type": "interface-requirement",
  "relations": {
    "derived_from": ["SI01-REQ-020"],
    "related_to": ["CommandHandler"],
    "verified_by": ["VC-ST1-001"]
  }
}
-->

The Remote API shall provide the current status query.

## VC-ST1-001 — Query and resynchronise first-executable status

<!-- eng
{
  "type": "verification-case",
  "relations": {
    "verifies": ["SI01-REQ-003", "SI01-REQ-020", "IF03-REQ-004"]
  }
}
-->

Start SI-01 with synthetic configuration, query version/status, connect and
reconnect the event stream, and verify the current state can be reconstructed.
