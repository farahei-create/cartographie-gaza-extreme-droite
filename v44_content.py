# -*- coding: utf-8 -*-
"""v44 : relevé X du 13 au 16 novembre 2026.
Textes repris des posts lus via l'API X (heure de Paris).
Un post de média n'est gardé que pour la phrase qu'il met entre guillemets,
attribuée à la personne, pas à la chaîne.
Les posts déjà en ligne (v42, v43) ne sont pas repris."""

G = "Gaza – déclarations"
F = "France – normalisation de l'extrême droite"

X_RET = "https://x.com/BrunoRetailleau/status/2121155423986180396"
X_ROUSSEL = "https://x.com/Fabien_Roussel/status/2121252617825247563"
X_LEJEUNE = "https://x.com/GeoffroyLejeune/status/2121194259273404891"
X_GW1 = "https://x.com/GWGoldnadel/status/2121531263739650356"
X_GW2 = "https://x.com/GWGoldnadel/status/2121560184262644212"
X_GW3 = "https://x.com/GWGoldnadel/status/2121585507683676406"
X_GW4 = "https://x.com/GWGoldnadel/status/2121615782786347335"
X_GW5 = "https://x.com/GWGoldnadel/status/2121665837933134334"
X_GW6 = "https://x.com/GWGoldnadel/status/2121880947985399877"
X_GW7 = "https://x.com/GWGoldnadel/status/2122100789132894676"
X_RIOUFOL = "https://x.com/ivanrioufol/status/2121298910794903629"
X_JLM = "https://x.com/JLMelenchon/status/2121632985321496587"
X_GALLOU = "https://x.com/jylgallou/status/2122102144966742481"
X_BARD_DUO = "https://x.com/J_Bardella/status/2121334296170406348"
X_LEVY = "https://x.com/ELevyCauseur/status/2122028803845140813"
X_MLP_LOG = "https://x.com/MLP_officiel/status/2122030794189181288"
X_MLP_APL = "https://x.com/MLP_officiel/status/2122031802550202623"
X_MLP_DBL = "https://x.com/MLP_officiel/status/2122036013514301653"
X_CNEWS_INTIM = "https://x.com/CNEWS/status/2121274837750493202"
X_LCI_CRIT = "https://x.com/LCI/status/2121241582527508582"
X_TOND = "https://x.com/marinetondelier/status/2122043729414357402"
X_MM = "https://x.com/MarionMarechal/status/2122105573546050039"
X_CIOTTI = "https://x.com/eciotti/status/2121687539006292151"
X_ZEM = "https://x.com/ZemmourEric/status/2122064723352924442"
X_JDD_ZEM = "https://x.com/leJDD/status/2121828049071050926"
X_TORRES = "https://x.com/CNEWS/status/2122095908103823377"
X_RN_DUO = "https://x.com/RNational_off/status/2121334707958972554"
X_RN_FRONT = "https://x.com/RNational_off/status/2121639292699357568"
X_BFM_ZAHAB = "https://x.com/BFMTV/status/2121288509818314754"
X_PANOT1 = "https://x.com/MathildePanot/status/2121273706924175854"
X_PANOT2 = "https://x.com/MathildePanot/status/2121941033516757057"
X_ODOUL = "https://x.com/JulienOdoul/status/2121994894306693279"
X_PHIL = "https://x.com/f_philippot/status/2121956505607966852"
X_BOMP_NICE = "https://x.com/mbompard/status/2121728155857613159"
X_BOMP_CNEWS = "https://x.com/mbompard/status/2121983554024362492"
X_NDA = "https://x.com/dupontaignan/status/2121601389662994662"
X_ONFRAY = "https://x.com/CNEWS/status/2121586073255960975"
X_MONT_STAT = "https://x.com/CNEWS/status/2121917876747801077"
X_MONT_VOTE = "https://x.com/CNEWS/status/2121921263283122358"
X_MONT_E1 = "https://x.com/Europe1/status/2121916128335135196"
X_JADOT = "https://x.com/BFMTV/status/2122094349211030011"
X_RIDEL = "https://x.com/Europe1/status/2121654530647445944"
X_ALLONCLE = "https://x.com/LCI/status/2122062419409199467"
X_RODWELL = "https://x.com/leJDD/status/2121847705613844851"
X_STAIN1 = "https://x.com/CNEWS/status/2121265949558895065"
X_STAIN2 = "https://x.com/CNEWS/status/2121269070070952381"
X_CHENU = "https://x.com/sebchenu/status/2121923164955668823"
X_LCI_MANIF = "https://x.com/LCI/status/2121320381986304467"
X_LCI_CTRL = "https://x.com/LCI/status/2121320672756375683"
X_LCI_TRAPPES = "https://x.com/LCI/status/2121323705137573988"
X_LCI_COUPLE = "https://x.com/LCI/status/2121334968567619659"
X_LCI_MACRO = "https://x.com/LCI/status/2121339447790678133"

