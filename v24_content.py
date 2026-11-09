# -*- coding: utf-8 -*-
"""v24 : parcours manquants, acteurs publics de coulisses, liens datés.
Chaque URL a été ouverte (HTTP 200) et les formules utilisées y figurent.
Aucune intention n'est ajoutée. Les démentis lus dans la source sont repris."""

POL = "Responsables politiques"
MED = "Médias & propriétaires"
JOU = "Journalistes & éditorialistes"
ORG = "Organisations & institutions"

# Sources vérifiées le 9 novembre 2026
U_KNAFO = "https://www.franceinfo.fr/politique/eric-zemmour/presidentielle-2022-conseillers-financiers-soutiens-qui-sont-les-membres-de-la-galaxie-zemmour_4865823.html"
U_KNAFO_CE = "https://www.franceinfo.fr/replay-magazine/france-2/complement-d-enquete/complement-d-enquete-sarah-knafo-zemmour-gloire-et-plan-b_8219074.html"
U_PRAUD = "https://www.franceinfo.fr/choix/tres-doue-un-peu-coq-conservateur-mais-pas-raciste-qui-est-pascal-praud-lanimateur-polemique-de-cnews_2459328.html"
U_PRAUD_E1 = "https://www.europe1.fr/emissions/lheure-des-pros"
U_LEJ = "https://www.franceinfo.fr/economie/medias/geoffroy-lejeune-ex-responsable-de-valeurs-actuelles-nomme-directeur-de-la-redaction-du-journal-du-dimanche-malgre-l-opposition-des-salaries_5907104.html"
U_LEJ_LAG = "https://www.lagardere.com/communique-presse/jerome-begle-devient-directeur-general-de-la-redaction-de-paris-match-geoffroy-lejeune-est-nomme-directeur-de-la-redaction-du-jdd/"
U_LEJ_AOUT = "https://www.franceinfo.fr/economie/medias/greve-du-journal-du-dimanche-geoffroy-lejeune-prendra-ses-fonctions-a-la-tete-de-la-redaction-de-l-hebdomadaire-a-partir-du-1er-aout-annonce-le-groupe-lagardere_5969546.html"
U_LEJ_PS = "https://www.publicsenat.fr/actualites/societe/larrivee-de-geoffroy-lejeune-au-jdd-relance-le-debat-au-senat-sur-lindependance-des-medias"
U_BOELL = "https://www.franceinfo.fr/culture/livres/hachette-livre-nomme-lise-boell-editrice-d-eric-zemmour-a-la-tete-des-editions-fayard_6586515.html"
U_PRISMA = "https://www.france24.com/fr/info-en-continu/20250910-le-patron-de-cnews-%C3%A9galement-nomm%C3%A9-directeur-des-r%C3%A9dactions-de-prisma-media"
U_UDR = "https://www.franceinfo.fr/politique/eric-ciotti-va-lancer-son-propre-parti-union-des-droites-pour-la-republique_6755497.html"
U_OLIVIER = "https://www.franceinfo.fr/elections/presidentielle/presidentielle-2022-communicants-strateges-ministres-potentiels-qui-entoure-marine-le-pen-durant-sa-campagne_5087401.html"
U_PFEFFER = "https://www.franceinfo.fr/politique/front-national/affaire-des-assistants-fn-au-parlement-europeen/presidentielle-2027-comment-les-condamnations-du-rn-l-empechent-de-preparer-le-financement-de-la-future-campagne_7337280.html"
U_E1 = "https://www.lagardere.com/communique-presse/nomination-de-donat-vidal-revel-en-tant-que-directeur-general-deurope-1/"
U_TEGNER = "https://www.franceinfo.fr/societe/justice/des-attaques-intolerables-des-magistrats-pris-pour-cible-apres-la-condamnation-du-patron-du-media-identitaire-frontieres_8071571.html"
U_VA = "https://www.valeursactuelles.com/societe/chers-lecteurs-chers-amis-le-message-du-nouveau-directeur-de-la-redaction"
U_VA_BFM = "https://www.bfmtv.com/replay-emissions/face-a-duhamel/face-a-duhamel-tugdual-denis-a-quoi-joue-edouard-philippe-11-09_EN-202409110738.html"
U_NUITS = "https://france3-regions.franceinfo.fr/bourgogne-franche-comte/cote-d-or/dijon/la-nuit-du-bien-commun-a-dijon-quelle-est-la-polemique-autour-de-cet-evenement-3259420.html"
U_NUITS_FAQ = "https://www.lanuitdubiencommun.com/faq"
U_ILIADE = "https://institut-iliade.com/presentation/"
U_ILIADE_F = "https://institut-iliade.com/halte-a-la-diffamation-et-a-la-desinformation/"
U_STERIN = "https://www.franceinfo.fr/politique/comment-le-milliardaire-conservateur-pierre-edouard-sterin-veut-gagner-la-bataille-des-idees_7086594.html"
U_AN = "https://www.assemblee-nationale.fr/dyn/17/comptes-rendus/ceelec/l17ceelec2425036_compte-rendu.pdf"
U_CIOTTI27 = "https://www.franceinfo.fr/politique/il-n-y-a-qu-une-voie-eric-ciotti-propose-a-marine-le-pen-un-pacte-d-alliance-pour-la-presidentielle-de-2027_8178815.html"
U_PERICLES = "https://www.franceinfo.fr/politique/front-national/plan-pericles-ce-que-l-on-sait-du-projet-du-milliardaire-catholique-pierre-edouard-sterin-pour-promouvoir-des-valeurs-conservatrices-et-faire-gagner-la-droite-aux-elections_6677268.html"
U_BOLLORE = "https://www.franceinfo.fr/economie/medias/canal-i-tele-paris-match-avant-le-jdd-la-mainmise-de-vincent-bollore-sur-d-autres-medias-a-braque-de-nombreuses-redactions_5910392.html"
U_MARECHAL = "https://www.franceinfo.fr/politique/marion-marechal-lance-son-propre-mouvement-politique-et-propose-une-coalition-a-marine-le-pen_6824000.html"
U_TF1_MAT = "https://www.tf1info.fr/politique/elections/legislatives/dissolution-video-marine-le-pen-sur-tf1-jordan-bardella-sera-premier-ministre-en-cas-de-majorite-rn-aux-legislatives-2303374.html"
U_ISSEP = "https://www.franceinfo.fr/politique/front-national/video-marion-marechal-le-pen-les-petits-secrets-de-son-ecole-de-sciences-politiques_2766371.html"
U_HAN = "https://www.franceinfo.fr/culture/tv/cyril-hanouna/l-animateur-cyril-hanouna-annonce-rejoindre-le-groupe-m6-en-septembre_7100610.html"
U_E1_HAN = "https://www.franceinfo.fr/elections/legislatives/legislatives-2024-l-arcom-met-en-demeure-europe-1-pour-manque-de-mesure-et-d-honnetete-dans-l-emission-de-cyril-hanouna_6629991.html"
U_GLU = "https://www.lefigaro.fr/politique/guerre-hamas-israel-raphael-glucksmann-refuse-le-terme-de-genocide-et-prefere-celui-de-carnage-20240312"
U_DARM = "https://www.franceinfo.fr/politique/jean-castex/gouvernement-de-jean-castex/le-groupe-d-extreme-droite-generation-identitaire-dissous-en-conseil-des-ministres-annonce-gerald-darmanin_4318225.html"
U_RETI = "https://www.franceinfo.fr/politique/gouvernement-de-michel-barnier/gouvernement-barnier-bruno-retailleau-figure-de-la-droite-conservatrice-a-l-interieur_6795379.html"
U_ATT = "https://www.franceinfo.fr/politique/remaniement/remaniement-gabriel-attal-est-nomme-premier-ministre-en-remplacement-d-elisabeth-borne_6292461.html"
U_PHI = "https://www.franceinfo.fr/elections/pourquoi-emmanuel-macron-a-choisi-edouard-philippe-pour-le-poste-de-premier-ministre_2192137.html"
U_MLP = "https://www.franceinfo.fr/politique/marine-le-pen-officiellement-proclamee-presidente-du-fn-recueille-67-65-des-voix-contre-32-35-pour-son-rival_231301.html"

