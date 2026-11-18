# -*- coding: utf-8 -*-
"""Garde-fous du relevé du matin. Aucune écriture dans data.json."""
import datetime
import json
import os
import subprocess
import sys
import tempfile
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

from tools.daily.collect import extract_html, parse_feed, publisher_from_batch
from tools.daily.engine import load_index, review_item, review_pages
from tools.daily.store import expect_line, merge_pending, merge_published, tier_counts
from tools.daily.textutil import forbidden_hits, norm_literal

ok = fail = 0
NOW = datetime.datetime(2026, 11, 18, 8, 0, tzinfo=ZoneInfo("Europe/Paris"))
DAY = "2026-11-17"


def check(cond, message):
    global ok, fail
    if cond:
        ok += 1
    else:
        fail += 1
        print("FAIL:", message)


def page(text, url="https://www.franceinfo.fr/exemple-releve", dates=None, title="Exemple"):
    return {
        "url": url,
        "outlet": "franceinfo",
        "title": title,
        "text": text,
        "html": "<html><p>%s</p></html>" % text,
        "dates": dates if dates is not None else [DAY],
        "feed_date": DAY,
    }


def raw(**kwargs):
    base = {
        "person_name": "Marine Le Pen",
        "quote": "Il faut une priorité nationale pour le logement social, dit-elle dans cet extrait de contrôle.",
        "date": DAY,
        "section": "france",
        "theme": "France – normalisation de l'extrême droite",
        "context": "",
        "denial": "",
        "video_url": "",
        "doubt": "",
        "public_role": "",
    }
    base.update(kwargs)
    return base


QUOTE = raw()["quote"]
TEXT = (
    "Article du 17 novembre 2026. Marine Le Pen, au sujet de l'immigration et du Rassemblement national, "
    "déclare : « %s » Elle ne parle pas d'autre chose."
) % QUOTE
INDEX = load_index({
    "nodes": [{
        "id": "marine-le-pen",
        "name": "Marine Le Pen",
        "type": "person",
        "statements": [{"quote": "déjà publiée telle quelle dans l'archive", "url": "https://www.franceinfo.fr/ancienne"}],
    }]
})


def review(**kwargs):
    item = raw(**kwargs.pop("raw_over", {}))
    return review_item(item, kwargs.pop("pg", page(TEXT)), INDEX, NOW, kwargs.pop("accepted", []), set(), {})


check(forbidden_hits("protéger la forêt") == [], "protéger n'est pas protégé")
check("protege" in forbidden_hits("un protégé du pouvoir"), "protégé")
check(forbidden_hits("les complices") and forbidden_hits("génocidaire") and forbidden_hits("infiltrée"), "mots interdits")
check(forbidden_hits("la condamnation du génocide") == [], "génocide n'est pas génocidaire")
check("  a  " not in norm_literal("a\u00a0b\u2019c") and norm_literal("a\u00a0b\u2019c") == "a b'c", "espaces et apostrophe")

kept = review()
check(kept["kind"] == "publish" and kept["statement"]["person_id"] == "marine-le-pen", "fiche connue acceptée : " + str(kept.get("reason") or kept.get("kind")))
check(review(raw_over={"quote": "Une paraphrase qui n'est pas dans la page du tout."})["reason"].startswith("citation absente"), "paraphrase")
narration = "Marine Le Pen a parlé d'immigration ce matin devant les caméras."
check(review(pg=page("Article du 17 novembre 2026. %s Le Rassemblement national était là." % narration), raw_over={"quote": narration})["reason"].startswith("citation non présentée"), "narration sans guillemets")
check(review(raw_over={"quote": QUOTE + " et ses complices dans cette affaire précise."})["reason"].startswith("mot interdit") and review(raw_over={"quote": QUOTE + " et ses complices dans cette affaire précise."})["quote"] == "", "mot interdit masqué")
check(review(raw_over={"date": "2020-01-01"})["reason"].startswith("date hors"), "vieille date")
check(review(raw_over={"date": "2026-11-19"})["reason"].startswith("date hors"), "date future")
check(review(pg=page(TEXT, url="https://fr.wikipedia.org/wiki/Exemple"))["reason"].startswith("source non publiable"), "wikipédia")
check(review(pg=page(TEXT, url="https://x.com/MLP_officiel/status/1"))["reason"].startswith("source non publiable"), "x.com")
check(review(raw_over={"quote": "déjà publiée telle quelle dans l'archive", "person_name": "Marine Le Pen"})["reason"] == "déjà en ligne" or review(pg=page(
    "Article du 17 novembre 2026. Marine Le Pen parle d'immigration. « déjà publiée telle quelle dans l'archive »"
), raw_over={"quote": "déjà publiée telle quelle dans l'archive"})["reason"] == "déjà en ligne", "doublon")
check(review(raw_over={"doubt": "attribution incertaine"})["reason"].startswith("doute"), "doute en file")
check(review(raw_over={"context": "Il a nommé son successeur sans que la page le dise ici."})["kind"] == "publish", "contexte inventé ignoré, phrase gardée")
off = page("Article du 17 novembre 2026. Marine Le Pen a parlé du prix du carburant. « %s »" % QUOTE)
# La phrase de contrôle contient « priorité nationale » et « logement social » : elle reste dans le sujet.
# Une phrase sans aucun mot du sujet, loin de ces mots, est écartée.
bare = "Le prix du carburant va baisser dès lundi matin selon elle."
off2 = page("Article du 17 novembre 2026. Marine Le Pen commente le carburant : « %s » Rien d'autre." % bare)
check(review(pg=off2, raw_over={"quote": bare})["reason"] == "hors des deux sujets", "hors sujet")

