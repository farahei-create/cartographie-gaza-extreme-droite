# -*- coding: utf-8 -*-
"""Versions : règle de conservation, tag, retour sans force-push."""
import datetime
import os
import shutil
import subprocess
import sys
import tempfile
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

from tools.versions.policy import keep_path, tag_ok
from tools.versions.restore import apply_restore
from tools.versions.save import already_tagged, create_tag, run

ok = fail = 0


def check(cond, message):
    global ok, fail
    if cond:
        ok += 1
    else:
        fail += 1
        print("FAIL:", message)


check(tag_ok("version-2026-11-18-avant-cartes"), "tag réel")
check(tag_ok("version-2026-11-18"), "tag daté")
check(not tag_ok("main"), "main refusé")
check(not tag_ok("version-avant"), "sans date refusé")
check(not tag_ok("version-2026-11-18-Avant"), "majuscule refusée")
check(not tag_ok("../version-2026-11-18"), "chemin refusé")
check(keep_path("auto_pending.json") and keep_path("admin.html") and keep_path("tools/daily/run.py"), "file, admin, relevé gardés")
check(keep_path(".github/workflows/daily-update.yml") and keep_path("docs/REPRISE.md"), "workflow et guide gardés")
check(not keep_path("tools/auto_published.json"), "mémoire des phrases remises avec la version")
check(not keep_path("app.js") and not keep_path("data.json") and not keep_path("c/a/0.html"), "le site public revient")

yml_save = open(".github/workflows/enregistrer-version.yml", encoding="utf-8").read()
yml_back = open(".github/workflows/revenir-version.yml", encoding="utf-8").read()
check("workflow_dispatch" in yml_save and "cron:" in yml_save and "app.js" in yml_save, "enregistrer : main, dimanche, interface")
check("workflow_dispatch" in yml_back and "REVENIR" in yml_back and "onrecord-daily" in yml_back, "revenir : confirmation, file avec le relevé")
check("--force" not in yml_save and "--force" not in yml_back, "pas de force-push dans les workflows")
check("push --force" not in open("tools/versions/restore.py", encoding="utf-8").read(), "le script ne force pas")

