# -*- coding: utf-8 -*-
"""Journal des problèmes du relevé automatique : incidents.json (page admin, catégorie « Problèmes »).

Chaque entrée : id, at (UTC), kind, title (français simple), detail, count, resolved.
Un même problème non réglé n'est pas dupliqué : son compteur monte.
Les noms des fournisseurs d'IA ne sont jamais écrits ici : « IA principale », « IA de secours ».
Usage en ligne de commande :
  python3 -m tools.daily.incidents add <kind> "<titre>" ["<détail>"]
"""
import datetime
import hashlib
import json
import os
import sys

MAX_ITEMS = 200
NOTICE = "Journal des problèmes du relevé automatique. Lu par la page admin. Pas lié depuis le site."


def _root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def path(root=None):
    return os.environ.get("ONRECORD_INCIDENTS_JSON") or os.path.join(root or _root(), "incidents.json")


def load(root=None):
    try:
        with open(path(root), encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, dict) and isinstance(data.get("items"), list):
            return data
    except (OSError, ValueError):
        pass
    return {"_notice": NOTICE, "items": []}


def save(data, root=None):
    data["_notice"] = NOTICE
    data["items"] = sorted(data.get("items") or [], key=lambda it: it.get("at") or "", reverse=True)[:MAX_ITEMS]
    with open(path(root), "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def add(kind, title, detail="", key=None, root=None):
    """Ajoute (ou incrémente) un incident. Ne lève jamais d'exception."""
    try:
        data = load(root)
        ident = hashlib.sha1(("%s|%s" % (kind, key or title)).encode("utf-8")).hexdigest()[:12]
        stamp = now_utc()
        for item in data["items"]:
            if item.get("id") == ident and not item.get("resolved"):
                item["count"] = int(item.get("count") or 1) + 1
                item["at"] = stamp
                if detail:
                    item["detail"] = str(detail)[:600]
                save(data, root)
                return True
        data["items"].append({
            "id": ident if not any(i.get("id") == ident for i in data["items"]) else ident + stamp[-9:-1].replace(":", ""),
            "at": stamp,
            "kind": kind,
            "title": str(title)[:200],
            "detail": str(detail or "")[:600],
            "count": 1,
            "resolved": False,
        })
        save(data, root)
        return True
    except Exception as exc:  # le journal ne doit jamais casser le relevé
        sys.stderr.write("incident non écrit : %s\n" % exc)
        return False


def enabled():
    """Le build n'écrit le journal que dans le workflow (pas dans les tests)."""
    return os.environ.get("ONRECORD_LOG_INCIDENTS") == "1"


def main(argv):
    if len(argv) >= 4 and argv[1] == "add":
        add(argv[2], argv[3], argv[4] if len(argv) > 4 else "")
        print("Incident noté :", argv[3])
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
