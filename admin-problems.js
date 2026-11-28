/* Admin : catégorie « Problèmes ». Lit incidents.json (écrit par le relevé automatique)
   et les derniers passages du workflow (API GitHub publique, sans jeton).
   « Marquer comme réglé » réécrit incidents.json sur main avec le jeton déjà enregistré
   sur cette page (onrecord:admin-token), via api.github.com seulement. */
(function () {
  "use strict";
  var OWNER = "farahei-create", REPO = "cartographie-gaza-extreme-droite", FILE = "incidents.json";
  var TOKEN_KEY = "onrecord:admin-token";
  var KIND = {
    workflow: "Relevé en panne", ia_quota: "IA : quota", ia_cle: "IA : clé", ia_panne: "IA : relecture",
    personne_sans_fiche: "Personne sans fiche", build_refus: "Phrase écartée", resume: "Résumé du jour"
  };
  function $(id) { return document.getElementById(id); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function when(iso) {
    try { return new Intl.DateTimeFormat("fr-FR", { timeZone: "Europe/Paris", dateStyle: "medium", timeStyle: "short" }).format(new Date(iso)) + " (Paris)"; } catch (e) { return iso || ""; }
  }
  function token() { try { return localStorage.getItem(TOKEN_KEY) || ""; } catch (e) { return ""; } }
  function linkify(text) {
    return esc(text).replace(/https:\/\/[^\s<]+/g, function (u) { return '<a href="' + u + '" target="_blank" rel="noopener noreferrer">' + (u.indexOf("/actions/runs/") > 0 ? "voir le détail" : u) + "</a>"; });
  }
  var items = [];
  function paint() {
    var open = items.filter(function (i) { return !i.resolved; });
    var done = items.filter(function (i) { return i.resolved; });
    var badge = $("n-problemes");
    if (badge) badge.textContent = open.length || "";
    var card = function (i) {
      return '<article class="pv" data-id="' + esc(i.id) + '"><p class="k">' + esc(KIND[i.kind] || "Problème") + " · " + esc(when(i.at)) +
        (i.count > 1 ? " · " + esc(i.count) + " fois" : "") + "</p><h3>" + esc(i.title) + "</h3>" +
        (i.detail ? '<p class="hint">' + linkify(i.detail) + "</p>" : "") +
        (i.resolved ? '<p class="hint">Réglé' + (i.resolved_at ? " le " + esc(when(i.resolved_at)) : "") + ".</p>"
          : '<p><button type="button" data-resolve="' + esc(i.id) + '">Marquer comme réglé</button></p>') + "</article>";
    };
    var html = open.length ? open.map(card).join("") : '<p class="hint">Aucun problème en cours. 🎉</p>';
    if (open.length > 1) html = '<p><button type="button" class="btn ghost" data-resolve="*">Tout marquer comme réglé</button></p>' + html;
    if (done.length) html += '<details class="sec"><summary>Déjà réglés (' + done.length + ")</summary>" + done.slice(0, 40).map(card).join("") + "</details>";
    $("pb-list").innerHTML = html;
  }
  function load() {
    fetch(FILE, { cache: "no-store" }).then(function (r) { return r.ok ? r.json() : { items: [] }; }).then(function (d) {
      items = (d && d.items) || [];
      paint();
    }).catch(function () { $("pb-list").textContent = "Journal des problèmes illisible."; });
  }
  function runs() {
    var box = $("pb-runs");
    fetch("https://api.github.com/repos/" + OWNER + "/" + REPO + "/actions/workflows/daily-update.yml/runs?per_page=6", { cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        var list = (d.workflow_runs || []);
        if (!list.length) { box.textContent = "Aucun passage récent."; return; }
        box.innerHTML = "<ul>" + list.map(function (r) {
          var st = r.status !== "completed" ? "en cours" : (r.conclusion === "success" ? "✅ réussi" : (r.conclusion === "cancelled" ? "annulé" : "❌ échec"));
          var how = r.event === "schedule" ? "secours GitHub" : (r.event === "workflow_dispatch" ? "lancé à l'heure" : r.event);
          return '<li>' + esc(when(r.run_started_at || r.created_at)) + " — " + st + ' <small>(' + esc(how) + ')</small> <a href="' + esc(r.html_url) + '" target="_blank" rel="noopener noreferrer">détail</a></li>';
        }).join("") + "</ul>";
      }).catch(function () { box.textContent = "GitHub n'a pas répondu. Réessaie plus tard."; });
  }
  function b64(str) { return btoa(unescape(encodeURIComponent(str))); }
  function unb64(str) { return decodeURIComponent(escape(atob(String(str).replace(/\s/g, "")))); }
  function gh(method, path, body) {
    return fetch("https://api.github.com" + path, {
      method: method, cache: "no-store",
      headers: { Accept: "application/vnd.github+json", Authorization: "Bearer " + token(), "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined
    }).then(function (r) { return r.json().catch(function () { return {}; }).then(function (b) { return { status: r.status, body: b }; }); });
  }
  function resolve(id) {
    var msg = $("pb-status");
    if (!token()) { msg.textContent = "Enregistre d'abord ton jeton GitHub dans la catégorie Ajouter."; return; }
    msg.textContent = "Enregistrement…";
    var path = "/repos/" + OWNER + "/" + REPO + "/contents/" + FILE;
    gh("GET", path + "?ref=main").then(function (r) {
      if (r.status === 401) throw new Error("Jeton refusé. Il est invalide ou expiré.");
      if (r.status !== 200) throw new Error("Lecture impossible (" + r.status + ").");
      var data = JSON.parse(unb64(r.body.content));
      var stamp = new Date().toISOString().replace(/\.\d+Z$/, "Z");
      (data.items || []).forEach(function (i) { if (!i.resolved && (id === "*" || i.id === id)) { i.resolved = true; i.resolved_at = stamp; } });
      return gh("PUT", path, {
        message: "Journal des problèmes : marqué comme réglé depuis l'admin",
        content: b64(JSON.stringify(data, null, 2) + "\n"), sha: r.body.sha, branch: "main"
      }).then(function (w) {
        if (w.status !== 200 && w.status !== 201) throw new Error("Écriture refusée (" + w.status + ").");
        items = data.items || [];
        paint();
        msg.textContent = "C'est noté. Le site se met à jour dans une minute environ.";
      });
    }).catch(function (e) { msg.textContent = e.message || "Échec."; });
  }
  function boot() {
    if (!$("pb-list")) return;
    load();
    runs();
    $("pb-refresh").addEventListener("click", function () { load(); runs(); });
    $("pb-list").addEventListener("click", function (ev) {
      var b = ev.target.closest && ev.target.closest("button[data-resolve]");
      if (!b) return;
      var id = b.getAttribute("data-resolve");
      if (id === "*" && !window.confirm("Marquer tous les problèmes comme réglés ?")) return;
      b.disabled = true;
      resolve(id);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
