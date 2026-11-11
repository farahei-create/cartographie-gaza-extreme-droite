# -*- coding: utf-8 -*-
"""v31 : Louise Montangon, UNI Bordeaux, liens publics.
Pages ouvertes le 11 novembre 2026. Les guillemets reprennent la page.
Le lycéen de 17 ans cité par la presse n'est pas nommé.
Le portrait du JDD ne dit pas qu'elle y est recrutée : Midi Libre et Public
l'écrivent le lendemain, le JDD écrit la veille au matin qu'elle ne rejette
pas l'offre de Cyril Hanouna. Les deux versions restent sur la fiche.
Aucune photo libre : monogramme."""

F = "France – normalisation de l'extrême droite"
NU = "Nuance / contexte"
G = "Gaza – déclarations"
POL = "Responsables politiques"
ORG = "Organisations & institutions"

U_20 = "https://www.20minutes.fr/societe/4252906-20261009-militante-rn-uni-bordelaise-louise-montangon-etudiante-echarpe-mobilisation-lyceenne"
U_SO = "https://www.sudouest.fr/gironde/bordeaux/decryptage-qui-est-la-bordelaise-louise-montangon-etoile-montante-du-rn-sur-les-plateaux-tele-de-la-colere-lyceenne-30996470.php"
U_LP = "https://www.leparisien.fr/societe/jai-honte-dappartenir-a-cette-generation-qui-est-louise-montangon-letudiante-candidate-rn-aux-municipales-qui-fustige-les-blocus-lyceens-08-10-2026-LORHOXBKGRGIRB7AKPWHQ2LWEA.php"
U_LP2 = "https://www.leparisien.fr/culture-loisirs/tv/moi-je-nasperge-pas-mes-professeurs-dessence-le-face-a-face-entre-elwan-et-louise-vire-au-reglement-de-comptes-sur-lci-09-10-2026-LPGLK6QOYZDYFHMI2QNUZGFEHM.php"
U_JDD = "https://www.lejdd.fr/Societe/mobilisation-lyceenne-louise-montangon-visage-de-la-resistance-aux-blocages-185745"
U_SENAT = "https://www.senat.fr/compte-rendu-commissions/20260413/ce_universites.html"
U_VA = "https://www.valeursactuelles.com/societe/a-15-ans-jetais-tres-a-gauche-louise-montangon-raconte-son-basculement-a-droite-et-son-combat-contre-les-blocages"
U_ML = "https://www.midilibre.fr/2026/10/12/elle-a-refuse-loffre-de-cyril-hanouna-pour-rejoindre-un-media-du-groupe-bollore-louise-montangon-est-le-nouveau-phenomene-mediatique-de-la-droite-13597210.php"
U_PUB = "https://www.public.fr/louise-montangon-refuse-rejoindre-cyril-hanouna-autre-media-seduite"

