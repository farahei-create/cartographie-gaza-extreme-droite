# -*- coding: utf-8 -*-
"""Relecture avec bascule automatique entre deux IA.

Ordre : IA principale (GEMINI_API_KEY), puis IA de secours (XAI_API_KEY).
Si une seule clé est posée, elle sert seule. Quota, clé refusée ou panne d'une IA :
la page passe à l'autre, et un incident est noté pour la page admin « Problèmes ».
"""
from tools.daily import gemini, grok, incidents
from tools.daily.gemini import KeyErrorRejected, QuotaError

LABELS = {"gemini": "IA principale", "grok": "IA de secours"}


def available():
    names = []
    if gemini.key_from_env():
        names.append("gemini")
    if grok.key_from_env():
        names.append("grok")
    return names


class Relecture:
    def __init__(self, providers=None, log=incidents.add):
        if providers is None:
            providers = []
            if gemini.key_from_env():
                providers.append(("gemini", gemini.Gemini(gemini.key_from_env())))
            if grok.key_from_env():
                providers.append(("grok", grok.Grok(grok.key_from_env())))
        self.providers = providers
        self.dead = {}
        self.used = set()
        self.log = log
        self.fallbacks = 0

    @property
    def requests(self):
        return sum(getattr(p, "requests", 0) for _, p in self.providers)

    @property
    def model(self):
        parts = ["%s (%s)" % (getattr(p, "model", "?"), LABELS.get(n, n)) for n, p in self.providers if n in self.used]
        return ", ".join(parts) or "—"

    def _kill(self, name, why, rejected):
        self.dead[name] = "rejected" if rejected else "quota"
        others = [n for n, _ in self.providers if n not in self.dead]
        title = "%s : %s" % (LABELS.get(name, name), "clé refusée" if rejected else "quota atteint ou indisponible")
        detail = why + (" Bascule sur l'%s." % LABELS.get(others[0], others[0]).lower() if others else " Aucune autre IA disponible : relecture arrêtée pour ce passage.")
        self.log("ia_" + ("cle" if rejected else "quota"), title, detail, key=title)

    def extract(self, page, names):
        errors = []
        for index, (name, provider) in enumerate(self.providers):
            if name in self.dead:
                continue
            try:
                items = provider.extract(page, names)
                self.used.add(name)
                if index > 0 and errors:
                    self.fallbacks += 1
                return items
            except KeyErrorRejected as exc:
                self._kill(name, str(exc), True)
                errors.append(str(exc))
            except QuotaError as exc:
                self._kill(name, str(exc), False)
                errors.append(str(exc))
            except (ValueError, OSError) as exc:
                errors.append(str(exc))
                continue
        if self.providers and all(n in self.dead for n, _ in self.providers):
            if all(v == "rejected" for v in self.dead.values()):
                raise KeyErrorRejected("toutes les clés d'IA sont refusées")
            raise QuotaError("toutes les IA sont au quota")
        raise ValueError("; ".join(errors) or "relecture impossible")
