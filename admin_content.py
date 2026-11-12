# -*- coding: utf-8 -*-
"""Applique tools/admin_additions.json à la fin de build.py.

Le fichier est la source écrite par /admin.html. Il ne remplace pas les modules
v24, v26, v35, etc. Une personne déjà présente n'est pas réécrite.
"""
import datetime
import json
import os
import re
from urllib.parse import urlparse

CATEGORIES = {
    "Responsables politiques",
    "Médias & propriétaires",
    "Journalistes & éditorialistes",
    "Intellectuels & essayistes",
    "Organisations & institutions",
    "Événements",
}
SECTIONS = {"gaza", "france"}
NATURES = {"ascension", "opposition", "autre"}
FORBIDDEN = (
    "complice", "génocidaire", "genocidaire", "pantin", "infiltré", "infiltre",
    "marionnette", "protégé", "protege", "copinage", "occulte",
)
PHOTO_HOSTS = {
    "commons.wikimedia.org",
    "upload.wikimedia.org",
    "www.europarl.europa.eu",
    "europarl.europa.eu",
    "www.assemblee-nationale.fr",
    "assemblee-nationale.fr",
    "www.senat.fr",
    "senat.fr",
}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _path():
    env = os.environ.get("ONRECORD_ADMIN_JSON")
    if env:
        return env
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "tools", "admin_additions.json")


def _host(url):
    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return ""
    if host.startswith("www.") and host.count(".") > 1:
        return host
    return host


def _https(url):
    try:
        u = urlparse(url or "")
    except Exception:
        return False
    return u.scheme == "https" and bool(u.hostname) and "." in u.hostname


def _wiki(url):
    host = _host(url)
    return host == "wikipedia.org" or host.endswith(".wikipedia.org")


def _bad_words(text):
    low = (text or "").lower()
    return [w for w in FORBIDDEN if w in low]


def _need(errors, cond, msg):
    if not cond:
        errors.append(msg)


def _medium(st):
    medium = (st.get("medium") or "").strip()
    ctx = (st.get("context") or "").strip()
    den = (st.get("denial") or "").strip()
    parts = [medium] if medium else []
    if ctx:
        parts.append("Contexte : " + ctx)
    if den:
        parts.append("Précision ou réponse : " + den)
    return " ".join(parts).strip()


def _video(raw):
    if not raw:
        return None
    if isinstance(raw, str):
        url = raw.strip()
        title, source = "", ""
        platform = _host(url)
    else:
        url = (raw.get("url") or "").strip()
        title = (raw.get("title") or "").strip()
        source = (raw.get("source") or "").strip()
        platform = (raw.get("platform") or _host(url) or "").strip()
    if not url:
        return None
    out = {"url": url, "platform": platform or _host(url), "title": title or "Vidéo", "source": source or platform or _host(url)}
    return out


def _license_ok(lic):
    low = (lic or "").lower()
    if re.search(r"(^|[^a-z])nc([^a-z]|$)", low) or re.search(r"(^|[^a-z])nd([^a-z]|$)", low):
        return False
    if "noncommercial" in low or "non-commercial" in low or "no derivatives" in low:
        return False
    hints = ("cc by", "cc-by", "cc0", "cc-0", "public domain", "domaine public", "portrait officiel")
    return any(h in low for h in hints)