private_text = (
    "Article du 17 novembre 2026. Camille Martin, témoin de 19 ans, habitant du quartier, a dit au sujet de l'immigration : "
    "« Je n'ai rien demandé, je passais devant l'immeuble. »"
)
private = review_item(
    raw(person_name="Camille Martin", quote="Je n'ai rien demandé, je passais devant l'immeuble.", public_role="témoin"),
    page(private_text), INDEX, NOW, [], set(), {},
)
check(private["kind"] == "pending" and private["person"] == "" and private["quote"] == "", "particulier masqué : " + private.get("reason", ""))

new_text = (
    "Article du 17 novembre 2026. Jeanne Exemple, députée, déclare au sujet de l'immigration : "
    "« Il faut réduire les entrées dès cette année, sans autre condition. »"
)
created = review_item(
    raw(person_name="Jeanne Exemple", quote="Il faut réduire les entrées dès cette année, sans autre condition.", public_role="députée"),
    page(new_text), INDEX, NOW, [], set(), {},
)
check(created["kind"] == "publish" and created["person"]["id"] == "jeanne-exemple", "nouvelle élue : " + str(created.get("reason") or created.get("kind")))
check(created["kind"] != "publish" or "image" not in created["person"], "pas de photo inventée")

wiki_batch = ')]}\'\n[["wrb.fr","Fbv4je","[\\"garturlres\\",\\"https://www.lemonde.fr/politique/article/exemple.html\\",1]"]]'
check(publisher_from_batch(wiki_batch) == "https://www.lemonde.fr/politique/article/exemple.html", "décodage Google News")
feed = parse_feed("""<?xml version="1.0"?><rss><channel><item>
<title>Gaza : une déclaration</title><link>https://www.lemonde.fr/a</link>
<pubDate>Tue, 17 Nov 2026 08:00:00 GMT</pubDate><description>Marine Le Pen</description>
</item></channel></rss>""")
check(len(feed) == 1 and feed[0]["url"].endswith("/a") and "Le Pen" in feed[0]["summary"], "flux RSS")
html = extract_html('<html><head><title>Titre</title><meta property="article:published_time" content="2026-11-17T06:00:00Z"></head><body><p>Marine Le Pen a dit bonjour.</p></body></html>')
check(html["title"] == "Titre" and "2026-11-17" in html["dates"] and "bonjour" in html["text"], "extraction HTML")

data = json.load(open("data.json", encoding="utf-8"))
js = open("app.js", encoding="utf-8").read()
counts = tier_counts(data, js)
expect = open("tests/test_v22.py", encoding="utf-8").read()
check(expect_line(counts) in expect, "EXPECT " + expect_line(counts))
real = load_index(data)
sample = None
for node in data["nodes"]:
    if node["id"] == "marine-le-pen" and node.get("statements"):
        sample = node["statements"][0]["quote"]
        break
if sample:
    again = review_item(raw(quote=sample), page("17 novembre 2026. Marine Le Pen, immigration. « %s »" % sample), real, NOW, [], set(), {})
    check(again["reason"] == "déjà en ligne", "doublon réel")

cfg = open("config.js", encoding="utf-8").read()
check('CORRECTION_EMAIL: ""' in cfg, "CORRECTION_EMAIL vide")
check("auto_pending" not in open("index.html", encoding="utf-8").read(), "pas de lien depuis l'accueil")
check("File d’attente" in open("admin.html", encoding="utf-8").read() and "auto_pending.json" in open("admin.js", encoding="utf-8").read(), "file sur la page admin")

