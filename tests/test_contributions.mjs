// Contributions des lecteurs : node --test tests/test_contributions.mjs
// Sans réseau : stockage en mémoire, e-mail et GitHub simulés.
import test from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const core = require("../lib/contrib/core.js");
const { memoryStore } = require("../lib/contrib/store.js");

const ENV = { BLOB_READ_WRITE_TOKEN: "vercel_blob_rw_test", SESSION_SECRET: "test-secret-0123456789abcdef", RESEND_API_KEY: "re_test" };
const GOOD_TOKEN = "github_pat_" + "x".repeat(30);

function setup(env = ENV) {
  let t = Date.UTC(2026, 10, 22, 20, 0, 0);
  const mails = [];
  const files = {}; // dépôt GitHub simulé
  let sha = 0;
  const deps = {
    env, now: () => t, store: memoryStore(() => t),
    sendMail: async (m) => { mails.push(m); },
    domainOk: async (d) => d !== "nexiste-pas.example",
    personExists: (id) => ["jordan-bardella", "marine-le-pen"].includes(id),
    github: async (method, path, tok, payload) => {
      if (tok !== GOOD_TOKEN) return { status: 401, body: {} };
      if (method === "GET" && /\/repos\/[^/]+\/[^/]+$/.test(path)) return { status: 200, body: { permissions: { push: true } } };
      const m = /\/contents\/([^?]+)/.exec(path);
      if (method === "GET" && m) return files[m[1]] ? { status: 200, body: { sha: files[m[1]].sha, content: files[m[1]].content } } : { status: 404, body: {} };
      if (method === "PUT" && m) {
        if (files[m[1]] && payload.sha !== files[m[1]].sha) return { status: 409, body: {} };
        files[m[1]] = { sha: "s" + (++sha), content: payload.content };
        return { status: 200, body: { commit: { sha: "c" + sha } } };
      }
      return { status: 404, body: {} };
    }
  };
  return { deps, mails, files, tick: (ms) => { t += ms; }, published: () => JSON.parse(Buffer.from(files["contributions.json"].content, "base64").toString()) };
}
const req = (body, extra = {}) => ({ method: "POST", body, headers: extra.headers || {}, ip: extra.ip || "1.2.3.4" });
const codeOf = (mail) => /(\d{6})/.exec(mail.subject)[1];
function cookieFrom(out) { return out.headers["Set-Cookie"].split(";")[0]; }

async function login(s, email = "lecteur@gmail.com", pseudo = "Lecteur_75") {
  const a = await core.handle("send-code", req({ email, charter: true }), s.deps);
  assert.equal(a.status, 200, JSON.stringify(a.body));
  const b = await core.handle("verify", req({ challenge: a.body.challenge, code: codeOf(s.mails.at(-1)), pseudo }), s.deps);
  assert.equal(b.status, 200, JSON.stringify(b.body));
  return cookieFrom(b);
}

test("adresses jetables refusées, sous-domaines compris", () => {
  assert.equal(core.isDisposable("a@yopmail.com"), true);
  assert.equal(core.isDisposable("a@mailinator.com"), true);
  assert.equal(core.isDisposable("a@x.mailinator.com"), true);
  assert.equal(core.isDisposable("a@gmail.com"), false);
  assert.equal(core.isDisposable("a@orange.fr"), false);
});

test("sans variables d'environnement : bientôt disponible, pas de plantage", async () => {
  const s = setup({});
  const st = await core.handle("status", { method: "GET", headers: {} }, s.deps);
  assert.equal(st.status, 200);
  assert.equal(st.body.enabled, false);
  const r = await core.handle("send-code", req({ email: "a@gmail.com", charter: true }), s.deps);
  assert.equal(r.status, 503);
  assert.equal(r.body.soon, true);
  const sub = await core.handle("submit", req({}), s.deps);
  assert.equal(sub.status, 503);
  const rep = await core.handle("report", req({ id: "abcdef12", reason: "faux" }), s.deps);
  assert.equal(rep.status, 503);
  const me = await core.handle("me", { method: "GET", headers: {} }, s.deps);
  assert.equal(me.body.logged, false);
});

