# -*- coding: utf-8 -*-
"""Garde-fous du relevé du matin. Aucune écriture dans data.json."""
import datetime
import json
import re
import os
import subprocess
import sys
import tempfile
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

from tools.daily.collect import extract_html, parse_feed, publisher_from_batch
from tools.daily.collect import select_diverse
from tools.daily.engine import ground_quote, load_index, review_item, review_pages
from tools.daily.run import summary_markdown
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
cut_page = page(
    "Article du 17 novembre 2026. Éric Zemmour, au sujet de l'immigration : "
    "« Une des plus stables, une des plus sérieuses où l'État de droit tient bon. »"
)
cut_quote = "Une des plus stables, une des plus sérieuses où l'État d"
check(review(pg=cut_page, raw_over={"quote": cut_quote, "person_name": "Éric Zemmour"})["reason"] == "citation coupée au milieu d'un mot", "coupe au milieu d'un mot")
mid = "Une des plus stables, une des plus sérieuses où l'État de droit"
check(review(pg=cut_page, raw_over={"quote": mid, "person_name": "Éric Zemmour"})["reason"] == "citation coupée au milieu d'une phrase", "coupe au milieu d'une phrase")
check(ground_quote("Elle s'arrête ici…", "« Elle s'arrête ici et la phrase continue. »").startswith("points de suspension"), "points de suspension ajoutés")
whole = "On retire la nationalité aux binationaux quand l'immigration est en cause."
ellipsis = "On retire la nationalité […] l'immigration est en cause."
ell_page = page("Article du 17 novembre 2026. Marine Le Pen déclare : « %s »" % whole)
kept_ell = review(pg=ell_page, raw_over={"quote": ellipsis})
check(kept_ell["kind"] == "publish" and "[…]" in kept_ell["statement"]["quote"], "ellipse dont les deux bouts sont dans la page : " + str(kept_ell.get("reason")))
check(ground_quote("On retire la nation […] l'immigration est en cause.", "« %s »" % whole) == "ellipse au milieu d'un mot", "ellipse au milieu d'un mot")
check(ground_quote("On retire la nationalité […] cette formule n'est pas écrite.", "« %s »" % whole).startswith("ellipse"), "ellipse inventée")
longer = "ramassis de gauchistes, d'une violence à l'égard des institutions qui est une véritable honte."
idx_pen = load_index({"nodes": [{"id": "marine-le-pen", "name": "Marine Le Pen", "type": "person", "statements": [{"quote": "ramassis de gauchistes"}]}]})
again = review_item(
    raw(quote=longer),
    page("Article du 17 novembre 2026. Marine Le Pen, immigration : « %s »" % longer),
    idx_pen, NOW, [], set(), {},
)
check(again["reason"] == "déjà en ligne", "ramassis de gauchistes déjà en ligne")
q2 = "L'immigration doit baisser dès cette année, dit-elle dans la même émission."
q3 = "Le logement social reste soumis à cette priorité nationale, ajoute-t-elle."
trio = page("Article du 17 novembre 2026. Marine Le Pen : « %s » « %s » « %s »" % (QUOTE, q2, q3))
spread = review_pages([trio], {trio["url"]: [
    raw(), raw(quote=q2), raw(quote=q3),
]}, INDEX, NOW)
check(sum(1 for item in spread["published"] if item["statement"]["person_id"] == "marine-le-pen") == 2, "plafond de deux phrases par personne")
check(any(item.get("reason", "").startswith("plafond") for item in spread["pending"]), "le surplus va dans la file")
found = []
for i in range(8):
    found.append({"url": "https://www.europe1.fr/b%d" % i, "outlet": "Europe 1", "title": "Jordan Bardella et l'immigration %d" % i, "summary": "", "score": 20 - i})
found.append({"url": "https://www.lemonde.fr/z", "outlet": "Le Monde", "title": "Éric Zemmour et l'immigration", "summary": "", "score": 3})
found.append({"url": "https://www.liberation.fr/m", "outlet": "Libération", "title": "Jean-Luc Mélenchon parle de Gaza", "summary": "", "score": 2})
picked = select_diverse(found, ["Jordan Bardella", "Éric Zemmour", "Jean-Luc Mélenchon"], limit=6)
check(sum(1 for item in picked if "Bardella" in item["title"]) <= 2, "au plus deux pages Bardella")
check(any("Zemmour" in item["title"] for item in picked) and any("Mélenchon" in item["title"] for item in picked), "les autres personnes sont lues")
report = summary_markdown(
    {"feeds_ok": 25, "feeds_fail": 1, "feed_errors": [{"outlet": "Sud Radio", "url": "https://www.sudradio.fr/feed/", "error": "HTTP Error 404: Not Found"}],
     "items": 1, "fetched": 1, "fetch_fail": 0, "google_unresolved": 0},
    {"published": [{"label": "Éric Zemmour", "statement": {"person_id": "eric-zemmour", "date": "2026-11-17", "quote": whole, "url": "https://www.europe1.fr/zemmour"}}], "pending": []},
    "gemini-3.5-flash-lite", 1, True)
