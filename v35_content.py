# -*- coding: utf-8 -*-
"""v35 : mise à jour du 11 novembre 2026 (soir).
Chaque phrase a été lue dans la page indiquée (HTTP 200) le 11 novembre 2026.
Le message X de Jordan Bardella sur la pétition CNews a été lu en entier
(texte long) sur son compte vérifié ; France 24 / AFP en cite les mêmes mots.
Le contexte, les nuances et les réponses lus dans la même page sont dans « medium »."""

F = "France – normalisation de l'extrême droite"
MS = "Médias – structure"
NU = "Nuance / contexte"
ORG = "Organisations & institutions"

U_PFEFFER = "https://www.franceinfo.fr/politique/front-national/info-franceinfo-le-rn-a-un-obtenu-un-pre-accord-de-deux-banques-europeennes-pour-financer-sa-campagne-pour-la-presidentielle_8276195.html"
U_BARDELLA_BFM = "https://www.bfmtv.com/politique/front-national/etat-pro-police-racisme-reforme-des-retraites-ce-qu-il-faut-retenir-du-face-a-bfm-de-jordan-bardella_AN-202611100999.html"
U_BARDELLA_X_CNEWS = "https://x.com/J_Bardella/status/2120164408357740552"
U_F24_CNEWS = "https://www.france24.com/fr/france/20261110-p%C3%A9tition-pour-supprimer-cnews-audiovisuel-fran%C3%A7ais-d%C3%A9put%C3%A9s-donnent-pas-suite"
U_BARDELLA_X_ZEM = "https://x.com/J_Bardella/status/2120292537067847764"
U_ZEMMOUR_RTL = "https://www.rtl.fr/actu/politique/je-me-presente-pour-conserver-une-france-francaise-eric-zemmour-officialise-sa-candidature-a-la-presidentielle-2027-7900694983"
U_ZEMMOUR_TF1 = "https://www.tf1info.fr/politique/videos/video-presidentielle-2027-eric-zemmour-officialise-sa-candidature-au-20h-de-tf1-4341-2475122.html"
U_FTDA = "https://www.france-terre-asile.org/communiques-presse/communiques-de-presse/communique-france-terre-d-asile-et-desinfox-migrations-saisissent-l-arcom-et-publient-un-rapport-sur-la-desinformation-au-sujet-de-l-immigration"
U_FTDA_SO = "https://www.sudouest.fr/international/immigration-un-collectif-de-scientifiques-sort-un-rapport-pour-retablir-les-faits-face-a-la-desinformation-31468731.php"

