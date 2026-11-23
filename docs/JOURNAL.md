# Journal des mises à jour

Les agents complètent ce fichier à chaque publication, en haut de la liste. Une entrée = un jour, les ajouts, les URL. Sert à ne pas republier deux fois la même phrase.

Les entrées d'avant le 10 novembre 2026 sont reconstituées depuis `git log`. Le détail des phrases est dans `data.json`.

## 2026-11-23 — onglet Liens épuré (cache `onrecord-v57`)

Tu enregistres d'abord `version-2026-11-23-avant-liens` (commit `5ade8e6`, cache `onrecord-v56`). Refonte visuelle de l'onglet Liens, sans changer les données : filets fins à la place des cadres violets et des halos, textes de commande à 13 px, chiffres et dates en chasse fixe. Réseau / Coulisses / Échelle devient un contrôle segmenté compact, le bouton Filtres est sur la ligne de recherche, les puces de filtre sont plus petites. Réseau : compteur « Fiche 001 / 138 », cartes compactes (deux et demie visibles sur téléphone), carte choisie bordée d'une seule couleur, point pour les fiches liées. Le détail devient une liste : nom, date (JJ.MM.AAAA), relation, nature du lien en petit, « Source » en ligne, et « Ouvrir la fiche ». Échelle et Coulisses reprennent les mêmes segments fins. Cibles de 44 px gardées, clair et sombre vérifiés à 390×844 et 1280. Code : bloc « 23/11 : onglet Liens épuré » en fin de `style.css`, `renderRail` dans `app.js`, `#rail-meta` dans `index.html`. Captures avant/après dans `shots/` (non versionnées). Aucune phrase nouvelle.

## 2026-11-22 (soir) — contributions des lecteurs (cache `onrecord-v56`)

Tu enregistres d'abord `version-2026-11-22-avant-contributions` (commit `8cdb488`, cache `onrecord-v55`). Nouvelle section gratuite : inscription par e-mail avec code à six chiffres (adresses jetables refusées), dépôt d'une note avec liens, photos ou vidéos sur une fiche existante, validation obligatoire dans `/admin.html`, bouton « Signaler un contenu » sur chaque contribution, charte et mentions sur `#/contributions`. Bloc « Contributions des lecteurs » en bas de chaque fiche, en ambre pointillé, distinct des citations sourcées. Fichiers : `contrib.js`, `admin-contrib.js`, `api/contrib/[action].js`, `lib/contrib/`, `contributions.json` (vide), `vendor/blob-upload.js`, `package.json`. Tant que les variables Vercel manquent, la section affiche « Bientôt disponible ». Mode d'emploi : `docs/REPRISE.md`, section 14. Aucune phrase nouvelle.

## 2026-11-22 — rattrapage du 18 au 22/11

Tu enregistres d'abord `version-2026-11-22-avant-maj` (commit `07db852`, cache `onrecord-v53`). Module `v54_content.py`. Tu publies 29 phrases, dont 7 nouvelles fiches (Jean-Philippe Tanguy, Laurent Nuñez, Hugues Moutouh, Edwige Diaz, David Lisnard, Gérard Larcher, Laure Lavalette). Chaque URL est ouverte ce jour et chaque phrase y figure mot pour mot. Pas de photo : monogramme.
Thèmes : affaire Moutouh (mail retrouvé chez Frédéric Chatillon), primaire de la droite et place d'Éric Zemmour, rapprochements LR-RN, Pierre Perret et Gaza, menace d'ultradroite selon le Pnat.
Correction du relevé automatique : les deux phrases d'Éric Zemmour sur Europe 1 sont datées du 21/11 (meeting du samedi), non du 22/11, date de la page.

