"""v30 : début de frise, études et premier métier, seulement si une page relue les date."""

FI_TRAVAIL = "https://www.franceinfo.fr/economie/emploi/metiers/presidentielle-les-candidats-et-le-monde-du-travail_2142710.html"
FI_BARDELLA = "https://www.radiofrance.fr/franceinter/cinq-choses-a-savoir-sur-jordan-bardella-designe-premier-vice-president-pour-remplacer-marine-le-pen-3829052"
FIG_ZEM = "https://www.lefigaro.fr/elections/presidentielles/presidentielle-2022-eric-zemmour-candidat-20211130"
EP_MAR = "https://www.europarl.europa.eu/meps/fr/256922/MARION_MARECHAL/cv"
ELYSEE = "https://www.elysee.fr/emmanuel-macron"
SP_MAC = "https://www.sciencespo.fr/fr/actualites/emmanuel-macron-promotion-2001/"
ECHOS_ATT = "https://www.lesechos.fr/politique-societe/education/quelles-etudes-ont-ete-suivies-par-gabriel-attal-nouveau-premier-ministre-2045292"
FI_PHI = "https://www.franceinfo.fr/politique/emmanuel-macron/six-choses-que-vous-ignorez-peut-etre-sur-edouard-philippe-pressenti-pour-devenir-le-premier-ministre-d-emmanuel-macron_2190663.html"
VP_PHI = "https://www.vie-publique.fr/discours/203599-declaration-de-m-edouard-philippe-premier-ministre-sur-les-grandes-or"
F24_TON = "https://www.france24.com/fr/france/20221127-congrès-eelv-marine-tondelier-la-favorite-qui-rêvait-d-un-avenir-en-vert"
F3_MEL = "https://france3-regions.franceinfo.fr/bourgogne-franche-comte/info/la-jeunesse-franc-comtoise-de-melenchon-31773.html"


