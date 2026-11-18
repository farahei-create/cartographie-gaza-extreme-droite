# -*- coding: utf-8 -*-
"""Pages statiques /c/<id>/<index>.html : lien profond et aperçu Open Graph.

Le navigateur dessine l'image (canvas). Ici, seulement le HTML : la citation
entière, pour les applications qui lisent la page sans exécuter de script.
"""
import os
import re

SITE = "https://onrecord-fr.vercel.app"
MONTHS = (
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
)
MARKER = "onrecord-citation"


def esc(text):
    return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def french_date(iso):
    found = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", iso or "")
    if not found:
        return iso or ""
    return "%d %s %s" % (int(found.group(3)), MONTHS[int(found.group(2)) - 1], found.group(1))


def has_context(statement):
    if statement.get("context") or statement.get("denial"):
        return True
    if statement.get("theme") == "Nuance / contexte":
        return True
    medium = statement.get("medium") or ""
    if re.search(r"contexte\s*:", medium, re.I):
        return True
    if re.search(r"d[eé]menti", medium, re.I):
        return True
    return bool(re.search(r"pr[eé]cision ou r[eé]ponse\s*:", medium, re.I))


def media_label(statement):
    medium = (statement.get("medium") or "").strip()
    medium = re.split(r"\s+Contexte\s*:", medium, maxsplit=1, flags=re.I)[0].strip()
    medium = re.split(r"\s+Pr[eé]cision ou r[eé]ponse\s*:", medium, maxsplit=1, flags=re.I)[0].strip()
    cut = re.split(r"\s;\s|\.\s", medium, maxsplit=1)[0].strip()
    if 8 <= len(cut) <= 110:
        return cut
    if len(medium) <= 110:
        return medium or "source non précisée"
    short = medium[:90]
    space = short.rfind(" ")
    if space > 40:
        short = short[:space]
    return short.rstrip(" ,;:.") + " […]"


def initials(name):
    words = []
    for part in re.split(r"[\s-]+", re.sub(r"[«»()]", "", name or "")):
        if len(part) > 1 and re.match(r"[A-Za-zÀ-ÿ0-9]", part):
            words.append(part)
    if not words:
        return "?"
    if len(words) == 1:
        return words[0][0].upper()
    return (words[0][0] + words[-1][0]).upper()


def og_description(quote, label):
    text = " ".join((quote or "").split())
    base = "« %s » — %s" % (text, label)
    if len(base) <= 240:
        return base
    cut = text[:200]
    space = cut.rfind(" ")
    if space > 80:
        cut = cut[:space]
    return "« %s […] » — %s" % (cut.rstrip(" ,;:."), label)


def fiche_url(node, index):
    kind = "personne" if node.get("type") == "person" else "organisation"
    return "%s/#/%s/%s#d%d" % (SITE, kind, node["id"], index)


def page_url(node, index):
    return "%s/c/%s/%d.html" % (SITE, node["id"], index)


def render_page(node, index, statement):
    label = media_label(statement)
    quote = statement.get("quote") or ""
    date = statement.get("date") or ""
    shown = french_date(date)
    role = node.get("role") or ""
    title = "%s, %s — Onrecord" % (node.get("name") or "", shown or date)
    desc = og_description(quote, label)
    ctx = '<p class="ctx">Contexte sur Onrecord</p>' if has_context(statement) else ""
    source = statement.get("url") or ""
    source_html = '<p><a href="%s">Lire la source</a></p>' % esc(source) if source.startswith("https://") else ""
    return """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:type" content="article">
<meta property="og:url" content="%s">
<meta property="og:site_name" content="Onrecord">
<meta property="og:locale" content="fr_FR">
<meta property="og:image" content="%s/icons/icon-512.png">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<meta name="theme-color" content="#07030f">
<style>
  body{margin:0;background:#07030f;color:#f7f3ff;font:18px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
  main{max-width:40rem;margin:0 auto;padding:28px 18px 48px}
  .brand{font-weight:800;letter-spacing:.08em;color:#fff;text-shadow:0 0 12px rgba(139,61,255,.85)}
  .mono{width:64px;height:64px;border-radius:50%%;display:grid;place-items:center;font-weight:700;color:#fff;
    background:linear-gradient(135deg,#3b0a57,#7b2cbf 55%%,#c2185b);box-shadow:0 0 18px rgba(124,58,237,.45)}
  h1{font-size:1.45rem;margin:12px 0 4px}
  .role,.meta{color:#d8c7ff}
  blockquote{margin:18px 0;font-size:1.35rem;line-height:1.45}
  a{color:#c084fc}
  .ctx{display:inline-block;margin:8px 0;padding:6px 12px;border:1px solid rgba(168,85,247,.7);border-radius:999px;color:#e9d5ff}
  .go{display:inline-block;margin-top:12px;padding:12px 18px;border-radius:999px;background:#7c3aed;color:#fff;text-decoration:none;font-weight:700}
</style>
</head>
<body>
<main>
<p class="brand">ONRECORD</p>
<div class="mono" aria-hidden="true">%s</div>
<h1>%s</h1>
<p class="role">%s</p>
<p class="meta"><time datetime="%s">%s</time> · %s</p>
<blockquote>%s</blockquote>
%s
%s
<p><a class="go" href="%s">Ouvrir la fiche</a></p>
</main>
<!-- %s -->
</body>
</html>
""" % (
        esc(title), esc(desc), esc(page_url(node, index)),
        esc(title), esc(desc), esc(page_url(node, index)), SITE,
        esc(title), esc(desc),
        esc(initials(node.get("name") or "")),
        esc(node.get("name") or ""),
        esc(role),
        esc(date), esc(shown or date), esc(label),
        esc(quote),
        ctx, source_html,
        esc(fiche_url(node, index)),
        MARKER,
    )


def write_pages(root, data):
    wanted = set()
    for node in data.get("nodes") or []:
        if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", node.get("id") or ""):
            continue
        for index, statement in enumerate(node.get("statements") or []):
            rel = os.path.join("c", node["id"], "%d.html" % index)
            wanted.add(rel)
            path = os.path.join(root, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            html = render_page(node, index, statement)
            current = ""
            if os.path.exists(path):
                with open(path, encoding="utf-8") as handle:
                    current = handle.read()
            if current != html:
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(html)
    base = os.path.join(root, "c")
    if not os.path.isdir(base):
        return len(wanted)
    for dirpath, _, files in os.walk(base):
        for name in files:
            if not name.endswith(".html"):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            if rel in wanted:
                continue
            with open(full, encoding="utf-8") as handle:
                head = handle.read(400)
            if MARKER in head or MARKER in open(full, encoding="utf-8").read()[-80:]:
                os.remove(full)
    return len(wanted)
