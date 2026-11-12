/* Page admin : validation, assemblage des sources, commit GitHub.
   Le jeton n'est jamais placé dans une URL. L'appel réseau est fait par la page,
   uniquement vers https://api.github.com. */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.OnrecordAdmin = api;
  if (typeof document !== "undefined" && document.getElementById("admin-app")) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { api.boot(); });
    else api.boot();
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  var OWNER = "farahei-create";
  var REPO = "cartographie-gaza-extreme-droite";
  var TOKEN_KEY = "onrecord:admin-token";
  var CATEGORIES = [
    "Responsables politiques",
    "Médias & propriétaires",
    "Journalistes & éditorialistes",
    "Intellectuels & essayistes",
    "Organisations & institutions",
    "Événements"
  ];
  var THEMES = [
    "Gaza – déclarations",
    "France – normalisation de l'extrême droite",
    "Proximité extrême droite",
    "Médias – structure",
    "Nuance / contexte",
    "France – montée des violences"
  ];
  var FORBIDDEN = ["complice", "génocidaire", "genocidaire", "pantin", "infiltré", "infiltre", "marionnette", "protégé", "protege", "copinage", "occulte"];
  var PHOTO_HOSTS = {
    "commons.wikimedia.org": 1,
    "upload.wikimedia.org": 1,
    "www.europarl.europa.eu": 1,
    "europarl.europa.eu": 1,
    "www.assemblee-nationale.fr": 1,
    "assemblee-nationale.fr": 1,
    "www.senat.fr": 1,
    "senat.fr": 1
  };

  function oneLine(s) { return String(s == null ? "" : s).replace(/\s+/g, " ").trim(); }
  function norm(s) {
    return oneLine(s).toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }
  function slugify(name) {
    var s = norm(name).replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    return s.slice(0, 60);
  }
  function hostOf(url) {
    try { return new URL(url).hostname.toLowerCase(); } catch (e) { return ""; }
  }
  function validUrl(url) {
    var h = hostOf(url);
    return /^https:\/\//i.test(url || "") && h.indexOf(".") > 0;
  }
  function isWiki(url) {
    var h = hostOf(url);
    return h === "wikipedia.org" || h.slice(-14) === ".wikipedia.org";
  }
  function badWords(text) {
    var low = norm(text);
    return FORBIDDEN.filter(function (w) { return low.indexOf(norm(w)) >= 0; });
  }
  function knownHas(ids, id) {
    if (!id || !ids) return false;
    if (typeof ids.indexOf === "function") return ids.indexOf(id) >= 0;
    return !!ids[id];
  }
  function licenseOk(lic) {
    var low = (lic || "").toLowerCase();
    if (/(^|[^a-z])nc([^a-z]|$)/.test(low) || /(^|[^a-z])nd([^a-z]|$)/.test(low)) return false;
    if (low.indexOf("noncommercial") >= 0 || low.indexOf("non-commercial") >= 0) return false;
    return /cc by|cc-by|cc0|cc-0|public domain|domaine public|portrait officiel/.test(low);
  }
  function photoHostOk(url) { return !!PHOTO_HOSTS[hostOf(url)]; }
  function validDate(d) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(d || "")) return false;
    var p = d.split("-");
    var dt = new Date(Date.UTC(+p[0], +p[1] - 1, +p[2]));
    return dt.getUTCFullYear() === +p[0] && dt.getUTCMonth() === +p[1] - 1 && dt.getUTCDate() === +p[2];
  }
  function foldMedium(st) {
    var parts = [];
    if (oneLine(st.medium)) parts.push(oneLine(st.medium));
    if (oneLine(st.context)) parts.push("Contexte : " + oneLine(st.context));
    if (oneLine(st.denial)) parts.push("Précision ou réponse : " + oneLine(st.denial));
    return parts.join(" ");
  }

  function validateDraft(draft, ids) {
    var errors = [];
    draft = draft || {};
    var people = draft.people || [];
    var statements = draft.statements || [];
    var edges = draft.edges || [];
    var photos = draft.photos || [];
    if (!people.length && !statements.length && !edges.length && !photos.length) {
      errors.push("Rien à publier : ajoute une personnalité, une déclaration ou un lien.");
    }
    var fresh = {};
    people.forEach(function (p) {
      var id = oneLine(p.id);
      if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id)) errors.push("Identifiant invalide : " + (id || "(vide)"));
      if (knownHas(ids, id) || fresh[id]) errors.push("Identifiant déjà utilisé : " + id);
      fresh[id] = 1;
      if (!oneLine(p.name)) errors.push("Nom manquant.");
      if (!oneLine(p.role)) errors.push("Fonction manquante.");
      if (!oneLine(p.description)) errors.push("Description manquante.");
      if (p.type !== "person" && p.type !== "org") errors.push("Type invalide.");
      if (CATEGORIES.indexOf(p.category) < 0) errors.push("Catégorie inconnue.");
      if (!oneLine(p.subcategory)) errors.push("Sous-catégorie manquante.");
      var secs = p.sections || [];
      if (!secs.length || secs.some(function (s) { return s !== "gaza" && s !== "france"; })) errors.push("Choisis Gaza, France, ou les deux.");
      ["name", "role", "description", "subcategory"].forEach(function (f) {
        var hit = badWords(p[f]);
        if (hit.length) errors.push("Mot à retirer dans " + f + " : " + hit.join(", "));
      });
      if (p.type === "person" && !statements.some(function (s) { return s.person_id === id; })) {
        errors.push("Ajoute une déclaration sourcée pour " + (p.name || id) + ".");
      }
    });
    function reachable(id) { return knownHas(ids, id) || !!fresh[id]; }
    statements.forEach(function (s) {
      if (!reachable(s.person_id)) errors.push("Déclaration : choisis une personne.");
      if (!oneLine(s.quote)) errors.push("Citation vide.");
      if (!validDate(s.date)) errors.push("Date invalide. Format AAAA-MM-JJ.");
      var medium = foldMedium(s);
      if (!medium) errors.push("Indique le média ou le support.");
      var hit = badWords(medium);
      if (hit.length) errors.push("Mot à retirer dans le média, le contexte ou la précision : " + hit.join(", "));
      if (!validUrl(s.url)) errors.push("L'URL de la source doit commencer par https://");
      if (isWiki(s.url)) errors.push("Wikipédia ne peut pas être la source.");
      if (!oneLine(s.theme)) errors.push("Choisis un thème.");
      if (s.section !== "gaza" && s.section !== "france") errors.push("Choisis la section de la déclaration.");
      var vid = s.video && (s.video.url || s.video);
      if (vid && typeof vid === "object") vid = vid.url;
      if (vid) {
        if (!validUrl(vid)) errors.push("L'URL de la vidéo doit commencer par https://");
        if (isWiki(vid)) errors.push("La vidéo ne peut pas être une page Wikipédia.");
      }
    });
    edges.forEach(function (e) {
      if (!reachable(e.source) || !reachable(e.target) || e.source === e.target) errors.push("Choisis deux entités différentes.");
      if (!oneLine(e.relation)) errors.push("Décris le lien, de façon neutre.");
      var hit = badWords(e.relation);
      if (hit.length) errors.push("Mot à retirer dans le lien : " + hit.join(", "));
      if (!validUrl(e.url)) errors.push("Le lien doit avoir une URL https://");
      if (isWiki(e.url)) errors.push("Wikipédia ne peut pas être la seule source d'un lien.");
      if (!validDate(e.date)) errors.push("Date du lien invalide.");
      if (e.section && e.section !== "gaza" && e.section !== "france") errors.push("Section du lien invalide.");
      if (e.nature && ["ascension", "opposition", "autre"].indexOf(e.nature) < 0) errors.push("Nature du lien invalide.");
    });
    photos.forEach(function (p) {
      if (!reachable(p.id)) errors.push("Photo : personne inconnue.");
      if (!/^img\/people\/[a-z0-9-]+\.webp$/.test(p.image || "")) errors.push("Photo : fichier WebP attendu.");
      var cr = p.image_credit || {};
      if (!oneLine(cr.author)) errors.push("Photo : indique l'auteur.");
      if (!licenseOk(cr.license)) errors.push("Photo : licence non autorisée (pas de CC BY-NC ni CC BY-ND).");
      if (!validUrl(cr.license_url)) errors.push("Photo : lien de licence https:// manquant.");
      if (!validUrl(cr.source_url)) errors.push("Photo : URL de la source manquante.");
      if (!photoHostOk(cr.source_url)) errors.push("Photo : seulement Wikimedia Commons, ou un portrait officiel (Parlement européen, Assemblée nationale, Sénat).");
    });
    return errors;
  }

  function cleanStatement(s) {
    var out = {
      person_id: s.person_id,
      quote: oneLine(s.quote) ? s.quote.trim() : s.quote,
      date: s.date,
      medium: foldMedium(s),
      url: s.url,
      theme: s.theme,
      section: s.section
    };
    if (s.video && s.video.url) out.video = s.video;
    return out;
  }

  function mergeAdditions(base, draft) {
    base = base && typeof base === "object" ? base : {};
    var out = {
      people: (base.people || []).slice(),
      statements: (base.statements || []).slice(),
      edges: (base.edges || []).slice(),
      photos: (base.photos || []).slice()
    };
    var ids = {};
    out.people.forEach(function (p) { ids[p.id] = 1; });
    (draft.people || []).forEach(function (p) { if (!ids[p.id]) { out.people.push(p); ids[p.id] = 1; } });
    var sq = {};
    out.statements.forEach(function (s) { sq[(s.person_id || "") + "\n" + (s.quote || "")] = 1; });
    (draft.statements || []).forEach(function (s) {
      var k = (s.person_id || "") + "\n" + (s.quote || "");
      if (!sq[k]) { out.statements.push(cleanStatement(s)); sq[k] = 1; }
    });
    var eq = {};
    out.edges.forEach(function (e) { eq[[e.source, e.target, e.url, e.relation].join("\n")] = 1; });
    (draft.edges || []).forEach(function (e) {
      var k = [e.source, e.target, e.url, e.relation].join("\n");
      if (!eq[k]) { out.edges.push(e); eq[k] = 1; }
    });
    var pq = {};
    out.photos.forEach(function (p) { pq[p.id] = { id: p.id, image: p.image, image_credit: p.image_credit }; });
    (draft.photos || []).forEach(function (p) {
      pq[p.id] = { id: p.id, image: p.image, image_credit: p.image_credit };
    });
    out.photos = Object.keys(pq).map(function (k) { return pq[k]; });
    return out;
  }

  function mergePeopleImages(base, photos) {
    var out = {};
    Object.keys(base || {}).forEach(function (k) { out[k] = base[k]; });
    (photos || []).forEach(function (p) {
      out[p.id] = { image: p.image, image_credit: p.image_credit };
    });
    return out;
  }

  function commitMessage(draft) {
    var bits = [];
    (draft.people || []).forEach(function (p) { bits.push(oneLine(p.name)); });
    (draft.statements || []).forEach(function (s) { bits.push("déclaration " + oneLine(s.person_name || s.person_id)); });
    (draft.edges || []).forEach(function (e) { bits.push("lien " + oneLine(e.source) + " – " + oneLine(e.target)); });
    if (!bits.length && (draft.photos || []).length) bits.push("photo");
    return ("admin: ajout " + bits.filter(Boolean).slice(0, 3).join(", ")).slice(0, 180);
  }

  function filesFromDraft(remote, draft) {
    remote = remote || {};
    var merged = mergeAdditions(remote.additions, draft);
    var files = [];
    var touches = (draft.people || []).length || (draft.statements || []).length || (draft.edges || []).length || (draft.photos || []).length;
    if (touches) {
      files.push({ path: "tools/admin_additions.json", encoding: "utf-8", content: JSON.stringify(merged, null, 2) + "\n" });
    }
    if ((draft.photos || []).length) {
      var imgs = mergePeopleImages(remote.peopleImages, draft.photos);
      files.push({ path: "tools/people_images.json", encoding: "utf-8", content: JSON.stringify(imgs, null, 1) + "\n" });
      draft.photos.forEach(function (p) {
        if (p.base64) files.push({ path: p.image, encoding: "base64", content: p.base64 });
      });
    }
    return { files: files, message: commitMessage(draft), additions: merged };
  }

  function decodeB64(s) {
    var bin = atob(String(s || "").replace(/\s/g, ""));
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i) & 255;
    if (typeof TextDecoder !== "undefined") return new TextDecoder("utf-8").decode(bytes);
    var out = "";
    for (var j = 0; j < bytes.length; j++) out += String.fromCharCode(bytes[j]);
    return out;
  }

  function commitFiles(opts) {
    var github = opts.github;
    var base = "/repos/" + (opts.owner || OWNER) + "/" + (opts.repo || REPO);
    var lastStatus = 0;
    function fail(msg) { var e = new Error(msg); e.status = lastStatus; throw e; }
    function run(attempt) {
      return Promise.resolve().then(function () { return opts.prepare(); }).then(function (prepared) {
        if (!prepared || !prepared.files || !prepared.files.length) fail("Rien à envoyer.");
        return github("GET", base + "/git/ref/heads/main").then(function (ref) {
          lastStatus = ref.status;
          if (ref.status === 401) fail("Jeton refusé. Il est invalide, expiré ou révoqué.");
          if (ref.status === 403) fail("Ce jeton ne peut pas modifier le dépôt. Il lui faut Contents en lecture et écriture, limité à ce dépôt.");
          if (ref.status === 404) fail("Dépôt introuvable avec ce jeton.");
          if (ref.status !== 200 || !ref.body || !ref.body.object) fail("Lecture de la branche impossible (" + ref.status + ").");
          var parent = ref.body.object.sha;
          return github("GET", base + "/git/commits/" + parent).then(function (commit) {
            lastStatus = commit.status;
            if (commit.status !== 200 || !commit.body || !commit.body.tree) fail("Lecture du commit impossible (" + commit.status + ").");
            var treeSha = commit.body.tree.sha;
            var chain = Promise.resolve([]);
            prepared.files.forEach(function (f) {
              chain = chain.then(function (entries) {
                return github("POST", base + "/git/blobs", { content: f.content, encoding: f.encoding || "utf-8" }).then(function (blob) {
                  lastStatus = blob.status;
                  if (blob.status === 401) fail("Jeton refusé. Il est invalide, expiré ou révoqué.");
                  if (blob.status !== 201 && blob.status !== 200) fail("Envoi de " + f.path + " refusé (" + blob.status + ").");
                  entries.push({ path: f.path, mode: "100644", type: "blob", sha: blob.body.sha });
                  return entries;
                });
              });
            });
            return chain.then(function (entries) {
              return github("POST", base + "/git/trees", { base_tree: treeSha, tree: entries });
            }).then(function (tree) {
              lastStatus = tree.status;
              if (tree.status !== 201 && tree.status !== 200) fail("Préparation du commit refusée (" + tree.status + ").");
              return github("POST", base + "/git/commits", {
                message: prepared.message,
                tree: tree.body.sha,
                parents: [parent]
              });
            }).then(function (made) {
              lastStatus = made.status;
              if (made.status !== 201 && made.status !== 200) fail("Création du commit refusée (" + made.status + ").");
              return github("PATCH", base + "/git/refs/heads/main", { sha: made.body.sha }).then(function (upd) {
                lastStatus = upd.status;
                if (upd.status === 200) {
                  var sha = made.body.sha;
                  return {
                    sha: sha,
                    url: "https://github.com/" + (opts.owner || OWNER) + "/" + (opts.repo || REPO) + "/commit/" + sha,
                    attempt: attempt
                  };
                }
                if ((upd.status === 422 || upd.status === 409) && attempt < 3) return run(attempt + 1);
                if (upd.status === 422 || upd.status === 409) fail("Conflit de version (sha). La page a relu le dépôt trois fois. Réessaie.");
                fail("Publication refusée (" + upd.status + ").");
              });
            });
          });
        });
      });
    }
    return run(1);
  }

  function fileToWebp(file, max) {
    max = max || 400;
    return new Promise(function (resolve, reject) {
      if (typeof document === "undefined") { reject(new Error("Conversion disponible dans le navigateur.")); return; }
      if (!file || !/^image\//.test(file.type || "")) { reject(new Error("Choisis une image.")); return; }
      if (file.size > 15 * 1024 * 1024) { reject(new Error("Image trop lourde (15 Mo maximum).")); return; }
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () {
        var iw = img.naturalWidth || img.width, ih = img.naturalHeight || img.height;
        var scale = Math.min(1, max / Math.max(iw, ih));
        var w = Math.max(1, Math.round(iw * scale));
        var h = Math.max(1, Math.round(ih * scale));
        var canvas = document.createElement("canvas");
        canvas.width = w; canvas.height = h;
        canvas.getContext("2d").drawImage(img, 0, 0, w, h);
        canvas.toBlob(function (blob) {
          URL.revokeObjectURL(url);
          if (!blob) { reject(new Error("Cet appareil n'a pas pu convertir la photo en WebP.")); return; }
          var reader = new FileReader();
          reader.onload = function () {
            var raw = String(reader.result || "");
            resolve({ base64: raw.split(",")[1] || "", w: w, h: h, type: blob.type });
          };
          reader.onerror = function () { reject(new Error("Lecture de la photo impossible.")); };
          reader.readAsDataURL(blob);
        }, "image/webp", 0.82);
      };
      img.onerror = function () { URL.revokeObjectURL(url); reject(new Error("Image illisible.")); };
      img.src = url;
    });
  }

  function boot() {
    var $ = function (id) { return document.getElementById(id); };
    function esc(s) {
      return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
      });
    }
    var draft = { people: [], statements: [], edges: [], photos: [] };
    var catalog = [];
    var byId = {};
    var token = "";

    function readToken() {
      try { return localStorage.getItem(TOKEN_KEY) || ""; } catch (e) { return ""; }
    }
    function writeToken(v) {
      try {
        if (v) localStorage.setItem(TOKEN_KEY, v);
        else localStorage.removeItem(TOKEN_KEY);
      } catch (e) {}
    }
    function showGate(msg) {
      $("gate").hidden = false;
      $("workspace").hidden = true;
      $("gate-error").hidden = !msg;
      $("gate-error").textContent = msg || "";
    }
    function showApp() {
      $("gate").hidden = true;
      $("workspace").hidden = false;
    }
    function setBusy(on) {
      $("btn-publish").disabled = on;
      $("btn-stage").disabled = on;
    }
    function github(method, path, body) {
      var url = "https://api.github.com" + path;
      if (url.indexOf("https://api.github.com/") !== 0) return Promise.reject(new Error("Requête bloquée."));
      return fetch(url, {
        method: method,
        headers: {
          Authorization: "Bearer " + token,
          Accept: "application/vnd.github+json",
          "X-GitHub-Api-Version": "2022-11-28",
          "Content-Type": "application/json",
          "User-Agent": "onrecord-admin"
        },
        body: body == null ? undefined : JSON.stringify(body)
      }).then(function (r) {
        return r.text().then(function (t) {
          var parsed = null;
          try { parsed = t ? JSON.parse(t) : null; } catch (e) { parsed = { message: t }; }
          return { status: r.status, body: parsed };
        });
      }, function () {
        throw new Error("Pas de réseau, ou GitHub ne répond pas.");
      });
    }
    function verify() {
      return github("GET", "/repos/" + OWNER + "/" + REPO).then(function (res) {
        if (res.status === 200) return;
        if (res.status === 401) throw new Error("Jeton refusé. Il est invalide, expiré ou révoqué.");
        if (res.status === 403) throw new Error("Ce jeton ne peut pas lire le dépôt. Contents : lecture et écriture, sur ce dépôt seulement.");
        if (res.status === 404) throw new Error("Dépôt introuvable avec ce jeton. Limite-le à " + OWNER + "/" + REPO + ".");
        throw new Error("GitHub a répondu " + res.status + ".");
      });
    }
    function taxonomy() {
      var map = {};
      catalog.forEach(function (n) {
        if (!n.category) return;
        if (!map[n.category]) map[n.category] = [];
        if (n.subcategory && map[n.category].indexOf(n.subcategory) < 0) map[n.category].push(n.subcategory);
      });
      CATEGORIES.forEach(function (c) { if (!map[c]) map[c] = []; });
      return map;
    }
    function fillCategories() {
      var map = taxonomy();
      var sel = $("p-cat");
      sel.innerHTML = CATEGORIES.map(function (c) { return '<option value="' + esc(c) + '">' + esc(c) + "</option>"; }).join("");
      function subs() {
        var list = map[sel.value] || [];
        $("p-sub").innerHTML = list.map(function (s) { return '<option value="' + esc(s) + '">' + esc(s) + "</option>"; }).join("")
          || '<option value="">Aucune sous-catégorie connue</option>';
      }
      sel.onchange = subs;
      subs();
      var themes = {};
      THEMES.forEach(function (t) { themes[t] = 1; });
      catalog.forEach(function (n) { (n.statements || []).forEach(function (s) { if (s.theme) themes[s.theme] = 1; }); });
      $("st-theme").innerHTML = Object.keys(themes).map(function (t) { return '<option value="' + esc(t) + '">' + esc(t) + "</option>"; }).join("");
    }
    function peopleOptions(filter) {
      var q = norm(filter);
      var rows = catalog.filter(function (n) {
        return !q || norm(n.name + " " + (n.role || "")).indexOf(q) >= 0;
      });
      draft.people.forEach(function (p) {
        if (!q || norm(p.name).indexOf(q) >= 0) rows.push({ id: p.id, name: p.name + " (brouillon)", role: p.role });
      });
      return rows;
    }
    function fillSelect(sel, filter) {
      var cur = sel.value;
      var rows = peopleOptions(filter);
      sel.innerHTML = '<option value="">Choisir…</option>' + rows.map(function (n) {
        return '<option value="' + esc(n.id) + '">' + esc(n.name) + "</option>";
      }).join("");
      if (cur) sel.value = cur;
    }
    function refreshSelects() {
      fillSelect($("st-person"), $("st-filter").value);
      fillSelect($("e-source"), $("e-filter").value);
      fillSelect($("e-target"), $("e-filter2").value);
      fillSelect($("ph-existing"), $("ph-filter").value);
    }
    function renderPreview() {
      var box = $("preview");
      var n = draft.people.length + draft.statements.length + draft.edges.length + draft.photos.length;
      if (!n) { box.innerHTML = '<p class="hint">L’aperçu est vide. Remplis un formulaire, puis « Voir l’aperçu ».</p>'; return; }
      var html = "";
      draft.people.forEach(function (p, i) {
        html += '<article class="pv"><p class="k">Personnalité</p><h3>' + esc(p.name) + '</h3><p>' + esc(p.role) + '</p><p class="hint">' + esc(p.category) + " · " + esc(p.subcategory) + " · " + esc((p.sections || []).join(", ")) + '</p><button type="button" data-rm="people:' + i + '">Retirer</button></article>';
      });
      draft.statements.forEach(function (s, i) {
        html += '<article class="pv"><p class="k">Déclaration</p><h3>' + esc(s.person_name || s.person_id) + '</h3><blockquote>' + esc(s.quote) + '</blockquote><p>' + esc(s.date) + " · " + esc(foldMedium(s)) + '</p><p class="hint">' + esc(s.url) + "</p>" + (s.video && s.video.url ? '<p class="hint">Vidéo : ' + esc(s.video.url) + "</p>" : "") + '<button type="button" data-rm="statements:' + i + '">Retirer</button></article>';
      });
      draft.edges.forEach(function (e, i) {
        html += '<article class="pv"><p class="k">Lien</p><h3>' + esc(e.source_name || e.source) + " → " + esc(e.target_name || e.target) + '</h3><p>' + esc(e.relation) + '</p><p class="hint">' + esc(e.date) + " · " + esc(e.url) + '</p><button type="button" data-rm="edges:' + i + '">Retirer</button></article>';
      });
      draft.photos.forEach(function (p, i) {
        html += '<article class="pv"><p class="k">Photo</p><h3>' + esc(p.name || p.id) + '</h3><p>' + esc((p.image_credit || {}).author || "") + " · " + esc((p.image_credit || {}).license || "") + '</p><p class="hint">' + esc(p.image) + '</p><button type="button" data-rm="photos:' + i + '">Retirer</button></article>';
      });
      box.innerHTML = html;
    }
    function val(id) { return ($(id).value || "").trim(); }
    function checked(name) {
      return Array.prototype.map.call(document.querySelectorAll('input[name="' + name + '"]:checked'), function (el) { return el.value; });
    }
    function personMode() { return document.querySelector('input[name="pmode"]:checked').value; }
    function stagePerson() {
      if (personMode() === "existing") {
        var id = val("ph-existing");
        if (!id || !byId[id]) return ["Choisis une personne déjà dans l’archive."];
        return attachPhoto(id, byId[id].name);
      }
      var name = val("p-name");
      var id = slugify(name);
      var n = 2;
      while ((byId[id] || draft.people.some(function (p) { return p.id === id; })) && n < 50) { id = slugify(name) + "-" + n; n++; }
      var role = val("p-role");
      var org = val("p-org");
      if (org && norm(role).indexOf(norm(org)) < 0) role = role + " (" + org + ")";
      var description = val("p-desc") || role;
      var person = {
        id: id,
        name: name,
        type: document.querySelector('input[name="ptype"]:checked').value,
        role: role,
        description: description,
        category: val("p-cat"),
        subcategory: val("p-sub"),
        sections: checked("psec")
      };
      var batch = { people: draft.people.concat([person]), statements: draft.statements, edges: draft.edges, photos: draft.photos.slice() };
      var photoErrors = [];
      var file = $("p-file").files && $("p-file").files[0];
      if (person.type === "org") file = null;
      function finish(extraPhoto) {
        if (extraPhoto) batch.photos = draft.photos.concat([extraPhoto]);
        var errs = validateDraft(batch, byId).filter(function (e) {
          return e.indexOf("Rien à publier") !== 0 && e.indexOf("Ajoute une déclaration") !== 0;
        });
        if (person.type === "person" && !draft.statements.some(function (s) { return s.person_id === id; })) {
          errs.push("Cette personne sera publiée avec une déclaration : ajoute-la dans l’onglet Déclaration avant de publier. Tu peux quand même la mettre dans l’aperçu.");
        }
        if (errs.length && !(errs.length === 1 && errs[0].indexOf("Cette personne sera publiée") === 0)) return Promise.resolve(errs);
        draft.people.push(person);
        if (extraPhoto) draft.photos.push(extraPhoto);
        return Promise.resolve(errs.filter(function (e) { return e.indexOf("Cette personne sera publiée") === 0; }));
      }
      if (!file) return finish(null);
      return readPhoto(file, id, name).then(function (ph) { return finish(ph); }, function (e) { return [e.message]; });
    }
    function creditFromForm() {
      return {
        author: val("ph-author"),
        license: val("ph-license"),
        license_url: val("ph-license-url"),
        source_url: val("ph-source")
      };
    }
    function readPhoto(file, id, name) {
      var cr = creditFromForm();
      if (!cr.author || !cr.license || !cr.license_url || !cr.source_url) {
        return Promise.reject(new Error("Photo : auteur, licence, lien de licence et URL de la source sont obligatoires. Sinon, laisse la photo vide."));
      }
      return fileToWebp(file, 400).then(function (img) {
        if (img.w > 400 || img.h > 400) throw new Error("La photo dépasse 400 px.");
        if (img.type.indexOf("webp") < 0) throw new Error("La conversion WebP a échoué.");
        return { id: id, name: name, image: "img/people/" + id + ".webp", image_credit: cr, base64: img.base64 };
      });
    }
    function attachPhoto(id, name) {
      var file = $("p-file").files && $("p-file").files[0];
      if (!file) return Promise.resolve(["Choisis une photo, ou passe en « Nouvelle personnalité »."]);
      return readPhoto(file, id, name).then(function (ph) {
        draft.photos = draft.photos.filter(function (p) { return p.id !== id; });
        draft.photos.push(ph);
        return [];
      }, function (e) { return [e.message]; });
    }
    function stageStatement() {
      var pid = val("st-person");
      var node = byId[pid] || draft.people.filter(function (p) { return p.id === pid; })[0];
      var videoUrl = val("st-video");
      var st = {
        person_id: pid,
        person_name: node ? node.name : pid,
        quote: $("st-quote").value.trim(),
        date: val("st-date"),
        medium: val("st-medium"),
        context: val("st-context"),
        denial: val("st-denial"),
        url: val("st-url"),
        theme: val("st-theme"),
        section: val("st-section")
      };
      if (videoUrl) {
        st.video = { url: videoUrl, title: val("st-video-title") || "Vidéo", source: val("st-video-source") || hostOf(videoUrl), platform: hostOf(videoUrl) };
      }
      var batch = { people: draft.people, statements: draft.statements.concat([st]), edges: draft.edges, photos: draft.photos };
      var errs = validateDraft(batch, byId).filter(function (e) { return e.indexOf("Rien à publier") !== 0 && e.indexOf("Ajoute une déclaration sourcée") !== 0; });
      if (errs.length) return errs;
      draft.statements.push(st);
      return [];
    }
    function stageEdge() {
      var src = val("e-source"), tgt = val("e-target");
      function label(id) {
        if (byId[id]) return byId[id].name;
        var p = draft.people.filter(function (x) { return x.id === id; })[0];
        return p ? p.name : id;
      }
      var edge = {
        source: src,
        target: tgt,
        source_name: label(src),
        target_name: label(tgt),
        relation: val("e-rel"),
        url: val("e-url"),
        date: val("e-date"),
        section: val("e-section"),
        nature: val("e-nature") || "autre"
      };
      var batch = { people: draft.people, statements: draft.statements, edges: draft.edges.concat([edge]), photos: draft.photos };
      var errs = validateDraft(batch, byId).filter(function (e) { return e.indexOf("Rien à publier") !== 0 && e.indexOf("Ajoute une déclaration sourcée") !== 0; });
      if (errs.length) return errs;
      draft.edges.push(edge);
      return [];
    }
    function activePanel() {
      var on = document.querySelector(".tabs button[aria-selected='true']");
      return on ? on.getAttribute("data-tab") : "person";
    }
    function stageActive() {
      var tab = activePanel();
      if (tab === "statement") return Promise.resolve(stageStatement());
      if (tab === "edge") return Promise.resolve(stageEdge());
      return Promise.resolve(stagePerson()).then(function (v) { return v; });
    }
    function showErrors(list) {
      var el = $("form-errors");
      if (!list || !list.length) { el.hidden = true; el.textContent = ""; return; }
      el.hidden = false;
      el.textContent = list.join(" ");
    }
    function clearStatus() { $("pub-status").textContent = ""; }
    function loadCatalog() {
      return fetch("data.json", { cache: "no-store" }).then(function (r) {
        if (!r.ok) throw new Error("data.json introuvable");
        return r.json();
      }).then(function (d) {
        catalog = d.nodes || [];
        byId = {};
        catalog.forEach(function (n) { byId[n.id] = n; });
        fillCategories();
        refreshSelects();
      });
    }
    function publish() {
      clearStatus();
      var errs = validateDraft(draft, byId);
      if (errs.length) { showErrors(errs); return; }
      showErrors([]);
      setBusy(true);
      $("pub-status").textContent = "Publication…";
      commitFiles({
        owner: OWNER,
        repo: REPO,
        github: github,
        prepare: function () {
          return readPair().then(function (remote) { return filesFromDraft(remote, draft); });
        }
      }).then(function (res) {
        draft.people = []; draft.statements = []; draft.edges = []; draft.photos = [];
        renderPreview();
        $("pub-status").innerHTML = 'Publié. <a href="' + esc(res.url) + '">Voir le commit</a>. En ligne dans ~1 min.';
      }, function (e) {
        $("pub-status").textContent = e.message || "Échec de la publication.";
      }).then(function () { setBusy(false); });
    }
    function readPair() {
      function read(path) {
        return github("GET", "/repos/" + OWNER + "/" + REPO + "/contents/" + path).then(function (res) {
          if (res.status === 404) return null;
          if (res.status === 401) throw new Error("Jeton refusé. Il est invalide, expiré ou révoqué.");
          if (res.status !== 200 || !res.body || !res.body.content) throw new Error("Lecture de " + path + " impossible (" + res.status + ").");
          return JSON.parse(decodeB64(res.body.content));
        });
      }
      return Promise.all([read("tools/admin_additions.json"), read("tools/people_images.json")]).then(function (pair) {
        return { additions: pair[0] || { people: [], statements: [], edges: [], photos: [] }, peopleImages: pair[1] || {} };
      });
    }

    document.querySelectorAll(".tabs button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        document.querySelectorAll(".tabs button").forEach(function (b) { b.setAttribute("aria-selected", b === btn ? "true" : "false"); });
        document.querySelectorAll(".pane").forEach(function (p) { p.hidden = p.id !== "pane-" + btn.getAttribute("data-tab"); });
        showErrors([]);
      });
    });
    $("preview").addEventListener("click", function (ev) {
      var b = ev.target.closest("button[data-rm]");
      if (!b) return;
      var parts = b.getAttribute("data-rm").split(":");
      draft[parts[0]].splice(+parts[1], 1);
      renderPreview();
    });
    $("st-filter").addEventListener("input", function () { fillSelect($("st-person"), $("st-filter").value); });
    $("e-filter").addEventListener("input", function () { fillSelect($("e-source"), $("e-filter").value); });
    $("e-filter2").addEventListener("input", function () { fillSelect($("e-target"), $("e-filter2").value); });
    $("ph-filter").addEventListener("input", function () { fillSelect($("ph-existing"), $("ph-filter").value); });
    $("ph-license").addEventListener("change", function () {
      var opt = $("ph-license").selectedOptions[0];
      if (opt && opt.getAttribute("data-url")) $("ph-license-url").value = opt.getAttribute("data-url");
    });
    document.querySelectorAll('input[name="pmode"]').forEach(function (el) {
      el.addEventListener("change", function () {
        var ex = personMode() === "existing";
        $("new-fields").hidden = ex;
        $("existing-fields").hidden = !ex;
      });
    });
    document.querySelectorAll('input[name="ptype"]').forEach(function (el) {
      el.addEventListener("change", function () {
        $("photo-block").hidden = document.querySelector('input[name="ptype"]:checked').value === "org";
      });
    });
    $("btn-login").addEventListener("click", function () {
      var v = val("token");
      if (v.length < 20 || (v.indexOf("github_pat_") !== 0 && v.indexOf("ghp_") !== 0)) {
        $("gate-error").hidden = false;
        $("gate-error").textContent = "Colle un jeton fine-grained (github_pat_…) ou classique (ghp_…).";
        return;
      }
      token = v;
      $("btn-login").disabled = true;
      verify().then(function () {
        writeToken(token);
        $("token").value = "";
        showApp();
        return loadCatalog();
      }, function (e) {
        token = "";
        $("gate-error").hidden = false;
        $("gate-error").textContent = e.message;
      }).then(function () { $("btn-login").disabled = false; }, function (e) {
        $("btn-login").disabled = false;
        $("form-errors").hidden = false;
        $("form-errors").textContent = (e && e.message) || "Lecture de data.json impossible.";
      });
    });
    $("btn-logout").addEventListener("click", function () {
      token = "";
      writeToken("");
      draft = { people: [], statements: [], edges: [], photos: [] };
      renderPreview();
      showGate("Jeton effacé de cet appareil.");
    });
    $("btn-stage").addEventListener("click", function () {
      clearStatus();
      Promise.resolve(stageActive()).then(function (errs) {
        var hard = (errs || []).filter(function (e) { return e.indexOf("Cette personne sera publiée") !== 0; });
        showErrors(hard.length ? hard : (errs || []));
        if (!hard.length) renderPreview();
        refreshSelects();
      });
    });
    $("btn-publish").addEventListener("click", publish);
    renderPreview();
    token = readToken();
    if (!token) { showGate(""); return; }
    showApp();
    verify().then(function () { return loadCatalog(); }, function (e) {
      token = "";
      writeToken("");
      showGate(e.message);
    }).catch(function (e) {
      $("form-errors").hidden = false;
      $("form-errors").textContent = e.message || "Lecture de data.json impossible.";
    });
  }

  return {
    OWNER: OWNER,
    REPO: REPO,
    CATEGORIES: CATEGORIES,
    slugify: slugify,
    validUrl: validUrl,
    isWiki: isWiki,
    badWords: badWords,
    foldMedium: foldMedium,
    validateDraft: validateDraft,
    mergeAdditions: mergeAdditions,
    mergePeopleImages: mergePeopleImages,
    commitMessage: commitMessage,
    filesFromDraft: filesFromDraft,
    decodeB64: decodeB64,
    commitFiles: commitFiles,
    fileToWebp: fileToWebp,
    boot: boot
  };
});
