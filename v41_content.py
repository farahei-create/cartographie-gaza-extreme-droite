# -*- coding: utf-8 -*-
"""v41 : mise à jour du 14 novembre 2026 (période du 11 au 14 novembre).
Chaque phrase a été lue dans la page indiquée (HTTP 200) le 14 novembre 2026.
Les messages X de Jean-Luc Mélenchon et de Jean-Noël Barrot ont été lus en entier
(texte long) sur leurs comptes ; franceinfo et LCP en citent les mêmes mots.
Le contexte, les nuances et les réponses lus dans la même page sont dans « medium »."""

G = "Gaza – déclarations"
F = "France – normalisation de l'extrême droite"
NU = "Nuance / contexte"

U_FI_BAN = "https://www.franceinfo.fr/politique/la-france-insoumise/israel-interdit-a-jean-luc-melenchon-et-mathilde-panot-l-entree-sur-son-territoire-denoncant-la-position-extremement-anti-israelienne-de-la-france-insoumise_8279801.html"
U_FI_JLM_VID = "https://www.franceinfo.fr/monde/israel/je-regrette-que-le-gouvernement-d-israel-me-poursuive-de-cette-maniere-denonce-jean-luc-melenchon-interdit-de-territoire-en-israel_8279831.html"
U_X_JLM = "https://x.com/JLMelenchon/status/2120932595126894785"
U_X_BARROT = "https://x.com/jnbarrot/status/2120953009983127868"
U_LCP_BARROT = "https://lcp.fr/actualites/israel-interdit-son-territoire-a-jean-luc-melenchon-la-reponse-cinglante-du-gouvernement"
U_BFM_ZEM = "https://www.bfmtv.com/politique/les-republicains/video-je-serai-ravi-d-etre-candidat-dans-cette-primaire-declare-eric-zemmour-candidat-reconquete-a-la-presidentielle-au-salon-made-in-france_VN-202611130526.html"
U_AFP_PRIMAIRE = "https://www.boursorama.com/actualite-economique/actualites/primaire-a-droite-zemmour-espere-y-participer-mais-attal-ne-veut-pas-40598195eed5b0dd0bb42f30821bddf8"
U_CNEWS_PRIMAIRE = "https://www.cnews.fr/france/2026-11-13/presidentielle-2027-eric-zemmour-espere-participer-une-primaire-de-la-droite-et"
U_SUDRADIO_MM = "https://www.sudradio.fr/sud-radio/marion-marechal-eric-zemmour-devrait-rejoindre-et-soutenir-marine-le-pen"
U_TF1_TONDELIER = "https://www.tf1info.fr/justice-faits-divers/attentat-de-trappes-le-rn-va-porter-plainte-contre-tondelier-pour-diffamation-2475583.html"
U_BFM_TONDELIER = "https://www.bfmtv.com/politique/elections/presidentielle/marine-tondelier-accusee-de-diffamation-par-le-rn-apres-des-propos-sur-le-suspect-de-l-attentat-des-yvelines-se-dit-extremement-sereine_AV-202611120933.html"
U_FI_STERIN = "https://www.franceinfo.fr/societe/justice/pierre-edouard-sterin-milliardaire-proche-de-l-extreme-droite-sera-juge-en-janvier-pour-son-refus-de-venir-devant-les-deputes_8280011.html"
U_LCP_STERIN = "https://lcp.fr/actualites/le-milliardaire-pierre-edouard-sterin-juge-en-janvier-pour-avoir-seche-plusieurs"

