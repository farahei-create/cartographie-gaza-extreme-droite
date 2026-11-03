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
    bindDonation();
    bindVideos();
    buildFilters();
    buildGraph();
    buildList();
    document.querySelector(".seg-thumb").style.transition = "none";
    bindTabs();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(moveThumb);
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
    if (!shell || !gl || $("view-graphe").hidden || shell.classList.contains("is-fs")) return;
    var mobile = MQ_MOBILE.matches;
    var ref = mobile ? gl : shell;
    var top = ref.getBoundingClientRect().top + window.scrollY;
    var bottomPad = mobile ? 12 : 16;
    var h = Math.max(mobile ? 360 : 480, window.innerHeight - top - bottomPad - (mobile ? 0 : 6));
    shell.style.setProperty("--graph-h", Math.round(h) + "px");
  }
  window.addEventListener("resize", function () { sizeGraph(); moveThumb(); });

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
        '<div class="meta">' + srcLink(s.url, "Lire la source") + "</div>" + videoHtml(s.video) + "</li>";
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
      return '<li class="rel">' + sentence + '<div class="meta">' + (e.date ? fmtDate(e.date) + " · " : "") + srcLink(e.url) + "</div></li>";
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
        '<td data-label="Personne">' + mediaHtml(n, "l-media") + '<p class="name" id="p-' + esc(n.id) + '">' + esc(n.name) + '</p><p class="role">' + esc(n.role) + "</p>" +
        '<div class="secs">' + sectionTags(n) + "</div>" +
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
      var q = norm($("list-search").value).trim(), th = sel.value, sec = $("list-section").value, shown = 0;
      body.querySelectorAll("tr").forEach(function (tr) {
        var n = byId[tr.getAttribute("data-id")];
        var okTheme = !th || (n.statements || []).some(function (s) { return s.theme === th; });
        var okSec = !sec || (n.sections || []).indexOf(sec) >= 0;
        var ok = okTheme && okSec && (!q || texts[n.id].indexOf(q) >= 0);
        tr.hidden = !ok;
        if (ok) { shown++; tr.querySelector(".st-cell").innerHTML = statementsHtml(n, th); }
      });
      $("list-count").textContent = shown + " personne" + (shown > 1 ? "s" : "") + " affichée" + (shown > 1 ? "s" : "") + " sur " + people.length + ".";
    }
    $("list-search").addEventListener("input", render);
    sel.addEventListener("change", render);
    $("list-section").addEventListener("change", render);
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
      moveThumb();
      if (tab !== "graphe") { document.body.classList.remove("sheet-open"); if (fsMode) exitFullscreen(); }
      else if (!$("panel").hidden) { document.body.classList.toggle("sheet-open", MQ_MOBILE.matches); }
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
    requestAnimationFrame(function () { document.querySelector(".seg-thumb").style.transition = ""; });

    /* Filtres repliables (mobile) */
    var ft = $("filters-toggle"), fl = $("filters");
    ft.addEventListener("click", function () {
      var open = ft.getAttribute("aria-expanded") !== "true";
      ft.setAttribute("aria-expanded", open ? "true" : "false");
      fl.classList.toggle("open", open);
      sizeGraph();
    });
    fl.addEventListener("transitionend", function (e) { if (e.target === fl) { sizeGraph(); } });

    /* Barre d'onglets : filet discret une fois collée en haut */
    var tb = document.querySelector(".tabbar");
    var onScroll = function () { tb.classList.toggle("stuck", tb.getBoundingClientRect().top <= 0 && window.scrollY > 4); };
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
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

  /* Contrôle segmenté : pastille glissante sous l'onglet actif */
  function moveThumb() {
    var th = document.querySelector(".seg-thumb"), sel = document.querySelector('.tabs a[aria-selected="true"]');
    if (!th || !sel) return;
    th.style.width = sel.offsetWidth + "px";
    th.style.transform = "translateX(" + sel.offsetLeft + "px)";
  }
})();
