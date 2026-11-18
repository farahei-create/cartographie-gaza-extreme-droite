# -*- coding: utf-8 -*-
"""Normalisation et filtres partagés par le relevé du matin.

La comparaison d'une citation avec la page ne change que les espaces et les
apostrophes, plus le tiret insécable et les guillemets qui entourent toute la
phrase. La casse et les accents restent.
"""
import hashlib
import re
import unicodedata

APOSTROPHES = {
    "\u2019": "'",
    "\u2018": "'",
    "\u2032": "'",
    "\u00b4": "'",
    "`": "'",
    "\u201b": "'",
    "\u02bc": "'",
}
SPACES = "\u00a0\u202f\u2007\u2008\u2009\u200a\u200b\ufeff"
WRAP_OPEN = "«\"“"
WRAP_CLOSE = "»\"”"

# Racines sans accent. Le suffixe admis est un pluriel ou un féminin, pas un
# autre mot (« protéger » ne contient pas « protégé »).
FORBIDDEN_STEMS = (
    "complice",
    "genocidaire",
    "pantin",
    "infiltre",
    "marionnette",
    "protege",
    "copinage",
    "occulte",
)
FORBIDDEN_SUFFIXES = ("", "s", "e", "es", "ee", "ees")

MONTHS = (
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
)

THEMES = (
    "Gaza – déclarations",
    "France – normalisation de l'extrême droite",
    "Proximité extrême droite",
    "Médias – structure",
    "Nuance / contexte",
    "France – montée des violences",
)

# Phrases que le site n'écrit pas si la page ne les contient pas.
CAUSAL = (
    "a nomme",
    "a finance",
    "a fait dire",
    "grace a",
)

TOPIC_PHRASES = (
    "gaza",
    "cisjordanie",
    "palestin",
    "israel",
    "hamas",
    "tsahal",
    "rafah",
    "hebron",
    "colonisation",
    "colonie",
    "extreme droite",
    "extreme-droite",
    "ultradroite",
    "ultra-droite",
    "rassemblement national",
    "front national",
    "reconquete",
    "remigration",
    "reimmigration",
    "immigration",
    "migratoire",
    "migrant",
    "identite nationale",
    "grand remplacement",
    "priorite nationale",
    "antisemit",
    "racis",
    "fascis",
    "xenophob",
    "islamophob",
    "musulman",
    "logement social",
    "association politisee",
    "associations politisees",
)

# Indices qu'une personne nommée dans la page n'est pas une personnalité publique.
PRIVATE_CUES = (
    "temoin",
    "habitant",
    "lyceen",
    "lyceenne",
    "collegien",
    "collegienne",
    "mineur",
    "mineure",
    "victime",
    "suspect",
    "prevenu",
    "mis en examen",
    "age de",
    "un homme de",
    "une femme de",
    "auditeur",
    "auditrice",
    "telespectateur",
    "telespectatrice",
    "riverain",
    "passant",
    "un manifestant",
    "une manifestante",
)

PUBLIC_OFFICE = (
    ("ministre", "Responsables politiques", "Gouvernement & exécutif"),
    ("premier ministre", "Responsables politiques", "Gouvernement & exécutif"),
    ("president de la republique", "Responsables politiques", "Gouvernement & exécutif"),
    ("presidente de la republique", "Responsables politiques", "Gouvernement & exécutif"),
    ("depute", "Responsables politiques", "Parlementaires & élus"),
    ("deputee", "Responsables politiques", "Parlementaires & élus"),
    ("senateur", "Responsables politiques", "Parlementaires & élus"),
    ("senatrice", "Responsables politiques", "Parlementaires & élus"),
    ("eurodepute", "Responsables politiques", "Parlementaires & élus"),
    ("eurodeputee", "Responsables politiques", "Parlementaires & élus"),
    ("maire", "Responsables politiques", "Parlementaires & élus"),
    ("candidat", "Responsables politiques", "Parlementaires & élus"),
    ("candidate", "Responsables politiques", "Parlementaires & élus"),
    ("porte-parole", "Responsables politiques", "Partis & dirigeants de parti"),
    ("porte parole", "Responsables politiques", "Partis & dirigeants de parti"),
    ("secretaire general", "Responsables politiques", "Partis & dirigeants de parti"),
    ("secretaire generale", "Responsables politiques", "Partis & dirigeants de parti"),
    ("president du", "Responsables politiques", "Partis & dirigeants de parti"),
    ("presidente du", "Responsables politiques", "Partis & dirigeants de parti"),
    ("president de", "Responsables politiques", "Partis & dirigeants de parti"),
    ("presidente de", "Responsables politiques", "Partis & dirigeants de parti"),
    ("journaliste", "Journalistes & éditorialistes", "Journalistes & chroniqueurs"),
    ("editorialiste", "Journalistes & éditorialistes", "Journalistes & chroniqueurs"),
    ("chroniqueur", "Journalistes & éditorialistes", "Journalistes & chroniqueurs"),
    ("chroniqueuse", "Journalistes & éditorialistes", "Journalistes & chroniqueurs"),
)