test("envoi du code : charte, jetable, domaine, débit", async () => {
  const s = setup();
  assert.equal((await core.handle("send-code", req({ email: "a@gmail.com" }), s.deps)).status, 400);
  const j = await core.handle("send-code", req({ email: "a@yopmail.com", charter: true }), s.deps);
  assert.equal(j.status, 400); assert.match(j.body.error, /jetables/);
  assert.equal((await core.handle("send-code", req({ email: "a@nexiste-pas.example", charter: true }), s.deps)).status, 400);
  assert.equal((await core.handle("send-code", req({ email: "pas-une-adresse", charter: true }), s.deps)).status, 400);
  const ok = await core.handle("send-code", req({ email: "A@Gmail.com ", charter: true }), s.deps);
  assert.equal(ok.status, 200);
  assert.equal(s.mails.length, 1); assert.equal(s.mails[0].to, "a@gmail.com");
  assert.ok(!ok.body.challenge.includes("gmail"), "l'adresse n'apparaît pas en clair dans le défi");
  assert.equal((await core.handle("send-code", req({ email: "a@gmail.com", charter: true }), s.deps)).status, 429, "une minute entre deux codes");
  for (let i = 0; i < 4; i++) { s.tick(61000); assert.equal((await core.handle("send-code", req({ email: "a@gmail.com", charter: true }), s.deps)).status, 200); }
  s.tick(61000);
  assert.equal((await core.handle("send-code", req({ email: "a@gmail.com", charter: true }), s.deps)).status, 429, "cinq par heure");
});

test("vérification : mauvais code, cinq essais, expiration, usage unique", async () => {
  const s = setup();
  const a = await core.handle("send-code", req({ email: "b@gmail.com", charter: true }), s.deps);
  const good = codeOf(s.mails[0]);
  const bad = good === "000000" ? "111111" : "000000";
  const w = await core.handle("verify", req({ challenge: a.body.challenge, code: bad, pseudo: "Bob" }), s.deps);
  assert.equal(w.status, 400); assert.match(w.body.error, /incorrect/);
  assert.equal((await core.handle("verify", req({ challenge: a.body.challenge, code: good, pseudo: "x" }), s.deps)).status, 400, "pseudo trop court");
  assert.equal((await core.handle("verify", req({ challenge: a.body.challenge, code: good, pseudo: "Le pantin" }), s.deps)).status, 400, "mot interdit dans le pseudo");
  const ok = await core.handle("verify", req({ challenge: a.body.challenge, code: good, pseudo: "Bob 13" }), s.deps);
  assert.equal(ok.status, 200);
  assert.match(ok.headers["Set-Cookie"], /HttpOnly; Secure; SameSite=Lax/);
  assert.equal((await core.handle("verify", req({ challenge: a.body.challenge, code: good, pseudo: "Bob 13" }), s.deps)).status, 400, "usage unique");
  const me = await core.handle("me", { method: "GET", headers: { cookie: cookieFrom(ok) } }, s.deps);
  assert.equal(me.body.logged, true); assert.equal(me.body.pseudo, "Bob 13");

  s.tick(120000);
  const c = await core.handle("send-code", req({ email: "c@gmail.com", charter: true }), s.deps);
  for (let i = 0; i < 5; i++) await core.handle("verify", req({ challenge: c.body.challenge, code: bad, pseudo: "Cid" }), s.deps);
  const locked = await core.handle("verify", req({ challenge: c.body.challenge, code: codeOf(s.mails.at(-1)), pseudo: "Cid" }), s.deps);
  assert.equal(locked.status, 429);

  const d = await core.handle("send-code", req({ email: "d@gmail.com", charter: true }), s.deps);
  s.tick(16 * 60000);
  const exp = await core.handle("verify", req({ challenge: d.body.challenge, code: codeOf(s.mails.at(-1)), pseudo: "Dan" }), s.deps);
  assert.equal(exp.status, 400); assert.match(exp.body.error, /expiré/);

  const forged = await core.handle("verify", req({ challenge: c.body.challenge.replace(/.$/, "A"), code: "123456", pseudo: "Cid" }), s.deps);
  assert.equal(forged.status, 400);
});

