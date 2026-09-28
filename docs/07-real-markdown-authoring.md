# Real Markdown authoring qualification

## Scope

Experiment 007 issue #9 evaluates how real BrainboxEmb engineering Markdown can
participate in the engineering graph without making normal project
documentation subordinate to Sphinx/MyST syntax.

Reference authority is pinned to:

`brainboxemb/2026-010-01.meta.event-timing-software@15f15c751d054f6a6af5e3478f5f9a85d046712c`

The qualified slice contains 19 engineering objects:

- use cases: `UC-001`, `UC-008`, `UC-014`;
- document-section sources: `SAD-TESTABILITY`, `SVP-ST-1`;
- architecture elements: `TimingNode`, `CommandHandler`, `Conductor`,
  `RemoteApi`;
- software requirements: `SI01-REQ-003/020/021/022/030/031`;
- interface requirements: `IF03-REQ-001/002/004`;
- verification case: `VC-ST1-001`.

Primary qualification run:

`36384556756`

Retained human-review artifact:

`authoring-review-output` — artifact `10954305681`

The run is green for:

- compact Markdown extraction/validation;
- sidecar extraction/validation;
- semantic equality between compact and sidecar forms;
- native MyST/Sphinx-Needs validation;
- generated backlinks;
- bad-link diagnostics;
- human-review site generation.

## Finding 1 — the first graph policy was too narrow

The first eight-object PoP assumed every software requirement had an upstream
use case.

The real event-timing traceability disproves that assumption.

For example:

- `SI01-REQ-030` is sourced from the SAD testability architecture;
- `SI01-REQ-031` is sourced from SAD testability and the SVP ST-1 profile.

The graph therefore now permits a `document-section` object as a legitimate
upstream requirement source.

This is a useful distinction:

```text
use case
    |
    +-------> requirement

document / architecture / verification section
    |
    +-------> requirement
```

Traceability should describe the actual engineering origin rather than forcing
every obligation through a use-case shape.

The original Sphinx-Needs schema was similarly overfit to the small fixture.
The real-source control configuration proves Sphinx-Needs can model the broader
rule once the schema is corrected.

## Finding 2 — stable IDs are not the same as stable deep links

The current event-timing use cases are Markdown headings such as:

```text
## UC-001 — Start and prepare a TimingNode
```

They naturally receive a browser anchor.

Current SI01/IF03 requirement identities are normally written as bold text:

```text
**SI01-REQ-020 — Authoritative current status snapshot**
```

That text has a stable engineering ID but does not create an object-level
Markdown heading anchor.

For an interactive documentation system this matters. A generated object page
must be able to return to the exact authoritative source object, not merely the
top of a large SRD/IDD file.

The experiment therefore adds a minimal explicit anchor beside such objects:

```html
<a id="SI01-REQ-020"></a>
```

The compact and sidecar fixtures each need 9 such anchor lines for the selected
SI01/IF03 objects.

A production convention may choose another syntax, but object-level deep-link
identity must be explicit where the document structure does not already provide
it.

## Finding 3 — author relations once

The larger slice confirms that inverse traceability should not be authored.

For example, the requirement owns:

```text
SI01-REQ-020
  source       -> UC-001
  source       -> UC-008
  allocated_to -> TimingNode
  allocated_to -> IF03-REQ-004
  verified_by  -> VC-ST1-001
```

The system generates the inverse views:

```text
UC-001
  incoming requirement <- SI01-REQ-020

TimingNode
  allocated requirement <- SI01-REQ-020

VC-ST1-001
  verifies <- SI01-REQ-020
```

This removes the need to keep manually authored use-case matrices, architecture
allocation tables and verification backlinks synchronized.

The compact and sidecar variants produce the same normalized object types,
titles, outgoing relations and generated incoming relations.

## Candidate A — native MyST / Sphinx-Needs

### Result

Technically qualified.

The 19-object native fixture passes a real Sphinx-Needs build including:

- use cases;
- document sections;
- requirements;
- interface requirements;
- architecture elements;
- verification;
- typed links and generated backlinks.

### Authoring impact

The engineering prose lives inside directives such as:

```text
```{req} Authoritative current status snapshot
:id: SI01-REQ-020
:derived_from: UC-001, UC-008
:allocated_to: TimingNode, IF03-REQ-004
:verified_by: VC-ST1-001

SI-01 shall maintain ...
```
```

This is natural inside a Sphinx/MyST documentation system.

