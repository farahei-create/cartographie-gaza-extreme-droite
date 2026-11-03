/* Cartographie des déclarations publiques — script principal (sans étape de build). */
(function () {
  "use strict";

  var THEME_ORDER = ["Gaza – déclarations", "Proximité extrême droite", "Nuance / contexte"];
  var THEME_CLASS = { "Gaza – déclarations": "t-gaza", "Proximité extrême droite": "t-ed", "Nuance / contexte": "t-nuance" };
  var NO_STATEMENT = "__none__";

  var TYPES = {
    person:      { label: "Personne",            color: "#3b5b7a", shape: "dot",      size: 14 },
    parti:       { label: "Parti / mouvement",   color: "#8a6a3b", shape: "diamond",  size: 15 },
    media:       { label: "Média / groupe média", color: "#4f7a64", shape: "square",   size: 12 },
    association: { label: "Association / organisation", color: "#6d6390", shape: "triangle", size: 13 },
    evenement:   { label: "Événement",           color: "#9a5b4b", shape: "star",     size: 15 },
    org:         { label: "Organisation (autre)", color: "#7a7a7a", shape: "box",      size: 12 }
  };

  /* Sous-type d'organisation déduit du champ « role » (aucune donnée modifiée). */
  function subtype(n) {
    if (n.type === "person") return "person";
    var r = (n.role || "").toLowerCase();
    if (/[ée]v[ée]nement/.test(r)) return "evenement";
    if (/parti|mouvement politique|groupe parlementaire/.test(r)) return "parti";
    if (/m[ée]dia|cha[iî]ne|radio|hebdomadaire|magazine|quotidien|journal|t[ée]l[ée]vision/.test(r)) return "media";
    if (/association|organisation|fondation|comit[ée]/.test(r)) return "association";
    return "org";
  }

  /* ---------- utilitaires ---------- */
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  var MONTHS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];
  function fmtDate(d) {
    if (!d) return "date non précisée";
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(d);
    if (!m) return esc(d);
    var day = parseInt(m[3], 10);
    return (day === 1 ? "1er" : day) + " " + MONTHS[parseInt(m[2], 10) - 1] + " " + m[1];
  }
  function quoteHtml(q) { return "«\u00a0" + esc(q) + "\u00a0»"; }
  function srcLink(url, text) {
    if (!url) return '<span class="empty">source non renseignée</span>';
    var host = "";
    try { host = new URL(url).hostname.replace(/^www\./, ""); } catch (e) { host = url; }
    return '<a class="src" href="' + esc(url) + '" target="_blank" rel="noopener noreferrer">' + esc(text || ("Source : " + host)) + "</a>";
  }
  function themeTag(t) { return '<span class="theme ' + (THEME_CLASS[t] || "") + '">' + esc(t) + "</span>"; }
  function norm(s) { return String(s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); }
  function $(id) { return document.getElementById(id); }

  /* ---------- état ---------- */
  var DATA, byId = {}, edgesOf = {}, themes = [], network, nodesDS, edgesDS;
  var state = { themes: {}, types: {}, search: "" };

  fetch("data.json", { cache: "no-cache" })
    .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
    .then(init)
    .catch(function (e) {
      $("graph").innerHTML = '<p style="padding:20px">Impossible de charger <code>data.json</code> (' + esc(e.message) +
        "). Ouvrez le site via un serveur web (par exemple <code>python3 -m http.server</code>).</p>";
    });

  function init(data) {
    DATA = data;
    data.nodes.forEach(function (n) { n._sub = subtype(n); byId[n.id] = n; edgesOf[n.id] = []; });
    data.edges.forEach(function (e, i) {
      e._id = "e" + i;
      if (edgesOf[e.source]) edgesOf[e.source].push(e);
      if (edgesOf[e.target]) edgesOf[e.target].push(e);
    });
    var seen = {};
    data.nodes.forEach(function (n) { (n.statements || []).forEach(function (s) { if (s.theme) seen[s.theme] = 1; }); });
    themes = THEME_ORDER.filter(function (t) { return seen[t]; })
      .concat(Object.keys(seen).filter(function (t) { return THEME_ORDER.indexOf(t) < 0; }).sort());

    fillMeta();
    buildFilters();
    buildGraph();
    buildList();
    bindTabs();
  }

  function fillMeta() {
    var m = DATA.meta || {};
    var upd = m.generated ? fmtDate(m.generated) : "—";
    $("last-update").textContent = upd;
    $("footer-update").textContent = upd;
    if (m.methodology) $("meta-methodology").textContent = m.methodology;
    var c = m.counts || {};
    var persons = DATA.nodes.filter(function (n) { return n.type === "person"; }).length;
    var stm = DATA.nodes.reduce(function (a, n) { return a + (n.statements || []).length; }, 0);
    $("meta-counts").textContent = "Contenu : " + (c.persons || persons) + " personnes, " +
      (c.orgs || (DATA.nodes.length - persons)) + " organisations ou événements, " +
      (c.statements || stm) + " déclarations et " + (c.edges || DATA.edges.length) + " relations sourcées.";
  }

  /* ---------- filtres ---------- */
  function chip(container, key, label, color, group) {
    var id = "f-" + group + "-" + norm(key).replace(/[^a-z0-9]+/g, "-");
    var l = document.createElement("label");
    l.className = "chip";
    l.innerHTML = '<input type="checkbox" checked id="' + id + '"> ' +
      (color ? '<span class="sw" style="background:' + color + '"></span>' : "") + esc(label);
    l.querySelector("input").addEventListener("change", function (ev) {
      state[group][key] = ev.target.checked; applyFilters();
    });
    container.appendChild(l);
    state[group][key] = true;
  }
  function buildFilters() {
    var tf = $("theme-filters");
    themes.forEach(function (t) { chip(tf, t, t, null, "themes"); });
    chip(tf, NO_STATEMENT, "Sans déclaration (liens seuls)", null, "themes");
    var present = {};
    DATA.nodes.forEach(function (n) { present[n._sub] = 1; });
    var ty = $("type-filters");
    Object.keys(TYPES).forEach(function (k) { if (present[k]) chip(ty, k, TYPES[k].label, TYPES[k].color, "types"); });

    var dl = $("node-names");
    DATA.nodes.slice().sort(function (a, b) { return a.name.localeCompare(b.name, "fr"); }).forEach(function (n) {
      var o = document.createElement("option"); o.value = n.name; dl.appendChild(o);
    });
    var inp = $("graph-search");
    inp.addEventListener("input", function () {
      state.search = inp.value; applyFilters();
      var exact = DATA.nodes.filter(function (n) { return norm(n.name) === norm(inp.value); })[0];
      if (exact) focusNode(exact.id);
    });
    inp.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter") {
        var m = matches(); if (m.length) focusNode(m[0].id);
      }
    });
    $("btn-fit").addEventListener("click", function () { network.fit({ animation: { duration: 400 } }); });
    $("btn-reset").addEventListener("click", function () {
      document.querySelectorAll("#theme-filters input, #type-filters input").forEach(function (i) { i.checked = true; });
      Object.keys(state.themes).forEach(function (k) { state.themes[k] = true; });
      Object.keys(state.types).forEach(function (k) { state.types[k] = true; });
      inp.value = ""; state.search = ""; closePanel(); applyFilters();
      network.fit({ animation: { duration: 400 } });
    });

    // Légende
    var lg = $("legend");
    Object.keys(TYPES).forEach(function (k) {
      if (!present[k]) return;
      var t = TYPES[k], shape;
      switch (t.shape) {
        case "dot": shape = '<circle cx="7" cy="7" r="6"/>'; break;
        case "diamond": shape = '<polygon points="7,0 14,7 7,14 0,7"/>'; break;
        case "square": shape = '<rect x="1" y="1" width="12" height="12"/>'; break;
        case "triangle": shape = '<polygon points="7,1 13,13 1,13"/>'; break;
        case "star": shape = '<polygon points="7,0 9,5 14,5 10,8.5 11.5,14 7,10.5 2.5,14 4,8.5 0,5 5,5"/>'; break;
        default: shape = '<rect x="0" y="3" width="14" height="8" rx="2"/>';
      }
      lg.insertAdjacentHTML("beforeend", '<div class="it"><svg width="14" height="14" fill="' + t.color + '" aria-hidden="true">' + shape + "</svg>" + esc(t.label) + "</div>");
    });
  }

  function nodeText(n) {
    var parts = [n.name, n.role, n.description];
    (n.statements || []).forEach(function (s) { parts.push(s.quote, s.medium); });
    return norm(parts.join(" "));
  }
  function matches() {
    var q = norm(state.search).trim();
    if (!q) return [];
    return DATA.nodes.filter(function (n) { return norm(n.name).indexOf(q) >= 0 || norm(n.role).indexOf(q) >= 0; });
  }

  function personVisibleByTheme(n) {
    var st = n.statements || [];
    if (!st.length) return !!state.themes[NO_STATEMENT];
    return st.some(function (s) { return state.themes[s.theme]; });
  }

  function visibleSet() {
    var vis = {};
    // 1) personnes selon thème et type
    DATA.nodes.forEach(function (n) {
      if (n.type === "person" && state.types.person && personVisibleByTheme(n)) vis[n.id] = true;
    });
    // 2) organisations : visibles si leur type est coché et reliées à un nœud visible (ou à une autre org visible)
    var changed = true, guard = 0;
    while (changed && guard++ < 10) {
      changed = false;
      DATA.nodes.forEach(function (n) {
        if (n.type === "person" || vis[n.id] || !state.types[n._sub]) return;
        var linked = edgesOf[n.id].some(function (e) { var o = e.source === n.id ? e.target : e.source; return vis[o]; });
        var noPeopleShown = !Object.keys(vis).length;
        if (linked || noPeopleShown) { vis[n.id] = true; changed = true; }
      });
    }
    return vis;
  }

  function applyFilters() {
    var vis = visibleSet();
    var q = norm(state.search).trim();
    var m = {}; matches().forEach(function (n) { m[n.id] = true; });
    nodesDS.update(DATA.nodes.map(function (n) {
      var dim = q && !m[n.id];
      return { id: n.id, hidden: !vis[n.id], opacity: dim ? 0.2 : 1, font: { color: dim ? "rgba(29,34,40,0.25)" : "#1d2228" } };
    }));
    edgesDS.update(DATA.edges.map(function (e) {
      var dim = q && !(m[e.source] || m[e.target]);
      return { id: e._id, hidden: !(vis[e.source] && vis[e.target]), color: { color: dim ? "rgba(150,150,150,0.15)" : "#b9b6ae", highlight: "#2f4f6f", hover: "#2f4f6f" } };
    }));
  }

  /* ---------- graphe ---------- */
  function sizeGraph() {
    var gl = document.querySelector(".graph-layout");
    if (!gl || window.matchMedia("(max-width: 860px)").matches) { if (gl) gl.style.height = ""; return; }
    var top = gl.getBoundingClientRect().top + window.scrollY;
    gl.style.height = Math.max(480, window.innerHeight - top) + "px";
  }
  window.addEventListener("resize", sizeGraph);

  function buildGraph() {
    sizeGraph();
    var nodes = DATA.nodes.map(function (n) {
      var t = TYPES[n._sub], deg = edgesOf[n.id].length;
      return {
        id: n.id, label: n.name, shape: t.shape,
        size: t.size + Math.min(deg, 12),
        color: { background: t.color, border: "#ffffff", highlight: { background: t.color, border: "#1d2228" }, hover: { background: t.color, border: "#1d2228" } },
        borderWidth: 2, borderWidthSelected: 3,
        font: { face: "system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif", size: n.type === "person" ? 20 : 17, color: "#1d2228", strokeWidth: 4, strokeColor: "#ffffff" },
        title: tooltip(n.name + " — " + n.role)
      };
    });
    var edges = DATA.edges.map(function (e) {
      return {
        id: e._id, from: e.source, to: e.target,
        arrows: { to: { enabled: true, scaleFactor: 0.45 } },
        width: 1.2, hoverWidth: 1.5, selectionWidth: 2,
        color: { color: "#b9b6ae", highlight: "#2f4f6f", hover: "#2f4f6f" },
        smooth: { type: "continuous" },
        title: tooltip(byId[e.source].name + " → " + byId[e.target].name + "\n" + e.relation + (e.date ? " (" + fmtDate(e.date) + ")" : "") + "\nCliquez pour afficher la source")
      };
    });
    nodesDS = new vis.DataSet(nodes);
    edgesDS = new vis.DataSet(edges);
    network = new vis.Network($("graph"), { nodes: nodesDS, edges: edgesDS }, {
      autoResize: true,
      interaction: { hover: true, tooltipDelay: 120, navigationButtons: false, keyboard: { enabled: true, bindToWindow: false }, multiselect: false },
      physics: {
        solver: "forceAtlas2Based",
        forceAtlas2Based: { gravitationalConstant: -45, centralGravity: 0.015, springLength: 80, springConstant: 0.06, avoidOverlap: 0.6 },
        stabilization: { iterations: 400, fit: true }
      },
      layout: { randomSeed: 7, improvedLayout: true }
    });
    network.once("stabilizationIterationsDone", function () {
      network.setOptions({ physics: { enabled: false } });
      network.fit();
      window.__graphReady = true;
      /* aide aux tests automatisés : position DOM d'un nœud */
      window.__nodeDOM = function (id) { var p = network.getPositions([id])[id]; return p ? network.canvasToDOM(p) : null; };
    });
    network.on("click", function (p) {
      if (p.nodes.length) {
        openNode(p.nodes[0], false);
        var nid = p.nodes[0];
        setTimeout(function () { network.focus(nid, { scale: Math.max(network.getScale(), 0.9), animation: { duration: 400 } }); }, 30);
      }
      else if (p.edges.length) openEdge(p.edges[0]);
    });
    $("panel-close").addEventListener("click", closePanel);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closePanel(); });
    applyFilters();
  }
  function tooltip(text) {
    var d = document.createElement("div");
    d.textContent = text;
    d.style.whiteSpace = "pre-line";
    return d;
  }

  function focusNode(id) {
    if (!network) return;
    var n = nodesDS.get(id);
    if (n && n.hidden) {
      // rendre visible en levant les filtres qui le masquent
      document.querySelectorAll("#theme-filters input, #type-filters input").forEach(function (i) { i.checked = true; });
      Object.keys(state.themes).forEach(function (k) { state.themes[k] = true; });
      Object.keys(state.types).forEach(function (k) { state.types[k] = true; });
      applyFilters();
    }
    network.selectNodes([id]);
    network.focus(id, { scale: 1.2, animation: { duration: 500, easingFunction: "easeInOutQuad" } });
    openNode(id, true);
  }

  /* ---------- panneau latéral ---------- */
  function statementsHtml(n, themeFilter) {
    var st = (n.statements || []).filter(function (s) { return !themeFilter || s.theme === themeFilter; });
    if (!st.length) return '<p class="empty">Aucune déclaration répertoriée.</p>';
    return '<ul class="stmts">' + st.map(function (s) {
      return '<li class="stmt"><blockquote>' + quoteHtml(s.quote) + "</blockquote>" +
        '<div class="meta"><span>' + fmtDate(s.date) + "</span><span>· " + esc(s.medium) + "</span>" + (s.theme ? themeTag(s.theme) : "") + "</div>" +
        '<div class="meta">' + srcLink(s.url, "Lire la source") + "</div></li>";
    }).join("") + "</ul>";
  }
  function relationsHtml(n, asButtons) {
    var es = edgesOf[n.id];
    if (!es.length) return '<p class="empty">Aucune relation répertoriée.</p>';
    return '<ul class="rels">' + es.map(function (e) {
      var out = e.source === n.id, other = byId[out ? e.target : e.source];
      var who = asButtons ? '<button type="button" class="link" data-node="' + esc(other.id) + '">' + esc(other.name) + "</button>" : '<span class="who">' + esc(other.name) + "</span>";
      var sentence = out
        ? esc(n.name) + " → " + who + " : " + esc(e.relation)
        : who + " → " + esc(n.name) + " : " + esc(e.relation);
      return '<li class="rel">' + sentence + '<div class="meta">' + (e.date ? fmtDate(e.date) + " · " : "") + srcLink(e.url) + "</div></li>";
    }).join("") + "</ul>";
  }
  function openNode(id, fromSearch) {
    var n = byId[id]; if (!n) return;
    var t = TYPES[n._sub];
    $("panel-body").innerHTML =
      '<span class="badge" style="background:' + t.color + '1f;color:' + t.color + '">' + esc(t.label) + "</span>" +
      "<h2>" + esc(n.name) + "</h2>" +
      '<p class="role">' + esc(n.role) + "</p>" +
      (n.description ? "<p>" + esc(n.description) + "</p>" : "") +
      (n.type === "person" || (n.statements || []).length ? "<h3>Déclarations publiques (" + (n.statements || []).length + ")</h3>" + statementsHtml(n) : "") +
      "<h3>Relations (" + edgesOf[id].length + ")</h3>" + relationsHtml(n, true);
    showPanel();
    if (!fromSearch && network) network.selectNodes([id]);
    if (location.hash.indexOf("#graphe") === 0 || !location.hash) history.replaceState(null, "", "#graphe/" + encodeURIComponent(id));
  }
  function openEdge(eid) {
    var e = DATA.edges.filter(function (x) { return x._id === eid; })[0]; if (!e) return;
    $("panel-body").innerHTML = '<span class="badge">Relation</span><h2>' + esc(byId[e.source].name) + " → " + esc(byId[e.target].name) + "</h2>" +
      '<p class="role">' + esc(e.relation) + "</p>" +
      '<p class="meta">' + fmtDate(e.date) + "</p><p>" + srcLink(e.url, "Lire la source") + "</p>" +
      '<h3>Voir</h3><ul class="rels"><li class="rel"><button type="button" class="link" data-node="' + esc(e.source) + '">' + esc(byId[e.source].name) + '</button></li><li class="rel"><button type="button" class="link" data-node="' + esc(e.target) + '">' + esc(byId[e.target].name) + "</button></li></ul>";
    showPanel();
  }
  function showPanel() {
    var p = $("panel"); p.hidden = false; p.scrollTop = 0;
    p.querySelectorAll("button.link[data-node]").forEach(function (b) {
      b.addEventListener("click", function () { focusNode(b.getAttribute("data-node")); });
    });
  }
  function closePanel() {
    $("panel").hidden = true;
    if (network) network.unselectAll();
    if (location.hash.indexOf("#graphe/") === 0) history.replaceState(null, "", "#graphe");
  }

  /* ---------- liste ---------- */
  function buildList() {
    var sel = $("list-theme");
    themes.forEach(function (t) { var o = document.createElement("option"); o.value = t; o.textContent = t; sel.appendChild(o); });
    var people = DATA.nodes.filter(function (n) { return n.type === "person"; })
      .sort(function (a, b) { return a.name.split(" ").slice(-1)[0].localeCompare(b.name.split(" ").slice(-1)[0], "fr"); });
    var body = $("people-body");
    body.innerHTML = people.map(function (n) {
      return '<tr data-id="' + esc(n.id) + '">' +
        '<td data-label="Personne"><p class="name" id="p-' + esc(n.id) + '">' + esc(n.name) + '</p><p class="role">' + esc(n.role) + "</p>" +
        (n.description ? '<p class="desc">' + esc(n.description) + "</p>" : "") +
        '<p class="desc"><a href="#graphe/' + encodeURIComponent(n.id) + '">Voir dans l\'arbre</a></p></td>' +
        '<td data-label="Déclarations publiques" class="st-cell"></td>' +
        '<td data-label="Relations">' + relationsHtml(n, false) + "</td></tr>";
    }).join("");
    var texts = {};
    people.forEach(function (n) {
      texts[n.id] = nodeText(n) + " " + norm(edgesOf[n.id].map(function (e) { return e.relation + " " + byId[e.source].name + " " + byId[e.target].name; }).join(" "));
    });
    function render() {
      var q = norm($("list-search").value).trim(), th = sel.value, shown = 0;
      body.querySelectorAll("tr").forEach(function (tr) {
        var n = byId[tr.getAttribute("data-id")];
        var okTheme = !th || (n.statements || []).some(function (s) { return s.theme === th; });
        var ok = okTheme && (!q || texts[n.id].indexOf(q) >= 0);
        tr.hidden = !ok;
        if (ok) { shown++; tr.querySelector(".st-cell").innerHTML = statementsHtml(n, th); }
      });
      $("list-count").textContent = shown + " personne" + (shown > 1 ? "s" : "") + " affichée" + (shown > 1 ? "s" : "") + " sur " + people.length + ".";
    }
    $("list-search").addEventListener("input", render);
    sel.addEventListener("change", render);
    render();
  }

  /* ---------- onglets ---------- */
  function bindTabs() {
    function route() {
      var h = location.hash.replace(/^#/, "");
      var parts = h.split("/"), tab = parts[0] || "graphe";
      if (["graphe", "liste", "methodologie"].indexOf(tab) < 0) tab = "graphe";
      ["graphe", "liste", "methodologie"].forEach(function (t) {
        $("view-" + t).hidden = t !== tab;
        $("tab-" + t).setAttribute("aria-selected", t === tab ? "true" : "false");
      });
      if (tab === "graphe" && network) {
        sizeGraph(); network.redraw();
        if (parts[1]) {
          var id = decodeURIComponent(parts[1]);
          if (byId[id]) setTimeout(function () { focusNode(id); }, 50);
        }
      }
    }
    window.addEventListener("hashchange", route);
    route();
  }
})();