NOTE = (" Texte du post lu via l'API X, heure de Paris. Le post s'arrête à la limite des 280 caractères lorsqu'il est incomplet.")


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

    # Comptes officiels déjà sur le site
    add("bruno-retailleau", [
        ("Il y a trop d’immigration en France. Pour reprendre le contrôle de notre politique migratoire, je donnerai la parole aux Français par référendum.",
         "2026-11-13",
         "Message sur X (@BrunoRetailleau), 13 novembre 2026, 9:17, heure de Paris. Le même jour, sur France 2, il développe ces propositions (fiche, entretien des 4V).",
         X_RET, F, "france"),
    ])
    add("fabien-roussel", [
        ("Le Rassemblement National est un poison contre le peuple.\n\nIls veulent couper dans le budget des services publics et ils sont contre le logement social.\n\nLeur projet, c’est fracturer la société, défendre le secteur privé et nous diviser en fonction de nos origines.",
         "2026-11-13",
         "Message sur X (@Fabien_Roussel), 13 novembre 2026, 15:43, heure de Paris. Compte non certifié dans le relevé ; c’est le compte public du secrétaire national du PCF.",
         X_ROUSSEL, F, "france"),
    ])
    add("geoffroy-lejeune", [
        ("J’aime beaucoup Tibo InShape, que je trouve courageux et positif. Mais il y a une erreur dans son analyse : le sujet n’est pas de savoir si les musulmans ont le droit de porter le voile. Le sujet, c’est de savoir si le voile est français.",
         "2026-11-13",
         "Message sur X (@GeoffroyLejeune), 13 novembre 2026, 11:51, heure de Paris. Compte non certifié dans le relevé ; c’est le compte public du directeur du JDD.",
         X_LEJEUNE, F, "france"),
    ])
    add("gilles-william-goldnadel", [
        ("Le vice président de la fac de Versailles hospitalisé après une attaque  au couteau ! Ni à 9 h ni à 10 h sur @franceinter pas 1 mot sur l’affaire . Les violences contre les profs , ils s’en tapent. Mais apologie d’une pièce sur Gaza . Radio France Insoumise en roue libre .",
         "2026-11-14",
         "Message sur X (@GWGoldnadel), 14 novembre 2026, 10:10, heure de Paris. Il ne nomme pas la victime.",
         X_GW1, G, "gaza"),
        ("Moi cette déclaration ne me choque pas , j’affirme simplement que l’assimilation de St Denis au Congo aurait permis à l’extrême gauche de terroriser intellectuellement C News injustement.",
         "2026-11-14",
         "Réponse sur X (@GWGoldnadel), 14 novembre 2026, 12:05, heure de Paris.",
         X_GW2, F, "france"),
        ("Voilà ce que tweeta le petit député du Parti Antisémite le jour du massacre islamiste du 13 novembre. On ne les méprisera jamais assez .",
         "2026-11-14",
         "Message sur X (@GWGoldnadel), 14 novembre 2026, 13:46, heure de Paris. « Parti Antisémite » est sa formule. Il ne nomme pas le député dans ce texte. Le message cité n’est pas recopié ici.",
         X_GW3, F, "france"),
        ("Rien à faire , la radio de sévices publics continue de dire le RN « d’extrême droite » et LFI  , parti antisémite , « radicale » ou « de gauche » . Malhonnête. Insupportable. Dégueulasse . Stupide. J’oubliais stupidement que @franceinter est radicalement d’extrême gauche.",
         "2026-11-14",
         "Message sur X (@GWGoldnadel), 14 novembre 2026, 15:46, heure de Paris.",
         X_GW4, F, "france"),
        ("Le désespoir de Gal Gadot est mien . Pas seulement la tristesse. Mais la rage devant l’injustice mensongère. Je publie le 2 décembre « Vérités sur le Mensonge » . Parmi tous ceux que je raconte, celui sur Gaza qui n’est plus un faux victorieux mais un vil fantasme qui a triomphé.",
         "2026-11-14",
         "Message sur X (@GWGoldnadel), 14 novembre 2026, 19:05, heure de Paris.",
         X_GW5, G, "gaza"),
        ("Encore un festival de sottise anti française ce dimanche sur @franceinter de Nora Hamadi, admiratrice de Rima Hassan. Les français sont racistes : MLP , Ciotti, Macron etc.. C’est raciste d’évoquer les immigrés. Sauf qu’elle se présente comme franco- algérienne . Le seul exemple",
         "2026-11-15",
         "Message sur X (@GWGoldnadel), 15 novembre 2026, 9:20, heure de Paris. Le post est coupé à 280 caractères." + NOTE,
         X_GW6, F, "france"),
        ("Dans « Vérités sur le Mensonge » à paraître le 2 décembre, j’écris qu’Amnesty s’est déshonorée en donnant mille exemples . Voila qu’elle honore Francesca Albanese qui a défendu le Grand Muphti allié de Hitler et raconte qu’Israel fait violer des femmes par des chiens. INDIGNE.",
         "2026-11-15",
         "Message sur X (@GWGoldnadel), 15 novembre 2026, 23:53, heure de Paris. Ce sont ses mots sur Amnesty International et Francesca Albanese.",
         X_GW7, G, "gaza"),
    ])
    add("jean-luc-melenchon", [
        ("Désolant. France inter tient une tranchée absurde contre la cause palestinienne en interdisant d'antenne le magnifique livre de Rima Hassan. \n\nPour l'honneur de l'esprit, pour l'honneur des Français, Viviant démissionne. Respect. \n\nLe moment venu, par les urnes, la résistance",
         "2026-11-14",
         "Message sur X (@JLMelenchon), 14 novembre 2026, 16:54, heure de Paris. Le post est coupé à 280 caractères. Il écrit « Viviant »." + NOTE,
         X_JLM, G, "gaza"),
    ])
    add("jordan-bardella", [
        ("Avec Marine Le Pen, on est riches de nos complémentarités.\n\nIl y a une relation de confiance très forte, qui sera, demain, un véritable atout, lorsque nous aurons peut-être la responsabilité immense de devoir servir le pays.",
         "2026-11-13",
         "Message sur X (@J_Bardella), 13 novembre 2026, 21:08, heure de Paris.",
         X_BARD_DUO, F, "france"),
        ("Nous souhaitons qu’il ait, sur le modèle du traitement des hooligans dans le football, des interdictions de manifester pour les individus violents qui sont fichés pour leur atteinte à la sûreté de l’État",
         "2026-11-13",
         "LCI, 13 novembre 2026, 20:12, heure de Paris. Phrase entre guillemets dans le post de @LCI, attribuée à Jordan Bardella, président du RN.",
         X_LCI_MANIF, F, "france"),
        ("Depuis maintenant plusieurs semaines, les Français le voient bien, le gouvernement est en train de perdre le contrôle sur la situation sécuritaire du pays",
         "2026-11-13",
         "LCI, 13 novembre 2026, 20:13, heure de Paris. Phrase entre guillemets dans le post de @LCI.",
         X_LCI_CTRL, F, "france"),
        ("On est là face à un individu qui a commis un acte raciste, ignoble, qui doit être condamné très fermement. (…) La place de cet individu est d’entrer en prison sans la possibilité d’en sortir un jour",
         "2026-11-13",
         "LCI, 13 novembre 2026, 20:25, heure de Paris, sur l’attentat de Trappes. Phrase entre guillemets dans le post de @LCI. Il ne nomme pas le suspect. La personne mise en cause reste présumée innocente : cette phrase est la sienne, pas un jugement.",
         X_LCI_TRAPPES, F, "france"),
        ("On a une relation qui est très fluide, qui est extrêmement naturelle et je pense que demain nous sommes les seuls à pouvoir assumer ce couple exécutif avec un tel niveau de confiance",
         "2026-11-13",
         "LCI, 13 novembre 2026, 21:10, heure de Paris, à propos de Marine Le Pen. Phrase entre guillemets dans le post de @LCI.",
         X_LCI_COUPLE, F, "france"),
        ("C'est bien, les macronistes se réveillent. (…) Ils ont gouverné comme des socialistes depuis dix ans, et à trois mois des élections, parce que c'est populaire et qu'on est donné gagnant, il faut parler comme le Rassemblement national",
         "2026-11-13",
         "LCI, 13 novembre 2026, 21:28, heure de Paris, rubrique « Immigration » du post de @LCI. Les parenthèses et points de suspension sont dans le post.",
         X_LCI_MACRO, F, "france"),
    ])
    add("elisabeth-levy", [
        ("Depuis des semaines, les insoumis ciblent les chaînes d’information, les accusant de racisme, ce qui, n’en déplaise à monsieur Mélenchon, est une insulte. Samedi à Lyon, un caméraman-pigiste travaillant pour BFM a été roué de coups en marge d’une manifestation. Sans agents de",
         "2026-11-15",
         "Message sur X (@ELevyCauseur), 15 novembre 2026, 19:07, heure de Paris. Le post est coupé à 280 caractères. Elle ne nomme pas le caméraman." + NOTE,
         X_LEVY, F, "france"),
    ])
    add("marine-le-pen", [
        ("Je demande que Jean-Luc Mélenchon demande à ses troupes de laisser les autres candidats faire campagne sans faire l'objet d'intimidations",
         "2026-11-13",
         "CNews, émission Punchline WE, 13 novembre 2026, 17:11, heure de Paris. Phrase entre guillemets dans le post de @CNEWS. BFMTV et Frontières publient la même demande le même jour.",
         X_CNEWS_INTIM, F, "france"),
        ("Ils n'arrivent même pas à se mettre d'accord sur les critères pour choisir un seul candidat. Partant de là, c'est pas moi qui vais régler leurs problèmes",
         "2026-11-13",
         "LCI, salon du Made in France, 13 novembre 2026, 14:59, heure de Paris. Phrase entre guillemets dans le post de @LCI, sur les candidats de la droite et du centre.",
         X_LCI_CRIT, F, "france"),
        ("Nous considérons que les Français doivent être prioritaires dans l’accès à un certain nombre de prestations sociales. C’est le cas du logement social.\n\nCes logements ont été payés par les parents, les grands-parents des Français. C’est normal qu’ils soient premiers servis chez",
         "2026-11-15",
         "Message sur X (@MLP_officiel), 15 novembre 2026, 19:15, heure de Paris. Le post est coupé à 280 caractères." + NOTE,
         X_MLP_LOG, F, "france"),
        ("Nous ne sommes pas contre les APL, nous souhaitons simplement les réserver aux Français et à ceux qui sont étrangers et qui ont travaillé cinq ans  équivalent temps plein en France.\n\nLe coût du logement étudiant est souvent insurmontable pour beaucoup de parents.",
         "2026-11-15",
         "Message sur X (@MLP_officiel), 15 novembre 2026, 19:19, heure de Paris.",
         X_MLP_APL, F, "france"),
        ("J’ai longtemps proposé l’interdiction de la double nationalité. Je pense que j’ai commis une erreur.\n\nJ’ai laissé penser à ceux qui ont la double nationalité que je nourrissais à leur égard une forme de suspicion. Il n’y a aucune raison d’avoir la moindre suspicion.",
         "2026-11-15",
         "Message sur X (@MLP_officiel), 15 novembre 2026, 19:36, heure de Paris. Elle revient ici sur une proposition antérieure.",
         X_MLP_DBL, F, "france"),
    ])
    add("marine-tondelier", [
        ("Emmanuel Macron avait promis d'être l'antidote au vote d'extrême droite.\n\nDeux quinquennats plus tard, elle n'a jamais été aussi haute.\n\nEt si elle arrive au pouvoir, elle pourra même profiter de certaines des dispositions qu'il a fait voter pour s'en prendre à l'opposition.",
         "2026-11-15",
         "Message sur X (@marinetondelier), 15 novembre 2026, 20:07, heure de Paris. « Elle » désigne, dans son texte, l’extrême droite.",
         X_TOND, F, "france"),
    ])
    add("marion-marechal", [
        ("À Marseille, une quinzaine d’individus cagoulés attaquent des militants du RN et de la Cocarde à coups de bouteille, causant 3 blessés.\n\nUn énième exemple de la violence décomplexée d’une ultra gauche encouragée par le laxisme judiciaire,  la bienveillance médiatique et la",
         "2026-11-16",
         "Message sur X (@MarionMarechal), 16 novembre 2026, 0:12, heure de Paris. Elle ne nomme aucun particulier. Le post est coupé à 280 caractères. BFMTV et CNews relatent les mêmes faits le 15 novembre, sans nommer les personnes." + NOTE,
         X_MM, F, "france"),
    ])
    add("eric-ciotti", [
        ("« one two three viva l’Algérie » scandé par des émeutiers à Lyon brandissant le drapeau algérien. \n\nNier le lien entre l’immigration et les émeutes est une faute et une folie",
         "2026-11-14",
         "Message sur X (@eciotti), 14 novembre 2026, 20:31, heure de Paris. Le slogan entre guillemets est celui qu’il dit avoir entendu ; la phrase sur l’immigration est la sienne.",
         X_CIOTTI, F, "france"),
    ])
    add("eric-zemmour", [
        ("Dans cette présidentielle, je suis le seul à proposer une politique d’immigration négative.\n\nLa Suède, l’une des plus vieilles démocraties du monde, réforme sa Constitution pour le faire. Nous devons faire de même en France.",
         "2026-11-15",
         "Message sur X (@ZemmourEric), 15 novembre 2026, 21:30, heure de Paris.",
         X_ZEM, F, "france"),
        ("Tout faire pour que notre avenir soit français",
         "2026-11-15",
         "Le JDD, entretien publié le 15 novembre 2026. Le post de @leJDD (5:50, heure de Paris) met la phrase entre guillemets : « Éric Zemmour au JDD : « Tout faire pour que notre avenir soit français » ».",
         X_JDD_ZEM, F, "france"),
    ])
    add("jules-torres", [
        ("S’il y a une chose qu’on ne peut pas enlever à Éric Zemmour, c’est que sur l’immigration, il a un programme",
         "2026-11-15",
         "CNews, « 100% Politique » week-end, 15 novembre 2026, 23:34, heure de Paris. Phrase entre guillemets dans le post de @CNEWS. Jules Torres est présenté comme journaliste au JDD.",
         X_TORRES, F, "france"),
    ])
    add("rn", [
        ("La confiance et l’amitié qui unissent @MLP_officiel et @J_Bardella constituent une véritable chance pour le redressement de la France.",
         "2026-11-13",
         "Message sur X (@RNational_off), 13 novembre 2026, 21:09, heure de Paris. La suite du post est coupée à 280 caractères.",
         X_RN_DUO, F, "france"),
        ("Remettre de l'ordre dans la rue, dans nos comptes publics et à nos frontières.",
         "2026-11-14",
         "Message sur X (@RNational_off), 14 novembre 2026, 17:20, heure de Paris, au sujet du livre de Jordan Bardella et de son déplacement à Saint-Savin.",
         X_RN_FRONT, F, "france"),
    ])
    add("gabriel-attal", [
        ("Monsieur Zemmour n'est pas invité dans cette primaire",
         "2026-11-13",
         "BFMTV, 13 novembre 2026, 18:06, heure de Paris. Phrase entre guillemets dans le post de @BFMTV, dite par Jad Zahab, présenté comme porte-parole de Gabriel Attal.",
         X_BFM_ZAHAB, F, "france"),
    ])
    add_link("gabriel-attal", "eric-zemmour",
             "son porte-parole Jad Zahab dit qu'Éric Zemmour n'est pas invité dans la primaire (13/11/2026, BFMTV)",
             X_BFM_ZAHAB, "2026-11-13", "france", "opposition")

    # Fiches nouvelles, sans photo libre : monogramme
    person(
        "mathilde-panot", "Mathilde Panot",
        "Députée, présidente du groupe La France insoumise à l'Assemblée nationale (X, 13 novembre 2026)",
        "Députée. Les 13 et 15 novembre 2026, elle publie sur X deux messages sur la Cisjordanie et sur un documentaire tourné dans l'armée israélienne.",
        "Responsables politiques", "Parlementaires & élus", ("gaza",),
        [
            ("Dimanche 15 novembre, Paris va abriter le salon de l’immobilier israélien Icube à Paris. Au programme : la promotion et la vente de biens dans des colonies en Cisjordanie.\n\nEn Cisjordanie, fin octobre, l’armée israélienne a forcé plus de 3 000 Palestiniens à quitter leur foyer à",
             "2026-11-13",
             "Message sur X (@MathildePanot), 13 novembre 2026, 17:07, heure de Paris. Le post est coupé à 280 caractères." + NOTE,
             X_PANOT1, G, "gaza"),
            ("Plus de 1,5 million de personne ont déjà vu le documentaire NAZA des réalisateurs israéliens Yuval Abraham et Rachel Szor. \n\nJe l’ai vu. Il est puissant, révoltant, glaçant et édifiant. Il donne à voir de l’intérieur de l’armée israélienne le processus de déshumanisation et la",
             "2026-11-15",
             "Message sur X (@MathildePanot), 15 novembre 2026, 13:19, heure de Paris. Le post est coupé à 280 caractères. « personne » est écrit ainsi dans le post." + NOTE,
             X_PANOT2, G, "gaza"),
        ],
        [step("2026-11-13", "Messages sur la Cisjordanie et Gaza",
              "Elle publie sur X un message sur le salon Icube et la vente de biens dans des colonies en Cisjordanie.",
              X_PANOT1, "X")],
    )
    person(
        "jean-yves-le-gallou", "Jean-Yves Le Gallou",
        "Essayiste, président de Polémia (X, 15 novembre 2026)",
        "Le 15 novembre 2026, il publie sur X un message sur la déchéance de nationalité en Suède et sur l’interdiction, selon lui, du débat sur la remigration en France.",
        "Intellectuels & essayistes", "Philosophes & essayistes", ("france",),
        [
            ("Pendant que la Suède agit pour déchoir de la nationalité suédoise les bi nationaux délinquants ou indélicats, en France les commissaires politiques de l’extrême gauche , du ministère de l’Interieur et des tribunaux administratifs interdisent tout débat sur la remigration au nom",
             "2026-11-15",
             "Message sur X (@jylgallou), 15 novembre 2026, 23:59, heure de Paris. Le post est coupé à 280 caractères." + NOTE,
             X_GALLOU, F, "france"),
        ],
        [step("2026-11-15", "Message sur la remigration",
              "Il publie sur X un message qui oppose une réforme suédoise de la nationalité à l’interdiction, selon lui, du débat sur la remigration en France.",
              X_GALLOU, "X")],
    )
    person(
        "julien-odoul", "Julien Odoul",
        "Député du Rassemblement national (X, 15 novembre 2026)",
        "Député RN. Le 15 novembre 2026, il demande sur X ce qu’il y a « d’extrême » chez Marine Le Pen.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("Si @Cyrilhanouna est partant mais cela ne répond pas à ma question. Qu’est-ce qu’il y a d’extrême chez @MLP_officiel ?",
             "2026-11-15",
             "Réponse sur X (@JulienOdoul), 15 novembre 2026, 16:53, heure de Paris.",
             X_ODOUL, F, "france"),
        ],
        [step("2026-11-15", "Question sur le mot « extrême »",
              "Dans une réponse sur X, il demande ce qu’il y a « d’extrême » chez Marine Le Pen.",
              X_ODOUL, "X")],
    )
    person(
        "florian-philippot", "Florian Philippot",
        "Président des Patriotes (X, 15 novembre 2026)",
        "Le 15 novembre 2026, il écrit sur X que son mouvement retire un drapeau européen à Paris.",
        "Responsables politiques", "Partis & dirigeants de parti", ("france",),
        [
            ("On se débarrasse du torchon bleu à étoiles en plein Paris, à l’appel des Patriotes !\n\nNotre drapeau c’est 🇫🇷 !\n\nÀ bas l’UE !\nFrexit !",
             "2026-11-15",
             "Message sur X (@f_philippot), 15 novembre 2026, 14:20, heure de Paris. Il présente ce geste comme celui de son mouvement, Les Patriotes.",
             X_PHIL, F, "france"),
        ],
        [step("2026-11-15", "Message sur un drapeau européen retiré",
              "Il écrit que Les Patriotes retirent un drapeau européen à Paris.",
              X_PHIL, "X")],
    )
    person(
        "ivan-rioufol", "Ivan Rioufol",
        "Éditorialiste (X, 13 novembre 2026)",
        "Le 13 novembre 2026, il précise sur X ce qu’il a dit de David Lisnard, de Sarah Knafo et d’Éric Zemmour.",
        "Journalistes & éditorialistes", "Journalistes & chroniqueurs", ("france",),
        [
            ("Je n'ai pas dit ce qui m'est attribué. J'ai soulevé une ambiguïté de @davidlisnard qui parle de rupture mais accepte une primaire avec le centre. J'ajoute : il pourrait personnaliser la synthèse \"Knafo-Zemmour\" mais il reste trop prudemment, pour l'instant, sur une jambe (Knafo).",
             "2026-11-13",
             "Réponse sur X (@ivanrioufol), 13 novembre 2026, 18:47, heure de Paris. Il dit que des propos lui ont été attribués à tort.",
             X_RIOUFOL, F, "france"),
        ],
        [step("2026-11-13", "Précision sur Lisnard, Knafo et Zemmour",
              "Il écrit sur X qu’il a soulevé une ambiguïté de David Lisnard sur une primaire avec le centre, et parle d’une « synthèse Knafo-Zemmour ».",
              X_RIOUFOL, "X")],
    )
    person(
        "manuel-bompard", "Manuel Bompard",
        "Député, coordinateur de La France insoumise (X, 14 novembre 2026)",
        "Député. Les 14 et 15 novembre 2026, il publie sur X deux messages, l’un sur des groupuscules à Nice, l’autre sur un reportage de CNews à Marseille.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("Des groupuscules d’extrême droite à Nice ont fait savoir que nous n’étions pas les bienvenus. \n\nVoilà la réponse du peuple niçois : nous sommes 3 000 ce soir !",
             "2026-11-14",
             "Message sur X (@mbompard), 14 novembre 2026, 23:13, heure de Paris. Le compte @FranceInsoumise publie le même soir un texte proche, qui ajoute : « En 2027, face à l’extrême droite, nous sommes le seul rempart. » Il ne nomme pas les groupuscules.",
             X_BOMP_NICE, F, "france"),
            ("Regardez comment @CNEWS a essayé de manipuler des commerçants marseillais pour servir leur propagande.\n\nEt regardez comment ils se sont fait avoir.",
             "2026-11-15",
             "Message sur X (@mbompard), 15 novembre 2026, 16:07, heure de Paris. Il ne nomme pas les commerçants.",
             X_BOMP_CNEWS, F, "france"),
        ],
        [step("2026-11-14", "Message sur des groupuscules à Nice",
              "Il écrit que des groupuscules d’extrême droite ont fait savoir que La France insoumise n’était pas la bienvenue à Nice, et annonce 3 000 personnes à un rassemblement.",
              X_BOMP_NICE, "X")],
    )
    person(
        "nicolas-dupont-aignan", "Nicolas Dupont-Aignan",
        "Président de Debout la France (X, 14 novembre 2026)",
        "Le 14 novembre 2026, il écrit sur X que Marine Le Pen a abandonné la sortie de l’Union européenne.",
        "Responsables politiques", "Partis & dirigeants de parti", ("france",),
        [
            ("L’oligarchie et les médias ont culpabilisé la classe politique pour qu’elle renonce à parler de la sortie de l’Union européenne. Marine Le Pen l’a abandonnée, Jean-Luc Mélenchon n’en parle même plus.",
             "2026-11-14",
             "Message sur X (@dupontaignan), 14 novembre 2026, 14:49, heure de Paris. La suite est coupée à 280 caractères." + NOTE,
             X_NDA, F, "france"),
        ],
        [step("2026-11-14", "Message sur la sortie de l’Union européenne",
              "Il écrit que Marine Le Pen a abandonné la sortie de l’Union européenne.",
              X_NDA, "X")],
    )
    person(
        "michel-onfray", "Michel Onfray",
        "Philosophe (CNews, 14 novembre 2026)",
        "Le 14 novembre 2026, CNews cite une phrase de lui sur Marine Le Pen et le Rassemblement national.",
        "Intellectuels & essayistes", "Philosophes & essayistes", ("france",),
        [
            ("Marine Le Pen n'est pas son père, le RN ce n'est plus le FN",
             "2026-11-14",
             "CNews, « Face à Michel Onfray », 14 novembre 2026, 13:48, heure de Paris. Phrase entre guillemets dans le post de @CNEWS. Il est présenté comme philosophe et essayiste.",
             X_ONFRAY, F, "france"),
        ],
        [step("2026-11-14", "Phrase citée par CNews",
              "CNews publie cette phrase, dite dans « Face à Michel Onfray ».",
              X_ONFRAY, "CNews")],
    )
    person(
        "thibault-de-montbrial", "Thibault de Montbrial",
        "Avocat, président du mouvement Concorde (CNews et Europe 1, 15 novembre 2026)",
        "Le 15 novembre 2026, CNews et Europe 1 citent des phrases de lui sur les étrangers et la violence, et sur un second tour entre Marine Le Pen et Jean-Luc Mélenchon.",
        "Responsables politiques", "Partis & dirigeants de parti", ("france",),
        [
            ("Statistiquement, il y a une surreprésentation des étrangers dans la violence",
             "2026-11-15",
             "CNews, 15 novembre 2026, 11:46, heure de Paris. Phrase entre guillemets dans le post de @CNEWS.",
             X_MONT_STAT, F, "france"),
            ("Il faut tout faire pour éviter que la France insoumise gagne l'élection présidentielle (...) Dans ce cas-là je voterais pour Marine Le Pen",
             "2026-11-15",
             "CNews, « Le Grand Rendez-vous », 15 novembre 2026, 12:00, heure de Paris. Phrase entre guillemets dans le post de @CNEWS. Il est présenté comme avocat et président du mouvement Concorde.",
             X_MONT_VOTE, F, "france"),
            ("Sans aucune hésitation, je voterai pour Marine Le Pen",
             "2026-11-15",
             "Europe 1, 15 novembre 2026, 11:40, heure de Paris. Phrase entre guillemets dans le post de @Europe1, « face à Jean-Luc Mélenchon ».",
             X_MONT_E1, F, "france"),
        ],
        [step("2026-11-15", "Phrases citées par CNews et Europe 1",
              "Les deux chaînes citent ses phrases sur un second tour entre Marine Le Pen et Jean-Luc Mélenchon.",
              X_MONT_VOTE, "CNews")],
    )
    add_link("thibault-de-montbrial", "marine-le-pen",
             "déclare qu'il voterait pour Marine Le Pen face à Jean-Luc Mélenchon (15/11/2026, CNews)",
             X_MONT_VOTE, "2026-11-15", "france", "autre")
    person(
        "yannick-jadot", "Yannick Jadot",
        "Sénateur, soutien de Raphaël Glucksmann (BFMTV, 15 novembre 2026)",
        "Le 15 novembre 2026, BFMTV cite une phrase de lui sur un second tour avec Marine Le Pen.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("Je n'en vois qu'un qui peut battre Marine Le Pen, c'est Raphaël Glucksmann",
             "2026-11-15",
             "BFMTV, 15 novembre 2026, 23:28, heure de Paris. Phrase entre guillemets dans le post de @BFMTV. Il est présenté comme sénateur et soutien de Raphaël Glucksmann.",
             X_JADOT, F, "france"),
        ],
        [step("2026-11-15", "Phrase citée par BFMTV",
              "BFMTV cite cette phrase sur Marine Le Pen et Raphaël Glucksmann.",
              X_JADOT, "BFMTV")],
    )
    add_link("yannick-jadot", "raphael-glucksmann",
             "dit que Raphaël Glucksmann est le seul qu'il voit battre Marine Le Pen (15/11/2026, BFMTV)",
             X_JADOT, "2026-11-15", "france", "autre")
    person(
        "chloe-ridel", "Chloé Ridel",
        "Députée européenne (Europe 1, 14 novembre 2026)",
        "Le 14 novembre 2026, Europe 1 cite une phrase d’elle sur un second tour entre Marine Le Pen et Jean-Luc Mélenchon.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("On ne peut pas avoir un second tour Le Pen/Mélenchon",
             "2026-11-14",
             "Europe 1, 14 novembre 2026, 18:20, heure de Paris. Phrase entre guillemets dans le post de @Europe1. Le post la présente au micro d’Hélène Roudil.",
             X_RIDEL, F, "france"),
        ],
        [step("2026-11-14", "Phrase citée par Europe 1",
              "Europe 1 cite cette phrase sur un second tour Le Pen / Mélenchon.",
              X_RIDEL, "Europe 1")],
    )
    person(
        "charles-alloncle", "Charles Alloncle",
        "Député UDR de l'Hérault (LCI, 15 novembre 2026)",
        "Le 15 novembre 2026, LCI cite une phrase de lui sur un second tour de Marine Le Pen.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("Quel que soit l'adversaire que Marine Le Pen pourrait affronter, selon les sondages au deuxième tour, il faudra le traiter avec exactement le même égard démocratique",
             "2026-11-15",
             "LCI, 15 novembre 2026, 21:21, heure de Paris. Phrase entre guillemets dans le post de @LCI. Il est présenté comme député UDR de l’Hérault.",
             X_ALLONCLE, F, "france"),
        ],
        [step("2026-11-15", "Phrase citée par LCI",
              "LCI cite cette phrase sur le second tour de Marine Le Pen.",
              X_ALLONCLE, "LCI")],
    )
    person(
        "charles-rodwell", "Charles Rodwell",
        "Député (Le JDD, 15 novembre 2026)",
        "Le 15 novembre 2026, le JDD met entre guillemets une phrase de lui sur les entrées d’étrangers.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("Il faut diviser les entrées par quatre",
             "2026-11-15",
             "Le JDD, 15 novembre 2026, 7:08, heure de Paris. Le post de @leJDD titre : « Immigration : « Il faut diviser les entrées par quatre », le plan du Charles Rodwell ».",
             X_RODWELL, F, "france"),
        ],
        [step("2026-11-15", "Phrase citée par le JDD",
              "Le JDD met cette phrase entre guillemets dans un titre sur l’immigration.",
              X_RODWELL, "Le JDD")],
    )
    person(
        "raphael-stainville", "Raphaël Stainville",
        "Journaliste au JDD (CNews, 13 novembre 2026)",
        "Le 13 novembre 2026, CNews cite deux phrases de lui sur l’interdiction d’entrée en Israël visant Jean-Luc Mélenchon et Mathilde Panot.",
        "Journalistes & éditorialistes", "Journalistes & chroniqueurs", ("gaza",),
        [
            ("Pourquoi leur donner l'occasion de (...) cracher leur haine sur Israël ?",
             "2026-11-13",
             "CNews, « 100% Actu », 13 novembre 2026, 16:36, heure de Paris. Phrase entre guillemets dans le post de @CNEWS. Les points de suspension entre parenthèses sont dans le post. Un post voisin, une minute plus tôt, omet le mot « sur ».",
             X_STAIN1, G, "gaza"),
            ("Ça donne l'occasion au leader insoumis de se victimiser",
             "2026-11-13",
             "CNews, 13 novembre 2026, 16:48, heure de Paris. Phrase entre guillemets dans le post de @CNEWS, sur l’interdiction de territoire visant Jean-Luc Mélenchon.",
             X_STAIN2, G, "gaza"),
        ],
        [step("2026-11-13", "Phrases citées par CNews",
              "CNews le présente comme journaliste au JDD et cite ses phrases sur l’interdiction d’entrée en Israël visant Jean-Luc Mélenchon et Mathilde Panot.",
              X_STAIN1, "CNews")],
    )
    person(
        "sebastien-chenu", "Sébastien Chenu",
        "Député du Rassemblement national (X, 15 novembre 2026)",
        "Le 15 novembre 2026, il écrit sur X que la liberté d’expression sera un combat de 2027, et renvoie à une tribune dans le JDD.",
        "Responsables politiques", "Parlementaires & élus", ("france",),
        [
            ("La liberté d’expression sera l’un des grands combats de 2027.",
             "2026-11-15",
             "Message sur X (@sebchenu), 15 novembre 2026, 12:08, heure de Paris. Il renvoie à une tribune dans le JDD. Le texte de la tribune n’est pas recopié ici.",
             X_CHENU, F, "france"),
        ],
        [step("2026-11-15", "Message sur la liberté d’expression",
              "Il écrit que la liberté d’expression sera l’un des grands combats de 2027.",
              X_CHENU, "X")],
    )