def apply(N, by, step):
    def add(pid, steps):
        n = by[pid]
        cur = list(n.get("parcours") or [])
        seen = {(s["date"], s["title"]) for s in cur}
        for s in steps:
            s = dict(s)
            s["kind"] = "formation"
            if (s["date"], s["title"]) not in seen:
                cur.append(s)
                seen.add((s["date"], s["title"]))
        cur.sort(key=lambda s: s["date"])
        n["parcours"] = cur

    add("marine-le-pen", [
        step("1992", "Prestation de serment",
             "Le journal de 20 heures de France 2, cité par franceinfo, rappelle qu'elle prête serment en 1992. Elle plaide pendant six ans.",
             FI_TRAVAIL, "franceinfo"),
        step("1998", "Service juridique du Front national",
             "Le même sujet indique qu'en 1998 elle intègre le service juridique du Front national.",
             FI_TRAVAIL, "franceinfo"),
    ])
    add("jordan-bardella", [
        step("2016", "Licence de géographie interrompue",
             "France Inter : titulaire d'un baccalauréat économique et social, mention très bien, obtenu au lycée privé Jean-Baptiste-de-La-Salle de Saint-Denis, il s'inscrit en licence de géographie à Paris-Sorbonne. Il quitte l'université en 2016, en troisième année, sans diplôme. L'article ne date pas le bac. L'adhésion au Front national, en 2012, est antérieure : il a alors 16 ans.",
             FI_BARDELLA, "France Inter"),
    ])
    add("eric-zemmour", [
        step("1979", "Sciences Po Paris",
             "Le Figaro écrit qu'il est diplômé de Sciences Po Paris en 1979 et qu'il échoue deux fois au concours d'entrée de l'ENA. Il se tourne ensuite vers la publicité. L'article ne date pas cette activité.",
             FIG_ZEM, "Le Figaro"),
        step("1986", "Quotidien de Paris",
             "La même biographie du Figaro : il devient journaliste au Quotidien de Paris en 1986.",
             FIG_ZEM, "Le Figaro"),
    ])
    add("marion-marechal", [
        step("2010-06", "Licence à Panthéon-Assas",
             "Le curriculum publié sur le site du Parlement européen, sous la responsabilité de l'élue, indique une licence de droit des affaires à l'université Panthéon-Assas en juin 2010.",
             EP_MAR, "Parlement européen"),
        step("2011-06", "Master 1 à Panthéon-Assas",
             "Le même curriculum indique un master 1 de droit public à Panthéon-Assas en juin 2011.",
             EP_MAR, "Parlement européen"),
        step("2018-06", "EM Lyon",
             "Le curriculum du Parlement européen indique, en juin 2018, un diplôme équivalent à un master 2 en management à l'EM Lyon.",
             EP_MAR, "Parlement européen"),
    ])
    add("emmanuel-macron", [
        step("2001", "Sciences Po, promotion 2001",
             "La page de Sciences Po titrée « promotion 2001 » écrit qu'il entre à 21 ans après trois années de classe préparatoire littéraire au lycée Henri-IV et deux échecs au concours de l'ENS. En parallèle, il obtient une maîtrise puis un DEA de philosophie à l'université de Nanterre. La page ne date pas ces deux diplômes.",
             SP_MAC, "Sciences Po"),
        step("2004", "ENA, puis Inspection des finances",
             "L'Élysée écrit qu'il a étudié la philosophie avant d'intégrer l'ENA, dont il est diplômé en 2004, puis l'Inspection générale des finances, où il travaille quatre ans.",
             ELYSEE, "Élysée"),
        step("2008", "Banque Rothschild",
             "franceinfo, citant le journal de 20 heures de France 2 : de 2008 à 2012, il est banquier d'affaires chez Rothschild.",
             FI_TRAVAIL, "franceinfo"),
    ])
    add("edouard-philippe", [
        step("1988", "Baccalauréat à Bonn",
             "Dans un discours du 15 septembre 2017 retranscrit par vie-publique.fr, il dit avoir vécu à Bonn de 1986 à 1988, avoir été élève au Friedrich-Ebert-Gymnasium et y avoir passé le baccalauréat français.",
             VP_PHI, "vie-publique.fr"),
        step("1995", "Entrée à l'ENA",
             "franceinfo : après le bac à Bonn, une année d'hypokhâgne, puis Sciences Po, section « service public ». Il intègre l'ENA en 1995. L'article ne date pas le diplôme de Sciences Po.",
             FI_PHI, "franceinfo"),
        step("1997", "Conseil d'État",
             "Le même article de franceinfo : il sort de l'ENA en 1997 et rejoint le Conseil d'État.",
             FI_PHI, "franceinfo"),
    ])
    add("gabriel-attal", [
        step("2007", "Entrée à Sciences Po",
             "Les Echos écrivent qu'il est scolarisé à l'École alsacienne, de la grande section de maternelle à la terminale. Le bac obtenu, il intègre Sciences Po Paris en 2007. L'article ne date pas le bac.",
             ECHOS_ATT, "Les Echos"),
        step("2013", "Master de Sciences Po",
             "Les Echos : il sort diplômé de Sciences Po en 2013, master en affaires publiques. En parallèle, une licence de droit à l'université Paris-Panthéon-Assas, qu'il n'obtient pas. L'université l'a indiqué au journal.",
             ECHOS_ATT, "Les Echos"),
    ])
    add("marine-tondelier", [
        step("2009", "IEP de Lille",
             "France 24 : après une classe préparatoire littéraire, elle entre à l'Institut d'études politiques de Lille. Pendant ces études, à 22 ans, elle adhère à Europe Écologie-Les Verts en 2009. L'article ne date pas l'entrée à l'IEP.",
             F24_TON, "France 24"),
        step("2011", "Diplôme, puis collaboratrice parlementaire",
             "France 24 : le diplôme en poche, elle devient collaboratrice parlementaire de la sénatrice Aline Archimbaud, de 2011 à 2015, chargée des questions sanitaires et sociales. L'article ne donne pas l'année du diplôme, seulement qu'il est obtenu avant ce poste.",
             F24_TON, "France 24"),
    ])
    add("jean-luc-melenchon", [
        step("1968", "Terminale au lycée Rouget-de-Lisle",
             "France 3 : il est en classe de terminale au lycée Rouget-de-Lisle, à Lons-le-Saunier, lorsque Mai 68 éclate. L'article ne dit pas la date du baccalauréat.",
             F3_MEL, "France 3"),
        step("1969", "Faculté de lettres de Besançon",
             "France 3 : en 1969, il étudie à la faculté de lettres de Besançon, où il prépare une licence de philosophie. L'article ne dit pas s'il obtient le diplôme.",
             F3_MEL, "France 3"),
        step("1976", "Professeur de français",
             "France 3 : en 1976, il devient professeur de français dans un lycée à Lons-le-Saunier. Il est aussi journaliste à La Dépêche du Jura.",
             F3_MEL, "France 3"),
    ])