- Marine Le Pen, 22 novembre 2026 : « Je ne sais absolument pas comment ce mail a pu se retrouver chez un de nos anciens prestataires. Mais en l'espèce, encore une fois, ce n'est pas passé par moi » — https://www.franceinfo.fr/politique/front-national/je-n-ai-jamais-recu-d-informations-confidentielles-affirme-marine-le-pen-au-sujet-du-prefet-hugues-moutouh-soupconne-d-avoir-renseigne-le-rn_8294876.html
- Jordan Bardella, 18 novembre 2026 : « Il y a un certain nombre de gens qui ont été mis en cause par Mediapart et qui ont nié les accusations. Vous-même vous avez été mis en cause. » — https://www.lejdd.fr/politique/vous-meme-vous-avez-ete-mis-en-cause-dans-une-affaire-de-harcelement-jordan-bardella-repond-a-patrick-cohen-sur-mediapart-189114
- Jordan Bardella, 18 novembre 2026 : « Je n'ai pas de leçons à recevoir, encore une fois, en matière de lutte contre l'antisémitisme. Mon parcours en la matière a toujours été exemplaire. » — https://www.closermag.fr/politique/jordan-bardella-accuse-dantisemitisme-il-patauge-dans-la-semoule-et-finit-par-sortir-de-ses-gonds-je-nai-pas-de-lecons-a-recevoir-3670179
- Éric Zemmour, 21 novembre 2026 : « Ma position est simple : j'ai été convié à cette primaire, j'ai accepté, donc j'y serai... si elle a lieu bien sûr » — https://www.europe1.fr/politique/jy-serai-si-elle-a-lieu-eric-zemmour-confirme-sa-volonte-de-participer-a-la-primaire-de-la-droite-et-du-centre-1241887
- Robert Ménard, 19 novembre 2026 : « Ils veulent vraiment perdre ? Ils sont fous. Ils portent une responsabilité personnelle dans cette histoire. » — https://www.europe1.fr/politique/edouard-philippe-gabriel-attal-ils-veulent-vraiment-perdre-ironise-robert-menard-1240143
- Gérald Darmanin, 18 novembre 2026 : « Cette primaire, c'est un marché de dupes, et aujourd'hui, elle ne va pas désigner le prochain candidat à la présidence de la République » — https://www.bfmtv.com/politique/elections/presidentielle/gerald-darmanin-estime-que-jean-luc-melenchon-gagnera-face-a-marine-le-pen-en-cas-de-duel-au-second-tour-de-l-election-presidentielle_AD-202611180359.html
- Bruno Retailleau, 18 novembre 2026 : « Si on veut que la primaire se tienne, il faut être raisonnable. Si vous dites demain qu'Eric Zemmour doit faire partie de la primaire, en réalité, vous flinguez la primaire. Car ni les uns, ni les autres, ni participeront » — https://www.publicsenat.fr/actualites/politique/primaire-en-incluant-eric-zemmour-david-lisnard-cherche-t-il-a-planter-le-processus-ou-a-en-faire-un-pre-premier-tour-de-la-presidentielle
- Bruno Retailleau, 19 novembre 2026 : « Un appel d'air » — https://www.bfmtv.com/politique/elections/presidentielle/video-un-appel-d-air-bruno-retailleau-s-oppose-a-la-regularisation-de-travailleurs-sans-papiers-dans-le-secteur-du-batiment_VN-202611190728.html
- Parquet national antiterroriste (Pnat), 22 novembre 2026 : « la première s'inscrit dans des projets de violences contre les personnes, la seconde dans des actions contre des biens et des infrastructures » — https://www.bfmtv.com/police-justice/terrorisme/islamisme-ultra-droite-radicale-violente-la-france-reste-sous-fortes-tensions-de-la-menace-terroriste-selon-le-procureur-antiterroriste_AD-202611220124.html
- Jean-Luc Mélenchon, 17 novembre 2026 : « Franchement, Pierre Perret dans le rôle où le place sa chanson contre les prétendus "antisémites" que nous serions, cela me fait de la peine » — https://www.lejdd.fr/politique/on-lefface-de-nos-tablettes-pour-les-repas-jean-luc-melenchon-appelle-a-ne-plus-ecouter-pierre-perret-189138
- Jean-Luc Mélenchon, 17 novembre 2026 : « Il sait très bien que "antisémite" désigne les adversaires du génocide à Gaza. » — https://www.lejdd.fr/politique/on-lefface-de-nos-tablettes-pour-les-repas-jean-luc-melenchon-appelle-a-ne-plus-ecouter-pierre-perret-189138
- Édouard Philippe, 19 novembre 2026 : « Ça n'est pas mon camp politique » — https://www.bfmtv.com/politique/elections/presidentielle/presidentielle-gerard-larcher-ne-ressent-pas-de-proximite-avec-eric-zemmour-et-ne-souhaite-pas-l-inclure-dans-la-primaire-de-la-droite_AV-202611190987.html
- Édouard Philippe, 18 novembre 2026 : « espèce de fascination malsaine » — https://www.bfmtv.com/politique/elections/presidentielle/guerre-en-ukraine-edouard-philippe-denonce-la-fascination-malsaine-de-jean-luc-melenchon-et-marine-le-pen-pour-vladimir-poutine_AD-202611180518.html
- Dominique de Villepin, 20 novembre 2026 : « Je ne mets pas le RN et LFI sur le même plan » — https://www.bfmtv.com/politique/front-national/video-je-ne-mets-pas-le-rn-et-lfi-sur-le-meme-plan-assure-dominique-de-villepin-declarant-que-le-rn-porte-un-heritage-de-xenophobie-de-racisme-et-d-antisemitisme_VN-202611200484.html
- Sandrine Rousseau, 21 novembre 2026 : « C'était une proposition du Rassemblement national, qui a été mise à l'agenda politique par les LR, et qui maintenant a été soutenue par le ministre de l'Intérieur. C'est honteux! » — https://www.bfmtv.com/politique/parlement/honteux-marchepied-a-marine-le-pen-la-gauche-denonce-l-adoption-de-la-loi-de-presomption-d-usage-legal-des-armes-par-les-forces-de-l-ordre_AD-202611210292.html
- Julien Odoul, 20 novembre 2026 : « J'observe qu'il faudrait que le secret de l'instruction soit préservé » — https://www.franceinfo.fr/societe/justice/direct-si-les-faits-sont-averes-ils-sont-evidemment-tres-graves-laurent-nunez-convoque-le-prefet-hugues-moutouh-soupconne-d-avoir-transmis-des-informations-sensibles-au-rassemblement-national_8291756.html
- Michel Onfray, 21 novembre 2026 : « Que va-t-on faire de cet antisémitisme que Jean-Luc Mélenchon libère comme des chiens furieux ? » — https://www.cnews.fr/videos/france/2026-11-21/que-va-t-faire-de-cet-antisemitisme-que-jean-luc-melenchon-libere-comme
- Sébastien Chenu, 18 novembre 2026 : « Je le dis aux électeurs de David Lisnard, Bruno Retailleau et Edouard Philippe : tournez-vous vers nous » — https://www.cnews.fr/france/2026-11-18/je-le-dis-aux-electeurs-de-david-lisnard-bruno-retailleau-et-edouard-philippe
- Jean-Philippe Tanguy, 20 novembre 2026 : « Ce sont des rumeurs et des accusations sans fondement en pleine campagne. Ça n'indigne personne parce que ça touche le RN. On prend les coups et on reste dignes » — https://www.lefigaro.fr/actualite-france/soupcons-de-fuites-au-profit-du-rn-si-les-faits-concernant-le-prefet-moutouh-sont-averes-ils-sont-tres-graves-reagit-laurent-nunez-20261120
- Jean-Philippe Tanguy, 20 novembre 2026 : « On n'a donc plus le droit d'être ami avec quelqu'un du Rassemblement national et de venir voir son ami au siège du Rassemblement national ? » — https://www.franceinfo.fr/politique/front-national/des-rumeurs-et-des-accusations-sans-fondement-reagit-jean-philippe-tanguy-dans-l-affaire-du-prefet-soupconne-d-avoir-renseigne-le-rn-sur-des-affaires-en-cours_8291828.html
- Laurent Nuñez, 20 novembre 2026 : « Si ces faits sont avérés, c'est très grave, ça jettera le discrédit sur le ministère de l'Intérieur. » — https://www.franceinfo.fr/societe/justice/direct-si-les-faits-sont-averes-ils-sont-evidemment-tres-graves-laurent-nunez-convoque-le-prefet-hugues-moutouh-soupconne-d-avoir-transmis-des-informations-sensibles-au-rassemblement-national_8291756.html
- Laurent Nuñez, 20 novembre 2026 : « J'ai besoin de l'entendre, d'écouter ce qu'il a à me dire. Ma main n'a jamais tremblé quand il y avait des décisions à prendre, croyez-le bien » — https://www.cnews.fr/france/2026-11-20/si-les-faits-sont-averes-ils-sont-tres-graves-laurent-nunez-reagit-laffaire-des
- Hugues Moutouh, 21 novembre 2026 : « Me faire passer pour un nervi à la solde d'un parti est odieux, me désigner comme étant une taupe est immonde. » — https://www.lejdd.fr/politique/me-designer-comme-une-taupe-est-immonde-le-prefet-hugues-moutouh-se-defend-et-dit-sa-verite-au-jdd-189351
- Edwige Diaz, 21 novembre 2026 : « C'est une victoire idéologique » — https://www.bfmtv.com/politique/video-loi-sur-la-presomption-d-usage-legal-des-armes-par-les-forces-de-l-ordre-adoptee-c-est-une-victoire-ideologique-pour-le-rassemblement-national-se-felicite-edwige-diaz-senatrice-rn_VN-202611210430.html
- David Lisnard, 22 novembre 2026 : « Je confirme que cette primaire devrait se tenir entre tous ceux qui se prétendent de la droite et du centre. Gabriel Attal dit qu'il est de droite, ce dont je doute, fort bien, qu'il participe. Reconquête devrait aussi pouvoir y concourir s'il en respecte les conditions d'accès » — https://www.cnews.fr/france/2026-11-22/primaire-de-la-droite-et-du-centre-je-ne-demanderai-pas-gabriel-attal-de-me
- David Lisnard, 22 novembre 2026 : « Je veux l'éliminer de la compétition » — https://www.bfmtv.com/replay-emissions/le-grand-oral-2027/video-je-veux-l-eliminer-de-la-competition-declare-david-lisnard-candidat-a-l-election-presidentielle-pour-justifier-d-ouvrir-a-eric-zemmour-une-primaire-de-la-droite-et-du-centre_VN-202611220360.html
- Gérard Larcher, 19 novembre 2026 : « ne fait pas partie de ceux que je souhaite convier à débattre » — https://www.bfmtv.com/politique/elections/presidentielle/presidentielle-gerard-larcher-ne-ressent-pas-de-proximite-avec-eric-zemmour-et-ne-souhaite-pas-l-inclure-dans-la-primaire-de-la-droite_AV-202611190987.html
- Laure Lavalette, 19 novembre 2026 : « Je ne vais pas me justifier de ce qu'il s'est passé il y a 30 ans dans un climat qui était tout à fait différent. Peut-être que je ne ferais pas la même chose maintenant » — https://www.lefigaro.fr/elections/presidentielles/le-climat-n-etait-pas-le-meme-accusee-d-avoir-cautionne-des-ecrits-antisemites-laure-lavalette-invoque-des-faits-vieux-de-30-ans-20261119
- Laure Lavalette, 19 novembre 2026 : « J'ai marché, moi, contrairement à d'autres, à la marche contre l'antisémitisme » — https://www.sudouest.fr/politique/marine-le-pen/laure-lavalette-je-ne-vais-pas-me-justifier-dit-la-deputee-du-rn-accusee-d-avoir-cautionne-des-ecrits-antisemites-durant-ses-etudes-a-bordeaux-31582634.php

Écarté : phrases d'Attal (page franceinfo en 404), de Boris Vallaud (fonction absente de la page), doublons des phrases du relevé automatique. Le Monde et Libération bloquent la lecture automatique.

Cache `onrecord-v54`.

## 2026-11-22 — relevé automatique

Tu pars des flux publics des dernières 48 heures. Tu publies 6 phrases et 1 fiche. Pas de photo : monogramme.

- Marine Le Pen, 22 novembre 2026 : « Je n'ai jamais reçu d'information confidentielle et je n'en ai jamais demandé » — https://www.radiofrance.fr/franceinter/podcasts/franc-jeu/franc-jeu-du-dimanche-22-novembre-2026-2672721
- Marine Le Pen, 22 novembre 2026 : « Il n'y a pas de discrimination d'État ou systémique. » — https://www.radiofrance.fr/franceinter/podcasts/franc-jeu/franc-jeu-du-dimanche-22-novembre-2026-2672721
- Éric Zemmour, 22 novembre 2026 : « Un vent mauvais souffle sur notre pays. Un vent liberticide, qui fait régner un totalitarisme d'atmosphère. On veut interdire des mots, des expressions, des théories » — https://www.europe1.fr/politique/presidentielle-eric-zemmour-se-pose-en-candidat-de-la-liberte-de-parler-face-au-totalitarisme-datmosphere-1241899?at_medium=RSS%20feeds&at_campaign=Flux%20Generique
- Éric Zemmour, 22 novembre 2026 : « On nous dit que nos mots sont trop durs. Mais ce ne sont pas nos mots, le problème : c'est le réel qu'ils décrivent [...] Je serai le candidat de la liberté, la liberté de penser, la liberté de parler » — https://www.europe1.fr/politique/presidentielle-eric-zemmour-se-pose-en-candidat-de-la-liberte-de-parler-face-au-totalitarisme-datmosphere-1241899?at_medium=RSS%20feeds&at_campaign=Flux%20Generique
- Sandrine Rousseau, 21 novembre 2026 : « Il doit être mis à pied » — https://www.franceinfo.fr/france/centre-val-de-loire/loiret/prefet-soupconne-de-fuites-vers-le-rn-il-doit-etre-mis-a-pied-estime-la-depute-ecologiste-sandrine-rousseau_8293574.html#xtor=RSS-3-%5Bpolitique%5D
- Mette Frederiksen, 20 novembre 2026 : « Je suis Européenne, Danoise et originaire d'Aalborg. Et je ne suis pas non plus favorable à un grand remplacement de la population. Je crois qu'il doit y avoir une culture majoritaire forte » — https://www.lefigaro.fr/international/danemark-concurrencee-a-droite-sur-l-immigration-la-premiere-ministre-mette-frederiksen-evoque-un-grand-remplacement-20261120