test("dépôt : connexion, preuve, fichiers du formulaire seulement, drapeaux", async () => {
  const s = setup();
  const anon = await core.handle("submit", req({ certify: true }), s.deps);
  assert.equal(anon.status, 401);
  const cookie = await login(s);
  const H = { headers: { cookie } };
  const base = { person: "jordan-bardella", title: "Vidéo du meeting", text: "Extrait public du meeting du 20 novembre, compte officiel du parti.", certify: true };
  assert.equal((await core.handle("submit", req({ ...base, certify: false }, H), s.deps)).status, 400);
  assert.equal((await core.handle("submit", req({ ...base, person: "inconnu" }, H), s.deps)).status, 400);
  assert.equal((await core.handle("submit", req(base, H), s.deps)).status, 400, "il faut une preuve");
  assert.equal((await core.handle("submit", req({ ...base, links: ["http://exemple.fr"] }, H), s.deps)).status, 400, "https seulement");
  assert.equal((await core.handle("submit", req({ ...base, media: [{ url: "https://evil.example/x.png", kind: "image" }] }, H), s.deps)).status, 400);
  const ok = await core.handle("submit", req({ ...base, text: base.text + " C'est un pantin. Tél. 06 12 34 56 78", links: ["https://www.youtube.com/watch?v=abc"],
    media: [{ url: "https://abc.public.blob.vercel-storage.com/uploads/x-AbC.jpg", kind: "image" }] }, H), s.deps);
  assert.equal(ok.status, 200, JSON.stringify(ok.body));
  const pend = s.deps.store.items.filter((i) => i.pathname.startsWith("contrib/pending/"));
  assert.equal(pend.length, 1);
  const stored = JSON.parse(pend[0].body);
  assert.deepEqual(stored.flags.forbidden, ["pantin"]);
  assert.deepEqual(stored.flags.private, ["numéro de téléphone"]);
  assert.ok(!pend[0].body.includes("lecteur@gmail.com"), "e-mail chiffré dans la file");
  assert.equal(stored.submitted, "2026-11-22T20:00:00.000Z");
  for (let i = 0; i < 4; i++) assert.equal((await core.handle("submit", req({ ...base, links: ["https://a.fr/" + i] }, H), s.deps)).status, 200);
  assert.equal((await core.handle("submit", req({ ...base, links: ["https://a.fr/z"] }, H), s.deps)).status, 429, "cinq par jour");
});

test("envoi de fichiers : session obligatoire, types et tailles", async () => {
  const s = setup();
  await assert.rejects(core.uploadPolicy("uploads/a.jpg", "image", req({}), s.deps), (e) => e.status === 401);
  const cookie = await login(s);
  const img = await core.uploadPolicy("uploads/a.jpg", "image", req({}, { headers: { cookie } }), s.deps);
  assert.equal(img.maximumSizeInBytes, 5 * 1024 * 1024);
  assert.ok(!img.allowedContentTypes.includes("video/mp4"));
  const vid = await core.uploadPolicy("uploads/b.mp4", "video", req({}, { headers: { cookie } }), s.deps);
  assert.equal(vid.maximumSizeInBytes, 50 * 1024 * 1024);
  assert.ok(vid.allowedContentTypes.includes("video/mp4"));
  await assert.rejects(core.uploadPolicy("../etc/passwd", "image", req({}, { headers: { cookie } }), s.deps), (e) => e.status === 400);
});

