import { createRequire } from "module";
import assert from "assert";
const require = createRequire(import.meta.url);
const A = require("../admin.js");

const ids = { "marine-le-pen": true, rn: true };
const good = {
  people: [],
  statements: [{
    person_id: "marine-le-pen",
    person_name: "Marine Le Pen",
    quote: "Phrase exacte d'exemple.",
    date: "2026-11-12",
    medium: "TF1, journal",
    context: "Elle répond à une question.",
    denial: "",
    url: "https://www.tf1info.fr/exemple",
    theme: "France – normalisation de l'extrême droite",
    section: "france"
  }],
  edges: [],
  photos: [{
    id: "marine-le-pen",
    image: "img/people/marine-le-pen.webp",
    image_credit: {
      author: "Auteur",
      license: "CC BY 4.0",
      license_url: "https://creativecommons.org/licenses/by/4.0/",
      source_url: "https://commons.wikimedia.org/wiki/File:Exemple.jpg"
    },
    base64: "aGVsbG8="
  }]
};

assert.deepEqual(A.validateDraft(good, ids), []);
assert.ok(A.validateDraft({
  statements: [{ ...good.statements[0], url: "https://fr.wikipedia.org/wiki/X" }]
}, ids).some((e) => /Wikipédia/.test(e)));
assert.ok(A.validateDraft({
  people: [{
    id: "x", name: "X", type: "person", role: "pantin du parti", description: "Rôle",
    category: "Responsables politiques", subcategory: "Parlementaires & élus", sections: ["france"]
  }],
  statements: [{ ...good.statements[0], person_id: "x" }]
}, ids).some((e) => /pantin/.test(e)));
assert.strictEqual(A.slugify("Éric Zemmour"), "eric-zemmour");
assert.ok(A.commitMessage(good).startsWith("admin: ajout "));
assert.ok(!/255, 255, 255/.test("purple"));

const remote = { additions: { people: [], statements: [], edges: [], photos: [] }, peopleImages: { rn: { logo: "img/orgs/rn.webp" } } };
const built = A.filesFromDraft(remote, good);
const jsonFile = built.files.find((f) => f.path === "tools/admin_additions.json");
const parsed = JSON.parse(jsonFile.content);
assert.strictEqual(parsed.statements.length, 1);
assert.ok(parsed.statements[0].medium.includes("Contexte"));
assert.ok(!JSON.stringify(parsed).includes("aGVsbG8"));
const img = built.files.find((f) => f.path === "img/people/marine-le-pen.webp");
assert.strictEqual(img.encoding, "base64");
assert.strictEqual(img.content, "aGVsbG8=");
const people = JSON.parse(built.files.find((f) => f.path === "tools/people_images.json").content);
assert.strictEqual(people.rn.logo, "img/orgs/rn.webp");
assert.strictEqual(people["marine-le-pen"].image_credit.license, "CC BY 4.0");

const hosts = [];
let patches = 0;
function github(method, path, body) {
  hosts.push(path);
  if (!path.startsWith("/repos/farahei-create/cartographie-gaza-extreme-droite/")) throw new Error(path);
  if (method === "GET" && path.endsWith("/git/ref/heads/main")) {
    return Promise.resolve({ status: 200, body: { object: { sha: "parent" + patches } } });
  }
  if (method === "GET" && path.includes("/git/commits/")) {
    return Promise.resolve({ status: 200, body: { tree: { sha: "tree0" } } });
  }
  if (method === "POST" && path.endsWith("/git/blobs")) {
    return Promise.resolve({ status: 201, body: { sha: "blob" + hosts.length } });
  }
  if (method === "POST" && path.endsWith("/git/trees")) {
    return Promise.resolve({ status: 201, body: { sha: "tree1" } });
  }
  if (method === "POST" && path.endsWith("/git/commits")) {
    assert.ok(body.message.startsWith("admin: ajout "));
    assert.deepEqual(body.parents, ["parent" + patches]);
    return Promise.resolve({ status: 201, body: { sha: "abc123deadbeef" } });
  }
  if (method === "PATCH") {
    patches += 1;
    if (patches === 1) return Promise.resolve({ status: 422, body: { message: "not a fast forward" } });
    return Promise.resolve({ status: 200, body: {} });
  }
  throw new Error("unexpected " + method + " " + path);
}

let prepares = 0;
const res = await A.commitFiles({
  github,
  prepare() {
    prepares += 1;
    return A.filesFromDraft(remote, good);
  }
});
assert.strictEqual(patches, 2);
assert.strictEqual(prepares, 2);
assert.strictEqual(res.sha, "abc123deadbeef");
assert.ok(res.url.includes("github.com/farahei-create/cartographie-gaza-extreme-droite/commit/abc123deadbeef"));
assert.ok(hosts.every((p) => p.startsWith("/repos/farahei-create/cartographie-gaza-extreme-droite/")));

await assert.rejects(
  () => A.commitFiles({
    github() { return Promise.resolve({ status: 401, body: { message: "Bad credentials" } }); },
    prepare() { return A.filesFromDraft(remote, good); }
  }),
  /Jeton refusé/
);

const merged = A.mergeAdditions(
  { statements: [{ person_id: "a", quote: "déjà" }] },
  { statements: [{ person_id: "a", quote: "déjà" }, { person_id: "a", quote: "nouvelle" }] }
);
assert.strictEqual(merged.statements.length, 2);
assert.strictEqual(A.decodeB64(Buffer.from('{"ok":1}', "utf8").toString("base64")), '{"ok":1}');
console.log("admin mock ok");
