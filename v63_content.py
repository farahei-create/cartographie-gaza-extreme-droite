# -*- coding: utf-8 -*-
"""Rattrapage du 16/11/2026 au soir, publié le 24/11/2026 (cache v63).
Contenu préparé le 16/11 (commit local 20521b0), jamais poussé. Réintégré
sans les doublons déjà en ligne depuis le 17/11.
Messages X relus le 24/11/2026 sur les comptes officiels (heure de Paris).
Pages de presse relues le même jour.
« génocide », « ignominie », « fliquer », « mauvaise foi » sont les mots
des personnes, pas ceux du site."""

G = "Gaza – déclarations"
F = "France – normalisation de l'extrême droite"
M = "Médias – structure"
V = "France – montée des violences"

X_RET = "https://x.com/BrunoRetailleau/status/2122378866601730339"
X_MLP = "https://x.com/MLP_officiel/status/2122291088513962173"
X_BAR = "https://x.com/J_Bardella/status/2122286328653951449"
X_JLM_MONDE = "https://x.com/JLMelenchon/status/2122246135523787044"
X_PANOT = "https://x.com/MathildePanot/status/2122340463986258359"
X_GWG = "https://x.com/GWGoldnadel/status/2122394263153762732"
X_AEK = "https://x.com/Aminelkhatmi/status/2122031054991262063"
U_CGTV = "https://www.cg-tv.com/articles/amine-el-khatmi-annonce-quitter-c-news-et-s-en-prend-a-l-arcom-des-fonctionnaires-sont-payes-pour-fliquer-le-debat-public"
U_DEP = "https://www.ladepeche.fr/2026/11/16/presidentielle-2027-aucune-banque-francaise-ne-veut-financer-la-campagne-du-rn-denonce-jean-philippe-tanguy-qui-pointe-un-echec-de-letat-13655212.php"
U_FIG = "https://www.lefigaro.fr/elections/presidentielles/en-direct-presidentielle-2027-marine-le-pen-edouard-philippe-emmanuel-macron-ukraine-teddy-riner-20261116"
U_TVMAG = "https://tvmag.lefigaro.fr/programme-tv/actu-tele/mais-pour-qui-il-se-prend-la-colere-de-pascal-praud-cnews-contre-benjamin-duhamel-france-inter-20261116"
U_F24 = "https://www.france24.com/fr/info-en-continu/20261116-lyc%C3%A9e-le-pen-veut-supprimer-parcoursup-le-contr%C3%B4le-continu-et-avancer-le-bac-en-mai"
VID_GG = {
    "url": "https://rmc.bfmtv.com/replay-emissions/les-grandes-gueules/video-jordan-bardella-face-aux-gg-16-11_VN-202611160436.html",
    "platform": "rmc.bfmtv.com",
    "title": "Jordan Bardella face aux GG - 16/11",
    "source": "RMC (site officiel)",
}


