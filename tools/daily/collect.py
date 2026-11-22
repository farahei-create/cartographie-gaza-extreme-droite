# -*- coding: utf-8 -*-
"""Flux RSS, pages publiques, résolution des liens Google News.

Google News ne sert qu'à trouver l'article. La citation est relue sur la page
de l'éditeur. Un lien qui ne se résout pas n'est pas publié.
"""
import json
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser

from tools.daily.textutil import fold, has_topic, name_in_text, norm_literal, parse_french_date

UA = "Mozilla/5.0 (compatible; OnrecordDaily/1.0; +https://onrecord-fr.vercel.app/)"
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
MAX_BYTES = 1_500_000
TIMEOUT = 20

# Flux répondant le 18/11/2026. RTL, LCI, TF1 et l'Assemblée n'avaient pas de
# flux stable ce jour-là : Google News les retrouve quand la page éditeur se résout.
FEEDS = (
    ("franceinfo", "https://www.franceinfo.fr/titres.rss"),
    ("franceinfo", "https://www.franceinfo.fr/politique.rss"),
    ("franceinfo", "https://www.franceinfo.fr/monde.rss"),
    ("BFMTV", "https://www.bfmtv.com/rss/politique/"),
    ("BFMTV", "https://www.bfmtv.com/rss/international/"),
    ("BFMTV", "https://www.bfmtv.com/rss/news-24-7/"),
    ("CNews", "https://www.cnews.fr/rss.xml"),
    ("Europe 1", "https://www.europe1.fr/rss.xml"),
    ("France Inter", "https://www.radiofrance.fr/franceinter/rss"),
    ("Sud Radio", "https://www.sudradio.fr/feed/"),
    ("Le Monde", "https://www.lemonde.fr/rss/une.xml"),
    ("Le Monde", "https://www.lemonde.fr/politique/rss_full.xml"),
    ("Le Monde", "https://www.lemonde.fr/international/rss_full.xml"),
    ("Le Monde", "https://www.lemonde.fr/societe/rss_full.xml"),
    ("Le Figaro", "https://www.lefigaro.fr/rss/figaro_actualites.xml"),
    ("Le Figaro", "https://www.lefigaro.fr/rss/figaro_politique.xml"),
    ("Le Figaro", "https://www.lefigaro.fr/rss/figaro_international.xml"),
    ("Libération", "https://www.liberation.fr/arc/outboundfeeds/rss/?outputType=xml"),
    ("Libération", "https://www.liberation.fr/arc/outboundfeeds/rss/category/politique/?outputType=xml"),
    ("Le JDD", "https://www.lejdd.fr/rss.xml"),
    ("Le HuffPost", "https://www.huffingtonpost.fr/rss/all_headline.xml"),
    ("LCP", "https://lcp.fr/rss-actualites.xml"),
    ("Arcom", "https://www.arcom.fr/rss.xml"),
    ("Conseil d'État", "https://www.conseil-etat.fr/pages/rss"),
    ("Public Sénat", "https://www.publicsenat.fr/feed"),
)

GOOGLE_QUERIES = (
    'Gaza OR Cisjordanie OR "bande de Gaza" OR Israël OR Palestine',
    '"extrême droite" OR "Rassemblement national" OR "Marine Le Pen" OR Zemmour OR Bardella OR Reconquête',
    '(immigration OR remigration OR "identité nationale") (Le Pen OR Retailleau OR Zemmour OR Mélenchon OR Bardella OR Attal)',
    '(site:rtl.fr OR site:tf1info.fr OR site:lci.fr OR site:assemblee-nationale.fr OR site:cnews.fr) (Gaza OR immigration OR "Le Pen" OR "extrême droite")',
)

HOST_OUTLET = (
    ("franceinfo.fr", "franceinfo"),
    ("francetvinfo.fr", "franceinfo"),
    ("bfmtv.com", "BFMTV"),
    ("cnews.fr", "CNews"),
    ("tf1info.fr", "TF1 Info"),
    ("lci.fr", "LCI"),
    ("europe1.fr", "Europe 1"),
    ("rtl.fr", "RTL"),
    ("radiofrance.fr", "France Inter"),
    ("sudradio.fr", "Sud Radio"),
    ("lemonde.fr", "Le Monde"),
    ("lefigaro.fr", "Le Figaro"),
    ("liberation.fr", "Libération"),
    ("lejdd.fr", "Le JDD"),
    ("huffingtonpost.fr", "Le HuffPost"),
    ("lcp.fr", "LCP"),
    ("assemblee-nationale.fr", "Assemblée nationale"),
    ("arcom.fr", "Arcom"),
    ("conseil-etat.fr", "Conseil d'État"),
    ("publicsenat.fr", "Public Sénat"),
    ("20minutes.fr", "20 Minutes"),
    ("ouest-france.fr", "Ouest-France"),
    ("francetvinfo.fr", "franceinfo"),
)


