# -*- coding: utf-8 -*-
"""Rattrapage du 18 au 22 novembre 2026 (mise à jour du 22/11).
Le relevé automatique n'a rien publié du 18 au 22/11 (voir docs/JOURNAL.md).
Chaque phrase a été relue le 22/11/2026 sur la page citée, entre guillemets.
Les crochets [ ] et les points de suspension sont ceux des sources.
« taupe », « immonde », « marché de dupes », « honteux », « chiens furieux »,
« génocide » sont les mots des personnes citées, pas ceux d'Onrecord."""

G = "Gaza – déclarations"
F = "France – normalisation de l'extrême droite"
NU = "Nuance / contexte"

# Affaire du préfet Hugues Moutouh
U_FI_MLP = "https://www.franceinfo.fr/politique/front-national/je-n-ai-jamais-recu-d-informations-confidentielles-affirme-marine-le-pen-au-sujet-du-prefet-hugues-moutouh-soupconne-d-avoir-renseigne-le-rn_8294876.html"
U_FIG_TANGUY = "https://www.lefigaro.fr/actualite-france/soupcons-de-fuites-au-profit-du-rn-si-les-faits-concernant-le-prefet-moutouh-sont-averes-ils-sont-tres-graves-reagit-laurent-nunez-20261120"
U_FI_TANGUY = "https://www.franceinfo.fr/politique/front-national/des-rumeurs-et-des-accusations-sans-fondement-reagit-jean-philippe-tanguy-dans-l-affaire-du-prefet-soupconne-d-avoir-renseigne-le-rn-sur-des-affaires-en-cours_8291828.html"
U_FI_LIVE = "https://www.franceinfo.fr/societe/justice/direct-si-les-faits-sont-averes-ils-sont-evidemment-tres-graves-laurent-nunez-convoque-le-prefet-hugues-moutouh-soupconne-d-avoir-transmis-des-informations-sensibles-au-rassemblement-national_8291756.html"
U_CNEWS_NUNEZ = "https://www.cnews.fr/france/2026-11-20/si-les-faits-sont-averes-ils-sont-tres-graves-laurent-nunez-reagit-laffaire-des"
U_JDD_MOUTOUH = "https://www.lejdd.fr/politique/me-designer-comme-une-taupe-est-immonde-le-prefet-hugues-moutouh-se-defend-et-dit-sa-verite-au-jdd-189351"
U_FI_ROUSSEAU = "https://www.franceinfo.fr/france/centre-val-de-loire/loiret/prefet-soupconne-de-fuites-vers-le-rn-il-doit-etre-mis-a-pied-estime-la-depute-ecologiste-sandrine-rousseau_8293574.html"

# Loi sur la présomption d'usage légal des armes
U_BFM_ARMES = "https://www.bfmtv.com/politique/parlement/honteux-marchepied-a-marine-le-pen-la-gauche-denonce-l-adoption-de-la-loi-de-presomption-d-usage-legal-des-armes-par-les-forces-de-l-ordre_AD-202611210292.html"
U_BFM_DIAZ = "https://www.bfmtv.com/politique/video-loi-sur-la-presomption-d-usage-legal-des-armes-par-les-forces-de-l-ordre-adoptee-c-est-une-victoire-ideologique-pour-le-rassemblement-national-se-felicite-edwige-diaz-senatrice-rn_VN-202611210430.html"