NEW_URLS = [U_20, U_SO, U_LP, U_LP2, U_JDD, U_SENAT, U_VA, U_ML, U_PUB]


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

    def cou(s, t, rel, url, date, stories=None):
        link(s, t, rel, url, date)
        E[-1]["nature"] = "coulisses"
        E[-1]["section"] = "france"
        if stories:
            E[-1]["stories"] = list(stories)

    add_node(
        "uni", "UNI (Union nationale interuniversitaire)", "org", "Syndicat étudiant",
        "20 Minutes le présente le 9 octobre 2026 comme un syndicat classé à droite, et en indique le slogan : Mérite, liberté et excellence. Sud Ouest, le même jour, le qualifie de « très droitier » et écrit que Louise Montangon en est la responsable à Bordeaux depuis septembre 2025. Le compte rendu du Sénat du 15 avril 2026 la nomme représentante de l'UNI, aux côtés du délégué national.",
        [st(
            "Face aux blocages et aux saccages de lycées encouragés par LFI, l'UNI exige le rétablissement de l'ordre et demande des sanctions financières à l'encontre des casseurs",
            "2026-10-09",
            "Pétition du syndicat, citée par 20 Minutes le 9 octobre 2026. L'article ne date pas la pétition elle-même. La phrase est celle du syndicat, pas une citation isolée de Louise Montangon.",
            U_20, F)],
        ORG, "Associations & représentants")

    desc = (
        "20 Minutes, Sud Ouest, Le Parisien et le JDD lui donnent 22 ans. Sud Ouest la dit originaire de Charente-Maritime. "
        "Valeurs actuelles, le 22 octobre 2026, écrit qu'elle arrive à l'université Bordeaux-Montaigne en septembre 2022, inscrite en philosophie, et que son engagement à l'UNI commence en octobre 2024. "
        "Sud Ouest écrit le 9 octobre 2026 qu'elle a suivi une licence de philosophie et un master 1 de science politique, qu'elle est responsable de l'UNI à Bordeaux depuis septembre 2025, qu'elle travaille à temps partiel pour la communication nationale de l'UNI, et qu'elle suit cette année un master de philosophie à distance rattaché à l'université de Reims. "
        "Le même jour, 20 Minutes écrit qu'elle est présentée comme étudiante en philosophie à Bordeaux-Montaigne, alors que l'université, sollicitée, précise qu'elle n'y est plus étudiante depuis 2025. "
        "Le JDD du 11 octobre la présente encore comme étudiante en master de philosophie à Bordeaux-Montaigne, et écrit aussi qu'elle poursuit un M1 à distance. "
        "20 Minutes écrit qu'elle assume des idées d'extrême droite. Le journal et Valeurs actuelles la disent 5e sur la liste du Rassemblement national aux municipales de Bordeaux. Le Parisien date cette candidature de mars 2026. Valeurs actuelles écrit qu'elle prend sa carte au RN en septembre 2026. Marie France écrit que la liste n'a pas obtenu d'élu (https://www.mariefrance.fr/actualite/societe/louise-montangon-qui-est-cette-etudiante-bordelaise-adherente-du-rn-qui-enchaine-les-plateaux-tele-1306002.html). "
        "Le 15 avril 2026, le Sénat la nomme représentante de l'UNI dans une audition. "
        "Le JDD publie son portrait le 11 octobre 2026 et écrit qu'elle ne rejette pas une offre de Cyril Hanouna. Midi Libre et Public, le 12 octobre, écrivent qu'elle n'a pas donné suite et qu'elle a mis en avant le Journal du dimanche. Le portrait du JDD ne dit pas qu'elle y est recrutée."
    )
    add_node(
        "louise-montangon", "Louise Montangon", "person",
        "Responsable de l'UNI à Bordeaux depuis septembre 2025 ; 5e sur la liste RN aux municipales de Bordeaux (mars 2026)",
        desc, [], POL, "Militants", ("france", "gaza"))

    add("louise-montangon", [
        ("Le calendrier de Parcoursup nous paraît problématique. Il exerce une pression continue sur les candidats et transforme la fin de l'année scolaire en une période d'incertitude. Le système des listes d'attente, qui peut se prolonger jusqu'à la fin de l'été, empêche les familles comme les étudiants de s'organiser sereinement sur le plan matériel et logistique.",
         "2026-04-15",
         "Compte rendu de la commission d'enquête du Sénat sur les universités, audition du 15 avril 2026. Elle y parle comme représentante de l'UNI. La suite, dans le même propos, décrit des inégalités pour les étudiants qui reçoivent une réponse tardive, et conclut : « La fluidité du calendrier n'est donc pas seulement une question administrative, elle constitue, selon nous, une condition d'équité sociale. »",
         U_SENAT, F, "france"),
        ("Il nous semble assez grossier de toujours demander plus de moyens quand on passe son temps à saccager l'université en la bloquant.",
         "2026-04-15",
         "Même audition. Phrase qui suit son constat, toujours comme représentante de l'UNI : beaucoup d'étudiants, dit-elle, commencent une licence dans le public, à Bordeaux par exemple, puis partent dans le privé, « dégoûtés des conditions de travail ».",
         U_SENAT, F, "france"),
        ("J\u2019ai honte d\u2019appartenir à cette génération",
         "2026-10-08",
         "Le Parisien, 8 octobre 2026. L'article ne nomme pas l'émission où la phrase a été dite. Il la présente comme étudiante en master de philosophie à Bordeaux-Montaigne. Le 9 octobre, 20 Minutes écrit que l'université précise qu'elle n'y est plus étudiante depuis 2025. Le 22 octobre, dans VA+, elle précise : « J\u2019ai pas honte de cette génération. J\u2019ai honte de cette partie de la jeunesse ».",
         U_LP, F, "france"),
        ("J\u2019ai pas honte de cette génération. J\u2019ai honte de cette partie de la jeunesse",
         "2026-10-22",
         "Entretien VA+, publié le 22 octobre 2026. Le journal écrit qu'elle revient sur la phrase « J\u2019ai honte d\u2019appartenir à cette génération », rapportée par Le Parisien le 8 octobre.",
         U_VA, NU, "france"),
        ("Ça ne sert à rien de me regarder avec un petit sourire, votre bilan est désastreux !",
         "2026-10-06",
         "LCI, face à Gabriel Attal. Le Parisien du 8 octobre 2026 date l'échange de « ce mardi ». 20 Minutes du 9 octobre publie la même phrase. Sud Ouest, le 9 octobre, la date aussi du mardi 6 octobre et la coupe en deux : « ça sert à rien de me regarder avec un petit sourire » et « bilan désastreux ». Le JDD du 11 octobre cite « Votre bilan est désastreux. »",
         U_LP, F, "france"),
        ("Vous êtes le visage du laxisme. […] Nous avons des milliers de lycéens qui n\u2019ont aucun cadre, aucune hiérarchie, qui ne respectent rien.",
         "2026-10-06",
         "Même échange sur LCI, cité par Le Parisien le 8 octobre 2026. Le journal coupe par (…). Il écrit qu'elle reproche à Gabriel Attal d'avoir « abandonné » l'Éducation nationale.",
         U_LP, F, "france"),
        ("Vous êtes les idiots utiles de ce mouvement. […] Vous êtes utilisés, vous êtes instrumentalisés.",
         "2026-10-07",
         "LCI, « La Grande Confrontation », David Pujadas. Le Parisien du 9 octobre 2026 écrit « mercredi 6 octobre », ce qui ne tombe pas un mercredi. Sud Ouest date ce débat du 7 octobre. Le JDD le place au lendemain du 6 octobre. 20 Minutes reproduit un message du compte « 24h Pujadas » daté du 7 octobre : « Vous êtes les idiots utiles de ce mouvement, personne ne parle plus de vos revendications, tout le monde parle du chaos que vous êtes en train de mettre partout ». Le Parisien coupe par (…). L'interlocuteur est un lycéen de 17 ans : il n'est pas nommé ici.",
         U_LP2, F, "france"),
        ("Bloquer des établissements c\u2019est i-llé-gal, vous êtes dans l\u2019illégalité la plus totale",
         "2026-10-07",
         "Même émission, citée par Le Parisien le 9 octobre 2026. Même réserve sur la date écrite « mercredi 6 octobre ». L'interlocuteur n'est pas nommé ici.",
         U_LP2, F, "france"),
        ("C\u2019est ça, une grosse semaine ? Ça vous fera très mal quand vous reviendrez les pieds sur terre.",
         "2026-10-06",
         "JDD, 11 octobre 2026, à propos de l'émission LCI du 6 octobre : elle commente l'emploi du temps d'un lycéen, qui n'est pas nommé ici. Sud Ouest, le 9 octobre, transcrit autrement la fin de la séquence : « Vous avez le désir de faire des études supérieures : ça va vous faire très mal. »",
         U_JDD, F, "france"),
        ("J\u2019ai préféré prendre du recul et ne rien risquer d\u2019inutile.",
         "2026-10-11",
         "Portrait du JDD, 11 octobre 2026. Elle refuse d'appeler abandon le fait d'avoir cessé de fréquenter le campus pendant son master, après avoir été prise à partie. Le 9 octobre, 20 Minutes écrit que, sur RMC, elle a dit avoir arrêté les cours en présentiel l'année précédente parce qu'elle ne se sentait plus en sécurité, et que l'université Bordeaux-Montaigne précise qu'elle n'y est plus étudiante depuis 2025. Sud Ouest écrit le même jour qu'elle suit un master de philosophie à distance rattaché à Reims.",
         U_JDD, NU, "france"),
        ("Il a un public plutôt jeune, celui auquel je m\u2019adresse, et il fait passer un message important : il existe aussi une jeunesse de droite, et elle ne se taira pas.",
         "2026-10-11",
         "Portrait du JDD, 11 octobre 2026, au sujet de Cyril Hanouna, que le journal dit « fan » et prêt à l'engager « tout de suite ». Elle serait « sincèrement touchée ». Le JDD écrit qu'elle ne rejette pas la proposition. Midi Libre (12 octobre) cite, pour le 8 octobre : « Si elle veut, je l\u2019engage tout de suite. » Midi Libre et Public (https://www.public.fr/louise-montangon-refuse-rejoindre-cyril-hanouna-autre-media-seduite), le 12 octobre, écrivent qu'elle n'a pas donné suite. Midi Libre ajoute que Hanouna a annoncé sa présence le 12 octobre dans TBT9 : l'article constate l'annonce, pas le passage.",
         U_JDD, F, "france"),
        ("J'étais très déçue par l'alliance entre LR et les macronistes.",
         "2026-10-09",
         "Sud Ouest, 9 octobre 2026. Elle explique ainsi son adhésion au RN, après avoir figuré sur la liste de Julie Rechagneux aux municipales de Bordeaux. Valeurs actuelles, le 22 octobre, date la carte de septembre 2026.",
         U_SO, F, "france"),
        ("Je dois tout à l'extrême gauche : ils ont réveillé en moi cette conscience politique.",
         "2026-10-09",
         "Sud Ouest, 9 octobre 2026. Le journal écrit qu'elle a « plusieurs fois » tenu cette phrase sur les plateaux de CNews. L'article ne donne pas une date d'émission unique.",
         U_SO, F, "france"),
        ("Je comprends pas comment, à 18 ou à 20 ans, on peut crier à la gloire du Hamas",
         "2026-10-22",
         "Entretien VA+, 22 octobre 2026. Elle parle d'une manifestation d'octobre 2024 sur son campus, au sujet du conflit israélo-palestinien. Le journal rapporte son récit : elle affirme avoir filmé des militants se félicitant des attaques du 7 octobre 2023, et que certains enseignants auraient applaudi. Ce récit n'est pas recoupé ici.",
         U_VA, G, "gaza"),
    ])

    add("cyril-hanouna", [
        ("Si elle veut, je l\u2019engage tout de suite.",
         "2026-10-08",
         "Midi Libre, 12 octobre 2026, qui date la phrase du 8 octobre et écrit que Louise Montangon a fait un autre choix. Le JDD du 11 octobre écrit qu'il se dit « fan », prêt à l'engager « tout de suite », et qu'elle ne rejette pas l'offre. Public, le 12 octobre, écrit aussi qu'elle n'a pas donné suite. Midi Libre ajoute qu'il a annoncé sa présence le 12 octobre dans TBT9.",
         U_ML, F, "france"),
    ])

    etudes = step(
        "2022-09", "Université Bordeaux-Montaigne",
        "Valeurs actuelles écrit le 22 octobre 2026 qu'elle arrive en septembre 2022, inscrite en philosophie. Sud Ouest, le 9 octobre 2026, écrit qu'elle a suivi une licence de philosophie et un master 1 de science politique, sans en donner l'année. Le même article écrit qu'elle suit cette année un master de philosophie à distance rattaché à l'université de Reims. 20 Minutes, le 9 octobre, écrit que l'université Bordeaux-Montaigne précise qu'elle n'y est plus étudiante depuis 2025. Le JDD du 11 octobre la présente encore comme étudiante en master à Bordeaux-Montaigne, et écrit qu'elle poursuit un M1 à distance.",
        U_VA, "Valeurs actuelles")
    etudes["kind"] = "formation"
    add_steps("louise-montangon", [
        etudes,
        step("2024-10", "Adhésion à l'UNI",
             "Le JDD date d'octobre 2024 son entrée à l'UNI, après une manifestation sur le parvis de sa faculté dont elle juge, selon le journal, qu'elle fait l'apologie du terrorisme. Valeurs actuelles confirme le mois et rapporte son récit sur cette manifestation. Ce récit n'est pas tenu pour établi au-delà de ce qu'elle en dit.",
             U_JDD, "Le JDD"),
        step("2025-09", "Responsable de l'UNI à Bordeaux",
             "Sud Ouest écrit le 9 octobre 2026 qu'elle est responsable de l'UNI à Bordeaux depuis septembre 2025, et qu'elle travaille à temps partiel pour la communication nationale du syndicat.",
             U_SO, "Sud Ouest"),
        step("2025-12", "Plateau de CNews",
             "Le JDD écrit que, depuis décembre 2025, elle est venue sur CNews parler de l'université. Midi Libre écrit qu'elle a commencé dans l'émission « 100 % Politique » de Gauthier Le Bret, sur CNews. Public date la première télévision de décembre 2025, chez Gauthier Le Bret.",
             U_JDD, "Le JDD"),
        step("2026-03", "Liste RN aux municipales de Bordeaux",
             "Valeurs actuelles écrit qu'en mars 2026 elle est 5e sur la liste de Julie Rechagneux. 20 Minutes indique la 5e place, sans le mois. Le Parisien du 8 octobre 2026 écrit « candidate RN aux municipales en mars 2026 ». Marie France écrit que la liste « Rassemblement national pour Bordeaux » n'a pas obtenu d'élu.",
             U_VA, "Valeurs actuelles"),
        step("2026-04", "Audition au Sénat",
             "Le 15 avril 2026, le compte rendu de la commission d'enquête sur les universités la nomme représentante de l'UNI. Elle prête serment avec les autres personnes auditionnées ce jour-là.",
             U_SENAT, "Sénat"),
        step("2026-09", "Carte du Rassemblement national",
             "Valeurs actuelles écrit qu'elle prend sa carte en septembre 2026, après la liste municipale. Sud Ouest, le 9 octobre, constate l'adhésion et cite son explication : la déception devant l'alliance entre LR et les macronistes.",
             U_VA, "Valeurs actuelles"),
    ])

    cou("louise-montangon", "uni",
        "responsable de l'UNI à Bordeaux depuis septembre 2025",
        U_SO, "2025-09")
    cou("louise-montangon", "uni",
        "représentante de l'UNI auditionnée le 15 avril 2026 par la commission d'enquête du Sénat",
        U_SENAT, "2026-04-15")
    cou("louise-montangon", "rn",
        "5e sur la liste de Julie Rechagneux aux municipales de Bordeaux en mars 2026",
        U_VA, "2026-03")
    cou("louise-montangon", "rn",
        "prend sa carte en septembre 2026, selon Valeurs actuelles",
        U_VA, "2026-09")
    cou("cyril-hanouna", "louise-montangon",
        "a déclaré le 8 octobre 2026, selon Midi Libre : « Si elle veut, je l\u2019engage tout de suite ». Le JDD du 11 octobre écrit qu'elle ne rejette pas l'offre. Midi Libre et Public, le 12 octobre, écrivent qu'elle n'y a pas donné suite",
        U_ML, "2026-10-08", ["medias"])
    cou("jdd", "louise-montangon",
        "a publié son portrait le 11 octobre 2026 ; Midi Libre écrit le 12 octobre qu'elle a annoncé un engagement auprès du journal, ce que le portrait ne dit pas",
        U_JDD, "2026-10-11", ["medias"])
    cou("louise-montangon", "gabriel-attal",
        "échange sur LCI le 6 octobre 2026 : « Ça ne sert à rien de me regarder avec un petit sourire, votre bilan est désastreux ! »",
        U_LP, "2026-10-06", ["medias"])

    by["louise-montangon"]["sphere"] = "partis"
    by["uni"]["sphere"] = "partis"
    if "gabriel-attal" in by and not by["gabriel-attal"].get("sphere"):
        by["gabriel-attal"]["sphere"] = "partis"