NEW_URLS = [U_FI_BAN, U_FI_JLM_VID, U_X_JLM, U_X_BARROT, U_LCP_BARROT, U_BFM_ZEM, U_AFP_PRIMAIRE,
            U_CNEWS_PRIMAIRE, U_SUDRADIO_MM, U_TF1_TONDELIER, U_BFM_TONDELIER, U_FI_STERIN, U_LCP_STERIN]


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

    # Jean-Luc Mélenchon, interdit d'entrée en Israël (12 novembre 2026)
    ctx_ban = ("Le 12 novembre 2026, le ministère israélien des Affaires étrangères a annoncé interdire l'entrée sur son territoire "
               "à Jean-Luc Mélenchon et à Mathilde Panot, « compte tenu des positions anti-israéliennes virulentes du parti La France Insoumise (LFI) "
               "et des propos scandaleux tenus par ses dirigeants » ; selon son communiqué, « Tous deux ont tenu des propos relayant des calomnies sanglantes à l'encontre d'Israël », "
               "et Jean-Luc Mélenchon a « appelé à ce que des navires français escortent des flottilles illégales vers Gaza » (franceinfo). "
               "Israël rejette fermement l'accusation de « génocide » (franceinfo).")
    add("jean-luc-melenchon", [
        ("Si nous arrivons au pouvoir, nous dirons ce que nous aurons à dire. À savoir : dénoncer le génocide à Gaza, la colonisation en Cisjordanie et l'annexion progressive du Sud-Liban et du plateau du Golan.",
         "2026-11-12",
         "Message sur X (@JLMelenchon), 12 novembre 2026, 17:31 UTC, qui commence par : « Israël m'interdit d'entrer sur son territoire ? Je n'ai pas demandé à y entrer. » et se termine par : « Refuser la loi du plus fort ou du plus fou et respecter, en toutes circonstances, le droit international : telle est notre ligne politique. » LCP cite le même message. " + ctx_ban,
         U_X_JLM, G, "gaza"),
        ("On m'interdit d'entrer sur un territoire où je n'ai pas demandé à entrer. […] Je regrette que le gouvernement d'Israël me poursuive de cette manière",
         "2026-11-12",
         "franceinfo, journée spéciale « Nos services publics », 12 novembre 2026, cité par franceinfo. Il écarte toute « normalisation » avec le gouvernement israélien s'il est élu : « On dira ce qu'on a à dire, on le dira franchement. » Dans la vidéo de franceinfo, il ajoute : « L'ambassadeur, ici, à Paris a dit qu'il préférait qu'on élise n'importe qui plutôt que moi, bon, dont acte, chacun ses goûts ». " + ctx_ban,
         U_FI_BAN, G, "gaza",
         {"url": U_FI_JLM_VID, "platform": "franceinfo.fr",
          "title": "« Je regrette que le gouvernement d'Israël me poursuive de cette manière », dénonce Jean-Luc Mélenchon",
          "source": "franceinfo (site officiel)"}),
    ])

    # Jean-Noël Barrot, ministre des Affaires étrangères (nouvelle fiche)
    add_node(
        "jean-noel-barrot", "Jean-Noël Barrot", "person",
        "Ministre des Affaires étrangères (selon franceinfo et LCP, 12 novembre 2026)",
        "Chef de la diplomatie française. Le 12 novembre 2026, il réagit sur X à la décision d'Israël d'interdire l'entrée sur son territoire à Jean-Luc Mélenchon et à Mathilde Panot (franceinfo, LCP).",
        [st("Cette décision démagogique, émanant d'un gouvernement qui a multiplié les violations du droit international, fait le jeu de ceux qui, comme La France insoumise, vivent de l'instrumentalisation du conflit israélo-palestinien.",
            "2026-11-12",
            "Message sur X (@jnbarrot), 12 novembre 2026, 18:52 UTC. Il commence par : « Le gouvernement d'affaires courantes de Benyamin Netanyahou vient d'interdire l'accès à son territoire à des responsables de la France insoumise. » et se termine par : « La France continuera inlassablement à agir pour la solution à deux États et la coexistence pacifique des peuples israélien et palestinien. » franceinfo et LCP citent le même message. Le ministère israélien des Affaires étrangères justifie sa décision par les « positions anti-israéliennes virulentes » de LFI (franceinfo).",
            U_X_BARROT, G, "gaza")],
        "Responsables politiques", "Gouvernement & exécutif", ("gaza",))
    by["jean-noel-barrot"]["parcours"] = [
        step("2026-11-12", "Ministre des Affaires étrangères",
             "franceinfo le présente comme « le chef de la diplomatie française » et « ministre des Affaires étrangères » en rapportant sa réaction à l'interdiction d'entrée en Israël visant Jean-Luc Mélenchon et Mathilde Panot.",
             U_FI_BAN, "franceinfo"),
    ]

    # Éric Zemmour et la primaire de la droite et du centre (13 novembre 2026)
    add("eric-zemmour", [
        ("Tous ces gens-là se retrouvent entre eux. Je suis assez déçu. Je vois que c'est la reconstitution de LR et la reconstitution du bloc central. J'espère me tromper et j'espère que Monsieur Lisnard résistera à cette pression de ses amis de LR et qu'il imposera la présence de reconquête",
         "2026-11-13",
         "Salon du Made in France (Paris), 13 novembre 2026, vidéo BFMTV. Selon BFMTV, les directeurs de campagne de Gabriel Attal, Bruno Retailleau et David Lisnard doivent se réunir le 17 novembre au sujet d'une primaire de la droite et du centre, à laquelle Édouard Philippe s'oppose. Selon l'AFP, il juge « curieux » que Gabriel Attal y participe ; celui-ci a refusé qu'il y soit intégré (fiche Gabriel Attal).",
         U_BFM_ZEM, F, "france",
         {"url": U_BFM_ZEM, "platform": "bfmtv.com",
          "title": "« Je serai ravi d'être candidat dans cette primaire », déclare Éric Zemmour au salon Made in France",
          "source": "BFMTV (site officiel)"}),
    ])
    add("gabriel-attal", [
        ("certainement pas [à] servir de marche-pied à l'extrême droite dont M. Zemmour est un représentant",
         "2026-11-13",
         "Propos tenus au Salon du Made in France (Paris), 13 novembre 2026, cités par l'AFP (dépêche reprise par Boursorama ; CNews publie la même phrase). Selon l'AFP, il refuse qu'Éric Zemmour soit intégré à la primaire de la droite et du centre, qui vise selon lui à « empêcher un deuxième tour entre les extrêmes ». Éric Zemmour, de son côté, a dit souhaiter y participer et qualifié Gabriel Attal de « militant socialiste ». Les crochets signalent un mot ajouté par l'AFP.",
         U_AFP_PRIMAIRE, F, "france"),
    ])
    add_link("gabriel-attal", "eric-zemmour",
             "refuse qu'Éric Zemmour participe à la primaire de la droite et du centre (13/11/2026, AFP)",
             U_AFP_PRIMAIRE, "2026-11-13", "france", "opposition")

    # Marion Maréchal, Sud Radio (11 novembre 2026)
    add("marion-marechal", [
        ("Quand on voit la menace — on en a longuement parlé aujourd'hui — que représente l'extrême gauche française, je pense qu'on n'a pas le droit de se disperser et qu'aujourd'hui le rempart le plus efficace et le mieux placé pour éviter à tout prix une victoire de Jean-Luc Mélenchon, que ce soit à la présidentielle ou aux législatives, c'est de se rassembler autour de Marine Le Pen.",
         "2026-11-11",
         "Invitée de Jacques Cardoze dans « Le Grand Matin » de Sud Radio, 11 novembre 2026 (retranscription publiée par Sud Radio). Interrogée sur la candidature d'Éric Zemmour, elle répond qu'elle ne fera pas campagne pour lui : « je soutiens Marine Le Pen évidemment à l'heure où je vous parle, les députés que j'ai à l'Assemblée nationale sont alliés au groupe du Rassemblement national ». Elle dit ne plus avoir « de contact humain » avec lui, la rupture ayant été « assez violente ».",
         U_SUDRADIO_MM, F, "france"),
    ])

    # Attentat de Trappes : le RN annonce une plainte en diffamation contre Marine Tondelier (12 novembre 2026)
    ctx_trappes = ("Selon l'AFP (TF1 Info), Marine Tondelier avait déclaré la semaine précédente sur BFMTV que le tireur de l'attentat raciste "
                   "du 23 octobre 2026 à Trappes et La Verrière « avait chez lui des tracts d'un parti politique qui peut arriver au pouvoir » ; "
                   "il s'agissait, selon l'AFP, d'autocollants « Vive la France, RN, fier d'être français » qu'il avait lui-même fait fabriquer. "
                   "Le suspect est présumé innocent ; il n'est pas nommé ici.")
    add("marine-tondelier", [
        ("Je ne dis pas que c'est un membre actif du RN qui, au nom de Marine Le Pen, a été assassiner des gens dans les rues […] je dis juste qu'il y a quand même une remise en question à avoir [pour] des mots qu'on prononce sur les plateaux, qui précèdent des actes et qui peuvent être parfois des munitions",
         "2026-11-12",
         "BFMTV (« Vous présidente »), 12 novembre 2026, cité par TF1 Info avec l'AFP ; les crochets signalent un mot ajouté par l'AFP. Elle se dit « extrêmement sereine » face à la plainte en diffamation annoncée par le RN, « habituée des menaces de procédures-bâillons ». Le RN lui reproche d'avoir affirmé que le tireur avait « tué au nom du RN » et annonce une plainte « très prochainement » (porte-parole Andréa Kotarac). " + ctx_trappes,
         U_TF1_TONDELIER, F, "france"),
    ])
    add("rn", [
        ("On engagera une procédure judiciaire contre Mme Tondelier",
         "2026-11-12",
         "Andréa Kotarac, porte-parole de Marine Le Pen, sur franceinfo le 12 novembre 2026, cité par TF1 Info avec l'AFP. Il reproche à Marine Tondelier d'avoir « expliqué que le tireur aurait tué au nom du RN », dit que le RN « ne laissera pas passer » et se dit prêt à « débattre avec la gauche […] jamais sur la base de fake news ». Interrogé par l'AFP, il indique que la plainte en diffamation sera déposée « très prochainement » : à cette date, les articles lus ne disent pas qu'elle a été déposée. Marine Tondelier se dit « extrêmement sereine » (BFMTV). " + ctx_trappes,
         U_TF1_TONDELIER, F, "france"),
    ])
    add_link("rn", "marine-tondelier",
             "annonce d'une plainte en diffamation après ses propos sur l'attentat de Trappes (12/11/2026 ; « très prochainement », selon le porte-parole de Marine Le Pen)",
             U_TF1_TONDELIER, "2026-11-12", "france", "opposition")

    # Pierre-Édouard Stérin cité devant le tribunal correctionnel (annoncé le 12 novembre 2026)
    add_steps("pierre-edouard-sterin", [
        step("2026-11-12", "Cité devant le tribunal correctionnel",
             "Selon le parquet de Paris, sollicité par l'AFP, une citation lui a été « délivrée à M. Pierre-Edouard Stérin pour comparaître à l'audience du 19 janvier 2027 devant la 10e chambre du tribunal correctionnel de Paris pour non-comparution devant une commission d'enquête parlementaire » : il avait refusé de se rendre aux convocations de la commission d'enquête de l'Assemblée nationale sur « l'organisation des élections en France » en 2025 (deux refus, les 14 et 20 mai 2025, selon franceinfo ; trois, entre avril et mai 2025, selon LCP). LCP rapporte qu'il avait invoqué à l'époque des menaces pour sa sécurité et demandé une audition en visioconférence. Il n'a pas été jugé : il est présumé innocent.",
             U_FI_STERIN, "franceinfo (AFP) ; LCP"),
    ])