def outlet_for(url, fallback=""):
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    for suffix, name in HOST_OUTLET:
        if host == suffix or host.endswith("." + suffix):
            return name
    return fallback or host or "Source"


def _get(url, timeout=TIMEOUT, ua=UA):
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "text/html,application/xml,application/rss+xml,*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        raw = res.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raw = raw[:MAX_BYTES]
        charset = res.headers.get_content_charset() or "utf-8"
        return res.geturl(), raw.decode(charset, "replace")


def _local(tag):
    return tag.rsplit("}", 1)[-1] if tag else ""


def _text(node):
    if node is None:
        return ""
    return "".join(node.itertext()).strip()


def parse_feed(xml_text):
    """RSS ou Atom. Les espaces de noms par défaut sont retirés."""
    cleaned = re.sub(r'\sxmlns="[^"]+"', "", xml_text, count=1)
    try:
        root = ET.fromstring(cleaned)
    except ET.ParseError:
        return []
    items = []
    for it in root.iter():
        if _local(it.tag) not in ("item", "entry"):
            continue
        title = link = desc = pub = source_url = source_name = ""
        for child in list(it):
            name = _local(child.tag)
            if name == "title" and not title:
                title = _text(child)
            elif name == "link" and not link:
                link = (child.get("href") or _text(child) or "").strip()
            elif name in ("description", "summary", "content") and not desc:
                desc = _text(child)
            elif name in ("pubDate", "published", "updated") and not pub:
                pub = _text(child)
            elif name == "source":
                source_url = child.get("url") or ""
                source_name = _text(child)
        if link:
            items.append({
                "title": title,
                "url": link.replace("&amp;", "&"),
                "summary": re.sub(r"<[^>]+>", " ", desc),
                "published": pub,
                "source_url": source_url,
                "source_name": source_name,
            })
    return items


def parse_feed_date(value):
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime_utc())
        return dt
    except (TypeError, ValueError, IndexError):
        iso = parse_french_date(value)
        if not iso:
            return None
        import datetime
        y, m, d = (int(x) for x in iso.split("-"))
        return datetime.datetime(y, m, d, tzinfo=datetime_utc())


def datetime_utc():
    import datetime
    return datetime.timezone.utc


def publisher_from_batch(body):
    found = re.findall(r"https?://(?!news\.google|www\.google)[^\s\"\\]+", body or "")
    for url in found:
        url = url.rstrip(".,);]")
        if url.startswith("https://"):
            return url
    return ""


def resolve_google_news(article_url, opener=_get):
    """Deux requêtes : la page Google, puis le décodage batchexecute. Retourne l'URL éditeur ou ''."""
    try:
        final, html = opener(article_url, ua=BROWSER_UA)
    except (urllib.error.URLError, socket.timeout, TimeoutError, ValueError):
        return ""
    sig = re.search(r'data-n-a-sg="([^"]+)"', html)
    ts = re.search(r'data-n-a-ts="([^"]+)"', html)
    art = re.search(r'data-n-a-id="([^"]+)"', html)
    if not (sig and ts and art):
        return ""
    inner = (
        '["garturlreq",[["X","X",["X","X"],null,null,1,1,"FR:fr",null,1,null,null,null,null,null,0,1],'
        '"X","X",1,[1,1,1],1,1,null,0,0,null,0],"%s",%s,"%s"]'
    ) % (art.group(1), ts.group(1), sig.group(1))
    freq = json.dumps([[["Fbv4je", inner, None, "generic"]]])
    data = urllib.parse.urlencode({"f.req": freq}).encode()
    req = urllib.request.Request(
        "https://news.google.com/_/DotsSplashUi/data/batchexecute?rpcids=Fbv4je",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "User-Agent": BROWSER_UA},
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as res:
            body = res.read(200_000).decode("utf-8", "replace")
    except (urllib.error.URLError, socket.timeout, TimeoutError):
        return ""
    return publisher_from_batch(body)