NAME_STOP = {"de", "du", "des", "le", "la", "les", "d", "et", "von", "van"}

BLOCKED_HOST_SUFFIXES = (
    "wikipedia.org",
    "wikimedia.org",
    "x.com",
    "twitter.com",
    "t.co",
    "facebook.com",
    "instagram.com",
    "tiktok.com",
    "news.google.com",
)


def norm_literal(value):
    """Espaces et apostrophes unifiés. La casse est gardée."""
    if value is None:
        return ""
    text = str(value)
    for src, dst in APOSTROPHES.items():
        text = text.replace(src, dst)
    for sp in SPACES:
        text = text.replace(sp, " ")
    text = text.replace("\u2011", "-").replace("\u2010", "-").replace("\u00ad", "")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) >= 2 and text[0] in WRAP_OPEN and text[-1] in WRAP_CLOSE:
        text = text[1:-1].strip()
    return text


def fold(value):
    text = norm_literal(value).lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def forbidden_hits(value):
    hits = []
    seen = set()
    for token in re.findall(r"[a-z]+", fold(value)):
        for stem in FORBIDDEN_STEMS:
            if token == stem or (token.startswith(stem) and token[len(stem):] in FORBIDDEN_SUFFIXES):
                if stem not in seen:
                    hits.append(stem)
                    seen.add(stem)
                break
    return hits


def has_phrase(text, phrase):
    folded = fold(text)
    needle = fold(phrase)
    if not needle:
        return False
    return re.search(r"(^|[^a-z0-9])" + re.escape(needle) + r"([^a-z0-9]|$)", folded) is not None


def has_topic(text):
    return any(has_phrase(text, phrase) for phrase in TOPIC_PHRASES)


def causal_missing(written, page):
    """Une causalité écrite par le site doit déjà être dans la page."""
    folded_page = fold(page)
    missing = []
    for phrase in CAUSAL:
        if phrase in fold(written) and phrase not in folded_page:
            missing.append(phrase)
    return missing


def name_tokens(name):
    return [t for t in re.findall(r"[a-z0-9]+", fold(name)) if t not in NAME_STOP and len(t) > 1]


def name_in_text(name, text):
    """Le nom est dans le texte : tous les mots significatifs, ou les deux derniers mots."""
    tokens = name_tokens(name)
    raw = re.findall(r"[a-z0-9]+", fold(name))
    if len(tokens) >= 2 and all(has_phrase(text, token) for token in tokens):
        return True
    if len(raw) >= 2 and has_phrase(text, " ".join(raw[-2:])):
        return True
    return False


def slugify(name):
    slug = re.sub(r"[^a-z0-9]+", "-", fold(name)).strip("-")
    return slug[:60]


def short_hash(*parts):
    raw = "\n".join(norm_literal(p).lower() for p in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def french_date(iso):
    year, month, day = iso.split("-")
    return "%d %s %s" % (int(day), MONTHS[int(month) - 1], year)


def parse_french_date(value):
    """Retourne AAAA-MM-JJ ou une chaîne vide."""
    text = norm_literal(value)
    iso = re.search(r"\b(20\d{2})-(\d{2})-(\d{2})\b", text)
    if iso:
        return "%s-%s-%s" % (iso.group(1), iso.group(2), iso.group(3))
    low = fold(text)
    for index, month in enumerate(MONTHS, start=1):
        m = re.search(r"\b(\d{1,2})\s+" + fold(month) + r"\s+(20\d{2})\b", low)
        if m:
            return "%s-%02d-%02d" % (m.group(2), index, int(m.group(1)))
    slash = re.search(r"\b(\d{1,2})/(\d{1,2})/(20\d{2})\b", text)
    if slash:
        return "%s-%02d-%02d" % (slash.group(3), int(slash.group(2)), int(slash.group(1)))
    return ""


def date_in_text(iso, text):
    if not iso or len(iso) != 10:
        return False
    if iso in (text or ""):
        return True
    year, month, day = iso.split("-")
    patterns = [
        french_date(iso),
        "%s/%s/%s" % (day, month, year),
        "%d/%d/%s" % (int(day), int(month), year),
        "%s.%s.%s" % (day, month, year),
    ]
    folded = fold(text)
    return any(fold(p) in folded for p in patterns)


def _office_hit(text, needle):
    folded = fold(text)
    token = fold(needle)
    if " " in token:
        return token in folded
    # « députés », « ministre » : le mot peut prendre un pluriel ou un féminin.
    return re.search(r"(^|[^a-z0-9])" + re.escape(token) + r"[a-z]*", folded) is not None


def classify_office(role):
    """(catégorie, sous-catégorie) si la fonction est un mandat public reconnaissable."""
    # L'ordre de PUBLIC_OFFICE compte : la fonction la plus précise d'abord.
    for needle, category, sub in PUBLIC_OFFICE:
        if _office_hit(role, needle):
            return category, sub
    return None


def private_cue(text):
    folded = fold(text)
    return any(has_phrase(folded, cue) or cue in folded for cue in PRIVATE_CUES)


def public_cue(text):
    return classify_office(text) is not None
