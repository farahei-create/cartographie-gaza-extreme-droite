# -*- coding: utf-8 -*-
"""Décision de publication. Aucune phrase ne sort d'ici sans contrôle déterministe.

Le modèle propose. Cette étape relit la page déjà téléchargée et écarte.
"""
import os
import datetime
import re

import admin_content

from tools.daily.textutil import (
    THEMES,
    causal_missing,
    classify_office,
    date_in_text,
    fold,
    forbidden_hits,
    french_date,
    has_topic,
    name_in_text,
    name_tokens,
    norm_literal,
    parse_french_date,
    private_cue,
    public_cue,
    short_hash,
    slugify,
)

WINDOW_HOURS = 54
MAX_QUOTES_PER_PAGE = 3
MAX_QUOTES_PER_PERSON = 2
MAX_QUOTES_PER_OUTLET = 4
MIN_QUOTE = 12
MAX_QUOTE = 500
# Une phrase déjà en ligne plus courte que ça peut être un fragment trop banal.
DUP_CONTAINS = 18
ELLIPSIS = re.compile(r"\s*(?:\[\s*(?:…|\.\.\.)\s*\]|…|\.\.\.)\s*")


def load_index(data):
    nodes = []
    quotes = []
    urls = set()
    for node in data.get("nodes") or []:
        nodes.append(node)
        for statement in node.get("statements") or []:
            if statement.get("quote"):
                quotes.append(statement["quote"])
            if statement.get("url"):
                urls.add(statement["url"])
    return {"nodes": nodes, "quotes": quotes, "urls": urls, "ids": {n["id"] for n in nodes}}


def _window(text, quote, radius=700):
    page = norm_literal(text)
    parts = split_ellipsis(quote)
    needle = parts[0] if parts else ""
    if not needle:
        return ""
    at = page.find(needle)
    if at < 0:
        return ""
    return page[max(0, at - radius): at + len(needle) + radius]


def _word(char):
    return char.isalnum() or char in "'’"


def bounded(text, start, end):
    """Le passage commence et finit sur un mot entier."""
    if start < 0 or end > len(text) or start >= end:
        return False
    if start > 0 and _word(text[start - 1]) and _word(text[start]):
        return False
    if end < len(text) and _word(text[end - 1]) and _word(text[end]):
        return False
    return True


def ends_clean(text, end):
    """Fin de phrase, ou fin du passage entre guillemets. Pas la suite d'une phrase."""
    if end <= 0 or end > len(text):
        return False
    if text[end - 1] in ".!?…":
        return True
    rest = text[end:].lstrip()
    return (not rest) or rest[0] in "»\"”"


def split_ellipsis(quote):
    needle = norm_literal(quote)
    if not needle or not ELLIPSIS.search(needle):
        return [needle] if needle else []
    return [part.strip() for part in ELLIPSIS.split(needle) if part.strip()]


def quoted_spans(page):
    """Repère les passages entre guillemets avant de normaliser toute la page."""
    raw = page or ""
    spans = []
    for pattern in (r"«([^»]{8,800})»", r"“([^”]{8,800})”", r'"([^"\n]{8,800})"'):
        spans.extend(norm_literal(match.group(1)) for match in re.finditer(pattern, raw))
    return [span for span in spans if span]


def ground_quote(quote, text):
    """'' si la citation est entière et fidèle. Jamais une coupe au milieu d'un mot."""
    raw = norm_literal(quote)
    parts = split_ellipsis(quote)
    page = norm_literal(text)
    if not parts or sum(len(part) for part in parts) < MIN_QUOTE:
        return "citation trop courte"
    if len(raw) > MAX_QUOTE:
        return "citation trop longue"
    trailing = bool(re.search(r"(?:…|\.\.\.)\s*$", raw))
    if trailing and len(parts) < 2:
        return "points de suspension ajoutés en fin de citation"
    spans = quoted_spans(text)
    if len(parts) == 1:
        needle = parts[0]
        if needle not in page:
            return "citation absente de la page"
        if not any(needle in span for span in spans):
            return "citation non présentée entre guillemets"
        at = page.find(needle)
        if not bounded(page, at, at + len(needle)):
            return "citation coupée au milieu d'un mot"
        if not ends_clean(page, at + len(needle)):
            return "citation coupée au milieu d'une phrase"
        return ""
    if any(len(part) < 8 for part in parts):
        return "ellipse au milieu d'un mot"
    saw_broken_word = False
    for span in spans:
        pos = 0
        broken = False
        missing = False
        for part in parts:
            at = span.find(part, pos)
            if at < 0:
                missing = True
                break
            if not bounded(span, at, at + len(part)):
                broken = True
                break
            pos = at + len(part)
        if missing or broken:
            saw_broken_word = saw_broken_word or broken
            continue
        if ends_clean(span, pos):
            return ""
        return "citation coupée au milieu d'une phrase"
    if saw_broken_word:
        return "ellipse au milieu d'un mot"
    return "ellipse : un segment n'est pas dans la page tel quel"


