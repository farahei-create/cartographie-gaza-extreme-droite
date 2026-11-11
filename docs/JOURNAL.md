# Journal des mises à jour

Les agents complètent ce fichier à chaque publication, en haut de la liste. Une entrée = un jour, les ajouts, les URL. Sert à ne pas republier deux fois la même phrase.

Les entrées d'avant le 10 novembre 2026 sont reconstituées depuis `git log`. Le détail des phrases est dans `data.json`.

## 2026-11-11 — v33

Tu raccourcis le haut de l'accueil. Le mot Onrecord redevient le titre, grand et centré, avec une ombre légère qui suit un peu le pointeur. Dessous : « Ils l'ont dit. On l'a archivé. » Puis une seule ligne, plus petite : « Déclarations publiques sur Gaza et l'extrême droite en France, et les liens entre leurs auteurs. » Les trois cartes restent, avec des libellés courts : Gaza, Extrême droite, Les liens. Le réseau, l'inclinaison des cartes et la recherche ne changent pas. Le reste de la page non plus. Cache `onrecord-v33`.

## 2026-11-11 — v32

Tu refais seulement le haut de l'accueil. En deux secondes, on voit ce que le site fait : il archive les déclarations publiques sur Gaza, il documente la normalisation de l'extrême droite en France, et il montre les liens entre les personnes, les médias, l'argent et les organisations. Trois accès, au doigt : Gaza, France, Coulisses. Le fond est un réseau qui tourne lentement, s'écarte du doigt et s'éclaircit près du pointeur. Les cartes s'inclinent. Le reste de la page ne change pas : compteurs, citation du jour, dernières entrées, bouton Soutenir. Cache `onrecord-v32`.

## 2026-11-11 — v31

Tu ajoutes Louise Montangon, 22 ans, responsable de l'UNI à Bordeaux, et le syndicat UNI. Pas de photo libre : monogramme. Tu recentres l'accueil.

Citations (la phrase, la date, la page) :

- Sénat, 15/04/2026 : Parcoursup, et « saccager l'université en la bloquant » — https://www.senat.fr/compte-rendu-commissions/20260413/ce_universites.html
- Le Parisien, 08/10/2026 : « J'ai honte d'appartenir à cette génération » — https://www.leparisien.fr/societe/jai-honte-dappartenir-a-cette-generation-qui-est-louise-montangon-letudiante-candidate-rn-aux-municipales-qui-fustige-les-blocus-lyceens-08-10-2026-LORHOXBKGRGIRB7AKPWHQ2LWEA.php
- VA+, 22/10/2026 : « J'ai pas honte de cette génération. J'ai honte de cette partie de la jeunesse » — https://www.valeursactuelles.com/societe/a-15-ans-jetais-tres-a-gauche-louise-montangon-raconte-son-basculement-a-droite-et-son-combat-contre-les-blocages
- LCI, 06/10/2026, face à Gabriel Attal : « Ça ne sert à rien de me regarder avec un petit sourire, votre bilan est désastreux ! » et « Vous êtes le visage du laxisme » — même article du Parisien
- LCI, 07/10/2026, « La Grande Confrontation » : « Vous êtes les idiots utiles de ce mouvement » et « Bloquer des établissements c'est i-llé-gal ». Le Parisien écrit « mercredi 6 octobre », qui n'est pas un mercredi. Sud Ouest et le JDD placent le débat le 7. Le lycéen n'est pas nommé — https://www.leparisien.fr/culture-loisirs/tv/moi-je-nasperge-pas-mes-professeurs-dessence-le-face-a-face-entre-elwan-et-louise-vire-au-reglement-de-comptes-sur-lci-09-10-2026-LPGLK6QOYZDYFHMI2QNUZGFEHM.php
- JDD, 11/10/2026 : l'emploi du temps, « J'ai préféré prendre du recul », et la phrase sur la jeunesse de droite — https://www.lejdd.fr/Societe/mobilisation-lyceenne-louise-montangon-visage-de-la-resistance-aux-blocages-185745
- Sud Ouest, 09/10/2026 : « J'étais très déçue par l'alliance entre LR et les macronistes » et « Je dois tout à l'extrême gauche » — https://www.sudouest.fr/gironde/bordeaux/decryptage-qui-est-la-bordelaise-louise-montangon-etoile-montante-du-rn-sur-les-plateaux-tele-de-la-colere-lyceenne-30996470.php
- VA+, 22/10/2026 : « Je comprends pas comment, à 18 ou à 20 ans, on peut crier à la gloire du Hamas ». C'est son récit d'octobre 2024, pas un fait recoupé
- UNI, pétition citée le 09/10/2026 par 20 Minutes — https://www.20minutes.fr/societe/4252906-20261009-militante-rn-uni-bordelaise-louise-montangon-etudiante-echarpe-mobilisation-lyceenne
- Cyril Hanouna, 08/10/2026, selon Midi Libre : « Si elle veut, je l'engage tout de suite. » — https://www.midilibre.fr/2026/10/12/elle-a-refuse-loffre-de-cyril-hanouna-pour-rejoindre-un-media-du-groupe-bollore-louise-montangon-est-le-nouveau-phenomene-mediatique-de-la-droite-13597210.php

