# -*- coding: utf-8 -*-
"""v26 : citations pour les fiches qui n'en avaient aucune, ou une seule.
Chaque phrase a été lue dans la page indiquée (HTTP 200) le 10 novembre 2026.
Les crochets et les points de suspension entre parenthèses sont ceux de la source.
Les démentis et le contexte lus dans la même page sont dans le champ « medium »."""

G = "Gaza – déclarations"
F = "France – normalisation de l'extrême droite"
NU = "Nuance / contexte"

U_PRAUD_FI = "https://www.franceinfo.fr/culture/tv/punaises-de-lit-indignation-apres-une-sequence-d-un-racisme-evident-sur-cnews-un-depute-lfi-annonce-saisir-l-arcom_6091530.html"
U_PRAUD_FIG = "https://www.lefigaro.fr/medias/l-arcom-saisie-apres-une-question-de-pascal-praud-liant-punaises-de-lit-et-immigration-20230929"
U_LEJ = "https://www.lefigaro.fr/medias/amende-de-50-000-euros-pour-cnews-a-cause-de-propos-sur-l-immigration-arabo-musulmane-20240523"
U_STERIN_FIG = "https://www.lefigaro.fr/vox/politique/pierre-edouard-sterin-face-aux-injonctions-des-deconstructeurs-ne-plus-courber-l-echine-20240717"
U_STERIN_CROIX = "https://www.la-croix.com/france/pericles-le-plan-du-milliardaire-pierre-edouard-sterin-pour-unir-et-faire-gagner-les-droites-20240722"
U_OLIVIER = "https://www.franceinfo.fr/politique/marine-le-pen/immigration-le-referendum-annonce-par-marine-le-pen-serait-un-arbitrage-de-l-ensemble-du-peuple-d-apres-son-conseiller-special_4786617.html"
U_KNAFO_PORTE = "https://www.cnews.fr/france/2025-02-10/immigration-il-faut-fermer-la-porte-insiste-la-deputee-europeenne-reconquete"
U_KNAFO_METEO = "https://www.cnews.fr/france/2024-12-09/sarah-knafo-limmigration-nest-pas-un-phenomene-meteorologique-1600173"
U_TEGNER = "https://www.europe1.fr/societe/six-millions-detrangers-recenses-en-france-erik-tegner-preconise-une-immigration-negative-775658"
U_NEDJAR = "https://www.ozap.com/actu/cnews-une-chaine-d-extreme-droite-serge-nedjar-pointe-un-manque-de-mesure-et-de-responsabilite-de-la-part-de-delphine-ernotte/651856"
U_DENIS = "https://www.valeursactuelles.com/clubvaleurs/politique/tugdual-denis-limmigration-un-noeud-gordien"
U_AN = "https://www.assemblee-nationale.fr/dyn/17/comptes-rendus/ceelec/l17ceelec2425036_compte-rendu.pdf"