NEW_URLS = [U_PFEFFER, U_BARDELLA_BFM, U_BARDELLA_X_CNEWS, U_F24_CNEWS, U_BARDELLA_X_ZEM,
            U_ZEMMOUR_RTL, U_ZEMMOUR_TF1, U_FTDA, U_FTDA_SO]


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

    # Kévin Pfeffer, trésorier du RN : prêt pour la campagne présidentielle
    add("kevin-pfeffer", [
        ("accord juridique sur la faisabilité et la solidité du dossier du parti a été trouvé avec deux banques européennes",
         "2026-11-10",
         "Propos recueillis par franceinfo (« Info franceinfo », 10 novembre 2026), qui le présente comme le trésorier du parti. Il se dit « assez optimiste » au vu de « discussions très avancées ». Selon franceinfo, les deux banques ne sont pas nommées et sont situées dans deux pays différents ; aucune banque française n'a accepté à ce jour de prêter au RN pour la campagne de Marine Le Pen ; le parti cherche 10,6 millions d'euros. Un accord pourrait aboutir « d'ici la fin du mois », selon un cadre du parti cité par franceinfo. Il s'agit d'un pré-accord, pas d'un prêt signé.",
         U_PFEFFER, F, "france"),
    ])
    add_steps("kevin-pfeffer", [
        step("2026-11-10", "Pré-accord bancaire pour 2027",
             "franceinfo, qui le présente comme trésorier du RN, rapporte qu'un pré-accord a été trouvé avec deux banques européennes non nommées pour un prêt destiné à la campagne présidentielle de Marine Le Pen ; le parti cherche 10,6 millions d'euros.",
             U_PFEFFER, "franceinfo"),
    ])

    # Jordan Bardella, « Face à BFM », 10 novembre 2026
    add("jordan-bardella", [
        ("Il n’y a pas de racisme systémique en France. Sinon pourquoi plus de 500.000 personnes voudraient venir chaque année dans notre pays? J’en ai ras le bol qu’on mette systématiquement la France sur le banc des accusés",
         "2026-11-10",
         "« Face à BFM » (BFMTV), 10 novembre 2026, cité par BFMTV. Il revient sur l'entretien de Marine Le Pen à CBS (« 60 Minutes ») où elle dit que la France est « le pays le moins raciste du monde », et se dit d'accord « à 300% ». Dans la même émission, interrogé sur l'attentat de Trappes et sur les accusations visant le RN, il répond : « nous avons condamné ce drame », et met en cause des « dirigeants de gauche et d'extrême gauche ».",
         U_BARDELLA_BFM, F, "france"),
        ("Une petite victoire de la démocratie et de la liberté : la délirante pétition d'extrême gauche appelant à la censure de CNews, média régulièrement suivi par des millions de Français, ne passera pas l'étape de la commission parlementaire, grâce aux voix des élus Rassemblement National.",
         "2026-11-10",
         "Message publié sur son compte X officiel (@J_Bardella) le 10 novembre 2026 à 14 h 39 UTC, après le classement de la pétition « Supprimer CNews de l'audiovisuel français » par la commission des affaires culturelles de l'Assemblée nationale (28 voix contre 25). Le message se termine par : « Face aux tentations totalitaires de l'extrême gauche, la vigilance doit être permanente ! » France 24, avec l'AFP, cite le même message. Les auteurs de la pétition comparaient CNews à « une machine de propagande », ce que la chaîne conteste en disant défendre la liberté d'expression (France 24).",
         U_BARDELLA_X_CNEWS, MS, "france"),
        ("Le temps n'est plus à voter pour des partis à 4%: l'enjeu, c'est de gagner cette élection. Quand on est patriote comme le sont les électeurs d'Eric Zemmour, quand on est traversé par l'angoisse existentielle de voir la France disparaître, alors il faut se rassembler.",
         "2026-11-10",
         "Message avec extrait vidéo publié sur son compte X officiel (@J_Bardella) le 10 novembre 2026 à 23 h 08 UTC, le soir de son passage dans « Face à BFM » et de l'annonce de candidature d'Éric Zemmour sur TF1. Il s'adresse aux électeurs d'Éric Zemmour ; le message ne nomme pas d'accord entre partis.",
         U_BARDELLA_X_ZEM, F, "france"),
    ])

    # Éric Zemmour, 20 heures de TF1, 10 novembre 2026
    add("eric-zemmour", [
        ("Je ne veux pas seulement contrôler les flux migratoires, je veux qu'il y ait moins d'immigrés à la fin de mon quinquennat",
         "2026-11-10",
         "Journal de 20 heures de TF1, 10 novembre 2026, jour de l'annonce de sa candidature, cité par RTL. Selon RTL, il chiffre cette baisse à « deux millions », en comptant par exemple « les prisonniers, les délinquants, les criminels étrangers », et ajoute : « Cela n'a rien de criminel ni de barbare ». Le Bien public, avec l'AFP, écrit qu'il veut aussi expulser « les chômeurs étrangers de plus de six mois », même en situation régulière, et rapporte que Dominique Sopo, président de SOS Racisme, juge que cette candidature pose « un problème républicain ».",
         U_ZEMMOUR_RTL, F, "france",
         {"url": U_ZEMMOUR_TF1, "platform": "tf1info.fr",
          "title": "Présidentielle 2027 : Éric Zemmour officialise sa candidature au 20H de TF1",
          "source": "TF1 Info (site officiel)"}),
    ])

    # France terre d'asile et Désinfox-Migrations saisissent l'Arcom
    add_node(
        "france-terre-dasile", "France terre d'asile", "org", "Association d'accueil des demandeurs d'asile et des réfugiés",
        "Sud Ouest, avec l'AFP, la présente le 10 novembre 2026 comme un opérateur public chargé de l'accueil des demandeurs d'asile et des réfugiés, dirigé par Jean-François Beaugrand. Le même jour, avec l'association Désinfox-Migrations (chercheurs et citoyens), elle annonce avoir saisi l'Arcom au sujet de quatre séquences diffusées sur CNews et Europe 1, et publie le rapport « Pour un débat éclairé sur les migrations ». Une saisine n'est pas une décision : l'Arcom ne s'est pas prononcée publiquement à ce stade.",
        [st(
            "Nous sommes sidérés de l’état du débat public sur le sujet de l’immigration, de la multiplication des fausses informations sur le sujet, comme la mise en avant de la fausse théorie du grand remplacement ou d’un prétendu appel d’air",
            "2026-11-10",
            "Jean-François Beaugrand, directeur général de France terre d'asile, en conférence de presse, cité par Sud Ouest avec l'AFP. Il ajoute : « Nous ne sommes pas opposés au débat public sur la question migratoire, on peut avoir des désaccords sur les orientations politiques, mais il doit se faire à partir de bases objectives et sourcées ». Selon Sud Ouest, les deux associations ont saisi l'Arcom pour la reprise « sans contradiction » d'affirmations « manifestement erronées » liées à la théorie du « grand remplacement » sur CNews et Europe 1 les 17 et 18 septembre. Le communiqué des associations parle de « quatre séquences ». Les articles lus ne rapportent pas de réponse de CNews ni d'Europe 1.",
            U_FTDA_SO, F)],
        ORG, "Associations & représentants")
    for tgt in ("cnews", "europe1"):
        link("france-terre-dasile", tgt,
             "saisine de l'Arcom, avec Désinfox-Migrations, au sujet de séquences liées à la théorie du « grand remplacement » (annoncée le 10/11/2026 ; pas de décision de l'Arcom à ce stade)",
             U_FTDA, "2026-11-10")
        E[-1]["section"] = "france"
        E[-1]["nature"] = "opposition"