Nuances sur la même fiche : Bordeaux-Montaigne dit à 20 Minutes qu'elle n'y est plus étudiante depuis 2025. Sud Ouest parle d'un master à distance rattaché à Reims. Le JDD la présente encore à Bordeaux-Montaigne. Le JDD écrit qu'elle ne rejette pas l'offre d'Hanouna. Midi Libre et Public, le 12 octobre, écrivent qu'elle n'a pas donné suite et qu'elle a mis en avant le JDD. Le portrait ne dit pas qu'elle y est recrutée. Marie France écrit que la liste municipale n'a pas eu d'élu.

Parcours : septembre 2022, octobre 2024, septembre 2025, décembre 2025, mars 2026, 15 avril 2026, septembre 2026. Liens coulisses vers l'UNI, le RN, Hanouna, le JDD et Gabriel Attal.

Accueil : textes centrés, promesse courte, compteurs lus dans `data.json` (animation coupée si `prefers-reduced-motion`), accès vers Coulisses, l'échelle et les candidats 2027, citation du jour avec un bouton « Une autre », dernières déclarations. Le bouton Soutenir ne change pas.

Module : `v31_content.py`.

## 2026-11-11 — v30

Tu fais commencer la frise « Voir comment elle/il est arrivé là » par les études, quand une page relue donne l'année. Repère Formation sur la frise. Pas d'étape si l'année manque.

- Marine Le Pen : 1992, serment ; 1998, service juridique du FN — franceinfo
- Jordan Bardella : 2016, licence de géographie quittée sans diplôme ; bac ES au lycée Jean-Baptiste-de-La-Salle, sans année — France Inter. L'adhésion de 2012 reste avant, il a 16 ans
- Éric Zemmour : 1979, Sciences Po ; 1986, Quotidien de Paris — Le Figaro
- Marion Maréchal : 2010, licence ; 2011, master 1 ; 2018, EM Lyon — Parlement européen
- Emmanuel Macron : 2001, Sciences Po ; 2004, ENA ; 2008, Rothschild — Sciences Po, Élysée, franceinfo
- Édouard Philippe : 1988, bac à Bonn ; 1995, ENA ; 1997, Conseil d'État — vie-publique.fr, franceinfo
- Gabriel Attal : 2007 et 2013, Sciences Po ; École alsacienne sans année de bac — Les Echos
- Marine Tondelier : 2009, IEP de Lille ; 2011, diplôme puis collaboratrice — France 24
- Jean-Luc Mélenchon : 1968, terminale ; 1969, faculté de Besançon ; 1976, professeur — France 3

Les autres fiches n'ont pas reçu d'étape : aucune page relue ne datait les études.

## 2026-11-11 — v29

Tu ranges Marine Le Pen dans « Candidats à la présidentielle 2027 », sans deuxième fiche. Le rôle, la photo et le parcours restent. Tu ajoutes la phrase du 20 heures de TF1, le 7 juillet 2026.