check("Sud Radio" in report and "HTTP Error 404" in report, "le flux en échec est nommé")
check(whole in report and "État d…" not in report, "le résumé ne coupe pas la phrase")
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

# --- 22/11 : extraction, pages bloquées, secours Gemini ---
from tools.daily.collect import extract_html, excerpt as _excerpt, is_challenge, is_hub
_html = ("<html><head><title>Article</title></head><body><nav><a>Gaza</a><a>Rassemblement national</a></nav>"
         "<p>Marine Le Pen, députée, a déclaré : « Nous ne <a href='#'>céderons</a> rien, jamais. »</p>"
         "<p>%s</p></body></html>") % ("Texte de contexte assez long pour compter comme un paragraphe utile. " * 3)
_ex = extract_html(_html)
check("Nous ne céderons rien, jamais." in _ex["text"], "lien dans une citation : pas d'espace ajouté")
check(_ex["article"].startswith("Marine Le Pen") and "Rassemblement national" not in _ex["article"], "paragraphes sans le menu")
check(_excerpt({"article": _ex["article"] + "\n" + "Autre paragraphe sans guillemets mais long, pour dépasser la limite basse. " * 5, "text": _ex["text"]}).startswith("Marine Le Pen"), "extrait = article")
check(is_challenge("Client Challenge", "x" * 1000) and is_challenge("Accès restreint - Le Monde", "x" * 1000) and not is_challenge("Un article", "x" * 1000), "mur anti-robot repéré")
check(is_hub("https://www.bfmtv.com/politique/marine-le-pen_DN-201201010011.html") and not is_hub("https://www.bfmtv.com/politique/elections/article_AN-1.html"), "page index écartée")

from tools.daily import gemini as _g
class _FakeGemini(_g.Gemini):
    def __init__(self, answers):
        super().__init__("cle", sleep=lambda s: None)
        self.answers = answers
        self.calls = []
    def _post(self, model, prompt, schema):
        self.requests += 1
        self.calls.append(model)
        status = self.answers.get(model, 200)
        if status == 200:
            return 200, json.dumps({"candidates": [{"content": {"parts": [{"text": json.dumps({"items": []})}]}}]})
        return status, "erreur"
_pg = {"url": "https://www.franceinfo.fr/x", "text": "texte " * 100, "outlet": "franceinfo", "title": "t"}
_f = _FakeGemini({_g.MODELS[0]: 503})
check(_f.extract(_pg, []) == [] and _f.model == _g.MODELS[1], "503 : modèle de secours")
_f = _FakeGemini({_g.MODELS[0]: 429})
check(_f.extract(_pg, []) == [] and _f.model == _g.MODELS[1] and _g.MODELS[0] in _f.dead, "429 : quota de secours")
_f = _FakeGemini({m: 429 for m in _g.MODELS})
try:
    _f.extract(_pg, [])
    check(False, "429 partout : arrêt")
except _g.QuotaError:
    check(True, "429 partout : arrêt")

# --- Filet de secours : déjà fait aujourd'hui, Chrome des tests ---
from tools.daily.already_done import is_daily_update_subject, update_already_done, avant_maj_tag
from tools.daily.browser import chrome_executable, launch_chromium

day = datetime.date(2026, 11, 24)
check(is_daily_update_subject("Mise à jour du 24/11 : relevé automatique, 6 phrases", day), "sujet relevé automatique")
check(is_daily_update_subject("Mise à jour du 24/11 : file d'attente, rien publié", day), "sujet file d'attente")
check(is_daily_update_subject("Mise à jour du 24/11 : 31 phrases du 22 au 24/11 (Bardella…) (cache v62)", day), "sujet routine 8 h")
check(is_daily_update_subject("Mise à jour du 24/11 : 1 phrase", day), "sujet une phrase")
check(not is_daily_update_subject("Mise à jour du 24/11 : liste des versions", day), "liste des versions ignorée")
check(not is_daily_update_subject("Mise à jour du 24/11 : onglet Condamnations, décisions de justice", day), "changement d'onglet ignoré")
check(not is_daily_update_subject("Mise à jour du 24/11 : filet de secours du relevé du matin", day), "correctif technique ignoré")
check(not is_daily_update_subject("Mise à jour du 23/11 : relevé automatique, 2 phrases", day), "jour précédent ignoré")
check(avant_maj_tag(day) == "version-2026-11-24-avant-maj", "nom du tag avant-maj")