Écarté, en file d'attente (23) : ce qui n'était pas dans la page mot pour mot, hors date, hors sujet, déjà en ligne, douteux, ou personne non établie. La page admin les montre.

Cache `onrecord-v53`.

## 2026-11-22 — v52 : dimensions

Tu enregistres d'abord `version-2026-11-22-avant-dimensions`. Aucune donnée ni le relevé du matin ne changent.
- Barre du bas : quatre colonnes égales et centrées (elle en comptait encore sept, les onglets se tassaient à gauche) ; largeur limitée sur tablette. Sur ordinateur, les onglets sont centrés dans la barre du haut.
- `html,body{overflow-x:hidden}` faisait de `body` un conteneur de défilement : la barre du haut (sticky) partait au défilement et les onglets restaient seuls, en blanc sur la page. Remplacé par `overflow-x:clip` ; les en-têtes collants de l'Échelle et des listes marchent aussi. `scroll-margin-top` sur les cartes pour qu'un saut ne finisse pas sous ces en-têtes.
- Enquête : champ de recherche à pleine largeur, champs « Relier deux noms » au même style (côte à côte sur grand écran), dossier et chemin amenés à l'écran quand on les ouvre. Les URL longues des citations reviennent à la ligne (le dossier débordait de 55 px sur mobile).
- Champs à 16 px minimum (pas de zoom iOS), segments de filtre dimensionnés selon le texte.

Cache `onrecord-v52`.

## 2026-11-22 — relevé automatique

Tu ne publies aucune phrase. 16 éléments attendent une relecture sur la page admin.

## 2026-11-19 — relevé automatique

Tu ne publies aucune phrase. 16 éléments attendent une relecture sur la page admin.

## 2026-11-18 — v51

Tu enregistres d'abord `version-2026-11-18-avant-enquete`. La barre passe à quatre onglets. Les anciennes adresses restent. Le réseau se feuillette en cartes. L'enquête rapproche les déclarations d'intérêts publiques de la HATVP, sans adresse, sans patrimoine, sans nom de conjoint. Le relevé du matin n'est pas modifié.

Cache `onrecord-v51`.

## 2026-11-18 — v50

Tu remets la photo en fondu sur les cartes carrée et story, seulement quand elle est déjà sur la fiche. Sans photo : le monogramme. Le crédit apparaît si la licence le demande. Tu ne touches pas au relevé du matin.

Cache `onrecord-v50`.

## 2026-11-18 — v49

Tu ne publies aucune phrase. Tu enregistres d'abord l'état du site sous le tag `version-2026-11-18-avant-cartes`. Tu ajoutes deux gestes sur la page admin : enregistrer une version, revenir à une version, sans réécrire l'historique. Tu ajoutes aussi, sur chaque citation, une image carrée et une image story (monogramme, citation entière, lien `/c/…`).

Cache `onrecord-v49`.

## 2026-11-18 — relevé, citations entières

Tu ne publies aucune phrase. Tu corriges le relevé du matin après le test à blanc : une citation coupée au milieu d'un mot ne passe plus, les points de suspension ajoutés non plus, et une ellipse `[…]` seulement si chaque morceau est dans la page. Les seize lectures se répartissent (deux pages par personne, trois par média, deux phrases publiées par personne). Une phrase déjà en ligne, même plus courte, n'est pas reprise. Le résumé nomme le flux qui a échoué. Le cache reste `onrecord-v48`.

## 2026-11-18 — v47

Tu ne publies aucune phrase. Tu poses le relevé du matin dans le dépôt : chaque jour, vers 8 h (heure de Paris), un workflow lit les flux publics, fait relire les pages par Gemini avec une clé gratuite, et ne publie que ce qui passe les contrôles. Le reste va dans la file d'attente, sur la page admin (`auto_pending.json`, à la racine, parce que le dossier `tools/` n'est pas servi). Sans clé, le workflow s'arrête et ne touche pas à main. Le mode d'emploi est dans `docs/REPRISE.md`, section Automatisation.

Cache `onrecord-v48`.

## 2026-11-17 — v46

Tu pars du matin du 16 novembre (v45) et tu vas jusqu’au 17 novembre, vers 8 h. Tu ne recopies aucune phrase déjà en ligne. Tu publies ce que les pages contiennent mot pour mot.

Tu ajoutes quarante et une phrases, une fiche (Bruno Le Maire) et sept liens. Pas de photo libre : monogramme. `tests/test_v22.py` : « elu » passe à 44. Jean-Luc Mélenchon, Raphaël Glucksmann et Yonathan Arfi, jusque-là seulement dans Gaza, entrent aussi dans la section France. La catégorie « Associations & représentants », posée hier pour l’AJC, entre dans `category_order`.

- Marine Le Pen, 16/11/2026, débat LCI aux Restos du Cœur : 15 à 16 % d’étrangers dans le logement social, « pas de les expulser », « une priorité » et non une exclusivité, « Moi je pique pas les logements des gens », « ramassis de gauchistes » pour la LDH, l’association qui appelle à voter doit « se constituer en parti politique », « Nous allons arrêter de subventionner les associations politisées », et elle dit qu’il n’est pas question de toucher aux dispositifs des Restos du Cœur. Vidéo LCI / TF1 Info. — https://www.franceinfo.fr/elections/marine-le-pen-critiquee-en-plein-debat-de-la-presidentielle-pour-sa-volonte-de-couper-les-subventions-des-associations-politisees_8285558.html et https://lcp.fr/actualites/logement-associations-jeunesse-ce-qu-il-faut-retenir-du-debat-presidentiel-sur-lci
- Gabriel Attal, même débat : Hayange, le maire RN, le Secours populaire et la justice ; les associations « au garde-à-vous » ; les associations qui accompagnent les migrants et la LDH ; « Où est-ce que vous trouvez les 3 milliards ? » ; priorité au « fait de travailler ». Il ne nomme pas le maire. Les pages lues ne citent pas de réponse de Marine Le Pen sur Hayange. — https://www.franceinfo.fr/elections/marine-le-pen-critiquee-en-plein-debat-de-la-presidentielle-pour-sa-volonte-de-couper-les-subventions-des-associations-politisees_8285558.html
- Raphaël Glucksmann, même débat : « le tri dans le logement social », « ségrégation spatiale, géographique », « telle ou telle association est politique », « complètement délirant », et « C’est totalement vrai » sur Hayange. — https://www.huffingtonpost.fr/politique/article/au-debat-de-tf1-lci-marine-le-pen-en-grande-difficulte-sur-le-financement-des-associations_359471.html
- Jean-Luc Mélenchon, même débat : pas de tri entre les populations à loger ; « C’est les communes qui décident » ; « savoir mieux que les conseils municipaux » ; « Ça c’est vrai » sur Hayange. Le même jour, i24NEWS cite son message : « condamnation du génocide » assimilée à l’antisémitisme, « opération coordonnée », « sondage bidon ». La phrase d’i24NEWS qui contient des crochets sur Le Parisien n’est pas reprise. — https://www.i24news.tv/fr/actu/france/artc-antisemitisme-melenchon-denonce-un-sondage-bidon-arfi-l-accuse-de-complotisme
- Bruno Retailleau, même débat : « Priorité au travail », face à la priorité nationale. — même page LCP
- Yonathan Arfi, 16/11/2026, réponse citée par i24NEWS : « Le problème c’est vous : vos mots, vos silences, vos menaces » ; « intimidations » et « complot » ; « un complot des médias ne sera jamais un démenti ». Une autre phrase de la même réponse n’est pas reprise. — même page i24NEWS
- Charles Rodwell, 16/11/2026, Europe 1 : « coup d’arrêt à l’immigration », niveaux « insoutenables », immigration « massivement réduite », « assécher toutes les autres voies », ministère « de l’immigration. Et de l’identité nationale », « quotas drastiques », et Nicolas Sarkozy « avait vu juste en 2007 ». La phrase du 15 novembre déjà en ligne n’est pas recopiée. — https://www.europe1.fr/societe/mon-objectif-est-de-mettre-un-coup-darret-a-limmigration-affirme-le-depute-epr-charles-rodwell-1237257 et https://www.europe1.fr/societe/reprendre-le-controle-charles-rodwell-propose-de-retablir-le-ministere-de-limmigration-et-de-lidentite-nationale-1237329
- Bruno Le Maire (nouvelle fiche), 16/11/2026, CNews : « CNEWS fait partie de la liberté et de la diversité de la presse ». — https://www.cnews.fr/france/2026-11-16/cnews-fait-partie-de-la-liberte-et-de-la-diversite-de-la-presse-considere-bruno