- Marine Le Pen, 07/07/2026 : « Ce soir, je suis candidate à l'élection présidentielle et je ne changerai pas d'avis. » — Journal de 20 heures de TF1, cité par franceinfo. La cour d'appel de Paris a confirmé la condamnation et ramené l'inéligibilité à 45 mois dont 30 avec sursis ; la partie ferme déjà exécutée, elle est éligible en 2027 — https://www.franceinfo.fr/politique/marine-le-pen/je-suis-candidate-a-l-election-presidentielle-marine-le-pen-annonce-son-pourvoi-en-cassation-apres-sa-condamnation-allegee-en-appel_8098361.html et https://www.franceinfo.fr/politique/front-national/affaire-des-assistants-fn-au-parlement-europeen/marine-le-pen-condamnee-en-appel-a-trois-ans-de-prison-dont-un-an-sous-bracelet-electronique-mais-eligible-en-2027_8097896.html
- Éric Zemmour, 10/11/2026 : « Oui, je vous le confirme je suis bien candidat à l'élection présidentielle » — TF1, cité par BFMTV. Même sous-catégorie — https://www.bfmtv.com/politique/elections/presidentielle/je-suis-bien-candidat-eric-zemmour-confirme-se-presenter-a-l-election-presidentielle_AN-202611100873.html
- Bruno Retailleau, 19/04/2026 : les adhérents LR le désignent candidat, plus de 73 % des voix (franceinfo). Phrase sur X citée par franceinfo. Même sous-catégorie — https://www.franceinfo.fr/politique/les-republicains/presidentielle-2027-les-adherents-lr-choisissent-bruno-retailleau-comme-candidat_7951298.html
- Pas reclassés : Jordan Bardella (candidat à Matignon, pas à l'Élysée ; 20 Minutes, 29/08/2026), Sarah Knafo (« donc non, je n'irai pas », BFMTV, 09/11/2026), Marion Maréchal (campagne de Marine Le Pen, Le Figaro, 09/09/2026), Éric Ciotti (écarte une candidature, Le Figaro, 28/05/2025), Valérie Pécresse (pas de déclaration, franceinfo, 31/08/2026)

## 2026-11-11 — v28

Tu ajoutes les instituts dont l'actionnaire est documenté, et le récit « Suivre les sondages ». La vidéo TikTok n'est pas une source.

- Ifop : vente au fonds LFPI annoncée le 25/07/2022 (Le Figaro) ; entretien du 04/11/2022 (actionnaire majoritaire, équipe aussi au capital) ; registre du 10/11/2026 : président ETUDINVEST, actionnaires non publiés — Le Figaro, ifopgroup.com, Pappers
- OpinionWay : entré en 2022 dans Les Echos-Le Parisien (LVMH) ; 20 Minutes du 24/07/2026 parle d'un rachat de 75 % et d'un projet de vente non signé dans l'article — opinion-way.com, 20 Minutes
- CSA : « fait partie du groupe Havas depuis 2015 » (communiqué du 13/02/2026). Havas coté depuis la scission de Vivendi ; Bolloré SE 30,4 % au 31/12/2025 ; famille au-dessus de 50 % le 23/02/2026 — CSA, bollore.com, Havas, Les Echos
- Harris Interactive acquis par Toluna en 2014 ; pas de groupe de médias nommé dans le communiqué du 28/09/2026 — Toluna
- Elabe : associés actionnaires selon CB News du 05/09/2022 ; mentions légales du 11/11/2026 sans groupe de médias — CB News, elabe.fr
- Commission des sondages : loi du 19/07/1977, champ limité au débat électoral ; gratification « s'il y a lieu », sans montant — commission-des-sondages.fr
- JDD, 04/01/2026 : Top 50 créé en 1988 avec l'Ifop, réalisé par CSA ; Bardella 4e, Le Pen 7e. 20 Minutes attribue au Monde la phrase sur les sept politiques de tête publiés chez Fayard. Le décompte « 4 de gauche sur 24 » n'est pas repris
- Éric Zemmour : Challenges, 06/10/2021, de 7 % à 17 % en moins d'un mois dans le sondage Harris, avant candidature déclarée ; 7,07 % le 10/04/2022 — Challenges, Conseil constitutionnel
- Odoxa non ajouté : la page lue nomme le président, pas l'actionnaire. Le 0,25 € des panels n'est pas publié

Module : `v28_content.py`.

## 2026-11-10 (soir) — v27

- CNews, 10/11/2026 : communiqué après le classement de la pétition « Supprimer CNews de l'audiovisuel français » par la commission des affaires culturelles (28 voix contre 25) — Le Parisien/AFP, franceinfo, site de l'Assemblée nationale
- RN (Caroline Parmentier), 10/11/2026 : « cette obsession de la censure… » dans le même débat, avec la réponse d'Aymeric Caron — franceinfo
- Sarah Knafo, 09/11/2026 : BFMTV-RMC, Darmanin aurait « dit la même chose » qu'Éric Zemmour ; VRAI/FAUX de BFMTV : faux — BFMTV
- Lise Boëll, 09/11/2026 : nommée directrice générale déléguée de Grasset (parcours), citation d'Arnaud Lagardère dans le communiqué, lien coulisses Lagardère → Boëll — franceinfo/AFP

Module : `v27_content.py`. Archives réessayées.

## 2026-11-10 — v26

Citations ajoutées sur des fiches qui en avaient 0 ou 1. Portraits Commons ou Parlement européen. Monogrammes. Page `#/credits`. Guide `docs/REPRISE.md`.

