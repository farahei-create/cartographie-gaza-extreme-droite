# -*- coding: utf-8 -*-
"""v27 : mise à jour du 10 novembre 2026.
Chaque phrase a été lue dans la page indiquée (HTTP 200) le 10 novembre 2026.
Le contexte et les nuances lus dans la même page sont dans le champ « medium »."""

F = "France – normalisation de l'extrême droite"
MS = "Médias – structure"

U_CNEWS_FI = "https://www.franceinfo.fr/politique/la-petition-appelant-a-supprimer-cnews-de-l-audiovisuel-francais-classee-par-la-commission-de-l-assemblee-nationale_8276303.html"
U_CNEWS_LP = "https://www.leparisien.fr/culture-loisirs/tv/cnews-les-deputes-decident-de-ne-pas-donner-suite-a-la-petition-pour-supprimer-la-chaine-10-11-2026-2QKCXKX3E5DPBJEH5QBO7F4IOY.php"
U_CNEWS_AN = "https://www.assemblee-nationale.fr/dyn/17/organes/commissions-permanentes/affaires-culturelles/actualites/decision-de-classement-de-la-petition-supprimer-cnews-de-l-audiovisuel-francais"
U_KNAFO_BFM = "https://www.bfmtv.com/politique/reconquete/vrai-faux-gerald-darmanin-a-t-il-dit-la-meme-chose-qu-eric-zemmour-sur-l-immigration-et-la-delinquance-comme-l-affirme-sarah-knafo_AV-202611090761.html"
U_GRASSET = "https://www.franceinfo.fr/culture/livres/lise-boell-ancienne-editrice-d-eric-zemmour-nommee-directrice-generale-deleguee-des-editions-grasset_8275976.html"

NEW_URLS = [U_CNEWS_FI, U_CNEWS_LP, U_CNEWS_AN, U_KNAFO_BFM, U_GRASSET]


def apply(N, E, by, step, link):
    def add(pid, rows):
        n = by[pid]
        seen = {s.get("quote") for s in n.get("statements") or []}
        for quote, date, medium, url, theme, section in rows:
            if quote in seen:
                continue
            n.setdefault("statements", []).append({
                "quote": quote, "date": date, "medium": medium, "url": url,
                "theme": theme, "section": section,
            })
            seen.add(quote)

    def add_steps(pid, steps):
        n = by[pid]
        cur = list(n.get("parcours") or [])
        seen = {(s["date"], s["title"]) for s in cur}
        for s in steps:
            if (s["date"], s["title"]) not in seen:
                cur.append(s)
                seen.add((s["date"], s["title"]))
        cur.sort(key=lambda s: s["date"])
        n["parcours"] = cur

    # Pétition « Supprimer CNews de l'audiovisuel français » classée en commission
    add("cnews", [
        ("Chacun est libre de critiquer CNews et de contester ses choix éditoriaux. Mais réclamer la disparition d'une chaîne pose une question essentielle pour le pluralisme et la liberté d'informer",
         "2026-11-10",
         "Communiqué de CNews, cité par Le Parisien avec AFP, après le vote de la commission des affaires culturelles de l'Assemblée nationale qui a classé, le 10 novembre 2026, la pétition « Supprimer CNews de l'audiovisuel français » (plus d'un million de signatures) par 28 voix contre 25 (site de l'Assemblée nationale). Le président et rapporteur Alexandre Portier (LR) : « Nous ne sommes pas l'Arcom » ; il propose un débat plus large sur la liberté de la presse et la régulation des médias. Selon franceinfo, le RN, l'UDR, LR et Horizons ont voté pour le classement ; la gauche et le MoDem contre ; le groupe EPR s'est divisé. Le PS et LFI demandent un débat dans l'hémicycle.",
         U_CNEWS_LP, F, "france"),
    ])
    add("rn", [
        ("cette obsession de la censure portée par la gauche et l'extrême gauche",
         "2026-11-10",
         "Caroline Parmentier, députée RN, en commission des affaires culturelles de l'Assemblée nationale lors de l'examen de la pétition visant CNews, citée par franceinfo. Dans le même débat, le député LFI Aymeric Caron parle d'un « outil promotionnel de l'extrême droite » et ajoute : « C'est un problème de droit, pas un problème de liberté d'expression ». La pétition a été classée par 28 voix contre 25.",
         U_CNEWS_FI, F, "france"),
    ])

    # Sarah Knafo, BFMTV-RMC, 9 novembre 2026
    add("sarah-knafo", [
        ("depuis, Gérald Darmanin a dit la même chose comme garde des Sceaux, comme ministre. Il n’a pas été condamné par la justice pour l’avoir dit.",
         "2026-11-09",
         "BFMTV-RMC, 9 novembre 2026, cité par BFMTV. Elle évoque la condamnation d'Éric Zemmour en 2011 pour provocation à la haine raciale, en défendant sa candidature à la présidentielle. La rubrique VRAI/FAUX de BFMTV conclut que l'affirmation est fausse : Gérald Darmanin n'a jamais justifié des contrôles au faciès ; BFMTV rappelle qu'il a toutefois lié à plusieurs reprises immigration et délinquance (Le Figaro, août 2022).",
         U_KNAFO_BFM, F, "france"),
    ])

    # Lise Boëll à Grasset (communiqué Hachette Livre du 9 novembre 2026)
    by["lise-boell"]["role"] = "Présidente-directrice générale des éditions Fayard (nommée le 5 juin 2024) ; directrice générale déléguée des éditions Grasset (9 novembre 2026)"
    add_steps("lise-boell", [
        step("2026-11-09", "Direction générale déléguée de Grasset",
             "Hachette Livre, dont Vincent Bolloré est l'actionnaire de référence selon franceinfo, annonce sa nomination comme directrice générale déléguée des éditions Grasset, aux côtés du PDG Jean-Christophe Thiery. Elle reste PDG de Fayard. La nomination intervient sept mois après le départ d'Olivier Nora, qui a dirigé Grasset pendant vingt-six ans.",
             U_GRASSET, "franceinfo"),
    ])
    add_steps("arnaud-lagardere", [
        step("2026-11-09", "Grasset",
             "PDG de Hachette Livre selon franceinfo, il est cité dans le communiqué annonçant la nomination de Lise Boëll comme directrice générale déléguée des éditions Grasset.",
             U_GRASSET, "franceinfo"),
    ])
    add("arnaud-lagardere", [
        ("Son exigence éditoriale, sa proximité avec les auteurs et sa vision seront des atouts précieux pour accompagner le développement des Editions Grasset, tout en restant fidèle à l'ADN qui a fait le succès de cette marque emblématique",
         "2026-11-09",
         "Communiqué de Hachette Livre, cité par franceinfo avec AFP (10 novembre 2026), sur la nomination de Lise Boëll comme directrice générale déléguée des éditions Grasset. franceinfo rappelle que Fayard, qu'elle dirige toujours, publie notamment Sarah Knafo, Charles Alloncle, Jordan Bardella et Philippe de Villiers.",
         U_GRASSET, MS, "france"),
    ])
    link("arnaud-lagardere", "lise-boell",
         "PDG de Hachette Livre selon franceinfo ; cité dans le communiqué annonçant sa nomination comme directrice générale déléguée des éditions Grasset",
         U_GRASSET, "2026-11-09")
    E[-1]["nature"] = "coulisses"
    E[-1]["section"] = "france"
    E[-1]["stories"] = ["nominations"]
