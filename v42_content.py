# -*- coding: utf-8 -*-
"""v42 : mise à jour du 16 novembre 2026 (période du 14 au 16 novembre).
Chaque phrase a été lue dans la page indiquée le 16 novembre 2026.
Les crochets [ ] sont ceux de la source, pas les nôtres.
Le contexte et la réponse lus dans les mêmes pages sont dans « medium »."""

F = "France – normalisation de l'extrême droite"
NU = "Nuance / contexte"

U_BFM_ROUS = "https://www.bfmtv.com/politique/elections/presidentielle/presidentielle-sandrine-rousseau-appelle-les-ecologistes-a-rejoindre-la-dynamique-de-jean-luc-melenchon-et-marine-tondelier-a-se-retirer_AV-202611150255.html"
U_BFM_VID = "https://www.bfmtv.com/replay-emissions/bfm-politique/video-invitee-sandrine-rousseau_VN-202611150243.html"
U_TF1 = "https://www.tf1info.fr/politique/elections/presidentielle/presidentielle-2027-sandrine-rousseau-appelle-marine-tondelier-a-retirer-sa-candidature-2475969.html"
U_LP = "https://www.leparisien.fr/politique/presidentielle-2027-rousseau-appelle-les-ecologistes-a-se-rallier-a-lfi-pour-la-presidentielle-tondelier-denonce-une-provocation-15-11-2026-D3HHDNGM5VEQ7JDCSCYCXE6XA4.php"
U_BFM_PORT = "https://www.bfmtv.com/politique/elections/presidentielle/video-teddy-riner-credite-de-4-5-des-intentions-de-vote-dans-un-sondage-ce-qui-est-tres-inquietant-au-dela-des-personnes-c-est-surtout-que-les-deux-extremes-sont-en-train-d-arriver-au-second-tour-declare-florence-portelli-vice-presidente-des-lr_VN-202611140375.html"

VID_ROUS = {"url": U_BFM_VID, "platform": "bfmtv.com",
            "title": "Sandrine Rousseau, invitée de BFM Politique",
            "source": "BFMTV (site officiel)"}