def duplicate(quote, quotes):
    needle = norm_literal(quote).lower()
    if not needle:
        return False
    for old in quotes:
        other = norm_literal(old).lower()
        if not other:
            continue
        if needle == other:
            return True
        short, long = (needle, other) if len(needle) <= len(other) else (other, needle)
        if len(short) >= DUP_CONTAINS and short in long:
            return True
    return False


def date_in_window(iso, now):
    try:
        day = datetime.date.fromisoformat(iso)
    except ValueError:
        return False
    if day > now.date():
        return False
    start = datetime.datetime.combine(day, datetime.time.min, tzinfo=now.tzinfo)
    end = datetime.datetime.combine(day, datetime.time.max, tzinfo=now.tzinfo)
    window_start = now - datetime.timedelta(hours=WINDOW_HOURS)
    return start <= now and end >= window_start


def supported_date(iso, page):
    """La date proposée est celle de la page, ou celle du flux si la page n'en donne pas d'autre."""
    if date_in_text(iso, page.get("text") or ""):
        return True
    meta = page.get("dates") or []
    if iso in meta:
        return True
    feed = page.get("feed_date") or ""
    if feed == iso and not meta:
        visible = parse_french_date(page.get("text") or "")
        return not visible or visible == iso
    return False


def _match_nodes(person_name, page_text, nodes):
    hits = []
    for node in nodes:
        if name_in_text(node.get("name") or "", person_name) and name_in_text(node.get("name") or "", page_text):
            hits.append(node)
        elif name_in_text(person_name, node.get("name") or "") and name_in_text(node.get("name") or "", page_text):
            hits.append(node)
    exact = [n for n in hits if fold(n.get("name")) == fold(person_name)]
    if len(exact) == 1:
        return exact[0], None
    # Un seul nœud dont le nom est contenu dans celui proposé, ou l'inverse.
    uniq = []
    seen = set()
    for node in hits:
        if node["id"] not in seen:
            uniq.append(node)
            seen.add(node["id"])
    if len(uniq) == 1:
        return uniq[0], None
    if len(uniq) > 1:
        return None, "plusieurs fiches portent ce nom"
    return None, None


def _host_blocked(url):
    from urllib.parse import urlparse
    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return True
    if host.startswith("www."):
        bare = host[4:]
    else:
        bare = host
    from tools.daily.textutil import BLOCKED_HOST_SUFFIXES
    return any(bare == s or bare.endswith("." + s) or host == s for s in BLOCKED_HOST_SUFFIXES)


def _pending(page, reason, person="", quote="", date="", detail=""):
    url = page.get("url") or ""
    title = (page.get("title") or "")[:180]
    # Un particulier ou un mot interdit ne reste pas en clair dans le dépôt public.
    if forbidden_hits(quote) or reason.startswith("mot interdit"):
        quote = ""
        if not reason.startswith("mot interdit"):
            reason = "mot interdit dans la citation"
    if reason.startswith("particulier"):
        person, quote = "", ""
    elif forbidden_hits(person):
        person = ""
    return {
        "kind": "pending",
        "id": short_hash(url, reason, person, quote),
        "reason": reason[:180],
        "detail": (detail or "")[:120],
        "person": (person or "")[:120],
        "date": date or "",
        "quote": (quote or "")[:500],
        "url": url,
        "title": title,
        "outlet": page.get("outlet") or "",
    }


def _theme(raw, section):
    theme = (raw.get("theme") or "").strip()
    if theme in THEMES:
        return theme
    if section == "gaza":
        return "Gaza – déclarations"
    return "France – normalisation de l'extrême droite"


def _medium(page, iso, context, denial):
    outlet = (page.get("outlet") or "Source").strip()
    if forbidden_hits(outlet):
        outlet = "Source"
    text = "%s, page du %s. La phrase est reproduite telle que cette page la publie." % (outlet, french_date(iso))
    ctx = norm_literal(context)
    if ctx and not forbidden_hits(ctx) and norm_literal(ctx) in norm_literal(page.get("text") or ""):
        text += " La page précise : " + ctx
    den = norm_literal(denial)
    if den and not forbidden_hits(den) and norm_literal(den) in norm_literal(page.get("text") or ""):
        text += " Précision ou réponse dans la même page : " + den
    return text


