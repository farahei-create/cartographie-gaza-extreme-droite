# -*- coding: utf-8 -*-
"""IA de secours : API xAI (compatible OpenAI), clé XAI_API_KEY.

Même consigne et même format de réponse que l'IA principale (tools/daily/gemini.py).
Absente si la clé n'est pas posée : le relevé continue sans elle.
"""
import json
import os
import time
import urllib.error
import urllib.request

from tools.daily.gemini import KeyErrorRejected, QuotaError, _prompt

ENDPOINT = "https://api.x.ai/v1/chat/completions"
MODELS = tuple(m for m in (os.environ.get("XAI_MODEL") or "", "grok-4.3", "grok-4.20-non-reasoning") if m)
MAX_REQUESTS = 60
RETRIES = 3
PAUSE_SECONDS = 3


def key_from_env():
    return (os.environ.get("XAI_API_KEY") or "").strip()


def _parse(body):
    data = json.loads(body)
    choices = data.get("choices") or []
    if not choices:
        raise ValueError("réponse vide")
    raw = ((choices[0].get("message") or {}).get("content") or "").strip()
    if raw.startswith("```"):
        raw = raw.strip("`").split("\n", 1)[-1]
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end < start:
        raise ValueError("réponse illisible")
    parsed = json.loads(raw[start:end + 1])
    items = parsed.get("items") if isinstance(parsed, dict) else None
    if not isinstance(items, list):
        raise ValueError("réponse illisible")
    return items


class Grok:
    label = "IA de secours"

    def __init__(self, key, sleep=time.sleep, max_requests=MAX_REQUESTS):
        self.key = key
        self.sleep = sleep
        self.max_requests = max_requests
        self.requests = 0
        self.model = MODELS[0]
        self.dead = set()
        self.no_effort = False

    def _post(self, model, prompt):
        self.requests += 1
        if self.requests > self.max_requests:
            raise QuotaError("plafond de requêtes du relevé")
        payload = {
            "model": model,
            "temperature": 0.1,
            "max_tokens": 4096,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": "Réponds uniquement par un objet JSON {\"items\": [...]} ; chaque item a les champs person_name, quote, date, section, theme, context, denial, video_url, doubt, public_role."},
                {"role": "user", "content": prompt},
            ],
        }
        if not self.no_effort:
            payload["reasoning_effort"] = "none"
        req = urllib.request.Request(
            ENDPOINT, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": "Bearer " + self.key},
            method="POST")
        try:
            with urllib.request.urlopen(req, timeout=90) as res:
                return res.status, res.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read().decode("utf-8", "replace")[:500]
        except (OSError, ValueError) as exc:
            return 0, str(exc)

    def extract(self, page, names):
        prompt = _prompt(page, names)
        last = ""
        for model in [self.model] + [m for m in MODELS if m != self.model]:
            if model in self.dead:
                continue
            delay = PAUSE_SECONDS
            for attempt in range(RETRIES):
                status, body = self._post(model, prompt)
                if status == 400 and "reasoning" in body.lower() and not self.no_effort:
                    self.no_effort = True
                    status, body = self._post(model, prompt)
                if status not in (0, 500, 502, 503, 504):
                    break
                if attempt + 1 < RETRIES:
                    self.sleep(delay)
                    delay *= 2
            if status == 200:
                self.model = model
                return _parse(body)
            if status in (401, 403):
                raise KeyErrorRejected("clé de l'IA de secours refusée (%s)" % status)
            if status == 429:
                raise QuotaError("quota de l'IA de secours atteint (429)")
            if status in (400, 404):
                self.dead.add(model)
                last = "modèle %s refusé (%s)" % (model, status)
                continue
            last = "HTTP %s" % status
        raise ValueError(last or "relecture impossible")
