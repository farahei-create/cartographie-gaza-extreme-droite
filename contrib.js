/* Contributions des lecteurs (vue #/contributions et bloc des fiches).
   Inscription par code e-mail, dépôt avec preuves, signalement. Rien n'est publié
   sans validation dans /admin.html. Serveur : api/contrib/[action].js. */
(function () {
  "use strict";
  var C = window.OnrecordContrib = {};
  var ctx = { nodes: [], byId: {} };
  var REPORT_KINDS = [["faux", "Information fausse ou trompeuse"], ["prive", "Donnée privée sur une personne"], ["injure", "Injure, harcèlement"], ["illicite", "Contenu illicite"], ["autre", "Autre"]];
  var IMAGE_MAX = 5 * 1024 * 1024, VIDEO_MAX = 50 * 1024 * 1024;
  var IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"], VIDEO_TYPES = ["video/mp4", "video/webm", "video/quicktime"];
  var BANNER = "Contenu publié par un contributeur, sous sa seule responsabilité. Onrecord ne l'a pas vérifié comme ses propres sources.";

  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; });
  }
  function toast(m) { if (ctx.toast) ctx.toast(m); }
  var FMT = null;
  function fmtWhen(iso) {
    var d = new Date(iso);
    if (isNaN(d)) return "";
    try {
      FMT = FMT || new Intl.DateTimeFormat("fr-FR", { timeZone: "Europe/Paris", day: "numeric", month: "long", year: "numeric", hour: "2-digit", minute: "2-digit" });
      return FMT.format(d).replace(/\s(\d{2}):(\d{2})$/, "\u00a0$1\u00a0h\u00a0$2");
    } catch (e) { return d.toISOString().slice(0, 16).replace("T", " "); }
  }
  function fmtDay(s) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || "");
    if (!m) return "";
    var M = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];
    return (+m[3] === 1 ? "1er" : +m[3]) + " " + M[+m[2] - 1] + " " + m[1];
  }
  function host(u) { try { return new URL(u).hostname.replace(/^www\./, ""); } catch (e) { return u; } }

  function api(action, body) {
    var opt = body === undefined ? { credentials: "same-origin", cache: "no-store" } :
      { method: "POST", credentials: "same-origin", cache: "no-store", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
    return fetch("/api/contrib/" + action, opt).then(function (r) {
      /* pas de JSON : les fonctions /api ne sont pas déployées, on dit « bientôt » */
      return r.json().catch(function () { return { soon: true }; }).then(function (b) { return { ok: r.ok, status: r.status, body: b || {} }; });
    }, function () { return { ok: false, status: 0, body: { error: "Pas de connexion. Réessaie." } }; });
  }
  var statusP = null;
  function status(force) {
    if (!statusP || force) statusP = api("status").then(function (r) { return r.ok ? r.body : { enabled: false, reports: false }; });
    return statusP;
  }
  var pubP = null;
  function published() {
    if (!pubP) pubP = fetch("contributions.json", { cache: "no-cache" }).then(function (r) { return r.ok ? r.json() : { items: [] }; })
      .catch(function () { return { items: [] }; }).then(function (d) { return Array.isArray(d.items) ? d.items : []; });
    return pubP;
  }

  C.init = function (o) {
    ctx = o || ctx;
    ctx.byId = {};
    (ctx.nodes || []).forEach(function (n) { ctx.byId[n.id] = n; });
    bindView();
  };

  /* ---------- bloc d'une fiche ---------- */
  function itemHtml(it, withWho) {
    var n = ctx.byId[it.person];
    var media = (it.media || []).map(function (m) {
      return m.kind === "video"
        ? '<video class="ctb-video" controls playsinline preload="metadata" src="' + esc(m.url) + '"></video>'
        : '<a class="ctb-img" href="' + esc(m.url) + '" target="_blank" rel="noopener"><img loading="lazy" src="' + esc(m.url) + '" alt="Pièce jointe déposée par ' + esc(it.pseudo) + '"></a>';
    }).join("");
    var links = (it.links || []).map(function (u) {
      return '<li><a href="' + esc(u) + '" target="_blank" rel="nofollow ugc noopener noreferrer">' + esc(host(u)) + "</a></li>";
    }).join("");
    return '<article class="ctb-item" id="ctb-' + esc(it.id) + '">' +
      '<p class="ctb-banner" role="note"><span>' + esc(BANNER) + '</span> <button type="button" class="ctb-report-btn" data-id="' + esc(it.id) + '">Signaler un contenu</button></p>' +
      (withWho && n ? '<p class="ctb-who"><a href="#/' + (n.type === "person" ? "personne" : "organisation") + "/" + encodeURIComponent(n.id) + '">' + esc(n.name) + "</a></p>" : "") +
      '<h3 class="ctb-title">' + esc(it.title) + "</h3>" +
      '<p class="ctb-meta">Par <strong>' + esc(it.pseudo) + "</strong> · posté le <time datetime=\"" + esc(it.submitted) + '">' + esc(fmtWhen(it.submitted)) + "</time> (heure de Paris)" +
      (it.event_date ? " · faits du " + esc(fmtDay(it.event_date)) : "") + "</p>" +
      '<div class="ctb-text">' + esc(it.text).replace(/\n/g, "<br>") + "</div>" +
      (media ? '<div class="ctb-media">' + media + "</div>" : "") +
      (links ? '<p class="ctb-k">Liens donnés par l\'auteur</p><ul class="ctb-links">' + links + "</ul>" : "") +
      '<div class="ctb-report" hidden></div></article>';
  }
  C.fiche = function (n, el) {
    if (!el) return;
    el.innerHTML = '<h2 class="h-sec">Contributions des lecteurs <span class="h-n">…</span></h2>';
    published().then(function (items) {
      if (!el.isConnected) return;
      var mine = items.filter(function (i) { return i.person === n.id; });
      el.innerHTML = '<h2 class="h-sec" id="contributions">Contributions des lecteurs <span class="h-n">' + mine.length + "</span></h2>" +
        '<p class="ctb-intro">Hors archive. Ce ne sont pas des sources vérifiées par Onrecord : des lecteurs inscrits les déposent, la modération les relit avant publication, chacun en reste responsable.</p>' +
        (mine.length ? mine.map(function (i) { return itemHtml(i, false); }).join("") : '<p class="empty">Aucune contribution publiée pour cette fiche.</p>') +
        '<p class="ctb-actions"><a class="btn-pill small" href="#/contributions/' + encodeURIComponent(n.id) + '">Ajouter une contribution</a>' +
        '<a class="btn-pill ghost small" href="#/contributions">Charte et retrait</a></p>';
    });
  };

  /* ---------- signalement ---------- */
  document.addEventListener("click", function (ev) {
    var b = ev.target.closest && ev.target.closest(".ctb-report-btn");
    if (!b) return;
    var box = b.closest(".ctb-item").querySelector(".ctb-report");
    if (!box.hidden) { box.hidden = true; return; }
    var id = b.getAttribute("data-id");
    box.innerHTML = '<form class="ctb-form" novalidate><p class="ctb-k">Signaler ce contenu</p>' +
      '<label>Motif <select name="kind">' + REPORT_KINDS.map(function (k) { return '<option value="' + k[0] + '">' + esc(k[1]) + "</option>"; }).join("") + "</select></label>" +
      '<label>Ce qui pose problème <textarea name="reason" rows="3" required minlength="5" maxlength="2000"></textarea></label>' +
      '<label>Ton e-mail (facultatif, pour une réponse) <input name="contact" type="email" autocomplete="email"></label>' +
      '<p class="ctb-err" role="alert" hidden></p><p><button type="submit" class="btn-pill small">Envoyer le signalement</button></p></form>';
    box.hidden = false;
    box.querySelector("form").addEventListener("submit", function (e) {
      e.preventDefault();
      var f = e.target, err = f.querySelector(".ctb-err"), btn = f.querySelector("button");
      btn.disabled = true;
      api("report", { id: id, kind: f.kind.value, reason: f.reason.value, contact: f.contact.value }).then(function (r) {
        btn.disabled = false;
        if (r.ok) { box.innerHTML = '<p class="ctb-ok">Merci. Le signalement est transmis à la modération.</p>'; return; }
        err.textContent = r.body.soon ? "Le signalement en ligne arrive bientôt. En attendant, passe par la page « Proposer une mise à jour » (demande de retrait)." : (r.body.error || "Envoi impossible.");
        err.hidden = false;
      });
    });
  });

  /* ---------- vue #/contributions ---------- */
  var CH_KEY = "onrecord:ctb-challenge";
  var bound = false;
  function bindView() {
    if (bound || !$("ctb-app")) return;
    bound = true;
  }
  C.view = function (personId) {
    var app = $("ctb-app");
    if (!app) return;
    app.innerHTML = '<p class="ctb-k">Chargement…</p>';
    Promise.all([status(true), api("me"), published()]).then(function (r) {
      var st = r[0], me = r[1].ok ? r[1].body : { logged: false }, items = r[2];
      var latest = items.slice(0, 5);
      var recent = latest.length ? '<h2 class="h-sec">Dernières contributions publiées</h2>' + latest.map(function (i) { return itemHtml(i, true); }).join("") : "";
      if (!st.enabled) {
        app.innerHTML = '<div class="ctb-soon card"><p class="ctb-k">Bientôt disponible</p><p>Le dépôt de contributions ouvre bientôt. L\'inscription sera gratuite.</p></div>' + recent;
        return;
      }
      if (!me.logged) { renderLogin(app, personId); app.insertAdjacentHTML("beforeend", recent); return; }
      renderForm(app, me.pseudo, personId);
      app.insertAdjacentHTML("beforeend", recent);
    });
  };

  function renderLogin(app, personId) {
    var ch = null;
    try { ch = JSON.parse(sessionStorage.getItem(CH_KEY) || "null"); } catch (e) {}
    if (ch && ch.until > Date.now()) return renderCode(app, ch, personId);
    app.innerHTML = '<form class="ctb-form card" id="ctb-login" novalidate><p class="ctb-k">1. Inscription gratuite</p>' +
      '<p>Ton adresse e-mail reste privée : elle n\'est jamais affichée. Les adresses jetables sont refusées.</p>' +
      '<label>E-mail <input name="email" type="email" autocomplete="email" inputmode="email" required></label>' +
      '<label class="ctb-check"><input name="charter" type="checkbox"> <span>J\'ai lu et j\'accepte la charte ci-dessous. Je publie sous ma seule responsabilité.</span></label>' +
      '<p class="ctb-err" role="alert" hidden></p><p><button type="submit" class="btn-pill">Recevoir un code</button></p></form>';
    $("ctb-login").addEventListener("submit", function (e) {
      e.preventDefault();
      var f = e.target, err = f.querySelector(".ctb-err"), btn = f.querySelector("button");
      err.hidden = true;
      if (!f.charter.checked) { err.textContent = "Il faut accepter la charte."; err.hidden = false; return; }
      btn.disabled = true; btn.textContent = "Envoi…";
      api("send-code", { email: f.email.value, charter: true }).then(function (r) {
        btn.disabled = false; btn.textContent = "Recevoir un code";
        if (!r.ok) { err.textContent = r.body.error || "Envoi impossible."; err.hidden = false; return; }
        var c = { challenge: r.body.challenge, email: f.email.value, until: Date.now() + (r.body.expires_in || 900) * 1000 };
        try { sessionStorage.setItem(CH_KEY, JSON.stringify(c)); } catch (x) {}
        renderCode(app, c, personId);
      });
    });
  }
  function renderCode(app, ch, personId) {
    app.innerHTML = '<form class="ctb-form card" id="ctb-code" novalidate><p class="ctb-k">2. Confirme ton adresse</p>' +
      "<p>Un code à six chiffres est parti vers <strong>" + esc(ch.email) + "</strong>. Il expire au bout de 15 minutes. Regarde aussi dans les indésirables.</p>" +
      '<label>Code <input name="code" inputmode="numeric" autocomplete="one-time-code" maxlength="6" pattern="[0-9]{6}" required></label>' +
      '<label>Pseudonyme public <input name="pseudo" maxlength="24" autocomplete="nickname" placeholder="3 à 24 caractères" required></label>' +
      '<p class="ctb-err" role="alert" hidden></p><p><button type="submit" class="btn-pill">Valider</button> <button type="button" class="btn-pill ghost" id="ctb-restart">Changer d\'adresse</button></p></form>';
    $("ctb-restart").addEventListener("click", function () { try { sessionStorage.removeItem(CH_KEY); } catch (x) {} renderLogin(app, personId); });
    $("ctb-code").addEventListener("submit", function (e) {
      e.preventDefault();
      var f = e.target, err = f.querySelector(".ctb-err"), btn = f.querySelector("button");
      err.hidden = true; btn.disabled = true;
      api("verify", { challenge: ch.challenge, code: f.code.value, pseudo: f.pseudo.value }).then(function (r) {
        btn.disabled = false;
        if (!r.ok) { err.textContent = r.body.error || "Code refusé."; err.hidden = false; return; }
        try { sessionStorage.removeItem(CH_KEY); } catch (x) {}
        toast("Bienvenue, " + r.body.pseudo);
        C.view(personId);
      });
    });
  }

  function loadUploader() {
    if (window.OnrecordBlob) return Promise.resolve(window.OnrecordBlob);
    return new Promise(function (res, rej) {
      var s = document.createElement("script");
      s.src = "vendor/blob-upload.js"; s.onload = function () { res(window.OnrecordBlob); }; s.onerror = function () { rej(new Error("chargement")); };
      document.head.appendChild(s);
    });
  }
  function safeName(f) {
    var base = String(f.name || "fichier").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9._-]+/g, "-").replace(/^[^a-z0-9]+/, "").slice(-60);
    return "uploads/" + Date.now().toString(36) + "-" + (base || "fichier");
  }
  function checkFile(f) {
    if (IMAGE_TYPES.indexOf(f.type) >= 0) return f.size <= IMAGE_MAX ? "image" : "« " + f.name + " » dépasse 5 Mo (photos).";
    if (VIDEO_TYPES.indexOf(f.type) >= 0) return f.size <= VIDEO_MAX ? "video" : "« " + f.name + " » dépasse 50 Mo (vidéos).";
    return "« " + f.name + " » : format refusé. Photos JPEG, PNG, WebP, GIF ; vidéos MP4, WebM, MOV.";
  }

  function renderForm(app, pseudo, personId) {
    var opts = ctx.nodes.slice().sort(function (a, b) { return a.name.localeCompare(b.name, "fr"); }).map(function (n) {
      return '<option value="' + esc(n.id) + '"' + (n.id === personId ? " selected" : "") + ">" + esc(n.name) + "</option>";
    }).join("");
    app.innerHTML = '<p class="ctb-logged">Connecté·e : <strong>' + esc(pseudo) + '</strong> <button type="button" class="btn-pill ghost small" id="ctb-logout">Se déconnecter</button></p>' +
      '<form class="ctb-form card" id="ctb-new" novalidate><p class="ctb-k">Nouvelle contribution</p>' +
      '<label>Fiche concernée <select name="person" required><option value="">— Choisir —</option>' + opts + "</select></label>" +
      '<label>Titre <input name="title" maxlength="120" required placeholder="Ce que montre ta preuve, en une ligne"></label>' +
      '<label>Date des faits (facultatif) <input name="event_date" type="date"></label>' +
      '<label>Ce que tu veux signaler <textarea name="text" rows="6" maxlength="3000" required placeholder="Les faits, sans insulte ni jugement. Cite tes sources."></textarea></label>' +
      '<label>Liens de preuve, un par ligne (https://…) <textarea name="links" rows="3" placeholder="https://"></textarea></label>' +
      '<label>Photos ou vidéos (facultatif, 4 au plus) <input name="files" type="file" multiple accept="image/jpeg,image/png,image/webp,image/gif,video/mp4,video/webm,video/quicktime"></label>' +
      '<p class="ctb-hint">Photos : 5 Mo au plus. Vidéos : 50 Mo au plus. Pas de visage ni de donnée d\'une personne privée.</p>' +
      '<label class="ctb-check"><input name="certify" type="checkbox"> <span>Je certifie que ma contribution respecte la charte, que je publie sous ma seule responsabilité, et que j\'ai le droit de diffuser ces fichiers.</span></label>' +
      '<p class="ctb-err" role="alert" hidden></p><p class="ctb-progress" hidden></p><p><button type="submit" class="btn-pill">Envoyer à la modération</button></p></form>';
    $("ctb-logout").addEventListener("click", function () { api("logout", {}).then(function () { C.view(personId); }); });
    $("ctb-new").addEventListener("submit", function (e) {
      e.preventDefault();
      var f = e.target, err = f.querySelector(".ctb-err"), prog = f.querySelector(".ctb-progress"), btn = f.querySelector("button[type=submit]");
      function bad(m) { err.textContent = m; err.hidden = false; btn.disabled = false; prog.hidden = true; }
      err.hidden = true;
      if (!f.certify.checked) return bad("Coche la case de certification.");
      if (!f.person.value) return bad("Choisis une fiche.");
      var files = Array.prototype.slice.call(f.files.files || []);
      if (files.length > 4) return bad("Quatre fichiers au plus.");
      var kinds = files.map(checkFile), wrong = kinds.filter(function (k) { return k !== "image" && k !== "video"; });
      if (wrong.length) return bad(wrong[0]);
      var links = f.links.value.split(/\s+/).map(function (s) { return s.trim(); }).filter(Boolean);
      btn.disabled = true;
      var media = [];
      var chain = Promise.resolve();
      if (files.length) {
        chain = loadUploader().then(function (B) {
          var seq = Promise.resolve();
          files.forEach(function (file, i) {
            seq = seq.then(function () {
              prog.hidden = false; prog.textContent = "Envoi du fichier " + (i + 1) + " sur " + files.length + "…";
              return B.upload(safeName(file), file, {
                access: "public", handleUploadUrl: "/api/contrib/upload", clientPayload: kinds[i], contentType: file.type,
                multipart: file.size > 8 * 1024 * 1024,
                onUploadProgress: function (p) { prog.textContent = "Envoi du fichier " + (i + 1) + " sur " + files.length + " : " + Math.round(p.percentage || 0) + " %"; }
              }).then(function (b) { media.push({ url: b.url, kind: kinds[i] }); });
            });
          });
          return seq;
        });
      }
      chain.then(function () {
        prog.textContent = "Envoi de la contribution…"; prog.hidden = false;
        return api("submit", { person: f.person.value, title: f.title.value, event_date: f.event_date.value, text: f.text.value, links: links, media: media, certify: true });
      }).then(function (r) {
        if (!r.ok) return bad(r.body.error || "Envoi impossible.");
        app.innerHTML = '<div class="card ctb-done"><p class="ctb-k">Merci</p><p>Ta contribution est en attente de validation. Elle paraîtra sur la fiche après relecture. Rien n\'est publié sans validation.</p>' +
          '<p><a class="btn-pill small" href="#/contributions/' + encodeURIComponent(f.person.value) + '" id="ctb-again">Déposer une autre contribution</a></p></div>';
        $("ctb-again").addEventListener("click", function (ev) { ev.preventDefault(); C.view(personId); });
      }, function (x) {
        bad("Un fichier n'a pas pu partir" + (x && x.message ? " (" + x.message + ")" : "") + ". Réessaie, ou mets un lien à la place.");
      });
    });
  }
})();
