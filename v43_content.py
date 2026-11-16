# -*- coding: utf-8 -*-
"""v43 : complément du 16 novembre 2026 (période du 13 au 16 novembre).
Phrases lues le 16 novembre 2026 dans les pages indiquées.
Le message X de Jordan Bardella a été lu sur la copie Nitter du post
(nitter.cf), x.com ne répondant pas ; l'URL citée est celle du post original.
Les crochets [ ] sont une coupure. Le contexte lu dans la même page est dans « medium »."""

F = "France – normalisation de l'extrême droite"

U_FI_RET = "https://www.franceinfo.fr/politique/vous-avez-en-france-des-minorites-bruyantes-agissantes-violentes-qu-on-laisse-agir-affirme-bruno-retailleau-a-propos-du-mouvement-social_8280638.html"
U_FI_MIF = "https://www.franceinfo.fr/economie/industrie/made-in-france-quand-la-presidentielle-s-invite-au-salon_8282180.html"
U_X_BARD = "https://x.com/J_Bardella/status/2121353541805592926"
U_NITTER = "https://nitter.cf/J_Bardella/status/2121353541805592926"
U_BFM_SARK = "https://www.bfmtv.com/politique/cet-exercice-n-a-d-interet-que-s-il-rassemble-nicolas-sarkozy-plaide-pour-l-organisation-d-une-large-primaire-de-la-droite-et-du-centre_AN-202611130733.html"

VID_RET = {"url": U_FI_RET, "platform": "franceinfo.fr",
           "title": "Bruno Retailleau, invité des 4V sur France 2",
           "source": "franceinfo (site officiel)"}
VID_MIF = {"url": U_FI_MIF, "platform": "franceinfo.fr",
           "title": "Le 23h info du 13 novembre 2026, salon du Made in France",
           "source": "franceinfo (site officiel)"}


