/* Service worker : coque de l'application + données + images disponibles hors ligne.
   - data.json et config.js : réseau d'abord (données à jour), cache en secours ;
   - pages (navigation) : réseau d'abord, index.html en cache en secours ;
   - autres fichiers du site : cache, puis mise à jour en arrière-plan.
   Les requêtes vers d'autres domaines (sources, YouTube, archives) ne sont pas interceptées. */
var VERSION = "onrecord-v25";
var SHELL = [
  "./", "index.html", "style.css", "app.js", "config.js", "data.json", "manifest.webmanifest",
  "vendor/vis-network.min.js",
  "icons/favicon-64.png", "icons/apple-touch-icon.png", "icons/icon-192.png", "icons/icon-512.png",
  "icons/icon-maskable-192.png", "icons/icon-maskable-512.png"
];
self.addEventListener("install", function (ev) {
  ev.waitUntil(caches.open(VERSION).then(function (c) {
    return c.addAll(SHELL).then(function () {
      /* images des fiches, lues dans data.json */
      return fetch("data.json", { cache: "no-cache" }).then(function (r) { return r.json(); }).then(function (d) {
        var imgs = [];
        (d.nodes || []).forEach(function (n) { if (n.image) imgs.push(n.image); if (n.logo) imgs.push(n.logo); });
        return Promise.all(imgs.map(function (u) { return c.add(u).catch(function () {}); }));
      }).catch(function () {});
    });
  }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener("activate", function (ev) {
  ev.waitUntil(caches.keys().then(function (ks) {
    return Promise.all(ks.filter(function (k) { return k !== VERSION; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
function networkFirst(req, fallbackUrl) {
  return fetch(req).then(function (res) {
    if (res && res.ok) { var copy = res.clone(); caches.open(VERSION).then(function (c) { c.put(fallbackUrl || req, copy); }); }
    return res;
  }).catch(function () {
    return caches.match(fallbackUrl || req, { ignoreSearch: true }).then(function (r) { return r || caches.match("index.html"); });
  });
}
function staleWhileRevalidate(req) {
  return caches.open(VERSION).then(function (c) {
    return c.match(req, { ignoreSearch: true }).then(function (hit) {
      var net = fetch(req).then(function (res) { if (res && res.ok) c.put(req, res.clone()); return res; }).catch(function () { return hit; });
      return hit || net;
    });
  });
}
self.addEventListener("fetch", function (ev) {
  var req = ev.request;
  if (req.method !== "GET") return;
  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (req.mode === "navigate") { ev.respondWith(networkFirst(req, "index.html")); return; }
  if (/\/(data\.json|config\.js)$/.test(url.pathname)) { ev.respondWith(networkFirst(req)); return; }
  ev.respondWith(staleWhileRevalidate(req));
});