Citations (personne, date, source) :

- Pascal Praud, 29/09/2023, trois phrases sur punaises de lit et immigration — franceinfo, Le Figaro
- Geoffroy Lejeune, 28/09/2023, deux phrases sur « l'immigration arabo-musulmane » — Le Figaro / AFP (décision Arcom)
- Pierre-Édouard Stérin, 17/07/2024 et 18/07/2024, tribune Périclès — Le Figaro, La Croix
- Philippe Olivier, 28/09/2021, référendum immigration — franceinfo
- Sarah Knafo, 09/12/2024 et 10/02/2025 — CNews
- Erik Tegnér, 08/10/2025 — Europe 1
- Serge Nedjar, 30/09/2025, réponse à Delphine Ernotte — Figaro cité par Puremédias
- Tugdual Denis, 02/07/2026, éditorial — Valeurs actuelles
- Arnaud Rérolle, 06/05/2025, audition — compte rendu Assemblée nationale

Pas de phrase exacte trouvée, fiches laissées telles quelles : Alban du Rostu, Arnaud Lagardère, Constance Benqué, Donat Vidal-Revel, François Durvye, Gérald-Brice Viret, Kévin Pfeffer (franceinfo du 25/06/2025 le paraphrase sans guillemets), Lise Boëll, Philippe Conrad. Déjà une citation, pas de deuxième phrase vérifiée ce jour-là : Gérard Carreyrou, Jean-Dominique Merchet, Joseph Thouvenel, Jules Torres, Patrick Klugman, Renaud Camus, Vincent Bolloré, Yonathan Arfi, Édouard Philippe.

Photos : 16 portraits (Commons CC BY, CC BY-SA, CC0, ou Parlement européen). Logos : M6 et Prisma Media (domaine public). Le reste sans fichier libre : monogramme.

## 2026-11-09 — v25

`d45e741` — Marine Le Pen (60 Minutes, CBS), archives.
`33f9c07` — v24 : parcours pour toutes les personnes, vue Coulisses (Tegnér, Knafo, Praud, Olivier, Pfeffer, Lejeune, Stérin, Rérolle, Nedjar, etc.).
`f451506` — v23 : parcours d'ascension, liens classés ascension / opposition / coulisses / autre.
`53904cc` — v22 : vue Échelle du pouvoir.

## 2026-11-08

`3670598` — Caroline Yadan (X, 07/11), contexte sur l'ambassadeur dans la fiche Mélenchon (Bourget), archives.

## 2026-11-07

`5140daa` — Mélenchon (Bourget et X, Gaza), Bardella (CNews, antifas).

## 2026-11-06

`a805771` — Le Pen et le RN (CNews), Bardella / Bainville, programme Gaza de Mélenchon.

## 2026-11-05

`6b10389` — v18 : bouton « Soutenir », animation au tap, `onrecord-v18`.
`956ff0e` — Bardella (*Gouverner*), refus de presse sur Fayard / Bolloré, pétition CNews.
`5fc1fac` — v16 : page « Proposer une mise à jour », retrait de la mention GitHub.
`7a2545b` — v15 : cartes Partager avec portrait en fond et médaillon.
`04c4e30` — v14 : huit candidats 2027 (Mélenchon, Glucksmann, Roussel, Tondelier, Philippe, Attal, Bertrand, Villepin) et Macron.
`b38be66` — v13 : Leetchi, citation du jour, « Continuer à explorer », « Reprendre ».
`cc95b3c` — v12 : groupes dissous (Génération identitaire, Zouaves, Civitas, Remparts, GUD), parquet national antiterroriste.

## 2026-11-04

`d91cb81` — v10 : Cyril Hanouna, Némésis, ISSEP, groupe M6.
`9201279` — retrait de la section « Déclarations et votes » (d'où l'échec durable de `test_v8.py`).
`c0c5c7e` — v8 : cette section, publiée puis retirée.
`889be48` — v7 : carte à partager, page Méthode, vue Avant / maintenant.

## 2026-11-03

`46b1a84` — condamnation pour menaces racistes, Nantes (02/11/2026). L'archive Le Parisien de cette affaire échoue encore (voir `docs/REPRISE.md`).
`5d50665` — trois décisions de l'Arcom (Europe 1, CNews).
`c7dcb49` — saisine de la justice par l'Arcom après des propos d'Éric Zemmour.
`101d3b8` — v5 : accueil, sections, fiches, chronologie, PWA.
`711db2f` — v4 : photos, logos, vidéos, section France.
`3567b04` — premier commit.
