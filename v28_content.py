# -*- coding: utf-8 -*-
"""v28 : instituts de sondage, actionnariats documentés, classement JDD, Zemmour 2021-2022.
Chaque URL a été ouverte le 11 novembre 2026. Les phrases entre guillemets sont celles de la page.
Aucune intention n'est ajoutée. Odoxa n'est pas créé : la page lue ne nomme pas d'actionnaire."""

MS = "Médias – structure"
NU = "Nuance / contexte"
MED = "Médias & propriétaires"
ORG = "Organisations & institutions"

U_FIGARO = "https://www.lefigaro.fr/flash-eco/l-ifop-vendu-par-la-famille-dentressangle-au-fonds-lfpi-20220725"
U_IFOP = "https://www.ifopgroup.com/article/larrivee-de-lfpi-nous-ouvre-de-superbes-perspectives-de-developpement-interview-stephane-truchi/"
U_PAPPERS = "https://www.pappers.fr/entreprise/ifop-348698754"
U_OW = "https://www.opinion-way.com/en/about-us/who-we-are/"
U_M20 = "https://www.20minutes.fr/societe/4235898-20260724-bollore-arnault-independants-appartiennent-instituts-sondage"
U_CSA = "https://csa.eu/news/xavier-terryn-et-pierre-labarraque-nommes-partners-chez-csa/"
U_HAVAS = "https://www.havas.com/press_release/havas-nv-announces-increased-shareholding-by-compagnie-de-letoile-des-mers/"
U_BOL = "https://www.bollore.com/fr/activites-et-participations-2/communication/"
U_ECHOS = "https://www.lesechos.fr/tech-medias/medias/la-famille-bollore-detient-plus-de-la-majorite-du-capital-de-havas-2217523"
U_JDD = "https://www.lejdd.fr/Societe/exclusif-top-50-jdd-decouvrez-les-personnalites-preferees-des-francais-165530"
U_LOI = "https://www.commission-des-sondages.fr/lois/lois.htm"
U_TOL = "https://tolunacorporate.com/fr/toluna-france-entre-dans-une-nouvelle-ere-avec-nathalie-perrio-combeaux-comme-ceo/"
U_ELABE = "https://elabe.fr/mentions-legales/"
U_CB = "https://www.cbnews.fr/conseil/etudes-conseils-elabe-linkup-se-rapprochent"
U_CHAL = "https://www.challenges.fr/politique/presidentielle-2022-eric-zemmour-double-marine-le-pen-et-s-envole-vers-le-second-tour_783521"
U_CC = "https://www.conseil-constitutionnel.fr/actualites/annonce-par-laurent-fabius-president-du-conseil-constitutionnel-des-resultats-officiels-du-premier"

NEW_URLS = [
    U_FIGARO, U_IFOP, U_PAPPERS, U_OW, U_M20, U_CSA, U_HAVAS, U_BOL, U_ECHOS,
    U_JDD, U_LOI, U_TOL, U_ELABE, U_CB, U_CHAL, U_CC,
]