Écarté, en une ligne : posts X du relevé dont la phrase n’a pas été relue sur une page qui répond (Camus, Caron, Aliot, Odoul, Goldnadel, de Villiers, Klarsfeld, Portes, Philippot, Rioufol, comptes RN, Chenu, Alloncle, Maréchal déjà en ligne) ; retraites, SMIC, TVA, permis, GTA, sondages, Ukraine, promotions d’émissions ; Gaza, communiqués du Royaume-Uni, de l’Italie, de l’Australie, du Canada et de Kaja Kallas, la France n’est pas l’auteur ; Barrot à Bruxelles sur Gaza Now, Anadolu Agency paraphrase et la transcription du Conseil est automatique ; décision européenne du 16/11 sur Gaza Now, texte du Conseil, pas une phrase de lui ; condamnation de Barbara Lefebvre du 13/11, déjà examinée le 14/11, hors de la fenêtre ; pas de décision nouvelle de l’Arcom ; particuliers (témoins du débat, lycéens, fille citée par Odoul, personne détenue nommée par Portes) ; « complices » dans une phrase d’Arfi, le mot ne peut pas entrer dans le fichier ; Face à Jordan Bardella annoncé pour le 17 au soir, pas encore diffusé ; réforme des retraites de Marine Le Pen annoncée pour le 17, pas encore tenue au moment de la lecture.

Les pages nouvelles ont une copie Wayback, y compris France 24. Les quatre pages du Parisien déjà en échec sont relancées : toujours l’erreur 520. Les messages X déjà en échec ne sont pas relancés un par un : l’erreur 523 se répète depuis le 14/11.

Cache `onrecord-v46`.

## 2026-11-16 (matin) — v45

Tu pars du relevé v44, lu jusqu’au 16/11 vers 2 h, et d’un second relevé X (92 comptes, depuis le 14/11 6 h). Tu ne recopies aucune phrase déjà en ligne. Tu publies ce que les pages du matin contiennent mot pour mot.

Tu ajoutes vingt-quatre phrases, trois fiches (American Jewish Committee, Anne-Sophie Sebban-Bécache, Olivier Rioult) et sept liens. Pas de photo libre : monogramme. `tests/test_v22.py` : « asso » passe à 21, « elu » à 43.

- American Jewish Committee, page datée du 15/11/2026, enquête Ifop avec la Fondapol : l’extrême droite et l’extrême gauche dans les causes perçues de l’antisémitisme (25 % chacune) ; sympathisants du RN et de LFI ; 58 % / 53 % / 47 % pour Mélenchon, Zemmour et Le Pen ; 69 % et 31 % à l’hypothèse d’une élection de Mélenchon ou de Le Pen ; 79 % des Français juifs se sont sentis rendus responsables des actions du gouvernement israélien ; 49 % des 18-24 ans sur la comparaison avec les nazis ; 82 % disent avoir déjà été victimes d’un acte antisémite. — https://ajcfrance.com/radiographie-de-lantisemitisme-en-france-edition-2027/
- Anne-Sophie Sebban-Bécache, 16/11/2026, France Inter, 6 h 20 : « Quelque chose s'est fissuré », « Une frontière s'est déplacée », « les deux extrêmes utilisent cette question de l'antisémitisme et la nourrissent », « tolérance zéro ». « les deux extrêmes » est sa formule. Lien vers l’AJC. — https://www.radiofrance.fr/franceinter/podcasts/l-invite-de-6h20/la-question-de-6h20-du-lundi-16-novembre-2026-4955302
- Olivier Rioult, 16/11/2026, Sud Radio : agression visant des militants du RN et de La Cocarde, « milice d’extrême-gauche », « cherchaient des fascistes », « nous nazifier ». Il ne nomme personne. « Je pense » et « les mots qui m’ont été rapportés » restent dans les phrases. Lien vers le RN. — https://www.sudradio.fr/faits-divers/marseille-de-jeunes-militants-du-rn-agresses-dans-un-bar
- Nicolas Sarkozy, entretien au Figaro du 13/11/2026, phrases lues dans le JDD du 15/11 à 1 h et dans BFMTV du 13/11 : C8, « bien étrange et dangereuse conception de la démocratie » pour CNews, L’Humanité, journalistes menacés, « géométrie variable », et « Vouloir interdire LFI ou le RN, les deux partis donnés par les sondages au deuxième tour de la présidentielle, c’est là encore une curieuse vision de la démocratie ». Ces phrases n’étaient pas sur la fiche, qui avait seulement la primaire. Liens vers CNews et le RN. — https://www.lejdd.fr/Societe/c8-cnews-nicolas-sarkozy-denonce-une-dangereuse-conception-de-la-democratie-188706 et https://www.bfmtv.com/politique/elections/presidentielle/une-curieuse-vision-de-la-democratie-nicolas-sarkozy-se-dit-contre-l-interdiction-de-lfi-suggeree-par-bruno-retailleau_AN-202611130717.html

Écarté, en une ligne : les phrases déjà en v42, v43 ou v44 (Goldnadel, Mélenchon et le livre de Rima Hassan, Lévy, Ciotti, Zemmour, Tondelier, Maréchal, Le Gallou, Odoul, Bompard à Nice, Dupont-Aignan, Onfray, Montbrial, Jadot, Ridel, Alloncle sur l’égard démocratique, Rodwell, Chenu, Panot, le RN sur l’ordre, Rousseau, Retailleau) ; Ukraine, Riner, bac, carburant, permis, SMIC, retraites, sondages et titres sans phrase nouvelle ; Crépol, audience du 16/11 sans décision et mis en cause mineurs non nommés ; Gaza, communiqués de Kaja Kallas et du Royaume-Uni, de l’Italie, de l’Australie et du Canada, la France n’est pas signataire ; pas de décision nouvelle de l’Arcom ; Bompard, le mot « complicité » reste hors du fichier ; Chloé Ridel sur la forêt de Saint-Cloud, insinuation pénale ; posts X (Autain, Faure, Rima Hassan, Karl Olive, Copé) dont la phrase exacte n’a pas été relue sur une page qui répond ; particuliers (Marlone, auditeurs, victimes non nommées au-delà du fait déjà dit) ; Alain Destexhe, pas une personnalité française.

Cache `onrecord-v45`.

## 2026-11-16 (relevé X) — v44

Tu pars d’un relevé de 154 posts (32 comptes), lus via l’API X entre le 13/11 et le 16/11, 2 h. Tu en publies 52. Les autres sont écartés. Les phrases déjà en ligne (v42, v43) ne sont pas recopiées. Quinze fiches nouvelles, sans photo libre : monogramme. `tests/test_v22.py` : « elu » passe à 42, « jour » à 25.

Comptes déjà sur le site :

