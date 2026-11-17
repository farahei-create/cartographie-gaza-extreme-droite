# -*- coding: utf-8 -*-
"""v46 : 17 novembre 2026.
Phrases lues le jour même sur les pages citées.
Les crochets [ ] et les points de suspension entre parenthèses sont ceux des sources.
« ramassis », « tri », « ségrégation », « délirant », « coup d'arrêt », « assécher » sont les mots des personnes."""

G = "Gaza – déclarations"
F = "France – normalisation de l'extrême droite"
NU = "Nuance / contexte"

U_FI = "https://www.franceinfo.fr/elections/marine-le-pen-critiquee-en-plein-debat-de-la-presidentielle-pour-sa-volonte-de-couper-les-subventions-des-associations-politisees_8285558.html"
U_LCP = "https://lcp.fr/actualites/logement-associations-jeunesse-ce-qu-il-faut-retenir-du-debat-presidentiel-sur-lci"
U_HUFF = "https://www.huffingtonpost.fr/politique/article/au-debat-de-tf1-lci-marine-le-pen-en-grande-difficulte-sur-le-financement-des-associations_359471.html"
U_F24 = "https://www.france24.com/fr/info-en-continu/20261116-imp%C3%B4ts-logement-smic-ce-qu-il-faut-retenir-du-d%C3%A9bat-entre-candidats-%C3%A0-la-pr%C3%A9sidentielle"
U_INT = "https://www.linternaute.com/actualite/politique/11314631-debat-presidentiel-du-16-novembre-pouvoir-d-achat-logement-etudiants-les-annonces-de-melenchon-et-le-pen/"
U_TF1 = "https://www.tf1info.fr/replay-lci/videos/video-elue-presidente-que-ferait-marine-le-pen-avec-la-ligue-des-droits-de-l-homme-17197-2476252.html"
U_I24 = "https://www.i24news.tv/fr/actu/france/artc-antisemitisme-melenchon-denonce-un-sondage-bidon-arfi-l-accuse-de-complotisme"
U_E1A = "https://www.europe1.fr/societe/mon-objectif-est-de-mettre-un-coup-darret-a-limmigration-affirme-le-depute-epr-charles-rodwell-1237257"
U_E1B = "https://www.europe1.fr/societe/reprendre-le-controle-charles-rodwell-propose-de-retablir-le-ministere-de-limmigration-et-de-lidentite-nationale-1237329"
U_CNEWS = "https://www.cnews.fr/france/2026-11-16/cnews-fait-partie-de-la-liberte-et-de-la-diversite-de-la-presse-considere-bruno"

VID_LDH = {"url": U_TF1, "platform": "tf1info.fr",
           "title": "Élue présidente, que ferait Marine Le Pen avec la Ligue des droits de l'Homme ?",
           "source": "LCI / TF1 Info (site officiel)"}