BLOCK_TAGS = (
    "p", "br", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "td", "th",
    "ul", "ol", "section", "article", "header", "footer", "nav", "aside", "blockquote",
    "figure", "figcaption", "main", "form", "button", "label", "option", "dt", "dd",
)
# Paragraphes de l'article : c'est là que sont les citations, pas dans les menus.
PARA_TAGS = ("p", "blockquote", "h1")
CHALLENGE_TITLES = ("client challenge", "acces restreint", "just a moment", "attention required", "access denied", "are you a robot")


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.dates = []
        self._skip = 0
        self.title = ""
        self._in_title = False
        self.paras = []
        self._para = None
        self._para_depth = 0

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        if tag in ("script", "style", "noscript", "svg"):
            self._skip += 1
        if tag == "title":
            self._in_title = True
        if tag in BLOCK_TAGS:
            self.parts.append("\n")
        if tag in PARA_TAGS:
            if self._para is None:
                self._para = []
                self._para_depth = 0
            self._para_depth += 1
        elif tag == "br" and self._para is not None:
            self._para.append(" ")
        if tag == "time" and ad.get("datetime"):
            self.dates.append(ad["datetime"][:10])
        if tag == "meta":
            key = (ad.get("property") or ad.get("name") or "").lower()
            content = ad.get("content") or ""
            if key in ("article:published_time", "pubdate", "date", "dc.date") and content:
                self.dates.append(content[:10])

    def _close_para(self):
        if self._para is not None:
            text = norm_literal("".join(self._para))
            if text:
                self.paras.append(text)
        self._para = None
        self._para_depth = 0

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self._skip:
            self._skip -= 1
        if tag == "title":
            self._in_title = False
        if tag in PARA_TAGS and self._para is not None:
            self._para_depth -= 1
            if self._para_depth <= 0:
                self._close_para()
        if tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._skip:
            return
        if self._in_title:
            self.title += data
        self.parts.append(data)
        if self._para is not None:
            self._para.append(data)


def article_text(paras):
    """Paragraphes utiles : assez longs, ou porteurs de guillemets."""
    kept = []
    seen = set()
    for para in paras:
        if para in seen:
            continue
        if len(para) >= 60 or any(mark in para for mark in "«“\""):
            kept.append(para)
            seen.add(para)
    return "\n".join(kept)


def is_challenge(title, text):
    """Page anti-robot ou mur d'accès : ce n'est pas l'article."""
    folded = fold(title or "")
    if any(mark in folded for mark in CHALLENGE_TITLES):
        return True
    return len(norm_literal(text or "")) < 400


def extract_html(html):
    parser = _Text()
    try:
        parser.feed(html)
        parser.close()
        parser._close_para()
    except Exception:
        return {"title": "", "text": norm_literal(re.sub(r"<[^>]+>", " ", html))[:20000], "dates": [], "article": ""}
    # Les morceaux sont collés tels que le navigateur les affiche : un lien au
    # milieu d'une phrase n'ajoute pas d'espace avant une virgule.
    text = norm_literal("".join(parser.parts))
    dates = []
    for raw in parser.dates:
        iso = parse_french_date(raw) or (raw[:10] if re.match(r"20\d{2}-\d{2}-\d{2}", raw or "") else "")
        if iso and iso not in dates:
            dates.append(iso)
    # Une date écrite dans le corps compte aussi.
    body_date = parse_french_date(text[:4000])
    if body_date and body_date not in dates:
        dates.append(body_date)
    article = article_text(parser.paras)
    return {"title": norm_literal(parser.title)[:180], "text": text[:80000], "dates": dates, "article": article[:60000]}


def _on_space(text, start, end):
    """Évite de couper un mot quand on découpe un extrait pour le modèle."""
    start = max(0, start)
    end = min(len(text), end)
    if start > 0:
        space = text.rfind(" ", 0, start + 1)
        if space != -1 and start - space < 40:
            start = space + 1
    if end < len(text):
        space = text.find(" ", end)
        if space != -1 and space - end < 40:
            end = space
    return text[start:end].strip()