It is a weaker fit for BrainboxEmb's current requirement that authored Markdown
remain pleasant to read and review directly on GitHub. A normal Markdown
renderer sees the directive as a fenced block rather than ordinary engineering
prose.

### Conclusion

**Strong engine fit, poor default production authoring fit.**

Sphinx-Needs remains a viable validation/relationship/export engine. Experiment
007 does not recommend making native MyST need directives the normal authored
form for the current project family.

## Candidate B — sidecar metadata

### Result

Technically qualified.

The sidecar document contains ordinary Markdown and produces exactly the same
graph semantics as the compact variant.

Measured fixture size:

- Markdown document: 168 lines;
- sidecar metadata: 197 additional JSON lines;
- total authored material across the pair: 365 lines;
- 19 objects.

### Strength

The prose file is visually clean.

### Weakness

The relationship meaning is separated from the engineering object it describes.

Changing a requirement can require the reviewer to notice that a second file
must also change. File moves, renames and new/removed objects can drift from the
sidecar even though both files remain syntactically valid.

Stable source anchors still need to exist in the Markdown itself. The sidecar
therefore does not remove all authoring conventions from the document.

### Conclusion

**Technically clean, but unnecessarily high synchronization risk for the default
case.**

A sidecar remains useful when metadata genuinely belongs outside a source file,
for example cross-repository retained evidence or generated/imported relations.
It is not the preferred default place for ordinary requirement/use-case/design
relationships.

## Candidate C — compact metadata beside normal Markdown

### Result

Technically qualified.

The compact fixture contains:

- 225 total lines;
- 57 hidden metadata lines;
- 19 objects;
- 9 explicit source-anchor lines.

The metadata is adjacent to the owning object and disappears from normal
rendered documentation.

Example:

```text
<a id="SI01-REQ-020"></a>
**SI01-REQ-020 — Authoritative current status snapshot**

<!-- eng
{"type":"requirement","relations":{
  "source":["UC-001","UC-008"],
  "allocated_to":["TimingNode","IF03-REQ-004"],
  "verified_by":["VC-ST1-001"]
}}
-->

SI-01 shall maintain an authoritative current application status model ...
```

The exact JSON-comment syntax is experimental. The qualified property is the
**authoring architecture**:

- normal Markdown owns the narrative;
- stable object identity remains visible/close to the source;
- a small project-owned metadata fragment sits beside the object;
- a generic extractor normalizes it into the engineering graph;
- generated views/backlinks do not become authored source.

### Conclusion

**Best fit of the three evaluated authoring shapes.**

It preserves ordinary rendered Markdown while keeping relationships close
enough to the owning text to review together.

## Qualified authoring direction

Experiment 007 selects the following direction for the next PoP:

```text
normal project Markdown
    |
    +-- stable object identity / anchor
    |
    +-- small adjacent project-owned relation metadata
            |
            v
      generic extractor
            |
            v
      engineering graph
            |
      +-----+----------------------+
      |                            |
      v                            v
validation/backlinks          reader views
(Sphinx-Needs or             (Material portal /
 smaller graph engine)        object/workspace)
```

This deliberately does **not** yet select the final metadata syntax.

The next production-oriented design should minimize that syntax further and
decide which generic responsibilities belong in `tool.eng-docs`.

## Use cases as first-class navigation objects

The real-source slice also validates the intended use-case experience.

A use case does not need to duplicate a requirements matrix.

For example, `UC-001` receives generated incoming links from:

- `SI01-REQ-003`;
- `SI01-REQ-020`;
- `SI01-REQ-021`.

`UC-014` receives a generated incoming link from:

- `SI01-REQ-003`.

The readable use-case narrative remains authoritative for:

- goal;
- actors;
- preconditions;
- main flow;
- alternatives/failures.

The graph adds navigation around that narrative:

```text
             architecture
                  |
                  v
requirements <- UC-001 -> interfaces
                  |
                  v
             verification
```

That is preferable to turning the whole use case into structured database
fields.

## Production boundary

This is still experiment evidence.

No event-timing production document has been modified.

A later adoption track should decide:

1. the smallest production metadata syntax;
2. how explicit stable anchors are represented in existing SRD/IDD objects;
3. how diagram nodes receive the same engineering object IDs;
4. whether Sphinx-Needs remains behind the normalized graph boundary or a
   smaller generic validator is sufficient;
5. which extraction/generation mechanisms belong in `tool.eng-docs`;
6. how the Step 05 reader view is integrated into the Experiment 007 Pages site.
