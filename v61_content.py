# -*- coding: utf-8 -*-
"""Mise à jour du 23/11/2026 (matin) : du 21/11 au 23/11, 8 h.
Chaque phrase a été relue le 23/11/2026 sur la page ou le message cité, entre guillemets.
Messages X : texte lu sur le compte officiel de la personne (heure de Paris).
« génocide », « délire », « lynchage », « terroristes » sont les mots des personnes citées,
pas ceux d'Onrecord."""

G = "Gaza – déclarations"
F = "France – normalisation de l'extrême droite"
NU = "Nuance / contexte"

# Messages X (comptes officiels)
X_MLP = "https://x.com/MLP_officiel/status/2124600571608924656"
X_ODOUL = "https://x.com/JulienOdoul/status/2124632436822970683"
X_RUFFIN = "https://x.com/Francois_Ruffin/status/2124615432292438516"
X_FAURE = "https://x.com/faureolivier/status/2124136628478169240"
X_AUBRY = "https://x.com/ManonAubryFr/status/2124457878874681827"
X_JLM = "https://x.com/JLMelenchon/status/2124442900591173906"
X_PANOT = "https://x.com/MathildePanot/status/2124196732355662032"
X_HASSAN = "https://x.com/RimaHas/status/2124473578150048248"

# Presse
U_E1_MOUTOUH = "https://www.europe1.fr/politique/soupcons-de-fuites-vers-le-rn-je-veux-savoir-qui-veut-ma-tete-le-prefet-hugues-moutouh-annonce-porter-plainte-1242523"
U_PE_MLP = "https://www.progres.net.eg/marine-le-pen-devoile-les-grandes-lignes-de-sa-politique-etrangere-en-cas-daccession-a-lelysee/"
U_JDD_RUFFIN = "https://www.lejdd.fr/politique/le-rn-est-aux-portes-du-pouvoir-francois-ruffin-jette-leponge-pour-2027-189369"
U_I24_FAURE = "https://www.i24news.tv/fr/actu/france/artc-france-la-loi-contre-le-commerce-avec-les-implantations-israeliennes-bloquee-a-l-assemblee-nationale"
U_AA_JLM = "https://www.aa.com.tr/fr/politique/le-candidat-%C3%A0-la-pr%C3%A9sidentielle-m%C3%A9lenchon-appelle-%C3%A0-la-lib%C3%A9ration-du-m%C3%A9decin-palestinien-abou-safiya-d%C3%A9tenu-par-isra%C3%ABl/4133641"
U_CNEWS_ROYAL = "https://www.cnews.fr/france/2026-11-23/si-le-rn-arrive-au-pouvoir-les-gens-dextreme-droite-vont-tuer-des-noirs-et-des"
U_JDD_ZEM = "https://www.lejdd.fr/politique/jai-ete-convie-jy-serai-zemmour-martele-sa-volonte-de-participer-a-une-primaire-de-la-droite-189375"
U_RTL_KNAFO = "https://www.rtl.fr/actu/politique/on-ne-craint-pas-la-concurrence-sur-rtl-sarah-knafo-dit-croire-plus-que-jamais-a-une-primaire-a-droite-et-assure-qu-il-n-est-absolument-pas-question-qu-eric-zemmour-se-retire-7900699235"
U_TF1_BALLARD = "https://www.tf1info.fr/politique/elections/presidentielle/en-direct-presidentielle-2027-colere-sociale-son-combat-est-le-mien-l-hommage-appuye-de-glucksmann-a-ruffin-apres-son-retrait-les-dernieres-informations-de-ce-lundi-23-novembre-2026-2477497.html"

MOUTOUH = ("Affaire des fuites présumées du ministère de l'Intérieur vers le RN : le préfet Hugues Moutouh est soupçonné "
           "d'avoir renseigné le Rassemblement national sur des affaires en cours ; une enquête judiciaire est ouverte. "
           "Il conteste. ")
