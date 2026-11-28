# -*- coding: utf-8 -*-
"""Applique tools/auto_published.json à la fin de build.py.

Même forme que les ajouts de la page admin. Une personne déjà présente
n'est pas réécrite. Pas de photo : le monogramme reste.
"""
import json
import os

import admin_content


def _path():
    env = os.environ.get("ONRECORD_AUTO_JSON")
    if env:
        return env
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "tools", "auto_published.json")


DEFERRED = []


def _skip(kind, item, why):
    """Un élément refusé est écarté et noté ; il n'arrête jamais le build."""
    who = (item.get("person_id") or item.get("person") or item.get("id") or item.get("source") or "?")
    quote = (item.get("quote") or item.get("relation") or "")[:200]
    print("auto_published.json : élément écarté (%s) — %s" % (who, why))
    try:
        from tools.daily import incidents
        if not incidents.enabled():
            return
        incidents.add("build_refus", "Phrase écartée à la construction du site (%s)" % who,
                      "%s. « %s » — %s. Elle n'est pas en ligne ; elle est dans la File d'attente." % (why, quote, item.get("url") or ""),
                      key="build|" + who + "|" + quote)
        from tools.daily.store import merge_pending, now_paris
        import hashlib
        merge_pending(os.path.dirname(os.path.abspath(__file__)), [{
            "id": hashlib.sha1(("build|" + who + "|" + quote).encode("utf-8")).hexdigest()[:16],
            "reason": "écartée au build : " + why[:120],
            "person": who, "quote": quote, "date": item.get("date") or "", "url": item.get("url") or "",
        }], now_paris().date())
    except Exception as exc:
        print("journal non écrit :", exc)


def _filter(data, known, final):
    """Garde ce qui est valide, élément par élément. Une phrase dont la fiche n'existe
    pas encore (fiche ajoutée par un module vNN plus loin dans build.py) attend la fin."""
    out = {"people": [], "statements": [], "edges": [], "photos": []}
    statements = list(data.get("statements") or [])
    new_ids = set()
    for person in data.get("people") or []:
        pid = (person.get("id") or "").strip()
        if pid in known:
            continue  # fiche déjà là (ajoutée ailleurs) : ses phrases restent
        mine = [s for s in statements if (s.get("person_id") or s.get("person")) == pid]
        errors = admin_content.validate({"people": [person], "statements": mine, "edges": [], "photos": []}, known | new_ids)
        if errors:
            _skip("fiche", person, errors[0])
            continue
        out["people"].append(person)
        new_ids.add(pid)
    ids = known | new_ids
    for statement in statements:
        pid = (statement.get("person_id") or statement.get("person") or "").strip()
        if statement.get("added") and not final:
            DEFERRED.append(statement)  # ajout récent : en fin de build (numéros c/ stables)
            continue
        if pid not in ids:
            if not final:
                DEFERRED.append(statement)
            else:
                _skip("phrase", statement, "personne sans fiche dans l'archive (" + pid + ")")
            continue
        errors = admin_content.validate({"people": [], "statements": [statement], "edges": [], "photos": []}, ids)
        if errors:
            _skip("phrase", statement, errors[0])
            continue
        out["statements"].append(statement)
    for edge in data.get("edges") or []:
        errors = admin_content.validate({"people": [], "statements": [], "edges": [edge], "photos": []}, ids)
        if errors:
            _skip("lien", edge, errors[0])
            continue
        out["edges"].append(edge)
    return out


def apply_deferred(N, E, PIMG=None):
    """À appeler à la fin de build.py, après tous les modules vNN."""
    if not DEFERRED:
        return
    pending = list(DEFERRED)
    del DEFERRED[:]
    apply(N, E, PIMG, data={"people": [], "statements": pending, "edges": [], "photos": []}, final=True)


def apply(N, E, PIMG=None, data=None, final=False):
    if data is None:
        path = _path()
        if not os.path.exists(path):
            return
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    if not any(data.get(key) for key in ("people", "statements", "edges", "photos")):
        return
    known = {n["id"] for n in N}
    data = _filter(data, known, final)
    by = {n["id"]: n for n in N}
    for person in data.get("people") or []:
        pid = person["id"].strip()
        node = {
            "id": pid,
            "name": person["name"].strip(),
            "type": person["type"],
            "role": person["role"].strip(),
            "description": person["description"].strip(),
            "statements": [],
            "sections": list(person["sections"]),
            "category": person["category"],
            "subcategory": person["subcategory"].strip(),
        }
        N.append(node)
        by[pid] = node
    for statement in data.get("statements") or []:
        pid = (statement.get("person_id") or statement.get("person") or "").strip()
        node = by[pid]
        quote = statement["quote"].strip()
        if any(row.get("quote") == quote for row in node.get("statements") or []):
            continue
        row = {
            "quote": quote,
            "date": statement["date"].strip(),
            "medium": admin_content._medium(statement),
            "url": statement["url"].strip(),
            "theme": statement["theme"].strip(),
            "section": statement["section"],
        }
        video = admin_content._video(statement.get("video"))
        if video:
            if isinstance(statement.get("video"), dict) and statement["video"].get("id"):
                video["id"] = statement["video"]["id"]
            row["video"] = video
        node.setdefault("statements", []).append(row)
        if row["section"] not in node.setdefault("sections", []):
            node["sections"].append(row["section"])
    for edge in data.get("edges") or []:
        src, tgt = edge["source"].strip(), edge["target"].strip()
        url = edge["url"].strip()
        rel = edge["relation"].strip()
        if any(item.get("source") == src and item.get("target") == tgt and item.get("url") == url and item.get("relation") == rel for item in E):
            continue
        E.append({
            "source": src,
            "target": tgt,
            "relation": rel,
            "url": url,
            "date": edge["date"].strip(),
            "section": edge.get("section") or "france",
            "nature": edge.get("nature") or "autre",
        })
    if PIMG:
        for node in N:
            if node["id"] in PIMG:
                node.update(PIMG[node["id"]])
    for person in data.get("people") or []:
        node = by[person["id"].strip()]
        if node.get("type") == "person" and not node.get("parcours"):
            statements = sorted(node.get("statements") or [], key=lambda row: row.get("date") or "")
            first = statements[0]
            source = (first.get("medium") or "source").split(".")[0][:80]
            node["parcours"] = [{
                "date": first["date"],
                "title": (node.get("role") or node["name"])[:90],
                "text": node.get("description") or node.get("role") or node["name"],
                "url": first["url"],
                "source": source or "source",
            }]
