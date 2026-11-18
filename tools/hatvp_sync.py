# -*- coding: utf-8 -*-
"""Met à jour enquete.json depuis l'open data HATVP (liste CSV + XML public).

Ne recopie pas : adresse, date de naissance, e-mail, téléphone, nom du conjoint,
patrimoine, enfants, ni les mentions « Données non publiées ».
Licence des fichiers HATVP : Licence Ouverte Etalab.
"""
import csv
import io
import json
import os
import re
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIST_URL = "https://www.hatvp.fr/livraison/opendata/liste.csv"
XML_URL = "https://www.hatvp.fr/livraison/merge/declarations.xml"
OUT = os.path.join(ROOT, "enquete.json")
UA = "Onrecord/1.0 (archive citoyenne; +https://onrecord-fr.vercel.app/)"
FORBIDDEN = (
    "complice", "génocidaire", "genocidaire", "pantin", "infiltré", "infiltre",
    "marionnette", "protégé", "protege", "copinage", "occulte",
)
OWNER_WORDS = ("propriétaire", "actionnaire", "filiale", "maison-mère", "maison mere")


def norm_name(text):
    text = unicodedata.normalize("NFD", text or "")
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.upper().replace("-", " ").replace("'", " ")
    text = re.sub(r"[^A-Z ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean(text):
    text = " ".join((text or "").replace("\xa0", " ").split())
    if not text or "non publi" in text.lower():
        return ""
    low = text.lower()
    if any(word in low for word in FORBIDDEN):
        return ""
    return text


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as res:
        return res.read()


def site_people():
    data = json.load(open(os.path.join(ROOT, "data.json"), encoding="utf-8"))
    people = {}
    for node in data.get("nodes") or []:
        if node.get("type") != "person":
            continue
        people[norm_name(node.get("name") or "")] = node["id"]
    return data, people


def match_csv(raw, people):
    text = raw.decode("utf-8", "replace")
    rows = csv.DictReader(io.StringIO(text), delimiter=";")
    best = {}
    for row in rows:
        if row.get("statut_publication") != "Livrée":
            continue
        if row.get("type_document") not in ("di", "dia"):
            continue
        key = norm_name((row.get("prenom") or "") + " " + (row.get("nom") or ""))
        if key not in people:
            continue
        date = (row.get("date_publication") or "")[:10]
        prev = best.get(key)
        if prev and prev["published"] >= date:
            continue
        dossier = row.get("url_dossier") or ""
        url = "https://www.hatvp.fr" + dossier if dossier.startswith("/") else "https://www.hatvp.fr/pages_nominatives/"
        best[key] = {
            "person_id": people[key],
            "published": date,
            "document": row.get("type_document") or "",
            "qualite": clean(row.get("qualite") or ""),
            "url": url,
        }
    return best


def fact(value, date, url):
    value = clean(value)
    if not value:
        return None
    return {"value": value, "date": (date or "")[:10], "url": url}


def add_item(bucket, value, date, url):
    item = fact(value, date, url)
    if item and item not in bucket:
        bucket.append(item)


def read_items(el, dto):
    node = el.find(dto)
    if node is None:
        return []
    return node.findall("items/items")


def extract(el, meta):
    url = meta["url"]
    mandates, activities, participations, collaborators, spouse = [], [], [], [], []
    for it in read_items(el, "mandatElectifDto"):
        desc = clean(it.findtext("descriptionMandat"))
        start = clean(it.findtext("dateDebut"))
        end = clean(it.findtext("dateFin"))
        when = start + (" – " + end if end else "")
        add_item(mandates, (desc + (" (" + when + ")") if when else desc), start, url)
    for it in read_items(el, "activProfCinqDerniereDto"):
        desc = clean(it.findtext("description"))
        emp = clean(it.findtext("employeur"))
        start = clean(it.findtext("dateDebut"))
        end = clean(it.findtext("dateFin"))
        label = desc
        if emp:
            label = (label + " — " + emp).strip(" —")
        if start or end:
            label += " (" + start + (" – " + end if end else "") + ")"
        add_item(activities, label, start, url)
    for dto in ("participationDirigeantDto", "participationFinanciereDto"):
        for it in read_items(el, dto):
            societe = clean(it.findtext("nomSociete"))
            activ = clean(it.findtext("activite") or it.findtext("description"))
            if not societe and not activ:
                continue
            add_item(participations, (societe + (" — " + activ if activ else "")).strip(" —"), "", url)
    for it in read_items(el, "activCollaborateursDto"):
        prenom = clean(it.findtext("prenom"))
        nom = clean(it.findtext("nom"))
        fonction = clean(it.findtext("fonction") or it.findtext("description") or it.findtext("qualite"))
        who = (prenom + " " + nom).strip()
        if not who and not fonction:
            continue
        add_item(collaborators, (who + (" — " + fonction if fonction else "")).strip(" —"), "", url)
    for it in read_items(el, "activProfConjointDto"):
        # Activité publiée seulement. Jamais le nom du conjoint.
        act = clean(it.findtext("activiteProf"))
        emp = clean(it.findtext("employeurConjoint"))
        label = act
        if emp:
            label = (label + " — " + emp).strip(" —")
        add_item(spouse, label, "", url)
    if not any((mandates, activities, participations, collaborators, spouse)):
        return None
    return {
        "person_id": meta["person_id"],
        "published": meta["published"],
        "document": meta["document"],
        "qualite": meta["qualite"],
        "url": url,
        "mandates": mandates[:12],
        "activities": activities[:12],
        "participations": participations[:12],
        "collaborators": collaborators[:12],
        "spouse_activity": spouse[:4],
    }


def declaration_type(el):
    node = el.find("general/typeDeclaration/id")
    return (node.text or "").strip().upper() if node is not None and node.text else ""


def declaration_name(el):
    nom = el.findtext("general/declarant/nom") or ""
    prenom = el.findtext("general/declarant/prenom") or ""
    return norm_name(prenom + " " + nom)


def declaration_date(el):
    raw = (el.findtext("dateDepot") or "").strip()
    match = re.match(r"(\d{2})/(\d{2})/(\d{4})", raw)
    if not match:
        return ""
    return "%s-%s-%s" % (match.group(3), match.group(2), match.group(1))


def scan_xml(path, matched):
    by_id = {}
    dates = {}
    for event, el in ET.iterparse(path, events=("end",)):
        if el.tag != "declaration":
            continue
        kind = declaration_type(el)
        key = declaration_name(el)
        meta = matched.get(key)
        if kind in ("DI", "DIA") and meta:
            when = declaration_date(el)
            prev = dates.get(meta["person_id"], "")
            if when >= prev:
                parsed = extract(el, meta)
                if parsed:
                    by_id[meta["person_id"]] = parsed
                    dates[meta["person_id"]] = when
        el.clear()
    return by_id


def media_facts(data):
    nodes = {n["id"]: n for n in data.get("nodes") or []}
    facts = []
    for edge in data.get("edges") or []:
        rel = edge.get("relation") or ""
        if not any(word in rel.lower() for word in OWNER_WORDS):
            continue
        url = edge.get("url") or ""
        if not url.startswith("https://"):
            continue
        for side in ("source", "target"):
            node = nodes.get(edge.get(side) or "")
            if not node or node.get("subcategory") not in ("Chaînes, radios & titres", "Édition"):
                continue
            other = nodes.get(edge["target"] if side == "source" else edge["source"])
            if not other:
                continue
            item = fact(other["name"] + " — " + rel, edge.get("date") or "", url)
            if not item:
                continue
            item["media_id"] = node["id"]
            item["owner_id"] = other["id"]
            facts.append(item)
    return facts


def load_out():
    if not os.path.exists(OUT):
        return {}
    return json.load(open(OUT, encoding="utf-8"))


def main():
    data, people = site_people()
    print("Personnes du site :", len(people))
    matched = match_csv(fetch(LIST_URL), people)
    print("Déclarations d'intérêts publiées repérées :", len(matched))
    xml_path = "/tmp/hatvp-declarations.xml"
    if not os.path.exists(xml_path) or os.path.getsize(xml_path) < 1000000:
        print("Téléchargement du XML HATVP…")
        blob = fetch(XML_URL)
        open(xml_path, "wb").write(blob)
    hatvp = scan_xml(xml_path, matched)
    print("Fiches avec un extrait :", len(hatvp))
    current = load_out()
    payload = {
        "_notice": "Faits publics. Intérêts : open data HATVP (licence ouverte). Pas d'adresse, pas de patrimoine, pas d'enfants, pas de nom de conjoint. L'activité du conjoint n'est recopiée que si la HATVP la publie.",
        "updated": "2026-11-18",
        "hatvp_list": LIST_URL,
        "hatvp": hatvp,
        "argent": current.get("argent") or [],
        "medias": media_facts(data),
    }
    blob = json.dumps(payload, ensure_ascii=False).lower()
    for banned in ("nomconjoint", "datenaissance", "adresse", "enfant", "patrimoine", "téléphone", "telephone"):
        if '"' + banned + '"' in blob or banned + ":" in blob:
            raise SystemExit("Champ privé dans la sortie : " + banned)
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    open(OUT, "w", encoding="utf-8").write(text)
    print("Écrit", OUT, "médias", len(payload["medias"]))


if __name__ == "__main__":
    main()