def _video(raw, page):
    url = (raw.get("video_url") or "").strip()
    html = page.get("html") or ""
    if not url.startswith("https://") or url not in html or _host_blocked(url):
        return None
    from urllib.parse import urlparse
    host = (urlparse(url).hostname or "").lower()
    allowed = (
        "youtube.com", "www.youtube.com", "youtu.be", "www.youtube-nocookie.com",
        "www.tf1info.fr", "www.franceinfo.fr", "www.francetvinfo.fr", "www.bfmtv.com",
        "www.cnews.fr", "www.lci.fr", "www.europe1.fr", "www.rtl.fr",
        "www.radiofrance.fr", "www.sudradio.fr", "www.lemonde.fr", "www.lefigaro.fr",
        "www.liberation.fr", "www.lejdd.fr", "www.huffingtonpost.fr", "lcp.fr", "www.lcp.fr",
        "www.assemblee-nationale.fr",
    )
    if host not in allowed:
        return None
    video = {
        "url": url,
        "platform": host[4:] if host.startswith("www.") else host,
        "title": (page.get("title") or "Vidéo")[:140],
        "source": page.get("outlet") or host,
    }
    if "youtube" in host or host == "youtu.be":
        import re
        found = re.search(r"(?:v=|youtu\.be/|embed/)([\w-]{11})", url)
        if not found:
            return None
        video["platform"] = "youtube"
        video["id"] = found.group(1)
    return video


def review_item(raw, page, index, now, accepted_quotes, new_ids, new_people):
    """Retourne un dict kind=publish ou kind=pending."""
    person_name = norm_literal(raw.get("person_name") or "")
    quote = norm_literal(raw.get("quote") or "")
    page_text = page.get("text") or ""
    doubt = norm_literal(raw.get("doubt") or "")

    if not quote or len(quote) < MIN_QUOTE:
        return _pending(page, "citation trop courte", person_name)
    if len(quote) > MAX_QUOTE:
        return _pending(page, "citation trop longue", person_name, quote)
    hits = forbidden_hits(quote)
    if hits:
        return _pending(page, "mot interdit dans la citation", person_name, quote, detail=hits[0])
    grounded = ground_quote(quote, page_text)
    if grounded:
        return _pending(page, grounded, person_name, quote)

    iso = parse_french_date(raw.get("date") or "")
    if not iso:
        return _pending(page, "date illisible", person_name, quote)
    if not date_in_window(iso, now):
        return _pending(page, "date hors de la fenêtre", person_name, quote, iso)
    if not supported_date(iso, page):
        return _pending(page, "date absente de la page", person_name, quote, iso)

    url = page.get("url") or ""
    if not url.startswith("https://") or _host_blocked(url):
        return _pending(page, "source non publiable", person_name, quote, iso)
    if duplicate(quote, list(index["quotes"]) + list(accepted_quotes)):
        return _pending(page, "déjà en ligne", person_name, quote, iso)

    window = _window(page_text, quote)
    if not window:
        return _pending(page, "citation absente de la page", person_name, quote, iso)
    if not has_topic(window) and not has_topic(quote):
        return _pending(page, "hors des deux sujets", person_name, quote, iso)
    if person_name and not name_in_text(person_name, window) and not name_in_text(person_name, page_text):
        return _pending(page, "nom absent de la page", person_name, quote, iso)
    if person_name and not name_in_text(person_name, window):
        return _pending(page, "citation éloignée du nom", person_name, quote, iso)

    if doubt:
        clean = "doute signalé par la relecture" if forbidden_hits(doubt) else "doute : " + doubt[:140]
        return _pending(page, clean, person_name, quote, iso)

    node, ambiguous = _match_nodes(person_name, page_text, index["nodes"])
    if node is None:
        for candidate in new_people.values():
            if fold(candidate["name"]) == fold(person_name) or name_in_text(candidate["name"], person_name):
                node = candidate
                ambiguous = None
                break
    if ambiguous:
        return _pending(page, ambiguous, person_name, quote, iso)

    section = (raw.get("section") or "").strip()
    if section not in ("gaza", "france"):
        section = "gaza" if has_topic(quote) and "gaza" in fold(window) else "france"
        if "gaza" in fold(quote) or "gaza" in fold(window) or "palestin" in fold(window) or "israel" in fold(window):
            if not any(k in fold(window) for k in ("extreme droite", "rassemblement national", "immigration", "reconquete")):
                section = "gaza"

    person = None
    if node is None:
        role = norm_literal(raw.get("public_role") or "")
        near = window
        if not role or norm_literal(role) not in norm_literal(page_text):
            return _pending(page, "personnalité publique non établie par la page", person_name, quote, iso)
        if private_cue(near) and not public_cue(near):
            return _pending(page, "particulier", person_name, quote, iso)
        office = classify_office(role) or classify_office(near)
        if not office:
            return _pending(page, "personnalité publique non établie par la page", person_name, quote, iso)
        if len(name_tokens(person_name)) < 2:
            return _pending(page, "nom incomplet", person_name, quote, iso)
        pid = slugify(person_name)
        if not pid or pid in index["ids"] or pid in new_ids:
            return _pending(page, "identifiant déjà pris", person_name, quote, iso)
        category, sub = office
        description = person_name + ". La page présente cette personne comme : " + role + "."
        if forbidden_hits(role) or forbidden_hits(description) or forbidden_hits(person_name):
            return _pending(page, "mot interdit dans la fiche", person_name, "", iso, detail=(forbidden_hits(role) or forbidden_hits(description) or [""])[0])
        if causal_missing(description, page_text):
            return _pending(page, "lien de causalité absent de la page", person_name, quote, iso)
        # 28/11 : plus aucune fiche créée automatiquement. La phrase va dans la file
        # d'attente (page admin) ; la fiche se crée à la main, avec une source vérifiée.
        if not os.environ.get("ONRECORD_AUTO_PEOPLE"):
            return _pending(page, PERSON_MISSING, person_name, quote, iso)
        person = {
            "id": pid,
            "name": person_name,
            "type": "person",
            "role": role[:180],
            "description": description[:400],
            "category": category,
            "subcategory": sub,
            "sections": [section],
        }
        person_id = pid
    else:
        person_id = node["id"]

    medium = _medium(page, iso, raw.get("context") or "", raw.get("denial") or "")
    if forbidden_hits(medium):
        return _pending(page, "mot interdit dans le contexte", person_name, quote, iso, detail=forbidden_hits(medium)[0])
    if causal_missing(medium, page_text):
        return _pending(page, "lien de causalité absent de la page", person_name, quote, iso)

    statement = {
        "person_id": person_id,
        "quote": quote,
        "date": iso,
        "medium": medium,
        "url": url,
        "theme": _theme(raw, section),
        "section": section,
    }
    video = _video(raw, page)
    if video:
        statement["video"] = video

    known = set(index["ids"]) | set(new_ids)
    payload = {"people": [person] if person else [], "statements": [statement], "edges": [], "photos": []}
    errors = admin_content.validate(payload, known if not person else known)
    # Une fiche nouvelle ne doit pas déjà être dans known : validate l'exige.
    if person:
        errors = admin_content.validate(payload, set(index["ids"]) | set(new_ids))
    if errors:
        return _pending(page, "contrôle du fichier : " + errors[0][:140], person_name, quote, iso)

    return {
        "kind": "publish",
        "person": person,
        "statement": statement,
        "label": person_name,
    }