# Primaire de la droite et Éric Zemmour
U_E1_ZEM = "https://www.europe1.fr/politique/jy-serai-si-elle-a-lieu-eric-zemmour-confirme-sa-volonte-de-participer-a-la-primaire-de-la-droite-et-du-centre-1241887"
U_CNEWS_LISNARD = "https://www.cnews.fr/france/2026-11-22/primaire-de-la-droite-et-du-centre-je-ne-demanderai-pas-gabriel-attal-de-me"
U_BFM_LISNARD = "https://www.bfmtv.com/replay-emissions/le-grand-oral-2027/video-je-veux-l-eliminer-de-la-competition-declare-david-lisnard-candidat-a-l-election-presidentielle-pour-justifier-d-ouvrir-a-eric-zemmour-une-primaire-de-la-droite-et-du-centre_VN-202611220360.html"
U_BFM_LARCHER = "https://www.bfmtv.com/politique/elections/presidentielle/presidentielle-gerard-larcher-ne-ressent-pas-de-proximite-avec-eric-zemmour-et-ne-souhaite-pas-l-inclure-dans-la-primaire-de-la-droite_AV-202611190987.html"
U_PS_RETAILLEAU = "https://www.publicsenat.fr/actualites/politique/primaire-en-incluant-eric-zemmour-david-lisnard-cherche-t-il-a-planter-le-processus-ou-a-en-faire-un-pre-premier-tour-de-la-presidentielle"
U_BFM_DARMANIN = "https://www.bfmtv.com/politique/elections/presidentielle/gerald-darmanin-estime-que-jean-luc-melenchon-gagnera-face-a-marine-le-pen-en-cas-de-duel-au-second-tour-de-l-election-presidentielle_AD-202611180359.html"
U_CNEWS_CHENU = "https://www.cnews.fr/france/2026-11-18/je-le-dis-aux-electeurs-de-david-lisnard-bruno-retailleau-et-edouard-philippe"
U_BFM_PHILIPPE = "https://www.bfmtv.com/politique/elections/presidentielle/guerre-en-ukraine-edouard-philippe-denonce-la-fascination-malsaine-de-jean-luc-melenchon-et-marine-le-pen-pour-vladimir-poutine_AD-202611180518.html"
U_BFM_RETAILLEAU_AIR = "https://www.bfmtv.com/politique/elections/presidentielle/video-un-appel-d-air-bruno-retailleau-s-oppose-a-la-regularisation-de-travailleurs-sans-papiers-dans-le-secteur-du-batiment_VN-202611190728.html"
U_E1_MENARD = "https://www.europe1.fr/politique/edouard-philippe-gabriel-attal-ils-veulent-vraiment-perdre-ironise-robert-menard-1240143"
U_BFM_VILLEPIN = "https://www.bfmtv.com/politique/front-national/video-je-ne-mets-pas-le-rn-et-lfi-sur-le-meme-plan-assure-dominique-de-villepin-declarant-que-le-rn-porte-un-heritage-de-xenophobie-de-racisme-et-d-antisemitisme_VN-202611200484.html"

# Antisémitisme : RN, LFI
U_FIG_LAVALETTE = "https://www.lefigaro.fr/elections/presidentielles/le-climat-n-etait-pas-le-meme-accusee-d-avoir-cautionne-des-ecrits-antisemites-laure-lavalette-invoque-des-faits-vieux-de-30-ans-20261119"
U_SO_LAVALETTE = "https://www.sudouest.fr/politique/marine-le-pen/laure-lavalette-je-ne-vais-pas-me-justifier-dit-la-deputee-du-rn-accusee-d-avoir-cautionne-des-ecrits-antisemites-durant-ses-etudes-a-bordeaux-31582634.php"
U_JDD_BARDELLA = "https://www.lejdd.fr/politique/vous-meme-vous-avez-ete-mis-en-cause-dans-une-affaire-de-harcelement-jordan-bardella-repond-a-patrick-cohen-sur-mediapart-189114"
U_CLOSER_BARDELLA = "https://www.closermag.fr/politique/jordan-bardella-accuse-dantisemitisme-il-patauge-dans-la-semoule-et-finit-par-sortir-de-ses-gonds-je-nai-pas-de-lecons-a-recevoir-3670179"
U_JDD_PERRET = "https://www.lejdd.fr/politique/on-lefface-de-nos-tablettes-pour-les-repas-jean-luc-melenchon-appelle-a-ne-plus-ecouter-pierre-perret-189138"
U_CNEWS_ONFRAY = "https://www.cnews.fr/videos/france/2026-11-21/que-va-t-faire-de-cet-antisemitisme-que-jean-luc-melenchon-libere-comme"
U_BFM_PNAT = "https://www.bfmtv.com/police-justice/terrorisme/islamisme-ultra-droite-radicale-violente-la-france-reste-sous-fortes-tensions-de-la-menace-terroriste-selon-le-procureur-antiterroriste_AD-202611220124.html"

MOUTOUH = ("Affaire des fuites présumées du ministère de l'Intérieur vers le RN : le préfet du Loiret Hugues Moutouh, "
           "secrétaire général du ministère de l'Intérieur d'avril 2025 à mai 2026, est soupçonné d'avoir renseigné le "
           "Rassemblement national sur des affaires en cours ; une enquête judiciaire est ouverte et le siège du RN a été "
           "perquisitionné. Il conteste et a demandé à être relevé de ses fonctions (JDD, 21 novembre 2026). ")