def apply(N, E, by, step, node, link, st):
    def add_node(*a, **k):
        node(*a, **k)
        by[a[0]] = N[-1]
        return N[-1]

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

    def own(s, t, rel, url, date, stories=("sondages",)):
        link(s, t, rel, url, date)
        E[-1]["nature"] = "ascension"
        E[-1]["section"] = "france"
        E[-1]["stories"] = list(stories)

    def cou(s, t, rel, url, date, stories=("sondages",)):
        link(s, t, rel, url, date)
        E[-1]["nature"] = "coulisses"
        E[-1]["section"] = "france"
        E[-1]["stories"] = list(stories)

    add_node(
        "lfpi", "LFPI", "org", "Gestionnaire d'actifs",
        "Le Figaro du 25 juillet 2022 écrit qu'un communiqué commun de l'Ifop, de Dentressangle et de LFPI annonce la vente de l'institut au fonds LFPI. L'article présente LFPI comme l'un des premiers gestionnaires d'actifs indépendants multi-stratégies en Europe, avec 14 milliards d'euros d'actifs sous gestion. Cette fiche ne dit pas quelle part LFPI détient encore en novembre 2026 : le registre consulté ce jour-là ne publie pas la liste des actionnaires.",
        [st(
            "L'institut de sondage d'opinion et d'études de marché Ifop a été vendu par la famille Dentressangle au fonds LFPI, ont annoncé lundi les trois sociétés dans un communiqué commun, confirmant une information de la lettre A.",
            "2022-07-25",
            "Le Figaro, avec l'AFP. Le même article rappelle que la famille Dentressangle était l'actionnaire majoritaire depuis fin 2016, après la famille Parisot. Le montant n'est pas indiqué. Stéphane Truchi, présenté comme patron du groupe Ifop, écrit à l'AFP : « Avec LFPI, un nouveau chapitre va s'écrire dans la longue et belle histoire du Groupe Ifop, avec l'ambition de poursuivre notre dynamique de croissance ».",
            U_FIGARO, MS)],
        MED, "Propriétaires, financeurs & groupes")

    add_node(
        "ifop", "Ifop", "org", "Institut de sondages et d'études",
        "Le Figaro du 25 juillet 2022 rapporte la vente de l'Ifop par la famille Dentressangle au fonds LFPI. Le 4 novembre 2022, le site du groupe publie un entretien de Stéphane Truchi où LFPI est appelé nouvel actionnaire majoritaire, et où il dit l'équipe de direction également présente au capital. La page Pappers, mise à jour du RCS le 10 novembre 2026, désigne ETUDINVEST comme dirigeant. L'annonce BODACC du 27 décembre 2022, reproduite sur cette page, constate la nomination d'ETUDINVEST comme président et le départ de LFPI Gestion du conseil de surveillance, à l'occasion d'un changement de forme juridique. La liste des actionnaires n'est pas sur la page consultée. Le 24 juillet 2026, 20 Minutes écrit encore que l'Ifop « est détenu par des investisseurs financiers regroupés dans le fonds LFPI ».",
        [st(
            "L’annonce de la cession du Groupe Ifop avec l’arrivée de LFPI en tant que nouvel actionnaire majoritaire fait partie des évènements marquants de ces derniers mois dans le paysage des études marketing.",
            "2022-11-04",
            "Site du groupe Ifop, introduction d'un entretien de Stéphane Truchi, alors présenté comme CEO, publié le 4 novembre 2022. Il répond : « nous ne sommes pas dans la course à la performance à tout prix, mais plutôt dans un LBO prudent, raisonnable, notre équipe managériale étant présente dans l’actionnariat ». La page Pappers consultée le 11 novembre 2026 ne publie pas les bénéficiaires effectifs et nomme ETUDINVEST comme dirigeant.",
            U_IFOP, MS)],
        ORG, "Instituts de sondage")

    add_node(
        "lvmh", "LVMH", "org", "Groupe",
        "20 Minutes écrit le 24 juillet 2026 que le groupe Les Echos-Le Parisien est une filiale de LVMH. La page « Who we are » d'OpinionWay, lue le 11 novembre 2026, présente l'institut comme entré en 2022 dans « the Les Echos-Le Parisien Group (LVMH) ». Cette fiche ne décrit pas d'autre activité du groupe.",
        [], MED, "Propriétaires, financeurs & groupes")

    add_node(
        "les-echos-le-parisien", "Les Echos-Le Parisien", "org", "Groupe de presse",
        "20 Minutes le présente le 24 juillet 2026 comme une filiale de LVMH, et écrit qu'il a racheté 75 % d'OpinionWay en 2022. Le même article écrit que, selon L'Informé en mai 2026, LVMH a prévu de mettre l'institut en vente. Il ne constate pas une cession signée. La page d'OpinionWay lue le 11 novembre 2026 présente toujours l'entrée dans ce groupe en 2022.",
        [st(
            "Racheté à 75 % en 2022 par le groupe Les Echos-Le Parisien, filiale du groupe LVMH du milliardaire Bernard Arnault, OpinionWay est scruté pour la même raison que CSA, car ses sondages ont pu alimenter des médias appartenant à son propre actionnaire.",
            "2026-07-24",
            "20 Minutes, 24 juillet 2026. La phrase qui suit dans l'article : « Mais selon une information de l’Informé, publiée en mai, LVMH a prévu de mettre en vente l’institut. » L'article parle d'un projet de vente, pas d'une cession déjà signée. La page d'OpinionWay lue le 11 novembre 2026 écrit encore : « in 2022 it became part of the Les Echos-Le Parisien Group (LVMH) ».",
            U_M20, MS)],
        MED, "Propriétaires, financeurs & groupes")

    add_node(
        "opinionway", "OpinionWay", "org", "Institut d'études et de sondages",
        "La page « Who we are », lue le 11 novembre 2026, écrit qu'en 2022 l'institut est entré dans le groupe Les Echos-Le Parisien (LVMH). 20 Minutes écrit le 24 juillet 2026 que ce rachat a porté sur 75 % du capital, et que LVMH a prévu, selon L'Informé en mai, de mettre l'institut en vente. Cette fiche ne présente pas la vente comme réalisée.",
        [st(
            "The OpinionWay Group has grown constantly since its creation, and in 2022 it became part of the Les Echos-Le Parisien Group (LVMH), with the aim of accelerating its development and internationalisation in order to better serve its clients.",
            "2022",
            "Page « Who we are » d'OpinionWay, lue le 11 novembre 2026. La page mentionne aussi, plus bas, l'adhésion au réseau WIN comme partenaire exclusif pour la France depuis le 1er janvier 2026. Elle ne parle pas d'une cession. 20 Minutes, le 24 juillet 2026, écrit un projet de mise en vente selon L'Informé (mai 2026), sans en constater la signature.",
            U_OW, MS)],
        ORG, "Instituts de sondage")

    add_node(
        "havas", "Havas", "org", "Groupe de communication coté",
        "CSA écrit le 13 février 2026 faire partie du groupe Havas depuis 2015. Havas est coté à Amsterdam depuis décembre 2024, après la scission de Vivendi. Le site du groupe Bolloré indique qu'au 31 décembre 2025 le groupe détient 30,4 % du capital et des droits de vote de Havas. Le 20 février 2026, Havas annonce que la Compagnie de l'Étoile des Mers, contrôlée par Bolloré Participations, a acquis près de 19 % supplémentaires, et qu'après apport de la part détenue via YB6 cette holding détiendrait environ 22 %. Les Echos écrivent le 23 février 2026 que la famille Bolloré détient plus de 50 % des actions.",
        [st(
            "In addition to the 30.4% stake held by Bolloré SE in Havas since its listing on Euronext Amsterdam in December 2024, Compagnie de l’Etoile des Mers, controlled by Bolloré Participations, has acquired over the past months close to 19% of Havas NV.",
            "2026-02-20",
            "Communiqué de Havas NV, 20 février 2026. Le texte ajoute qu'à l'issue de l'apport de YB6, la Compagnie de l'Étoile des Mers « will hold approximately 22% » et que Yannick Bolloré, président-directeur général de Havas NV, en sera nommé président. Les Echos du 23 février 2026 titrent que la famille détient plus de la moitié du capital. Le site du groupe Bolloré, lu le 11 novembre 2026, maintient le chiffre de 30,4 % au 31 décembre 2025, après la scission de Vivendi.",
            U_HAVAS, MS)],
        MED, "Propriétaires, financeurs & groupes")

    add_node(
        "institut-csa", "Institut CSA", "org", "Institut d'études et de sondages",
        "CSA écrit le 13 février 2026, dans la présentation jointe à un communiqué de nominations : « CSA, dirigé par Yves Del Frate, CEO, fait partie du groupe Havas depuis 2015. » Le 4 janvier 2026, le JDD écrit que son Top 50, créé en 1988 avec l'Ifop, a été réalisé cette année par CSA. Havas n'est plus une filiale de Vivendi : le groupe est coté depuis la scission de décembre 2024. Voir la fiche Havas pour les pourcentages publiés en 2025 et 2026.",
        [st(
            "CSA, dirigé par Yves Del Frate, CEO, fait partie du groupe Havas depuis 2015.",
            "2026-02-13",
            "Communiqué de CSA du 13 février 2026 (nominations de Xavier Terryn et Pierre Labarraque), rubrique « À propos de CSA ». Le 4 janvier 2026, le JDD écrit avoir fait réaliser son Top 50 par cet institut, sur 1 006 personnes interrogées du 17 au 22 décembre 2025.",
            U_CSA, MS)],
        ORG, "Instituts de sondage")

    add_node(
        "toluna", "Toluna", "org", "Groupe d'études",
        "Le 28 septembre 2026, Toluna annonce que Harris Interactive a été acquis par Toluna en 2014, et que Nathalie Perrio-Combeaux, cofondatrice de Harris Interactive avec Patrick Van Bloeme, prend seule la direction de Toluna France le 29 septembre 2026. Le communiqué nomme Frederic Charles-Petit comme fondateur et CEO de Toluna. Il ne désigne pas un groupe de médias comme actionnaire.",
        [st(
            "Nathalie et Patrick Van Bloeme ont co-fondé Harris Interactive en 1995, contribuant à faire émerger les études en ligne en France, et ont dirigé l’entreprise ensemble depuis lors, devenant co-CEOs de Toluna France à la suite de l’acquisition de Harris Interactive par Toluna en 2014.",
            "2026-09-28",
            "Communiqué de Toluna, Paris, 28 septembre 2026. Nathalie Perrio-Combeaux devient seule CEO de Toluna France le 29 septembre 2026. Patrick Van Bloeme quitte ses fonctions le 28 septembre. Le texte ne nomme pas de groupe de presse ou de chaîne au capital.",
            U_TOL, MS)],
        ORG, "Instituts de sondage")

    add_node(
        "harris-interactive", "Harris Interactive", "org", "Institut d'études",
        "Toluna écrit le 28 septembre 2026 avoir acquis Harris Interactive en 2014. Le communiqué ne désigne pas d'autre actionnaire, ni un groupe de médias. Challenges du 6 octobre 2021 publie un sondage « Harris Interactive » pour Challenges sur les intentions de vote, qui place alors Éric Zemmour à 17 %.",
        [], ORG, "Instituts de sondage")

    add_node(
        "elabe", "Elabe", "org", "Cabinet d'études et de conseil",
        "Les mentions légales d'elabe.fr, lues le 11 novembre 2026, présentent l'éditeur comme « BERNARD SANANES CONSEILS – ELABE », SAS, et Bernard Sananes comme directeur de la publication et président. CB News du 5 septembre 2022 écrit que Bernard Sananès, Marie-Rose Beslin, Laurence Bedeau, Benoit Viala, Sandrine Raffin et Philippe Raffin deviennent actionnaires de la structure qui détiendra intégralement Elabe et LinkUp. Ni cette page ni les mentions légales ne nomment un groupe de médias.",
        [st(
            "Bernard Sananès, Marie-Rose Beslin, Laurence Bedeau, et Benoit Viala, associés au sein d’Elabe, ainsi que Sandrine Raffin et Philippe Raffin, associés au sein de LinkUp, deviennent actionnaires de la nouvelle structure qui détiendra intégralement le capital des deux sociétés, « gage d’indépendance et de vision de long terme », assure un communiqué, tandis que Bernard Sananès devient le président de cette structure.",
            "2022-09-05",
            "CB News, 5 septembre 2022, citant le communiqué du rapprochement. Bernard Sananès en devient le président. Les mentions légales lues le 11 novembre 2026 désignent encore « BERNARD SANANES CONSEILS – ELABE » et Bernard Sananes comme président. Elles ne citent pas de groupe de médias.",
            U_CB, MS)],
        ORG, "Instituts de sondage")

    add_node(
        "commission-des-sondages", "Commission des sondages", "org",
        "Autorité créée par la loi du 19 juillet 1977",
        "La loi n° 77-808 du 19 juillet 1977, dans le texte publié sur le site de la Commission, régit les sondages publiés ou diffusés qui portent sur le débat électoral. Elle ne s'applique pas, d'après cet article 1er, à toute enquête d'opinion. L'article 3 prévoit que la notice déposée avant publication indique, s'il y a lieu, la gratification versée aux personnes interrogées. Le site ne fixe aucun montant.",
        [st(
            "Sont régis par la présente loi les sondages publiés, diffusés ou rendus publics sur le territoire national, portant sur des sujets liés, de manière directe ou indirecte, au débat électoral.",
            "2016-04-25",
            "Article 1er de la loi n° 77-808 du 19 juillet 1977, texte consolidé publié sur le site de la Commission des sondages. La page indique que l'article a été modifié par la loi n° 2016-508 du 25 avril 2016. Le même article définit le sondage comme une enquête par échantillon et vise aussi les simulations de vote réalisées à partir de ces sondages.",
            U_LOI, NU),
         st(
            "S’il y a lieu, la nature et la valeur de la gratification perçue par les personnes interrogées",
            "2016-04-25",
            "Article 3, 6°, de la même loi, sur la notice déposée à la Commission avant la publication d'un sondage entrant dans le champ de l'article 1er. La mention n'existe que « s'il y a lieu ». La page ne donne ni un barème ni un montant, pour OpinionWay ou pour un autre institut.",
            U_LOI, NU)],
        ORG, "Institutions publiques")

    add("jdd", [
        ("Le Top 50 du JDD, créé en 1988 avec l’Ifop, a été réalisé cette année par l’institut CSA, sur un échantillon représentatif de 1 006 Français âgés de 15 ans et plus.",
         "2026-01-04",
         "Le Journal du dimanche, 4 janvier 2026 (Antonin André). L'article précise que 121 personnalités ont été soumises, et que l'étude s'est déroulée du 17 au 22 décembre 2025. Il place Jordan Bardella 4e (10e l'année précédente), Marine Le Pen 7e (11e), l'entrée de Marion Maréchal à la 30e place, Philippe de Villiers 37e (77e l'année précédente) et Nicolas Sarkozy 53e. Il cite trois livres chez Fayard : « Ce que veulent les Français » de Jordan Bardella (100 000 exemplaires), « Populicide » de Philippe de Villiers (175 000) et « Journal d’un prisonnier » de Nicolas Sarkozy (plus de 180 000).",
         U_JDD, MS, "france"),
        ("Le Monde soulevait que les sept responsables politiques arrivés en tête étaient tous publiés chez Fayard….",
         "2026-07-24",
         "20 Minutes, 24 juillet 2026, à propos du Top 50 du JDD réalisé par CSA. La phrase est attribuée au Monde par 20 Minutes. L'article du JDD du 4 janvier 2026, lui, cite trois ouvrages Fayard (Bardella, Villiers, Sarkozy) et place en tête du classement général Jean-Jacques Goldman, Zinédine Zidane et Omar Sy. La page du Monde n'a pas renvoyé le corps de l'article le 11 novembre 2026.",
         U_M20, MS, "france"),
    ])

    add_steps("eric-zemmour", [
        step("2021-10-06", "Sondage Harris Interactive pour Challenges",
             "Challenges écrit qu'il « n’a toujours pas déclaré sa candidature » et que, « en moins d’un mois », il est « passant de 7% à 17% des intentions de vote ». L'enquête, en ligne du 1er au 4 octobre 2021, porte sur 1 310 personnes, dont 1 062 inscrites sur les listes électorales. L'article précise : « Les intentions de vote mesurent un rapport de force à un moment donné. Elles ne peuvent en aucun cas être considérées comme étant prédictives des résultats du scrutin. »",
             U_CHAL, "Challenges"),
        step("2022-04-10", "Premier tour",
             "Le 13 avril 2022, Laurent Fabius, président du Conseil constitutionnel, annonce les résultats officiels du premier tour du 10 avril : Eric Zemmour, 2 485 226 voix, soit 7,07 % des suffrages exprimés. Les deux candidats en tête sont Emmanuel Macron et Marine Le Pen.",
             U_CC, "Conseil constitutionnel"),
    ])

    add_steps("ifop", [
        step("1938", "Création indiquée par Le Figaro",
             "Le Figaro du 25 juillet 2022 parle de la « première entreprise de sondages d'opinion et d'études marketing à voir le jour en France en 1938 ».",
             U_FIGARO, "Le Figaro"),
        step("2022-07-25", "Vente au fonds LFPI",
             "Un communiqué commun, rapporté par Le Figaro, annonce la vente par la famille Dentressangle au fonds LFPI. L'entretien du 4 novembre 2022 sur le site du groupe appelle LFPI l'actionnaire majoritaire et dit l'équipe de direction aussi au capital.",
             U_FIGARO, "Le Figaro"),
        step("2022-12-27", "Présidence d'ETUDINVEST au registre",
             "L'annonce BODACC reproduite par Pappers constate la nomination d'ETUDINVEST comme président et le départ de LFPI Gestion du conseil de surveillance. La page, à jour du RCS le 10 novembre 2026, ne publie pas la liste des actionnaires.",
             U_PAPPERS, "Pappers"),
        step("2026-01-04", "Le JDD change d'institut pour le Top 50",
             "Le JDD écrit que le Top 50, créé en 1988 avec l'Ifop, est réalisé cette année par CSA.",
             U_JDD, "Le JDD"),
    ])
    add_steps("opinionway", [
        step("2022", "Entrée dans Les Echos-Le Parisien",
             "La page de l'institut écrit : « in 2022 it became part of the Les Echos-Le Parisien Group (LVMH) ». 20 Minutes, le 24 juillet 2026, parle d'un rachat de 75 % et d'un projet de mise en vente, sans en constater la signature.",
             U_OW, "OpinionWay"),
    ])
    add_steps("institut-csa", [
        step("2015", "Entrée dans Havas",
             "Le communiqué du 13 février 2026 écrit que CSA « fait partie du groupe Havas depuis 2015 » et qu'Yves Del Frate en est le CEO.",
             U_CSA, "CSA"),
        step("2026-01-04", "Top 50 du JDD",
             "Le JDD écrit que ce classement, créé en 1988 avec l'Ifop, est réalisé cette année par CSA, auprès de 1 006 personnes, du 17 au 22 décembre 2025.",
             U_JDD, "Le JDD"),
    ])
    add_steps("havas", [
        step("2024-12", "Cotation après la scission de Vivendi",
             "Le communiqué du 20 février 2026 rappelle la cotation de Havas à Amsterdam en décembre 2024 et la part de 30,4 % détenue par Bolloré SE depuis cette cotation.",
             U_HAVAS, "Havas"),
        step("2026-02-23", "Participation familiale",
             "Les Echos écrivent que la famille Bolloré détient plus de 50 % des actions, après les achats de la Compagnie de l'Étoile des Mers.",
             U_ECHOS, "Les Echos"),
    ])
    add_steps("lfpi", [
        step("2022-07-25", "Acquisition de l'Ifop annoncée",
             "Le Figaro rapporte le communiqué commun. L'entretien du groupe Ifop du 4 novembre 2022 parle d'un actionnaire majoritaire et d'une équipe de direction également au capital.",
             U_FIGARO, "Le Figaro"),
    ])
    add_steps("les-echos-le-parisien", [
        step("2022", "Participation dans OpinionWay",
             "OpinionWay écrit être entré cette année-là dans le groupe. 20 Minutes précise le 24 juillet 2026 un rachat de 75 %, et un projet de revente non constaté comme signé.",
             U_OW, "OpinionWay"),
    ])
    add_steps("lvmh", [
        step("2026-07-24", "Filiale nommée par 20 Minutes",
             "20 Minutes présente Les Echos-Le Parisien comme une filiale de LVMH et décrit le projet de mise en vente d'OpinionWay selon L'Informé.",
             U_M20, "20 Minutes"),
    ])
    add_steps("harris-interactive", [
        step("2014", "Acquisition par Toluna",
             "Le communiqué de Toluna du 28 septembre 2026 date l'acquisition de 2014. Il ne nomme pas de groupe de médias.",
             U_TOL, "Toluna"),
        step("2021-10-06", "Sondage pour Challenges",
             "Challenges publie le sondage Harris Interactive qui crédite Éric Zemmour de 17 %, après un passage de 7 % à 17 % « en moins d’un mois », et rappelle que ces intentions ne prédisent pas le scrutin.",
             U_CHAL, "Challenges"),
    ])
    add_steps("toluna", [
        step("2014", "Acquisition de Harris Interactive",
             "Le communiqué du 28 septembre 2026 rappelle cette acquisition et la direction commune de Nathalie Perrio-Combeaux et Patrick Van Bloeme jusqu'au 28 septembre 2026.",
             U_TOL, "Toluna"),
        step("2026-09-29", "Direction de Toluna France",
             "Nathalie Perrio-Combeaux prend seule la direction. Frederic Charles-Petit est nommé dans le communiqué comme fondateur et CEO de Toluna.",
             U_TOL, "Toluna"),
    ])
    add_steps("elabe", [
        step("2022-09-05", "Actionnariat des associés",
             "CB News écrit que six associés d'Elabe et de LinkUp deviennent actionnaires de la structure qui détiendra les deux sociétés, et que Bernard Sananès en est le président.",
             U_CB, "CB News"),
        step("2026-11-11", "Mentions légales",
             "La page lue ce jour désigne « BERNARD SANANES CONSEILS – ELABE » et Bernard Sananes comme président. Elle ne nomme pas de groupe de médias.",
             U_ELABE, "Elabe"),
    ])
    add_steps("commission-des-sondages", [
        step("1977-07-19", "Loi sur certains sondages",
             "La loi n° 77-808 encadre la publication et la diffusion de certains sondages d'opinion. Le texte en ligne vise, à l'article 1er modifié en 2016, les sondages liés au débat électoral.",
             U_LOI, "Commission des sondages"),
        step("2016-04-25", "Notice et gratification",
             "La loi du 25 avril 2016, dans le texte publié par la Commission, fait figurer dans la notice, s'il y a lieu, la nature et la valeur de la gratification perçue par les personnes interrogées.",
             U_LOI, "Commission des sondages"),
    ])
    add_steps("vincent-bollore", [
        step("2025-12-31", "Part dans Havas après la scission",
             "Le site du groupe indique qu'au 31 décembre 2025, à la suite de la scission de Vivendi, le Groupe Bolloré détient 30,4 % du capital et des droits de vote de Havas, de Canal+ et de Louis Hachette Group. Les Echos écrivent le 23 février 2026 que la famille dépasse 50 % de Havas, holdings comprises.",
             U_BOL, "Groupe Bolloré"),
    ])
    add_steps("jdd", [
        step("2026-01-04", "Top 50 réalisé par CSA",
             "L'article dit le classement créé en 1988 avec l'Ifop, et réalisé cette année par CSA. Il donne les rangs de Jordan Bardella (4e), Marine Le Pen (7e), Marion Maréchal (30e), Philippe de Villiers (37e) et Nicolas Sarkozy (53e), et cite trois livres publiés chez Fayard.",
             U_JDD, "Le JDD"),
    ])

    own("lfpi", "ifop",
        "Le Figaro du 25 juillet 2022 rapporte la vente de l'Ifop au fonds LFPI. L'entretien du groupe, le 4 novembre 2022, parle d'un actionnaire majoritaire, l'équipe de direction étant aussi au capital. Le registre consulté le 11 novembre 2026 nomme ETUDINVEST comme président et ne publie pas les actionnaires",
        U_FIGARO, "2022-07-25")
    own("les-echos-le-parisien", "opinionway",
        "OpinionWay écrit être entré en 2022 dans le groupe Les Echos-Le Parisien (LVMH). 20 Minutes, le 24 juillet 2026, parle d'un rachat de 75 % et d'un projet de mise en vente non constaté comme signé",
        U_OW, "2022")
    own("lvmh", "les-echos-le-parisien",
        "20 Minutes le présente le 24 juillet 2026 comme une filiale de LVMH",
        U_M20, "2026-07-24")
    own("havas", "institut-csa",
        "CSA écrit le 13 février 2026 faire partie du groupe Havas depuis 2015",
        U_CSA, "2015")
    own("vincent-bollore", "havas",
        "le site du groupe indique qu'au 31 décembre 2025, après la scission de Vivendi, le Groupe Bolloré détient 30,4 % du capital et des droits de vote de Havas",
        U_BOL, "2025-12-31")
    own("vincent-bollore", "havas",
        "Les Echos écrivent le 23 février 2026 que la famille Bolloré détient plus de 50 % des actions de Havas, après les achats de la Compagnie de l'Étoile des Mers",
        U_ECHOS, "2026-02-23")
    own("toluna", "harris-interactive",
        "Toluna écrit le 28 septembre 2026 avoir acquis Harris Interactive en 2014. Le communiqué ne nomme pas de groupe de médias",
        U_TOL, "2014")
    cou("institut-csa", "jdd",
        "le JDD écrit le 4 janvier 2026 que son Top 50, créé en 1988 avec l'Ifop, a été réalisé cette année par l'institut CSA, auprès de 1 006 personnes du 17 au 22 décembre 2025",
        U_JDD, "2026-01-04", ["sondages", "medias"])
    cou("ifop", "jdd",
        "le JDD écrit le 4 janvier 2026 que ce Top 50 a été créé en 1988 avec l'Ifop, et qu'il est réalisé cette année par CSA",
        U_JDD, "2026-01-04", ["sondages", "medias"])

    spheres = {
        "lfpi": "argent", "lvmh": "argent", "les-echos-le-parisien": "argent", "havas": "argent",
        "ifop": "idees", "opinionway": "idees", "institut-csa": "idees",
        "harris-interactive": "idees", "toluna": "idees", "elabe": "idees",
        "commission-des-sondages": "institutions",
    }
    for i, s in spheres.items():
        if i in by:
            by[i]["sphere"] = s