- Bruno Retailleau, 13/11, 9:17, X : « Il y a trop d’immigration en France. Pour reprendre le contrôle de notre politique migratoire, je donnerai la parole aux Français par référendum. » — https://x.com/BrunoRetailleau/status/2121155423986180396
- Fabien Roussel, 13/11, 15:43, X : « Le Rassemblement National est un poison contre le peuple » et « nous diviser en fonction de nos origines ». — https://x.com/Fabien_Roussel/status/2121252617825247563
- Geoffroy Lejeune, 13/11, 11:51, X : « le sujet, c’est de savoir si le voile est français ». — https://x.com/GeoffroyLejeune/status/2121194259273404891
- Gilles-William Goldnadel, 14/11 et 15/11, sept messages sur X : pièce sur Gaza et France Inter, Saint-Denis, « Parti Antisémite », le RN dit « d’extrême droite », Gaza comme « vil fantasme », Nora Hamadi et Marine Le Pen, Amnesty et Francesca Albanese. — https://x.com/GWGoldnadel/status/2121531263739650356
- Jean-Luc Mélenchon, 14/11, 16:54, X : « France inter tient une tranchée absurde contre la cause palestinienne » et le livre de Rima Hassan. — https://x.com/JLMelenchon/status/2121632985321496587
- Jordan Bardella, 13/11, X, 21:08 : « Avec Marine Le Pen, on est riches de nos complémentarités. » — https://x.com/J_Bardella/status/2121334296170406348
- Jordan Bardella, 13/11, LCI, cinq phrases citées par @LCI : interdiction de manifester pour les personnes fichées, « perdre le contrôle » sécuritaire, l’attentat de Trappes (suspect non nommé, présumé innocent), « couple exécutif » avec Marine Le Pen, « il faut parler comme le Rassemblement national ». — https://x.com/LCI/status/2121323705137573988
- Élisabeth Lévy, 15/11, 19:07, X : les insoumis « ciblent les chaînes d’information, les accusant de racisme ». — https://x.com/ELevyCauseur/status/2122028803845140813
- Marine Le Pen, 13/11, CNews : « laisser les autres candidats faire campagne sans faire l'objet d'intimidations ». — https://x.com/CNEWS/status/2121274837750493202
- Marine Le Pen, 13/11, LCI : « Ils n'arrivent même pas à se mettre d'accord sur les critères pour choisir un seul candidat. » — https://x.com/LCI/status/2121241582527508582
- Marine Le Pen, 15/11, X : priorité aux Français pour le logement social ; APL réservées aux Français et aux étrangers ayant travaillé cinq ans ; elle dit avoir « commis une erreur » en proposant l’interdiction de la double nationalité. — https://x.com/MLP_officiel/status/2122030794189181288 et https://x.com/MLP_officiel/status/2122036013514301653
- Marine Tondelier, 15/11, 20:07, X : Macron « avait promis d'être l'antidote au vote d'extrême droite » et « elle n'a jamais été aussi haute ». — https://x.com/marinetondelier/status/2122043729414357402
- Marion Maréchal, 16/11, 0:12, X : à Marseille, « une quinzaine d’individus cagoulés » attaquent des militants du RN et de la Cocarde, 3 blessés, aucun nom. — https://x.com/MarionMarechal/status/2122105573546050039
- Éric Ciotti, 14/11, 20:31, X : « Nier le lien entre l’immigration et les émeutes est une faute et une folie ». — https://x.com/eciotti/status/2121687539006292151
- Éric Zemmour, 15/11, 21:30, X : « je suis le seul à proposer une politique d’immigration négative ». — https://x.com/ZemmourEric/status/2122064723352924442
- Éric Zemmour, 15/11, JDD cité par @leJDD : « Tout faire pour que notre avenir soit français ». — https://x.com/leJDD/status/2121828049071050926
- Jules Torres, 15/11, CNews : « sur l’immigration, il a un programme », à propos d’Éric Zemmour. — https://x.com/CNEWS/status/2122095908103823377
- Rassemblement national, 13/11 et 14/11, X : « la confiance et l’amitié » entre Marine Le Pen et Jordan Bardella ; « de l'ordre dans la rue, dans nos comptes publics et à nos frontières ». — https://x.com/RNational_off/status/2121334707958972554
- Gabriel Attal, 13/11, BFMTV : Jad Zahab, son porte-parole, « Monsieur Zemmour n'est pas invité dans cette primaire ». Lien d’opposition vers Éric Zemmour. — https://x.com/BFMTV/status/2121288509818314754

Fiches nouvelles :

- Mathilde Panot, 13/11 et 15/11, X : salon Icube et colonies en Cisjordanie ; documentaire NAZA, « processus de déshumanisation ». — https://x.com/MathildePanot/status/2121273706924175854
- Jean-Yves Le Gallou, 15/11, 23:59, X : la Suède et « tout débat sur la remigration ». — https://x.com/jylgallou/status/2122102144966742481
- Julien Odoul, 15/11, X : « Qu’est-ce qu’il y a d’extrême chez » Marine Le Pen ? — https://x.com/JulienOdoul/status/2121994894306693279
- Florian Philippot, 15/11, X : « On se débarrasse du torchon bleu à étoiles en plein Paris ». — https://x.com/f_philippot/status/2121956505607966852
- Ivan Rioufol, 13/11, X : il parle d’une « synthèse Knafo-Zemmour » et dit qu’on lui a attribué des propos à tort. — https://x.com/ivanrioufol/status/2121298910794903629
- Manuel Bompard, 14/11, X : « Des groupuscules d’extrême droite à Nice ont fait savoir que nous n’étions pas les bienvenus. » Le 15/11, il écrit que CNews a « essayé de manipuler des commerçants marseillais ». — https://x.com/mbompard/status/2121728155857613159
- Nicolas Dupont-Aignan, 14/11, X : « Marine Le Pen l’a abandonnée » (la sortie de l’Union européenne). — https://x.com/dupontaignan/status/2121601389662994662
- Michel Onfray, 14/11, CNews : « Marine Le Pen n'est pas son père, le RN ce n'est plus le FN ». — https://x.com/CNEWS/status/2121586073255960975
- Thibault de Montbrial, 15/11, CNews : « une surreprésentation des étrangers dans la violence » ; « je voterais pour Marine Le Pen ». Europe 1 : « Sans aucune hésitation, je voterai pour Marine Le Pen ». Lien vers Marine Le Pen. — https://x.com/CNEWS/status/2121921263283122358
- Yannick Jadot, 15/11, BFMTV : « Je n'en vois qu'un qui peut battre Marine Le Pen, c'est Raphaël Glucksmann ». — https://x.com/BFMTV/status/2122094349211030011
- Chloé Ridel, 14/11, Europe 1 : « On ne peut pas avoir un second tour Le Pen/Mélenchon ». — https://x.com/Europe1/status/2121654530647445944
- Charles Alloncle, 15/11, LCI : traiter l’adversaire de Marine Le Pen « avec exactement le même égard démocratique ». — https://x.com/LCI/status/2122062419409199467
- Charles Rodwell, 15/11, JDD : « Il faut diviser les entrées par quatre ». — https://x.com/leJDD/status/2121847705613844851
- Raphaël Stainville, 13/11, CNews : « cracher leur haine sur Israël » et « se victimiser », sur l’interdiction visant Jean-Luc Mélenchon et Mathilde Panot. — https://x.com/CNEWS/status/2121265949558895065
- Sébastien Chenu, 15/11, X : « La liberté d’expression sera l’un des grands combats de 2027. » — https://x.com/sebchenu/status/2121923164955668823

102 posts écartés : 14 déjà en ligne ou même phrase gardée une seule fois ; 46 hors sujet (Ukraine, Riner, bac, pouvoir d’achat, permis, SMIC, 35 heures, Frexit sans propos sur le RN, promotions, logistique) ; 22 titres, sondages ou paraphrases sans phrase exacte ; 8 particuliers ou propos anonymes ; 6 qui ne viennent pas d’une personnalité publique française ; 4 fragments ou citations dont le message cité manque ; 2 qui contiennent « complicité », mot exclu du fichier de données.

Les 52 URL X ont été soumises à la Wayback Machine : toutes échouent (erreur 523 ou coupure TLS), comme les messages X déjà en échec.

Cache `onrecord-v44`.

## 2026-11-16 (complément) — v43

La v42 du même jour était trop courte. Tu reprends du 13 au 16 novembre, sans republier les phrases déjà en ligne.

Tu ajoutes sept phrases, une fiche (Nicolas Sarkozy) et un lien.

