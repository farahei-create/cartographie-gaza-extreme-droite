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


def apply(N, E, PIMG=None):
    path = _path()
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if not any(data.get(key) for key in ("people", "statements", "edges", "photos")):
        return
    known = {n["id"] for n in N}
    errors = admin_content.validate(data, known)
    if errors:
        raise SystemExit("auto_published.json refusé :\n- " + "\n- ".join(errors))
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