def apply(N, E, by, step, node, link, st):
    by.update({n["id"]: n for n in N})

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

    def add_step(pid, s):
        n = by[pid]
        ps = n.setdefault("parcours", [])
        if any(p.get("date") == s["date"] and p.get("title") == s["title"] for p in ps):
            return
        ps.append(s)

    def add_link(src, tgt, rel, url, date, section, nature):
        for e in E:
            if e["source"] == src and e["target"] == tgt and e.get("url") == url:
                return
        link(src, tgt, rel, url, date)
        E[-1]["section"] = section
        E[-1]["nature"] = nature

    def person(pid, name, role, desc, cat, sub, secs, statements, steps):
        if pid in by:
            add(pid, statements)
            for s in steps:
                add_step(pid, s)
            return
        add_node(pid, name, "person", role, desc, [], cat, sub, secs)
        add(pid, statements)
        by[pid]["parcours"] = steps

    # --- Fiches déjà en ligne ---
    add("bruno-retailleau", [
        ("Si je suis élu, la France rejoindra sans délai cette initiative. Un étranger en situation irrégulière doit partir. S'il ne peut pas être renvoyé chez lui, il le sera vers un pays tiers qui l'accueillera.",
         "2026-11-16",
         "Message sur X (@BrunoRetailleau), 16 novembre 2026, 18:18, heure de Paris. Il parle de l'accord annoncé à Vienne par l'Allemagne, l'Autriche, le Danemark, la Grèce et les Pays-Bas avec le Rwanda pour des « centres de retour ». Le Figaro rappelle le même jour qu'Emmanuel Macron avait jugé ces centres « ni efficaces », ni conformes aux valeurs de l'UE, et que 45 ONG se disent « fermement opposées » au projet.",
         X_RET, F, "france"),
        ("La France, elle, ne fait pas partie de cet accord en raison de l’opposition du Président de la République.",
         "2026-11-16",
         "Même message sur X, 16 novembre 2026. Il ajoute : « Un centre de retour au Rwanda sera notamment la meilleure solution pour lutter contre l'immigration irrégulière venue de l'Afrique des Grands Lacs vers Mayotte. »",
         X_RET, F, "france"),
    ])

    add("marine-le-pen", [
        ("Nous voulons aussi mettre en place la priorité nationale dans l’accès aux logements étudiants. C’est la moindre des choses que d’offrir à nos jeunes une priorité d’accès dans leur propre pays.",
         "2026-11-16",
         "Message sur X (@MLP_officiel), 16 novembre 2026, 12:30, heure de Paris, avec un extrait vidéo. Selon l'AFP (France 24, 16 novembre), la vidéo publiée ce lundi est un entretien avec le président du mouvement de jeunesse du RN et Louise Montangon, responsable de l'UNI à Bordeaux.",
         X_MLP, F, "france"),
    ])

    add("jordan-bardella", [
        ("On ne propose plus l'interdiction de la double nationalité, en revanche, nous sommes favorables à la déchéance de nationalité pour les terroristes islamistes ou pour toute personne qui s'en prend aux intérêts fondamentaux de la Nation française.",
         "2026-11-16",
         "Message sur X (@J_Bardella), 16 novembre 2026, 12:11, heure de Paris, extrait de son passage dans Les Grandes Gueules (RMC). La veille, Marine Le Pen disait avoir « commis une erreur » en proposant l'interdiction de la double nationalité.",
         X_BAR, F, "france", VID_GG),
    ])

    # Le message X du 16/11 13:26 (« sondage bidon », Le Parisien) est déjà
    # en ligne, en trois fragments, d'après i24NEWS : on ne le recopie pas.
    add("jean-luc-melenchon", [
        ("Manque de vocabulaire ? « Le Monde » de dimanche caractérise l'offensive de Le Pen d'« illibérale ». Mot creux et protecteur de ceux qui protégeront l'extrême droite jusqu'au bout et diffameront la gauche radicale jusqu'à la mort.",
         "2026-11-16",
         "Message sur X (@JLMelenchon), 16 novembre 2026, 9:31, heure de Paris. La phrase suivante, sur le référendum en Ukraine, n'est pas reprise. Il ne nomme personne au Monde.",
         X_JLM_MONDE, F, "france"),
    ])

    add("mathilde-panot", [
        ("Une partie de nos concitoyens vit aujourd’hui dans la peur de mourir sous les balles des racistes.\n\nQuand est-ce que le gouvernement va prendre au sérieux la montée de l’islamophobie et de la négrophobie dans notre pays ?",
         "2026-11-16",
         "Message sur X (@MathildePanot), 16 novembre 2026, 15:46, heure de Paris. Avant ces phrases, elle écrit qu'un policier hors service a été arrêté à Paris alors qu'il menaçait de « tuer des personnes de couleur », et cite l'attentat de Trappes. Aucun suspect n'est nommé sur le site.",
         X_PANOT, V, "france"),
    ])

    add("gilles-william-goldnadel", [
        ("19h : Très bel exploit journalistique de @franceinter qui réussit à faire un reportage sur l’antisémitisme en progression sans prononcer les mots « islamistes » « extrême gauche » et « France Insoumise » . Déni et mauvaise foi sont les 2 mamelles de l’odieux visuel  public .",
         "2026-11-16",
         "Message sur X (@GWGoldnadel), 16 novembre 2026, 19:19, heure de Paris. Il cite un message du Parisien sur l'enquête selon laquelle l'antisémitisme est en hausse pour 8 Français sur 10.",
         X_GWG, M, "france"),
    ])

    add("pascal-praud", [
        ("France Inter est un média engagé dans la campagne électorale.",
         "2026-11-16",
         "CNews, L'Heure des pros, 16 novembre 2026, cité par TV Magazine (Le Figaro). Il réagit à une question de Benjamin Duhamel, sur France Inter, demandant à Guillaume Debré (LCI) si CNews est une chaîne d'opinion. Guillaume Debré avait répondu que CNews est « un concurrent, considéré par l'Arcom comme une chaîne Info ».",
         U_TVMAG, M, "france"),
        ("Je rappelle que nous sommes une chaîne d’information qui montre le réel, contrairement aux autres.",
         "2026-11-16",
         "CNews, 16 novembre 2026, cité par TV Magazine. Il dit aussi : « Nous ne sommes pas un média d’opinion ».",
         U_TVMAG, M, "france"),
    ])

    add_link("louise-montangon", "marine-le-pen",
             "interroge Marine Le Pen, avec le président du mouvement de jeunesse du RN, dans une vidéo publiée le 16/11/2026 sur les réseaux de la candidate (AFP)",
             U_F24, "2026-11-16", "france", "autre")

    # Fiche déjà créée le 20/11 (fuites présumées) : on ajoute seulement les
    # phrases du 16/11 sur les banques, absentes jusqu'ici.
    add("jean-philippe-tanguy", [
        ("Aucune banque française n'a voulu nous prêter. C'est un échec pour ce gouvernement qui avait promis un accès à une banque de la démocratie. Le RN est mal traité par le système bancaire.",
         "2026-11-16",
         "France 2, Les 4 Vérités (Télématin), 16 novembre 2026, phrase publiée par @telematin et reprise par La Dépêche. Le Parisien et La Dépêche rappellent que Bruno Retailleau dit lui aussi n'avoir « pas de prêt bancaire », que la Société générale et la Banque postale ne financent plus aucune campagne, et que le RN a annoncé un préaccord avec deux banques européennes.",
         U_DEP, F, "france"),
        ("Les banques françaises ne sont pas très contentes de notre programme et c’est plutôt bon signe. Aucune n’a voulu nous prêter pour la campagne présidentielle",
         "2026-11-16",
         "France 2, 16 novembre 2026, cité par le direct du Figaro. Le journal écrit qu'il a aussi appelé les maires à parrainer Marine Le Pen.",
         U_FIG, F, "france"),
    ])
    add_step("jean-philippe-tanguy",
             step("2026-11-16", "France 2, financement de la campagne",
                  "Il dit qu'aucune banque française n'a voulu prêter au RN et que le parti a sollicité des banques de l'Union européenne, comme la loi le permet.",
                  U_DEP, "La Dépêche"))
    add_link("jean-philippe-tanguy", "rn",
             "député RN de la Somme, chargé du programme économique du parti (La Dépêche, 16/11/2026)",
             U_DEP, "2026-11-16", "france", "ascension")

    person(
        "amine-el-khatmi", "Amine El-Khatmi",
        "Essayiste, chroniqueur sur CNews jusqu'en novembre 2026 (X, 15 novembre 2026)",
        "Le 15 novembre 2026, il annonce sur X qu'il n'est plus chroniqueur sur CNews, l'Arcom ayant décidé de décompter son temps de parole comme personnalité politique divers droite. Il critique ce décompte. Pas de photo libre : monogramme.",
        "Journalistes & éditorialistes", "Journalistes & chroniqueurs", ("france",),
        [
            ("Après dix années de présence sur CNews, je ne serai plus chroniqueur sur la chaîne, l’ARCOM ayant décidé de décompter mon temps de parole comme « personnalité politique divers droite ».",
             "2026-11-15",
             "Message sur X (@Aminelkhatmi), 15 novembre 2026, 19:16, heure de Paris. CGTV écrit le 16 novembre qu'il s'est présenté aux municipales de Paris sur la liste LR menée par Rachida Dati, et que l'Arcom ne le contraint pas à quitter la chaîne tant que celle-ci équilibre son temps de parole.",
             X_AEK, M, "france"),
            ("En France, tout se casse la gueule, mais des fonctionnaires sont payés pour fliquer le débat public. Une hérésie de plus au pays de toutes les hérésies.",
             "2026-11-15",
             "Même message sur X, 15 novembre 2026. Il termine par « Vive CNews et vive la liberté d’expression ! ».",
             X_AEK, M, "france"),
        ],
        [step("2026-11-15", "Départ de CNews",
              "Il annonce qu'il n'est plus chroniqueur sur CNews après le décompte de son temps de parole par l'Arcom comme personnalité politique divers droite.",
              X_AEK, "X")],
    )
    add_link("amine-el-khatmi", "cnews",
             "annonce le 15/11/2026 qu'il n'est plus chroniqueur sur la chaîne, après dix ans",
             X_AEK, "2026-11-15", "france", "autre")
    add_link("amine-el-khatmi", "arcom",
             "critique la décision de décompter son temps de parole comme « personnalité politique divers droite » (X, 15/11/2026)",
             X_AEK, "2026-11-15", "france", "opposition")

    # Fiche déjà créée le 17/11 d'après la page CNews (« CNEWS fait partie
    # de la liberté et de la diversité de la presse ») : on n'ajoute que
    # la phrase sur le débat, absente jusqu'ici.
    add("bruno-le-maire", [
        ("Poser ce genre de débats à un moment où les nationalismes peuvent gagner en Europe, où nous risquons de voir l’Europe de disloquer entre la Chine d’un côté et les États-Unis de l’autre, s’occuper de voir si l’on va interdire une chaîne, je trouve cela déplacé et dérisoire",
         "2026-11-16",
         "CNews/Europe 1, 16 novembre 2026, cité par le direct du Figaro. « de disloquer » est la graphie du Figaro. Le journal rappelle que la pétition pour la fermeture de CNews a été écartée par les parlementaires et que La France insoumise défend encore la mesure.",
         U_FIG, M, "france"),
    ])
    add_step("bruno-le-maire",
             step("2026-11-16", "CNews/Europe 1, débat sur l'interdiction de CNews",
                  "Il juge « déplacé et dérisoire » le débat sur l'interdiction d'une chaîne.",
                  U_FIG, "Le Figaro"))
    add_link("bruno-le-maire", "cnews",
             "juge « déplacé et dérisoire » le débat sur l'interdiction de la chaîne (CNews/Europe 1, 16/11/2026, cité par Le Figaro)",
             U_FIG, "2026-11-16", "france", "autre")