def apply(N, by):
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

    add("pascal-praud", [
        ("Est-ce qu'on sait pourquoi il y a plus de punaises de lit aujourd'hui ? Est-ce lié à l'hygiène ?",
         "2023-09-29",
         "CNews, « L'Heure des pros » (29 septembre 2023), cité par franceinfo. Il s'adresse à Nicolas Roux de Bézieux (Badbugs.fr). L'invité répond « Absolument pas ». Plusieurs élus annoncent saisir l'Arcom ; l'article ne rapporte pas de décision de l'Arcom.",
         U_PRAUD_FI, F, "france"),
        ("Je vais poser toutes les questions. Il y a beaucoup d'immigration en ce moment. Est-ce que c'est des personnes qui n'ont pas les mêmes conditions d'hygiène que ceux qui sont sur le sol de France qui apportent, parce qu'ils sont dans la rue, peut-être n'ont-ils pas accès à tous les services comme les autres, est-ce que c'est lié à cela ?",
         "2023-09-29",
         "Même séquence de « L'Heure des pros », citée par franceinfo, qui signale un [sic]. L'invité répond « Absolument pas » et avait indiqué sur franceinfo que la première cause d'infestation, ce sont les voyages.",
         U_PRAUD_FI, F, "france"),
        ("L'Association nationale d'assistance aux frontières pour les étrangers (...) s'est retirée de la zone d'attente de Roissy infestée par les punaises de lit. Une situation qui, selon elle, ne cesse de se dégrader",
         "2023-09-29",
         "Fin de la même émission, cité par Le Figaro : Pascal Praud justifie sa question. Les points de suspension entre parenthèses sont ceux de l'article. Le Figaro rapporte aussi la réponse « Absolument pas » de l'invité.",
         U_PRAUD_FIG, F, "france"),
    ])

    add("geoffroy-lejeune", [
        ("C'est une des conséquences, ce sondage, une des conséquences de l'immigration arabo-musulmane. C'est une des conséquences, comme une partie du trafic de drogue, comme la surpopulation carcérale, comme l'abaya, comme tout ça",
         "2023-09-28",
         "CNews, « L'Heure des pros 2 » du 28 septembre 2023, cité par Le Figaro avec AFP (23 mai 2024). L'Arcom a infligé 50 000 euros à CNews pour ces propos : elle estime qu'ils imputent des faits graves à un groupe de population et qu'ils n'ont fait l'objet d'aucune réaction sur le plateau.",
         U_LEJ, F, "france"),
        ("En fait, l'antisémitisme dont sont victimes les juifs aujourd'hui, c'est juste qu'on n'a pas eu une politique d'immigration qui avait juste le début du commencement d'une cohérence",
         "2023-09-28",
         "Même séquence, même article du Figaro. Geoffroy Lejeune est présenté comme directeur du Journal du dimanche et chroniqueur régulier de l'émission.",
         U_LEJ, F, "france"),
    ])

    add("pierre-edouard-sterin", [
        ("Minoritaire dans les urnes, la gauche est sans doute plus minoritaire que jamais dans les esprits. Il n'y a qu'à consulter les enquêtes d'opinion sur l'immigration, la sécurité, la fiscalité ou les dépenses publiques pour se rendre compte combien les aspirations des Français sont éloignées des vieilles rengaines que seule la gauche française, plus urbaine et moins populaire que jamais, ose encore porter.",
         "2024-07-17",
         "Tribune signée au Figaro (page datée du 17 juillet 2024). La suite de l'article est réservée aux abonnés : seule la partie lisible sans compte est citée.",
         U_STERIN_FIG, F, "france"),
        ("La gauche française est minoritaire, mais elle est habile, doublement habile même\u00a0: elle est habile quand elle se partage les circonscriptions alors que les partis qui la composent ne sont d'accord sur rien, et habile encore quand, à grand renfort d'une communication tonitruante, elle fait croire au pays qu'elle a gagné les élections alors que 75 % des Français n'ont pas voté pour elle .",
         "2024-07-17",
         "Suite de la même tribune, partie lisible sans abonnement.",
         U_STERIN_FIG, F, "france"),
        ("Je ne peux plus me résoudre à voir cette gauche mélenchonisée mener cette bataille culturelle sans rencontrer une résistance des forces de droite, qui, depuis cinquante ans, courbent l’échine sous les injonctions culturelles des déconstructeurs.",
         "2024-07-18",
         "La Croix (22 juillet 2024, avec AFP) présente cette phrase, entre guillemets, comme celle par laquelle il a annoncé Périclès « dans les pages du Figaro du 18 juillet ». Le Figaro en ligne date sa page du 17 juillet ; la phrase complète n'y est pas lisible sans abonnement.",
         U_STERIN_CROIX, F, "france"),
    ])

    add("philippe-olivier", [
        ("Est-ce que oui ou non vous approuvez le projet de loi ci-joint",
         "2021-09-28",
         "franceinfo, « Votre invité politique » (article du 28 septembre 2021). Il explique la question que poserait le référendum sur l'immigration annoncé la veille par Marine Le Pen sur France 2.",
         U_OLIVIER, F, "france"),
        ("un projet de loi qui comprend un dispositif complet de lutte contre l'immigration, de régulation de l'immigration",
         "2021-09-28",
         "Même entretien. L'article écrit : « Le texte sera selon lui » cette formule.",
         U_OLIVIER, F, "france"),
        ("un arbitrage de l'ensemble du peuple",
         "2021-09-28",
         "Même entretien. Il ajoute que les mesures seraient « à prendre ou à laisser ».",
         U_OLIVIER, F, "france"),
        ("à prendre ou à laisser",
         "2021-09-28",
         "Même entretien, à propos des mesures du projet de loi soumis à référendum.",
         U_OLIVIER, F, "france"),
    ])

    add("sarah-knafo", [
        ("L’immigration n’est pas un phénomène météorologique",
         "2024-12-09",
         "CNews, article du site (9 décembre 2024). L'article, très court, ne retranscrit pas le reste de l'entretien. Il la présente comme eurodéputée Reconquête.",
         U_KNAFO_METEO, F, "france"),
        ("Il faut fermer la porte",
         "2025-02-10",
         "CNews, « La Grande Interview » (lundi 10 février 2025), article du site. L'article dit qu'elle réagit aux flux migratoires et à l'assimilation, sans citer d'autre phrase.",
         U_KNAFO_PORTE, F, "france"),
    ])

    add("erik-tegner", [
        ("L'immigration, c'est l'éléphant au milieu de la pièce",
         "2025-10-08",
         "Europe 1, « Christine Kelly et vous » (article du 8 octobre 2025). Il commente une étude de l'Insee publiée la veille : six millions d'étrangers en France, soit 8,8 % de la population. L'article écrit qu'il juge cette étude inaperçue des autres médias.",
         U_TEGNER, F, "france"),
        ("immigration négative",
         "2025-10-08",
         "Même article d'Europe 1. Le terme est entre guillemets. L'article, et non une phrase continue de l'intéressé, écrit qu'il préconise de mettre en place cette politique, « consistant à ne pas renouveler le titre de séjour d'un certain nombre d'étrangers ».",
         U_TEGNER, F, "france"),
    ])

    add("serge-nedjar", [
        ("CNews est une chaîne d’opinions, avec un \"s\", comme nous l’avons toujours revendiqué, et avant tout une chaîne d’information. Bien évidemment, nous ne sommes pas une chaîne d’extrême droite !",
         "2025-09-30",
         "Entretien au Figaro publié le 30 septembre 2025, cité par Puremédias (article du 4 octobre 2025). Il répond à Delphine Ernotte, qui avait dit au Monde : « Qu’ils assument d’être une chaîne d’extrême droite ! »",
         U_NEDJAR, NU, "france"),
        ("Cette phrase a fait beaucoup de mal en interne. Je peux vous dire que l’émotion était très vive dans les couloirs. Nos 200 collaborateurs ont pris cette attaque de plein fouet.",
         "2025-09-30",
         "Même entretien, même article de Puremédias.",
         U_NEDJAR, NU, "france"),
    ])

    add("tugdual-denis", [
        ("L’immigration, comme une évidence. Car l’immigration partout et tout le temps. L’immigration derrière les lynchages, l’immigration dans le poids sur nos comptes publics, l’immigration derrière les incivilités du canal Saint-Martin .",
         "2026-07-02",
         "Éditorial signé dans Valeurs actuelles (2 juillet 2026), « L'immigration, un nœud gordien ». Le texte qui suit est le sien : le site ne reprend pas le lien de causalité comme un fait établi.",
         U_DENIS, F, "france"),
        ("Ce sujet, qui fait consensus dans la société française (une majorité écrasante de nos concitoyens souhaite réduire drastiquement les flux), continue à faire l’objet de pudeurs dans le débat public.",
         "2026-07-02",
         "Suite du même éditorial. La parenthèse est dans le texte.",
         U_DENIS, F, "france"),
    ])

    add("arnaud-rerolle", [
        ("Le document publié par L’Humanité en juillet 2024 date de septembre 2023.",
         "2025-05-06",
         "Audition sous serment, commission d'enquête de l'Assemblée nationale sur l'organisation des élections (compte rendu n° 36). Il parle du document révélé par L'Humanité.",
         U_AN, NU, "france"),
        ("J’assume ce document, dont je suis l’auteur, mais certains des éléments qui y sont présentés ne sont plus d’actualité.",
         "2025-05-06",
         "Même audition. Cette phrase précise la portée du document de septembre 2023.",
         U_AN, NU, "france"),
        ("notre activité consiste aujourd’hui à produire et à soutenir des idées, ce que nous assumons complètement, dans le respect du cadre légal.",
         "2025-05-06",
         "Même audition, après avoir rappelé l'article L. 52-8 du code électoral. Il venait de dire que Périclès ne finance pas de candidats, ni directement ni indirectement.",
         U_AN, NU, "france"),
        ("C’est donc dans un souci de rééquilibrage démocratique, lié à notre attachement au pluralisme, que nous avons jugé opportun de lancer une organisation agissant dans le champ métapolitique pour promouvoir ces valeurs.",
         "2025-05-06",
         "Même audition, propos liminaire. « Ces valeurs » renvoie, dans le compte rendu, aux « valeurs libérales et conservatrices » qu'il dit défendre.",
         U_AN, F, "france"),
    ])