- Bruno Retailleau, 13/11/2026, Les 4V, France 2, retranscription franceinfo : « il y a trop d'immigration en France […] accueillir beaucoup moins et […] expulse beaucoup plus » ; « il n'y a pas de politique d'immigration en France ». Il dit que Marine Le Pen « ne respecte pas la Constitution » et que « les maires n'organiseront pas son référendum ». Lien « opposition » vers Marine Le Pen. Vidéo franceinfo — https://www.franceinfo.fr/politique/vous-avez-en-france-des-minorites-bruyantes-agissantes-violentes-qu-on-laisse-agir-affirme-bruno-retailleau-a-propos-du-mouvement-social_8280638.html
- Bruno Retailleau, même entretien : « La France n'est pas raciste. La France n'a jamais été raciste, mais il y a des discriminations. » Il nomme Trappes (« racisme anti-maghrébin, anti-africain, anti-musulman ») et Crépol (« racisme anti-blanc »). Le suspect de Trappes n'est pas nommé. Même URL.
- Bruno Retailleau, même entretien : « je ne dis jamais islamophobe parce que c'est un terme qui a été forgé par les Frères musulmans, je dis anti-musulman ». Même URL.
- Marine Le Pen, 13/11/2026, salon du Made in France, 23h info de franceinfo : « une priorité nationale dans la commande publique ». Vidéo franceinfo — https://www.franceinfo.fr/economie/industrie/made-in-france-quand-la-presidentielle-s-invite-au-salon_8282180.html
- Jordan Bardella, 13/11/2026, 21:24 UTC, X : « Au bout de 6 mois, un étranger sans contrat de travail devra partir. La France n'est ni un hôtel, ni un guichet social ! » Texte lu sur la copie Nitter, x.com ne répondant pas. URL du post — https://x.com/J_Bardella/status/2121353541805592926
- Nicolas Sarkozy (nouvelle fiche, portrait Commons CC BY-SA 2.5, Aleph), 13/11/2026, Le Figaro cité par BFMTV : « si primaire il y a, elle doit être large » et « tous ceux qui s'engageront à en respecter les règles devront pouvoir y concourir ». Il ne nomme pas Éric Zemmour. BFMTV pose la question de l'inclure, dans le contexte de sondages Le Pen–Mélenchon — https://www.bfmtv.com/politique/cet-exercice-n-a-d-interet-que-s-il-rassemble-nicolas-sarkozy-plaide-pour-l-organisation-d-une-large-primaire-de-la-droite-et-du-centre_AN-202611130733.html

Écarté : Kaja Kallas (14/11) et le communiqué du 15/11 (Royaume-Uni, Italie, Australie, Canada) — pas une personnalité française, la France n'est pas signataire du second ; Gérard Larcher (14/11) — les phrases entre guillemets ne nomment ni le RN ni l'extrême droite ; Jean-Charles Orsucci (14/11) — Politique Matin paraphrase l'exclusion de Zemmour, la page BFMTV ne donne pas la phrase ; Thomas Ménagé (14/11) — pas de citation exacte sur le racisme, seulement le bac ; message de Bardella du 14/11 sur l'université — il vise « l'extrême gauche », hors des deux sujets ; dédicaces de Bardella et de Knafo — pas de phrase nouvelle sur les sujets ; Barbara Lefebvre, condamnation du 13/11 — l'UJFP (partie civile) et L'Humanité ne donnent pas la même phrase, le jugement n'a pas été lu ; livret de Retailleau sur le droit du sol — fichier daté du 11/11, annonce située au 12/11 par France Inter, hors période ; droits de douane de Zemmour le 13/11 — hors sujet ; Sarkozy ne nomme pas Zemmour, seule la phrase sur le périmètre est retenue ; aucune décision nouvelle de l'Arcom.

Archives : copies pour les deux pages franceinfo, BFMTV (Sarkozy) et la copie Nitter du message de Bardella. Le post x.com échoue encore (erreur 523).

`tests/test_v22.py` : « elu » passe à 31. Cache `onrecord-v43`.

## 2026-11-16 — v42

Tu couvres du 14 au 16 novembre. Rien n'était entré par la page admin (`tools/admin_additions.json` vide).

Tu ajoutes cinq phrases, deux fiches (Sandrine Rousseau, Florence Portelli) et deux liens.

- Sandrine Rousseau (nouvelle fiche, portrait Commons CC BY-SA 4.0, Tilou90), 15/11/2026, BFM Politique : « Présentez-moi un seul candidat qui aujourd'hui n'est pas battu au second tour par Marine Le Pen. La question qui va se poser au second tour c'est ce que va faire le bloc central ». Elle ajoute que si le bloc central « ne voit pas la différence entre les deux », « ce sera le moment de vérité ». BFMTV écrit qu'elle déplore un « signe égal » entre LFI et le RN. Vidéo BFMTV — https://www.bfmtv.com/politique/elections/presidentielle/presidentielle-sandrine-rousseau-appelle-les-ecologistes-a-rejoindre-la-dynamique-de-jean-luc-melenchon-et-marine-tondelier-a-se-retirer_AV-202611150255.html et https://www.bfmtv.com/replay-emissions/bfm-politique/video-invitee-sandrine-rousseau_VN-202611150243.html
- Sandrine Rousseau, même entretien : « avec la montée du fascisme » — la formule est la sienne, les crochets « [pour la présidentielle] » sont ceux de BFMTV. Même URL.
- Sandrine Rousseau, 15/11/2026, cité par TF1 Info : « J'appelle mon parti à rejoindre la dynamique de Jean-Luc Mélenchon ». Elle ne donnera pas son parrainage à Marine Tondelier (« Je ne le donnerai pas ») et l'appelle à se retirer. Lien « autre » vers Jean-Luc Mélenchon, lien « opposition » vers Marine Tondelier — https://www.tf1info.fr/politique/elections/presidentielle/presidentielle-2027-sandrine-rousseau-appelle-marine-tondelier-a-retirer-sa-candidature-2475969.html
- Marine Tondelier, 15/11/2026 au soir, franceinfo cité par Le Parisien : « J'en ai aussi un peu ras-le-bol que, dans des moments aussi difficiles que le nôtre, on se permette parler à tort et à travers en son nom propre ». La phrase est reprise telle que le journal l'imprime. Elle dit aussi que Sandrine Rousseau « cherche la provocation » et que « la question sera tranchée » le 13 décembre — https://www.leparisien.fr/politique/presidentielle-2027-rousseau-appelle-les-ecologistes-a-se-rallier-a-lfi-pour-la-presidentielle-tondelier-denonce-une-provocation-15-11-2026-D3HHDNGM5VEQ7JDCSCYCXE6XA4.php
- Florence Portelli (nouvelle fiche, portrait Commons CC BY 2.0, Jacques Paquier), 14/11/2026, BFMTV : « Ce qui est très inquiétant au-delà des personnes, c'est surtout que les deux extrêmes sont en train d'arriver au second tour ». « Les deux extrêmes » est sa formulation. Le Parisien, le 15/11, donne les chiffres du sondage publié la veille : Marine Le Pen entre 31 et 33 %. Vidéo BFMTV — https://www.bfmtv.com/politique/elections/presidentielle/video-teddy-riner-credite-de-4-5-des-intentions-de-vote-dans-un-sondage-ce-qui-est-tres-inquietant-au-dela-des-personnes-c-est-surtout-que-les-deux-extremes-sont-en-train-d-arriver-au-second-tour-declare-florence-portelli-vice-presidente-des-lr_VN-202611140375.html

Écarté : le communiqué du 14/11 de Kaja Kallas (Union européenne) et celui du 15/11 du Royaume-Uni, de l'Italie, de l'Australie et du Canada sur l'aide à Gaza — pas une personnalité publique française, la France n'est pas signataire du second ; l'appel de Gérard Larcher du 14/11 à une « méthode de départage » — ses phrases citées ne nomment ni le RN ni l'extrême droite, le duel Le Pen–Mélenchon est un résumé de l'AFP sans guillemets ; les dédicaces de Jordan Bardella (Saint-Savin) et de Sarah Knafo (Montauban, Perpignan) — pas de phrase nouvelle sur les deux sujets, la plainte « faux et usage de faux » était déjà écartée le 14/11 ; Thomas Ménagé sur BFMTV le 14/11 — Politique Matin paraphrase, la page BFMTV ne donne en citation exacte que le bac (« Plus aucun lycée ne doit être bloqué »), hors sujet ; l'entourage d'Emmanuel Macron sur l'Ukraine et Marine Le Pen (15/11) — hors des deux sujets ; l'interdiction de la manifestation des Normaux à Rouen — arrêté des 12-13/11, hors période ; l'agression visant des militants RN et de La Cocarde à Marseille (14/11) — particuliers, pas un fait de normalisation ; le livret de Bruno Retailleau sur le droit du sol — page datée du 12/11, déjà publique avant cette mise à jour ; l'échange Zemmour–Bouleau du 10/11 (« délit d'opinion ») — hors période, la candidature TF1 est déjà en ligne ; aucune décision nouvelle de l'Arcom.

Archives : copies Wayback pour l'article BFMTV, la vidéo de BFM Politique, TF1 Info et la vidéo de Florence Portelli. Le Parisien (réponse de Marine Tondelier) échoue encore (erreur 520), comme les trois pages déjà en échec, dont Nantes. Les messages X échouent encore (erreur 523). Une copie déjà en ligne a été retrouvée pour la page vidéo franceinfo de Jean-Luc Mélenchon, en échec depuis le 14/11.