NU = "Nuance / contexte"


def apply(N, E, by, step, node, link, st):
    def add_node(*a, **k):
        node(*a, **k)
        by[a[0]] = N[-1]
        return N[-1]

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

    def C(s, t, rel, url, date, stories):
        link(s, t, rel, url, date)
        E[-1]["nature"] = "coulisses"
        E[-1]["section"] = "france"
        E[-1]["stories"] = list(stories)

    def tag(a, b, stories):
        for e in E:
            if {e["source"], e["target"]} == {a, b}:
                got = e.setdefault("stories", [])
                for s in stories:
                    if s not in got:
                        got.append(s)

    # ----- fiches nouvelles : personnes publiques nommées par la source -----
    add_node("sarah-knafo", "Sarah Knafo", "person",
             "Eurodéputée (Reconquête) ; directrice de campagne présidentielle en 2022",
             "franceinfo (4 décembre 2021) la présente comme magistrate à la Cour des comptes, plume, conseillère spéciale, directrice de campagne et de la communication d'Éric Zemmour, et écrit qu'elle partage sa vie. Le 21 octobre 2026, la présentation d'un Complément d'enquête sur franceinfo la dit « élue Reconquête au Parlement européen » deux ans après cette campagne. Cette fiche ne décrit pas d'autre fonction.",
             [], POL, "Partis & dirigeants de parti")
    add_node("pascal-praud", "Pascal Praud", "person",
             "Présentateur de « L'Heure des pros » (CNews ; page d'émission Europe 1)",
             "Un portrait de franceinfo du 13 novembre 2017 le présente comme animateur de « L'Heure des Pros » sur CNews, chaîne du groupe Bolloré. La page de l'émission sur europe1.fr, lue le 9 novembre 2026, indique que « L'Heure des Pros » y est « présentée par Pascal Praud ». La page ne donne pas la date de début de cette diffusion.",
             [], JOU, "Journalistes & chroniqueurs")
    add_node("francois-durvye", "François Durvye", "person",
             "Directeur général d'Otium Capital ; nommé dans le document « Périclès » de 2023",
             "franceinfo, dans son article du 20 juillet 2024 sur le document révélé par L'Humanité, écrit que le projet est présenté comme fondé et administré par Pierre-Édouard Stérin et deux proches : François Durvye, directeur général du fonds Otium Capital, et Alban du Rostu, directeur général du Fonds du bien commun. Le 6 mai 2025, Arnaud Rérolle, directeur général de Périclès, déclare sous serment que ce document date de septembre 2023 et que certains éléments ne sont plus d'actualité. Cette fiche ne dit pas que François Durvye exerce encore cette fonction.",
             [], MED, "Propriétaires, financeurs & groupes")
    add_node("alban-du-rostu", "Alban du Rostu", "person",
             "Directeur général du Fonds du bien commun ; nommé dans le document « Périclès » de 2023",
             "Même article de franceinfo (20 juillet 2024) : le document le présente, avec Pierre-Édouard Stérin et François Durvye, comme fondateur et administrateur du projet. Nuance du 6 mai 2025 : Arnaud Rérolle dit sous serment que certains éléments du document de septembre 2023 ne sont plus d'actualité. Cette fiche ne dit pas qu'Alban du Rostu exerce encore cette fonction.",
             [], MED, "Propriétaires, financeurs & groupes")
    add_node("arnaud-rerolle", "Arnaud Rérolle", "person",
             "Directeur général de Périclès (audition du 6 mai 2025)",
             "Il se présente ainsi devant la commission d'enquête de l'Assemblée nationale le 6 mai 2025, sous serment. Il dit être l'auteur du document publié par L'Humanité, daté de septembre 2023, et que certains éléments « ne sont plus d'actualité ». franceinfo le désigne aussi comme directeur général de Périclès dans un article du 21 février 2025.",
             [st("Périclès ne finance pas de candidats, ni directement ni indirectement.",
                 "2025-05-06",
                 "Audition sous serment devant la commission d'enquête de l'Assemblée nationale sur l'organisation des élections (compte rendu n° 36). Il précise viser l'article L. 52-8 du code électoral. Le président de la commission, Thomas Cazenave, lui avait demandé de confirmer qu'il ne finançait pas directement des candidats.",
                 U_AN, NU)],
             ORG, "Projets & réseaux")
    add_node("lise-boell", "Lise Boëll", "person",
             "Présidente-directrice générale des éditions Fayard (nommée le 5 juin 2024)",
             "franceinfo (5 juin 2024) : Hachette Livre, propriété du groupe Vivendi, annonce sa nomination à la tête de Fayard. Le même article la présente comme l'éditrice d'Éric Zemmour et rappelle le licenciement, en avril 2024, d'Isabelle Saporta, pour « différends stratégiques ». Il cite aussi Vincent Bolloré, en mars, devant des députés : « Je n'ai aucun projet idéologique, je suis tout doux et débonnaire ».",
             [], JOU, "Directions de rédaction")
    add_node("serge-nedjar", "Serge Nedjar", "person",
             "Directeur des rédactions de Prisma Media (nommé le 10 septembre 2025) ; patron de CNews, selon France 24",
             "France 24 avec AFP (10 septembre 2025) : Arnaud Lagardère, président de Prisma Media, annonce dans un message aux salariés que Serge Nedjar est nommé directeur des rédactions. Il conserve ses fonctions à CNews. Il est placé sous l'autorité de Gérald-Brice Viret, vice-président de Prisma et directeur général de Canal+ France. L'article écrit que Vivendi a racheté Prisma Media en 2021.",
             [], JOU, "Directions de rédaction")
    add_node("gerald-brice-viret", "Gérald-Brice Viret", "person",
             "Directeur général de Canal+ France ; vice-président de Prisma Media, selon France 24",
             "France 24 avec AFP (10 septembre 2025) le désigne comme le supérieur hiérarchique de Serge Nedjar à Prisma Media, et comme directeur général de Canal+ France, « auquel appartient CNews ». L'article ne dit pas qu'il a nommé Serge Nedjar : l'annonce citée est signée d'Arnaud Lagardère.",
             [], JOU, "Directions de rédaction")
    add_node("philippe-olivier", "Philippe Olivier", "person",
             "Conseiller de Marine Le Pen ; directeur de la cellule « Idées et images » du RN, selon franceinfo (2022)",
             "franceinfo (18 avril 2022) le présente comme « le plus proche conseiller de Marine Le Pen » et comme directeur de la cellule « Idées et images » du parti. Le même article écrit qu'il est l'époux de Marie-Caroline Le Pen et le père de Nolwenn Olivier, « l'actuelle compagne de Jordan Bardella ». Ces liens familiaux sont ceux que l'article énonce.",
             [], POL, "Partis & dirigeants de parti")
    add_node("kevin-pfeffer", "Kévin Pfeffer", "person",
             "Trésorier du Rassemblement national, selon franceinfo (25 juin 2025)",
             "Dans un article du 25 juin 2025 sur le financement de la campagne de 2027, franceinfo le désigne deux fois comme « le trésorier » du parti et lui attribue l'indication selon laquelle des dossiers seraient envoyés à une cinquantaine de banques. L'article ne date pas le début de cette fonction. Le communiqué du congrès de 2021 sur le site du RN n'a pas répondu (redirection) : il n'est pas utilisé.",
             [], POL, "Partis & dirigeants de parti")
    add_node("tugdual-denis", "Tugdual Denis", "person",
             "Directeur de la rédaction de Valeurs actuelles",
             "Le 21 juin 2023, Valeurs actuelles publie un texte signé de lui, dont le titre parle du « message du nouveau directeur de la rédaction ». Le 11 septembre 2024, BFMTV le présente encore comme « directeur de la rédaction de Valeurs actuelles ». Le nom du propriétaire n'est pas repris ici : la page lue ne le désigne pas dans le corps accessible hors commentaires.",
             [], JOU, "Directions de rédaction")
    add_node("erik-tegner", "Erik Tegnér", "person",
             "Directeur et fondateur du média Frontières ; éditorialiste sur CNews, selon franceinfo",
             "franceinfo (20 juin 2026) le désigne comme « directeur de Frontières », « fondateur du média » et « éditorialiste sur CNews », dans un article sur sa condamnation du jeudi précédent : six mois de prison avec sursis et 10 000 euros d'amende pour divulgation de données personnelles d'avocats. Aucune participation au capital n'est affirmée ici.",
             [], JOU, "Journalistes & chroniqueurs")
    add_node("philippe-conrad", "Philippe Conrad", "person",
             "Président d'honneur de l'Institut Iliade ; l'institut le nomme parmi ses fondateurs",
             "La page « Présentation » de l'institut le cite comme « Président d'honneur » et indique « Né en 2014 ». Une page de l'institut au ton de droit de réponse écrit : « L'Institut Iliade a été fondé il y a plus de dix ans par Jean-Yves Le Gallou, Philippe Conrad et Bernard Lugan. » La même page dément toute participation d'Henry de Lesquen. Jean-Yves Le Gallou et Bernard Lugan n'ont pas de fiche dans cette version.",
             [], ORG, "Projets & réseaux")
    add_node("donat-vidal-revel", "Donat Vidal-Revel", "person",
             "Directeur général d'Europe 1 (nommé le 20 octobre 2022)",
             "Communiqué de Lagardère du 20 octobre 2022 : Arnaud Lagardère et Constance Benqué, présidente de Lagardère News, le nomment directeur général d'Europe 1, en charge de la rédaction, des programmes et de l'antenne. Il conserve la direction de l'information. Ce communiqué ne dit pas s'il occupe encore le poste en 2026.",
             [], JOU, "Directions de rédaction")
    add_node("arnaud-lagardere", "Arnaud Lagardère", "person",
             "Président-directeur général du groupe Lagardère ; président de Prisma Media, selon France 24 (2025)",
             "Le communiqué du groupe du 23 juin 2023 dit que Geoffroy Lejeune « est nommé ce jour directeur de la rédaction du JDD par Arnaud Lagardère ». Le communiqué du 20 octobre 2022 le nomme parmi les deux signataires de la nomination du directeur général d'Europe 1. France 24 (10 septembre 2025) le dit auteur du message nommant Serge Nedjar à Prisma Media, et président de Prisma Media.",
             [], MED, "Propriétaires, financeurs & groupes")
    add_node("constance-benque", "Constance Benqué", "person",
             "Présidente de Lagardère News (au 20 octobre 2022)",
             "Le communiqué de Lagardère du 20 octobre 2022 la nomme, avec Arnaud Lagardère, comme auteur de la nomination de Donat Vidal-Revel à la direction générale d'Europe 1. Il la présente comme présidente de Lagardère News. Le communiqué ne dit pas si elle occupe encore cette fonction en 2026.",
             [], JOU, "Directions de rédaction")

    add_node("prisma-media", "Prisma Media", "org", "Groupe de magazines",
             "France 24 avec AFP (10 septembre 2025) écrit que Vivendi a racheté Prisma Media en 2021, et que le 10 septembre 2025 Serge Nedjar y est nommé directeur des rédactions par un message d'Arnaud Lagardère, sous l'autorité de Gérald-Brice Viret.",
             [], MED, "Chaînes, radios & titres")
    add_node("nuits-du-bien-commun", "La Nuit du bien commun", "org", "Fonds et soirées de levée de dons",
             "France 3 Bourgogne (2 décembre 2025) écrit que le fonds a été fondé en 2017 et que ses fondateurs sont Stanislas de Lochner, Thibault Farrenq et Pierre-Édouard Stérin. Le même article écrit qu'ils ont quitté le conseil d'administration en juin 2025. La foire aux questions du site de l'organisation dit que Stérin et Thibault Farrenq n'exercent plus de responsabilité exécutive, et que le conseil a pris acte le 3 juin 2025 de la sortie du collège des fondateurs. Stanislas de Lochner et Thibault Farrenq n'ont pas de fiche dans cette version.",
             [], ORG, "Projets & réseaux")
    add_node("institut-iliade", "Institut Iliade", "org", "Institut de formation et de réflexion",
             "Sa page « Présentation » indique « Né en 2014 » et cite Philippe Conrad comme président d'honneur. Une page de l'institut nomme comme fondateurs Jean-Yves Le Gallou, Philippe Conrad et Bernard Lugan, et écrit qu'Henry de Lesquen n'y a jamais participé. Cette fiche suit ces deux textes de l'institut, pas une autre version.",
             [], ORG, "Projets & réseaux")
    add_node("frontieres", "Frontières", "org", "Média",
             "franceinfo (20 juin 2026) parle du « média identitaire Frontières » et d'Erik Tegnér comme de son directeur et de son fondateur. L'article porte sur une condamnation pénale, pas sur l'actionnariat.",
             [], MED, "Chaînes, radios & titres")
    add_node("udr", "Union des droites pour la République (UDR)", "org", "Parti politique",
             "franceinfo (31 août 2024) : Éric Ciotti annonce créer ce parti pour « rassembler toutes les droites ». L'article précise qu'il est alors encore, officiellement, président des Républicains. Le 5 septembre 2026, franceinfo le présente comme le président de l'UDR, « allié du RN », et rapporte qu'il a proposé à Marine Le Pen un « pacte d'alliance » pour 2027. L'article relate une proposition, pas un accord signé.",
             [], POL, "Partis & dirigeants de parti")

    # nuance sur la fiche Périclès déjà publiée : on ajoute, on ne réécrit pas les citations
    per = by["pericles"]
    note = " Le 6 mai 2025, Arnaud Rérolle, qui se présente comme directeur général, déclare sous serment à l'Assemblée nationale qu'il est l'auteur du document, que celui-ci date de septembre 2023, que certains éléments « ne sont plus d'actualité », et que « Périclès ne finance pas de candidats, ni directement ni indirectement »."
    if note.strip()[:40] not in per["description"]:
        per["description"] += note

    # ----- liens de coulisses (nature fixée, non reclassée) -----
    C("sarah-knafo", "eric-zemmour",
      "franceinfo la présente comme directrice de campagne et de la communication, et écrit qu'elle partage sa vie",
      U_KNAFO, "2021-12-04", ["nominations"])
    C("pascal-praud", "cnews",
      "présentateur de « L'Heure des Pros », selon un portrait de franceinfo",
      U_PRAUD, "2017-11-13", ["medias"])
    C("pascal-praud", "europe1",
      "la page de l'émission sur europe1.fr indique qu'elle est « présentée par Pascal Praud » (lecture du 9 novembre 2026 ; la page ne date pas le début)",
      U_PRAUD_E1, "2026", ["medias"])
    C("francois-durvye", "pericles",
      "le document de 2023, selon franceinfo, le nomme parmi les fondateurs et administrateurs, avec Pierre-Édouard Stérin et Alban du Rostu. Arnaud Rérolle dira le 6 mai 2025 que certains éléments de ce document ne sont plus d'actualité",
      U_PERICLES, "2024-07-20", ["argent"])
    C("alban-du-rostu", "pericles",
      "le document de 2023, selon franceinfo, le nomme parmi les fondateurs et administrateurs. Même nuance : audition du 6 mai 2025",
      U_PERICLES, "2024-07-20", ["argent"])
    C("arnaud-rerolle", "pericles",
      "se présente comme directeur général, sous serment, et dit être l'auteur du document de septembre 2023",
      U_AN, "2025-05-06", ["argent"])
    C("lise-boell", "fayard",
      "nommée présidente-directrice générale par Hachette Livre, que franceinfo présente comme la propriété du groupe Vivendi",
      U_BOELL, "2024-06-05", ["nominations"])
    C("lise-boell", "eric-zemmour",
      "franceinfo la présente comme son éditrice",
      U_BOELL, "2024-06-05", ["nominations"])
    C("serge-nedjar", "prisma-media",
      "nommé directeur des rédactions par un message d'Arnaud Lagardère, selon France 24/AFP",
      U_PRISMA, "2025-09-10", ["nominations", "medias"])
    C("serge-nedjar", "cnews",
      "France 24/AFP le désigne comme le patron de CNews, fonction qu'il conserve lors de la nomination chez Prisma",
      U_PRISMA, "2025-09-10", ["medias"])
    C("gerald-brice-viret", "prisma-media",
      "vice-président, présenté par France 24/AFP comme l'autorité hiérarchique de Serge Nedjar. L'annonce de la nomination est attribuée à Arnaud Lagardère, pas à lui",
      U_PRISMA, "2025-09-10", ["medias"])
    C("gerald-brice-viret", "cnews",
      "directeur général de Canal+ France, « auquel appartient CNews », selon France 24/AFP",
      U_PRISMA, "2025-09-10", ["medias"])
    C("vivendi-canal", "prisma-media",
      "France 24/AFP écrit que Vivendi a racheté Prisma Media en 2021",
      U_PRISMA, "2021", ["argent", "medias"])
    C("arnaud-lagardere", "geoffroy-lejeune",
      "le communiqué du groupe dit qu'il le nomme directeur de la rédaction du JDD. Public Sénat rapportera le 1er août 2023 cette phrase d'Arnaud Lagardère au Figaro : « Ni Vincent Bolloré, ni quiconque de Vivendi, n'a été impliqué dans cette décision. »",
      U_LEJ_LAG, "2023-06-23", ["nominations", "medias"])
    C("arnaud-lagardere", "serge-nedjar",
      "France 24/AFP attribue à un message d'Arnaud Lagardère l'annonce de sa nomination à la tête des rédactions de Prisma Media",
      U_PRISMA, "2025-09-10", ["nominations"])
    C("arnaud-lagardere", "donat-vidal-revel",
      "le nomme directeur général d'Europe 1, avec Constance Benqué, selon le communiqué du groupe",
      U_E1, "2022-10-20", ["nominations", "medias"])
    C("constance-benque", "donat-vidal-revel",
      "le nomme directeur général d'Europe 1, avec Arnaud Lagardère, selon le communiqué du groupe",
      U_E1, "2022-10-20", ["nominations", "medias"])
    C("philippe-olivier", "marine-le-pen",
      "franceinfo le présente comme son plus proche conseiller et comme directeur de la cellule « Idées et images » du parti",
      U_OLIVIER, "2022-04-18", ["nominations"])
    C("philippe-olivier", "rn",
      "directeur de la cellule « Idées et images », selon franceinfo",
      U_OLIVIER, "2022-04-18", ["nominations"])
    C("kevin-pfeffer", "rn",
      "franceinfo le désigne comme le trésorier du parti",
      U_PFEFFER, "2025-06-25", ["argent"])
    C("tugdual-denis", "valeurs-actuelles",
      "un texte du 21 juin 2023 est publié sous un titre qui le présente comme le nouveau directeur de la rédaction ; BFMTV le désigne encore ainsi le 11 septembre 2024",
      U_VA, "2023-06-21", ["medias", "nominations"])
    C("erik-tegner", "frontieres",
      "franceinfo le désigne comme fondateur et directeur du média",
      U_TEGNER, "2026-06-20", ["medias"])
    C("erik-tegner", "cnews",
      "franceinfo le désigne comme éditorialiste sur CNews",
      U_TEGNER, "2026-06-20", ["medias"])
    C("philippe-conrad", "institut-iliade",
      "la page Présentation le cite comme président d'honneur ; une page de l'institut le nomme parmi les fondateurs, avec Jean-Yves Le Gallou et Bernard Lugan, et dément toute participation d'Henry de Lesquen",
      U_ILIADE, "2014", ["nominations"])
    C("pierre-edouard-sterin", "nuits-du-bien-commun",
      "France 3 le présente comme cofondateur en 2017, avec Stanislas de Lochner et Thibault Farrenq, et écrit qu'ils ont quitté le conseil d'administration en juin 2025",
      U_NUITS, "2017", ["argent"])
    C("eric-ciotti", "udr",
      "franceinfo rapporte qu'il annonce créer ce parti. L'article précise qu'il est alors encore officiellement président des Républicains",
      U_UDR, "2024-08-31", ["nominations"])
    C("eric-ciotti", "marine-le-pen",
      "franceinfo rapporte qu'il dit lui avoir proposé un « pacte d'alliance » pour la présidentielle de 2027. L'article relate une proposition, pas un accord signé",
      U_CIOTTI27, "2026-09-05", ["nominations"])

    for a, b, stories in (
        ("vincent-bollore", "vivendi-canal", ["argent", "medias"]),
        ("vivendi-canal", "cnews", ["medias"]),
        ("vivendi-canal", "lagardere", ["argent", "medias"]),
        ("lagardere", "europe1", ["medias"]),
        ("lagardere", "jdd", ["medias"]),
        ("vivendi-canal", "c8", ["medias"]),
        ("fayard", "vivendi-canal", ["medias"]),
        ("vincent-bollore", "fayard", ["medias"]),
        ("geoffroy-lejeune", "jdd", ["nominations", "medias"]),
        ("geoffroy-lejeune", "valeurs-actuelles", ["medias"]),
        ("pierre-edouard-sterin", "pericles", ["argent"]),
        ("marion-marechal", "issep", ["nominations"]),
        ("europe1", "cnews", ["medias"]),
        ("cyril-hanouna", "europe1", ["medias"]),
        ("cyril-hanouna", "c8", ["medias"]),
    ):
        tag(a, b, stories)

    # ----- parcours : compléments, puis toutes les personnes encore sans frise -----
    add_steps("marine-le-pen", [
        step("2024-06-10", "Annonce conditionnelle pour Matignon",
             "Sur TF1, elle annonce que Jordan Bardella sera Premier ministre si le RN obtient une majorité aux législatives anticipées. La phrase est conditionnelle : ce n'est pas une nomination.",
             U_TF1_MAT, "TF1 Info"),
    ])
    add_steps("marion-marechal", [
        step("2018", "Fondation de l'ISSEP",
             "franceinfo la présente comme la fondatrice de cette école, à Lyon, en 2018.",
             U_ISSEP, "franceinfo"),
        step("2024-10-07", "Identité-Libertés",
             "franceinfo écrit qu'elle lance son propre mouvement et propose une coalition à Marine Le Pen. L'article décrit une proposition.",
             U_MARECHAL, "franceinfo"),
    ])
    add_steps("eric-ciotti", [
        step("2024-08-31", "Annonce de l'UDR",
             "Il annonce créer l'Union des droites pour la République. franceinfo précise qu'il est alors encore officiellement président des Républicains.",
             U_UDR, "franceinfo"),
        step("2026-09-05", "Proposition d'alliance pour 2027",
             "franceinfo, qui le présente comme président de l'UDR et allié du RN, rapporte qu'il a proposé à Marine Le Pen un pacte d'alliance. Aucun accord signé n'est constaté par l'article.",
             U_CIOTTI27, "franceinfo"),
    ])
    add_steps("geoffroy-lejeune", [
        step("2023-06-23", "Nomination annoncée par Arnaud Lagardère",
             "Le communiqué du groupe Lagardère dit qu'Arnaud Lagardère le nomme directeur de la rédaction du JDD. Il vient de Valeurs actuelles.",
             U_LEJ_LAG, "Lagardère"),
        step("2023-08-01", "Prise de fonction",
             "franceinfo : le groupe annonce qu'il prend la direction effective le 1er août, après une grève de la société des journalistes.",
             U_LEJ_AOUT, "franceinfo"),
        step("2023-08-01", "Phrase d'Arnaud Lagardère sur Vivendi",
             "Public Sénat rapporte cette déclaration d'Arnaud Lagardère au Figaro : « Ni Vincent Bolloré, ni quiconque de Vivendi, n'a été impliqué dans cette décision. »",
             U_LEJ_PS, "Public Sénat"),
    ])
    add_steps("vincent-bollore", [
        step("2021", "Prisma Media",
             "France 24 avec AFP écrit, le 10 septembre 2025, que Vivendi a racheté Prisma Media en 2021. L'article parle du groupe, pas d'une nomination signée de Vincent Bolloré ce jour-là.",
             U_PRISMA, "France 24"),
        step("2023-06-25", "Médias décrits par franceinfo",
             "franceinfo décrit, dans un article du 25 juin 2023, son rôle à Vivendi et à Canal+, et les titres Lagardère (Europe 1, JDD, Paris Match) alors en cours de rapprochement. Les liens correspondants sont ceux déjà sourcés sur la fiche.",
             U_BOLLORE, "franceinfo"),
    ])
    add_steps("pierre-edouard-sterin", [
        step("2017", "Nuit du bien commun",
             "France 3 le présente comme cofondateur en 2017, avec Stanislas de Lochner et Thibault Farrenq.",
             U_NUITS, "France 3"),
        step("2025-06", "Sortie du conseil",
             "Le même article de France 3 écrit qu'il a quitté le conseil d'administration en juin 2025. La FAQ du site de la Nuit du bien commun dit qu'il n'exerce plus de responsabilité exécutive, et date du 3 juin 2025 la prise d'acte par le conseil.",
             U_NUITS_FAQ, "La Nuit du bien commun"),
        step("2025-02-21", "Périclès, selon franceinfo",
             "franceinfo écrit qu'il veut consacrer 150 millions d'euros en dix ans au projet, et cite Arnaud Rérolle comme directeur général. L'article ne constate pas un versement à un parti.",
             U_STERIN, "franceinfo"),
    ])
    add_steps("cyril-hanouna", [
        step("2024-06-27", "Europe 1",
             "franceinfo traite de son émission « On marche sur la tête », visée par une mise en demeure de l'Arcom.",
             U_E1_HAN, "franceinfo"),
        step("2025-02-28", "Fin de C8 sur la TNT",
             "L'article de franceinfo sur son arrivée au groupe M6 rappelle l'arrêt de C8 sur la TNT le 28 février 2025.",
             U_HAN, "franceinfo"),
    ])
    add_steps("gerald-darmanin", [
        step("2021-03-03", "Ministre de l'Intérieur",
             "franceinfo : il annonce la dissolution de Génération identitaire, décidée en Conseil des ministres. L'article le nomme comme ministre de l'Intérieur.",
             U_DARM, "franceinfo"),
        step("2024-09-21", "Fin du ministère de l'Intérieur",
             "franceinfo présente Bruno Retailleau comme le nouveau ministre de l'Intérieur et écrit qu'il succède à Gérald Darmanin.",
             U_RETI, "franceinfo"),
    ])
    add_steps("emmanuel-macron", [
        step("2017-05-15", "Choix du Premier ministre",
             "franceinfo titre sur le choix d'Édouard Philippe. L'article constate la nomination.",
             U_PHI, "franceinfo"),
        step("2024-01-09", "Remaniement",
             "franceinfo : Gabriel Attal est nommé Premier ministre. L'article identifie le président de la République : Emmanuel Macron.",
             U_ATT, "franceinfo"),
    ])
    add_steps("raphael-glucksmann", [
        step("2024-03-11", "Prise de parole sur le mot « génocide »",
             "Le Figaro rend compte de son passage dans Quotidien. La citation figure sur la fiche. L'article ne sert pas ici à dater une investiture.",
             U_GLU, "Le Figaro"),
    ])
    add_steps("eric-zemmour", [
        step("2021-12-04", "Direction de campagne",
             "franceinfo présente Sarah Knafo comme directrice de sa campagne et de sa communication.",
             U_KNAFO, "franceinfo"),
    ])
    add_steps("bruno-retailleau", [
        step("2024-09-21", "Prédécesseur nommé par l'article",
             "franceinfo le présente comme ministre de l'Intérieur du gouvernement de Michel Barnier, succédant à Gérald Darmanin. Michel Barnier n'a pas de fiche : aucun lien n'est créé vers lui.",
             U_RETI, "franceinfo"),
    ])

    add_steps("sarah-knafo", [
        step("2021-12-04", "Campagne de 2022",
             "franceinfo la présente comme directrice de campagne et de la communication d'Éric Zemmour, et écrit qu'elle partage sa vie.",
             U_KNAFO, "franceinfo"),
        step("2024", "Parlement européen",
             "Le 21 octobre 2026, franceinfo écrit qu'elle a été « élue Reconquête au Parlement européen » deux ans après la campagne de 2022.",
             U_KNAFO_CE, "franceinfo"),
    ])
    add_steps("pascal-praud", [
        step("2017-11-13", "L'Heure des pros sur CNews",
             "franceinfo le présente comme l'animateur de cette émission sur CNews.",
             U_PRAUD, "franceinfo"),
        step("2026", "Diffusion sur Europe 1",
             "La page de l'émission sur europe1.fr, lue le 9 novembre 2026, indique qu'elle est présentée par lui. Elle ne date pas le début.",
             U_PRAUD_E1, "Europe 1"),
    ])
    add_steps("arnaud-rerolle", [
        step("2025-05-06", "Audition à l'Assemblée",
             "Sous serment, il se présente comme directeur général de Périclès, dit être l'auteur du document de septembre 2023, et déclare que Périclès ne finance pas de candidats, ni directement ni indirectement.",
             U_AN, "Assemblée nationale"),
    ])
    add_steps("lise-boell", [
        step("2024-06-05", "Direction de Fayard",
             "Hachette Livre, propriété de Vivendi selon franceinfo, annonce sa nomination. Le même article la présente comme l'éditrice d'Éric Zemmour.",
             U_BOELL, "franceinfo"),
    ])
    add_steps("serge-nedjar", [
        step("2025-09-10", "Prisma et CNews",
             "France 24/AFP : il est nommé directeur des rédactions de Prisma Media et conserve la direction de CNews.",
             U_PRISMA, "France 24"),
    ])
    add_steps("gerald-brice-viret", [
        step("2025-09-10", "Canal+ et Prisma",
             "France 24/AFP le présente comme directeur général de Canal+ France et vice-président de Prisma Media.",
             U_PRISMA, "France 24"),
    ])
    add_steps("philippe-olivier", [
        step("2022-04-18", "Campagne de Marine Le Pen",
             "franceinfo le présente comme son plus proche conseiller et comme directeur de la cellule « Idées et images ».",
             U_OLIVIER, "franceinfo"),
    ])
    add_steps("kevin-pfeffer", [
        step("2025-06-25", "Trésorier du RN",
             "franceinfo le désigne comme le trésorier du parti, sans dater le début de la fonction.",
             U_PFEFFER, "franceinfo"),
    ])
    add_steps("tugdual-denis", [
        step("2023-06-21", "Direction de Valeurs actuelles",
             "Le journal publie son texte sous un titre qui le présente comme le nouveau directeur de la rédaction.",
             U_VA, "Valeurs actuelles"),
        step("2024-09-11", "Fonction encore indiquée par BFMTV",
             "BFMTV le présente comme directeur de la rédaction de Valeurs actuelles.",
             U_VA_BFM, "BFMTV"),
    ])
    add_steps("erik-tegner", [
        step("2026-06-20", "Frontières et CNews",
             "franceinfo le désigne comme fondateur et directeur de Frontières, et comme éditorialiste sur CNews.",
             U_TEGNER, "franceinfo"),
    ])
    add_steps("philippe-conrad", [
        step("2014", "Institut Iliade",
             "L'institut indique être né en 2014, le cite comme président d'honneur et le nomme parmi ses fondateurs.",
             U_ILIADE, "Institut Iliade"),
    ])
    add_steps("donat-vidal-revel", [
        step("2022-10-20", "Direction générale d'Europe 1",
             "Lagardère annonce sa nomination par Arnaud Lagardère et Constance Benqué. Le communiqué ne dit pas s'il est encore en poste en 2026.",
             U_E1, "Lagardère"),
    ])
    add_steps("arnaud-lagardere", [
        step("2022-10-20", "Nomination à Europe 1",
             "Il nomme Donat Vidal-Revel directeur général d'Europe 1, avec Constance Benqué.",
             U_E1, "Lagardère"),
        step("2023-06-23", "Nomination au JDD",
             "Le communiqué du groupe dit qu'il nomme Geoffroy Lejeune directeur de la rédaction.",
             U_LEJ_LAG, "Lagardère"),
        step("2025-09-10", "Prisma Media",
             "France 24/AFP le présente comme président de Prisma Media et comme l'auteur du message nommant Serge Nedjar.",
             U_PRISMA, "France 24"),
    ])
    add_steps("constance-benque", [
        step("2022-10-20", "Lagardère News",
             "Le communiqué la présente comme présidente de Lagardère News et comme coautrice de la nomination du directeur général d'Europe 1.",
             U_E1, "Lagardère"),
    ])
    add_steps("francois-durvye", [
        step("2024-07-20", "Nom cité dans le document Périclès",
             "franceinfo, d'après le document de 2023, le nomme fondateur et administrateur aux côtés de Pierre-Édouard Stérin. Le 6 mai 2025, Arnaud Rérolle dit que certains éléments de ce document ne sont plus d'actualité.",
             U_PERICLES, "franceinfo"),
    ])
    add_steps("alban-du-rostu", [
        step("2024-07-20", "Nom cité dans le document Périclès",
             "Même article : le document le nomme fondateur et administrateur. Même nuance, tirée de l'audition du 6 mai 2025.",
             U_PERICLES, "franceinfo"),
    ])

    keys = ("président", "direct", "déput", "maire", "ministre", "fondat", "chronique",
            "candidat", "élu", "secrétaire", "animat", "journaliste", "avocat", "trésor", "membre")

    def best(n):
        es = [e for e in E if n["id"] in (e["source"], e["target"]) and e.get("date") and str(e.get("url", "")).startswith("https")]
        if not es:
            return None
        def score(e):
            r = e["relation"].lower()
            role = 1 if any(k in r for k in keys) else 0
            outgoing = 1 if e["source"] == n["id"] else 0
            return (role and outgoing, role, outgoing, e["date"])
        return sorted(es, key=score)[-1]

    for n in list(N):
        if n["type"] != "person" or n.get("parcours"):
            continue
        e = best(n)
        if e:
            other_id = e["target"] if e["source"] == n["id"] else e["source"]
            other = by[other_id]["name"]
            if e["source"] == n["id"]:
                text = "Lien déjà sourcé vers " + other + " : " + e["relation"]
            else:
                text = "Lien déjà sourcé depuis " + other + " : " + e["relation"]
            add_steps(n["id"], [step(e["date"], "Lien public daté", text[:360], e["url"], "source de la fiche")])
            continue
        sts = [s for s in n["statements"] if s.get("date") and str(s.get("url", "")).startswith("https")]
        if not sts:
            continue
        s = sorted(sts, key=lambda x: x["date"])[0]
        add_steps(n["id"], [step(
            s["date"], "Déclaration publique",
            (s.get("medium") or "Déclaration déjà reproduite sur la fiche.")[:280],
            s["url"], "source de la fiche")])

    # ----- frises courtes d'organisations -----
    add_steps("jdd", [
        step("2023-06-23", "Nomination de Geoffroy Lejeune",
             "Communiqué de Lagardère : Arnaud Lagardère le nomme directeur de la rédaction. Il vient de Valeurs actuelles. franceinfo écrit le même jour que la rédaction fait grève contre cette arrivée.",
             U_LEJ_LAG, "Lagardère"),
        step("2023-08-01", "Prise de fonction et phrase sur Vivendi",
             "Public Sénat constate la prise de fonction et rapporte qu'Arnaud Lagardère a déclaré au Figaro n'avoir associé ni Vincent Bolloré ni Vivendi à la décision.",
             U_LEJ_PS, "Public Sénat"),
    ])
    add_steps("fayard", [
        step("2023", "Contrôle de Vivendi",
             "franceinfo écrit, le 5 juin 2024, qu'Hachette Livre est passé fin 2023 sous le contrôle de Vivendi, groupe de Vincent Bolloré, et que Fayard en fait partie.",
             U_BOELL, "franceinfo"),
        step("2024-04", "Départ d'Isabelle Saporta",
             "Le même article écrit qu'Isabelle Saporta, en poste moins de deux ans, a été licenciée en avril pour « différends stratégiques ». Elle n'a pas de fiche dans cette version.",
             U_BOELL, "franceinfo"),
        step("2024-06-05", "Nomination de Lise Boëll",
             "Hachette Livre annonce sa nomination comme présidente-directrice générale. franceinfo la présente comme l'éditrice d'Éric Zemmour.",
             U_BOELL, "franceinfo"),
    ])
    add_steps("europe1", [
        step("2021", "Rapprochement avec CNews",
             "L'article de franceinfo du 25 juin 2023, déjà utilisé pour les liens du groupe, situe en 2021 le rapprochement éditorial avec CNews. La date de l'article n'est pas la date de l'opération.",
             U_BOLLORE, "franceinfo"),
        step("2022-10-20", "Directeur général",
             "Lagardère annonce la nomination de Donat Vidal-Revel par Arnaud Lagardère et Constance Benqué.",
             U_E1, "Lagardère"),
    ])
    add_steps("cnews", [
        step("2016", "Chaîne du groupe",
             "Le portrait de Pascal Praud par franceinfo (13 novembre 2017) le situe sur la chaîne d'information du groupe Bolloré, devenue CNews, où il présente « L'Heure des Pros ».",
             U_PRAUD, "franceinfo"),
        step("2025-09-10", "Direction citée par France 24",
             "France 24 désigne Serge Nedjar comme le patron de CNews et Gérald-Brice Viret comme directeur général de Canal+ France, groupe auquel la chaîne appartient.",
             U_PRISMA, "France 24"),
    ])
    add_steps("vivendi-canal", [
        step("2014", "Conseil de surveillance",
             "franceinfo (25 juin 2023) écrit qu'il préside le conseil de surveillance de Vivendi, et par là Canal+, depuis 2014.",
             U_BOLLORE, "franceinfo"),
        step("2021", "Prisma Media",
             "France 24 avec AFP écrit que Vivendi a racheté Prisma Media en 2021.",
             U_PRISMA, "France 24"),
        step("2023-06-25", "Lagardère",
             "Le même article de franceinfo décrit l'OPA de Vivendi sur Lagardère, propriétaire d'Europe 1, du JDD et de Paris Match.",
             U_BOLLORE, "franceinfo"),
    ])
    add_steps("pericles", [
        step("2023-09", "Document",
             "Arnaud Rérolle déclare sous serment, le 6 mai 2025, que le document publié par L'Humanité date de septembre 2023 et qu'il en est l'auteur. Il ajoute que certains éléments ne sont plus d'actualité.",
             U_AN, "Assemblée nationale"),
        step("2024-07-18", "Publication",
             "franceinfo relate la publication du document par L'Humanité et les noms qui y figurent comme fondateurs et administrateurs : Pierre-Édouard Stérin, François Durvye, Alban du Rostu.",
             U_PERICLES, "franceinfo"),
        step("2025-05-06", "Audition et démenti sur le financement électoral",
             "Sous serment, Arnaud Rérolle déclare : « Périclès ne finance pas de candidats, ni directement ni indirectement. »",
             U_AN, "Assemblée nationale"),
    ])
    add_steps("issep", [
        step("2018", "Création à Lyon",
             "franceinfo présente l'école comme fondée à Lyon en 2018 par Marion Maréchal.",
             U_ISSEP, "franceinfo"),
        step("2022-05", "Départ de la direction",
             "L'article de franceinfo qui annonce sa tête de liste pour Reconquête écrit qu'elle a quitté la direction de l'ISSEP, jugeant l'engagement politique incompatible avec cette fonction.",
             "https://www.franceinfo.fr/elections/europeennes/europeennes-marion-marechal-designee-tete-de-liste-du-parti-reconquete-annonce-eric-zemmour_6047075.html",
             "franceinfo"),
    ])
    add_steps("valeurs-actuelles", [
        step("2023-06-21", "Nouveau directeur de la rédaction",
             "Le journal publie un texte signé Tugdual Denis. Le titre le présente comme le nouveau directeur de la rédaction, après le départ de Geoffroy Lejeune.",
             U_VA, "Valeurs actuelles"),
        step("2024-09-11", "Fonction confirmée par BFMTV",
             "BFMTV le présente comme directeur de la rédaction de Valeurs actuelles lors d'un débat avec Alain Duhamel.",
             U_VA_BFM, "BFMTV"),
    ])
    add_steps("prisma-media", [
        step("2021", "Rachat par Vivendi",
             "France 24 avec AFP l'écrit dans son article du 10 septembre 2025.",
             U_PRISMA, "France 24"),
        step("2025-09-10", "Direction des rédactions",
             "Serge Nedjar est nommé directeur des rédactions. Gérald-Brice Viret est vice-président. Arnaud Lagardère est président, selon le même article.",
             U_PRISMA, "France 24"),
    ])
    add_steps("udr", [
        step("2024-08-31", "Annonce de création",
             "Éric Ciotti annonce le parti à Levens. franceinfo note qu'il demeure officiellement président des Républicains à cette date.",
             U_UDR, "franceinfo"),
        step("2026-09-05", "Proposition à Marine Le Pen",
             "franceinfo le présente comme président de l'UDR et rapporte sa proposition de pacte pour 2027. Ce n'est pas un accord constaté.",
             U_CIOTTI27, "franceinfo"),
    ])
    add_steps("frontieres", [
        step("2026-06-20", "Direction",
             "franceinfo désigne Erik Tegnér comme fondateur et directeur, et comme éditorialiste sur CNews.",
             U_TEGNER, "franceinfo"),
    ])
    add_steps("nuits-du-bien-commun", [
        step("2017", "Création",
             "France 3 nomme trois fondateurs : Stanislas de Lochner, Thibault Farrenq et Pierre-Édouard Stérin.",
             U_NUITS, "France 3"),
        step("2025-06-03", "Sortie des fondateurs",
             "La FAQ de l'organisation date du 3 juin 2025 la prise d'acte, par le conseil, de la sortie du collège des fondateurs. France 3 écrit que le départ du conseil d'administration date de juin 2025.",
             U_NUITS_FAQ, "La Nuit du bien commun"),
    ])
    add_steps("institut-iliade", [
        step("2014", "Création indiquée par l'institut",
             "La page Présentation écrit « Né en 2014 » et cite Philippe Conrad comme président d'honneur.",
             U_ILIADE, "Institut Iliade"),
        step("2014", "Fondateurs selon l'institut",
             "L'institut écrit avoir été fondé par Jean-Yves Le Gallou, Philippe Conrad et Bernard Lugan, et qu'Henry de Lesquen n'y a jamais participé. La page ne donne pas le jour.",
             U_ILIADE_F, "Institut Iliade"),
    ])
    add_steps("rn", [
        step("2011-01-16", "Présidence de Marine Le Pen",
             "Elle est proclamée présidente du Front national, qui deviendra le Rassemblement national. L'article constate le vote du congrès de Tours.",
             U_MLP, "franceinfo"),
        step("2025-06-25", "Trésorier désigné par franceinfo",
             "franceinfo désigne Kévin Pfeffer comme le trésorier du parti. L'article ne date pas l'entrée en fonction.",
             U_PFEFFER, "franceinfo"),
    ])

    spheres = {
        "sarah-knafo": "partis", "philippe-olivier": "partis", "kevin-pfeffer": "partis",
        "eric-ciotti": "partis", "udr": "partis", "marine-le-pen": "partis", "jordan-bardella": "partis",
        "eric-zemmour": "partis", "marion-marechal": "partis", "bruno-retailleau": "partis",
        "rn": "partis", "reconquete": "partis", "lr": "partis", "identite-libertes": "partis",
        "pascal-praud": "medias", "serge-nedjar": "medias", "gerald-brice-viret": "medias",
        "tugdual-denis": "medias", "erik-tegner": "medias", "donat-vidal-revel": "medias",
        "constance-benque": "medias", "geoffroy-lejeune": "medias", "cyril-hanouna": "medias",
        "cnews": "medias", "c8": "medias", "europe1": "medias", "jdd": "medias",
        "valeurs-actuelles": "medias", "prisma-media": "medias", "frontieres": "medias",
        "vivendi-canal": "medias", "lagardere": "medias",
        "vincent-bollore": "argent", "pierre-edouard-sterin": "argent",
        "francois-durvye": "argent", "alban-du-rostu": "argent", "arnaud-lagardere": "argent",
        "kevin-pfeffer": "partis",
        "pericles": "idees", "arnaud-rerolle": "idees", "issep": "idees",
        "institut-iliade": "idees", "philippe-conrad": "idees", "nuits-du-bien-commun": "idees",
        "fayard": "edition", "lise-boell": "edition",
        "arcom": "institutions",
    }
    for i, s in spheres.items():
        if i in by:
            by[i]["sphere"] = s

    missing = [n["id"] for n in N if n["type"] == "person" and not n.get("parcours")]
    if missing:
        raise SystemExit("parcours manquant : " + ", ".join(missing))