tmp = tempfile.mkdtemp(prefix="onrecord-versions-")
try:
    def sh(*args, check_run=True):
        result = subprocess.run(["git", *args], cwd=tmp, check=False, capture_output=True, text=True)
        if check_run and result.returncode != 0:
            raise SystemExit(result.stderr or result.stdout)
        return result

    sh("init", "-b", "main")
    sh("config", "user.email", "test@example.com")
    sh("config", "user.name", "Test")

    def write(rel, text):
        path = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    write("app.js", "ANCIEN")
    write("data.json", '{"ancien": true}\n')
    write("tools/auto_published.json", '{"statements": ["ancienne"]}\n')
    write("auto_pending.json", '{"items": ["ancienne-file"]}\n')
    write("admin.html", "ADMIN-ANCIEN")
    write("docs/JOURNAL.md", "# Journal\n\n## 2026-01-01 — départ\n\nAncien.\n")
    write("docs/REPRISE.md", "guide ancien\n")
    write("AGENTS.md", "agents\n")
    write("sw.js", 'var VERSION = "onrecord-v3";\n')
    for name in ("test_v13.py", "test_v22.py", "test_v23.py", "test_v24.py", "test_admin.py"):
        write("tests/" + name, 'check("onrecord-v3" in open("sw.js").read(), "sw")\n')
    write("tests/test_daily.py", "DAILY-ANCIEN\n")
    write(".github/workflows/daily-update.yml", "name: ancien\n")
    write("tools/daily/run.py", "DAILYCODE-ANCIEN\n")
    sh("add", "-A")
    sh("commit", "-m", "base")
    when = datetime.datetime(2026, 1, 1, 8, 0, tzinfo=ZoneInfo("Europe/Paris"))
    base = create_tag(tmp, "HEAD", "Point de départ du test.", slug="base", when=when)
    check(base == "version-2026-01-01-base", "nom du tag " + base)
    check(already_tagged(tmp, "HEAD"), "le commit de départ est tagué")

    write("app.js", "NOUVEAU")
    write("data.json", '{"nouveau": true}\n')
    write("tools/auto_published.json", '{"statements": ["nouvelle"]}\n')
    write("auto_pending.json", '{"items": ["file-gardée"]}\n')
    write("admin.html", "ADMIN-NEUF")
    write("tests/test_daily.py", "DAILY-NEUF\n")
    write(".github/workflows/daily-update.yml", "name: neuf\n")
    write("tools/daily/run.py", "DAILYCODE-NEUF\n")
    write("c/alice/0.html", "PAGE-NEUVE\n")
    sh("add", "-A")
    sh("commit", "-m", "apres")
    head_before = sh("rev-parse", "HEAD").stdout.strip()

    refused = subprocess.run(
        [sys.executable, "-m", "tools.versions.restore", "--version", "main", "--confirm", "REVENIR", "--apply", "--root", tmp],
        cwd=ROOT, capture_output=True, text=True,
    )
    check(refused.returncode != 0 and sh("rev-parse", "HEAD").stdout.strip() == head_before, "nom invalide : rien ne bouge")
    wrong = subprocess.run(
        [sys.executable, "-m", "tools.versions.restore", "--version", base, "--confirm", "oui", "--apply", "--root", tmp],
        cwd=ROOT, capture_output=True, text=True,
    )
    check(wrong.returncode != 0 and sh("rev-parse", "HEAD").stdout.strip() == head_before, "sans REVENIR : rien ne bouge")

    code = apply_restore(tmp, base, push=False)
    check(code == 0, "retour appliqué")
    def read(rel):
        with open(os.path.join(tmp, rel), encoding="utf-8") as handle:
            return handle.read()
    check(read("app.js") == "ANCIEN" and '"ancien"' in read("data.json"), "site revenu")
    check('"ancienne"' in read("tools/auto_published.json"), "phrases auto remises avec la version")
    check("file-gardée" in read("auto_pending.json"), "file d'attente gardée")
    check(read("admin.html") == "ADMIN-NEUF", "page admin gardée")
    check("DAILY-NEUF" in read("tests/test_daily.py") and "DAILYCODE-NEUF" in read("tools/daily/run.py"), "relevé du matin gardé")
    check("name: neuf" in read(".github/workflows/daily-update.yml"), "workflows gardés")
    check(not os.path.exists(os.path.join(tmp, "c/alice/0.html")), "page ajoutée après retirée")
    check("retour à %s" % base in read("docs/JOURNAL.md") and "2026-01-01 — départ" in read("docs/JOURNAL.md"), "journal complété, pas effacé")
    check('onrecord-v4' in read("sw.js") and 'onrecord-v4' in read("tests/test_v13.py"), "cache monté au-dessus des deux")
    check(sh("rev-parse", "HEAD").stdout.strip() != head_before, "nouveau commit")
    check(head_before in sh("rev-list", "HEAD").stdout, "l'historique garde l'état d'après")
    tags = sh("tag", "--points-at", head_before).stdout
    check("avant-retour" in tags, "état d'avant le retour tagué " + tags.strip())
    check("force" not in sh("log", "-1", "--format=%B").stdout, "message sans force")

    write("app.js", "APRES-RETOUR")
    sh("add", "-A")
    sh("commit", "-m", "suite")
    again = run(tmp, "schedule", "", "", "", push=False)
    catalog = read("versions.json")
    check(again == 0 and sh("tag").stdout.count("hebdo") == 1 and "hebdo" in catalog and "Point de départ" in catalog, "dimanche : une version dans la liste")
    again2 = run(tmp, "schedule", "", "", "", push=False)
    check(again2 == 0 and sh("tag").stdout.count("hebdo") == 1, "deuxième dimanche sur le même commit : pas de doublon")
finally:
    shutil.rmtree(tmp)

from tools.share_pages import render_page
sample = {
    "id": "ada-exemple", "type": "person", "name": "Ada Exemple", "role": "Députée",
}
exact = "Phrase exacte, sans coupe."
page = render_page(sample, 0, {
    "quote": exact, "date": "2026-11-18",
    "medium": "franceinfo. Contexte : précision lue dans la même page.",
    "url": "https://www.franceinfo.fr/a", "theme": "France – normalisation de l'extrême droite",
})
check(exact in page and "Contexte sur Onrecord" in page and "<img" not in page, "page de partage")
check('property="og:title"' in page and "og:description" in page and "Ouvrir la fiche" in page, "balises et lien de fiche")
long_quote = ("mot " * 80).strip()
long_page = render_page(sample, 1, {
    "quote": long_quote, "date": "2026-11-18", "medium": "BFMTV",
    "url": "https://www.bfmtv.com/a", "theme": "Médias – structure",
})
check(long_quote in long_page and "[…]" in long_page, "aperçu raccourci, citation entière dans la page")
for bad in ("complice", "génocidaire", "pantin", "infiltré", "marionnette", "protégé", "copinage", "occulte"):
    check(bad not in page, "modèle sans " + bad)

print("%d ok, %d fail" % (ok, fail))
sys.exit(1 if fail else 0)
