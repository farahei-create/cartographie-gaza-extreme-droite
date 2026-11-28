/* Déclencheur fiable du relevé automatique (Vercel Cron, voir vercel.json).
   Les crons GitHub partent souvent avec des heures de retard : Vercel appelle cette
   fonction à heure fixe, et elle lance le workflow « Relevé du matin » sur GitHub
   (workflow_dispatch) avec le créneau matin ou soir. Le workflow ne republie jamais
   un créneau déjà couvert.
   Variables d'environnement Vercel :
   - GITHUB_DISPATCH_TOKEN (obligatoire) : jeton GitHub fine-grained limité au dépôt,
     permission « Actions : Read and write ».
   - CRON_SECRET (conseillé) : Vercel l'envoie tout seul à ses crons ; sans lui,
     n'importe qui pourrait appeler l'adresse (sans danger : créneau déjà couvert = rien). */
"use strict";

var OWNER = "farahei-create";
var REPO = "cartographie-gaza-extreme-droite";
var WORKFLOW = "daily-update.yml";

module.exports = async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  var secret = process.env.CRON_SECRET || "";
  if (secret && (req.headers.authorization || "") !== "Bearer " + secret) {
    res.status(401).json({ ok: false, error: "non autorisé" });
    return;
  }
  var token = process.env.GITHUB_DISPATCH_TOKEN || "";
  if (!token) {
    res.status(503).json({ ok: false, error: "GITHUB_DISPATCH_TOKEN manquant dans Vercel" });
    return;
  }
  var q = (req.query && req.query.slot) || "";
  var slot = q === "soir" || q === "matin" ? q : (new Date().getUTCHours() < 12 ? "matin" : "soir");
  try {
    var r = await fetch("https://api.github.com/repos/" + OWNER + "/" + REPO + "/actions/workflows/" + WORKFLOW + "/dispatches", {
      method: "POST",
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: "Bearer " + token,
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "onrecord-cron"
      },
      body: JSON.stringify({ ref: "main", inputs: { slot: slot } })
    });
    if (r.status === 204) { res.status(200).json({ ok: true, slot: slot }); return; }
    var text = (await r.text()).slice(0, 300);
    res.status(502).json({ ok: false, slot: slot, status: r.status, error: text });
  } catch (e) {
    res.status(502).json({ ok: false, slot: slot, error: String(e && e.message || e) });
  }
};