def excerpt(page, limit=11000):
    """Morceaux envoyés au modèle.

    D'abord les paragraphes de l'article (sans menus), en commençant par ceux
    qui portent des guillemets. Sinon, l'ancien découpage sur le texte entier.
    Le séparateur n'est pas une ellipse : le modèle ne doit pas la recopier.
    """
    article = page.get("article") or ""
    if len(article) >= 400:
        paras = [p for p in article.split("\n") if p.strip()]
        head = []
        size = 0
        for para in paras[:4]:
            head.append(para)
            size += len(para)
        quoted = [p for p in paras[4:] if any(mark in p for mark in "«“\"")]
        rest = [p for p in paras[4:] if p not in quoted]
        out = list(head)
        for para in quoted + rest:
            if size + len(para) > limit:
                continue
            out.append(para)
            size += len(para)
        # Ordre de la page, pour garder le fil (qui parle, quand).
        order = {p: i for i, p in enumerate(paras)}
        out.sort(key=lambda p: order.get(p, 0))
        return "\n\n".join(out)
    text = page.get("text") or ""
    chunks = [_on_space(text, 0, 3500)]
    folded = fold(text)
    for needle in ("gaza", "le pen", "extreme droite", "immigration", "rassemblement national", "israel", "zemmour", "bardella"):
        n = fold(needle)
        at = folded.find(n)
        if at < 0 or len(chunks) >= 5:
            continue
        chunks.append(_on_space(text, at - 600, at + 1800))
    out = []
    seen = set()
    for chunk in chunks:
        if not chunk or chunk[:80] in seen:
            continue
        seen.add(chunk[:80])
        out.append(chunk)
    body = "\n\n---\n\n".join(out)
    if len(body) <= limit:
        return body
    return _on_space(body, 0, limit)


# Pages index (fiche personnalité, émission, tag) : pas un article daté.
HUB_PATTERNS = (
    r"_DN-\d+\.html$", r"/emission/", r"/tag/", r"/tags/", r"/personnalites?/", r"/sujet/", r"/theme/",
    r"/replay-radio/?$", r"/videos?/?$",
)
# Éditeurs qui renvoient un mur anti-robot aux requêtes automatiques : lus en dernier.
LOW_PRIORITY_HOSTS = ("lemonde.fr", "liberation.fr", "mediapart.fr", "lexpress.fr", "lepoint.fr")


def is_hub(url):
    path = urllib.parse.urlparse(url or "").path
    return any(re.search(pattern, path) for pattern in HUB_PATTERNS)


def low_priority(url):
    host = (urllib.parse.urlparse(url or "").hostname or "").lower()
    return any(host == h or host.endswith("." + h) for h in LOW_PRIORITY_HOSTS)


def relevant(item, names):
    blob = "%s %s" % (item.get("title") or "", item.get("summary") or "")
    if has_topic(blob):
        return True
    for name in names:
        if name_in_text(name, blob):
            return True
    return False


def score_item(item, names, known_urls):
    title = item.get("title") or ""
    summary = item.get("summary") or ""
    score = 0
    if has_topic(title):
        score += 3
    if any(name_in_text(name, title) for name in names):
        score += 5
    if has_topic(summary):
        score += 1
    if any(name_in_text(name, summary) for name in names):
        score += 2
    if item.get("url") in known_urls:
        score -= 2
    return score


def primary_person(item, names):
    title = "%s %s" % (item.get("title") or "", item.get("summary") or "")
    hits = [name for name in names if name_in_text(name, title)]
    if not hits:
        return ""
    hits.sort(key=len, reverse=True)
    return hits[0]


def select_diverse(found, names, limit=16, per_person=2, per_outlet=3):
    """Choisit les pages à lire : d'abord une personne ou un média encore absent."""
    pool = [dict(item) for item in found]
    for item in pool:
        item["_person"] = primary_person(item, names)
    chosen = []
    while pool and len(chosen) < limit:
        people = {}
        outlets = {}
        for item in chosen:
            people[item.get("_person") or ""] = people.get(item.get("_person") or "", 0) + 1
            outlets[item.get("outlet") or ""] = outlets.get(item.get("outlet") or "", 0) + 1

        def rank(item):
            person = item.get("_person") or ""
            outlet = item.get("outlet") or ""
            return (
                0 if person and people.get(person, 0) == 0 else 1,
                0 if outlets.get(outlet, 0) == 0 else 1,
                people.get(person, 0),
                outlets.get(outlet, 0),
                -(item.get("score") or 0),
            )

        pool.sort(key=rank)
        pick = None
        for item in pool:
            person = item.get("_person") or ""
            outlet = item.get("outlet") or ""
            if person and people.get(person, 0) >= per_person:
                continue
            if outlets.get(outlet, 0) >= per_outlet:
                continue
            pick = item
            break
        if pick is None:
            break
        pool.remove(pick)
        chosen.append(pick)
    for item in chosen:
        item.pop("_person", None)
    return chosen


def google_feed_url(query):
    q = urllib.parse.quote(query + " when:2d")
    return "https://news.google.com/rss/search?q=%s&hl=fr&gl=FR&ceid=FR:fr" % q


MIN_SCORE = 3