DEB = ("Débat LCI « Quelle société pour demain ? », 16 novembre 2026, "
       "entrepôt des Restos du Cœur, avec Gabriel Attal, Raphaël Glucksmann, "
       "Marine Le Pen, Jean-Luc Mélenchon et Bruno Retailleau. ")


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

    def person(pid, name, role, desc, cat, sub, secs, statements, steps):
        add_node(pid, name, "person", role, desc, [], cat, sub, secs)
        add(pid, statements)
        by[pid]["parcours"] = steps

    add("marine-le-pen", [
        ("Il y a 15 à 16% d'étrangers dans les logements sociaux, ça fait donc 800 000 logements. Il ne s'agit pas de les expulser, mais qu'il y ait un accès prioritaire quand les logements sont disponibles",
         "2026-11-16",
         DEB + "L'Internaute, 16 novembre 2026, 23 h 42. La page écrit qu'elle s'est dite favorable à une priorité nationale dans l'accès aux logements sociaux, puis donne cette phrase.",
         U_INT, F, "france"),
        ("Le logement social a été construit avec les efforts de nos parents, de nos grands-parents, de nos arrière-grands-parents",
         "2026-11-16",
         DEB + "LCP, article du 17 novembre 2026 à 0 h 43. LCP écrit qu'elle a « justifié » ainsi une priorité d'accès aux Français. La formule « priorité d'accès aux Français dans [l'accessibilité au] logement social » contient des crochets de LCP : elle n'est pas reprise comme citation.",
         U_LCP, F, "france"),
        ("Ça ne veut pas dire une exclusivité, ça veut dire une priorité",
         "2026-11-16",
         DEB + "LCP, 17 novembre 2026. LCP écrit qu'elle a « complété » ainsi la phrase sur le logement social.",
         U_LCP, F, "france"),
        ("Moi je pique pas les logements des gens",
         "2026-11-16",
         DEB + "France 24, dépêche du 16 novembre 2026 à 23 h 39, mise à jour le 17 novembre à 0 h 18. La page écrit qu'elle répond cela à Jean-Luc Mélenchon, qui souhaite que les préfets réquisitionnent les logements vides, et qu'elle appelle à utiliser les bureaux vides pour loger des étudiants. Cette dernière formule n'est pas entre guillemets.",
         U_F24, F, "france"),
        ("ramassis de gauchistes",
         "2026-11-16",
         DEB + "franceinfo, 17 novembre 2026, 0 h. La page écrit qu'elle a « qualifié la Ligue des Droits de l'Homme » de ces mots, alors que Raphaël Glucksmann lui demandait des exemples d'associations « politisées », et s'il rangeait le Planning familial parmi elles. Extrait officiel LCI / TF1 Info.",
         U_FI, F, "france", VID_LDH),
        ("A partir du moment où une association vient dire 'il faut voter untel, il ne faut pas voter untel', elle fait de la politique. Si c'est comme ça, et bien dans ces cas-là, il faut qu'elle se constitue en parti politique",
         "2026-11-16",
         DEB + "franceinfo, 17 novembre 2026. Les apostrophes intérieures sont celles de la page. La page place cette phrase juste après « ramassis de gauchistes ».",
         U_FI, F, "france"),
        ("Une association qui fait de la politique c'est un parti politique. Les associations doivent être apolitiques. Si elles sont associatives, elles touchent des subventions publiques. C'est le respect dû aux Français qu'elles respectent leur caractère apolitique",
         "2026-11-16",
         DEB + "L'Internaute, 16 novembre 2026. La page écrit qu'elle a dit ne plus vouloir d'associations « politiques », puis donne cette phrase.",
         U_INT, F, "france"),
        ("Nous allons arrêter de subventionner les associations politisées",
         "2026-11-16",
         DEB + "LCP, 17 novembre 2026. LCP écrit qu'elle a répondu cela « sans vouloir donner de noms », après la question de Gabriel Attal sur Hayange et Beaucaire. franceinfo retient, le même soir, la formule plus courte « arrêter de subventionner les associations politisées ».",
         U_LCP, F, "france"),
        ("Il n'est pas question de toucher à l'ensemble des dispositifs existants qui permettent aux Restos du cœur de remplir ce rôle essentiel",
         "2026-11-16",
         DEB + "LCP, 17 novembre 2026. LCP écrit qu'elle a « assuré » cela au sujet des Restos du Cœur, avant l'échange sur les associations qu'elle dit « politisées ».",
         U_LCP, NU, "france"),
        ("Moi, je suis dans mon rôle politique, je présente une vision politique, je fais des choix politiques et il y a un monde associatif qui n'a pas précisément à faire de choix politiques",
         "2026-11-16",
         DEB + "Le HuffPost, 16 novembre 2026. La page écrit qu'elle répond cela à Raphaël Glucksmann, après avoir cité son projet de priorité nationale pour le logement social, et qu'elle assure ne rien reprocher aux associations d'aide sociale.",
         U_HUFF, F, "france"),
        ("violente à l'égard de la police et des institutions",
         "2026-11-16",
         DEB + "Page vidéo LCI / TF1 Info, 16 novembre 2026, 22 h 30. La page écrit qu'interrogée par Gilles Bouleau sur le financement de la Ligue des droits de l'Homme, elle « dénonce une association » en ces mots. L'extrait est celui du diffuseur.",
         U_TF1, F, "france", VID_LDH),
    ])

    add("gabriel-attal", [
        ("A Hayange, le maire du Rassemblement national a coupé l'électricité et le gaz au Secours populaire et c'est la justice qui a dû obliger la ville à remettre l'électricité et le gaz au Secours populaire",
         "2026-11-16",
         DEB + "franceinfo, 17 novembre 2026. Il ne nomme pas le maire. La page ne cite pas de réponse de Marine Le Pen sur ce point. Jean-Luc Mélenchon dit « Ça c'est vrai » et Raphaël Glucksmann « C'est totalement vrai », phrases reprises plus bas. LCP formule autrement la question d'Attal, sans la phrase sur la justice : « Pourquoi vous ne parlez pas de Hayange où le maire a coupé l'électricité et le gaz au Secours populaire ? De Beaucaire, où la mairie RN a supprimé du soutien à des associations d'aide aux devoirs ? »",
         U_FI, F, "france"),
        ("En gros, si vous arrivez au pouvoir, il y aura les associations qui seront au garde-à-vous derrière vous, qui pourront être soutenues et il y aura toutes les autres qui verront leur financement retiré",
         "2026-11-16",
         DEB + "franceinfo, 17 novembre 2026. La page écrit qu'il « a dénoncé » cela, après avoir rappelé que le programme du RN parle de baisser les subventions aux associations « ne relevant pas de l'intérêt général », pour 3,7 milliards d'euros par an. Ce chiffre est celui de la page, pas une phrase distincte de lui.",
         U_FI, F, "france"),
        ("Les seules déclarations que vous avez faites, c'est que vous avez dit ce sera les associations qui accompagnent les migrants et des associations type Ligue des droits de l'homme",
         "2026-11-16",
         DEB + "Le HuffPost, 16 novembre 2026. La page écrit qu'il « conteste » ainsi, en s'adressant à Marine Le Pen, et qu'il estime que ces structures ne représentent qu'un milliard d'euros.",
         U_HUFF, F, "france"),
        ("Où est-ce que vous trouvez les 3 milliards ?",
         "2026-11-16",
         DEB + "Le HuffPost, 16 novembre 2026. La page place cette question juste après le milliard d'euros qu'il attribue aux associations qu'il vient de nommer, face à l'économie de 3,7 milliards avancée pour le projet du RN.",
         U_HUFF, F, "france"),
        ("fait de travailler, notamment pour les services publics",
         "2026-11-16",
         DEB + "LCP, 17 novembre 2026. LCP écrit qu'il souhaite donner une priorité, dans les critères d'attribution des logements sociaux, au « fait de travailler, notamment pour les services publics », en s'opposant à la proposition de Marine Le Pen.",
         U_LCP, F, "france"),
    ])

    add("raphael-glucksmann", [
        ("Vous proposez le tri dans le logement social !",
         "2026-11-16",
         DEB + "LCP, 17 novembre 2026. LCP écrit qu'il a « répliqué » cela à Marine Le Pen.",
         U_LCP, F, "france"),
        ("un tri entre les Français qui ont de l'argent et ceux qui n'en ont pas",
         "2026-11-16",
         DEB + "LCP, 17 novembre 2026. LCP rattache ce membre de phrase à « l'abolition de la loi SRU », qu'il présente comme « un autre tri ». France 24 retient, le même soir, la formule plus courte « Une politique de ségrégation ».",
         U_LCP, F, "france"),
        ("une politique de ségrégation spatiale, géographique",
         "2026-11-16",
         DEB + "LCP, 17 novembre 2026. Même passage que le « tri » et la loi SRU.",
         U_LCP, F, "france"),
        ("Si vous êtes au pouvoir, vous allez décider que telle ou telle association est politique",
         "2026-11-16",
         DEB + "Le HuffPost, 16 novembre 2026. La page écrit qu'il « s'inquiète », puis qu'il prend l'exemple d'organisations qui s'opposeraient à des lois jugées xénophobes. Le mot « xénophobes » est celui de la page, dans le récit de son exemple, pas une citation séparée.",
         U_HUFF, F, "france"),
        ("Ça donne un pouvoir à l'État complètement délirant",
         "2026-11-16",
         DEB + "Le HuffPost, 16 novembre 2026. France 24 retient le même soir « complètement délirant » pour ce qu'il dit du pouvoir que le critère donnerait à l'État.",
         U_HUFF, F, "france"),
        ("C'est totalement vrai",
         "2026-11-16",
         DEB + "franceinfo, 17 novembre 2026. La page écrit qu'il a « abondé » ainsi après la phrase de Gabriel Attal sur Hayange, le Secours populaire, et la justice. Il ne nomme personne.",
         U_FI, F, "france"),
    ])

    add("jean-luc-melenchon", [
        ("Il ne peut pas y avoir de tri entre les populations à loger, (...) les enfants de l'un sont les enfants de tout le monde",
         "2026-11-16",
         DEB + "LCP, 17 novembre 2026. Les points de suspension entre parenthèses sont ceux de LCP. La page écrit qu'il a « commenté » ainsi la priorité nationale de Marine Le Pen.",
         U_LCP, F, "france"),
        ("C'est les communes qui décident",
         "2026-11-16",
         DEB + "Le HuffPost, 16 novembre 2026. La page écrit qu'il « rappelle » cela, pour contester qu'un gouvernement décide quelles associations financent selon leurs prises de position.",
         U_HUFF, F, "france"),
        ("Maintenant vous prétendez savoir mieux que les conseils municipaux. Alors pourquoi les élire ?",
         "2026-11-16",
         DEB + "Le HuffPost, 16 novembre 2026. La page écrit qu'il s'adresse ainsi à Marine Le Pen, dans la même intervention.",
         U_HUFF, F, "france"),
        ("Ça c'est vrai",
         "2026-11-16",
         DEB + "franceinfo, 17 novembre 2026. La page écrit qu'il a « soutenu » ainsi la phrase de Gabriel Attal sur Hayange et le Secours populaire. Il ne nomme personne.",
         U_FI, F, "france"),
        ("Après avoir assimilé la condamnation du génocide à de l'antisémitisme, les responsables de cette ignominie continuent avec une opération coordonnée",
         "2026-11-16",
         "i24NEWS, 16 novembre 2026, citant son message sur X. La page écrit qu'il conteste l'enquête Ifop pour l'AJC et la Fondapol. La suite mise entre guillemets par i24NEWS, « la Une et [un] papier abject dans Le Parisien », contient des crochets du média : elle n'est pas reprise. i24NEWS écrit aussi qu'il dénonce un « sondage bidon » et une émission sur France 5.",
         U_I24, G, "gaza"),
        ("sondage bidon",
         "2026-11-16",
         "i24NEWS, 16 novembre 2026. La page isole ces deux mots comme les siens, à propos de l'enquête Ifop de l'AJC. Le message original sur X n'a pas été rouvert : la page d'i24NEWS est la source lue.",
         U_I24, G, "gaza"),
        ("La gravité irresponsable d'un tel comportement échappe à ses auteurs. Mais personne ne doit l'oublier",
         "2026-11-16",
         "i24NEWS, 16 novembre 2026. La page écrit qu'il a « ajouté » cela après la phrase sur l'« opération coordonnée ».",
         U_I24, G, "gaza"),
    ])

    add("bruno-retailleau", [
        ("Priorité au travail",
         "2026-11-16",
         DEB + "LCP, 17 novembre 2026. LCP écrit : « Priorité au travail », également pour Bruno Retailleau, après la phrase de Gabriel Attal sur le « fait de travailler » dans l'attribution des logements sociaux, face à la priorité nationale de Marine Le Pen.",
         U_LCP, F, "france"),
    ])

    add("yonathan-arfi", [
        ("M. Mélenchon, le problème n'est pas un sondage qui vous incrimine ou un débat sur l'antisémitisme de LFI. Le problème c'est vous : vos mots, vos silences, vos menaces",
         "2026-11-16",
         "i24NEWS, 16 novembre 2026. La page le présente comme président du CRIF et écrit qu'il a répondu sur X au message de Jean-Luc Mélenchon sur l'enquête de l'AJC. Une autre phrase de la même réponse, dans le même article, n'est pas reprise.",
         U_I24, F, "france"),
        ("Comme toujours, quand Jean-Luc Mélenchon est accusé de nourrir l'antisémitisme, il répond par des intimidations et par le complot",
         "2026-11-16",
         "i24NEWS, 16 novembre 2026. La page écrit qu'il a « poursuivi » ainsi.",
         U_I24, F, "france"),
        ("Expliquer les accusations par un complot des médias ne sera jamais un démenti à votre antisémitisme, cela en est au contraire l'illustration.",
         "2026-11-16",
         "i24NEWS, 16 novembre 2026. La page écrit qu'il a « conclu » ainsi. Le point final est celui de la page.",
         U_I24, F, "france"),
    ])

    add("charles-rodwell", [
        ("Mon objectif, il est assez clair, il est de mettre un coup d'arrêt à l'immigration",
         "2026-11-16",
         "Europe 1 matin, 16 novembre 2026, au micro de Dimitri Pavlenko. La page le présente comme député EPR des Yvelines. La phrase du 15 novembre déjà en ligne, « Il faut diviser les entrées par quatre », n'est pas recopiée.",
         U_E1A, F, "france"),
        ("insoutenables pour notre pays",
         "2026-11-16",
         "Europe 1, 16 novembre 2026. La page écrit qu'il estime que les flux migratoires ont atteint des niveaux « insoutenables pour notre pays », notamment pour les services publics.",
         U_E1A, F, "france"),
        ("massivement réduite, choisie pour répondre aux besoins de notre économie et nos entreprises",
         "2026-11-16",
         "Europe 1, 16 novembre 2026. La page écrit qu'il propose que l'immigration en France devienne une immigration de travail en ces mots.",
         U_E1A, F, "france"),
        ("réduire ou assécher toutes les autres voies d'immigration",
         "2026-11-16",
         "Europe 1, 16 novembre 2026. La page écrit qu'il « ajoute » cela après « On organise l'immigration économique pour répondre spécifiquement à nos besoins ».",
         U_E1A, F, "france"),
        ("Je propose de rétablir le ministère de l'immigration. Et de l'identité nationale",
         "2026-11-16",
         "Europe 1, 16 novembre 2026, 11 h 18. La page écrit qu'il ajoute cela au micro de Dimitri Pavlenko, avec l'objectif d'avoir « une personne politiquement en charge de reprendre le contrôle de toute notre politique » migratoire. La même page cite aussi : « Je propose une réforme de la Constitution ».",
         U_E1B, F, "france"),
        ("des quotas drastiques pour répondre à ces besoins, aux besoins de notre économie",
         "2026-11-16",
         "Europe 1, 16 novembre 2026. La page écrit qu'il propose des quotas migratoires fixés tous les trois ans, par une loi de programmation à l'Assemblée nationale, afin de « définir à la fois nos besoins et des quotas drastiques » en ces mots.",
         U_E1B, F, "france"),
        ("avait vu juste en 2007 en voulant mettre un pilote dans l'avion pour piloter toute notre immigration",
         "2026-11-16",
         "Europe 1, 16 novembre 2026. La page écrit que, selon lui, Nicolas Sarkozy « avait vu juste en 2007 » en ces mots. C'est son jugement, pas une phrase de Nicolas Sarkozy.",
         U_E1B, F, "france"),
    ])

    person(
        "bruno-le-maire", "Bruno Le Maire",
        "Ancien ministre de l'Économie et des Finances (CNews, 16 novembre 2026)",
        "Le 16 novembre 2026, dans La Grande Interview sur CNews, il dit que la chaîne fait partie de la liberté et de la diversité de la presse. Pas de photo libre : monogramme.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("CNEWS fait partie de la liberté et de la diversité de la presse",
             "2026-11-16",
             "CNews, La Grande Interview, 16 novembre 2026, 8 h 35. La page reprend cette phrase et le présente comme ancien ministre de l'Économie et des Finances. Elle ne cite pas d'autre phrase.",
             U_CNEWS, F, "france"),
        ],
        [step("2026-11-16", "CNews, La Grande Interview",
              "Il dit sur CNews que la chaîne fait partie de la liberté et de la diversité de la presse.",
              U_CNEWS, "CNews")],
    )

    add_link("gabriel-attal", "marine-le-pen",
             "au débat LCI du 16/11/2026, il lui oppose le maire RN d'Hayange et le Secours populaire, et dit que les associations « au garde-à-vous » seraient les seules soutenues",
             U_FI, "2026-11-16", "france", "opposition")
    add_link("raphael-glucksmann", "marine-le-pen",
             "au débat LCI du 16/11/2026, il lui répond « Vous proposez le tri dans le logement social ! » et parle d'une « politique de ségrégation spatiale, géographique »",
             U_LCP, "2026-11-16", "france", "opposition")
    add_link("jean-luc-melenchon", "marine-le-pen",
             "au débat LCI du 16/11/2026, il lui dit : « Maintenant vous prétendez savoir mieux que les conseils municipaux. Alors pourquoi les élire ? »",
             U_HUFF, "2026-11-16", "france", "opposition")
    add_link("jean-luc-melenchon", "ajc",
             "le 16/11/2026, i24NEWS cite son message : il parle d'une « opération coordonnée » après l'enquête Ifop de l'AJC, et d'un « sondage bidon »",
             U_I24, "2026-11-16", "gaza", "opposition")
    add_link("yonathan-arfi", "jean-luc-melenchon",
             "le 16/11/2026, i24NEWS cite sa réponse : « Le problème c'est vous : vos mots, vos silences, vos menaces »",
             U_I24, "2026-11-16", "france", "opposition")
    add_link("charles-rodwell", "nicolas-sarkozy",
             "le 16/11/2026 sur Europe 1, il dit que Nicolas Sarkozy « avait vu juste en 2007 » en voulant un ministère de l'Immigration",
             U_E1B, "2026-11-16", "france", "autre")
    add_link("bruno-le-maire", "cnews",
             "le 16/11/2026, dans La Grande Interview, il dit que CNews fait partie de la liberté et de la diversité de la presse",
             U_CNEWS, "2026-11-16", "france", "autre")