PERSON_MISSING = "personne sans fiche dans l'archive : à créer à la main dans l'admin"


def review_pages(pages, proposals, index, now):
    """proposals : {url: [raw, ...]} ou {url: Exception message}."""
    published = []
    pending = []
    accepted = []
    new_ids = set()
    new_people = {}
    notes = []
    per_person = {}
    per_outlet = {}
    for page in pages:
        url = page.get("url") or ""
        got = proposals.get(url)
        if isinstance(got, str):
            pending.append(_pending(page, got))
            continue
        items = list(got or [])
        if not items:
            if len(norm_literal(page.get("text") or "")) < 400:
                pending.append(_pending(page, "page trop courte pour être relue"))
            else:
                pending.append(_pending(page, "aucune citation exacte retenue"))
            continue
        kept = 0
        for raw in items:
            if kept >= MAX_QUOTES_PER_PAGE:
                pending.append(_pending(page, "plafond de phrases pour cette page", raw.get("person_name") or "", raw.get("quote") or ""))
                continue
            result = review_item(raw, page, index, now, accepted, new_ids, new_people)
            if result["kind"] == "publish":
                person_key = fold(result.get("label") or result["statement"]["person_id"])
                outlet_key = fold(page.get("outlet") or "")
                if per_person.get(person_key, 0) >= MAX_QUOTES_PER_PERSON:
                    pending.append(_pending(
                        page, "plafond : deux phrases déjà retenues pour cette personne",
                        result.get("label") or "", result["statement"]["quote"], result["statement"]["date"]))
                    continue
                if outlet_key and per_outlet.get(outlet_key, 0) >= MAX_QUOTES_PER_OUTLET:
                    pending.append(_pending(
                        page, "plafond : ce média a déjà plusieurs phrases dans ce relevé",
                        result.get("label") or "", result["statement"]["quote"], result["statement"]["date"]))
                    continue
                published.append(result)
                accepted.append(result["statement"]["quote"])
                per_person[person_key] = per_person.get(person_key, 0) + 1
                if outlet_key:
                    per_outlet[outlet_key] = per_outlet.get(outlet_key, 0) + 1
                if result["person"]:
                    new_ids.add(result["person"]["id"])
                    new_people[result["person"]["id"]] = result["person"]
                kept += 1
            else:
                pending.append(result)
        notes.append("%s : %d publiée(s)" % (url, kept))
    return {"published": published, "pending": pending, "notes": notes}