def validate(data, known_ids):
    """Retourne une liste de messages. known_ids : identifiants déjà dans le site."""
    errors = []
    people = data.get("people") or []
    statements = data.get("statements") or []
    edges = data.get("edges") or []
    photos = data.get("photos") or []
    if not isinstance(people, list) or not isinstance(statements, list) or not isinstance(edges, list) or not isinstance(photos, list):
        return ["Le fichier admin n'a pas la forme attendue (listes people, statements, edges, photos)."]
    new_ids = []
    for p in people:
        pid = (p.get("id") or "").strip()
        _need(errors, ID_RE.match(pid or ""), "Identifiant invalide : " + (pid or "(vide)"))
        _need(errors, pid not in known_ids, "Identifiant déjà utilisé : " + pid)
        _need(errors, pid not in new_ids, "Identifiant en double dans le fichier : " + pid)
        new_ids.append(pid)
        _need(errors, (p.get("name") or "").strip(), "Nom manquant pour " + pid)
        _need(errors, (p.get("role") or "").strip(), "Fonction manquante pour " + pid)
        _need(errors, (p.get("description") or "").strip(), "Description manquante pour " + pid)
        _need(errors, p.get("type") in ("person", "org"), "Type invalide pour " + pid)
        _need(errors, p.get("category") in CATEGORIES, "Catégorie inconnue pour " + pid)
        _need(errors, (p.get("subcategory") or "").strip(), "Sous-catégorie manquante pour " + pid)
        secs = p.get("sections") or []
        _need(errors, isinstance(secs, list) and secs and set(secs) <= SECTIONS, "Section invalide pour " + pid)
        for field in ("name", "role", "description", "subcategory"):
            hit = _bad_words(p.get(field) or "")
            if hit:
                errors.append("Mot à retirer dans " + field + " (" + pid + ") : " + ", ".join(hit))
        if p.get("type") == "person":
            has = any((s.get("person_id") or s.get("person")) == pid for s in statements)
            _need(errors, has, "Ajoute une déclaration sourcée pour " + (p.get("name") or pid) + " (une personne nouvelle en a besoin).")
    all_ids = set(known_ids) | set(new_ids)
    for s in statements:
        pid = (s.get("person_id") or s.get("person") or "").strip()
        _need(errors, pid in all_ids, "Déclaration : personne inconnue (" + pid + ")")
        _need(errors, (s.get("quote") or "").strip(), "Citation vide (" + pid + ")")
        date = (s.get("date") or "").strip()
        try:
            datetime.date.fromisoformat(date)
        except Exception:
            errors.append("Date invalide (" + pid + ") : " + date)
        medium = _medium(s)
        _need(errors, medium, "Média manquant (" + pid + ")")
        hit = _bad_words(medium)
        if hit:
            errors.append("Mot à retirer dans le média ou le contexte (" + pid + ") : " + ", ".join(hit))
        url = (s.get("url") or "").strip()
        _need(errors, _https(url), "URL de source invalide (" + pid + ")")
        if _wiki(url):
            errors.append("Wikipédia ne peut pas être la source (" + pid + ")")
        _need(errors, (s.get("theme") or "").strip(), "Thème manquant (" + pid + ")")
        _need(errors, (s.get("section") or "") in SECTIONS, "Section de déclaration invalide (" + pid + ")")
        vid = _video(s.get("video"))
        if vid:
            _need(errors, _https(vid["url"]), "URL de vidéo invalide (" + pid + ")")
            if _wiki(vid["url"]):
                errors.append("La vidéo ne peut pas être une page Wikipédia (" + pid + ")")
    for e in edges:
        src = (e.get("source") or "").strip()
        tgt = (e.get("target") or "").strip()
        _need(errors, src in all_ids and tgt in all_ids and src != tgt, "Lien : entités invalides (" + src + " → " + tgt + ")")
        rel = (e.get("relation") or "").strip()
        _need(errors, rel, "Lien sans relation")
        hit = _bad_words(rel)
        if hit:
            errors.append("Mot à retirer dans la relation : " + ", ".join(hit))
        url = (e.get("url") or "").strip()
        _need(errors, _https(url), "Lien : URL de source invalide")
        if _wiki(url):
            errors.append("Wikipédia ne peut pas être la seule source d'un lien")
        date = (e.get("date") or "").strip()
        try:
            datetime.date.fromisoformat(date)
        except Exception:
            errors.append("Lien : date invalide (" + date + ")")
        _need(errors, (e.get("section") or "france") in SECTIONS, "Lien : section invalide")
        nat = e.get("nature") or "autre"
        _need(errors, nat in NATURES, "Lien : nature invalide")
    for ph in photos:
        pid = (ph.get("id") or "").strip()
        _need(errors, pid in all_ids or pid in new_ids, "Photo : personne inconnue (" + pid + ")")
        _need(errors, (ph.get("image") or "").startswith("img/people/") and ph.get("image", "").endswith(".webp"), "Photo : chemin WebP attendu pour " + pid)
        cr = ph.get("image_credit") or {}
        _need(errors, (cr.get("author") or "").strip(), "Photo : auteur manquant (" + pid + ")")
        _need(errors, _license_ok(cr.get("license") or ""), "Photo : licence non autorisée (" + pid + ")")
        _need(errors, _https(cr.get("license_url") or ""), "Photo : lien de licence invalide (" + pid + ")")
        src = (cr.get("source_url") or "").strip()
        _need(errors, _https(src), "Photo : URL de la source invalide (" + pid + ")")
        _need(errors, _host(src) in PHOTO_HOSTS, "Photo : source Commons ou portrait officiel seulement (" + pid + ")")
    return errors