def apply(N, E, by, step, node, link, st):
    def add_node(*a, **k):
        node(*a, **k)
        by[a[0]] = N[-1]
        return N[-1]

    def add(pid, rows):
        n = by[pid]
        seen = {s.get("quote") for s in n.get("statements") or []}
        for row in rows:
            quote, date, medium, url, theme, section = row[:6]
            if quote in seen:
                continue
            s = {"quote": quote, "date": date, "medium": medium, "url": url,
                 "theme": theme, "section": section}
            if len(row) > 6 and row[6]:
                s["video"] = row[6]
            n.setdefault("statements", []).append(s)
            seen.add(quote)
            if section not in n.setdefault("sections", []):
                n["sections"].append(section)

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

    def add_link(src, tgt, rel, url, date, section, nature):
        for e in E:
            if e["source"] == src and e["target"] == tgt and e.get("url") == url:
                return
        link(src, tgt, rel, url, date)
        E[-1]["section"] = section
        E[-1]["nature"] = nature

    ctx_ret = ("Les 4V, France 2, 13 novembre 2026, retranscription publiée par franceinfo. "
               "Le journaliste dit qu'il détaille ce jour-là ses propositions sur l'immigration. "
               "Sur l'asile, il dit qu'il ne renverra pas des Afghanes tant que la situation ne s'améliore pas, "
               "puis : « ce ne sont pas des Afghanes qui viennent ici, ce sont des Afghans qui, parfois d'ailleurs, n'ont rien contre le régime des talibans ». "
               "Il veut un asile « temporaire et révocable », les demandes étant « examinées dans des pays tiers sûrs ». "
               "À la question « le Maroc, l'Algérie, la Tunisie, ce sont des pays sûrs pour vous ? », il répond : « Ce sont des pays sûrs. »")

    add("bruno-retailleau", [
        ("Avec moi, ce sont les Français qui choisiront. Ils nous disent à une écrasante majorité, il y a trop d'immigration en France, trop d'immigration illégale avec des clandestins qu'on ne parvient pas à expulser, à éloigner, trop d'immigration légale avec des immigrés qui malheureusement désormais ne veulent plus s'intégrer ou s'assimiler. Concrètement, j'assume une position très ferme pour qu'on puisse accueillir beaucoup moins et qu'on expulse beaucoup plus. Comment fait-on ? On change la Constitution. Aujourd'hui, avec le droit tel qu'il est, vous savez qu'il n'y a pas de politique d'immigration en France.",
         "2026-11-13",
         ctx_ret,
         U_FI_RET, F, "france", VID_RET),
        ("Elle ne le fera pas parce qu'elle ne respecte pas la Constitution et que les maires n'organiseront pas son référendum. Moi, je respecte la Constitution et je donnerai la possibilité aux Français, par le référendum, de choisir justement la politique migratoire, sinon on sera censuré. Il faut bien sûr changer la Constitution par un référendum.",
         "2026-11-13",
         "Les 4V, France 2, 13 novembre 2026, retranscription franceinfo. Francis Letellier venait de dire : « Ce que veut faire Marine Le Pen, elle veut aussi changer la Constitution pour un référendum sur l'immigration. »",
         U_FI_RET, F, "france"),
        ("Mais la France n'est pas raciste. La France n'a jamais été raciste, mais il y a des discriminations. […] Le mal est partout, il y a des individus. Regardez Trappes, c'est le racisme. Voilà, un racisme anti-maghrébin, anti-africain, anti-musulman. Vous avez Trappes et vous avez Crépol. Crépol, c'est un racisme anti-blanc. Vous voyez bien que le mal est dans des êtres humains, mais pas dans le peuple français.",
         "2026-11-13",
         "Les 4V, France 2, 13 novembre 2026, retranscription franceinfo. Question : « Pour Marine Le Pen, la France est le pays le moins raciste. Est-ce que vous êtes d'accord avec ça ? » Les crochets signalent la coupure entre deux phrases de la même réponse. Il cite aussi Joséphine Baker. L'attentat de Trappes du 23 octobre 2026 est rappelé ici comme il le nomme ; le suspect n'est pas nommé et reste présumé innocent.",
         U_FI_RET, F, "france"),
        ("Non, je ne dis jamais islamophobe parce que c'est un terme qui a été forgé par les Frères musulmans, je dis anti-musulman. D'ailleurs, au ministère de l'Intérieur, lorsqu'on comptabilise des actes antireligieux, nous avons écarté ce concept.",
         "2026-11-13",
         "Les 4V, France 2, 13 novembre 2026, retranscription franceinfo. Question : « Sur Trappes, certains disent que c'est même un acte islamophobe. Est-ce que vous reprenez cette définition ? »",
         U_FI_RET, F, "france"),
    ])
    add_steps("bruno-retailleau", [
        step("2026-11-13", "Propositions sur l'immigration",
             "Invité des 4V sur France 2, il détaille des propositions : moins d'entrées, plus d'expulsions, révision de la Constitution pour un référendum sur l'immigration, asile temporaire examiné dans des pays tiers.",
             U_FI_RET, "franceinfo"),
    ])
    add_link("bruno-retailleau", "marine-le-pen",
             "dit que Marine Le Pen ne fera pas son référendum sur l'immigration parce qu'elle ne respecte pas la Constitution (13/11/2026, France 2)",
             U_FI_RET, "2026-11-13", "france", "opposition")

    add("marine-le-pen", [
        ("La baisse des impôts de production, le développement de la commande publique avec une priorité nationale dans la commande publique. La commande publique, c'est 200 milliards d'euros par an. C'est absolument considérable. Or, cette commande publique, elle n'est pas fléchée sur les entreprises françaises, ce qui pose un problème",
         "2026-11-13",
         "Salon du Made in France (Paris), 13 novembre 2026, reportage du 23h info de franceinfo publié le 14 novembre. franceinfo écrit qu'elle a été « accueillie sous les huées par des militants insoumis selon la candidate ».",
         U_FI_MIF, F, "france", VID_MIF),
    ])

    add("jordan-bardella", [
        ("Au bout de 6 mois, un étranger sans contrat de travail devra partir. La France n'est ni un hôtel, ni un guichet social !",
         "2026-11-13",
         "Message sur X (@J_Bardella), 13 novembre 2026, 21:24 UTC. Le texte a été lu le 16 novembre 2026 sur la copie Nitter du post (" + U_NITTER + ") : x.com ne répond pas depuis la machine. Le message est accompagné d'un extrait intitulé « Jordan Bardella sur LCI ».",
         U_X_BARD, F, "france"),
    ])

    add_node(
        "nicolas-sarkozy", "Nicolas Sarkozy", "person",
        "Ancien président de la République (Le Figaro, cité par BFMTV, 13 novembre 2026)",
        "Ancien président de la République. Le 13 novembre 2026, dans un entretien au Figaro cité par BFMTV, il parle d'une primaire « large » de la droite et du centre. Il ne nomme pas Éric Zemmour dans les phrases citées.",
        [st("entrer dans le sujet par la question des noms, c'est déjà créer les conditions de l'impasse. […] si primaire il y a, elle doit être large. […] tous ceux qui s'engageront à en respecter les règles devront pouvoir y concourir",
            "2026-11-13",
            "Entretien au Figaro publié le 13 novembre 2026, cité par BFMTV. Les crochets séparent trois phrases de la même page. BFMTV écrit que la primaire est agitée par des sondages donnant un second tour entre Marine Le Pen et Jean-Luc Mélenchon, et demande si elle doit inclure Éric Zemmour, qui l'a réclamé le même jour. Sarkozy ne le nomme pas. Il dit aussi : « La primaire est le pire des systèmes, à l'exception de tous les autres ! », « Cet exercice n'a d'intérêt que s'il rassemble ! Autrement, mieux vaut s'abstenir », et qu'il soutiendra « celui qui, au sein de la droite et du centre, aura réussi à rassembler le plus largement ».",
            U_BFM_SARK, F, "france")],
        "Responsables politiques", "Parlementaires & élus", ("france",))
    by["nicolas-sarkozy"]["parcours"] = [
        step("2026-11-13", "Entretien au Figaro sur la primaire",
             "BFMTV rend compte d'un entretien au Figaro où il plaide pour une primaire large de la droite et du centre, ouverte à ceux qui en respectent les règles.",
             U_BFM_SARK, "BFMTV"),
    ]