PRIMAIRE = ("Projet de primaire de la droite et du centre (équipes de Gabriel Attal, Bruno Retailleau et David Lisnard, "
            "novembre 2026) : la participation d'Éric Zemmour (Reconquête) est en débat. ")
LAVALETTE = ("Le média Les Jours a publié le 18 novembre 2026 une enquête sur une publication étudiante de Bordeaux, "
             "il y a une trentaine d'années ; Laure Lavalette est accusée d'avoir cautionné des écrits antisémites. "
             "Elle répond que le climat était « tout à fait différent » et qualifie Les Jours d'« officine d'extrême gauche » (Sud Ouest). ")
BARDELLA_MP = ("Mediapart a publié en septembre 2026 une enquête sur des messages privés à caractère antisémite qu'il lui "
               "attribue. Jordan Bardella dit ne pas avoir tenu ces propos et a porté plainte ; la justice doit se prononcer. ")


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

    def person(pid, name, role, desc, cat, sub, secs, statements, steps):
        if pid in by:
            add(pid, statements)
            return
        add_node(pid, name, "person", role, desc, [], cat, sub, secs)
        add(pid, statements)
        by[pid]["parcours"] = steps

    def add_link(src, tgt, rel, url, date, section, nature):
        for e in E:
            if e["source"] == src and e["target"] == tgt and e.get("url") == url:
                return
        link(src, tgt, rel, url, date)
        E[-1]["section"] = section
        E[-1]["nature"] = nature

    # --- Affaire Moutouh ---
    add("marine-le-pen", [
        ("Je ne sais absolument pas comment ce mail a pu se retrouver chez un de nos anciens prestataires. Mais en l'espèce, encore une fois, ce n'est pas passé par moi",
         "2026-11-22",
         MOUTOUH + "franceinfo, 22 novembre 2026 : la page écrit qu'un mail du service de Hugues Moutouh a été retrouvé par les enquêteurs chez Frédéric Chatillon, qu'elle présente comme une figure de l'extrême droite proche du RN et de sa dirigeante. Le même jour, sur France Inter, elle dit n'avoir jamais reçu ni demandé d'information confidentielle.",
         U_FI_MLP, F, "france"),
    ])
    add("julien-odoul", [
        ("J'observe qu'il faudrait que le secret de l'instruction soit préservé",
         "2026-11-20",
         MOUTOUH + "franceinfo, direct du 20 novembre 2026 : porte-parole du RN, invité de franceinfo. La page écrit qu'il a dénoncé « l'instrumentalisation de cette affaire, notamment par Jean-Luc Mélenchon ».",
         U_FI_LIVE, F, "france"),
    ])
    add("sandrine-rousseau", [
        ("C'était une proposition du Rassemblement national, qui a été mise à l'agenda politique par les LR, et qui maintenant a été soutenue par le ministre de l'Intérieur. C'est honteux!",
         "2026-11-21",
         "BFMTV, 21 novembre 2026 : au micro de franceinfo, à propos de la loi sur la présomption d'usage légal des armes par les forces de l'ordre, adoptée par le Parlement. La page cite aussi sa phrase « la Macronie a complètement dérivé sur ses valeurs ». Boris Vallaud (PS) annonce saisir le Conseil constitutionnel.",
         U_BFM_ARMES, F, "france"),
    ])

    person(
        "jean-philippe-tanguy", "Jean-Philippe Tanguy",
        "Député RN de la Somme (franceinfo, 20 novembre 2026)",
        "Député du Rassemblement national (Somme). Le 20 novembre 2026, il qualifie de « rumeurs » et d'« accusations sans fondement » les soupçons de fuites du ministère de l'Intérieur vers le RN. Pas de photo libre : monogramme.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("Ce sont des rumeurs et des accusations sans fondement en pleine campagne. Ça n'indigne personne parce que ça touche le RN. On prend les coups et on reste dignes",
             "2026-11-20",
             MOUTOUH + "Le Figaro, 20 novembre 2026 : la page écrit qu'il l'a dit sur France Inter et qu'il assure n'avoir « jamais vu » Hugues Moutouh « à une seule réunion programmatique ».",
             U_FIG_TANGUY, F, "france"),
            ("On n'a donc plus le droit d'être ami avec quelqu'un du Rassemblement national et de venir voir son ami au siège du Rassemblement national ?",
             "2026-11-20",
             MOUTOUH + "franceinfo, 20 novembre 2026 : à propos du magistrat présent au siège du RN lors de la perquisition. Il ajoute : « Les autorités elles-mêmes disent que ce monsieur, magistrat, était là et n'avait rien à faire avec la perquisition ».",
             U_FI_TANGUY, F, "france"),
        ],
        [step("2026-11-20", "Fuites présumées vers le RN",
              "Il qualifie les soupçons de « rumeurs » et d'« accusations sans fondement ».",
              U_FIG_TANGUY, "Le Figaro")],
    )
    person(
        "laurent-nunez", "Laurent Nuñez",
        "Ministre de l'Intérieur (BFMTV, 20 novembre 2026)",
        "Ministre de l'Intérieur. Le 20 novembre 2026, il convoque le préfet Hugues Moutouh, soupçonné d'avoir renseigné le RN, et dit que les faits seraient « très graves » s'ils étaient avérés. Pas de photo libre : monogramme.",
        "Responsables politiques", "Gouvernement & exécutif", ("france",),
        [
            ("Si ces faits sont avérés, c'est très grave, ça jettera le discrédit sur le ministère de l'Intérieur.",
             "2026-11-20",
             MOUTOUH + "franceinfo, direct du 20 novembre 2026 : la page écrit qu'il l'a dit sur BFMTV et qu'il devait rencontrer le préfet à 11 heures.",
             U_FI_LIVE, NU, "france"),
            ("J'ai besoin de l'entendre, d'écouter ce qu'il a à me dire. Ma main n'a jamais tremblé quand il y avait des décisions à prendre, croyez-le bien",
             "2026-11-20",
             MOUTOUH + "CNews, 20 novembre 2026.",
             U_CNEWS_NUNEZ, NU, "france"),
        ],
        [step("2026-11-20", "Convocation du préfet Moutouh",
              "Il convoque le préfet soupçonné d'avoir renseigné le RN.",
              U_FI_LIVE, "franceinfo")],
    )
    person(
        "hugues-moutouh", "Hugues Moutouh",
        "Préfet du Loiret, ancien secrétaire général du ministère de l'Intérieur (JDD, 21 novembre 2026)",
        "Préfet du Loiret, secrétaire général du ministère de l'Intérieur d'avril 2025 à mai 2026, conseiller au cabinet de Nicolas Sarkozy de 2011 à 2012 (JDD). En novembre 2026, il est soupçonné d'avoir renseigné le RN sur des affaires en cours ; une enquête judiciaire est ouverte. Il conteste, dit n'avoir « rien à se reprocher » et a demandé à être relevé de ses fonctions. Aucune mise en examen au 20 novembre 2026 selon le ministre (CNews). Pas de photo libre : monogramme.",
        "Organisations & institutions", "Institutions publiques", ("france",),
        [
            ("Me faire passer pour un nervi à la solde d'un parti est odieux, me désigner comme étant une taupe est immonde.",
             "2026-11-21",
             MOUTOUH + "JDD, 21 novembre 2026 : entretien téléphonique, « sa seule prise de parole » selon la page, quelques heures avant un communiqué à l'AFP où il demande à « être relevé de [s]es fonctions ». C'est sa réponse aux soupçons ; l'enquête est en cours.",
             U_JDD_MOUTOUH, NU, "france"),
        ],
        [step("2026-11-21", "Il conteste les soupçons",
              "Dans le JDD, il conteste les soupçons de fuites vers le RN et demande à être relevé de ses fonctions.",
              U_JDD_MOUTOUH, "JDD")],
    )

    # --- Loi sur les armes ---
    person(
        "edwige-diaz", "Edwige Diaz",
        "Sénatrice RN (BFMTV, 21 novembre 2026)",
        "Élue du Rassemblement national, présentée par BFMTV le 21 novembre 2026 comme sénatrice RN. Pas de photo libre : monogramme.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("C'est une victoire idéologique",
             "2026-11-21",
             "BFMTV, vidéo du 21 novembre 2026 : à propos de l'adoption par le Parlement de la loi sur la présomption d'usage légal des armes par les forces de l'ordre. La page écrit qu'elle s'en félicite « pour le Rassemblement national ». La gauche dénonce le même jour une loi « honteuse » (BFMTV).",
             U_BFM_DIAZ, F, "france"),
        ],
        [step("2026-11-21", "Loi sur l'usage des armes",
              "Elle salue une « victoire idéologique » pour le RN.",
              U_BFM_DIAZ, "BFMTV")],
    )

    # --- Primaire, Zemmour ---
    add("eric-zemmour", [
        ("Ma position est simple : j'ai été convié à cette primaire, j'ai accepté, donc j'y serai... si elle a lieu bien sûr",
         "2026-11-21",
         PRIMAIRE + "Europe 1, 21 novembre 2026, meeting de Toulon. Gérard Larcher, Édouard Philippe et Bruno Retailleau s'opposent à sa participation (BFMTV, Public Sénat).",
         U_E1_ZEM, F, "france"),
    ])
    person(
        "david-lisnard", "David Lisnard",
        "Maire de Cannes, candidat Nouvelle Énergie à la présidentielle 2027 (CNews, 22 novembre 2026)",
        "Maire de Cannes, candidat de Nouvelle Énergie à l'élection présidentielle de 2027. En novembre 2026, il plaide pour une primaire de la droite et du centre ouverte à Reconquête, ce que refusent les équipes de Gabriel Attal et d'Édouard Philippe. Pas de photo libre : monogramme.",
        "Responsables politiques", "Candidats à la présidentielle 2027", ("france",),
        [
            ("Je confirme que cette primaire devrait se tenir entre tous ceux qui se prétendent de la droite et du centre. Gabriel Attal dit qu'il est de droite, ce dont je doute, fort bien, qu'il participe. Reconquête devrait aussi pouvoir y concourir s'il en respecte les conditions d'accès",
             "2026-11-22",
             PRIMAIRE + "CNews, 22 novembre 2026, reprenant son entretien au JDD. Il ajoute : « Il faut un certain nombre de parrainages et une charte commune engageant chacun ». Édouard Philippe et Gabriel Attal sont opposés à la participation d'Éric Zemmour, selon la page.",
             U_CNEWS_LISNARD, F, "france"),
            ("Je veux l'éliminer de la compétition",
             "2026-11-22",
             PRIMAIRE + "BFMTV, Le Grand Oral 2027, 22 novembre 2026 : la page écrit qu'il le dit pour justifier d'ouvrir la primaire à Éric Zemmour.",
             U_BFM_LISNARD, F, "france"),
        ],
        [step("2026-11-22", "Primaire ouverte à Reconquête",
              "Il plaide pour une primaire de la droite et du centre ouverte à Reconquête.",
              U_CNEWS_LISNARD, "CNews")],
    )
    person(
        "gerard-larcher", "Gérard Larcher",
        "Président du Sénat (BFMTV, 19 novembre 2026)",
        "Président du Sénat. Le 19 novembre 2026, sur BFMTV, il dit qu'Éric Zemmour n'est « pas de la droite républicaine » et ne souhaite pas l'inclure dans la primaire de la droite et du centre. Pas de photo libre : monogramme.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("ne fait pas partie de ceux que je souhaite convier à débattre",
             "2026-11-19",
             PRIMAIRE + "BFMTV, 19 novembre 2026. Le sujet de la phrase est Éric Zemmour. La page écrit qu'il cite Gabriel Attal, Bruno Retailleau, Édouard Philippe et David Lisnard comme « le périmètre du centre et de la droite républicaine ».",
             U_BFM_LARCHER, F, "france"),
        ],
        [step("2026-11-19", "Primaire sans Éric Zemmour",
              "Il ne souhaite pas inclure Éric Zemmour dans la primaire de la droite et du centre.",
              U_BFM_LARCHER, "BFMTV")],
    )
    add("edouard-philippe", [
        ("Ça n'est pas mon camp politique",
         "2026-11-19",
         PRIMAIRE + "BFMTV, 19 novembre 2026 : la page écrit que le candidat d'Horizons s'est « fermement opposé » à participer à une telle primaire.",
         U_BFM_LARCHER, F, "france"),
        ("espèce de fascination malsaine",
         "2026-11-18",
         "BFMTV, 18 novembre 2026 : la page écrit qu'il prête à Jean-Luc Mélenchon et à Marine Le Pen une « espèce de fascination malsaine » pour Vladimir Poutine, ce qu'il juge « profondément » inquiétant « pour la sécurité de notre pays ».",
         U_BFM_PHILIPPE, F, "france"),
    ])
    add("bruno-retailleau", [
        ("Si on veut que la primaire se tienne, il faut être raisonnable. Si vous dites demain qu'Eric Zemmour doit faire partie de la primaire, en réalité, vous flinguez la primaire. Car ni les uns, ni les autres, ni participeront",
         "2026-11-18",
         PRIMAIRE + "Public Sénat, 19 novembre 2026, au micro de Public Sénat (« ni participeront » est l'orthographe de la page). Sur Sud Radio le même mercredi : « Si Eric Zemmour y participe, il n'y a pas de primaire, vous le savez bien ».",
         U_PS_RETAILLEAU, F, "france"),
        ("Un appel d'air",
         "2026-11-19",
         "BFMTV, vidéo du 19 novembre 2026 : la page écrit qu'il s'oppose ainsi à la régularisation de travailleurs sans papiers dans le secteur du bâtiment.",
         U_BFM_RETAILLEAU_AIR, F, "france"),
    ])
    add("gerald-darmanin", [
        ("Cette primaire, c'est un marché de dupes, et aujourd'hui, elle ne va pas désigner le prochain candidat à la présidence de la République",
         "2026-11-18",
         PRIMAIRE + "BFMTV, 18 novembre 2026 : la page écrit qu'il voit dans la primaire « l'antichambre de l'union des droites » et de l'extrême droite, et qu'il estime que Jean-Luc Mélenchon « gagnera » face à Marine Le Pen en cas de duel.",
         U_BFM_DARMANIN, F, "france"),
    ])
    add("sebastien-chenu", [
        ("Je le dis aux électeurs de David Lisnard, Bruno Retailleau et Edouard Philippe : tournez-vous vers nous",
         "2026-11-18",
         "CNews, La Grande Interview, 18 novembre 2026 : la page le présente comme député RN du Nord.",
         U_CNEWS_CHENU, F, "france"),
    ])
    add("robert-menard", [
        ("Ils veulent vraiment perdre ? Ils sont fous. Ils portent une responsabilité personnelle dans cette histoire.",
         "2026-11-19",
         PRIMAIRE + "Europe 1, La Grande Interview, 19 novembre 2026 : à propos d'Édouard Philippe et de Gabriel Attal, réticents à la primaire. La page le présente comme maire divers droite de Béziers.",
         U_E1_MENARD, F, "france"),
    ])
    add("dominique-de-villepin", [
        ("Je ne mets pas le RN et LFI sur le même plan",
         "2026-11-20",
         "BFMTV, vidéo du 20 novembre 2026, jour de sa déclaration de candidature : la page écrit qu'il déclare que le RN « porte un héritage de xénophobie, de racisme et d'antisémitisme ».",
         U_BFM_VILLEPIN, F, "france"),
    ])

    # --- Antisémitisme ---
    person(
        "laure-lavalette", "Laure Lavalette",
        "Députée RN du Var, porte-parole de la campagne présidentielle de Marine Le Pen (Sud Ouest, 19 novembre 2026)",
        "Députée du Rassemblement national (Var), porte-parole de la campagne présidentielle de Marine Le Pen. " + LAVALETTE + "Pas de photo libre : monogramme.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("Je ne vais pas me justifier de ce qu'il s'est passé il y a 30 ans dans un climat qui était tout à fait différent. Peut-être que je ne ferais pas la même chose maintenant",
             "2026-11-19",
             LAVALETTE + "Le Figaro, 19 novembre 2026. Selon Sud Ouest, elle s'exprimait sur BFMTV et a dit n'avoir « aucune leçon à recevoir sur l'antisémitisme ».",
             U_FIG_LAVALETTE, F, "france"),
            ("J'ai marché, moi, contrairement à d'autres, à la marche contre l'antisémitisme",
             "2026-11-19",
             LAVALETTE + "Sud Ouest, 19 novembre 2026 : la page précise « en novembre 2023 » et y voit une allusion apparente à Jean-Luc Mélenchon.",
             U_SO_LAVALETTE, F, "france"),
        ],
        [step("2026-11-19", "Enquête des Jours",
              "Accusée d'avoir cautionné des écrits antisémites il y a trente ans, elle invoque un climat « tout à fait différent ».",
              U_SO_LAVALETTE, "Sud Ouest")],
    )
    add("jordan-bardella", [
        ("Il y a un certain nombre de gens qui ont été mis en cause par Mediapart et qui ont nié les accusations. Vous-même vous avez été mis en cause.",
         "2026-11-18",
         BARDELLA_MP + "JDD, 18-19 novembre 2026 : « C à vous », France 5, 18 novembre, face à Patrick Cohen, qui lui demandait pourquoi il ne réactivait pas son compte Messenger. La page cite la réponse de Patrick Cohen : « Pas pour une affaire pénale ».",
         U_JDD_BARDELLA, F, "france"),
        ("Je n'ai pas de leçons à recevoir, encore une fois, en matière de lutte contre l'antisémitisme. Mon parcours en la matière a toujours été exemplaire.",
         "2026-11-18",
         BARDELLA_MP + "Closer, 18 novembre 2026, même émission. La page écrit qu'il a ajouté : « Je ne peux pas prouver une conversation que je n'ai pas tenue. »",
         U_CLOSER_BARDELLA, F, "france"),
    ])
    add("jean-luc-melenchon", [
        ("Franchement, Pierre Perret dans le rôle où le place sa chanson contre les prétendus \"antisémites\" que nous serions, cela me fait de la peine",
         "2026-11-17",
         "Message publié sur X après la sortie de la chanson « Les Antisémites » de Pierre Perret, qui vise La France insoumise ; cité par le JDD le 19 novembre 2026. franceinfo date sa réaction du mardi 17 novembre 2026. Les guillemets intérieurs sont ceux de la page.",
         U_JDD_PERRET, G, "gaza"),
        ("Il sait très bien que \"antisémite\" désigne les adversaires du génocide à Gaza.",
         "2026-11-17",
         "Message publié sur X après la chanson « Les Antisémites » de Pierre Perret, cité par le JDD le 19 novembre 2026. « génocide » est le mot de l'auteur du message.",
         U_JDD_PERRET, G, "gaza"),
    ])
    add("michel-onfray", [
        ("Que va-t-on faire de cet antisémitisme que Jean-Luc Mélenchon libère comme des chiens furieux ?",
         "2026-11-21",
         "CNews, vidéo du 21 novembre 2026. C'est son jugement sur Jean-Luc Mélenchon. La réponse de Jean-Luc Mélenchon à la chanson « Les Antisémites » de Pierre Perret (17 novembre 2026) est sur sa fiche.",
         U_CNEWS_ONFRAY, F, "france"),
    ])
    add("pnat", [
        ("la première s'inscrit dans des projets de violences contre les personnes, la seconde dans des actions contre des biens et des infrastructures",
         "2026-11-22",
         "BFMTV, 22 novembre 2026 : le procureur national antiterroriste Olivier Christen distingue ainsi l'ultra-droite radicale violente (la première) de l'ultra-gauche radicale violente (la seconde). La France reste sous « fortes tensions » de la menace terroriste, selon la page.",
         U_BFM_PNAT, NU, "france"),
    ])

    add_link("laurent-nunez", "rn",
             "le 20/11/2026, il convoque le préfet Hugues Moutouh, soupçonné d'avoir renseigné le RN, et dit que les faits seraient « très graves » s'ils étaient avérés",
             U_FI_LIVE, "2026-11-20", "france", "autre")
    add_link("david-lisnard", "eric-zemmour",
             "le 22/11/2026, il plaide pour que Reconquête puisse concourir à la primaire de la droite et du centre, et dit vouloir « l'éliminer de la compétition »",
             U_BFM_LISNARD, "2026-11-22", "france", "autre")
    add_link("gerard-larcher", "eric-zemmour",
             "le 19/11/2026, il dit qu'Éric Zemmour n'est « pas de la droite républicaine » et ne souhaite pas l'inclure dans la primaire",
             U_BFM_LARCHER, "2026-11-19", "france", "opposition")
    add_link("laure-lavalette", "marine-le-pen",
             "porte-parole de sa campagne présidentielle (Sud Ouest, 19/11/2026)",
             U_SO_LAVALETTE, "2026-11-19", "france", "ascension")
