# -*- coding: utf-8 -*-
"""v45 : matin du 16 novembre 2026.
Phrases lues le jour même sur les pages citées.
Les crochets [ ] ne sont pas utilisés : les phrases sont continues.
« les deux extrêmes », « milice », « nazifier » sont les mots des personnes, pas ceux du site."""

G = "Gaza – déclarations"
F = "France – normalisation de l'extrême droite"

U_AJC = "https://ajcfrance.com/radiographie-de-lantisemitisme-en-france-edition-2027/"
U_FI = "https://www.radiofrance.fr/franceinter/podcasts/l-invite-de-6h20/la-question-de-6h20-du-lundi-16-novembre-2026-4955302"
U_SUD = "https://www.sudradio.fr/faits-divers/marseille-de-jeunes-militants-du-rn-agresses-dans-un-bar"
U_JDD = "https://www.lejdd.fr/Societe/c8-cnews-nicolas-sarkozy-denonce-une-dangereuse-conception-de-la-democratie-188706"
U_BFM = "https://www.bfmtv.com/politique/elections/presidentielle/une-curieuse-vision-de-la-democratie-nicolas-sarkozy-se-dit-contre-l-interdiction-de-lfi-suggeree-par-bruno-retailleau_AN-202611130717.html"

AJC_MED = ("Page de l'American Jewish Committee, datée du 15 novembre 2026. "
           "Enquête Ifop pour l'AJC et la Fondapol. "
           "Anne-Sophie Sebban-Bécache la présente le 16 novembre 2026 sur France Inter. "
           "La page écrit aussi qu'en 2025 le ministère de l'Intérieur a recensé 1 320 actes antisémites.")


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
            n.setdefault("statements", []).append(s)
            seen.add(quote)
            if section not in n.setdefault("sections", []):
                n["sections"].append(section)

    def add_link(src, tgt, rel, url, date, section, nature):
        for e in E:
            if e["source"] == src and e["target"] == tgt and e.get("url") == url:
                return
        link(src, tgt, rel, url, date)
        E[-1]["section"] = section
        E[-1]["nature"] = nature

    def person(pid, name, role, desc, cat, sub, secs, statements, steps):
        add_node(pid, name, "person", role, desc, [], cat, sub, secs)
        add(pid, statements)
        by[pid]["parcours"] = steps

    add_node(
        "ajc", "American Jewish Committee (AJC)", "org",
        "Organisation. Enquête Ifop avec la Fondapol, page datée du 15 novembre 2026",
        "L'AJC publie une enquête sur l'antisémitisme en France. La page date le texte du 15 novembre 2026. Le 16 novembre, Anne-Sophie Sebban-Bécache le présente sur France Inter.",
        [], "Associations & représentants", "Associations & représentants", ("france", "gaza"))
    add("ajc", [
        ("À l’antisémitisme historiquement ancré à l’extrême droite s’ajoute une diffusion croissante des préjugés antisémites parmi les sympathisants de l’extrême gauche.",
         "2026-11-15", AJC_MED, U_AJC, F, "france"),
        ("Pour la première fois, les idées d’extrême gauche et d’extrême droite sont citées dans les mêmes proportions (25 % chacune) parmi les principales causes de l’antisémitisme. En 2022, les premières n’étaient mentionnées que par 13 % des Français, contre 36 % pour les secondes.",
         "2026-11-15", AJC_MED, U_AJC, F, "france"),
        ("Alors que les préjugés traditionnels demeurent présents chez les sympathisants du Rassemblement national, ils sont désormais plus répandus parmi ceux de La France insoumise sur la quasi-totalité des indicateurs mesurés.",
         "2026-11-15", AJC_MED, U_AJC, F, "france"),
        ("Ainsi, 51 % des sympathisants LFI estiment que les Juifs ont trop de pouvoir dans l’économie et la finance (+17 points depuis 2022), et 50 % dans les médias (+21 points). Par ailleurs, 81 % considèrent qu’Israël se comporte envers les Palestiniens comme les nazis envers les Juifs.",
         "2026-11-15",
         AJC_MED + " Le « par ailleurs » suit la phrase sur les sympathisants LFI.",
         U_AJC, G, "gaza"),
        ("58 % des Français estiment que Jean-Luc Mélenchon contribue à la montée de l’antisémitisme, contre 53 % pour Éric Zemmour et 47 % pour Marine Le Pen.",
         "2026-11-15", AJC_MED, U_AJC, F, "france"),
        ("69 % des Français juifs déclarent qu’ils pourraient quitter la France si Jean-Luc Mélenchon était élu président de la République en 2027, dont 40 % « certainement ».",
         "2026-11-15",
         AJC_MED + " La phrase suivante de la page rappelle le chiffre de 2024 pour un candidat LFI : 57 %.",
         U_AJC, F, "france"),
        ("Une élection de Marine Le Pen conduirait 31 % d’entre eux à envisager de quitter le pays.",
         "2026-11-15",
         AJC_MED + " « d’entre eux » renvoie, dans le même paragraphe, aux Français juifs.",
         U_AJC, F, "france"),
        ("Cette hostilité dépasse parfois la critique de la politique israélienne pour se reporter sur les Juifs de France : 79 % d’entre eux déclarent s’être déjà sentis accusés ou rendus responsables des actions du gouvernement israélien.",
         "2026-11-15", AJC_MED, U_AJC, G, "gaza"),
        ("Près d’un jeune de 18 à 24 ans sur deux (49 %) considère qu’Israël se comporte envers les Palestiniens comme les nazis envers les Juifs, une proportion en hausse de 7 points depuis 2024.",
         "2026-11-15", AJC_MED, U_AJC, G, "gaza"),
        ("82 % des Français juifs déclarent avoir déjà été victimes d’un acte antisémite au cours de leur vie.",
         "2026-11-15", AJC_MED, U_AJC, F, "france"),
    ])
    by["ajc"]["parcours"] = [
        step("2026-11-15", "Enquête sur l'antisémitisme",
             "L'AJC publie, avec la Fondapol, une enquête Ifop. La page rapproche l'extrême droite, l'extrême gauche et le rejet d'Israël, tels que l'enquête les mesure.",
             U_AJC, "AJC"),
    ]

    person(
        "anne-sophie-sebban-becache", "Anne-Sophie Sebban-Bécache",
        "Vice-présidente de l'antenne Europe de l'American Jewish Committee (France Inter, 16 novembre 2026)",
        "Le 16 novembre 2026, sur France Inter, elle présente l'enquête de l'AJC. Elle parle d'une fissure, d'une frontière de ce qui est acceptable, et des « deux extrêmes ».",
        "Associations & représentants", "Associations & représentants", ("france",),
        [
            ("Quelque chose s'est fissuré entre la France et une partie croissante des Français de confession juive",
             "2026-11-16",
             "France Inter, L'invité de 6h20, 16 novembre 2026. La page de l'émission reprend la phrase. franceinfo publie les mêmes mots le matin.",
             U_FI, F, "france"),
            ("Une frontière s'est déplacée dans ce qui est socialement acceptable aujourd'hui",
             "2026-11-16",
             "France Inter, 16 novembre 2026. La page ajoute qu'elle note un sentiment de haine « alimenté par tous les phénomènes qui traversent notre société ».",
             U_FI, F, "france"),
            ("On voit aujourd'hui dans la polarisation de la politique en France comment les deux extrêmes utilisent cette question de l'antisémitisme et la nourrissent",
             "2026-11-16",
             "France Inter, 16 novembre 2026. « les deux extrêmes » est sa formule. La page dit que l'enquête est, selon elle, un « dernier avertissement ». Les pourcentages Mélenchon et Le Pen sont ceux de la page de l'AJC, pas une phrase distincte d'elle sur cette antenne.",
             U_FI, F, "france"),
            ("Il y a cette question de la tolérance zéro qui n'est pas véritablement appliquée en matière d'antisémitisme et l'idée que les institutions de la République ne sont plus tout à fait à même de nous protéger",
             "2026-11-16",
             "France Inter, 16 novembre 2026. La page écrit aussi qu'elle décrit « le sentiment d'une forme d'impunité face à l'antisémitisme ».",
             U_FI, F, "france"),
        ],
        [step("2026-11-16", "France Inter, enquête de l'AJC",
              "Elle présente sur France Inter la radiographie de l'antisémitisme publiée par l'AJC.",
              U_FI, "France Inter")],
    )
    add_link("anne-sophie-sebban-becache", "ajc",
             "vice-présidente de l'antenne Europe, elle présente l'enquête de l'AJC sur France Inter (16/11/2026)",
             U_FI, "2026-11-16", "france", "autre")
    add_link("ajc", "marine-le-pen",
             "l'enquête indique que 47 % des Français estiment qu'elle contribue à la montée de l'antisémitisme, et que 31 % des Français juifs envisageraient de quitter le pays si elle était élue (page du 15/11/2026)",
             U_AJC, "2026-11-15", "france", "autre")
    add_link("ajc", "eric-zemmour",
             "l'enquête indique que 53 % des Français estiment qu'il contribue à la montée de l'antisémitisme (page du 15/11/2026)",
             U_AJC, "2026-11-15", "france", "autre")
    add_link("ajc", "jean-luc-melenchon",
             "l'enquête indique que 58 % des Français estiment qu'il contribue à la montée de l'antisémitisme, et que 69 % des Français juifs déclarent qu'ils pourraient quitter la France s'il était élu (page du 15/11/2026)",
             U_AJC, "2026-11-15", "france", "autre")

    person(
        "olivier-rioult", "Olivier Rioult",
        "Maire RN des 11e et 12e arrondissements de Marseille (Sud Radio, 16 novembre 2026)",
        "Le 16 novembre 2026, sur Sud Radio, il parle d'une agression visant des militants du RN et de La Cocarde. Il ne nomme personne. « milice » et « nazifier » sont ses mots.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("C’était des jeunes qui étaient tranquillement en train de boire un verre et qui ont subi une attaque de la part d’un commando cagoulé et habillé en noir",
             "2026-11-16",
             "Sud Radio, « C'est à la une », 16 novembre 2026, au micro de Jacques Cardoze. La page le présente comme maire RN des 11e et 12e arrondissements de Marseille. Il ne nomme aucune personne.",
             U_SUD, F, "france"),
            ("Cela fait référence à des black blocs. Je pense que c’était une milice d’extrême-gauche, comme on en voit à Marseille et un peu partout en France.",
             "2026-11-16",
             "Sud Radio, 16 novembre 2026. « Je pense » est dans la phrase. La page ne présente pas cette qualification comme une décision de justice.",
             U_SUD, F, "france"),
            ("Les mots qui m’ont été rapportés quand ils étaient sur place est qu’ils cherchaient des fascistes.",
             "2026-11-16",
             "Sud Radio, 16 novembre 2026. La tournure « est qu’ils » est celle de la page. Il dit rapporter des mots, il ne nomme personne.",
             U_SUD, F, "france"),
            ("Il ne faut pas s’étonner que cela arrive quand vous avez des élus de gauche et d’extrême-gauche qui passent leur temps à nous nazifier.",
             "2026-11-16",
             "Sud Radio, 16 novembre 2026. Il ajoute : « Aujourd’hui, des militants, hier des journalistes, et demain des quidams. Il y a deux poids deux mesures : nous ne sommes pas les bonnes victimes. » Il dit aussi que deux jeunes ont reçu des coups et qu’un client a eu le nez cassé. Aucun nom.",
             U_SUD, F, "france"),
        ],
        [step("2026-11-16", "Sud Radio, agression à Marseille",
              "Il parle sur Sud Radio d'une agression visant des militants du RN et de La Cocarde. Il ne nomme personne.",
              U_SUD, "Sud Radio")],
    )
    add_link("olivier-rioult", "rn",
             "Sud Radio le présente comme maire RN des 11e et 12e arrondissements de Marseille (16/11/2026)",
             U_SUD, "2026-11-16", "france", "ascension")

    add("nicolas-sarkozy", [
        ("Un scandale démocratique sans précédent.",
         "2026-11-13",
         "Entretien au Figaro publié le 13 novembre 2026, cité par le JDD le 15 novembre 2026 à 1 h. La phrase qualifie, dans l'article du JDD, la fermeture de C8 en 2025.",
         U_JDD, F, "france"),
        ("bien étrange et dangereuse conception de la démocratie",
         "2026-11-13",
         "Le JDD, 15 novembre 2026, cite l'entretien au Figaro du 13 novembre. Le journal écrit qu'il « dénonce » cette formule face aux appels à la suppression de CNews.",
         U_JDD, F, "france"),
        ("Il ne me serait jamais venu à l’idée de plaider pour l’interdiction de L’Humanité !",
         "2026-11-13",
         "Le JDD, 15 novembre 2026, citant l'entretien au Figaro du 13 novembre, à propos de CNews.",
         U_JDD, F, "france"),
        ("Je n’accepterai jamais qu’un journaliste quelles que soient ses opinions soit menacé dans l’exercice de son travail.",
         "2026-11-13",
         "Le JDD, 15 novembre 2026, citant l'entretien au Figaro du 13 novembre. La phrase suivante citée est : « Cette indignation ne doit pas être à géométrie variable. »",
         U_JDD, F, "france"),
        ("Cette indignation ne doit pas être à géométrie variable.",
         "2026-11-13",
         "Le JDD, 15 novembre 2026, citant l'entretien au Figaro du 13 novembre.",
         U_JDD, F, "france"),
        ("Vouloir interdire LFI ou le RN, les deux partis donnés par les sondages au deuxième tour de la présidentielle, c’est là encore une curieuse vision de la démocratie",
         "2026-11-13",
         "BFMTV, 13 novembre 2026, citant l'entretien au Figaro du même jour. BFMTV écrit que ce raisonnement « vaut aussi » pour le Rassemblement national, puis donne cette phrase. Il dit aussi : « L’interdiction de La France Insoumise, dont le candidat est donné au second tour par tous les sondages, n’aurait aucun sens (...) Je n’ai aucune sympathie pour le mouvement de Jean-Luc Mélenchon mais, à partir du moment où les Insoumis ont le droit de concourir aux élections, cela signifie qu’ils font partie de l’arc républicain ». Les points de suspension entre parenthèses sont ceux de BFMTV.",
         U_BFM, F, "france"),
    ])
    add_link("nicolas-sarkozy", "cnews",
             "il parle d'une « bien étrange et dangereuse conception de la démocratie » face aux appels à supprimer la chaîne (Figaro du 13/11/2026, cité par le JDD le 15/11)",
             U_JDD, "2026-11-13", "france", "autre")
    add_link("nicolas-sarkozy", "rn",
             "il dit que vouloir interdire le RN, comme LFI, est « une curieuse vision de la démocratie » (Figaro du 13/11/2026, cité par BFMTV)",
             U_BFM, "2026-11-13", "france", "autre")
