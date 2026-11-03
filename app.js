/* Cartographie des déclarations publiques — script principal (sans étape de build). */
(function () {
  "use strict";

  var THEME_FR = "France – normalisation de l'extrême droite";
  var THEME_ORDER = ["Gaza – déclarations", THEME_FR, "Proximité extrême droite", "Nuance / contexte"];
  var THEME_CLASS = { "Gaza – déclarations": "t-gaza", "Proximité extrême droite": "t-ed", "Nuance / contexte": "t-nuance" };
  THEME_CLASS[THEME_FR] = "t-fr";
  var SECTIONS = { gaza: "Gaza", france: "France – normalisation de l'extrême droite" };
  var CFG = window.SITE_CONFIG || {};
  var NO_STATEMENT = "__none__";

  /* Couleurs : lues dans les variables CSS (--c-*) pour suivre le mode clair / sombre. */
  var TYPES = {
    person:      { label: "Personne",            cssVar: "--c-person",      shape: "dot",      size: 14 },
    parti:       { label: "Parti / mouvement",   cssVar: "--c-parti",       shape: "diamond",  size: 15 },
    media:       { label: "Média / groupe média", cssVar: "--c-media",      shape: "square",   size: 12 },
    association: { label: "Association / organisation", cssVar: "--c-association", shape: "triangle", size: 13 },
    evenement:   { label: "Événement",           cssVar: "--c-evenement",   shape: "star",     size: 15 },
    org:         { label: "Organisation (autre)", cssVar: "--c-org",        shape: "box",      size: 12 }
  };
  var THEME_VAR = { "Gaza – déclarations": "--t-gaza", "Proximité extrême droite": "--t-ed", "Nuance / contexte": "--t-nuance" };
  THEME_VAR[THEME_FR] = "--t-fr";
  var FONT = "-apple-system, BlinkMacSystemFont, SF Pro Text, Inter, system-ui, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif";
  var MQ_MOBILE = window.matchMedia("(max-width: 860px)");
  var MQ_DARK = window.matchMedia("(prefers-color-scheme: dark)");
  var MQ_RM = window.matchMedia("(prefers-reduced-motion: reduce)");
  function anim(d) { return MQ_RM.matches ? false : { duration: d, easingFunction: "easeInOutCubic" }; }
  function cssv(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
  var PAL = {};
  function readPalette() {
    PAL = {
      bg: cssv("--g-bg"), edge: cssv("--g-edge"), edgeDim: cssv("--g-edge-dim"), label: cssv("--g-label"),
      labelDim: cssv("--g-label-dim"), border: cssv("--g-node-border"), shadow: cssv("--g-shadow"), accent: cssv("--accent"), types: {}
    };
    Object.keys(TYPES).forEach(function (k) { PAL.types[k] = cssv(TYPES[k].cssVar) || "#8e8e93"; });
  }

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
  function archLink(o) {
    if (!o || !o.archive_url) return "";
    return '<a class="arch" href="' + esc(o.archive_url) + '" target="_blank" rel="noopener noreferrer" title="Copie archivée (Wayback Machine)' + (o.archived ? ", " + fmtDate(o.archived) : "") + '">Archive' + (o.archived ? '<span class="arch-d"> · ' + esc(o.archived.slice(0, 4)) + "</span>" : "") + "</a>";
  }
  function themeTag(t) { return '<span class="theme ' + (THEME_CLASS[t] || "") + '">' + esc(t) + "</span>"; }
  function norm(s) { return String(s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); }
  function $(id) { return document.getElementById(id); }

  /* ---------- état ---------- */
  var DATA, byId = {}, edgesOf = {}, themes = [], network, nodesDS, edgesDS;
  var state = { themes: {}, types: {}, search: "" };
  var panelOpenedAt = 0;

  fetch("data.json", { cache: "no-cache" })
    .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
    .then(init)
    .catch(function (e) {
      $("main").insertAdjacentHTML("afterbegin", '<p style="padding:20px">Impossible de charger <code>data.json</code> (' + esc(e.message) +
        "). Ouvrez le site via un serveur web (par exemple <code>python3 -m http.server</code>).</p>");
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

    computeDerived();
    fillMeta();
    bindDonation();
    bindVideos();
    buildFilters();
    buildHome();
    buildSections();
    buildTimeline();
    bindFiche();
    bindRouter();
    registerSW();
  }

  /* Bouton « Soutenir ce travail » : affiché seulement si config.js renseigne DONATION_URL */
  function bindDonation() {
    var url = String(CFG.DONATION_URL || "").trim();
    var okUrl = /^https:\/\//i.test(url);
    document.querySelectorAll(".donate").forEach(function (a) {
      if (okUrl) { a.href = url; a.hidden = false; } else { a.hidden = true; a.removeAttribute("href"); }
    });
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
    l.className = "chip is-on" + (color ? "" : " no-sw");
    if (color) l.style.setProperty("--sw", color);
    l.innerHTML = '<input type="checkbox" checked id="' + id + '">' +
      (color ? '<span class="sw" aria-hidden="true"></span>' : '<svg class="ck" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>') +
      "<span>" + esc(label) + "</span>";
    l.querySelector("input").addEventListener("change", function (ev) {
      state[group][key] = ev.target.checked; applyFilters();
    });
    container.appendChild(l);
    state[group][key] = true;
  }
  function buildFilters() {
    var tf = $("theme-filters");
    themes.forEach(function (t) { chip(tf, t, t, THEME_VAR[t] ? "var(" + THEME_VAR[t] + ")" : null, "themes"); });
    chip(tf, NO_STATEMENT, "Sans déclaration (liens seuls)", null, "themes");
    var present = {};
    DATA.nodes.forEach(function (n) { present[n._sub] = 1; });
    var ty = $("type-filters");
    Object.keys(TYPES).forEach(function (k) { if (present[k]) chip(ty, k, TYPES[k].label, "var(" + TYPES[k].cssVar + ")", "types"); });

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
    $("btn-fit").addEventListener("click", function () { network.fit({ animation: anim(450) }); });
    $("btn-reset").addEventListener("click", function () {
      document.querySelectorAll("#theme-filters input, #type-filters input").forEach(function (i) { i.checked = true; });
      Object.keys(state.themes).forEach(function (k) { state.themes[k] = true; });
      Object.keys(state.types).forEach(function (k) { state.types[k] = true; });
      inp.value = ""; state.search = ""; closePanel(); applyFilters();
      network.fit({ animation: anim(450) });
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
      lg.insertAdjacentHTML("beforeend", '<div class="it"><svg width="14" height="14" viewBox="0 0 14 14" style="fill:var(' + t.cssVar + ')" stroke-linejoin="round" aria-hidden="true">' + shape + "</svg>" + esc(t.label) + "</div>");
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
    if (!nodesDS) return;
    var vis = visibleSet();
    var q = norm(state.search).trim();
    var m = {}; matches().forEach(function (n) { m[n.id] = true; });
    nodesDS.update(DATA.nodes.map(function (n) {
      var dim = q && !m[n.id];
      var o = nodeStyle(n, dim); o.hidden = !vis[n.id]; return o;
    }));
    edgesDS.update(DATA.edges.map(function (e) {
      var dim = q && !(m[e.source] || m[e.target]);
      return { id: e._id, hidden: !(vis[e.source] && vis[e.target]), color: edgeColor(dim) };
    }));
    var allOn = Object.keys(state.themes).every(function (k) { return state.themes[k]; }) &&
      Object.keys(state.types).every(function (k) { return state.types[k]; });
    document.querySelector(".toolbar").classList.toggle("has-off", !allOn);
    document.querySelectorAll(".chip").forEach(function (c) { c.classList.toggle("is-on", c.querySelector("input").checked); });
  }

  function nodeStyle(n, dim) {
    var c = PAL.types[n._sub];
    /* nœud illustré (photo / logo chargé) : fond clair et anneau coloré selon le type */
    var col = n._imgReady
      ? { background: "#ffffff", border: c, highlight: { background: "#ffffff", border: PAL.accent }, hover: { background: "#ffffff", border: c } }
      : { background: c, border: PAL.border, highlight: { background: c, border: PAL.accent }, hover: { background: c, border: PAL.border } };
    return {
      id: n.id, opacity: dim ? 0.18 : 1,
      color: col,
      shadow: { enabled: !dim, color: PAL.shadow, size: 10, x: 0, y: 3 },
      font: { face: FONT, size: n.type === "person" ? 19 : 16, color: dim ? PAL.labelDim : PAL.label, strokeWidth: 5, strokeColor: PAL.bg, vadjust: 2 }
    };
  }
  function edgeColor(dim) {
    return { color: dim ? PAL.edgeDim : PAL.edge, highlight: PAL.accent, hover: PAL.accent, inherit: false };
  }

  /* ---------- graphe ---------- */
  function sizeGraph() {
    var shell = document.querySelector(".graph-shell"), gl = document.querySelector(".graph-layout");
    if (!shell || !gl || $("view-reseau").hidden || shell.classList.contains("is-fs")) return;
    var mobile = MQ_MOBILE.matches;
    var ref = mobile ? gl : shell;
    var top = ref.getBoundingClientRect().top + window.scrollY;
    var nav = $("tabnav"), navH = mobile && nav ? nav.offsetHeight : 0;
    var bottomPad = mobile ? 12 + navH : 16;
    var h = Math.max(mobile ? 360 : 480, window.innerHeight - top - bottomPad - (mobile ? 0 : 6));
    shell.style.setProperty("--graph-h", Math.round(h) + "px");
  }
  window.addEventListener("resize", function () { sizeGraph(); });

  function buildGraph() {
    sizeGraph();
    readPalette();
    var nodes = DATA.nodes.map(function (n) {
      var t = TYPES[n._sub], deg = edgesOf[n.id].length;
      var o = nodeStyle(n, false);
      o.label = n.name; o.shape = t.shape; o.size = t.size + Math.min(deg, 12);
      o.borderWidth = 2.5; o.borderWidthSelected = 3.5; o.shapeProperties = { borderRadius: 8 };
      o.title = tooltip(n.name + " — " + n.role);
      return o;
    });
    var edges = DATA.edges.map(function (e) {
      return {
        id: e._id, from: e.source, to: e.target,
        arrows: { to: { enabled: true, scaleFactor: 0.42, type: "arrow" } },
        arrowStrikethrough: false,
        width: 1.3, hoverWidth: 1.2, selectionWidth: 1.6,
        color: edgeColor(false),
        smooth: { enabled: true, type: "curvedCW", roundness: 0.14 },
        title: tooltip(byId[e.source].name + " → " + byId[e.target].name + "\n" + e.relation + (e.date ? " (" + fmtDate(e.date) + ")" : "") + "\nCliquez pour afficher la source")
      };
    });
    nodesDS = new vis.DataSet(nodes);
    edgesDS = new vis.DataSet(edges);
    network = new vis.Network($("graph"), { nodes: nodesDS, edges: edgesDS }, {
      autoResize: true,
      interaction: { hover: true, hoverConnectedEdges: true, tooltipDelay: 120, navigationButtons: false, keyboard: { enabled: true, bindToWindow: false }, multiselect: false, zoomSpeed: 0.8 },
      nodes: {
        chosen: {
          node: function (v, id, selected, hovering) {
            if (hovering || selected) { v.size = v.size * 1.12; v.shadowSize = 20; v.shadowY = 6; }
            if (selected) { v.borderWidth = 3.5; }
          },
          label: function (v, id, selected, hovering) { if (selected || hovering) v.mod = "bold"; }
        }
      },
      physics: {
        solver: "forceAtlas2Based",
        forceAtlas2Based: { gravitationalConstant: -75, centralGravity: 0.012, springLength: 100, springConstant: 0.05, avoidOverlap: 0.8 },
        stabilization: { iterations: 400, fit: true }
      },
      layout: { randomSeed: 7, improvedLayout: true }
    });
    network.once("stabilizationIterationsDone", function () {
      network.setOptions({ physics: { enabled: false } });
      network.fit();
      window.__graphReady = true;
      window.__graphReadyAt = performance.now();
      /* aides aux tests automatisés : forme et visibilité des nœuds */
      window.__nodeShape = function (id) { var o = nodesDS.get(id); return o ? o.shape : null; };
      window.__visible = function () { return nodesDS.get().filter(function (o) { return !o.hidden; }).map(function (o) { return o.id; }); };
      loadNodeImages();
      /* aide aux tests automatisés : position DOM d'un nœud */
      window.__nodeDOM = function (id) { var p = network.getPositions([id])[id]; return p ? network.canvasToDOM(p) : null; };
    });
    network.on("click", function (p) {
      var tt = document.querySelector("#graph .vis-tooltip"); if (tt) tt.style.visibility = "hidden";
      if (p.nodes.length) {
        openNode(p.nodes[0], false);
        var nid = p.nodes[0];
        setTimeout(function () { network.focus(nid, { scale: Math.max(network.getScale(), 0.9), offset: focusOffset(), animation: anim(500) }); }, 30);
      }
      else if (p.edges.length) openEdge(p.edges[0]);
    });
    network.on("hoverNode", function () { $("graph").style.cursor = "pointer"; });
    network.on("blurNode", function () { $("graph").style.cursor = ""; });
    $("panel-close").addEventListener("click", closePanel);
    /* ignore le « clic fantôme » émis juste après le tap qui a ouvert la feuille */
    $("sheet-scrim").addEventListener("click", function () { if (Date.now() - panelOpenedAt > 450) closePanel(); });
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      if (!$("panel").hidden) closePanel();
      else if (fsMode === "pseudo") exitFullscreen();
    });
    bindFullscreen();
    bindSheet();
    var onScheme = function () { readPalette(); applyFilters(); network.redraw(); };
    if (MQ_DARK.addEventListener) MQ_DARK.addEventListener("change", onScheme); else if (MQ_DARK.addListener) MQ_DARK.addListener(onScheme);
    applyFilters();
  }
  /* ---------- images des nœuds (chargement différé, repli sur la forme colorée) ---------- */
  function nodeImageUrl(n) { return n.image || n.logo || null; }
  function logoDisc(img) {
    /* compose le logo dans un disque blanc (contenu entièrement visible dans le cercle) */
    var S = 160, c = document.createElement("canvas"); c.width = c.height = S;
    var x = c.getContext("2d"); x.fillStyle = "#ffffff"; x.fillRect(0, 0, S, S);
    var box = S * 0.64, r = Math.min(box / img.naturalWidth, box / img.naturalHeight);
    var w = img.naturalWidth * r, h = img.naturalHeight * r;
    x.drawImage(img, (S - w) / 2, (S - h) / 2, w, h);
    return c.toDataURL("image/png");
  }
  function loadNodeImages() {
    var todo = DATA.nodes.filter(nodeImageUrl), i = 0;
    window.__imgState = { total: todo.length, loaded: 0, failed: 0 };
    function next() {
      /* quelques images à la fois pour ne pas bloquer le rendu */
      for (var k = 0; k < 4 && i < todo.length; k++) one(todo[i++]);
    }
    function one(n) {
      var img = new Image();
      img.decoding = "async";
      img.onload = function () {
        try {
          var src = n.image ? img.src : logoDisc(img);
          n._imgReady = true;
          var o = nodeStyle(n, false);
          o.shape = "circularImage"; o.image = src; o.size = TYPES[n._sub].size + Math.min(edgesOf[n.id].length, 12) + 6;
          o.borderWidth = 3; o.borderWidthSelected = 4.5;
          o.shapeProperties = { useBorderWithImage: true, interpolation: true };
          nodesDS.update(o);
          window.__imgState.loaded++;
        } catch (e) { n._imgReady = false; window.__imgState.failed++; }
        done();
      };
      img.onerror = function () { window.__imgState.failed++; done(); }; /* repli : la forme colorée reste affichée */
      img.src = nodeImageUrl(n);
    }
    var pending = todo.length;
    function done() { pending--; if (i < todo.length) next(); if (!pending) { applyFilters(); window.__imagesDone = true; } }
    if (!todo.length) { window.__imagesDone = true; return; }
    (window.requestIdleCallback || function (f) { return setTimeout(f, 60); })(next);
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
    openNode(id, true);
    network.focus(id, { scale: 1.2, offset: focusOffset(), animation: anim(550) });
  }

  /* ---------- panneau latéral ---------- */
  function statementsHtml(n, themeFilter) {
    var st = (n.statements || []).filter(function (s) { return !themeFilter || s.theme === themeFilter; });
    if (!st.length) return '<p class="empty">Aucune déclaration répertoriée.</p>';
    return '<ul class="stmts">' + st.map(function (s) {
      return '<li class="stmt"><blockquote>' + quoteHtml(s.quote) + "</blockquote>" +
        '<div class="meta"><span>' + fmtDate(s.date) + "</span><span>· " + esc(s.medium) + "</span>" + (s.theme ? themeTag(s.theme) : "") + "</div>" +
        '<div class="meta">' + srcLink(s.url, "Lire la source") + archLink(s) + "</div>" + videoHtml(s.video) + "</li>";
    }).join("") + "</ul>";
  }
  /* ---------- vidéos : intégration « légère », chargée uniquement au clic ---------- */
  function videoHtml(v) {
    if (!v || !v.url) return "";
    var cap = '<span class="v-title">' + esc(v.title) + '</span><span class="v-src">' + esc(v.source || v.platform) + "</span>";
    if (v.platform === "youtube" && /^[\w-]{11}$/.test(v.id || "")) {
      return '<div class="video" data-yt="' + esc(v.id) + '">' +
        '<button type="button" class="video-btn" aria-label="Voir la vidéo : ' + esc(v.title) + '">' +
        '<span class="play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5.5v13l10.5-6.5z"/></svg></span>' +
        '<span class="v-txt"><span class="v-cta">Voir la vidéo</span>' + cap + "</span></button>" +
        '<p class="v-note">Lecteur YouTube (youtube-nocookie.com) chargé uniquement après le clic · <a href="' + esc(v.url) + '" target="_blank" rel="noopener noreferrer">Ouvrir sur YouTube ↗</a></p></div>';
    }
    return '<a class="video video-link" href="' + esc(v.url) + '" target="_blank" rel="noopener noreferrer">' +
      '<span class="play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5.5v13l10.5-6.5z"/></svg></span>' +
      '<span class="v-txt"><span class="v-cta">Voir la vidéo sur ' + esc(v.platform) + " ↗</span>" + cap + "</span></a>";
  }
  function bindVideos() {
    document.addEventListener("click", function (ev) {
      var b = ev.target.closest && ev.target.closest(".video-btn"); if (!b) return;
      var box = b.closest(".video"), id = box.getAttribute("data-yt");
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(id) + "?autoplay=1&rel=0";
      f.title = b.getAttribute("aria-label");
      f.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      f.allowFullscreen = true; f.referrerPolicy = "strict-origin-when-cross-origin";
      f.setAttribute("loading", "lazy");
      var wrap = document.createElement("div"); wrap.className = "video-frame"; wrap.appendChild(f);
      b.replaceWith(wrap); box.classList.add("is-playing");
    });
  }
  /* ---------- photo / logo du panneau, avec crédit ---------- */
  function mediaHtml(n, cls) {
    var cr, url, label;
    if (n.image) { cr = n.image_credit || {}; url = n.image; label = "Photo"; }
    else if (n.logo) { cr = n.logo_credit || {}; url = n.logo; label = "Logo"; }
    else return "";
    var lic = cr.license ? (cr.license_url ? '<a href="' + esc(cr.license_url) + '" target="_blank" rel="noopener noreferrer license">' + esc(cr.license) + "</a>" : esc(cr.license)) : "";
    var credit = label + " : " + (cr.author ? esc(cr.author) + " · " : "") + (lic ? lic + " · " : "") +
      (cr.source_url ? '<a href="' + esc(cr.source_url) + '" target="_blank" rel="noopener noreferrer">Wikimedia Commons ↗</a>' : "") +
      (n.logo && !n.image ? " · reproduit à des fins d'identification" : "");
    return '<figure class="' + cls + (n.image ? " is-photo" : " is-logo") + '"><img src="' + esc(url) + '" alt="' + esc(label + " : " + n.name) +
      '" loading="lazy" decoding="async" width="256" height="256" onerror="this.closest(\'figure\').classList.add(\'img-failed\')">' +
      '<figcaption class="credit">' + credit + "</figcaption></figure>";
  }
  function sectionTags(n) {
    return (n.sections || []).map(function (k) { return '<span class="sec sec-' + esc(k) + '">' + esc(k === "gaza" ? "Section Gaza" : "Section France") + "</span>"; }).join("");
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
      return '<li class="rel">' + sentence + '<div class="meta">' + (e.date ? fmtDate(e.date) + " · " : "") + srcLink(e.url) + archLink(e) + "</div></li>";
    }).join("") + "</ul>";
  }
  function openNode(id, fromSearch) {
    var n = byId[id]; if (!n) return;
    var t = TYPES[n._sub];
    $("panel-body").innerHTML =
      '<div class="panel-id">' + mediaHtml(n, "p-media") + '<div class="p-id-txt">' +
      '<span class="badge" style="--tc:var(' + t.cssVar + ')">' + esc(t.label) + "</span>" + '<div class="secs">' + sectionTags(n) + "</div>" +
      "<h2>" + esc(n.name) + "</h2></div></div>" +
      '<p class="role">' + esc(n.role) + "</p>" +
      '<p class="to-fiche"><a class="btn-pill small" href="' + ficheHref(n) + '">Ouvrir la fiche complète</a></p>' +
      (n.description ? "<p>" + esc(n.description) + "</p>" : "") +
      (n.type === "person" || (n.statements || []).length ? "<h3>Déclarations publiques (" + (n.statements || []).length + ")</h3>" + statementsHtml(n) : "") +
      "<h3>Relations (" + edgesOf[id].length + ")</h3>" + relationsHtml(n, true);
    showPanel();
    if (!fromSearch && network) network.selectNodes([id]);
    if (location.hash.indexOf("#/reseau") === 0) history.replaceState(null, "", "#/reseau/" + encodeURIComponent(id));
  }
  function openEdge(eid) {
    var e = DATA.edges.filter(function (x) { return x._id === eid; })[0]; if (!e) return;
    $("panel-body").innerHTML = '<span class="badge">Relation</span><h2>' + esc(byId[e.source].name) + " → " + esc(byId[e.target].name) + "</h2>" +
      '<p class="role">' + esc(e.relation) + "</p>" +
      '<p class="meta">' + fmtDate(e.date) + "</p><p class=\"src-row\">" + srcLink(e.url, "Lire la source") + archLink(e) + "</p>" +
      '<h3>Voir</h3><ul class="rels"><li class="rel"><button type="button" class="link" data-node="' + esc(e.source) + '">' + esc(byId[e.source].name) + '</button></li><li class="rel"><button type="button" class="link" data-node="' + esc(e.target) + '">' + esc(byId[e.target].name) + "</button></li></ul>";
    showPanel();
  }
  function showPanel() {
    var p = $("panel"); p.style.transform = ""; p.hidden = false; p.scrollTop = 0; panelOpenedAt = Date.now();
    document.body.classList.add("panel-open");
    document.body.classList.toggle("sheet-open", MQ_MOBILE.matches);
    p.querySelectorAll("button.link[data-node]").forEach(function (b) {
      b.addEventListener("click", function () { focusNode(b.getAttribute("data-node")); });
    });
  }
  /* Décalage du centrage pour que le nœud reste visible à côté du panneau / au-dessus de la feuille. */
  function focusOffset() {
    var p = $("panel"), g = $("graph");
    if (p.hidden || !g) return { x: 0, y: 0 };
    var gr = g.getBoundingClientRect();
    if (MQ_MOBILE.matches) {
      var sheetTop = window.innerHeight - p.offsetHeight - 8;
      var overlap = Math.max(0, gr.bottom - sheetTop);
      return { x: 0, y: -Math.min(overlap, gr.height - 80) / 2 };
    }
    var w = p.offsetWidth + 12;
    return gr.width > w * 1.6 ? { x: -w / 2, y: 0 } : { x: 0, y: 0 };
  }
  /* Feuille inférieure (mobile) : glisser vers le bas pour fermer. */
  function bindSheet() {
    var p = $("panel"), head = p.querySelector(".panel-head");
    var y0 = null, dy = 0, t0 = 0, fromContent = false, active = false;
    function start(y, content) {
      if (!MQ_MOBILE.matches || p.hidden) return;
      if (content && p.scrollTop > 0) return;
      y0 = y; dy = 0; t0 = Date.now(); fromContent = content; active = false;
    }
    function move(y, ev) {
      if (y0 === null) return;
      dy = y - y0;
      if (dy <= 0) { if (active) { p.style.transform = ""; } if (fromContent) { y0 = null; } return; }
      if (!active && dy < 6) return;
      active = true;
      if (ev && ev.cancelable) ev.preventDefault();
      p.classList.add("dragging");
      p.style.transform = "translateY(" + dy + "px)";
    }
    function end() {
      if (y0 === null) return;
      var v = dy / Math.max(1, Date.now() - t0);
      p.classList.remove("dragging");
      var shouldClose = active && (dy > Math.min(140, p.offsetHeight * 0.3) || (v > 0.5 && dy > 30));
      y0 = null; active = false;
      if (shouldClose) closePanel(); else p.style.transform = "";
    }
    p.addEventListener("touchstart", function (e) { if (e.touches.length === 1) start(e.touches[0].clientY, !head.contains(e.target)); }, { passive: true });
    p.addEventListener("touchmove", function (e) { if (e.touches.length === 1) move(e.touches[0].clientY, e); }, { passive: false });
    p.addEventListener("touchend", end);
    p.addEventListener("touchcancel", end);
    head.addEventListener("pointerdown", function (e) {
      if (e.pointerType !== "mouse" || e.target.closest("button")) return;
      start(e.clientY, false); try { head.setPointerCapture(e.pointerId); } catch (x) {}
    });
    head.addEventListener("pointermove", function (e) { if (e.pointerType === "mouse") move(e.clientY, e); });
    head.addEventListener("pointerup", function (e) { if (e.pointerType === "mouse") end(); });
    MQ_MOBILE.addEventListener && MQ_MOBILE.addEventListener("change", function () {
      document.body.classList.toggle("sheet-open", MQ_MOBILE.matches && !p.hidden);
    });
  }
  function closePanel() {
    var p = $("panel");
    p.hidden = true;
    p.style.transform = "";
    document.body.classList.remove("panel-open", "sheet-open");
    if (network) network.unselectAll();
    if (location.hash.indexOf("#/reseau/") === 0) history.replaceState(null, "", "#/reseau");
  }

  /* ---------- plein écran ---------- */
  var fsMode = null; /* null | "native" | "pseudo" */
  function fsElement() { return document.fullscreenElement || document.webkitFullscreenElement || null; }
  function nativeFsAvailable(el) {
    var req = el.requestFullscreen || el.webkitRequestFullscreen;
    var enabled = document.fullscreenEnabled !== undefined ? document.fullscreenEnabled : document.webkitFullscreenEnabled;
    return !!req && enabled !== false;
  }
  function setFsUi(on) {
    var shell = document.querySelector(".graph-shell"), b = $("btn-fs");
    shell.classList.toggle("is-fs", on);
    var label = on ? "Quitter le plein écran" : "Plein écran";
    b.querySelector(".btn-fs-label").textContent = label;
    b.title = label;
    b.setAttribute("aria-pressed", on ? "true" : "false");
  }
  function afterFsResize() {
    if (!network) return;
    var go = function () {
      network.setSize("100%", "100%");
      network.redraw();
      network.fit({ animation: anim(400) });
    };
    requestAnimationFrame(function () { requestAnimationFrame(go); });
    setTimeout(go, MQ_RM.matches ? 50 : 420);
  }
  function enterPseudo() {
    fsMode = "pseudo";
    document.querySelector(".graph-shell").classList.add("is-pseudo-fs");
    document.documentElement.classList.add("fs-lock");
    setFsUi(true); afterFsResize();
  }
  function enterFullscreen() {
    var shell = document.querySelector(".graph-shell");
    if (nativeFsAvailable(shell)) {
      fsMode = "native"; setFsUi(true);
      try {
        var r = (shell.requestFullscreen || shell.webkitRequestFullscreen).call(shell);
        if (r && typeof r.then === "function") r.catch(function () { if (!fsElement()) enterPseudo(); });
        else setTimeout(function () { if (fsMode === "native" && !fsElement()) enterPseudo(); }, 400);
      } catch (e) { enterPseudo(); }
    } else enterPseudo();
  }
  function exitFullscreen() {
    var mode = fsMode; fsMode = null;
    var shell = document.querySelector(".graph-shell");
    if (mode === "native" && fsElement()) {
      var ex = document.exitFullscreen || document.webkitExitFullscreen;
      try { var r = ex && ex.call(document); if (r && r.catch) r.catch(function () {}); } catch (e) {}
    }
    shell.classList.remove("is-pseudo-fs");
    document.documentElement.classList.remove("fs-lock");
    setFsUi(false);
    sizeGraph(); afterFsResize();
  }
  function bindFullscreen() {
    $("btn-fs").addEventListener("click", function () { if (fsMode) exitFullscreen(); else enterFullscreen(); });
    var onChange = function () {
      var shell = document.querySelector(".graph-shell");
      if (fsElement() === shell) { fsMode = "native"; setFsUi(true); afterFsResize(); }
      else if (fsMode === "native") exitFullscreen();
    };
    document.addEventListener("fullscreenchange", onChange);
    document.addEventListener("webkitfullscreenchange", onChange);
    window.__fs = function () { return fsMode; };
  }

  /* ==========================================================================
     v5 : accueil, sections / catégories, fiches, chronologie, routage, PWA
     ========================================================================== */
  var CAT_ORDER = [], ALL_ST = [], SOURCES = {}, navCount = 0;
  var SEC_LABEL = { gaza: "Gaza", france: "France – normalisation de l'extrême droite", commun: "Communs aux deux sections", tout: "Toutes les sections" };
  var SEC_INTRO = {
    tout: "Toutes les personnalités et organisations, regroupées par catégorie.",
    gaza: "Déclarations publiques en France au sujet de la guerre à Gaza, et liens publics entre les personnes et organisations concernées.",
    france: "Propos publics datés et décisions d'institutions portant sur la reprise de termes ou de thèmes associés à l'extrême droite, et liens publics entre partis, médias, éditeurs et financeurs.",
    commun: "Personnalités et organisations présentes dans les deux sections."
  };
  var SUB_ORDER = ["Gouvernement & exécutif", "Parlementaires & élus", "Partis & dirigeants de parti", "Propriétaires, financeurs & groupes", "Chaînes, radios & titres", "Édition",
    "Directions de rédaction", "Journalistes & chroniqueurs", "Philosophes & essayistes", "Historiens", "Institutions publiques", "Associations & représentants", "Projets & réseaux"];
  var MONTHS_S = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."];

  function computeDerived() {
    CAT_ORDER = (DATA.meta && DATA.meta.category_order) || [];
    DATA.nodes.forEach(function (n) {
      if (n.category && CAT_ORDER.indexOf(n.category) < 0) CAT_ORDER.push(n.category);
      (n.statements || []).forEach(function (s, i) { ALL_ST.push({ s: s, n: n, i: i }); if (s.url) SOURCES[s.url] = 1; });
    });
    DATA.edges.forEach(function (e) { if (e.url) SOURCES[e.url] = 1; });
  }
  function ficheHref(n) { return "#/" + (n.type === "person" ? "personne" : "organisation") + "/" + encodeURIComponent(n.id); }
  function initials(name) {
    var w = String(name).replace(/[«»()]/g, "").split(/[\s-]+/).filter(function (x) { return x && /[A-Za-zÀ-ÿ0-9]/.test(x[0]) && x.length > 1; });
    return ((w[0] || "?")[0] + (w.length > 1 ? w[w.length - 1][0] : "")).toUpperCase();
  }
  function avatar(n, cls) {
    var url = n.image || n.logo, tv = TYPES[n._sub].cssVar;
    var ini = '<span class="av-ini" aria-hidden="true">' + esc(initials(n.name)) + "</span>";
    var c = "av " + (cls || "") + (n.logo && !n.image ? " is-logo" : "") + (url ? "" : " no-img");
    return '<span class="' + c + '" style="--tc:var(' + tv + ')">' + (url ? '<img src="' + esc(url) + '" alt="" loading="lazy" decoding="async" width="96" height="96" onerror="this.parentNode.classList.add(\'no-img\');this.remove()">' : "") + ini + "</span>";
  }
  function catLabel(n) { return n.category ? esc(n.category) + (n.subcategory && n.subcategory !== n.category ? ' <span class="sep">›</span> ' + esc(n.subcategory) : "") : ""; }
  function shortDate(d) { var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(d || ""); return m ? parseInt(m[3], 10) + " " + MONTHS_S[parseInt(m[2], 10) - 1] : esc(d || ""); }
  function plural(n, a, b) { return n + " " + (n > 1 ? b : a); }
  function stSection(s, n) { return s.section || (n.sections || [])[0] || "gaza"; }
  function toast(msg) {
    var t = $("toast"); t.textContent = msg; t.hidden = false;
    requestAnimationFrame(function () { t.classList.add("show"); });
    clearTimeout(toast._t); toast._t = setTimeout(function () { t.classList.remove("show"); setTimeout(function () { t.hidden = true; }, 300); }, 2600);
  }

  /* ---------- Accueil ---------- */
  function buildHome() {
    var persons = DATA.nodes.filter(function (n) { return n.type === "person"; }).length;
    var vids = ALL_ST.filter(function (x) { return x.s.video; }).length;
    var arch = {}; ALL_ST.forEach(function (x) { if (x.s.archive_url) arch[x.s.url] = 1; }); DATA.edges.forEach(function (e) { if (e.archive_url) arch[e.url] = 1; });
    var nsrc = Object.keys(SOURCES).length;
    var upd = DATA.meta && DATA.meta.generated;
    var stats = [
      [persons, "personnalités"], [DATA.nodes.length - persons, "organisations et événements"], [ALL_ST.length, "déclarations datées"],
      [nsrc, "sources"], [Object.keys(arch).length, "sources archivées"], [vids, "vidéos officielles"]
    ];
    $("home-stats").innerHTML = stats.map(function (s) { return '<div class="stat"><dt>' + esc(s[1]) + "</dt><dd>" + s[0] + "</dd></div>"; }).join("") +
      '<div class="stat stat-date"><dt>dernière mise à jour</dt><dd><time datetime="' + esc(upd || "") + '">' + (upd ? fmtDate(upd) : "—") + "</time></dd></div>";
    function cnt(sec) {
      var ns = DATA.nodes.filter(function (n) { return (n.sections || []).indexOf(sec) >= 0; }).length;
      var st = ALL_ST.filter(function (x) { return stSection(x.s, x.n) === sec; }).length;
      return plural(ns, "fiche", "fiches") + " · " + plural(st, "déclaration", "déclarations");
    }
    var cards = [
      ["#/sections/gaza", "Section", "Gaza", SEC_INTRO.gaza, cnt("gaza"), "c-gaza"],
      ["#/sections/france", "Section", "France – normalisation de l'extrême droite", SEC_INTRO.france, cnt("france"), "c-fr"],
      ["#/chronologie", "Vue", "Chronologie", "Toutes les déclarations et tous les liens datés, filtrables par section, catégorie, thème et année.", plural(ALL_ST.length + DATA.edges.filter(function (e) { return e.date; }).length, "élément daté", "éléments datés"), "c-chrono"],
      ["#/reseau", "Vue", "Réseau des relations", "Graphe interactif des liens publics entre personnalités et organisations, chacun sourcé.", plural(DATA.edges.length, "relation", "relations"), "c-net"],
      ["#/methodologie", "À propos", "Méthodologie", "Critères d'inclusion, neutralité, images, vidéos, archivage et réutilisation des données.", "Sources vérifiées et archivées", "c-meth"]
    ];
    $("home-entries").innerHTML = cards.map(function (c) {
      return '<a class="entry ' + c[5] + '" href="' + c[0] + '"><span class="entry-k">' + esc(c[1]) + '</span><span class="entry-t">' + esc(c[2]) + '</span><span class="entry-d">' + esc(c[3]) + '</span><span class="entry-c">' + esc(c[4]) + '</span><span class="entry-go" aria-hidden="true">›</span></a>';
    }).join("");
    var latest = ALL_ST.filter(function (x) { return x.s.date; }).sort(function (a, b) { return b.s.date.localeCompare(a.s.date); }).slice(0, 6);
    $("home-latest").innerHTML = latest.map(function (x) {
      return '<li><a class="latest-it" href="' + ficheHref(x.n) + '#d' + x.i + '">' + avatar(x.n, "av-sm") + '<span class="latest-txt"><span class="latest-who">' + esc(x.n.name) +
        '</span><span class="latest-q">' + quoteHtml(x.s.quote) + '</span><span class="latest-m"><time datetime="' + esc(x.s.date) + '">' + fmtDate(x.s.date) + "</time> · " + esc(x.s.medium) + "</span></span></a></li>";
    }).join("");
    bindSearch($("home-search"), $("home-results"));
  }
  function searchAll(q) {
    q = norm(q).trim(); if (q.length < 2) return [];
    var out = [];
    DATA.nodes.forEach(function (n) {
      var sc = norm(n.name).indexOf(q) >= 0 ? 3 : (norm(n.role + " " + n.category + " " + n.subcategory).indexOf(q) >= 0 ? 2 : 0);
      if (sc) out.push({ sc: sc, href: ficheHref(n), n: n, label: n.name, sub: n.role });
    });
    ALL_ST.forEach(function (x) {
      if (norm(x.s.quote + " " + x.s.medium).indexOf(q) >= 0) out.push({ sc: 1, href: ficheHref(x.n) + "#d" + x.i, n: x.n, label: x.n.name + " · " + shortDate(x.s.date) + " " + (x.s.date || "").slice(0, 4), sub: "«\u00a0" + x.s.quote + "\u00a0»" });
    });
    out.sort(function (a, b) { return b.sc - a.sc; });
    return out.slice(0, 10);
  }
  function bindSearch(inp, list) {
    function render() {
      var r = searchAll(inp.value);
      if (!inp.value.trim()) { list.hidden = true; list.innerHTML = ""; return; }
      list.hidden = false;
      list.innerHTML = r.length ? r.map(function (x) {
        return '<li><a href="' + x.href + '">' + avatar(x.n, "av-xs") + '<span><span class="r-l">' + esc(x.label) + '</span><span class="r-s">' + esc(x.sub) + "</span></span></a></li>";
      }).join("") : '<li class="r-none">Aucun résultat.</li>';
    }
    inp.addEventListener("input", render);
    inp.form && inp.form.addEventListener("submit", function (e) {
      e.preventDefault(); var a = list.querySelector("a"); if (a) { location.hash = a.getAttribute("href"); }
    });
    inp.addEventListener("keydown", function (e) { if (e.key === "Escape") { inp.value = ""; render(); } });
    list.addEventListener("click", function () { setTimeout(function () { inp.value = ""; render(); }, 0); });
  }

  /* ---------- Sections ---------- */
  var curSec = "tout";
  function inSec(n, sec) {
    var s = n.sections || [];
    if (sec === "tout") return true;
    if (sec === "commun") return s.indexOf("gaza") >= 0 && s.indexOf("france") >= 0;
    return s.indexOf(sec) >= 0;
  }
  function buildSections() {
    $("sec-seg").innerHTML = ["tout", "gaza", "france", "commun"].map(function (k) {
      var c = DATA.nodes.filter(function (n) { return inSec(n, k); }).length;
      var lab = { tout: "Tout", gaza: "Gaza", france: "France", commun: "Communs" }[k];
      return '<a role="tab" class="seg-b" href="#/sections/' + k + '" data-sec="' + k + '" title="' + esc(SEC_LABEL[k]) + '">' + lab + ' <span class="seg-n">' + c + "</span></a>";
    }).join("");
    var html = CAT_ORDER.map(function (cat, ci) {
      var subs = [];
      DATA.nodes.forEach(function (n) { if (n.category === cat && subs.indexOf(n.subcategory) < 0) subs.push(n.subcategory); });
      subs.sort(function (x, y) { var i = SUB_ORDER.indexOf(x), j = SUB_ORDER.indexOf(y); return (i < 0 ? 99 : i) - (j < 0 ? 99 : j); });
      return '<details class="cat" open data-cat="' + esc(cat) + '"><summary><span class="cat-t">' + esc(cat) + '</span><span class="cat-n"></span><svg class="i chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 10l5 5 5-5"/></svg></summary>' +
        subs.map(function (sub) {
          var ns = DATA.nodes.filter(function (n) { return n.category === cat && n.subcategory === sub; })
            .sort(function (a, b) { return (b.statements || []).length - (a.statements || []).length || a.name.localeCompare(b.name, "fr"); });
          return '<div class="sub" data-sub="' + esc(sub) + '">' + (sub !== cat ? '<h3 class="sub-t">' + esc(sub) + "</h3>" : "") + '<ul class="ncards">' + ns.map(function (n) {
            var k = (n.statements || []).length;
            return '<li data-id="' + esc(n.id) + '" data-q="' + esc(norm(n.name + " " + n.role)) + '"><a class="ncard" href="' + ficheHref(n) + '">' + avatar(n, "av-md") +
              '<span class="nc-txt"><span class="nc-name">' + esc(n.name) + '</span><span class="nc-role">' + esc(n.role) + '</span><span class="nc-meta">' +
              (k ? '<span class="nc-k">' + plural(k, "déclaration", "déclarations") + "</span>" : "") + (n.sections || []).map(function (s) { return '<span class="dot-sec ds-' + s + '" title="Section ' + esc(SEC_LABEL[s]) + '"></span>'; }).join("") +
              '</span></span><span class="chev-r" aria-hidden="true">›</span></a></li>';
          }).join("") + "</ul></div>";
        }).join("") + "</details>";
    }).join("");
    $("sec-groups").innerHTML = html;
    $("sec-search").addEventListener("input", renderSections);
  }
  function renderSections() {
    var q = norm($("sec-search").value).trim(), total = 0;
    document.querySelectorAll("#sec-seg .seg-b").forEach(function (b) { var on = b.getAttribute("data-sec") === curSec; b.setAttribute("aria-selected", on ? "true" : "false"); });
    $("sec-intro").textContent = SEC_INTRO[curSec];
    document.querySelectorAll("#sec-groups .cat").forEach(function (d) {
      var shownCat = 0;
      d.querySelectorAll(".sub").forEach(function (sb) {
        var shown = 0;
        sb.querySelectorAll("li[data-id]").forEach(function (li) {
          var ok = inSec(byId[li.getAttribute("data-id")], curSec) && (!q || li.getAttribute("data-q").indexOf(q) >= 0);
          li.hidden = !ok; if (ok) shown++;
        });
        sb.hidden = !shown; shownCat += shown;
      });
      d.hidden = !shownCat; d.querySelector(".cat-n").textContent = shownCat; total += shownCat;
    });
    $("sec-count").textContent = plural(total, "fiche", "fiches") + " · " + SEC_LABEL[curSec];
  }

  /* ---------- Fiche personne / organisation ---------- */
  var curFiche = null;
  function renderFiche(id, anchor) {
    var n = byId[id], body = $("fiche-body");
    if (!n) { curFiche = null; body.innerHTML = '<p class="empty">Fiche introuvable.</p><p><a class="btn-pill" href="#/sections">Voir toutes les sections</a></p>'; return; }
    curFiche = n;
    var t = TYPES[n._sub];
    var st = (n.statements || []).map(function (s, i) { return { s: s, i: i }; }).sort(function (a, b) { return (a.s.date || "").localeCompare(b.s.date || ""); });
    var es = edgesOf[n.id].slice().sort(function (a, b) { return (a.date || "").localeCompare(b.date || ""); });
    var media = mediaHtml(n, "f-media") || '<figure class="f-media no-photo">' + avatar(n, "av-xl") + "</figure>";
    body.innerHTML =
      '<header class="f-head">' + media + '<div class="f-id">' +
      '<div class="f-badges"><span class="badge" style="--tc:var(' + t.cssVar + ')">' + esc(t.label) + "</span>" + sectionTags(n) + "</div>" +
      '<h1 class="f-name" tabindex="-1">' + esc(n.name) + "</h1>" + '<p class="f-role">' + esc(n.role) + "</p>" +
      (n.category ? '<p class="f-cat"><a href="#/sections">' + catLabel(n) + "</a></p>" : "") + "</div></header>" +
      (n.description ? '<p class="f-desc">' + esc(n.description) + "</p>" : "") +
      '<div class="f-actions"><a class="btn-pill ghost small" href="#/reseau/' + encodeURIComponent(n.id) + '">Voir dans le réseau</a></div>' +
      (st.length || n.type === "person" ? '<h2 class="h-sec">Déclarations publiques <span class="h-n">' + st.length + "</span></h2>" +
        (st.length ? '<ol class="tl">' + st.map(function (x) { return tlItem(x.s, n, x.i, false); }).join("") + "</ol>" : '<p class="empty">Aucune déclaration répertoriée.</p>') : "") +
      '<h2 class="h-sec">Relations <span class="h-n">' + es.length + "</span></h2>" +
      (es.length ? '<ul class="rel-list">' + es.map(function (e) { return relItem(e, n); }).join("") + "</ul>" : '<p class="empty">Aucune relation répertoriée.</p>');
    document.title = n.name + " — Cartographie des déclarations et des liens publics";
    if (anchor) { var el = document.getElementById(anchor); if (el) setTimeout(function () { el.scrollIntoView({ block: "center", behavior: MQ_RM.matches ? "auto" : "smooth" }); el.classList.add("flash"); }, 60); }
  }
  function tlItem(s, n, i, withWho) {
    return '<li class="tl-item"' + (withWho ? "" : ' id="d' + i + '"') + '><time class="tl-date" datetime="' + esc(s.date || "") + '">' + fmtDate(s.date) + "</time>" +
      '<article class="tl-card">' + (withWho ? '<a class="tl-who" href="' + ficheHref(n) + '#d' + i + '">' + avatar(n, "av-xs") + "<span>" + esc(n.name) + "</span></a>" : "") +
      "<blockquote>" + quoteHtml(s.quote) + "</blockquote>" +
      '<div class="meta"><span class="medium">' + esc(s.medium) + "</span>" + (s.theme ? themeTag(s.theme) : "") + "</div>" +
      '<div class="meta actions">' + srcLink(s.url, "Lire la source") + archLink(s) + "</div>" + videoHtml(s.video) + "</article></li>";
  }
  function relItem(e, n) {
    var out = e.source === n.id, o = byId[out ? e.target : e.source];
    var sentence = out ? esc(n.name) + " → <strong>" + esc(o.name) + "</strong>" : "<strong>" + esc(o.name) + "</strong> → " + esc(n.name);
    return '<li class="rel-card"><a class="rel-main" href="' + ficheHref(o) + '">' + avatar(o, "av-sm") + '<span class="rel-txt"><span class="rel-s">' + sentence + '</span><span class="rel-r">' + esc(e.relation) + '</span></span><span class="chev-r" aria-hidden="true">›</span></a>' +
      '<div class="meta">' + (e.date ? '<time datetime="' + esc(e.date) + '">' + fmtDate(e.date) + "</time>" : "") + srcLink(e.url, "Source") + archLink(e) + "</div></li>";
  }
  function bindFiche() {
    $("fiche-back").addEventListener("click", function () {
      if (navCount > 0 && history.length > 1) history.back(); else location.hash = "#/sections";
    });
    $("fiche-share").addEventListener("click", function () {
      if (!curFiche) return;
      var url = location.href.split("#")[0] + ficheHref(curFiche);
      var data = { title: curFiche.name + " — Cartographie", text: curFiche.name + " : déclarations publiques et liens, avec leurs sources.", url: url };
      if (navigator.share) { navigator.share(data).catch(function () {}); return; }
      copyText(url).then(function () { toast("Lien copié : " + url); }, function () { toast(url); });
    });
  }
  function copyText(t) {
    if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(t);
    return new Promise(function (res, rej) {
      var ta = document.createElement("textarea"); ta.value = t; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy") ? res() : rej(); } catch (e) { rej(e); } ta.remove();
    });
  }

  /* ---------- Chronologie ---------- */
  var TL_ITEMS = [], tlDesc = false, LINKS = "__links__";
  function buildTimeline() {
    ALL_ST.forEach(function (x) { if (x.s.date) TL_ITEMS.push({ k: "s", d: x.s.date, x: x, sec: stSection(x.s, x.n), cats: [x.n.category], theme: x.s.theme }); });
    DATA.edges.forEach(function (e) { if (e.date) TL_ITEMS.push({ k: "e", d: e.date, e: e, sec: e.section || "gaza", cats: [byId[e.source].category, byId[e.target].category], theme: LINKS }); });
    function opt(sel, v, l) { var o = document.createElement("option"); o.value = v; o.textContent = l; $(sel).appendChild(o); }
    opt("tl-section", "gaza", "Gaza"); opt("tl-section", "france", "France – normalisation de l'extrême droite");
    CAT_ORDER.forEach(function (c) { opt("tl-category", c, c); });
    themes.forEach(function (t) { opt("tl-theme", t, t); }); opt("tl-theme", LINKS, "Liens publics datés (relations)");
    var years = {}; TL_ITEMS.forEach(function (it) { years[it.d.slice(0, 4)] = 1; });
    Object.keys(years).sort().reverse().forEach(function (y) { opt("tl-year", y, y); });
    ["tl-section", "tl-category", "tl-theme", "tl-year"].forEach(function (id) { $(id).addEventListener("change", renderTimeline); });
    $("tl-order").addEventListener("click", function () {
      tlDesc = !tlDesc; this.setAttribute("aria-pressed", tlDesc ? "true" : "false");
      this.textContent = tlDesc ? "Plus ancien d'abord" : "Plus récent d'abord"; renderTimeline();
    });
    renderTimeline();
  }
  function renderTimeline() {
    var sec = $("tl-section").value, cat = $("tl-category").value, th = $("tl-theme").value, yr = $("tl-year").value;
    var items = TL_ITEMS.filter(function (it) {
      return (!sec || it.sec === sec) && (!cat || it.cats.indexOf(cat) >= 0) && (!th || it.theme === th) && (!yr || it.d.slice(0, 4) === yr);
    }).sort(function (a, b) { return tlDesc ? b.d.localeCompare(a.d) : a.d.localeCompare(b.d); });
    var groups = [], cur = null;
    items.forEach(function (it) { var y = it.d.slice(0, 4); if (!cur || cur.y !== y) { cur = { y: y, it: [] }; groups.push(cur); } cur.it.push(it); });
    var ns = items.filter(function (i) { return i.k === "s"; }).length;
    $("tl-count").textContent = plural(ns, "déclaration", "déclarations") + " · " + plural(items.length - ns, "lien daté", "liens datés");
    $("timeline").innerHTML = groups.length ? groups.map(function (g) {
      return '<section class="tl-year" data-year="' + g.y + '"><h2 class="year-h"><span>' + g.y + '</span><span class="year-n">' + g.it.length + "</span></h2><ol class=\"tl\">" +
        g.it.map(function (it) { return it.k === "s" ? tlItem(it.x.s, it.x.n, it.x.i, true).replace('class="tl-item"', 'class="tl-item k-s" data-sec="' + it.sec + '"') : tlEdge(it.e); }).join("") + "</ol></section>";
    }).join("") : '<p class="empty">Aucun élément ne correspond à ces filtres.</p>';
  }
  function tlEdge(e) {
    var a = byId[e.source], b = byId[e.target];
    return '<li class="tl-item k-e" data-sec="' + esc(e.section || "") + '"><time class="tl-date" datetime="' + esc(e.date) + '">' + fmtDate(e.date) + '</time><article class="tl-card tl-link">' +
      '<span class="badge lk">Lien public</span><p class="tl-rel"><a href="' + ficheHref(a) + '">' + esc(a.name) + '</a> → <a href="' + ficheHref(b) + '">' + esc(b.name) + "</a> : " + esc(e.relation) + "</p>" +
      '<div class="meta actions">' + srcLink(e.url, "Lire la source") + archLink(e) + "</div></article></li>";
  }

  /* ---------- Routage par ancre (#/…) ---------- */
  var VIEWS = ["accueil", "sections", "fiche", "chronologie", "reseau", "methodologie"];
  var TITLES = { accueil: "Gaza et extrême droite en France : cartographie des déclarations et des liens publics", sections: "Sections", chronologie: "Chronologie", reseau: "Réseau des relations", methodologie: "Méthodologie" };
  var lastView = null;
  function ensureGraph(focusId) {
    if (!network) buildGraph(); else { sizeGraph(); network.redraw(); }
    if (focusId && byId[focusId]) {
      (function wait(k) { if (window.__graphReady) focusNode(focusId); else if (k < 200) setTimeout(function () { wait(k + 1); }, 50); })(0);
    }
  }
  function route() {
    var h = location.hash.replace(/^#/, "");
    /* anciennes adresses (v1–v4) */
    var legacy = /^(graphe|liste|methodologie)(?:\/(.*))?$/.exec(h);
    if (legacy) {
      var to = legacy[1] === "graphe" ? "/reseau" + (legacy[2] ? "/" + legacy[2] : "") : legacy[1] === "liste" ? "/sections" : "/methodologie";
      history.replaceState(null, "", "#" + to); h = to;
    }
    var parts = h.replace(/^\//, "").split("#")[0].split("/"), v = parts[0] || "accueil";
    var anchor = (h.split("#")[1]) || null;
    if (v === "personne" || v === "organisation") v = "fiche";
    if (VIEWS.indexOf(v) < 0) v = "accueil";
    VIEWS.forEach(function (k) { $("view-" + k).hidden = k !== v; });
    var tab = v === "fiche" ? "sections" : v;
    document.querySelectorAll("#tabnav a").forEach(function (a) {
      if (a.getAttribute("data-tab") === tab) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    document.body.setAttribute("data-view", v);
    if (v !== "reseau") {
      if (!$("panel").hidden) closePanel();
      document.body.classList.remove("sheet-open", "panel-open");
      if (fsMode) exitFullscreen();
    }
    if (v !== "fiche") document.title = v === "accueil" ? TITLES.accueil : TITLES[v] + " — Cartographie des déclarations et des liens publics";
    if (v === "sections") { curSec = ["tout", "gaza", "france", "commun"].indexOf(parts[1]) >= 0 ? parts[1] : "tout"; renderSections(); }
    if (v === "fiche") renderFiche(decodeURIComponent(parts[1] || ""), anchor);
    var key = v + "/" + (v === "fiche" ? parts[1] : "");
    if (key !== lastView && !(v === "reseau" && lastView && lastView.indexOf("reseau") === 0)) window.scrollTo(0, 0);
    lastView = key;
    if (v === "reseau") requestAnimationFrame(function () { ensureGraph(parts[1] ? decodeURIComponent(parts[1]) : null); });
    window.__route = v;
  }
  function bindRouter() {
    window.addEventListener("hashchange", function () { navCount++; route(); });
    route();
    var ft = $("filters-toggle"), fl = $("filters");
    ft.addEventListener("click", function () {
      var open = ft.getAttribute("aria-expanded") !== "true";
      ft.setAttribute("aria-expanded", open ? "true" : "false");
      fl.classList.toggle("open", open);
      sizeGraph();
    });
    fl.addEventListener("transitionend", function (e) { if (e.target === fl) { sizeGraph(); } });
    var ab = document.querySelector(".appbar");
    var onScroll = function () { ab.classList.toggle("stuck", window.scrollY > 4); };
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }

  /* ---------- Application installable : service worker ---------- */
  function registerSW() {
    if (!("serviceWorker" in navigator) || !/^https?:$/.test(location.protocol)) return;
    navigator.serviceWorker.register("sw.js", { scope: "./" })
      .then(function () { window.__swRegistered = true; })
      .catch(function (e) { window.__swError = String(e); });
  }
})();