VID_PORT = {"url": U_BFM_PORT, "platform": "bfmtv.com",
            "title": "Florence Portelli sur un sondage pour 2027",
            "source": "BFMTV (site officiel)"}


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

    def add_link(src, tgt, rel, url, date, section, nature):
        for e in E:
            if e["source"] == src and e["target"] == tgt and e.get("url") == url:
                return
        link(src, tgt, rel, url, date)
        E[-1]["section"] = section
        E[-1]["nature"] = nature

    ctx_ton = ("Le soir même, sur franceinfo, Marine Tondelier répond. Le Parisien cite ses mots : Sandrine Rousseau « cherche la provocation », "
               "« Tout ça est n'importe quoi », « la question sera tranchée, c'est mon engagement, c'est ce qu'on a toujours dit », "
               "et « Les options sur lesquelles nous voterons seront détaillées à la fin du mois de novembre ». "
               "Le vote interne des Écologistes est prévu du 10 au 13 décembre (BFMTV).")

    add_node(
        "sandrine-rousseau", "Sandrine Rousseau", "person",
        "Députée Les Écologistes de Paris (BFMTV, 15 novembre 2026)",
        "Députée. Le 15 novembre 2026, sur BFMTV, elle parle d'un second tour avec Marine Le Pen et appelle son parti à « rejoindre la dynamique » de Jean-Luc Mélenchon. Marine Tondelier répond le soir même sur franceinfo (Le Parisien).",
        [st("Présentez-moi un seul candidat qui aujourd'hui n'est pas battu au second tour par Marine Le Pen. La question qui va se poser au second tour c'est ce que va faire le bloc central",
            "2026-11-15",
            "BFM Politique, BFMTV, 15 novembre 2026. Elle ajoute : « Si le bloc central ne voit pas la différence entre les deux, alors, ce sera le moment de vérité, les masques vont tomber. » "
            "BFMTV écrit qu'elle déplore le « jeu extrêmement dangereux » de représentants du bloc central « en mettant un signe égal » entre LFI et le RN. "
            "Elle dit aussi : « cette candidature écologiste qui fait 3% doit alimenter une dynamique plus large » et « Ça pourrait être les pourcents qui manquent à la gauche pour accéder au second tour. » "
            "TF1 Info, sur le même entretien, cite le sondage Elabe du 14 novembre : la candidate écologiste est créditée de 3 à 3,5 %. " + ctx_ton,
            U_BFM_ROUS, F, "france"),
         st("Je dis que dans un moment comme celui-ci, il nous faut une ligne politique, nous sommes un parti politique, avec la montée du fascisme, nous ne pouvons pas nous exonérer d'avoir un débat sur la ligne politique au-delà des négociations [pour la présidentielle]",
            "2026-11-15",
            "BFM Politique, BFMTV, 15 novembre 2026. Les crochets sont ceux de BFMTV. La formule « montée du fascisme » est la sienne. " + ctx_ton,
            U_BFM_ROUS, F, "france"),
         st("J'appelle mon parti à rejoindre la dynamique de Jean-Luc Mélenchon, et la rejoindre très tôt, pour que nous ne soyons pas dans une démarche politique de négociation de place mais que nous soyons vraiment dans l'appui à une ligne politique",
            "2026-11-15",
            "BFM Politique, 15 novembre 2026, cité par TF1 Info. Sur son parrainage à Marine Tondelier, elle dit : « Je ne le donnerai pas ». Elle l'appelle « absolument » à retirer sa candidature « le plus rapidement possible » et ajoute : « Je la qualifierais même de dangereuse si elle se maintient ». "
            "Le même article rappelle que Marine Tondelier avait déclaré le 9 novembre sur TF1 : « Je ne me désisterai pas, je ne disparaîtrai pas comme ça d'un coup de l'élection présidentielle ». " + ctx_ton,
            U_TF1, F, "france")],
        "Responsables politiques", "Parlementaires & élus", ("france",))
    by["sandrine-rousseau"]["statements"][0]["video"] = VID_ROUS
    by["sandrine-rousseau"]["parcours"] = [
        step("2026-11-15", "Députée Les Écologistes de Paris",
             "BFMTV la présente comme « députée écologiste de Paris » et « députée Les Écologistes de Paris » en rapportant son entretien du 15 novembre 2026.",
             U_BFM_ROUS, "BFMTV"),
    ]

    add("marine-tondelier", [
        ("J'en ai aussi un peu ras-le-bol que, dans des moments aussi difficiles que le nôtre, on se permette parler à tort et à travers en son nom propre, et jamais au nom du collectif. C'est un peu facile, et ça abîme beaucoup le collectif et l'exercice compliqué qu'on est en train de mener",
         "2026-11-15",
         "franceinfo, 15 novembre 2026 au soir, cité par Le Parisien, au sujet de Sandrine Rousseau. La phrase est reproduite telle que Le Parisien l'imprime. "
         "Le Parisien cite aussi : elle dit que Sandrine Rousseau « cherche la provocation », « Tout ça est n'importe quoi », « la question sera tranchée, c'est mon engagement, c'est ce qu'on a toujours dit », "
         "et « Les options sur lesquelles nous voterons seront détaillées à la fin du mois de novembre ». "
         "Le journal écrit qu'un sondage publié la veille attribue à Marine Le Pen entre 31 et 33 % au premier tour, et à Jean-Luc Mélenchon 18,5 % si Marine Tondelier et François Ruffin ne se présentent pas (3,5 % et 3 % sinon).",
         U_LP, NU, "france"),
    ])

    add_link("sandrine-rousseau", "marine-tondelier",
             "appelle Marine Tondelier à retirer sa candidature et dit qu'elle ne lui donnera pas son parrainage (15/11/2026, TF1 Info)",
             U_TF1, "2026-11-15", "france", "opposition")
    add_link("sandrine-rousseau", "jean-luc-melenchon",
             "appelle son parti à rejoindre la dynamique de Jean-Luc Mélenchon (15/11/2026, TF1 Info)",
             U_TF1, "2026-11-15", "france", "autre")

    add_node(
        "florence-portelli", "Florence Portelli", "person",
        "Vice-présidente des Républicains (BFMTV, 14 novembre 2026)",
        "Le 14 novembre 2026, BFMTV publie une vidéo où elle commente un sondage d'intentions de vote pour 2027. La chaîne attribue la phrase au titre de la page.",
        [st("Ce qui est très inquiétant au-delà des personnes, c'est surtout que les deux extrêmes sont en train d'arriver au second tour",
            "2026-11-14",
            "BFMTV, vidéo du 14 novembre 2026. La phrase figure dans le titre de la page, introduite par « déclare Florence Portelli, vice-présidente des LR ». "
            "« Les deux extrêmes » est sa formulation. Le 15 novembre, Le Parisien écrit qu'un sondage publié la veille attribue à Marine Le Pen entre 31 et 33 % des voix au premier tour, "
            "et à Jean-Luc Mélenchon 18,5 % dans l'hypothèse où Marine Tondelier et François Ruffin ne se présentent pas.",
            U_BFM_PORT, F, "france")],
        "Responsables politiques", "Partis & dirigeants de parti", ("france",))
    by["florence-portelli"]["statements"][0]["video"] = VID_PORT
    by["florence-portelli"]["parcours"] = [
        step("2026-11-14", "Vice-présidente des Républicains",
             "BFMTV la présente comme « vice-présidente des LR » dans le titre de la vidéo du 14 novembre 2026.",
             U_BFM_PORT, "BFMTV"),
    ]
