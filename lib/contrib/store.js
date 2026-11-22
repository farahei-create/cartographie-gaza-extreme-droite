/* Stockage des contributions.
   - blobStore : Vercel Blob (BLOB_READ_WRITE_TOKEN). Chaque objet reçoit un suffixe
     aléatoire : une adresse n'est jamais réécrite, donc jamais servie périmée par le cache.
   - memoryStore : même interface, en mémoire, pour les tests. */
"use strict";

function blobStore() {
  var blob = require("@vercel/blob");
  var opts = { access: "public", addRandomSuffix: true, contentType: "application/json", cacheControlMaxAge: 60 };
  return {
    kind: "blob",
    put: function (pathname, obj) {
      return blob.put(pathname, JSON.stringify(obj), opts).then(function (r) { return { pathname: r.pathname, url: r.url }; });
    },
    list: function (prefix) {
      var out = [];
      function page(cursor) {
        return blob.list({ prefix: prefix, limit: 1000, cursor: cursor }).then(function (r) {
          r.blobs.forEach(function (b) { out.push({ pathname: b.pathname, url: b.url, uploadedAt: new Date(b.uploadedAt).getTime(), size: b.size }); });
          return r.hasMore && r.cursor ? page(r.cursor) : out;
        });
      }
      return page(undefined);
    },
    read: function (item) {
      return fetch(item.url, { cache: "no-store" }).then(function (r) { if (!r.ok) return null; return r.json(); }).catch(function () { return null; });
    },
    del: function (urls) {
      urls = (urls || []).filter(Boolean);
      return urls.length ? blob.del(urls) : Promise.resolve();
    }
  };
}

function memoryStore(clock) {
  var items = [];
  var n = 0;
  var now = clock || Date.now;
  return {
    kind: "memory",
    items: items,
    put: function (pathname, obj) {
      var p = pathname + "-" + (++n).toString(36);
      var it = { pathname: p, url: "https://test.public.blob.vercel-storage.com/" + p, uploadedAt: now(), body: JSON.stringify(obj) };
      items.push(it);
      return Promise.resolve({ pathname: p, url: it.url });
    },
    list: function (prefix) {
      return Promise.resolve(items.filter(function (i) { return i.pathname.indexOf(prefix) === 0; })
        .map(function (i) { return { pathname: i.pathname, url: i.url, uploadedAt: i.uploadedAt }; }));
    },
    read: function (item) {
      var it = items.find(function (i) { return i.url === item.url; });
      return Promise.resolve(it ? JSON.parse(it.body) : null);
    },
    del: function (urls) {
      (urls || []).forEach(function (u) {
        var k = items.findIndex(function (i) { return i.url === u; });
        if (k >= 0) items.splice(k, 1);
      });
      return Promise.resolve();
    }
  };
}

module.exports = { blobStore: blobStore, memoryStore: memoryStore };
