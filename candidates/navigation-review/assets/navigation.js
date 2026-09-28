(() => {
  const data = JSON.parse(document.getElementById("navigation-data").textContent);
  const inspector = document.getElementById("inspector");
  const hitNodes = [...document.querySelectorAll("[data-engineering-id]")];
  const stage = document.querySelector("[data-zoom-stage]");

  const byId = data.objects;

  function esc(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  function titleFor(id) {
    const obj = byId[id];
    return obj ? obj.title : id;
  }

  function typeFor(id) {
    const obj = byId[id];
    return obj ? obj.type : "engineering object";
  }

  function sourceRow(id) {
    const source = data.source_index[id];
    if (!source) return "";
    const anchor = source.stable_anchor
      ? ""
      : '<span class="anchor-note">pinned line link · stable object anchor still needed</span>';
    return '<div class="source-row">' +
      '<a class="source-link" href="' + esc(source.url) + '" target="_blank" rel="noreferrer">Open authoritative source ↗</a>' +
      anchor +
      "</div>";
  }

  function chips(ids, cssClass = "") {
    if (!ids || !ids.length) return '<p>None in this qualified slice.</p>';
    return '<div class="chips">' + ids.map(id =>
      '<button type="button" class="chip ' + cssClass + '" data-open-object="' + esc(id) + '">' +
      esc(id) + " · " + esc(titleFor(id)) +
      "</button>"
    ).join("") + "</div>";
  }

  function setDiagramHighlights(selectedIds, relatedIds = []) {
    const selected = new Set(selectedIds);
    const related = new Set(relatedIds);
    hitNodes.forEach(node => {
      const id = node.dataset.engineeringId;
      node.classList.toggle("is-selected", selected.has(id));
      node.classList.toggle("is-related", !selected.has(id) && related.has(id));
    });
  }

  function header(id) {
    return '<div class="object-head">' +
      '<p class="object-type">' + esc(typeFor(id)) + "</p>" +
      "<h2>" + esc(id) + " · " + esc(titleFor(id)) + "</h2>" +
      sourceRow(id) +
      "</div>";
  }

  function renderArchitecture(id) {
    const context = data.architecture_context[id] || {
      use_cases: [], requirements: [], verification: []
    };
    setDiagramHighlights([id]);

    inspector.innerHTML = header(id) +
      '<section class="context-section"><h3>Related use cases</h3>' +
      '<p>Derived through requirements allocated to this architecture element.</p>' +
      chips(context.use_cases) + "</section>" +
      '<section class="context-section"><h3>Allocated requirements / interface obligations</h3>' +
      chips(context.requirements, "requirement") + "</section>" +
      '<section class="context-section"><h3>Verification reached through those requirements</h3>' +
      chips(context.verification, "verification") + "</section>";

    wireInspector();
  }

  function renderUseCase(id) {
    const context = data.use_case_context[id] || {
      architecture: [], requirements: [], verification: []
    };
    const clickableArchitecture = context.architecture.filter(
      item => data.diagram_identity[item]
    );
    setDiagramHighlights([], clickableArchitecture);

    inspector.innerHTML = header(id) +
      '<section class="context-section"><h3>Architecture context</h3>' +
      '<p>The diagram stays visible while this real use-case narrative is open.</p>' +
      chips(clickableArchitecture, "architecture") + "</section>" +
      '<section class="context-section"><h3>Derived requirements</h3>' +
      chips(context.requirements, "requirement") + "</section>" +
      '<section class="context-section"><h3>Verification</h3>' +
      chips(context.verification, "verification") + "</section>" +
      '<article class="narrative">' + (data.use_case_html[id] || "<p>Narrative not mirrored in this slice.</p>") + "</article>";

    wireInspector();
  }

  function renderGeneric(id) {
    const obj = byId[id];
    if (!obj) return;
    const outgoing = (obj.relations || []).map(rel => rel.target);
    const incoming = (obj.incoming || []).map(rel => rel.source);
    setDiagramHighlights(data.diagram_identity[id] ? [id] : []);

    inspector.innerHTML = header(id) +
      '<section class="context-section"><h3>Outgoing relationships</h3>' +
      chips(outgoing) + "</section>" +
      '<section class="context-section"><h3>Generated backlinks</h3>' +
      chips(incoming) + "</section>";

    wireInspector();
  }

  function openObject(id) {
    if (!byId[id]) return;
    if (byId[id].type === "use-case") renderUseCase(id);
    else if (data.diagram_identity[id]) renderArchitecture(id);
    else renderGeneric(id);

    const url = new URL(window.location.href);
    url.searchParams.set("object", id);
    history.replaceState(null, "", url);
  }

  function wireInspector() {
    inspector.querySelectorAll("[data-open-object]").forEach(button => {
      button.addEventListener("click", () => openObject(button.dataset.openObject));
    });
  }

  hitNodes.forEach(node => {
    const open = () => openObject(node.dataset.engineeringId);
    node.addEventListener("click", open);
    node.addEventListener("keydown", event => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        open();
      }
    });
  });

  document.querySelectorAll("[data-zoom]").forEach(button => {
    button.addEventListener("click", () => {
      const mode = button.dataset.zoom;
      if (mode === "fit") stage.style.width = "100%";
      else if (mode === "native") stage.style.width = "1540px";
      else stage.style.width = mode + "%";
    });
  });

  const requested = new URL(window.location.href).searchParams.get("object");
  openObject(requested && byId[requested] ? requested : "TimingNode");
})();