def _git_init(path):
    subprocess.run(["git", "init", "-b", "main"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=path, check=True, capture_output=True)

def _git_commit(path, message, when="2026-11-24T08:00:00+01:00"):
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = when
    env["GIT_COMMITTER_DATE"] = when
    marker = os.path.join(path, "README")
    with open(marker, "a", encoding="utf-8") as handle:
        handle.write(message + "\n")
    subprocess.run(["git", "add", "-A"], cwd=path, check=True, capture_output=True)
    done = subprocess.run(["git", "commit", "-m", message], cwd=path, capture_output=True, text=True, env=env)
    if done.returncode != 0:
        raise RuntimeError(done.stderr or done.stdout)

sandbox = tempfile.mkdtemp()
try:
    repo = os.path.join(sandbox, "repo")
    os.makedirs(repo)
    _git_init(repo)
    open(os.path.join(repo, "README"), "w").write("x\n")
    _git_commit(repo, "départ", "2026-11-23T18:00:00+01:00")
    hit = update_already_done(repo, day=day, ref="HEAD", fetch=False)
    check(not hit["done"], "dépôt sans mise à jour du jour")
    _git_commit(repo, "Mise à jour du 24/11 : liste des versions", "2026-11-24T07:50:00+01:00")
    hit = update_already_done(repo, day=day, ref="HEAD", fetch=False)
    check(not hit["done"], "liste des versions seule : pas encore fait")
    _git_commit(repo, "Mise à jour du 24/11 : 31 phrases du 22 au 24/11 (cache v62)", "2026-11-24T08:30:00+01:00")
    hit = update_already_done(repo, day=day, ref="HEAD", fetch=False)
    check(hit["done"] and "31 phrases" in hit["reason"], "phrases de la routine : déjà fait")

    repo2 = os.path.join(sandbox, "tag-only")
    os.makedirs(repo2)
    _git_init(repo2)
    open(os.path.join(repo2, "README"), "w").write("ok\n")
    _git_commit(repo2, "veille", "2026-11-23T18:00:00+01:00")
    subprocess.run(["git", "tag", "-a", "version-2026-11-24-avant-maj", "-m", "avant maj"], cwd=repo2, check=True, capture_output=True)
    hit = update_already_done(repo2, day=day, ref="HEAD", fetch=False)
    check(hit["done"] and "version-2026-11-24-avant-maj" in hit["reason"], "tag avant-maj : déjà fait")

    repo3 = os.path.join(sandbox, "auto")
    os.makedirs(repo3)
    _git_init(repo3)
    open(os.path.join(repo3, "README"), "w").write("ok\n")
    _git_commit(repo3, "Mise à jour du 24/11 : relevé automatique, 2 phrases", "2026-11-24T06:30:00+01:00")
    hit = update_already_done(repo3, day=day, ref="HEAD", fetch=False)
    check(hit["done"] and "relevé automatique" in hit["reason"], "workflow déjà passé")

    repo4 = os.path.join(sandbox, "hier")
    os.makedirs(repo4)
    _git_init(repo4)
    open(os.path.join(repo4, "README"), "w").write("ok\n")
    _git_commit(repo4, "Mise à jour du 23/11 : relevé automatique, 2 phrases", "2026-11-23T08:00:00+01:00")
    hit = update_already_done(repo4, day=day, ref="HEAD", fetch=False)
    check(not hit["done"], "relevé de la veille : pas encore fait")
finally:
    import shutil
    shutil.rmtree(sandbox, ignore_errors=True)

# Les tests Playwright du site doivent viser Chrome système, comme en CI.
# Un launch() nu cherche le Chromium de Playwright, absent du runner.
bare = []
for name in sorted(os.listdir(os.path.join(ROOT, "tests"))):
    if not name.endswith(".py"):
        continue
    src = open(os.path.join(ROOT, "tests", name), encoding="utf-8").read()
    if "chromium.launch" not in src:
        continue
    for match in re.finditer(r"chromium\.launch\((.*?)\)", src, re.S):
        args = match.group(1)
        if "executable_path" not in args:
            bare.append("%s: %s" % (name, match.group(0).replace("\n", " ")[:80]))
check(not bare, "launch Playwright sans Chrome système : " + ", ".join(bare))
check(chrome_executable() or True, "helper Chrome importable")
check(callable(launch_chromium), "launch_chromium disponible")

# Sur le dépôt réel, le 24/11/2026 a déjà sa mise à jour (routine de 8 h).
live = update_already_done(ROOT, day=datetime.date(2026, 11, 24), fetch=False)
check(live["done"], "main du 24/11 déjà à jour : " + (live.get("reason") or "sans raison"))

print("%d ok, %d fail" % (ok, fail))
sys.exit(1 if fail else 0)