def collect(index, now, sleep=0.3, max_pages=24, max_google=12):
    """Retourne (pages, stats). N'écrit rien."""
    stats = {
        "feeds_ok": 0, "feeds_fail": 0, "feed_errors": [],
        "items": 0, "google_unresolved": 0, "fetched": 0, "fetch_fail": 0,
    }

    def note_feed(outlet, url, error):
        stats["feeds_fail"] += 1
        stats["feed_errors"].append({"outlet": outlet, "url": url, "error": (error or "échec")[:180]})
    names = [n.get("name") or "" for n in index["nodes"] if n.get("name")]
    found = []
    seen_urls = set()

    def add(item, outlet):
        url = item.get("url") or ""
        if not url.startswith("https://") or url in seen_urls:
            return
        if not relevant(item, names):
            return
        published = parse_feed_date(item.get("published") or "")
        if published is not None:
            age = now - published.astimezone(now.tzinfo)
            if age.total_seconds() > 54 * 3600 or age.total_seconds() < -3600:
                return
            item = dict(item)
            item["feed_date"] = published.astimezone(now.tzinfo).date().isoformat()
        item = dict(item)
        item["outlet"] = outlet
        item["score"] = score_item(item, names, index["urls"])
        seen_urls.add(url)
        found.append(item)

    for outlet, url in FEEDS:
        try:
            _, body = _get(url)
            items = parse_feed(body)
            if not items:
                note_feed(outlet, url, "flux vide ou illisible")
                continue
            stats["feeds_ok"] += 1
            for item in items:
                add(item, outlet)
            time.sleep(sleep)
        except (urllib.error.URLError, socket.timeout, TimeoutError, ET.ParseError, ValueError) as exc:
            note_feed(outlet, url, str(exc))
    google_used = 0
    for query in GOOGLE_QUERIES:
        if google_used >= max_google:
            break
        try:
            _, body = _get(google_feed_url(query))
            items = parse_feed(body)
            stats["feeds_ok"] += 1
            for item in items:
                if google_used >= max_google:
                    break
                if "news.google.com" not in (item.get("url") or ""):
                    add(item, item.get("source_name") or "Presse")
                    continue
                if not relevant(item, names):
                    continue
                published = parse_feed_date(item.get("published") or "")
                if published is not None:
                    age = now - published.astimezone(now.tzinfo)
                    if age.total_seconds() > 54 * 3600 or age.total_seconds() < -3600:
                        continue
                publisher = resolve_google_news(item["url"])
                google_used += 1
                time.sleep(sleep)
                if not publisher:
                    stats["google_unresolved"] += 1
                    continue
                copied = dict(item)
                copied["url"] = publisher
                add(copied, item.get("source_name") or outlet_for(publisher))
            time.sleep(sleep)
        except (urllib.error.URLError, socket.timeout, TimeoutError, ET.ParseError, ValueError) as exc:
            note_feed("Google News", query[:80], str(exc))

    stats["items"] = len(found)
    pages = []
    # Pages index écartées ; titres sans sujet ni nom connu écartés ;
    # éditeurs à mur anti-robot gardés pour la fin.
    pool = [item for item in found if not is_hub(item["url"]) and (item.get("score") or 0) >= MIN_SCORE]
    first = [item for item in pool if not low_priority(item["url"])]
    last = [item for item in pool if low_priority(item["url"])]
    ordered = select_diverse(first, names, limit=max_pages * 3) + select_diverse(last, names, limit=max_pages)
    tried = 0
    for item in ordered:
        if len(pages) >= max_pages or tried >= max_pages * 3:
            break
        tried += 1
        try:
            final, html = _get(item["url"], ua=BROWSER_UA)
        except (urllib.error.URLError, socket.timeout, TimeoutError, ValueError, ConnectionError):
            # Page bloquée (403, 402, délai) : on passe à la suivante, sans perdre une place.
            stats["fetch_fail"] += 1
            continue
        if "news.google.com" in final or any(final.find(b) >= 0 for b in ("wikipedia.org", "x.com/", "twitter.com/")):
            stats["fetch_fail"] += 1
            continue
        if is_hub(final):
            continue
        extracted = extract_html(html)
        if is_challenge(extracted["title"], extracted["text"]):
            stats["fetch_fail"] += 1
            continue
        pages.append({
            "url": final,
            "outlet": outlet_for(final, item.get("outlet") or ""),
            "title": extracted["title"] or item.get("title") or "",
            "text": extracted["text"],
            "article": extracted.get("article") or "",
            "html": html,
            "dates": extracted["dates"],
            "feed_date": item.get("feed_date") or "",
        })
        stats["fetched"] += 1
        time.sleep(sleep)
    return pages, stats
