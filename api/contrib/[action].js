/* Fonction Vercel unique pour les contributions : /api/contrib/<action>.
   Sans les variables d'environnement, elle répond « bientôt disponible » (503) sans planter.
   Logique : lib/contrib/core.js. Mode d'emploi : docs/REPRISE.md, section 14. */
"use strict";
var fs = require("fs");
var path = require("path");
var dns = require("dns");
var core = require("../../lib/contrib/core.js");
var storeLib = require("../../lib/contrib/store.js");

var PERSONS = null;
function personExists(id) {
  if (PERSONS === null) {
    try {
      var d = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "..", "data.json"), "utf8"));
      PERSONS = new Set((d.nodes || []).map(function (n) { return n.id; }));
    } catch (e) { PERSONS = false; }
  }
  return PERSONS ? PERSONS.has(id) : true;
}

function domainOk(domain) {
  var timer;
  var t = new Promise(function (res) { timer = setTimeout(function () { res(true); }, 3000); });
  var q = dns.promises.resolveMx(domain).then(function (mx) { return mx.length > 0; }, function (e) {
    if (e && e.code === "ENOTFOUND") return false;
    if (e && e.code === "ENODATA") return dns.promises.resolve4(domain).then(function (a) { return a.length > 0; }, function () { return false; });
    return true;
  });
  return Promise.race([q, t]).then(function (v) { clearTimeout(timer); return v; });
}

function parseFrom(from) {
  var m = /^\s*(.*?)\s*<([^>]+)>\s*$/.exec(from || "");
  return m ? { name: m[1] || "Onrecord", email: m[2] } : { name: "Onrecord", email: String(from || "").trim() };
}

function sendMail(env) {
  var cfg = core.config(env);
  return function (msg) {
    if (cfg.mail === "resend") {
      return fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { Authorization: "Bearer " + env.RESEND_API_KEY, "Content-Type": "application/json" },
        body: JSON.stringify({ from: cfg.from, to: [msg.to], subject: msg.subject, text: msg.text })
      }).then(function (r) { if (!r.ok) return r.text().then(function (t) { throw new Error("resend " + r.status + " " + t.slice(0, 200)); }); });
    }
    var f = parseFrom(cfg.from);
    return fetch("https://api.brevo.com/v3/smtp/email", {
      method: "POST",
      headers: { "api-key": env.BREVO_API_KEY, "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ sender: f, to: [{ email: msg.to }], subject: msg.subject, textContent: msg.text })
    }).then(function (r) { if (!r.ok) return r.text().then(function (t) { throw new Error("brevo " + r.status + " " + t.slice(0, 200)); }); });
  };
}

function github(method, p, token, payload) {
  return fetch("https://api.github.com" + p, {
    method: method,
    headers: {
      Authorization: "Bearer " + token, Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "onrecord-contributions",
      "Content-Type": "application/json"
    },
    body: payload ? JSON.stringify(payload) : undefined
  }).then(function (r) {
    return r.text().then(function (t) { var b = null; try { b = t ? JSON.parse(t) : null; } catch (e) {} return { status: r.status, body: b }; });
  });
}

function send(res, out) {
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("X-Robots-Tag", "noindex");
  Object.keys(out.headers || {}).forEach(function (k) { res.setHeader(k, out.headers[k]); });
  res.status(out.status).json(out.body);
}

module.exports = async function (req, res) {
  var env = process.env;
  var action = String((req.query && req.query.action) || "");
  var ip = String(req.headers["x-forwarded-for"] || req.headers["x-real-ip"] || "").split(",")[0].trim();
  if (req.method === "POST" && !/application\/json/i.test(String(req.headers["content-type"] || ""))) {
    return send(res, { status: 415, body: { ok: false, error: "JSON attendu." } });
  }
  var cfg = core.config(env);
  var deps = {
    env: env, now: Date.now, store: cfg.storage ? storeLib.blobStore() : null,
    sendMail: sendMail(env), domainOk: domainOk, github: github, personExists: personExists
  };
  var r = { method: req.method, body: req.body, headers: req.headers, ip: ip };

  if (action === "upload") {
    if (!cfg.enabled) return send(res, { status: 503, body: { ok: false, soon: true, error: "Les contributions arrivent bientôt." } });
    var body = req.body || {};
    if (req.method !== "POST" || body.type !== "blob.generate-client-token") {
      return send(res, { status: 400, body: { ok: false, error: "Requête d'envoi invalide." } });
    }
    try {
      var client = require("@vercel/blob/client");
      var json = await client.handleUpload({
        body: body, request: req,
        onBeforeGenerateToken: function (pathname, clientPayload) { return core.uploadPolicy(pathname, clientPayload, r, deps); }
      });
      return send(res, { status: 200, body: json });
    } catch (e) {
      return send(res, { status: e.status || 400, body: { ok: false, error: e.status ? e.message : "Envoi refusé." } });
    }
  }
  var out = await core.handle(action, r, deps);
  return send(res, out);
};
