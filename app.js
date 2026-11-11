/* Onrecord — cartographie des déclarations publiques — script principal (sans étape de build). */
(function () {
  "use strict";

  var THEME_FR = "France – normalisation de l'extrême droite";
  var THEME_FV = "France – montée des violences";
  var THEME_ORDER = ["Gaza – déclarations", THEME_FR, THEME_FV, "Proximité extrême droite", "Nuance / contexte"];
  var THEME_CLASS = { "Gaza – déclarations": "t-gaza", "Proximité extrême droite": "t-ed", "Nuance / contexte": "t-nuance" };
  THEME_CLASS[THEME_FR] = "t-fr"; THEME_CLASS[THEME_FV] = "t-fv";
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
  THEME_VAR[THEME_FR] = "--t-fr"; THEME_VAR[THEME_FV] = "--t-fv";
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
    if (m) {
      var day = parseInt(m[3], 10);
      return (day === 1 ? "1er" : day) + " " + MONTHS[parseInt(m[2], 10) - 1] + " " + m[1];
    }
    var ym = /^(\d{4})-(\d{2})$/.exec(d);
    if (ym) return MONTHS[parseInt(ym[2], 10) - 1] + " " + ym[1];
    if (/^\d{4}$/.test(d)) return d;
    return esc(d);
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
    assignPower();
    fillMeta();
    bindDonation();
    bindVideos();
    buildFilters();
    buildHome();
    buildSections();
    buildTimeline(); initContrib();
    bindFiche();
    bindCards();
    bindRouter();
    registerSW();
  }

  /* Bouton « Soutenir » : affiché seulement si config.js renseigne DONATION_URL */
  function bindDonation() {
    var url = String(CFG.DONATION_URL || "").trim();
    var okUrl = /^https:\/\//i.test(url);
    document.querySelectorAll(".donate").forEach(function (a) {
      if (okUrl) { a.href = url; a.hidden = false; } else { a.hidden = true; a.removeAttribute("href"); }
      armDonateTap(a);
    });
  }
  /* Rebond court au tap. N'empêche pas l'ouverture (target=_blank) : le lien part pendant l'anim. */
  function armDonateTap(a) {
    if (a.getAttribute("data-donate-tap")) return;
    a.setAttribute("data-donate-tap", "1");
    var last = 0;
    function play() {
      var now = Date.now();
      if (now - last < 90) return;
      last = now;
      var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      a.classList.remove("is-loved");
      clearDonateSparks(a);
      void a.offsetWidth;
      a.classList.add("is-loved");
      if (!reduce) burstDonate(a);
      clearTimeout(a._donateT);
      a._donateT = setTimeout(function () {
        a.classList.remove("is-loved");
        clearDonateSparks(a);
      }, 420);
    }
    a.addEventListener("pointerdown", play);
    a.addEventListener("click", play);
  }
  function clearDonateSparks(a) {
    var old = a.querySelectorAll(".donate-spark");
    for (var i = 0; i < old.length; i++) old[i].parentNode.removeChild(old[i]);
  }
  function burstDonate(a) {
    var n = 6;
    for (var i = 0; i < n; i++) {
      var s = document.createElement("span");
      s.className = "donate-spark";
      s.setAttribute("aria-hidden", "true");
      s.textContent = "\u2665";
      var ang = (-168 + i * (150 / (n - 1))) * Math.PI / 180;
      var dist = 14 + (i % 3) * 7;
      s.style.setProperty("--dx", (Math.cos(ang) * dist).toFixed(1) + "px");
      s.style.setProperty("--dy", (Math.sin(ang) * dist).toFixed(1) + "px");
      s.style.animationDelay = ((i % 3) * 16) + "ms";
      a.appendChild(s);
    }
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
        // événement sans lien (ex. fait judiciaire) : visible selon le thème de ses propres déclarations
        var standalone = !edgesOf[n.id].length && (n.statements || []).length && personVisibleByTheme(n);
        if (linked || noPeopleShown || standalone) { vis[n.id] = true; changed = true; }
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
      return { id: e._id, hidden: !(vis[e.source] && vis[e.target]), color: edgeColor(dim, e), dashes: edgeNature(e) === "opposition" };
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
  function edgeNature(e) {
    return e && (e.nature === "ascension" || e.nature === "opposition" || e.nature === "coulisses" || e.nature === "autre") ? e.nature : "autre";
  }
  function edgeColor(dim, e) {
    var c = dim ? PAL.edgeDim : PAL.edge;
    if (!dim && e && edgeNature(e) === "opposition") c = cssv("--t-fv") || "#B3261E";
    return { color: c, highlight: PAL.accent, hover: PAL.accent, inherit: false };
  }
  function natureLabel(nat) {
    return nat === "ascension" ? "Ascension" : nat === "opposition" ? "Opposition" : nat === "coulisses" ? "Coulisses" : "Autre";
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
        color: edgeColor(false, e),
        dashes: edgeNature(e) === "opposition",
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
    var extra = "";
    if (!url) {
      if (n.sphere) extra += ' data-sphere="' + esc(n.sphere) + '"';
      extra += ' data-kind="' + esc(n._sub || n.type || "person") + '"';
    }
    return '<span class="' + c + '" style="--tc:var(' + tv + ')"' + extra + '>' + (url ? '<img src="' + esc(url) + '" alt="" loading="lazy" decoding="async" width="96" height="96" onerror="this.parentNode.classList.add(\'no-img\');this.remove()">' : "") + ini + "</span>";
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
      [persons, "personnalités", "#/sections"], [DATA.nodes.length - persons, "organisations et événements", "#/sections"], [ALL_ST.length, "déclarations datées", "#/chronologie"],
      [nsrc, "sources", "#/methodologie"], [Object.keys(arch).length, "sources archivées", "#/methodologie"], [vids, "vidéos officielles", "#/chronologie"]
    ];
    $("home-stats").innerHTML = stats.map(function (s) { return '<div class="stat stat-tap"><dt>' + esc(s[1]) + '</dt><dd><a class="stat-a" href="' + s[2] + '" aria-label="' + esc(s[0] + " " + s[1]) + '">' + s[0] + "</a></dd></div>"; }).join("") +
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
      ["#/pouvoir", "Vue", "Échelle du pouvoir", "Les mêmes fiches, rangées par fonction publique documentée. Un tap montre les liens déjà sourcés, vers le haut et vers le bas.", plural(DATA.nodes.length, "fiche", "fiches") + " · " + plural(DATA.edges.length, "lien", "liens"), "c-pow"],
      ["#/coulisses", "Vue", "Coulisses", "Partis, médias, argent, idées, édition, institutions : les ponts datés et sourcés. Un récit suit l'argent, les médias ou les nominations.", "Liens publics entre sphères", "c-cou"],
      ["#/methodologie", "À propos", "Méthodologie", "Critères d'inclusion, neutralité, images, vidéos, archivage et réutilisation des données.", "Sources vérifiées et archivées", "c-meth"],
      ["#/contribuer", "Participer", "Proposer une mise à jour", "Une erreur, une précision, une nouvelle déclaration sourcée ? Chaque proposition est vérifiée avant publication.", "Formulaire de contribution", "c-contrib"]
    ];
    $("home-entries").innerHTML = cards.map(function (c) {
      return '<a class="entry ' + c[5] + '" href="' + c[0] + '"><span class="entry-k">' + esc(c[1]) + '</span><span class="entry-t">' + esc(c[2]) + '</span><span class="entry-d">' + esc(c[3]) + '</span><span class="entry-c">' + esc(c[4]) + '</span><span class="entry-go" aria-hidden="true">›</span></a>';
    }).join("");
    var latest = ALL_ST.filter(function (x) { return x.s.date; }).sort(function (a, b) { return b.s.date.localeCompare(a.s.date); }).slice(0, 6);
    $("home-latest").innerHTML = latest.map(function (x) {
      return '<li><a class="latest-it" href="' + ficheHref(x.n) + '#d' + x.i + '">' + avatar(x.n, "av-sm") + '<span class="latest-txt"><span class="latest-who">' + esc(x.n.name) +
        '</span><span class="latest-q">' + quoteHtml(x.s.quote) + '</span><span class="latest-m"><time datetime="' + esc(x.s.date) + '">' + fmtDate(x.s.date) + "</time> · " + esc(x.s.medium) + "</span></span></a></li>";
    }).join("");
    renderQotd(); renderResume();
    bindSearch($("home-search"), $("home-results"));
  }
  /* v13 : citation du jour (déterministe par date à Paris), reprise de la dernière fiche */
  function parisDay() {
    try { return new Intl.DateTimeFormat("fr-CA", { timeZone: "Europe/Paris", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date()); }
    catch (e) { return new Date().toISOString().slice(0, 10); }
  }
  function qotdPick(day) {
    var pool = ALL_ST.filter(function (x) { return x.n.type === "person" && x.s.date && x.s.quote && x.s.quote.length <= 260; })
      .sort(function (a, b) { return (a.n.id + a.i).localeCompare(b.n.id + b.i); });
    if (!pool.length) return null;
    var h = 0; for (var k = 0; k < day.length; k++) h = (h * 31 + day.charCodeAt(k)) >>> 0;
    return pool[h % pool.length];
  }
  window.__renderCard = function (id, i) { var n = byId[id]; return n ? renderCard(n, n.statements[i || 0]) : null; };
  window.__qotd = function (d) { var x = qotdPick(d || parisDay()); return x ? { id: x.n.id, i: x.i } : null; };
  function renderQotd() {
    var el = $("home-qotd"); if (!el) return;
    var day = parisDay(), x = qotdPick(day); if (!x) { el.hidden = true; return; }
    el.hidden = false; preloadImg(x.n.image);
    el.innerHTML = '<p class="qotd-k">Citation du jour · <time datetime="' + esc(day) + '">' + fmtDate(day) + "</time></p>" +
      '<blockquote class="qotd-q">' + quoteHtml(x.s.quote) + "</blockquote>" +
      '<p class="qotd-m"><a class="qotd-who" href="' + ficheHref(x.n) + "#d" + x.i + '">' + avatar(x.n, "av-xs") + "<span>" + esc(x.n.name) + "</span></a> · " +
      '<time datetime="' + esc(x.s.date) + '">' + fmtDate(x.s.date) + "</time> · " + esc(x.s.medium) + "</p>" +
      '<div class="meta actions">' + srcLink(x.s.url, "Lire la source") + actionsHtml(x.n, x.i) + "</div>" +
      '<p class="qotd-note">Une nouvelle citation chaque jour.</p>';
  }
  function renderResume() {
    var el = $("home-resume"); if (!el) return;
    var id = null; try { id = localStorage.getItem("onrecord:last"); } catch (e) {}
    var n = id && byId[id];
    if (!n) { el.hidden = true; el.innerHTML = ""; return; }
    el.hidden = false;
    el.innerHTML = '<a class="chip resume-chip" href="' + ficheHref(n) + '">' + avatar(n, "av-xs") + "<span>Reprendre : " + esc(n.name) + "</span></a>";
  }
  function exploreHtml(n) {
    var seen = {}, out = []; seen[n.id] = 1;
    (edgesOf[n.id] || []).forEach(function (e) {
      var o = e.source === n.id ? e.target : e.source;
      if (!seen[o] && byId[o] && byId[o].type === "person") { seen[o] = 1; out.push(byId[o]); }
    });
    (edgesOf[n.id] || []).forEach(function (e) {
      var o = e.source === n.id ? e.target : e.source;
      if (!seen[o] && byId[o]) { seen[o] = 1; out.push(byId[o]); }
    });
    if (out.length < 3) {
      var others = DATA.nodes.filter(function (x) { return x.type === "person" && !seen[x.id]; });
      var h = 0; for (var k = 0; k < n.id.length; k++) h = (h * 31 + n.id.charCodeAt(k)) >>> 0;
      for (var j = 0; j < others.length && out.length < 3; j++) out.push(others[(h + j * 7) % others.length]);
    }
    out = out.slice(0, 3);
    return '<section class="explore" id="explore"><h2 class="h-sec">Continuer à explorer</h2><ul class="explore-list">' + out.map(function (o) {
      return '<li><a class="explore-it" href="' + ficheHref(o) + '">' + avatar(o, "av-sm") + '<span class="explore-txt"><span class="explore-n">' + esc(o.name) + '</span><span class="explore-r">' + esc(o.role) + '</span></span><span class="chev-r" aria-hidden="true">›</span></a></li>';
    }).join("") + "</ul></section>";
  }
  function donateInvite() {
    var url = String(CFG.DONATION_URL || "").trim();
    if (!/^https:\/\//i.test(url) || !curFiche || window.__route !== "fiche") return;
    var el = $("donate-invite");
    if (!el) {
      el = document.createElement("p"); el.id = "donate-invite"; el.className = "donate-invite";
      el.innerHTML = 'Onrecord vit des dons — <a href="' + esc(url) + '" target="_blank" rel="noopener noreferrer">Soutenir</a>';
      var ex = $("explore"); if (ex) ex.parentNode.insertBefore(el, ex); else $("fiche-body").appendChild(el);
    }
    el.hidden = false;
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
      '<div class="f-actions">' + (hasParcours(n) ? '<a class="btn-pill small" href="' + ficheHref(n) + '#parcours">' + esc(arriveLabel(n)) + '</a>' : "") +
      '<a class="btn-pill ghost small" href="#/reseau/' + encodeURIComponent(n.id) + '">Voir dans le réseau</a><a class="btn-pill ghost small" href="#/pouvoir/' + encodeURIComponent(n.id) + '">Voir sur l\'échelle</a>' +
      (n.sphere ? '<a class="btn-pill ghost small" href="#/coulisses/' + encodeURIComponent(n.id) + '">Voir dans les coulisses</a>' : "") + "</div>" +
      parcoursHtml(n) +
      amHtml(n) +
      (st.length || n.type === "person" ? '<h2 class="h-sec">Déclarations publiques <span class="h-n">' + st.length + "</span></h2>" +
        (st.length ? '<ol class="tl">' + st.map(function (x) { return tlItem(x.s, n, x.i, false); }).join("") + "</ol>" : '<p class="empty">Aucune déclaration répertoriée.</p>') : "") +
      '<h2 class="h-sec">Relations <span class="h-n">' + es.length + "</span></h2>" +
      (es.length ? '<ul class="rel-list">' + es.map(function (e) { return relItem(e, n); }).join("") + "</ul>" : '<p class="empty">Aucune relation répertoriée.</p>') +
      exploreHtml(n);
    try { localStorage.setItem("onrecord:last", n.id); } catch (e) {}
    preloadImg(n.image);
    document.title = n.name + " — Onrecord";
    if (anchor) { var el = document.getElementById(anchor); if (el) setTimeout(function () { el.scrollIntoView({ block: "center", behavior: MQ_RM.matches ? "auto" : "smooth" }); el.classList.add("flash"); }, 60); }
  }
  function tlItem(s, n, i, withWho) {
    return '<li class="tl-item"' + (withWho ? "" : ' id="d' + i + '"') + '><time class="tl-date" datetime="' + esc(s.date || "") + '">' + fmtDate(s.date) + "</time>" +
      '<article class="tl-card">' + (withWho ? '<a class="tl-who" href="' + ficheHref(n) + '#d' + i + '">' + avatar(n, "av-xs") + "<span>" + esc(n.name) + "</span></a>" : "") +
      "<blockquote>" + quoteHtml(s.quote) + "</blockquote>" +
      '<div class="meta"><span class="medium">' + esc(s.medium) + "</span>" + (s.theme ? themeTag(s.theme) : "") + "</div>" +
      '<div class="meta actions">' + srcLink(s.url, "Lire la source") + archLink(s) + actionsHtml(n, i) + "</div>" + videoHtml(s.video) + "</article></li>";
  }
  function relItem(e, n) {
    var out = e.source === n.id, o = byId[out ? e.target : e.source];
    var sentence = out ? esc(n.name) + " → <strong>" + esc(o.name) + "</strong>" : "<strong>" + esc(o.name) + "</strong> → " + esc(n.name);
    var nat = edgeNature(e);
    return '<li class="rel-card nat-' + nat + '"><a class="rel-main" href="' + ficheHref(o) + '">' + avatar(o, "av-sm") + '<span class="rel-txt"><span class="rel-s">' + sentence + '</span><span class="rel-r">' + esc(e.relation) + '</span></span><span class="chev-r" aria-hidden="true">›</span></a>' +
      '<div class="meta">' + natureBadge(nat) + (e.date ? '<time datetime="' + esc(e.date) + '">' + fmtDate(e.date) + "</time>" : "") + srcLink(e.url, "Source") + archLink(e) + "</div></li>";
  }
  var FEMALE = { "caroline-yadan": 1, "aurore-berge": 1, "marine-le-pen": 1, "marion-marechal": 1, "yael-braun-pivet": 1, "elisabeth-levy": 1, "caroline-fourest": 1, "valerie-pecresse": 1, "marine-tondelier": 1, "sarah-knafo": 1, "lise-boell": 1, "constance-benque": 1 };
  function arriveLabel(n) {
    if (!n || n.type !== "person") return "Voir la frise";
    return FEMALE[n.id] ? "Voir comment elle est arrivée là" : "Voir comment il est arrivé là";
  }
  function hasParcours(n) { return !!(n && n.parcours && n.parcours.length); }
  function natureBadge(nat) {
    return '<span class="nat nat-' + nat + '">' + esc(natureLabel(nat)) + "</span>";
  }
  function parcoursHtml(n) {
    if (!hasParcours(n)) return "";
    var steps = n.parcours.slice().sort(function (a, b) { return String(a.date).localeCompare(String(b.date)); });
    return '<section class="parcours" id="parcours" aria-labelledby="parcours-title"><div class="parcours-h"><h2 class="h-sec" id="parcours-title">Parcours <span class="h-n">' + steps.length + "</span></h2>" +
      '<p class="parcours-lead">' + (n.type === "person"
        ? "Étapes datées, des études documentées jusqu'au statut actuel. Le repère Formation marque la scolarité, un diplôme ou le premier métier. Une pastille n'apparaît que si la source nomme qui a désigné, nommé, confié ou chargé."
        : "Frise courte : création, rachat, direction ou ligne, seulement quand une source le décrit.") + "</p></div>" +
      '<ol class="p-rail">' + steps.map(function (s, i) {
        var who = s.by && byId[s.by] ? byId[s.by] : null;
        var last = i === steps.length - 1;
        var form = s.kind === "formation";
        return '<li class="p-step' + (form ? " is-formation" : "") + (last ? " is-now" : "") + '" style="--i:' + i + '"><time datetime="' + esc(s.date) + '">' + fmtDate(s.date) + "</time>" +
          '<article class="p-card"><h3>' + esc(s.title) + "</h3><p>" + esc(s.text) + "</p>" +
          (who ? '<a class="p-by" href="' + ficheHref(who) + '#parcours">' + avatar(who, "av-xs") + "<span><strong>" + esc(who.name) + "</strong><em>" + esc(s.verb || "") + "</em></span></a>" : "") +
          '<div class="meta">' + (form ? '<span class="nat nat-formation">Formation</span>' : "") + srcLink(s.url, s.source || "Lire la source") + archLink(s) + "</div></article></li>";
      }).join("") + "</ol></section>";
  }
  function bindFiche() {
    $("fiche-back").addEventListener("click", function () {
      if (navCount > 0 && history.length > 1) history.back(); else location.hash = "#/sections";
    });
    $("fiche-share").addEventListener("click", function () {
      if (!curFiche) return;
      var url = location.href.split("#")[0] + ficheHref(curFiche);
      var data = { title: curFiche.name + " — Onrecord", text: curFiche.name + " : déclarations publiques et liens, avec leurs sources.", url: url };
      if (navigator.share) { navigator.share(data).catch(function () {}); return; }
      copyText(url).then(function () { toast("Lien copié : " + url); donateInvite(); }, function () { toast(url); });
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

  /* ==========================================================================
     v7 : cartes de citation (PNG 1080x1350), « Copier le lien », Avant / maintenant
     ========================================================================== */
  var CARD_W = 1080, CARD_H = 1350, CARD_PAD = 96;
  var CARD_FONT = '-apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Helvetica, Arial, "Liberation Sans", sans-serif';
  var SITE_HOST = "onrecord-fr.vercel.app";
  function dmy(d) { var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(d || ""); return m ? m[3] + "/" + m[2] + "/" + m[1] : (d || "date non précisée"); }
  function hostOf(u) { try { return new URL(u).hostname.replace(/^www\./, ""); } catch (e) { return ""; } }
  function stLink(n, i) { return location.origin + location.pathname + ficheHref(n) + "#d" + i; }
  function duoLink(n) { return location.origin + location.pathname + ficheHref(n) + "#am"; }
  /* découpe en lignes (les mots trop longs sont coupés par caractère, sans rien retirer) */
  function wrapLines(ctx, text, maxW) {
    var words = text.split(/ /), lines = [], cur = "";
    words.forEach(function (w) {
      var t = cur ? cur + " " + w : w;
      if (ctx.measureText(t).width <= maxW) { cur = t; return; }
      if (cur) lines.push(cur);
      cur = w;
      while (ctx.measureText(cur).width > maxW && cur.length > 1) {
        var k = cur.length; while (k > 1 && ctx.measureText(cur.slice(0, k)).width > maxW) k--;
        lines.push(cur.slice(0, k)); cur = cur.slice(k);
      }
    });
    if (cur) lines.push(cur);
    return lines;
  }
  /* Ajuste une citation dans une boîte : police décroissante, puis troncature « […] » en dernier recours. */
  function fitQuote(ctx, quote, maxW, maxH, maxSize, minSize, weight) {
    var q = String(quote).replace(/\s+/g, " ").trim();
    function lay(txt, size) { ctx.font = weight + " " + size + "px " + CARD_FONT; var L = wrapLines(ctx, "«\u00a0" + txt + "\u00a0»", maxW); return { lines: L, size: size, lh: Math.round(size * 1.3) }; }
    for (var s = maxSize; s >= minSize; s -= 2) {
      var r = lay(q, s); if (r.lines.length * r.lh <= maxH) { r.truncated = false; return r; }
    }
    var words = q.split(" "), lo = 1, hi = words.length - 1, best = null;
    while (lo <= hi) {
      var mid = (lo + hi) >> 1, t = lay(words.slice(0, mid).join(" ").replace(/[\s,;:.]+$/, "") + " […]", minSize);
      if (t.lines.length * t.lh <= maxH) { best = t; lo = mid + 1; } else hi = mid - 1;
    }
    best = best || lay("[…]", minSize); best.truncated = true; return best;
  }
  function clampText(ctx, text, maxW, maxLines) {
    var L = wrapLines(ctx, text, maxW);
    if (L.length <= maxLines) return L;
    var words = text.split(" "), lo = 1, hi = words.length, best = ["[…]"];
    while (lo <= hi) { var mid = (lo + hi) >> 1, t = wrapLines(ctx, words.slice(0, mid).join(" ").replace(/[\s,;:.]+$/, "") + " […]", maxW); if (t.length <= maxLines) { best = t; lo = mid + 1; } else hi = mid - 1; }
    return best;
  }
  function cardBase(ctx, kicker, im) {
    var g = ctx.createLinearGradient(0, 0, CARD_W, CARD_H);
    g.addColorStop(0, "#3b0a57"); g.addColorStop(0.55, "#5a1a7a"); g.addColorStop(1, "#8e1d5c");
    ctx.fillStyle = g; ctx.fillRect(0, 0, CARD_W, CARD_H);
    if (im) { try { drawPortraitBg(ctx, im); } catch (e) {} }
    ctx.textBaseline = "alphabetic"; ctx.textAlign = "left";
    ctx.fillStyle = "#ffffff"; ctx.font = "800 64px " + CARD_FONT; ctx.fillText("Onrecord", CARD_PAD, 150);
    ctx.fillStyle = "rgba(255,255,255,.72)"; ctx.font = "500 30px " + CARD_FONT; ctx.fillText(kicker || "Leurs mots, datés et sourcés.", CARD_PAD, 200);
    ctx.fillStyle = "rgba(255,255,255,.28)"; ctx.fillRect(CARD_PAD, 236, CARD_W - 2 * CARD_PAD, 2);
    ctx.fillStyle = "rgba(255,255,255,.28)"; ctx.fillRect(CARD_PAD, CARD_H - 140, CARD_W - 2 * CARD_PAD, 2);
    ctx.fillStyle = "rgba(255,255,255,.9)"; ctx.font = "600 32px " + CARD_FONT; ctx.fillText(SITE_HOST, CARD_PAD, CARD_H - 76);
  }
  /* v15 : portrait sur les cartes (préchargé, dessin synchrone pour rester lié au geste) */
  window.__imgCache = window.__imgCache || {};
  function preloadImg(src) {
    if (!src || window.__imgCache[src]) return;
    var im = new Image(); im.decoding = "async"; im.src = src; window.__imgCache[src] = im;
    if (im.decode) im.decode().catch(function () {});
  }
  function readyImg(src) {
    if (!src) return null;
    var im = window.__imgCache[src];
    if (im && im.complete && im.naturalWidth) return im;
    var all = document.images;
    for (var k = 0; k < all.length; k++) if (all[k].getAttribute("src") === src && all[k].complete && all[k].naturalWidth) return all[k];
    preloadImg(src); return null;
  }
  function coverCrop(im, w, h) {
    var iw = im.naturalWidth, ih = im.naturalHeight, sc = Math.max(w / iw, h / ih), sw = w / sc, sh = h / sc;
    return [(iw - sw) / 2, Math.max(0, (ih - sh) * 0.25), sw, sh];
  }
  function drawPortraitBg(ctx, im) {
    var x0 = Math.round(CARD_W * 0.3), w = CARD_W - x0, h = Math.round(CARD_H * 0.8), cr = coverCrop(im, w, h);
    var o = document.createElement("canvas"); o.width = w; o.height = h;
    var oc = o.getContext("2d");
    try { oc.filter = "saturate(.55) contrast(1.05)"; } catch (e) {}
    oc.drawImage(im, cr[0], cr[1], cr[2], cr[3], 0, 0, w, h);
    try { oc.filter = "none"; } catch (e) {}
    oc.fillStyle = "rgba(40,8,64,.32)"; oc.fillRect(0, 0, w, h);
    /* fondu doux : masque alpha gauche→droite puis haut→bas */
    oc.globalCompositeOperation = "destination-in";
    var gl = oc.createLinearGradient(0, 0, w, 0);
    gl.addColorStop(0, "rgba(0,0,0,0)"); gl.addColorStop(0.45, "rgba(0,0,0,.75)"); gl.addColorStop(1, "rgba(0,0,0,1)");
    oc.fillStyle = gl; oc.fillRect(0, 0, w, h);
    var gb = oc.createLinearGradient(0, 0, 0, h);
    gb.addColorStop(0, "rgba(0,0,0,1)"); gb.addColorStop(0.55, "rgba(0,0,0,1)"); gb.addColorStop(1, "rgba(0,0,0,0)");
    oc.fillStyle = gb; oc.fillRect(0, 0, w, h);
    ctx.save(); ctx.globalAlpha = 0.62; ctx.drawImage(o, x0, 0); ctx.restore();
  }
  var SPHERE_GRAD = {
    partis: ["#9a3412", "#fb923c"], medias: ["#14532d", "#4ade80"], argent: ["#78350f", "#fbbf24"],
    idees: ["#134e4a", "#5eead4"], edition: ["#4a044e", "#e879f9"], institutions: ["#1e293b", "#cbd5e1"]
  };
  var KIND_GRAD = {
    person: ["#3b0a57", "#7b2cbf", "#c2185b"], parti: ["#9a3412", "#fb923c"], media: ["#14532d", "#4ade80"],
    association: ["#4a044e", "#e879f9"], evenement: ["#881337", "#fb7185"], org: ["#1e293b", "#cbd5e1"]
  };
  function monoColors(n) {
    if (n && n.sphere && SPHERE_GRAD[n.sphere]) return SPHERE_GRAD[n.sphere];
    if (n && KIND_GRAD[n._sub]) return KIND_GRAD[n._sub];
    return KIND_GRAD.person;
  }
  function drawMonogram(ctx, n, cx, cy, r) {
    var cols = monoColors(n), g = ctx.createLinearGradient(cx - r, cy - r, cx + r, cy + r);
    cols.forEach(function (col, i) { g.addColorStop(cols.length === 1 ? 0 : i / (cols.length - 1), col); });
    ctx.save();
    ctx.beginPath(); ctx.arc(cx, cy, r + 4, 0, Math.PI * 2); ctx.fillStyle = "rgba(255,255,255,.92)"; ctx.fill();
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fillStyle = g; ctx.fill();
    ctx.fillStyle = "#ffffff"; ctx.font = "700 " + Math.round(r * 0.7) + "px " + CARD_FONT;
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(initials(n.name), cx, cy + Math.round(r * 0.04));
    ctx.restore();
    ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
  }
  function drawPhotoCredit(ctx, n) {
    if (!n || !n.image || !n.image_credit) return;
    var cr = n.image_credit;
    var t = "Photo : " + (cr.author || "auteur non précisé") + (cr.license ? " · " + cr.license : "");
    ctx.fillStyle = "rgba(255,255,255,.62)"; ctx.font = "400 18px " + CARD_FONT;
    ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
    ctx.fillText(clampText(ctx, t, CARD_W - 2 * CARD_PAD, 1)[0], CARD_PAD, CARD_H - 36);
  }
  function drawPortraitRing(ctx, im, cx, cy, r) {
    ctx.save();
    ctx.shadowColor = "rgba(0,0,0,.45)"; ctx.shadowBlur = 30; ctx.shadowOffsetY = 10;
    ctx.beginPath(); ctx.arc(cx, cy, r + 5, 0, Math.PI * 2); ctx.fillStyle = "#ffffff"; ctx.fill();
    ctx.restore(); ctx.save();
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.clip();
    var cr = coverCrop(im, 2 * r, 2 * r); ctx.drawImage(im, cr[0], cr[1], cr[2], cr[3], cx - r, cy - r, 2 * r, 2 * r);
    ctx.restore();
  }
  function drawLines(ctx, r, x, y) { ctx.font = "600 " + r.size + "px " + CARD_FONT; r.lines.forEach(function (l, k) { ctx.fillText(l, x, y + r.size + k * r.lh); }); return y + r.lines.length * r.lh; }
  function drawSource(ctx, s, x, y, maxW, lines) {
    ctx.fillStyle = "rgba(255,255,255,.72)"; ctx.font = "400 28px " + CARD_FONT;
    var t = clampText(ctx, "Support : " + (s.medium || "non précisé"), maxW, lines);
    t.forEach(function (l, k) { ctx.fillText(l, x, y + 28 + k * 38); });
    y += t.length * 38;
    var h = hostOf(s.url); if (h) { ctx.fillText("Source : " + h, x, y + 28 + 6); y += 44; }
    return y;
  }
  function renderCard(n, s) {
    var c = document.createElement("canvas"); c.width = CARD_W; c.height = CARD_H;
    var ctx = c.getContext("2d"), W = CARD_W - 2 * CARD_PAD;
    var im = readyImg(n.image);
    cardBase(ctx, null, im);
    ctx.fillStyle = "#ffffff";
    var qh = im ? 560 : 580;
    var r = fitQuote(ctx, s.quote, W, qh, 72, 34, "600");
    drawLines(ctx, r, CARD_PAD, 300);
    var y = 300 + qh + 40, tx = CARD_PAD, tw = W;
    if (im) { var R = 100; drawPortraitRing(ctx, im, CARD_PAD + R, y + R, R); tx = CARD_PAD + 2 * R + 40; tw = W - 2 * R - 40; }
    else { var Rm = 68; drawMonogram(ctx, n, CARD_PAD + Rm, y + Rm, Rm); tx = CARD_PAD + 2 * Rm + 32; tw = W - 2 * Rm - 32; }
    ctx.fillStyle = "#ffffff"; ctx.font = "700 44px " + CARD_FONT; ctx.fillText(clampText(ctx, n.name, tw, 1)[0], tx, y + 44); y += 64;
    ctx.fillStyle = "rgba(255,255,255,.9)"; ctx.font = "600 32px " + CARD_FONT; ctx.fillText(dmy(s.date), tx, y + 32); y += 44;
    drawSource(ctx, s, tx, y, tw, 2);
    drawPhotoCredit(ctx, n);
    c.__truncated = r.truncated; c.__fontSize = r.size; c.__portrait = !!im; window.__lastCardHadPortrait = !!im;
    return c;
  }
  function renderDuoCard(n, a, b) {
    var c = document.createElement("canvas"); c.width = CARD_W; c.height = CARD_H;
    var ctx = c.getContext("2d"), W = CARD_W - 2 * CARD_PAD, tr = false, y = 268;
    var im = readyImg(n.image);
    cardBase(ctx, "Avant / maintenant · écart : " + gapText(a.date, b.date), im);
    if (im) drawPortraitRing(ctx, im, CARD_PAD + 36, y + 30, 36);
    else drawMonogram(ctx, n, CARD_PAD + 36, y + 30, 36);
    var nx = CARD_PAD + 92;
    ctx.fillStyle = "#ffffff"; ctx.font = "700 44px " + CARD_FONT; ctx.fillText(clampText(ctx, n.name, W - (nx - CARD_PAD), 1)[0], nx, y + 44); y += 76;
    [a, b].forEach(function (s, k) {
      ctx.fillStyle = "rgba(255,255,255,.9)"; ctx.font = "700 32px " + CARD_FONT; ctx.fillText((k ? "Maintenant · " : "Avant · ") + dmy(s.date), CARD_PAD, y + 32); y += 50;
      ctx.fillStyle = "#ffffff";
      var r = fitQuote(ctx, s.quote, W, 250, 50, 28, "600"); tr = tr || r.truncated;
      drawLines(ctx, r, CARD_PAD, y); y += 250 + 6;
      y = drawSource(ctx, s, CARD_PAD, y, W, 1) + (k ? 0 : 24);
      if (!k) { ctx.fillStyle = "rgba(255,255,255,.2)"; ctx.fillRect(CARD_PAD, y, W, 2); y += 26; }
    });
    drawPhotoCredit(ctx, n);
    c.__truncated = tr; c.__portrait = !!im; window.__lastCardHadPortrait = !!im;
    return c;
  }
  function canvasBlob(c) {
    /* toDataURL est synchrone : le partage reste lié au geste de l'utilisateur (exigence de Safari iOS) */
    var u = c.toDataURL("image/png"), bin = atob(u.split(",")[1]), arr = new Uint8Array(bin.length);
    for (var k = 0; k < bin.length; k++) arr[k] = bin.charCodeAt(k);
    return { blob: new Blob([arr], { type: "image/png" }), dataUrl: u };
  }
  function shareCanvas(c, fname, title, link) {
    var o = canvasBlob(c); window.__lastCard = { dataUrl: o.dataUrl, size: o.blob.size, w: c.width, h: c.height, truncated: !!c.__truncated, portrait: !!c.__portrait, name: fname };
    var file = null;
    try { file = new File([o.blob], fname, { type: "image/png" }); } catch (e) { file = null; }
    if (file && navigator.canShare && navigator.share && navigator.canShare({ files: [file] })) {
      navigator.share({ files: [file], title: title, text: title + " — " + link }).then(donateInvite).catch(function () {});
      return "share";
    }
    var a = document.createElement("a"), url = URL.createObjectURL(o.blob);
    a.href = url; a.download = fname; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
    toast("Image téléchargée : " + fname); donateInvite();
    return "download";
  }
  function slug(s) { return norm(s).replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""); }
  function copyLink(link) { copyText(link).then(function () { toast("Lien copié"); donateInvite(); }, function () { toast(link); }); }
  function actionsHtml(n, i) {
    return '<button type="button" class="act" data-act="share" data-n="' + esc(n.id) + '" data-i="' + i + '">Partager</button>' +
      '<button type="button" class="act" data-act="copy" data-n="' + esc(n.id) + '" data-i="' + i + '">Copier le lien</button>';
  }
  /* écart neutre entre deux dates */
  function gapText(d1, d2) {
    var a = /^(\d{4})-(\d{2})-(\d{2})$/.exec(d1 || ""), b = /^(\d{4})-(\d{2})-(\d{2})$/.exec(d2 || "");
    if (!a || !b) return "—";
    if (d1 > d2) { var t = a; a = b; b = t; }
    var mo = (+b[1] - +a[1]) * 12 + (+b[2] - +a[2]) - (+b[3] < +a[3] ? 1 : 0);
    if (mo < 1) { var days = Math.round((Date.UTC(+b[1], +b[2] - 1, +b[3]) - Date.UTC(+a[1], +a[2] - 1, +a[3])) / 864e5); return days === 0 ? "même jour" : plural(days, "jour", "jours"); }
    if (mo < 12) return mo + " mois";
    var y = Math.floor(mo / 12), m = mo % 12;
    return plural(y, "an", "ans") + (m ? " et " + m + " mois" : "");
  }
  function datedSt(n) { return (n.statements || []).map(function (s, i) { return { s: s, i: i }; }).filter(function (x) { return /^\d{4}-\d{2}-\d{2}$/.test(x.s.date || ""); }).sort(function (a, b) { return a.s.date.localeCompare(b.s.date) || a.i - b.i; }); }
  function defaultPair(list) {
    var byT = {}, best = null;
    list.forEach(function (x) { (byT[x.s.theme || ""] = byT[x.s.theme || ""] || []).push(x); });
    Object.keys(byT).forEach(function (t) {
      var g = byT[t]; if (g.length < 2) return;
      var span = Date.parse(g[g.length - 1].s.date) - Date.parse(g[0].s.date);
      if (!best || span > best.span) best = { a: g[0], b: g[g.length - 1], span: span };
    });
    return best && best.span > 0 ? [best.a.i, best.b.i] : [list[0].i, list[list.length - 1].i];
  }
  var amSel = {};
  function amHtml(n) {
    var list = datedSt(n);
    if (n.type !== "person" || list.length < 2) return "";
    var p = amSel[n.id] || defaultPair(list);
    function opts(sel) { return list.map(function (x) { return '<option value="' + x.i + '"' + (x.i === sel ? " selected" : "") + ">" + dmy(x.s.date) + " · " + esc(String(x.s.quote).slice(0, 60)) + (String(x.s.quote).length > 60 ? "…" : "") + "</option>"; }).join(""); }
    var A = n.statements[p[0]], B = n.statements[p[1]];
    if ((A.date || "") > (B.date || "")) { var t = A; A = B; B = t; p = [p[1], p[0]]; }
    function col(s, i, lab) {
      return '<article class="am-card"><p class="am-k">' + lab + ' · <time datetime="' + esc(s.date) + '">' + dmy(s.date) + "</time></p><blockquote>" + quoteHtml(s.quote) + "</blockquote>" +
        '<div class="meta"><span class="medium">' + esc(s.medium) + "</span></div>" +
        '<div class="meta actions">' + srcLink(s.url, "Lire la source") + archLink(s) + '<a class="act" href="' + ficheHref(n) + "#d" + i + '">Voir dans la frise</a></div></article>';
    }
    return '<section class="am" id="am" aria-labelledby="am-h"><h2 class="h-sec" id="am-h">Avant / maintenant</h2>' +
      '<div class="am-pick"><label>Avant <select id="am-a">' + opts(p[0]) + '</select></label><label>Maintenant <select id="am-b">' + opts(p[1]) + "</select></label></div>" +
      '<p class="am-gap">Écart : <strong id="am-gap">' + gapText(A.date, B.date) + "</strong></p>" +
      '<div class="am-grid">' + col(A, p[0], "Avant") + col(B, p[1], "Maintenant") + "</div>" +
      '<div class="meta actions am-act"><button type="button" class="act" data-act="share-duo" data-n="' + esc(n.id) + '" data-a="' + p[0] + '" data-b="' + p[1] + '">Partager</button>' +
      '<button type="button" class="act" data-act="copy-duo" data-n="' + esc(n.id) + '">Copier le lien</button></div></section>';
  }
  function bindCards() {
    document.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("button.act[data-act]"); if (!b) return;
      var n = byId[b.getAttribute("data-n")]; if (!n) return;
      var act = b.getAttribute("data-act");
      if (act === "share" || act === "copy") {
        var i = +b.getAttribute("data-i"), s = n.statements[i];
        if (act === "copy") return copyLink(stLink(n, i));
        window.__lastShare = shareCanvas(renderCard(n, s), "onrecord-" + slug(n.name) + "-" + (s.date || "sd") + ".png", n.name + " — Onrecord", stLink(n, i));
      } else if (act === "copy-duo") copyLink(duoLink(n));
      else if (act === "share-duo") {
        var A = n.statements[+b.getAttribute("data-a")], B = n.statements[+b.getAttribute("data-b")];
        window.__lastShare = shareCanvas(renderDuoCard(n, A, B), "onrecord-" + slug(n.name) + "-avant-maintenant.png", n.name + " — Avant / maintenant — Onrecord", duoLink(n));
      }
    });
    document.addEventListener("change", function (e) {
      if (!curFiche || (e.target.id !== "am-a" && e.target.id !== "am-b")) return;
      var na = +$("am-a").value, nb = +$("am-b").value;
      if (na === nb) { toast("Choisissez deux déclarations différentes."); }
      else amSel[curFiche.id] = [na, nb];
      var sec = $("am"); var tmp = document.createElement("div"); tmp.innerHTML = amHtml(curFiche); sec.replaceWith(tmp.firstChild);
    });
    window.__renderCard = function (id, i) { var c = renderCard(byId[id], byId[id].statements[i]); return { dataUrl: c.toDataURL("image/png"), truncated: c.__truncated, size: c.__fontSize }; };
    window.__renderCardQuote = function (id, q) { var c = renderCard(byId[id], { quote: q, date: "2026-01-01", medium: "Test", url: "https://example.org/" }); return { dataUrl: c.toDataURL("image/png"), truncated: c.__truncated, size: c.__fontSize }; };
  }
  function renderMethode() {
    var mail = String(CFG.CORRECTION_EMAIL || "").trim(), el = $("methode-contact");
    if (/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail)) el.innerHTML = 'Écrire à <a href="mailto:' + esc(mail) + '?subject=' + encodeURIComponent("Onrecord : demande de correction ou de retrait") + '">' + esc(mail) + "</a> en indiquant la fiche concernée (lien), l'élément en cause et, si possible, une source.";
    else el.textContent = "";
  }
  /* ---------- Proposer une mise à jour (#/contribuer) ---------- */
  var EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  function contribMessage() {
    function v(id) { return String($(id).value || "").trim(); }
    var f = { type: v("cf-type"), who: v("cf-who"), fiche: v("cf-fiche"), date: v("cf-date"), text: v("cf-text"), src: v("cf-src"), mail: v("cf-mail") };
    var err = [];
    if (!f.type) err.push("choisir un type de proposition");
    if (!f.text) err.push("indiquer une citation ou une description");
    if (!/^https?:\/\/\S+\.\S+/.test(f.src)) err.push("indiquer une URL de source valide (https://…)");
    if (f.mail && !EMAIL_RE.test(f.mail)) err.push("vérifier l'adresse e-mail");
    var body = ["Proposition de mise à jour — Onrecord", "",
      "Type : " + f.type, "Personne ou organisation : " + (f.who || "—"), "Fiche Onrecord : " + (f.fiche || "—"),
      "Date du propos : " + (f.date ? fmtDate(f.date) : "—"), "", "Citation ou description :", f.text, "",
      "Source : " + f.src, "E-mail pour le suivi : " + (f.mail || "—")].join("\n");
    return { err: err, body: body };
  }
  function initContrib() {
    $("contrib-form").addEventListener("submit", function (ev) {
      ev.preventDefault();
      var r = contribMessage(), e = $("cf-err");
      if (r.err.length) { e.textContent = "Merci de " + r.err.join(", ") + "."; e.hidden = false; $("cf-out").hidden = true; return; }
      e.hidden = true;
      var mail = String(CFG.CORRECTION_EMAIL || "").trim();
      if (EMAIL_RE.test(mail)) {
        var href = "mailto:" + mail + "?subject=" + encodeURIComponent("Onrecord : proposition de mise à jour") + "&body=" + encodeURIComponent(r.body);
        window.__lastMailto = href; $("cf-out").hidden = true;
        toast("Votre application mail s'ouvre…"); location.href = href;
      } else {
        $("cf-msg").value = r.body; $("cf-out").hidden = false; $("cf-out").scrollIntoView({ block: "nearest" });
      }
    });
    $("cf-copy").addEventListener("click", function () {
      copyText($("cf-msg").value).then(function () { toast("Message copié"); }, function () { $("cf-msg").select(); toast("Sélectionnez puis copiez le message"); });
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
      '<span class="badge lk">Lien public</span>' + natureBadge(edgeNature(e)) + '<p class="tl-rel"><a href="' + ficheHref(a) + '">' + esc(a.name) + '</a> → <a href="' + ficheHref(b) + '">' + esc(b.name) + "</a> : " + esc(e.relation) + "</p>" +
      '<div class="meta actions">' + srcLink(e.url, "Lire la source") + archLink(e) + "</div></article></li>";
  }

  /* ---------- v22 : échelle du pouvoir ----------
     Palier = fonction publique déjà écrite sur la fiche. Pas un jugement.
     Les liens sont les edges existants. Un montant de fortune n'est affiché
     que si une source publique datée le donne ; ici, seul le rang Challenges
     est repris, parce que la page publique ne publie pas la somme. */
  var POWER_TIERS = [
    { id: "evt", label: "Événements documentés", hint: "Fait public daté. Ce n'est pas une fonction permanente." },
    { id: "col", label: "Collectifs et groupes", hint: "Collectif, groupement ou organisation dissoute, d'après la fiche." },
    { id: "asso", label: "Associations et représentants", hint: "Association, organisation représentative, établissement ou institut de sondage, et la personne qui la représente." },
    { id: "jour", label: "Auteurs, journalistes et éditorialistes", hint: "Fonction d'auteur, de journaliste, d'éditorialiste ou d'animateur, d'après la fiche." },
    { id: "media", label: "Médias et maisons d'édition", hint: "Chaîne, radio, titre de presse ou maison d'édition, d'après la fiche." },
    { id: "elu", label: "Élus, candidats et dirigeants de parti", hint: "Mandat, candidature déclarée ou direction de parti, d'après la fiche." },
    { id: "gouv", label: "Gouvernement et institutions", hint: "Fonction au gouvernement, à la présidence, ou institution publique, d'après la fiche." },
    { id: "prop", label: "Propriétaires et groupes de médias", hint: "Groupe de médias, actionnaire de référence ou investisseur, d'après la fiche." }
  ];
  var POWER_OF = {
    "conf-jerusalem-2025": 0, "loi-immigration-2023": 0, "proces-nantes-menaces-2026": 0,
    "civitas": 1, "gud": 1, "generation-identitaire": 1, "les-remparts": 1, "zouaves-paris": 1, "nemesis": 1, "pericles": 1,
    "avocats-sans-frontieres": 2, "crif": 2, "yad-vashem-fr": 2, "patrick-klugman": 2, "yonathan-arfi": 2, "issep": 2,
    "serge-klarsfeld": 3, "bernard-henri-levy": 3, "raphael-enthoven": 3, "renaud-camus": 3, "caroline-fourest": 3,
    "geoffroy-lejeune": 3, "elisabeth-levy": 3, "gilles-william-goldnadel": 3, "gerard-carreyrou": 3,
    "jean-dominique-merchet": 3, "joseph-thouvenel": 3, "jules-torres": 3, "cyril-hanouna": 3,
    "c8": 4, "cnews": 4, "causeur": 4, "europe1": 4, "franc-tireur": 4, "m6": 4, "lexpress": 4, "jdd": 4,
    "le-point": 4, "sud-radio": 4, "valeurs-actuelles": 4, "fayard": 4,
    "dominique-de-villepin": 5, "fabien-roussel": 5, "gabriel-attal": 5, "jean-luc-melenchon": 5, "marine-tondelier": 5,
    "raphael-glucksmann": 5, "xavier-bertrand": 5, "edouard-philippe": 5, "caroline-yadan": 5, "marine-le-pen": 5,
    "marion-marechal": 5, "meyer-habib": 5, "eric-ciotti": 5, "robert-menard": 5, "valerie-pecresse": 5,
    "yael-braun-pivet": 5, "bruno-retailleau": 5, "eric-zemmour": 5, "jordan-bardella": 5,
    "identite-libertes": 5, "lr": 5, "reconquete": 5, "renaissance-epr": 5, "rn": 5,
    "aurore-berge": 6, "emmanuel-macron": 6, "gerald-darmanin": 6, "manuel-valls": 6,
    "arcom": 6, "conseil-constitutionnel": 6, "conseil-etat": 6, "pnat": 6,
    "vincent-bollore": 7, "pierre-edouard-sterin": 7, "lagardere": 7, "vivendi-canal": 7,
    "institut-iliade": 2, "nuits-du-bien-commun": 2, "philippe-conrad": 2, "arnaud-rerolle": 2,
    "pascal-praud": 3, "lise-boell": 3, "serge-nedjar": 3, "gerald-brice-viret": 3,
    "tugdual-denis": 3, "erik-tegner": 3, "donat-vidal-revel": 3, "constance-benque": 3,
    "prisma-media": 4, "frontieres": 4,
    "sarah-knafo": 5, "philippe-olivier": 5, "kevin-pfeffer": 5, "udr": 5,
    "francois-durvye": 7, "alban-du-rostu": 7, "arnaud-lagardere": 7,
    "ifop": 2, "opinionway": 2, "institut-csa": 2, "harris-interactive": 2, "toluna": 2, "elabe": 2,
    "commission-des-sondages": 6,
    "lfpi": 7, "havas": 7, "les-echos-le-parisien": 7, "lvmh": 7
  };
  /* Rangs publiés le 8 juillet 2026. La page publique donne le rang et la variation,
     pas le montant : aucun chiffre de fortune n'est donc affiché. */
  var FORTUNE = {
    "vincent-bollore": {
      rank: 13, date: "2026-07-08", source: "Challenges", family: true,
      url: "https://www.challenges.fr/classements/fortune/vincent-bollore-et-sa-famille_26544"
    },
    "pierre-edouard-sterin": {
      rank: 74, date: "2026-07-08", source: "Challenges", family: false,
      url: "https://www.challenges.fr/classements/fortune/pierre-edouard-sterin_26641"
    }
  };
  var powFilter = "tout", powNature = "ascension", powSel = null, powBuilt = "", powReady = false, climbToken = 0;

  function fallbackPow(n) {
    var sub = n.subcategory || "", blob = sub + " " + (n.role || "") + " " + (n.category || "");
    if (n.category === "Événements" || /événement/i.test(sub)) return 0;
    if (n.type === "org" && /dissous|dissoute|collectif|projet/i.test(blob)) return 1;
    if (/Associations|Projets/.test(sub)) return 2;
    if (n.category === "Journalistes & éditorialistes" || n.category === "Intellectuels & essayistes" || sub === "Animateurs & producteurs") return 3;
    if (sub === "Chaînes, radios & titres" || sub === "Édition") return 4;
    if (sub === "Gouvernement & exécutif" || sub === "Institutions publiques") return 6;
    if (sub === "Propriétaires, financeurs & groupes") return 7;
    if (n.category === "Responsables politiques" || /parti/i.test(sub)) return 5;
    return 3;
  }
  function assignPower() {
    DATA.nodes.forEach(function (n) {
      n._pow = Object.prototype.hasOwnProperty.call(POWER_OF, n.id) ? POWER_OF[n.id] : fallbackPow(n);
    });
  }
  function nodeInFilter(n, f) {
    if (!n) return false;
    if (!f || f === "tout") return true;
    return (n.sections || []).indexOf(f) >= 0;
  }
  function visibleNode(n) { return nodeInFilter(n, powFilter); }
  function tierIndex(id) { var n = byId[id]; return n && typeof n._pow === "number" ? n._pow : -1; }
  function edgesBetween(a, b, pred) {
    return (edgesOf[a] || []).filter(function (e) {
      var hit = (e.source === a && e.target === b) || (e.source === b && e.target === a);
      return hit && (!pred || pred(e));
    });
  }
  function edgeShown(e) {
    if (powNature === "tous") return true;
    return edgeNature(e) === powNature;
  }
  function isAscent(e) { return edgeNature(e) === "ascension"; }
  function visNeighbors(id, pred) {
    var out = [];
    (edgesOf[id] || []).forEach(function (e) {
      if (pred && !pred(e)) return;
      var o = e.source === id ? e.target : e.source;
      if (byId[o] && visibleNode(byId[o])) out.push({ id: o, e: e });
    });
    return out;
  }
  function uniqueDir(id) {
    var up = {}, down = {}, same = {};
    visNeighbors(id, edgeShown).forEach(function (nb) {
      var d = tierIndex(nb.id) - tierIndex(id);
      if (d > 0) up[nb.id] = 1; else if (d < 0) down[nb.id] = 1; else same[nb.id] = 1;
    });
    return { up: Object.keys(up).length, down: Object.keys(down).length, same: Object.keys(same).length };
  }
  function climbPath(start) {
    if (!byId[start] || !visibleNode(byId[start])) return [];
    /* Plus court chemin vers le palier le plus haut atteignable.
       À longueur égale, on garde le fil qui traverse les paliers les plus hauts
       (somme des indices). Uniquement des edges existants. */
    var dist = {}, score = {}, parent = {};
    dist[start] = 0; score[start] = tierIndex(start); parent[start] = null;
    var q = [start], guard = 0;
    while (q.length && guard++ < 4000) {
      var id = q.shift(), seen = {};
      visNeighbors(id, isAscent).forEach(function (nb) {
        if (seen[nb.id]) return;
        seen[nb.id] = 1;
        var nd = dist[id] + 1, ns = score[id] + tierIndex(nb.id);
        var better = dist[nb.id] === undefined || nd < dist[nb.id] || (nd === dist[nb.id] && ns > score[nb.id]);
        if (!better) return;
        dist[nb.id] = nd; score[nb.id] = ns; parent[nb.id] = id;
        q.push(nb.id);
      });
    }
    var best = start;
    Object.keys(parent).forEach(function (id) {
      var better = tierIndex(id) > tierIndex(best) ||
        (tierIndex(id) === tierIndex(best) && dist[id] < dist[best]) ||
        (tierIndex(id) === tierIndex(best) && dist[id] === dist[best] && score[id] > score[best]) ||
        (tierIndex(id) === tierIndex(best) && dist[id] === dist[best] && score[id] === score[best] && id.localeCompare(best) < 0);
      if (better) best = id;
    });
    var path = [], cur = best, hop = 0;
    while (cur && hop++ < 40) { path.push(cur); cur = parent[cur]; }
    path.reverse();
    return path;
  }
  function longestFil() {
    var best = 1;
    DATA.nodes.forEach(function (n) {
      if (!visibleNode(n)) return;
      var len = climbPath(n.id).length;
      if (len > best) best = len;
    });
    return best;
  }
  function fortuneLine(n, longNote) {
    var f = FORTUNE[n.id];
    if (!f || !/^https:\/\//.test(f.url)) return "";
    var label = f.rank + "e rang · " + f.source + " · " + fmtDate(f.date);
    var note = "";
    if (longNote) {
      note = '<p class="pow-fort-n">Rang du classement Challenges des 500 plus grandes fortunes de France, publié le ' + fmtDate(f.date) + "." +
        (f.family ? " L'entrée publiée concerne " + esc(n.name) + " et sa famille." : "") +
        " Le montant en euros n'est pas affiché : la page publique indique le rang et la variation, pas la somme.</p>";
    }
    return '<a class="pow-fort" href="' + esc(f.url) + '" target="_blank" rel="noopener noreferrer">' + esc(label) + "</a>" + note;
  }
  function goPower(id, replace) {
    var url = "#/pouvoir" + (id ? "/" + encodeURIComponent(id) : "");
    if (replace) { history.replaceState(null, "", url); route(); }
    else if (location.hash !== url) location.hash = url;
    else route();
  }
  function bindPouvoir() {
    $("pow-seg").addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-pow]");
      if (!b) return;
      climbToken++;
      powFilter = b.getAttribute("data-pow");
      powBuilt = "";
      if (powSel && !visibleNode(byId[powSel])) goPower(null, true);
      else { buildLadder(); applyPowSelection(false); }
    });
    $("pow-nat").addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-nat]");
      if (!b) return;
      climbToken++;
      powNature = b.getAttribute("data-nat");
      powBuilt = "";
      buildLadder();
      applyPowSelection(false);
    });
    $("pow-ladder").addEventListener("click", function (ev) {
      if (ev.target.closest("a")) return;
      var b = ev.target.closest(".pow-node");
      if (!b) return;
      climbToken++;
      goPower(b.getAttribute("data-id"), false);
    });
    $("pow-sheet").addEventListener("click", function (ev) {
      var go = ev.target.closest("[data-pow-go]");
      if (go) { climbToken++; goPower(go.getAttribute("data-pow-go"), false); return; }
      if (ev.target.closest("#pow-climb")) { playClimb(); return; }
      if (ev.target.closest("#pow-close")) { climbToken++; goPower(null, false); }
    });
  }
  function buildLadder() {
    var buckets = POWER_TIERS.map(function () { return []; });
    DATA.nodes.forEach(function (n) { if (visibleNode(n)) buckets[n._pow].push(n); });
    buckets.forEach(function (list) {
      list.sort(function (a, b) {
        var fa = FORTUNE[a.id], fb = FORTUNE[b.id];
        if (fa && fb && fa.rank !== fb.rank) return fa.rank - fb.rank;
        if (fa && !fb) return -1;
        if (fb && !fa) return 1;
        return a.name.localeCompare(b.name, "fr");
      });
    });
    var html = "";
    for (var t = POWER_TIERS.length - 1; t >= 0; t--) {
      var tier = POWER_TIERS[t], list = buckets[t];
      if (!list.length) continue;
      var upLinks = 0;
      list.forEach(function (n) {
        var seen = {};
        visNeighbors(n.id, edgeShown).forEach(function (nb) {
          if (tierIndex(nb.id) > t && !seen[nb.id]) { seen[nb.id] = 1; upLinks++; }
        });
      });
      var mark = t === POWER_TIERS.length - 1 ? "Sommet" : (t === 0 ? "Base" : "");
      html += '<section class="pow-tier" data-tier="' + tier.id + '" style="--lift:' + t + '"><header class="pow-tier-h"><p class="pow-k">' + (mark ? '<span class="pow-mark">' + mark + "</span>" : "") + '<h2>' + esc(tier.label) + '</h2></p><p class="pow-hint">' + esc(tier.hint) + '</p><p class="pow-meta">' + list.length + (list.length > 1 ? " fiches" : " fiche") + (upLinks ? " · " + upLinks + (upLinks > 1 ? " liens" : " lien") + " vers un palier supérieur" : "") + '</p></header><ul class="pow-nodes">' +
        list.map(function (n) {
          var d = uniqueDir(n.id);
          var aria = n.name + ". " + d.up + " acteur" + (d.up > 1 ? "s" : "") + " plus haut, " + d.down + " plus bas";
          return '<li class="pow-card" id="pow-n-' + esc(n.id) + '"><button type="button" class="pow-node" data-id="' + esc(n.id) + '" aria-pressed="false" aria-label="' + esc(aria) + '"><span class="pow-id">' + avatar(n, "av-sm") + '<span class="pow-txt"><span class="pow-name">' + esc(n.name) + '</span><span class="pow-role">' + esc(n.role) + '</span></span></span><span class="pow-mini" aria-hidden="true">↑ ' + d.up + "  ↓ " + d.down + "</span></button>" + fortuneLine(n, false) + "</li>";
        }).join("") + "</ul></section>";
    }
    $("pow-ladder").innerHTML = html || '<p class="empty">Aucune fiche dans ce filtre.</p>';
    var shown = DATA.nodes.filter(visibleNode).length;
    var edges = DATA.edges.filter(function (e) { return edgeShown(e) && byId[e.source] && byId[e.target] && visibleNode(byId[e.source]) && visibleNode(byId[e.target]); }).length;
    var fil = longestFil();
    $("pow-stats").textContent = plural(shown, "fiche", "fiches") + " · " + plural(edges, "lien", "liens") + " · plus long fil : " + fil + (fil > 1 ? " étapes" : " étape");
    document.querySelectorAll("#pow-seg [data-pow]").forEach(function (b) {
      var f = b.getAttribute("data-pow");
      var c = DATA.nodes.filter(function (n) { return nodeInFilter(n, f); }).length;
      var lab = { tout: "Tout", gaza: "Gaza", france: "France" }[f];
      b.textContent = lab + " " + c;
      var on = f === powFilter;
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
    powBuilt = powFilter + "/" + powNature;
    markNature();
  }
  function markNature() {
    document.querySelectorAll("#pow-nat [data-nat]").forEach(function (b) {
      var on = b.getAttribute("data-nat") === powNature;
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
  }
  function linkGroup(title, items) {
    if (!items.length) return "";
    return '<h3 class="pow-h">' + esc(title) + '</h3><ul class="pow-links">' + items.map(function (it) {
      var o = byId[it.id];
      return '<li class="nat-' + edgeNature(it.e) + '"><button type="button" class="pow-link nat-' + edgeNature(it.e) + '" data-pow-go="' + esc(it.id) + '">' + avatar(o, "av-xs") +
        '<span><span class="pow-ln">' + esc(o.name) + '</span><span class="pow-lr">' + esc(it.e.relation) + "</span></span></button>" +
        '<div class="pow-lsrc">' + natureBadge(edgeNature(it.e)) + (it.e.date ? '<time datetime="' + esc(it.e.date) + '">' + fmtDate(it.e.date) + "</time> " : "") + srcLink(it.e.url, "Source") + "</div></li>";
    }).join("") + "</ul>";
  }
  function applyPowSelection(scroll) {
    var path = powSel ? climbPath(powSel) : [];
    var pathSet = {}, nearSet = {};
    path.forEach(function (id) { pathSet[id] = 1; });
    if (powSel) visNeighbors(powSel, edgeShown).forEach(function (nb) { nearSet[nb.id] = 1; });
    document.querySelectorAll("#pow-ladder .pow-node").forEach(function (b) {
      var id = b.getAttribute("data-id");
      b.classList.toggle("is-on", id === powSel);
      b.classList.toggle("is-path", !!pathSet[id] && id !== powSel);
      b.classList.toggle("is-near", !!nearSet[id] && !pathSet[id] && id !== powSel);
      b.classList.toggle("is-dim", !!powSel && id !== powSel && !pathSet[id] && !nearSet[id]);
      b.setAttribute("aria-pressed", id === powSel ? "true" : "false");
    });
    var sheet = $("pow-sheet");
    if (!powSel || !byId[powSel]) {
      sheet.hidden = true; sheet.innerHTML = "";
      document.body.classList.remove("pow-on");
      return;
    }
    var n = byId[powSel];
    var dir = uniqueDir(powSel);
    var ups = [], downs = [], same = [];
    visNeighbors(powSel, edgeShown).forEach(function (nb) {
      var d = tierIndex(nb.id) - n._pow;
      (d > 0 ? ups : d < 0 ? downs : same).push(nb);
    });
    var orderNb = function (a, b) { return tierIndex(b.id) - tierIndex(a.id) || byId[a.id].name.localeCompare(byId[b.id].name, "fr"); };
    ups.sort(orderNb); downs.sort(orderNb); same.sort(orderNb);
    var reached = path.length && tierIndex(path[path.length - 1]) === POWER_TIERS.length - 1;
    var crumb = "";
    if (path.length > 1) {
      crumb = '<ol class="pow-crumb" aria-label="Fil de liens">';
      path.forEach(function (id, i) {
        if (i) {
          var rels = edgesBetween(path[i - 1], id, isAscent);
          crumb += '<li class="pow-crumb-rel">' + esc(rels.length ? rels[0].relation : "") + (rels.length > 1 ? " · " + rels.length + " liens" : "") + "</li>";
        }
        crumb += '<li><button type="button" class="pow-crumb-b' + (id === powSel ? " is-here" : "") + '" data-pow-go="' + esc(id) + '">' + esc(byId[id].name) + "</button></li>";
      });
      crumb += "</ol>";
    }
    var climbBtn = path.length > 1 ? '<button type="button" class="btn-pill small" id="pow-climb">' + (reached ? "Remonter jusqu'au sommet" : "Remonter le fil") + "</button>" : "";
    var parcBtn = hasParcours(n) ? '<a class="btn-pill ghost small" href="' + ficheHref(n) + '#parcours">' + esc(arriveLabel(n)) + "</a>" : "";
    var modeNote = powNature === "opposition"
      ? '<p class="pow-fort-n">Ces liens documentent une opposition, une sanction ou un contrôle. Le fil « Remonter » ne les suit pas.</p>'
      : '<p class="pow-fort-n">Le fil ne suit que les liens d\'ascension : nomination, investiture, recrutement, soutien public ou financement documenté.</p>';
    var upPhrase = "Relié à " + dir.up + " acteur" + (dir.up === 1 ? "" : "s") + " plus haut";
    sheet.hidden = false;
    document.body.classList.add("pow-on");
    sheet.innerHTML = '<div class="pow-sheet-bar"><span class="grabber" aria-hidden="true"></span><button type="button" class="panel-close" id="pow-close" aria-label="Fermer"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7 7 17"/></svg></button></div>' +
      '<div class="pow-who">' + avatar(n, "av-sm") + '<div class="pow-who-t"><strong>' + esc(n.name) + "</strong><span>" + esc(n.role) + '</span><span class="pow-tier-tag">' + esc(POWER_TIERS[n._pow].label) + "</span></div></div>" +
      fortuneLine(n, true) +
      '<p class="pow-statline">' + upPhrase + (dir.down ? " · " + dir.down + " plus bas" : "") + "</p>" +
      '<div class="pow-actions">' + climbBtn + parcBtn + '<a class="btn-pill ghost small" href="' + ficheHref(n) + '">Ouvrir la fiche</a></div>' +
      modeNote +
      crumb +
      (ups.length ? linkGroup("Vers le haut", ups) : '<p class="pow-fort-n">Aucun lien documenté vers un palier supérieur.</p>') +
      linkGroup("Vers le bas", downs) +
      linkGroup("Même palier", same);
    if (scroll !== false) {
      var el = document.getElementById("pow-n-" + powSel);
      if (el) {
        var reduce = MQ_RM.matches;
        el.scrollIntoView({ block: "center", behavior: reduce ? "auto" : "smooth" });
        if (!reduce) { el.classList.remove("is-step"); void el.offsetWidth; el.classList.add("is-step"); }
      }
    }
  }
  function playClimb() {
    if (!powSel) return;
    var path = climbPath(powSel);
    if (path.length < 2) return;
    var token = ++climbToken;
    if (MQ_RM.matches) { goPower(path[path.length - 1], true); return; }
    var i = 1;
    (function step() {
      if (token !== climbToken) return;
      goPower(path[i], true);
      i++;
      if (i < path.length) setTimeout(step, 560);
    })();
  }
  function renderPouvoir(id) {
    if (!powReady) { bindPouvoir(); powReady = true; }
    var sel = id && byId[id] ? id : null;
    if (sel && !nodeInFilter(byId[sel], powFilter)) { powFilter = "tout"; powBuilt = ""; }
    powSel = sel;
    if (powBuilt !== powFilter + "/" + powNature) buildLadder();
    applyPowSelection(true);
    window.__power = function () {
      var path = powSel ? climbPath(powSel) : [];
      return {
        filter: powFilter,
        selected: powSel,
        path: path,
        nature: powNature,
        tiers: POWER_TIERS.map(function (t, i) {
          return { id: t.id, label: t.label, n: DATA.nodes.filter(function (n) { return n._pow === i; }).length };
        })
      };
    };
  }
  window.__powerTier = function (id) {
    var n = byId[id];
    return n && POWER_TIERS[n._pow] ? POWER_TIERS[n._pow].id : null;
  };
  window.__parcours = function (id) {
    var n = byId[id];
    if (!n || !n.parcours) return [];
    return n.parcours.map(function (s) {
      return { date: s.date, title: s.title, by: s.by || null, verb: s.verb || null, url: s.url };
    });
  };

  /* ---------- v24 : coulisses ---------- */
  var COU_SPHERES = [
    { id: "partis", label: "Partis", hint: "Partis, candidats et cadres nommés dans la presse." },
    { id: "medias", label: "Médias", hint: "Chaînes, radios, titres et leurs directions." },
    { id: "argent", label: "Argent", hint: "Actionnaires, fonds et financeurs nommés." },
    { id: "idees", label: "Idées", hint: "Écoles, instituts et projets documentés." },
    { id: "edition", label: "Édition", hint: "Maisons et éditrices." },
    { id: "institutions", label: "Institutions", hint: "Régulateur et contrôles publics." }
  ];
  var COU_STORIES = {
    tout: "Tout",
    argent: "Suivre l'argent",
    medias: "Suivre les médias",
    nominations: "Suivre les nominations",
    sondages: "Suivre les sondages"
  };
  var couStory = "tout", couSel = null, couStep = 0, couReady = false;

  function sphereOf(n) { return n && n.sphere; }
  function sphereMeta(id) {
    for (var i = 0; i < COU_SPHERES.length; i++) if (COU_SPHERES[i].id === id) return COU_SPHERES[i];
    return { id: id, label: id, hint: "" };
  }
  function couEdges() {
    return DATA.edges.filter(function (e) {
      var a = byId[e.source], b = byId[e.target];
      if (!a || !b || !sphereOf(a) || !sphereOf(b)) return false;
      if (couStory === "tout") return sphereOf(a) !== sphereOf(b);
      return (e.stories || []).indexOf(couStory) >= 0;
    }).sort(function (a, b) {
      var cross = function (e) {
        var x = byId[e.source], y = byId[e.target];
        return (x && y && x.sphere !== y.sphere) ? 0 : 1;
      };
      return cross(a) - cross(b) || String(a.date).localeCompare(String(b.date));
    });
  }
  function couPeople() {
    var ids = {};
    DATA.nodes.forEach(function (n) { if (sphereOf(n)) ids[n.id] = n; });
    if (couStory === "tout") return Object.keys(ids).map(function (id) { return ids[id]; });
    var keep = {};
    couEdges().forEach(function (e) { keep[e.source] = 1; keep[e.target] = 1; });
    return Object.keys(keep).map(function (id) { return byId[id]; }).filter(Boolean);
  }
  function renderCoulisses(arg) {
    if (!couReady) { bindCoulisses(); couReady = true; }
    if (arg && COU_STORIES[arg]) {
      if (couStory !== arg) couStep = 0;
      couStory = arg;
      couSel = null;
    } else if (arg && byId[arg]) couSel = arg;
    else if (!arg) { couStory = "tout"; couSel = null; couStep = 0; }
    var edges = couEdges();
    if (couStep >= edges.length) couStep = 0;
    var people = couPeople();
    var lead = "Acteurs publics rangés par sphère. Un pont n'est affiché que s'il est daté et sourcé. Rien ici ne prête une intention.";
    if (couStory === "sondages") lead += " Les ponts suivent des actionnariats et des commandes publiés. Les sondages liés au débat électoral, publiés ou diffusés, relèvent de la loi du 19 juillet 1977 et de la Commission des sondages.";
    $("cou-lead").textContent = lead;
    $("cou-stories").innerHTML = Object.keys(COU_STORIES).map(function (k) {
      return '<button type="button" class="seg-b" role="tab" data-story="' + k + '" id="cou-story-' + k + '" aria-selected="' + (couStory === k ? "true" : "false") + '">' + esc(COU_STORIES[k]) + "</button>";
    }).join("");
    $("cou-stats").textContent = plural(people.length, "acteur", "acteurs") + " · " + plural(edges.length, "pont daté", "ponts datés");
    var storyHtml = "";
    if (edges.length) {
      var e = edges[couStep], a = byId[e.source], b = byId[e.target];
      var from = sphereMeta(a.sphere).label, to = sphereMeta(b.sphere).label;
      var kicker = couStory === "tout" ? "Pont entre sphères" : COU_STORIES[couStory];
      storyHtml = '<article class="cou-now" aria-live="polite"><p class="cou-k">' + esc(kicker) + " · " + (couStep + 1) + " / " + edges.length + "</p>" +
        '<div class="cou-bridge">' + couChip(a) + '<p class="cou-rel">' + esc(e.relation) + "</p>" + couChip(b) + "</div>" +
        '<div class="meta">' + natureBadge(edgeNature(e)) +
        '<span class="cou-sp">' + esc(from === to ? from : from + " → " + to) + "</span>" +
        (e.date ? '<time datetime="' + esc(e.date) + '">' + fmtDate(e.date) + "</time>" : "") +
        srcLink(e.url, "Source") + "</div>" +
        '<div class="cou-nav"><button type="button" class="btn-pill ghost small" id="cou-prev">Précédent</button><button type="button" class="btn-pill small" id="cou-next">Suivant</button></div></article>';
    } else if (couStory !== "tout") {
      storyHtml = '<p class="empty">Aucun pont de ce récit dans les sources retenues.</p>';
    }
    $("cou-story").innerHTML = storyHtml;
    var byS = {};
    people.forEach(function (n) { (byS[n.sphere] || (byS[n.sphere] = [])).push(n); });
    $("cou-spheres").innerHTML = COU_SPHERES.filter(function (s) { return byS[s.id] && byS[s.id].length; }).map(function (s) {
      var list = byS[s.id].slice().sort(function (a, b) { return a.name.localeCompare(b.name, "fr"); });
      return '<section class="cou-lane" id="cou-lane-' + s.id + '"><h2 class="h-sec">' + esc(s.label) + ' <span class="h-n">' + list.length + "</span></h2><p class=\"cou-hint\">" + esc(s.hint) + "</p><ul class=\"cou-people\">" +
        list.map(function (n) {
          return '<li><button type="button" class="cou-person' + (couSel === n.id ? " is-on" : "") + '" data-cou="' + esc(n.id) + '">' + avatar(n, "av-sm") + "<span><strong>" + esc(n.name) + "</strong><em>" + esc(n.role) + "</em></span></button></li>";
        }).join("") + "</ul></section>";
    }).join("");
    renderCouSheet(edges);
    window.__coulisses = function () {
      return { story: couStory, selected: couSel, step: couStep, bridges: couEdges().length, people: couPeople().length };
    };
  }
  function couChip(n) {
    return '<button type="button" class="cou-end" data-cou="' + esc(n.id) + '">' + avatar(n, "av-sm") + "<span><strong>" + esc(n.name) + "</strong><em>" + esc(sphereMeta(n.sphere).label) + "</em></span></button>";
  }
  function renderCouSheet() {
    var sheet = $("cou-sheet");
    if (!couSel || !byId[couSel]) { sheet.hidden = true; document.body.classList.remove("cou-on"); return; }
    var n = byId[couSel];
    var groups = { coulisses: [], ascension: [], opposition: [], autre: [] };
    (edgesOf[n.id] || []).forEach(function (e) {
      var nat = edgeNature(e);
      (groups[nat] || groups.autre).push(e);
    });
    function group(title, list) {
      if (!list.length) return "";
      return "<h3 class=\"cou-h\">" + esc(title) + "</h3><ul class=\"cou-links\">" + list.map(function (e) {
        var other = byId[e.source === n.id ? e.target : e.source];
        return '<li><button type="button" class="cou-link" data-cou="' + esc(other.id) + '">' + avatar(other, "av-xs") + "<span><strong>" + esc(other.name) + "</strong><em>" + esc(e.relation) + "</em></span></button>" +
          '<div class="meta">' + natureBadge(edgeNature(e)) + (e.date ? '<time datetime="' + esc(e.date) + '">' + fmtDate(e.date) + "</time>" : "") + srcLink(e.url, "Source") + "</div></li>";
      }).join("") + "</ul>";
    }
    var parc = hasParcours(n) ? '<a class="btn-pill ghost small" href="' + ficheHref(n) + '#parcours">' + esc(arriveLabel(n)) + "</a>" : "";
    sheet.hidden = false;
    document.body.classList.add("cou-on");
    sheet.innerHTML = '<div class="cou-sheet-bar"><span class="grabber" aria-hidden="true"></span><button type="button" class="panel-close" id="cou-close" aria-label="Fermer"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7 7 17"/></svg></button></div>' +
      '<div class="cou-who">' + avatar(n, "av-sm") + '<div><strong>' + esc(n.name) + "</strong><span>" + esc(n.role) + "</span><span class=\"cou-tag\">" + esc(sphereMeta(n.sphere).label) + "</span></div></div>" +
      '<div class="cou-actions"><a class="btn-pill small" href="' + ficheHref(n) + '">Ouvrir la fiche</a>' + parc + "</div>" +
      group("Coulisses", groups.coulisses) + group("Ascension", groups.ascension) + group("Opposition", groups.opposition) + group("Autre", groups.autre);
    $("cou-close").addEventListener("click", function () {
      couSel = null; sheet.hidden = true; document.body.classList.remove("cou-on");
      if (location.hash.indexOf("#/coulisses/") === 0) history.replaceState(null, "", "#/coulisses" + (couStory !== "tout" ? "/" + couStory : ""));
    });
  }
  function bindCoulisses() {
    $("view-coulisses").addEventListener("click", function (ev) {
      var story = ev.target.closest("[data-story]");
      if (story) {
        ev.preventDefault();
        location.hash = "#/coulisses/" + story.getAttribute("data-story");
        return;
      }
      var who = ev.target.closest("[data-cou]");
      if (who) {
        ev.preventDefault();
        location.hash = "#/coulisses/" + encodeURIComponent(who.getAttribute("data-cou"));
        return;
      }
      if (ev.target.closest("#cou-prev")) {
        var n = couEdges().length;
        couStep = (couStep - 1 + n) % n;
        renderCoulisses(couStory);
      } else if (ev.target.closest("#cou-next")) {
        var m = couEdges().length;
        couStep = (couStep + 1) % m;
        renderCoulisses(couStory);
      }
    });
  }

  /* ---------- Routage par ancre (#/…) ---------- */
  var VIEWS = ["accueil", "sections", "fiche", "chronologie", "reseau", "pouvoir", "coulisses", "methodologie", "methode", "contribuer", "credits"];
  var TITLES = { accueil: "Onrecord — Leurs mots, datés et sourcés", sections: "Sections", chronologie: "Chronologie", reseau: "Réseau des relations", pouvoir: "Échelle du pouvoir", coulisses: "Coulisses", methodologie: "Méthodologie", methode: "Méthode", contribuer: "Proposer une mise à jour", credits: "Crédits photos" };
  function renderCredits() {
    var rows = DATA.nodes.filter(function (n) { return n.image || n.logo; }).slice().sort(function (a, b) { return a.name.localeCompare(b.name, "fr"); });
    $("credits-count").textContent = rows.length + (rows.length > 1 ? " images" : " image");
    $("credits-list").innerHTML = rows.map(function (n) {
      var photo = !!n.image, url = photo ? n.image : n.logo, cr = (photo ? n.image_credit : n.logo_credit) || {};
      var lic = cr.license ? (cr.license_url ? '<a href="' + esc(cr.license_url) + '" target="_blank" rel="noopener noreferrer license">' + esc(cr.license) + "</a>" : esc(cr.license)) : "—";
      var src = cr.source_url ? '<a href="' + esc(cr.source_url) + '" target="_blank" rel="noopener noreferrer">page du fichier</a>' : "—";
      return '<li class="cred"><img src="' + esc(url) + '" alt="" width="72" height="72"><div><a href="' + ficheHref(n) + '"><strong>' + esc(n.name) + "</strong></a><span>" + (photo ? "Photo" : "Logo") + " · " + esc(cr.author || "auteur non précisé") + "</span><span>" + lic + " · " + src + "</span></div></li>";
    }).join("");
  }
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
    var tab = v === "fiche" ? "sections" : (v === "methode" || v === "contribuer" || v === "credits") ? "methodologie" : v;
    document.querySelectorAll("#tabnav a").forEach(function (a) {
      if (a.getAttribute("data-tab") === tab) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    document.body.setAttribute("data-view", v);
    if (v !== "reseau") {
      if (!$("panel").hidden) closePanel();
      document.body.classList.remove("sheet-open", "panel-open");
      if (fsMode) exitFullscreen();
    }
    if (v !== "pouvoir") {
      document.body.classList.remove("pow-on");
      if ($("pow-sheet")) $("pow-sheet").hidden = true;
    }
    if (v !== "coulisses") {
      document.body.classList.remove("cou-on");
      if ($("cou-sheet")) $("cou-sheet").hidden = true;
    }
    if (v !== "fiche") document.title = v === "accueil" ? TITLES.accueil : TITLES[v] + " — Onrecord";
    if (v === "sections") { curSec = ["tout", "gaza", "france", "commun"].indexOf(parts[1]) >= 0 ? parts[1] : "tout"; renderSections(); }
    if (v === "methode") renderMethode();
    if (v === "credits") renderCredits();
    if (v === "accueil") { renderResume(); renderQotd(); }
    if (v === "fiche") renderFiche(decodeURIComponent(parts[1] || ""), anchor);
    var key = v + "/" + ((v === "fiche" || v === "pouvoir") ? (parts[1] || "") : "");
    var stay = (v === "reseau" && lastView && lastView.indexOf("reseau") === 0) || (v === "pouvoir" && lastView && lastView.indexOf("pouvoir") === 0) || (v === "coulisses" && lastView && lastView.indexOf("coulisses") === 0);
    if (key !== lastView && !stay) window.scrollTo(0, 0);
    lastView = key;
    if (v === "reseau") requestAnimationFrame(function () { ensureGraph(parts[1] ? decodeURIComponent(parts[1]) : null); });
    if (v === "pouvoir") renderPouvoir(parts[1] ? decodeURIComponent(parts[1]) : null);
    if (v === "coulisses") renderCoulisses(parts[1] ? decodeURIComponent(parts[1]) : "");
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