`tests/test_v22.py` : « elu » passe à 30. Cache `onrecord-v42`. Les tests Playwright passent, sauf les 4 cas déjà connus de `tests/test_v5.py` (« graph built lazily on Réseau ») et `tests/test_v8.py`, laissés tels quels.

## 2026-11-14 — v41

La routine du 13/11 n'a rien publié : aucun commit, aucun agent cloud, aucune exécution GitHub Actions entre le 12/11 (`c3b4ad0`) et le 14/11. La cause n'est pas visible depuis le dépôt (l'échec a eu lieu avant toute écriture). Cette mise à jour couvre donc du 11/11 au soir au 14/11. Rien n'était entré par la page admin (`tools/admin_additions.json` vide).

Tu ajoutes huit phrases, une fiche (Jean-Noël Barrot), deux liens et une étape de parcours.

- Jean-Luc Mélenchon, 12/11/2026, X (17:31 UTC), après l'interdiction d'entrée en Israël annoncée le même jour : « Si nous arrivons au pouvoir, nous dirons ce que nous aurons à dire. À savoir : dénoncer le génocide à Gaza, la colonisation en Cisjordanie et l'annexion progressive du Sud-Liban et du plateau du Golan. » Motifs du ministère israélien et rejet par Israël de l'accusation de « génocide » dans la fiche — https://x.com/JLMelenchon/status/2120932595126894785
- Jean-Luc Mélenchon, 12/11/2026, franceinfo : « On m'interdit d'entrer sur un territoire où je n'ai pas demandé à entrer. […] Je regrette que le gouvernement d'Israël me poursuive de cette manière ». Vidéo franceinfo — https://www.franceinfo.fr/politique/la-france-insoumise/israel-interdit-a-jean-luc-melenchon-et-mathilde-panot-l-entree-sur-son-territoire-denoncant-la-position-extremement-anti-israelienne-de-la-france-insoumise_8279801.html et https://www.franceinfo.fr/monde/israel/je-regrette-que-le-gouvernement-d-israel-me-poursuive-de-cette-maniere-denonce-jean-luc-melenchon-interdit-de-territoire-en-israel_8279831.html
- Jean-Noël Barrot (nouvelle fiche, ministre des Affaires étrangères ; portrait Commons domaine public, U.S. Department of State), 12/11/2026, X (18:52 UTC) : « Cette décision démagogique, émanant d'un gouvernement qui a multiplié les violations du droit international, fait le jeu de ceux qui, comme La France insoumise, vivent de l'instrumentalisation du conflit israélo-palestinien. » — https://x.com/jnbarrot/status/2120953009983127868 (cité par LCP : https://lcp.fr/actualites/israel-interdit-son-territoire-a-jean-luc-melenchon-la-reponse-cinglante-du-gouvernement )
- Éric Zemmour, 13/11/2026, Salon du Made in France, vidéo BFMTV : « Tous ces gens-là se retrouvent entre eux. […] c'est la reconstitution de LR et la reconstitution du bloc central. […] » sur la primaire de la droite et du centre — https://www.bfmtv.com/politique/les-republicains/video-je-serai-ravi-d-etre-candidat-dans-cette-primaire-declare-eric-zemmour-candidat-reconquete-a-la-presidentielle-au-salon-made-in-france_VN-202611130526.html
- Gabriel Attal, 13/11/2026, AFP : « certainement pas [à] servir de marche-pied à l'extrême droite dont M. Zemmour est un représentant ». Lien « opposition » Attal → Zemmour — https://www.boursorama.com/actualite-economique/actualites/primaire-a-droite-zemmour-espere-y-participer-mais-attal-ne-veut-pas-40598195eed5b0dd0bb42f30821bddf8 (CNews publie la même phrase : https://www.cnews.fr/france/2026-11-13/presidentielle-2027-eric-zemmour-espere-participer-une-primaire-de-la-droite-et )
- Marion Maréchal, 11/11/2026, Sud Radio : « […] le rempart le plus efficace et le mieux placé pour éviter à tout prix une victoire de Jean-Luc Mélenchon […] c'est de se rassembler autour de Marine Le Pen. » ; ses députés « sont alliés au groupe du Rassemblement national » — https://www.sudradio.fr/sud-radio/marion-marechal-eric-zemmour-devrait-rejoindre-et-soutenir-marine-le-pen
- Marine Tondelier, 12/11/2026, BFMTV, cité par TF1 Info / AFP : « Je ne dis pas que c'est un membre actif du RN qui, au nom de Marine Le Pen, a été assassiner des gens dans les rues […] » ; contexte de l'attentat de Trappes, suspect non nommé et présumé innocent — https://www.tf1info.fr/justice-faits-divers/attentat-de-trappes-le-rn-va-porter-plainte-contre-tondelier-pour-diffamation-2475583.html
- Rassemblement national, 12/11/2026 : Andréa Kotarac, porte-parole de Marine Le Pen, sur franceinfo : « On engagera une procédure judiciaire contre Mme Tondelier » ; plainte annoncée « très prochainement », pas encore déposée selon les articles lus. Lien « opposition » RN → Tondelier — même URL TF1 Info.
- Pierre-Édouard Stérin, étape de parcours du 12/11/2026 : cité à comparaître le 19 janvier 2027 devant la 10e chambre du tribunal correctionnel de Paris pour non-comparution devant une commission d'enquête parlementaire (parquet de Paris via l'AFP). Deux refus selon franceinfo, trois selon LCP ; présumé innocent — https://www.franceinfo.fr/societe/justice/pierre-edouard-sterin-milliardaire-proche-de-l-extreme-droite-sera-juge-en-janvier-pour-son-refus-de-venir-devant-les-deputes_8280011.html et https://lcp.fr/actualites/le-milliardaire-pierre-edouard-sterin-juge-en-janvier-pour-avoir-seche-plusieurs

Écarté : la plainte de Jordan Bardella pour « faux et usage de faux » (12/11) — elle renvoie aux écrits que Mediapart lui attribue, déjà écartés le 11/11 ; son « Grand Entretien » sur LCI (13/11 : sécurité, retraites), hors des deux sujets ; la réaction de Mathilde Panot (pas de fiche) ; les propos d'Édouard Philippe sur les « Français issus de l'immigration » et la réaction de Raphaël Glucksmann (04-08/11, hors de la période) ; aucune décision nouvelle de l'Arcom. Pas de phrase nouvelle trouvée pour les fiches sans citation des coulisses (Durvye, du Rostu, Boëll, Viret, Conrad, Vidal-Revel, Benqué).