PRIMAIRE = ("Projet de primaire de la droite et du centre (novembre 2026) : la participation d'Éric Zemmour (Reconquête) "
            "est en débat ; Gabriel Attal et Bruno Retailleau s'y opposent (JDD, 22 novembre 2026). ")


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

    def add_step(pid, s):
        n = by[pid]
        ps = n.setdefault("parcours", [])
        if any(p.get("date") == s["date"] and p.get("title") == s["title"] for p in ps):
            return
        ps.append(s)

    def person(pid, name, role, desc, cat, sub, secs, statements, steps):
        if pid in by:
            add(pid, statements)
            for s in steps:
                add_step(pid, s)
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
    add("hugues-moutouh", [
        ("Je veux savoir qui veut ma tête et pourquoi. Donc, je vais me battre.",
         "2026-11-23",
         MOUTOUH + "Europe 1 matin, 23 novembre 2026, au micro de Dimitri Pavlenko. Il annonce porter plainte « pour violation du secret de l'enquête, recel et complicité » et dit : « Je n'ai jamais fait de politique dans les fonctions que j'ai exercées ».",
         U_E1_MOUTOUH, F, "france"),
        ("C'est un lynchage médiatique qui est commandé",
         "2026-11-23",
         MOUTOUH + "Europe 1 matin, 23 novembre 2026. Le Figaro, dans la version mise à jour de son article, rapporte la phrase ainsi : « C'est un lynchage médiatique. Et je pense que ce lynchage est organisé ». Il ne dit pas, dans ces pages, qui l'organiserait.",
         U_E1_MOUTOUH, NU, "france"),
    ])
    add_step("hugues-moutouh", step("2026-11-23", "Annonce d'une plainte",
             "Sur Europe 1, il annonce porter plainte pour violation du secret de l'enquête, recel et complicité.",
             U_E1_MOUTOUH, "Europe 1"))

    # --- Gaza ---
    add("marine-le-pen", [
        ("L'Égypte a joué un rôle extrêmement important dans le conflit israélo-palestien, elle détient la clé de la solution. Je soutiens la solution à deux États, mais reconnaître aujourd'hui l'État palestinien, c'est reconnaître le Hamas. Cela ne l'affaiblira pas, au contraire.",
         "2026-11-22",
         "Message sur X (@MLP_officiel), 22 novembre 2026, 21:27, heure de Paris, avec un extrait vidéo de son entretien à une chaîne égyptienne. Texte recopié tel que le compte le publie (« israélo-palestien » compris). Dans la version française de l'entretien publiée par Le Progrès Égyptien (22 novembre 2026), elle dit aussi : « Je ne confonds pas les civils avec le Hamas ».",
         X_MLP, G, "gaza"),
    ])
    add("jean-luc-melenchon", [
        ("Il faut sauver le docteur palestinien Hussam Abu Safiya !",
         "2026-11-22",
         "Message sur X (@JLMelenchon), 22 novembre 2026, 11:00, heure de Paris, avec une vidéo et le lien d'une pétition d'Amnesty International. Mathilde Panot a publié le même message. Selon l'agence Anadolu, le Dr Abou Safiya, directeur de l'hôpital Kamal Adwan, est détenu par Israël depuis décembre 2024.",
         X_JLM, G, "gaza"),
    ])
    add("mathilde-panot", [
        ("Nous n'arrêterons jamais de nous battre pour la liberté et la dignité du peuple palestinien.",
         "2026-11-21",
         "Message sur X (@MathildePanot), 21 novembre 2026, 18:42, heure de Paris : elle dit avoir rencontré « Dana et sa famille, évacués de Gaza ».",
         X_PANOT, G, "gaza"),
    ])

    person(
        "olivier-faure", "Olivier Faure",
        "Premier secrétaire du Parti socialiste, député (i24NEWS, 21 novembre 2026)",
        "Premier secrétaire du Parti socialiste. Auteur d'une proposition de loi visant à interdire le commerce avec les implantations israéliennes en Cisjordanie et sur le Golan, adoptée en commission le 9 novembre 2026 ; la séance du 19 novembre s'est achevée à minuit sans vote sur le texte (i24NEWS, NosParlementaires). Pas de photo libre : monogramme.",
        "Responsables politiques", "Partis & dirigeants de parti", ("gaza", "france"),
        [
            ("Voilà ce que le RN et Renaissance ont souhaité couvrir par leur obstruction jeudi. Nous n'avons pas pu aller au terme de la proposition de loi. Je demande au gouvernement de procéder par voie réglementaire pour que toute complicité soit désormais interdite. Commerce, services et investissements doivent être interdits dans les colonies illégales israéliennes en Cisjordanie.",
             "2026-11-21",
             "Message sur X (@faureolivier), 21 novembre 2026, 14:43, heure de Paris, en réponse à un reportage de franceinfo sur une nouvelle colonie près de Jéricho. « obstruction » et « complicité » sont ses mots. i24NEWS écrit qu'il accuse le RN et Renaissance d'obstruction parlementaire ; la réponse de ces groupes n'est pas citée dans ces pages.",
             X_FAURE, G, "gaza"),
        ],
        [step("2026-11-19", "Proposition de loi sur les implantations",
              "Le texte, inscrit à la journée réservée aux socialistes, n'est pas voté avant minuit.",
              U_I24_FAURE, "i24NEWS")],
    )
    person(
        "rima-hassan", "Rima Hassan",
        "Députée européenne (LFI) (compte X officiel, 22 novembre 2026)",
        "Députée européenne de La France insoumise, membre de la commission des affaires étrangères et des droits humains (présentation de son compte X). Pas de photo libre : monogramme.",
        "Responsables politiques", "Parlementaires & élus", ("gaza",),
        [
            ("Le génocide à Gaza c'est : • 74 702 Palestiniens tués par Israël depuis octobre 2023 • 176 105 Palestiniens blessés par Israël depuis octobre 2023 • 1 613 Palestiniens tués par Israël depuis l'accord d'octobre 2025",
             "2026-11-22",
             "Message sur X (@RimaHas), 22 novembre 2026, 13:02, heure de Paris : début de la liste, qui se poursuit avec des chiffres sur les blessés, l'insécurité alimentaire et les destructions. « génocide » est son mot. Les chiffres sont ceux du message, qui n'en donne pas la source.",
             X_HASSAN, G, "gaza"),
        ],
        [step("2026-11-22", "Message sur Gaza",
              "Sur X, elle publie une liste de chiffres sur les morts, les blessés et les destructions à Gaza.",
              X_HASSAN, "X (@RimaHas)")],
    )

    # --- Gauche face au RN ---
    person(
        "francois-ruffin", "François Ruffin",
        "Député de la Somme (JDD, 22 novembre 2026)",
        "Député de la Somme, ancien proche de Jean-Luc Mélenchon, avec qui il a rompu en 2024 (JDD). Le 21 novembre 2026, il retire sa candidature à la présidentielle de 2027 ; le JDD écrit qu'il justifie ce retrait en estimant que le Rassemblement national est « aux portes du pouvoir ». Pas de photo libre : monogramme.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("« Vous allez vous faire avoir ! » Avec Debout!, nous lançons une campagne contre le Rassemblement national. Pour démasquer l'aRNaque sociale de Marine Le Pen. Sur l'économie, le social, c'est Macron avec un autre visage !",
             "2026-11-22",
             "Message sur X (@Francois_Ruffin), 22 novembre 2026, 22:26, heure de Paris, avec une vidéo et le lien de la campagne de son mouvement Debout!.",
             X_RUFFIN, F, "france"),
        ],
        [step("2026-11-21", "Retrait de la présidentielle",
              "Il retire sa candidature à la présidentielle de 2027 et ne soutient aucun candidat ; il dit le RN « aux portes du pouvoir ».",
              U_JDD_RUFFIN, "JDD")],
    )
    person(
        "manon-aubry", "Manon Aubry",
        "Députée européenne (LFI) (compte X officiel, 22 novembre 2026)",
        "Députée européenne de La France insoumise, présidente du groupe de la Gauche au Parlement européen (présentation de son compte X). Pas de photo libre : monogramme.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("Je confronte Agnès Panier-Runacher sur la responsabilité des macronistes dans la montée de l'extrême droite. Ils ont fait voter la loi asile-immigration Ils entretiennent la confusion entre musulmans & islamistes Ils s'attaquent à l'Etat de droit Les conséquences sont terribles",
             "2026-11-22",
             "Message sur X (@ManonAubryFr), 22 novembre 2026, 12:00, heure de Paris, avec l'extrait d'un débat face à Agnès Pannier-Runacher (orthographe du message conservée). C'est son jugement sur les macronistes ; la réponse d'Agnès Pannier-Runacher n'est pas reprise ici.",
             X_AUBRY, F, "france"),
        ],
        [step("2026-11-22", "Débat face à Agnès Pannier-Runacher",
              "Sur X, elle publie l'extrait d'un débat sur la responsabilité des macronistes dans la montée de l'extrême droite.",
              X_AUBRY, "X (@ManonAubryFr)")],
    )
    person(
        "segolene-royal", "Ségolène Royal",
        "Ancienne ministre socialiste (CNews, 23 novembre 2026)",
        "Ancienne ministre socialiste (CNews). Le 22 novembre 2026, sur LCI, elle dit craindre des violences racistes en cas de victoire du RN ; d'autres invités du plateau la contredisent (CNews). Pas de photo libre : monogramme.",
        "Responsables politiques", "Gouvernement & exécutif", ("france",),
        [
            ("les gens d'extrême droite vont tuer des noirs et tuer des arabes",
             "2026-11-22",
             "LCI, 22 novembre 2026, cité par CNews le 23 novembre 2026. La phrase est reproduite telle que cette page la publie ; d'autres médias rapportent une formulation voisine. Selon CNews, elle parlait d'une victoire du RN à la présidentielle et prenait l'exemple de crimes racistes de ces dernières années ; les autres invités l'ont contredite et elle n'est pas revenue sur ses propos. Réaction du journaliste Raphaël Stainville sur sa fiche.",
             U_CNEWS_ROYAL, F, "france"),
        ],
        [step("2026-11-22", "Propos sur LCI",
              "Sur LCI, elle dit craindre des violences racistes en cas de victoire du RN ; d'autres invités la contredisent.",
              U_CNEWS_ROYAL, "CNews")],
    )
    add("raphael-stainville", [
        ("On est là dans du pur délire",
         "2026-11-23",
         "CNews, La Matinale, 23 novembre 2026 (message du compte @CNEWS reproduit dans l'article). Il réagit aux propos de Ségolène Royal sur LCI la veille. Il ajoute : « C'est une vision apocalyptique et délirante ».",
         U_CNEWS_ROYAL, NU, "france"),
    ])

    # --- RN ---
    add("julien-odoul", [
        ("« Raciste », « xénophobe » : les accusations fusent dès qu'on évoque la priorité nationale. J'ai rappelé à @LeaBalage que la proposition du RN se fonde sur la nationalité, non sur l'origine ou la couleur de peau !",
         "2026-11-22",
         "Message sur X (@JulienOdoul), 22 novembre 2026, 23:33, heure de Paris, avec l'extrait d'un débat sur BFMTV face à la députée écologiste Léa Balage El Mariky. Les mots « raciste » et « xénophobe » sont ceux qu'il dit avoir entendus ; la réponse de la députée n'est pas reprise ici.",
         X_ODOUL, F, "france"),
    ])
    person(
        "philippe-ballard", "Philippe Ballard",
        "Député RN de l'Oise, porte-parole du RN (TF1 Info, 23 novembre 2026)",
        "Député du Rassemblement national (Oise) et porte-parole du parti. Le 23 novembre 2026, sur TF1, il dit que le RN votera la règle d'or budgétiaire qu'Emmanuel Macron envisage d'inscrire dans la Constitution. Pas de photo libre : monogramme.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("On le votera bien sûr. On va regarder le texte précisément, mais le principe nous convient très, très bien",
             "2026-11-23",
             "Bonjour ! La Matinale TF1, 23 novembre 2026, cité par le direct de TF1 Info. Il parle de la règle d'or budgétaire qu'Emmanuel Macron envisage d'inscrire dans la Constitution en janvier ; la page écrit que cette règle est réclamée par Marine Le Pen et Jordan Bardella.",
             U_TF1_BALLARD, F, "france"),
        ],
        [step("2026-11-23", "Règle d'or budgétaire",
              "Sur TF1, il annonce que le RN votera la règle d'or envisagée par Emmanuel Macron.",
              U_TF1_BALLARD, "TF1 Info")],
    )

    # --- Reconquête ---
    add("eric-zemmour", [
        ("Défendre le droit du peuple français à rester majoritaire sur sa terre, ce n'est pas une faute, c'est un devoir, c'est moral, c'est beau et c'est juste",
         "2026-11-21",
         "Meeting de Toulon, 21 novembre 2026, cité par le JDD le 22 novembre 2026. Le JDD écrit qu'il y a « invoqué ses thèmes de prédilection : l'identité et l'immigration ».",
         U_JDD_ZEM, F, "france"),
    ])
    add("sarah-knafo", [
        ("On a tous les moyens de l'emporter, je pense qu'elle doit avoir lieu",
         "2026-11-23",
         PRIMAIRE + "RTL Matin, 23 novembre 2026. Elle parle de la primaire de la droite, avec Éric Zemmour. Elle ajoute : « Il n'est absolument pas question de se retirer ». Le baromètre Toluna Harris Interactive pour RTL, M6 et L'Express crédite Éric Zemmour de 3 à 4 % des intentions de vote, selon la page.",
         U_RTL_KNAFO, F, "france"),
    ])

    # --- Liens ---
    add_link("francois-ruffin", "rn",
             "le 22/11/2026, il lance avec Debout! une campagne contre le Rassemblement national",
             X_RUFFIN, "2026-11-22", "france", "opposition")
    add_link("olivier-faure", "rn",
             "le 21/11/2026, il reproche au RN et à Renaissance leur « obstruction » sur sa proposition de loi sur les implantations israéliennes",
             X_FAURE, "2026-11-21", "gaza", "opposition")
    add_link("raphael-stainville", "segolene-royal",
             "le 23/11/2026 sur CNews, il qualifie ses propos sur LCI de « pur délire »",
             U_CNEWS_ROYAL, "2026-11-23", "france", "autre")
    add_link("philippe-ballard", "rn",
             "porte-parole du RN (TF1 Info, 23/11/2026)",
             U_TF1_BALLARD, "2026-11-23", "france", "ascension")
