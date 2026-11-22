/* Contributions des lecteurs : inscription par code e-mail, dépôt, signalement, modération.
   Toute la logique est ici, sans dépendance au réseau : api/contrib/[action].js branche
   le vrai stockage (Vercel Blob), l'envoi d'e-mail (Resend ou Brevo), le DNS et GitHub.
   Les tests (tests/test_contributions.mjs) branchent des doublures. */
"use strict";
var crypto = require("crypto");

var OWNER = "farahei-create";
var REPO = "cartographie-gaza-extreme-droite";
var PUBLISHED_PATH = "contributions.json";

var CODE_TTL = 15 * 60 * 1000;
var SESSION_TTL = 30 * 24 * 3600 * 1000;
var IMAGE_MAX = 5 * 1024 * 1024;
var VIDEO_MAX = 50 * 1024 * 1024;
var IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"];
var VIDEO_TYPES = ["video/mp4", "video/webm", "video/quicktime"];
var COOKIE = "onrecord_s";

var FORBIDDEN = ["complice", "genocidaire", "pantin", "infiltre", "marionnette", "protege", "copinage", "occulte"];
var REPORT_KINDS = ["faux", "prive", "injure", "illicite", "autre"];

var DISPOSABLE = null;
function disposableSet() {
  if (!DISPOSABLE) DISPOSABLE = new Set(require("./disposable_domains.json").domains);
  return DISPOSABLE;
}