Archives : 10 des 13 URL nouvelles ont une copie Wayback (franceinfo sur l'interdiction, franceinfo sur Stérin, LCP ×2, BFMTV ×2, TF1 Info, AFP/Boursorama, CNews, Sud Radio). En échec : la page vidéo franceinfo de Jean-Luc Mélenchon et les deux messages X. Les 17 URL déjà en échec ont été relancées : aucune ne passe. Les trois pages du Parisien, dont Nantes (condamnation pour menaces racistes), échouent encore (erreur 520 puis coupure TLS de web.archive.org) ; les messages X aussi (erreur 523 ou coupure TLS). Le service /save/ de la Wayback Machine coupait souvent la connexion ce soir-là depuis la machine.

Module : `v41_content.py`. Cache `onrecord-v41`. `tests/test_v22.py` : « gouv » passe à 10 (fiche Barrot). `tests/test_v5.py` échoue déjà sur « graph built lazily on Réseau » (4 cas, même échec sur `c3b4ad0`), à ne pas confondre avec une régression.

## 2026-11-12 — v40

Tu corriges l'accueil sans toucher à la palette. La barre de recherche du hero ne recouvre plus les chiffres : la marge négative et le z-index qui tiraient les cartes vers le haut disparaissent. Le bloc « Reprendre » a sa propre marge, au-dessus des accès rapides. ONRECORD garde le blanc Anton ; la lueur externe passe au violet (#8b3dff, #b388ff, #7b2cbf), et un trait néon, un peu moins large que le mot, sépare le titre du slogan.

Tu ajoutes une page privée, https://onrecord-fr.vercel.app/admin.html , non liée depuis le site, en `noindex`. Ta propriétaire y colle un jeton GitHub (fine-grained, Contents lecture/écriture, ce dépôt seulement). Il reste dans le navigateur de l'appareil et ne part que vers api.github.com. Depuis le téléphone elle peut ajouter une personnalité (photo WebP 400 px, ou monogramme), une déclaration, ou un lien du réseau, voir l'aperçu, puis publier. Le commit `admin: ajout …` écrit `tools/admin_additions.json` (et la photo, le crédit). GitHub Actions relance `build.py` et ne commit `data.json` que si le contenu change, pas si seule la date bouge. Aucune citation nouvelle dans cette version. Cache `onrecord-v40`.

## 2026-11-12 — v39

Tu étends l'ambiance du hero à tout le site : fond sombre violacé, cartes en verre, bord violet, titres de section en Anton, liens et pastilles lavande, séparateur ✦. Le sombre néon est le thème par défaut (theme-color et manifeste `#07030f`). Le mode clair, s'il est demandé par l'appareil, reste lisible avec les accents violets. Le hero v38 ne change pas. Aucune citation, aucune source, aucune fiche n'est réécrite.

Sur le Réseau, un interrupteur « Vue 3D » (mémorisé sur l'appareil) affiche les personnes, organisations et médias de `data.json`, avec les mêmes filtres et la même recherche. Constellation canvas, même famille que le hero : nœuds lavande / violet / blanc / rose, taille selon les liens, liens qui pulsent, rotation lente, glisser et pincer. Un toucher met le nœud et ses voisins en évidence et ouvre le panneau déjà en place, avec le lien vers la fiche. La vue 2D vis-network reste là. Le script `vendor/reseau3d.js` ne se charge qu'à l'activation, puis le service worker le met en cache. Pas de WebGL : si le canvas 2D manque, tu restes en 2D. `prefers-reduced-motion` coupe la rotation automatique. Cache `onrecord-v39`.

## 2026-11-12 — v38

Tu ne touches pas au reste de la page. Le haut de l'accueil reprend le visuel sombre : fond presque noir violacé, ONRECORD en blanc avec un halo violet, puis deux lignes en Anton, plus grandes : « ILS L’ONT DIT » en blanc, « ON L’A ARCHIVÉ » en violet néon. Un surlignage violet se dessine sur DIT et ARCHIVÉ. La ligne d'explication, en lavande, reprend Gaza, la banalisation de l'extrême droite en France, et les liens, ces trois bouts en blanc gras surlignés. Le cadre d'ampoules, la guirlande et le voile dépoli disparaissent. Les trois cartes et la recherche passent au verre sombre, bord violet. Le réseau derrière devient une constellation en profondeur, nette, qui tourne, pulse, et suit le doigt, le défilement et l'inclinaison du téléphone. Cache `onrecord-v38`.

## 2026-11-12 — v37

Tu ne changes pas les textes, le mot ONRECORD, les couleurs, ni le mouvement du réseau. Tu rends le haut de l'accueil plus lisible. Le canevas `#hero-net` est légèrement flou et moins contrasté ; un masque le laisse plus discret derrière les phrases et plus visible sur les bords. Derrière « Ils l'ont dit. On l'a archivé. » et la ligne d'explication, un voile violet dépoli (`rgba(36,6,58,.55)`, `backdrop-filter`, coins arrondis, ombre de texte légère). Les trois cartes ont le même verre, un peu plus couvrant, pour les sous-titres. Sans `backdrop-filter`, le voile et les cartes passent à un fond plus opaque. Cache `onrecord-v37`.

## 2026-11-12 — v36

Tu ne changes pas les textes. Tu rends au haut de l'accueil les couleurs d'avant l'enseigne néon : violet `#7b2cbf` / `#3b0a57` (sombre : `#c9a2f5` / `#24063a` / `#5a1a91`), blush `#f6d4e6`, lavande `#e4c2ff`. Le mot ONRECORD garde la taille, le relief, le scintillement et l'inclinaison, mais le dégradé reste dans cette famille. La punchline, le cadre, la guirlande, le projecteur, les trois cartes et le réseau derrière redeviennent blanc, lavande et violet. Plus d'or, de cyan, ni de rose néon. Le mouvement du réseau reste. Cache `onrecord-v36`.

## 2026-11-11 (soir) — v35

Tu ajoutes six phrases et une organisation. Rien de neuf sur Gaza ne passait les règles dans les 48 heures.

- Kévin Pfeffer, 10/11/2026 : première citation de sa fiche. Trésorier du RN selon franceinfo : « accord juridique sur la faisabilité et la solidité du dossier du parti a été trouvé avec deux banques européennes ». Pré-accord, pas un prêt signé ; banques non nommées ; le parti cherche 10,6 millions d'euros. Étape ajoutée à son parcours — https://www.franceinfo.fr/politique/front-national/info-franceinfo-le-rn-a-un-obtenu-un-pre-accord-de-deux-banques-europeennes-pour-financer-sa-campagne-pour-la-presidentielle_8276195.html
- Jordan Bardella, 10/11/2026, « Face à BFM » : « Il n’y a pas de racisme systémique en France. Sinon pourquoi plus de 500.000 personnes voudraient venir chaque année dans notre pays? […] », d'accord « à 300% » avec Marine Le Pen sur CBS — https://www.bfmtv.com/politique/front-national/etat-pro-police-racisme-reforme-des-retraites-ce-qu-il-faut-retenir-du-face-a-bfm-de-jordan-bardella_AN-202611100999.html
- Jordan Bardella, 10/11/2026, X : « Une petite victoire de la démocratie et de la liberté » après le classement de la pétition CNews (texte entier lu sur son compte ; France 24 / AFP cite le même message) — https://x.com/J_Bardella/status/2120164408357740552
- Jordan Bardella, 10/11/2026, X : « Le temps n'est plus à voter pour des partis à 4% […] quand on est patriote comme le sont les électeurs d'Eric Zemmour […] il faut se rassembler. » — https://x.com/J_Bardella/status/2120292537067847764
- Éric Zemmour, 10/11/2026, 20 heures de TF1 : « Je ne veux pas seulement contrôler les flux migratoires, je veux qu'il y ait moins d'immigrés à la fin de mon quinquennat » (RTL), « deux millions », réaction de SOS Racisme (Le Bien public / AFP). Vidéo TF1 Info — https://www.rtl.fr/actu/politique/je-me-presente-pour-conserver-une-france-francaise-eric-zemmour-officialise-sa-candidature-a-la-presidentielle-2027-7900694983 et https://www.tf1info.fr/politique/videos/video-presidentielle-2027-eric-zemmour-officialise-sa-candidature-au-20h-de-tf1-4341-2475122.html
- France terre d'asile (nouvelle fiche, monogramme), 10/11/2026 : avec Désinfox-Migrations, saisine de l'Arcom au sujet de séquences liées au « grand remplacement » sur CNews et Europe 1 ; citation de Jean-François Beaugrand (Sud Ouest / AFP). Deux liens « opposition » vers CNews et Europe 1. Une saisine n'est pas une décision — https://www.france-terre-asile.org/communiques-presse/communiques-de-presse/communique-france-terre-d-asile-et-desinfox-migrations-saisissent-l-arcom-et-publient-un-rapport-sur-la-desinformation-au-sujet-de-l-immigration et https://www.sudouest.fr/international/immigration-un-collectif-de-scientifiques-sort-un-rapport-pour-retablir-les-faits-face-a-la-desinformation-31468731.php

Écarté : discours du 11-Novembre (Marine Le Pen, Jean-Luc Mélenchon), hors des deux sujets ; les propos que Mediapart attribue à Jordan Bardella, qu'il conteste (plaintes annoncées selon BFMTV), ne sont pas repris.

Archives : nouvelles copies pour CBS (article 60 Minutes), BFMTV (VRAI/FAUX Knafo), franceinfo (Boëll à Grasset), Assemblée nationale (classement de la pétition) et pour les nouvelles sources. Toujours en échec : les messages X (erreur 523) et les trois pages du Parisien, dont Nantes (erreur 520). Module : `v35_content.py`. Cache `onrecord-v35`.

## 2026-11-11 — v34

Tu ne touches qu'au haut de l'accueil. ONRECORD devient une enseigne : Anton (OFL, `fonts/anton-latin.woff2`), très grand, en capitales, dégradé magenta / violet / rose / or, halo rose et cyan, profondeur, bref scintillement au chargement, reflet qui traverse les lettres, légère inclinaison au pointeur ou à l'orientation. « Ils l'ont dit. On l'a archivé. » est plus grand, en or, dans un cadre d'ampoules. La ligne d'explication reste petite. Le réseau derrière le texte redevient visible (le masque ne creuse plus le centre), nœuds et liens néon, rotation lente, réaction au doigt et au défilement. Les trois cartes gardent leur inclinaison et gagnent un liseré néon. Le reste de la page ne change pas. Cache `onrecord-v34`.

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