published_before = open("tools/auto_published.json", encoding="utf-8").read()
pending_before = open("auto_pending.json", encoding="utf-8").read()
data_before = open("data.json", encoding="utf-8").read()
env = os.environ.copy()
env.pop("GEMINI_API_KEY", None)
env.pop("ONRECORD_AUTO_JSON", None)
env.pop("ONRECORD_PENDING_JSON", None)
missing = subprocess.run([sys.executable, "-m", "tools.daily.run"], cwd=ROOT, env=env, capture_output=True, text=True)
check(missing.returncode == 0 and "GEMINI_API_KEY" in missing.stdout, "sans clé : arrêt propre")
mock = subprocess.run([sys.executable, "-m", "tools.daily.run", "--mock", "--dry-run"], cwd=ROOT, env=env, capture_output=True, text=True)
check(mock.returncode == 0 and "à blanc" in mock.stdout, "simulation à blanc : " + (mock.stderr or "")[-300:])
check(open("tools/auto_published.json", encoding="utf-8").read() == published_before, "rien écrit dans auto_published")
check(open("auto_pending.json", encoding="utf-8").read() == pending_before, "rien écrit dans la file")
check(open("data.json", encoding="utf-8").read() == data_before, "data.json intact")
check("ne doit pas être publiée" not in data_before, "la phrase de contrôle n'est pas dans l'archive")

tmp = tempfile.mkdtemp()
os.environ["ONRECORD_AUTO_JSON"] = os.path.join(tmp, "pub.json")
os.environ["ONRECORD_PENDING_JSON"] = os.path.join(tmp, "wait.json")
try:
    added, people = merge_published(ROOT, [kept], NOW.date())
    check(added == 1 and people == 0, "ajout d'une phrase sur une fiche connue")
    added2, _ = merge_published(ROOT, [kept], NOW.date())
    check(added2 == 0, "pas de second ajout")
    changed = merge_pending(ROOT, [private], NOW.date())
    check(changed, "file écrite")
    saved = json.load(open(os.environ["ONRECORD_PENDING_JSON"], encoding="utf-8"))
    check(saved["items"] and saved["items"][0]["quote"] == "" and saved["items"][0]["person"] == "", "file sans particulier")
    blob = json.dumps(saved, ensure_ascii=False)
    check("Je n'ai rien demandé" not in blob, "citation privée absente du fichier")
finally:
    os.environ.pop("ONRECORD_AUTO_JSON", None)
    os.environ.pop("ONRECORD_PENDING_JSON", None)

fixture = {
    "people": [],
    "statements": [{
        "person_id": "marine-le-pen",
        "quote": "Phrase de contrôle du build, absente du site.",
        "date": "2026-11-17",
        "medium": "franceinfo, page du 17 novembre 2026. Contrôle technique.",
        "url": "https://www.franceinfo.fr/controle-build-onrecord",
        "theme": "France – normalisation de l'extrême droite",
        "section": "france",
    }],
    "edges": [],
}
fix_path = os.path.join(tmp, "auto.json")
out_path = os.path.join(tmp, "data.json")
json.dump(fixture, open(fix_path, "w", encoding="utf-8"))
built = subprocess.run([sys.executable, "build.py"], cwd=ROOT, env={**os.environ, "ONRECORD_AUTO_JSON": fix_path, "ONRECORD_DATA_OUT": out_path, "GEMINI_API_KEY": ""}, capture_output=True, text=True)
check(built.returncode == 0, (built.stderr or built.stdout)[-400:])
if built.returncode == 0:
    out = json.load(open(out_path, encoding="utf-8"))
    by = {n["id"]: n for n in out["nodes"]}
    quotes = [s["quote"] for s in by["marine-le-pen"]["statements"]]
    check("Phrase de contrôle du build, absente du site." in quotes, "build applique le fichier")
    check(all(not n.get("image") or n["id"] != "personne-inexistante" for n in out["nodes"]), "build")
bad_fix = json.loads(json.dumps(fixture))
bad_fix["statements"][0]["medium"] = "Un pantin, selon la rédaction du contrôle."
bad_path = os.path.join(tmp, "bad.json")
json.dump(bad_fix, open(bad_path, "w", encoding="utf-8"))
bad = subprocess.run([sys.executable, "build.py"], cwd=ROOT, env={**os.environ, "ONRECORD_AUTO_JSON": bad_path, "ONRECORD_DATA_OUT": os.path.join(tmp, "bad-out.json")}, capture_output=True, text=True)
check(bad.returncode != 0 and "pantin" in (bad.stderr + bad.stdout).lower(), "build refuse un mot interdit")
check(open("data.json", encoding="utf-8").read() == data_before, "le build de contrôle n'a pas touché data.json")

print("%d ok, %d fail" % (ok, fail))
sys.exit(1 if fail else 0)