/* ---------- utilitaires ---------- */
function fail(status, msg, extra) { var e = new Error(msg); e.status = status; e.extra = extra; return e; }
function b64u(buf) { return Buffer.from(buf).toString("base64").replace(/=+$/, "").replace(/\+/g, "-").replace(/\//g, "_"); }
function unb64u(s) { return Buffer.from(String(s).replace(/-/g, "+").replace(/_/g, "/"), "base64"); }
function hmac(secret, data) { return crypto.createHmac("sha256", secret).update(data).digest(); }
function hhex(secret, data, n) { return hmac(secret, data).toString("hex").slice(0, n || 32); }
function safeEq(a, b) {
  a = Buffer.from(String(a)); b = Buffer.from(String(b));
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}
function str(v, max) { return String(v == null ? "" : v).replace(/\u0000/g, "").trim().slice(0, max || 10000); }
function fold(s) { return String(s || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase(); }

function sign(secret, payload) {
  var body = b64u(JSON.stringify(payload));
  return body + "." + b64u(hmac(secret, "tok:" + body));
}
function unsign(secret, token) {
  var parts = String(token || "").split(".");
  if (parts.length !== 2) return null;
  if (!safeEq(parts[1], b64u(hmac(secret, "tok:" + parts[0])))) return null;
  try { return JSON.parse(unb64u(parts[0]).toString("utf8")); } catch (e) { return null; }
}
function encKey(secret) { return crypto.createHash("sha256").update("enc:" + secret).digest(); }
function encrypt(secret, text) {
  var iv = crypto.randomBytes(12), c = crypto.createCipheriv("aes-256-gcm", encKey(secret), iv);
  var out = Buffer.concat([c.update(String(text), "utf8"), c.final()]);
  return b64u(Buffer.concat([iv, c.getAuthTag(), out]));
}
function decrypt(secret, blob) {
  try {
    var raw = unb64u(blob), d = crypto.createDecipheriv("aes-256-gcm", encKey(secret), raw.subarray(0, 12));
    d.setAuthTag(raw.subarray(12, 28));
    return Buffer.concat([d.update(raw.subarray(28)), d.final()]).toString("utf8");
  } catch (e) { return ""; }
}

/* ---------- règles ---------- */
var EMAIL_RE = /^[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+)$/;
function normEmail(e) { return str(e, 254).toLowerCase(); }
function isDisposable(email) {
  var m = EMAIL_RE.exec(email);
  if (!m) return false;
  var parts = m[1].split("."), set = disposableSet();
  for (var i = 0; i < parts.length - 1; i++) if (set.has(parts.slice(i).join("."))) return true;
  return false;
}
function checkPseudo(p) {
  p = str(p, 40).replace(/\s+/g, " ");
  if (p.length < 3 || p.length > 24) throw fail(400, "Le pseudonyme doit faire entre 3 et 24 caractères.");
  if (!/^[\p{L}\p{N} ._'-]+$/u.test(p)) throw fail(400, "Le pseudonyme ne peut contenir que des lettres, des chiffres, des espaces et . _ ' -");
  if (/@/.test(p)) throw fail(400, "Pas d'adresse e-mail dans le pseudonyme.");
  if (forbiddenIn(p).length) throw fail(400, "Ce pseudonyme contient un mot refusé par la charte.");
  return p;
}
function forbiddenIn(text) {
  var t = fold(text), found = [];
  FORBIDDEN.forEach(function (w) { if (new RegExp("(^|[^a-z])" + w + "(e|s|es)?([^a-z]|$)").test(t)) found.push(w); });
  return found;
}
/* Indices de données personnelles : à vérifier par l'admin, pas un refus automatique. */
function privateHints(text) {
  var t = String(text || ""), hints = [];
  if (/(?:\+33|0)\s?[1-9](?:[\s.-]?\d{2}){4}/.test(t)) hints.push("numéro de téléphone");
  if (/[^\s@]+@[^\s@]+\.[a-z]{2,}/i.test(t)) hints.push("adresse e-mail");
  if (/\b\d{1,4}\s?(bis|ter)?,?\s+(rue|avenue|av\.|boulevard|bd|impasse|allée|chemin|place)\b/i.test(t)) hints.push("adresse postale");
  return hints;
}
function httpsUrl(u) {
  u = str(u, 600);
  if (!/^https:\/\/[^\s<>"']+$/i.test(u)) return "";
  try { var x = new URL(u); return x.protocol === "https:" && x.hostname.indexOf(".") > 0 ? x.toString() : ""; } catch (e) { return ""; }
}
function isOurMedia(u) {
  try {
    var x = new URL(u);
    return x.protocol === "https:" && /\.public\.blob\.vercel-storage\.com$/.test(x.hostname) && x.pathname.indexOf("/uploads/") === 0;
  } catch (e) { return false; }
}
function newId(now) { return now.toString(36) + crypto.randomBytes(8).toString("hex"); }

/* ---------- configuration ---------- */
function config(env) {
  env = env || {};
  var secret = String(env.SESSION_SECRET || "");
  var mail = env.RESEND_API_KEY ? "resend" : env.BREVO_API_KEY ? "brevo" : "";
  var c = {
    storage: !!env.BLOB_READ_WRITE_TOKEN,
    secret: secret.length >= 16,
    mail: mail,
    from: String(env.MAIL_FROM || (mail === "resend" ? "Onrecord <onboarding@resend.dev>" : ""))
  };
  c.enabled = c.storage && c.secret && !!c.mail && !!c.from;
  c.reports = c.storage && c.secret;
  return c;
}
function status(env) {
  var c = config(env);
  return { enabled: c.enabled, reports: c.reports, storage: c.storage, session: c.secret, mail: c.mail || null, from_set: !!c.from };
}

/* ---------- limites de débit (marqueurs immuables dans le stockage) ---------- */
function countSince(store, prefix, since) {
  return store.list(prefix).then(function (xs) { return xs.filter(function (x) { return x.uploadedAt >= since; }).length; });
}
function mark(store, prefix) { return store.put(prefix + "/m", { t: 1 }); }
function sweep(store, now) {
  /* marqueurs de plus de deux jours : on les retire de temps en temps */
  if (Math.random() > 0.05) return Promise.resolve();
  return store.list("rl/").then(function (xs) {
    return store.del(xs.filter(function (x) { return x.uploadedAt < now - 2 * 86400000; }).map(function (x) { return x.url; }));
  }).catch(function () {});
}

/* ---------- session ---------- */
function parseCookies(h) {
  var out = {};
  String(h || "").split(/;\s*/).forEach(function (p) { var i = p.indexOf("="); if (i > 0) out[p.slice(0, i)] = decodeURIComponent(p.slice(i + 1)); });
  return out;
}
function sessionFrom(req, env, now) {
  var c = config(env);
  if (!c.secret) return null;
  var tok = parseCookies(req.headers && req.headers.cookie)[COOKIE];
  var s = unsign(env.SESSION_SECRET, tok);
  if (!s || s.k !== "s" || !s.eh || !s.p || !(s.x > now)) return null;
  return s;
}
function cookieFor(token, maxAgeSec) {
  return COOKIE + "=" + encodeURIComponent(token) + "; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=" + maxAgeSec;
}

/* ---------- actions publiques ---------- */
function requireEnabled(env) {
  if (!config(env).enabled) throw fail(503, "Les contributions arrivent bientôt.", { soon: true });
}

function sendCode(body, req, deps) {
  var env = deps.env, now = deps.now();
  requireEnabled(env);
  if (body.charter !== true) throw fail(400, "Il faut accepter la charte.");
  var email = normEmail(body.email);
  if (!EMAIL_RE.test(email)) throw fail(400, "Adresse e-mail invalide.");
  if (isDisposable(email)) throw fail(400, "Les adresses e-mail jetables ne sont pas acceptées.");
  var domain = email.split("@")[1];
  var eh = hhex(env.SESSION_SECRET, "email:" + email);
  var iph = hhex(env.SESSION_SECRET, "ip:" + (req.ip || "?"), 20);
  var store = deps.store;
  return Promise.resolve(deps.domainOk ? deps.domainOk(domain) : true).then(function (ok) {
    if (!ok) throw fail(400, "Ce domaine ne reçoit pas d'e-mail. Vérifie l'adresse.");
    return Promise.all([
      countSince(store, "rl/send/" + eh, now - 60000),
      countSince(store, "rl/send/" + eh, now - 3600000),
      countSince(store, "rl/ip/" + iph, now - 3600000)
    ]);
  }).then(function (n) {
    if (n[0] >= 1) throw fail(429, "Un code vient d'être envoyé. Attends une minute.");
    if (n[1] >= 5) throw fail(429, "Trop de codes demandés pour cette adresse. Réessaie dans une heure.");
    if (n[2] >= 20) throw fail(429, "Trop de demandes depuis ce réseau. Réessaie dans une heure.");
    var code = String(crypto.randomInt(0, 1000000)).padStart(6, "0");
    var x = now + CODE_TTL, nonce = crypto.randomBytes(9).toString("hex");
    var challenge = sign(env.SESSION_SECRET, {
      k: "c", eh: eh, ee: encrypt(env.SESSION_SECRET, email), x: x, n: nonce,
      h: hhex(env.SESSION_SECRET, "code:" + nonce + ":" + eh + ":" + code, 64)
    });
    var text = "Ton code Onrecord : " + code + "\n\nIl expire dans 15 minutes. Si tu n'as rien demandé, ignore ce message.\n\nOnrecord — contributions des lecteurs";
    return deps.sendMail({ to: email, subject: "Ton code Onrecord : " + code, text: text })
      .catch(function () { throw fail(502, "L'e-mail n'a pas pu partir. Réessaie plus tard."); })
      .then(function () { return Promise.all([mark(store, "rl/send/" + eh), mark(store, "rl/ip/" + iph), sweep(store, now)]); })
      .then(function () { return { status: 200, body: { ok: true, challenge: challenge, expires_in: CODE_TTL / 1000 } }; });
  });
}

function verifyCode(body, req, deps) {
  var env = deps.env, now = deps.now(), store = deps.store;
  requireEnabled(env);
  var ch = unsign(env.SESSION_SECRET, body.challenge);
  if (!ch || ch.k !== "c") throw fail(400, "Demande un nouveau code.");
  if (!(ch.x > now)) throw fail(400, "Ce code a expiré. Demande un nouveau code.");
  var code = str(body.code, 12).replace(/\s+/g, "");
  if (!/^\d{6}$/.test(code)) throw fail(400, "Le code a six chiffres.");
  var pseudo = checkPseudo(body.pseudo);
  return Promise.all([countSince(store, "rl/fail/" + ch.n, 0), countSince(store, "rl/used/" + ch.n, 0)]).then(function (n) {
    if (n[1] > 0) throw fail(400, "Ce code a déjà servi. Demande un nouveau code.");
    if (n[0] >= 5) throw fail(429, "Trop d'essais. Demande un nouveau code.");
    var want = hhex(env.SESSION_SECRET, "code:" + ch.n + ":" + ch.eh + ":" + code, 64);
    if (!safeEq(want, ch.h)) {
      return mark(store, "rl/fail/" + ch.n).then(function () {
        throw fail(400, "Code incorrect. Il te reste " + Math.max(0, 4 - n[0]) + " essai(s).");
      });
    }
    return mark(store, "rl/used/" + ch.n).then(function () {
      var tok = sign(env.SESSION_SECRET, { k: "s", eh: ch.eh, ee: ch.ee, p: pseudo, x: now + SESSION_TTL });
      return { status: 200, body: { ok: true, pseudo: pseudo }, headers: { "Set-Cookie": cookieFor(tok, SESSION_TTL / 1000) } };
    });
  });
}

function me(req, deps) {
  var s = sessionFrom(req, deps.env, deps.now());
  return { status: 200, body: { logged: !!s, pseudo: s ? s.p : null, enabled: config(deps.env).enabled } };
}
function logout() {
  return { status: 200, body: { ok: true }, headers: { "Set-Cookie": COOKIE + "=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0" } };
}

/* Règle d'envoi d'un fichier (appelée avant de délivrer un jeton d'envoi Blob). */
function uploadPolicy(pathname, clientPayload, req, deps) {
  return Promise.resolve().then(function () { return uploadPolicySync(pathname, clientPayload, req, deps); });
}
function uploadPolicySync(pathname, clientPayload, req, deps) {
  var env = deps.env, now = deps.now();
  requireEnabled(env);
  var s = sessionFrom(req, env, now);
  if (!s) throw fail(401, "Connecte-toi d'abord.");
  var kind = clientPayload === "video" ? "video" : "image";
  if (!/^uploads\/[a-z0-9][a-z0-9._-]{0,120}$/i.test(String(pathname || ""))) throw fail(400, "Nom de fichier refusé.");
  return countSince(deps.store, "rl/up/" + s.eh, now - 86400000).then(function (n) {
    if (n >= 20) throw fail(429, "Limite d'envois du jour atteinte.");
    return mark(deps.store, "rl/up/" + s.eh).then(function () {
      return {
        allowedContentTypes: kind === "video" ? VIDEO_TYPES : IMAGE_TYPES,
        maximumSizeInBytes: kind === "video" ? VIDEO_MAX : IMAGE_MAX,
        addRandomSuffix: true,
        tokenPayload: JSON.stringify({ eh: s.eh, kind: kind })
      };
    });
  });
}

function submit(body, req, deps) {
  var env = deps.env, now = deps.now(), store = deps.store;
  requireEnabled(env);
  var s = sessionFrom(req, env, now);
  if (!s) throw fail(401, "Connecte-toi d'abord.");
  if (body.certify !== true) throw fail(400, "Coche la case : tu certifies que ta contribution respecte la charte.");
  var person = str(body.person, 100);
  if (!/^[a-z0-9][a-z0-9-]{0,99}$/.test(person)) throw fail(400, "Choisis une fiche.");
  if (deps.personExists && !deps.personExists(person)) throw fail(400, "Cette fiche n'existe pas.");
  var title = str(body.title, 200).replace(/\s+/g, " ");
  var text = str(body.text, 4000).replace(/\r\n?/g, "\n").replace(/\n{3,}/g, "\n\n");
  if (title.length < 3 || title.length > 120) throw fail(400, "Le titre fait entre 3 et 120 caractères.");
  if (text.length < 20 || text.length > 3000) throw fail(400, "Le texte fait entre 20 et 3 000 caractères.");
  var eventDate = str(body.event_date, 10);
  if (eventDate) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(eventDate) || isNaN(Date.parse(eventDate + "T00:00:00Z"))) throw fail(400, "Date des faits invalide.");
    if (Date.parse(eventDate + "T00:00:00Z") > now + 86400000) throw fail(400, "La date des faits est dans le futur.");
  }
  var links = (Array.isArray(body.links) ? body.links : []).map(function (u) { return str(u, 600); }).filter(Boolean);
  if (links.length > 6) throw fail(400, "Six liens au plus.");
  var clean = links.map(httpsUrl);
  if (clean.some(function (u) { return !u; })) throw fail(400, "Chaque lien doit commencer par https://");
  var media = Array.isArray(body.media) ? body.media : [];
  if (media.length > 4) throw fail(400, "Quatre fichiers au plus.");
  media = media.map(function (m) {
    var url = str(m && m.url, 600), kind = m && m.kind === "video" ? "video" : "image";
    if (!isOurMedia(url)) throw fail(400, "Fichier refusé : il doit être envoyé par le formulaire.");
    return { url: url, kind: kind };
  });
  if (!clean.length && !media.length) throw fail(400, "Ajoute au moins une preuve : un lien ou un fichier.");
  return countSince(store, "rl/sub/" + s.eh, now - 86400000).then(function (n) {
    if (n >= 5) throw fail(429, "Cinq contributions par jour au plus.");
    var id = newId(now);
    var all = title + "\n" + text;
    var item = {
      id: id, person: person, pseudo: s.p, eh: s.eh, ee: s.ee,
      submitted: new Date(now).toISOString(), event_date: eventDate || null,
      title: title, text: text, links: clean, media: media,
      flags: { forbidden: forbiddenIn(all), private: privateHints(all) }
    };
    return store.put("contrib/pending/" + id + ".json", item).then(function () { return mark(store, "rl/sub/" + s.eh); })
      .then(function () { return { status: 200, body: { ok: true, id: id } }; });
  });
}

function report(body, req, deps) {
  var env = deps.env, now = deps.now(), store = deps.store, c = config(env);
  if (!c.reports) throw fail(503, "Le signalement arrive bientôt.", { soon: true });
  var id = str(body.id, 60);
  if (!/^[a-z0-9]{6,60}$/.test(id)) throw fail(400, "Contribution inconnue.");
  var kind = REPORT_KINDS.indexOf(body.kind) >= 0 ? body.kind : "autre";
  var reason = str(body.reason, 2000);
  if (reason.length < 5) throw fail(400, "Explique en quelques mots ce qui pose problème.");
  var contact = normEmail(body.contact || "");
  if (contact && !EMAIL_RE.test(contact)) throw fail(400, "Adresse de contact invalide.");
  var iph = hhex(env.SESSION_SECRET, "ip:" + (req.ip || "?"), 20);
  return countSince(store, "rl/rep/" + iph, now - 3600000).then(function (n) {
    if (n >= 10) throw fail(429, "Trop de signalements depuis ce réseau. Réessaie dans une heure.");
    var rid = newId(now);
    return store.put("contrib/reports/" + rid + ".json", {
      rid: rid, id: id, kind: kind, reason: reason, contact_enc: contact ? encrypt(env.SESSION_SECRET, contact) : "",
      at: new Date(now).toISOString()
    }).then(function () { return mark(store, "rl/rep/" + iph); })
      .then(function () { return { status: 200, body: { ok: true } }; });
  });
}

/* ---------- administration ---------- */
/* L'admin envoie le jeton GitHub qu'elle a déjà collé dans /admin.html.
   On vérifie côté serveur qu'il ouvre le dépôt en écriture. Aucun secret de plus. */
var ADMIN_CACHE = new Map();
function adminCheck(req, deps) {
  var auth = String((req.headers && (req.headers.authorization || req.headers.Authorization)) || "");
  var tok = /^Bearer\s+(\S{20,})$/.exec(auth);
  if (!tok) return Promise.reject(fail(401, "Jeton GitHub manquant."));
  tok = tok[1];
  var key = crypto.createHash("sha256").update(tok).digest("hex"), hit = ADMIN_CACHE.get(key), now = deps.now();
  if (hit && hit > now) return Promise.resolve(tok);
  return deps.github("GET", "/repos/" + OWNER + "/" + REPO, tok).then(function (r) {
    if (r.status !== 200 || !r.body || !r.body.permissions || !r.body.permissions.push) throw fail(403, "Ce jeton n'a pas l'écriture sur le dépôt.");
    ADMIN_CACHE.set(key, now + 5 * 60000);
    return tok;
  });
}
function readAll(store, prefix) {
  return store.list(prefix).then(function (xs) {
    return Promise.all(xs.map(function (x) { return store.read(x).then(function (b) { return b ? { meta: x, body: b } : null; }); }));
  }).then(function (xs) { return xs.filter(Boolean); });
}
function findPending(store, id) {
  if (!/^[a-z0-9]{6,60}$/.test(String(id || ""))) return Promise.reject(fail(400, "Identifiant invalide."));
  return readAll(store, "contrib/pending/" + id).then(function (xs) {
    var x = xs.find(function (y) { return y.body.id === id; });
    if (!x) throw fail(404, "Contribution introuvable (déjà traitée ?).");
    return x;
  });
}
function publicItem(p, now) {
  return {
    id: p.id, person: p.person, pseudo: p.pseudo, submitted: p.submitted, approved: new Date(now).toISOString(),
    event_date: p.event_date || null, title: p.title, text: p.text, links: p.links || [], media: p.media || []
  };
}
function readPublished(deps, tok) {
  return deps.github("GET", "/repos/" + OWNER + "/" + REPO + "/contents/" + PUBLISHED_PATH + "?ref=main", tok).then(function (r) {
    if (r.status === 404) return { sha: null, data: { items: [] } };
    if (r.status !== 200) throw fail(502, "Lecture de contributions.json impossible (GitHub " + r.status + ").");
    var data = JSON.parse(Buffer.from(r.body.content || "", "base64").toString("utf8") || "{}");
    if (!Array.isArray(data.items)) data.items = [];
    return { sha: r.body.sha, data: data };
  });
}
function writePublished(deps, tok, change, message) {
  function attempt(left) {
    return readPublished(deps, tok).then(function (cur) {
      var data = change(cur.data);
      data.items.sort(function (a, b) { return String(b.submitted).localeCompare(String(a.submitted)); });
      var content = Buffer.from(JSON.stringify(data, null, 1) + "\n", "utf8").toString("base64");
      var payload = { message: message, content: content, branch: "main" };
      if (cur.sha) payload.sha = cur.sha;
      return deps.github("PUT", "/repos/" + OWNER + "/" + REPO + "/contents/" + PUBLISHED_PATH, tok, payload).then(function (r) {
        if ((r.status === 409 || r.status === 422) && left > 0) return attempt(left - 1);
        if (r.status !== 200 && r.status !== 201) throw fail(502, "Écriture sur GitHub refusée (" + r.status + ").");
        return { commit: r.body && r.body.commit && r.body.commit.sha, count: data.items.length };
      });
    });
  }
  return attempt(2);
}

function admin(body, req, deps) {
  var env = deps.env, store = deps.store, now = deps.now(), c = config(env);
  return adminCheck(req, deps).then(function (tok) {
    var op = String(body.op || "list");
    if (!c.storage || !c.secret) {
      if (op !== "list" && op !== "unpublish") throw fail(503, "Stockage ou SESSION_SECRET absent dans Vercel.");
    }
    if (op === "list") {
      var pend = c.storage ? readAll(store, "contrib/pending/") : Promise.resolve([]);
      var reps = c.storage ? readAll(store, "contrib/reports/") : Promise.resolve([]);
      return Promise.all([pend, reps, readPublished(deps, tok)]).then(function (r) {
        return { status: 200, body: {
          status: status(env),
          pending: r[0].map(function (x) {
            var b = Object.assign({}, x.body); b.email = c.secret ? decrypt(env.SESSION_SECRET, b.ee) : ""; delete b.ee; delete b.eh; return b;
          }).sort(function (a, b) { return String(a.submitted).localeCompare(String(b.submitted)); }),
          reports: r[1].map(function (x) {
            var b = Object.assign({}, x.body); b.contact = b.contact_enc && c.secret ? decrypt(env.SESSION_SECRET, b.contact_enc) : ""; delete b.contact_enc; return b;
          }).sort(function (a, b) { return String(b.at).localeCompare(String(a.at)); }),
          published: r[2].data.items
        } };
      });
    }
    if (op === "approve") {
      return findPending(store, body.id).then(function (x) {
        var item = publicItem(x.body, now);
        return writePublished(deps, tok, function (data) {
          data.items = data.items.filter(function (i) { return i.id !== item.id; });
          data.items.push(item);
          return data;
        }, "contributions: publication " + item.id).then(function (w) {
          /* trace privée gardée pour la LCEN (identification de l'auteur sur réquisition) */
          return store.put("contrib/archive/" + item.id + ".json", Object.assign({}, x.body, { approved: item.approved }))
            .then(function () { return store.del([x.meta.url]); })
            .then(function () { return { status: 200, body: { ok: true, commit: w.commit, item: item } }; });
        });
      });
    }
    if (op === "reject") {
      return findPending(store, body.id).then(function (x) {
        var urls = (x.body.media || []).map(function (m) { return m.url; });
        return store.del(urls.concat([x.meta.url])).then(function () { return { status: 200, body: { ok: true } }; });
      });
    }
    if (op === "unpublish") {
      var id = String(body.id || "");
      if (!/^[a-z0-9]{6,60}$/.test(id)) throw fail(400, "Identifiant invalide.");
      var removed = null;
      return writePublished(deps, tok, function (data) {
        removed = data.items.find(function (i) { return i.id === id; }) || null;
        data.items = data.items.filter(function (i) { return i.id !== id; });
        return data;
      }, "contributions: retrait " + id).then(function (w) {
        if (!removed) throw fail(404, "Déjà retirée.");
        var urls = (removed.media || []).map(function (m) { return m.url; }).filter(isOurMedia);
        return (c.storage ? store.del(urls) : Promise.resolve()).then(function () { return { status: 200, body: { ok: true, commit: w.commit } }; });
      });
    }
    if (op === "dismiss") {
      var rid = String(body.rid || "");
      if (!/^[a-z0-9]{6,60}$/.test(rid)) throw fail(400, "Identifiant invalide.");
      return store.list("contrib/reports/" + rid).then(function (xs) {
        return store.del(xs.map(function (x) { return x.url; }));
      }).then(function () { return { status: 200, body: { ok: true } }; });
    }
    throw fail(400, "Opération inconnue.");
  });
}

/* ---------- point d'entrée ---------- */
function handle(action, req, deps) {
  var body = req.body && typeof req.body === "object" ? req.body : {};
  return Promise.resolve().then(function () {
    if (action === "status") return { status: 200, body: status(deps.env) };
    if (action === "me") return me(req, deps);
    if (req.method !== "POST") throw fail(405, "Méthode non acceptée.");
    if (action === "send-code") return sendCode(body, req, deps);
    if (action === "verify") return verifyCode(body, req, deps);
    if (action === "logout") return logout();
    if (action === "submit") return submit(body, req, deps);
    if (action === "report") return report(body, req, deps);
    if (action === "admin") return admin(body, req, deps);
    throw fail(404, "Action inconnue.");
  }).catch(function (e) {
    if (e && e.status) return { status: e.status, body: Object.assign({ ok: false, error: e.message }, e.extra || {}) };
    console.error("contrib", action, e);
    return { status: 500, body: { ok: false, error: "Erreur interne. Réessaie plus tard." } };
  });
}

module.exports = {
  handle: handle, uploadPolicy: uploadPolicy, status: status, config: config,
  isDisposable: isDisposable, forbiddenIn: forbiddenIn, privateHints: privateHints, checkPseudo: checkPseudo,
  sessionFrom: sessionFrom, encrypt: encrypt, decrypt: decrypt, sign: sign, unsign: unsign,
  IMAGE_MAX: IMAGE_MAX, VIDEO_MAX: VIDEO_MAX, IMAGE_TYPES: IMAGE_TYPES, VIDEO_TYPES: VIDEO_TYPES, OWNER: OWNER, REPO: REPO
};