def apply(N, E, PIMG=None):
    path = _path()
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not any(data.get(k) for k in ("people", "statements", "edges", "photos")):
        return
    known = {n["id"] for n in N}
    errors = validate(data, known)
    if errors:
        raise SystemExit("admin_additions.json refusé :\n- " + "\n- ".join(errors))
    by = {n["id"]: n for n in N}
    for p in data.get("people") or []:
        pid = p["id"].strip()
        node = {
            "id": pid,
            "name": p["name"].strip(),
            "type": p["type"],
            "role": p["role"].strip(),
            "description": p["description"].strip(),
            "statements": [],
            "sections": list(p["sections"]),
            "category": p["category"],
            "subcategory": p["subcategory"].strip(),
        }
        N.append(node)
        by[pid] = node
    for s in data.get("statements") or []:
        pid = (s.get("person_id") or s["person"]).strip()
        n = by[pid]
        quote = s["quote"].strip()
        if any(x.get("quote") == quote for x in n.get("statements") or []):
            continue
        row = {
            "quote": quote,
            "date": s["date"].strip(),
            "medium": _medium(s),
            "url": s["url"].strip(),
            "theme": s["theme"].strip(),
            "section": s["section"],
        }
        vid = _video(s.get("video"))
        if vid:
            row["video"] = vid
        n.setdefault("statements", []).append(row)
    for e in data.get("edges") or []:
        src, tgt = e["source"].strip(), e["target"].strip()
        url = e["url"].strip()
        rel = e["relation"].strip()
        if any(x.get("source") == src and x.get("target") == tgt and x.get("url") == url and x.get("relation") == rel for x in E):
            continue
        E.append({
            "source": src,
            "target": tgt,
            "relation": rel,
            "url": url,
            "date": e["date"].strip(),
            "section": e.get("section") or "france",
            "nature": e.get("nature") or "autre",
        })
    if PIMG:
        for n in N:
            if n["id"] in PIMG:
                n.update(PIMG[n["id"]])
    for ph in data.get("photos") or []:
        n = by[ph["id"].strip()]
        n["image"] = ph["image"]
        n["image_credit"] = {
            "author": ph["image_credit"]["author"].strip(),
            "license": ph["image_credit"]["license"].strip(),
            "license_url": ph["image_credit"]["license_url"].strip(),
            "source_url": ph["image_credit"]["source_url"].strip(),
        }
        if ph["image_credit"].get("file"):
            n["image_credit"]["file"] = ph["image_credit"]["file"]
    for p in data.get("people") or []:
        n = by[p["id"].strip()]
        if n.get("type") == "person" and not n.get("parcours"):
            sts = sorted(n.get("statements") or [], key=lambda x: x.get("date") or "")
            s0 = sts[0]
            src = (s0.get("medium") or "source").split(".")[0][:80]
            n["parcours"] = [{
                "date": s0["date"],
                "title": (n.get("role") or n["name"])[:90],
                "text": n.get("description") or n.get("role") or n["name"],
                "url": s0["url"],
                "source": src or "source",
            }]
