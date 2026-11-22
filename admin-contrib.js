/* Admin : modération des contributions des lecteurs.
   Le jeton GitHub déjà collé sur cette page (onrecord:admin-token) est envoyé à
   /api/contrib/admin, qui vérifie côté serveur qu'il ouvre le dépôt en écriture.
   Publier écrit contributions.json sur main (Vercel redéploie en une minute environ). */
(function () {
  "use strict";
  var TOKEN_KEY = "onrecord:admin-token";
  var names = {};
  function $(id) { return document.getElementById(id); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function when(iso) {
    try { return new Intl.DateTimeFormat("fr-FR", { timeZone: "Europe/Paris", dateStyle: "medium", timeStyle: "short" }).format(new Date(iso)) + " (Paris)"; } catch (e) { return iso; }
  }
  function token() { try { return localStorage.getItem(TOKEN_KEY) || ""; } catch (e) { return ""; } }
  function call(op, extra) {
    var body = Object.assign({ op: op }, extra || {});
    return fetch("/api/contrib/admin", {
      method: "POST", cache: "no-store",
      headers: { "Content-Type": "application/json", Authorization: "Bearer " + token() },
      body: JSON.stringify(body)
    }).then(function (r) { return r.json().catch(function () { return {}; }).then(function (b) { return { ok: r.ok, status: r.status, body: b }; }); },
      function () { return { ok: false, status: 0, body: { error: "Pas de connexion." } }; });
  }
  function media(list) {
    return (list || []).map(function (m) {
      return m.kind === "video" ? '<video controls preload="metadata" playsinline src="' + esc(m.url) + '" style="width:100%;max-height:260px"></video>'
        : '<a href="' + esc(m.url) + '" target="_blank" rel="noopener"><img src="' + esc(m.url) + '" alt="" style="max-width:100%;max-height:220px;border-radius:10px"></a>';
    }).join("");
  }
  function links(list) {
    return (list || []).length ? "<ul>" + list.map(function (u) { return '<li><a href="' + esc(u) + '" target="_blank" rel="noopener noreferrer">' + esc(u) + "</a></li>"; }).join("") + "</ul>" : "";
  }
  function flags(f) {
    f = f || {};
    var out = [];
    if ((f.forbidden || []).length) out.push("Mots interdits : " + f.forbidden.join(", "));
    if ((f.private || []).length) out.push("À vérifier, donnée privée possible : " + f.private.join(", "));
    return out.length ? '<p class="err">' + esc(out.join(" · ")) + "</p>" : "";
  }
  function who(id) { return names[id] ? esc(names[id]) + " <small>(" + esc(id) + ")</small>" : esc(id); }

  function render(b) {
    var box = $("ctb-admin-list"), st = b.status || {};
    var miss = [];
    if (!st.storage) miss.push("Vercel Blob (BLOB_READ_WRITE_TOKEN)");
    if (!st.session) miss.push("SESSION_SECRET");
    if (!st.mail) miss.push("RESEND_API_KEY ou BREVO_API_KEY");
    if (st.mail && !st.from_set) miss.push("MAIL_FROM");
    var html = miss.length ? '<p class="err">Pas encore ouvert au public. Manque dans Vercel : ' + esc(miss.join(", ")) + ". Le mode d'emploi est dans docs/REPRISE.md, section 14.</p>"
      : '<p class="hint">Ouvert au public. Rien ne paraît sans « Publier ».</p>';
    html += "<h3>En attente (" + (b.pending || []).length + ")</h3>";
    html += (b.pending || []).map(function (p) {
      return '<div class="pv"><p class="k">' + who(p.person) + "</p><h3>" + esc(p.title) + "</h3>" +
        "<p class=\"hint\">Par <strong>" + esc(p.pseudo) + "</strong> · " + esc(p.email || "e-mail illisible") + " · déposé le " + esc(when(p.submitted)) + (p.event_date ? " · faits du " + esc(p.event_date) : "") + "</p>" +
        flags(p.flags) + "<blockquote>" + esc(p.text).replace(/\n/g, "<br>") + "</blockquote>" + links(p.links) + media(p.media) +
        '<p><button type="button" data-op="approve" data-id="' + esc(p.id) + '">Publier</button> <button type="button" data-op="reject" data-id="' + esc(p.id) + '">Refuser et effacer</button></p></div>';
    }).join("") || '<p class="hint">Rien en attente.</p>';
    html += "<h3>Signalements (" + (b.reports || []).length + ")</h3>";
    html += (b.reports || []).map(function (r) {
      return '<div class="pv"><p class="k">' + esc(r.kind) + " · " + esc(when(r.at)) + "</p><p>" + esc(r.reason) + "</p>" +
        (r.contact ? '<p class="hint">Contact : ' + esc(r.contact) + "</p>" : "") + '<p class="hint">Contribution <code>' + esc(r.id) + "</code></p>" +
        '<p><button type="button" data-op="unpublish" data-id="' + esc(r.id) + '">Retirer la contribution</button> <button type="button" data-op="dismiss" data-rid="' + esc(r.rid) + '">Classer</button></p></div>';
    }).join("") || '<p class="hint">Aucun signalement.</p>';
    html += "<h3>Publiées (" + (b.published || []).length + ")</h3>";
    html += (b.published || []).map(function (p) {
      return '<div class="pv"><p class="k">' + who(p.person) + "</p><h3>" + esc(p.title) + '</h3><p class="hint">' + esc(p.pseudo) + " · " + esc(when(p.submitted)) + " · <code>" + esc(p.id) + "</code></p>" +
        '<p><button type="button" data-op="unpublish" data-id="' + esc(p.id) + '">Retirer</button></p></div>';
    }).join("") || '<p class="hint">Aucune contribution publiée.</p>';
    box.innerHTML = html;
  }
  function load() {
    var box = $("ctb-admin-list"), msg = $("ctb-admin-status");
    if (!token()) { box.innerHTML = '<p class="hint">Enregistre d\'abord le jeton GitHub plus bas sur cette page, puis appuie sur « Actualiser ».</p>'; return; }
    msg.textContent = "Chargement…";
    call("list").then(function (r) {
      msg.textContent = "";
      if (r.status === 404 || (r.status === 0)) { box.innerHTML = '<p class="err">Les fonctions /api ne répondent pas encore.</p>'; return; }
      if (!r.ok) { box.innerHTML = '<p class="err">' + esc(r.body.error || ("Erreur " + r.status)) + "</p>"; return; }
      render(r.body);
    });
  }
  var LABEL = { approve: "Publier cette contribution ?", reject: "Refuser et effacer définitivement (fichiers compris) ?", unpublish: "Retirer cette contribution du site (fichiers effacés) ?", dismiss: "Classer ce signalement ?" };
  document.addEventListener("click", function (ev) {
    var b = ev.target.closest && ev.target.closest("#ctb-admin-list button[data-op]");
    if (!b) return;
    var op = b.getAttribute("data-op");
    if (!window.confirm(LABEL[op])) return;
    b.disabled = true;
    call(op, { id: b.getAttribute("data-id"), rid: b.getAttribute("data-rid") }).then(function (r) {
      $("ctb-admin-status").textContent = r.ok ? (op === "approve" || op === "unpublish" ? "Fait. Le site se met à jour dans une minute environ." : "Fait.") : (r.body.error || "Erreur " + r.status);
      load();
    });
  });
  function boot() {
    if (!$("ctb-admin")) return;
    $("ctb-admin-refresh").addEventListener("click", load);
    fetch("data.json", { cache: "no-cache" }).then(function (r) { return r.json(); }).then(function (d) {
      (d.nodes || []).forEach(function (n) { names[n.id] = n.name; });
    }).catch(function () {}).then(load);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