test("modération : jeton vérifié, publier, refuser, retirer, signalement", async () => {
  const s = setup();
  const cookie = await login(s);
  const H = { headers: { cookie } };
  const mk = (title) => core.handle("submit", req({ person: "marine-le-pen", title, text: "Un fait public daté, avec une source ouverte à tous.", links: ["https://www.lemonde.fr/x"], certify: true }, H), s.deps);
  const a = await mk("Premier"); s.tick(1000); const b = await mk("Second");
  const admin = (body, tok = GOOD_TOKEN) => core.handle("admin", req(body, { headers: { authorization: "Bearer " + tok } }), s.deps);

  assert.equal((await core.handle("admin", req({ op: "list" }), s.deps)).status, 401);
  assert.equal((await admin({ op: "list" }, "github_pat_" + "y".repeat(30))).status, 403);
  const list = await admin({ op: "list" });
  assert.equal(list.status, 200);
  assert.equal(list.body.pending.length, 2);
  assert.equal(list.body.pending[0].email, "lecteur@gmail.com", "l'admin voit l'e-mail");
  assert.equal(list.body.published.length, 0);

  const ap = await admin({ op: "approve", id: a.body.id });
  assert.equal(ap.status, 200, JSON.stringify(ap.body));
  const pub = s.published();
  assert.equal(pub.items.length, 1);
  assert.equal(pub.items[0].pseudo, "Lecteur_75");
  assert.equal(JSON.stringify(pub).includes("gmail"), false, "jamais l'e-mail en public");
  assert.equal(pub.items[0].ee, undefined);
  assert.equal(s.deps.store.items.filter((i) => i.pathname.startsWith("contrib/archive/")).length, 1, "trace LCEN gardée");
  assert.equal((await admin({ op: "approve", id: a.body.id })).status, 404, "déjà traitée");

  assert.equal((await admin({ op: "reject", id: b.body.id })).status, 200);
  assert.equal((await admin({ op: "list" })).body.pending.length, 0);

  const rep = await core.handle("report", req({ id: a.body.id, kind: "prive", reason: "Donne le nom d'un enfant.", contact: "plaignant@orange.fr" }), s.deps);
  assert.equal(rep.status, 200);
  const l2 = await admin({ op: "list" });
  assert.equal(l2.body.reports.length, 1);
  assert.equal(l2.body.reports[0].contact, "plaignant@orange.fr");
  assert.equal((await admin({ op: "unpublish", id: a.body.id })).status, 200);
  assert.equal(s.published().items.length, 0);
  assert.equal((await admin({ op: "dismiss", rid: l2.body.reports[0].rid })).status, 200);
  assert.equal((await admin({ op: "list" })).body.reports.length, 0);
});

test("fonction Vercel sans variables : répond proprement", async () => {
  const saved = { ...process.env };
  for (const k of ["BLOB_READ_WRITE_TOKEN", "SESSION_SECRET", "RESEND_API_KEY", "BREVO_API_KEY", "MAIL_FROM"]) delete process.env[k];
  const handler = require("../api/contrib/[action].js");
  function res() {
    const r = { headers: {}, code: 0, out: null };
    r.setHeader = (k, v) => { r.headers[k] = v; };
    r.status = (c) => { r.code = c; return r; };
    r.json = (b) => { r.out = b; return r; };
    return r;
  }
  for (const [action, method, code] of [["status", "GET", 200], ["me", "GET", 200], ["send-code", "POST", 503], ["upload", "POST", 503], ["submit", "POST", 503], ["inconnue", "POST", 404]]) {
    const r = res();
    await handler({ method, query: { action }, headers: { "content-type": "application/json" }, body: { email: "a@gmail.com", charter: true } }, r);
    assert.equal(r.code, code, action + " " + JSON.stringify(r.out));
    assert.equal(r.headers["Cache-Control"], "no-store");
  }
  Object.assign(process.env, saved);
});
