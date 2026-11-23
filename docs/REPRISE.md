# Reprendre Onrecord

Ce guide permet de continuer le site sans l'assistant qui l'a rédigé. Lis-le en entier avant la première modification. `AGENTS.md`, à la racine, y renvoie : un agent de code le charge tout seul.

## 1. Le projet

Onrecord est une archive citoyenne, gratuite, non commerciale et indépendante. Elle rassemble des **déclarations publiques** et des **liens publics** sur deux sujets :

- la guerre à Gaza ;
- la normalisation de l'extrême droite en France (immigration, « remigration », médias, alliances, institutions).

Le site ne qualifie ni les personnes ni leurs intentions. Chaque élément renvoie à une source. Crédibilité d'abord : une phrase douteuse ne paraît pas.

- Site : https://onrecord-fr.vercel.app/
- Dépôt : `farahei-create/cartographie-gaza-extreme-droite`, branche `main`
- Publication : commit sur `main`, puis `git push`. Pas de pull request. Chaque push sur `main` redéploie Vercel (équipe **valladeaus-projects**).
- Dons anonymes, sans effet sur le contenu : https://www.leetchi.com/fr/c/onrecord-1411528212 (`DONATION_URL` dans `config.js`).

## 2. Architecture

Site statique à la racine. Pas de CDN. Pas d'étape de build côté Vercel : `data.json` est déjà dans le dépôt. `vis-network` 9.1.9 est dans `vendor/` (Apache-2.0 / MIT).

| Fichier | Rôle |
|---|---|
| `index.html` | Page unique, vues en `#/…` |
| `style.css`, `app.js` | Mise en forme et routage |
| `data.json` | Contenu. **Généré.** Ne pas l'éditer à la main |
| `build.py` | Construit `data.json` (personnes, liens, archives, compteurs) |
| `v24_content.py`, `v26_content.py`, `v27_content.py`, `v28_content.py`, `v30_content.py`, `v31_content.py`, `v35_content.py`, `v41_content.py`, `v42_content.py`, `v43_content.py`, `v44_content.py`, `v45_content.py` | Ajouts branchés à la fin de `build.py` |
| `config.js` | `DONATION_URL`, `CORRECTION_EMAIL` |
| `sw.js` | Service worker. La constante `VERSION` doit monter à chaque publication |
| `manifest.webmanifest`, `icons/` | PWA |
| `img/people/`, `img/orgs/` | Portraits et logos hébergés (webp, environ 400 px) |
| `tools/people_images.json`, `tools/org_logos.json` | Crédits (auteur, licence, lien). `build.py` les recopie sur les fiches |
| `tools/archive.py`, `tools/archives.json` | Copies Wayback |
| `.github/workflows/daily-update.yml`, `tools/daily/` | Relevé du matin. Section 10 |
| `.github/workflows/enregistrer-version.yml`, `.github/workflows/revenir-version.yml`, `tools/versions/` | Enregistrer une version, y revenir. Section 11 |
| `versions.json` | Liste de secours des versions, lue par `/admin.html` |
| `c/<id>/<n>.html` | Page d'une citation : lien profond et aperçu des réseaux. Générée par `build.py` |
| `tools/build.v*.py` | Anciens scripts, conservés pour l'historique. Ne pas les lancer |
| `tests/test_v*.py` | Playwright |
| `docs/JOURNAL.md` | Journal daté des mises à jour |
| `contrib.js`, `admin-contrib.js` | Contributions des lecteurs : vue `#/contributions`, bloc des fiches, modération dans `/admin.html`. Section 14 |
| `api/contrib/[action].js`, `lib/contrib/` | Fonction Vercel des contributions (code e-mail, dépôt, signalement, modération). Section 14 |
| `contributions.json` | Contributions validées, écrites par la modération. Ne pas y mettre de donnée privée |
| `package.json`, `vendor/blob-upload.js` | Seule dépendance : `@vercel/blob` (fonction et envoi direct des fichiers). `bash tools/contrib/build_blob_client.sh` reconstruit le fichier du navigateur |

### Données

`data.json` :

- `meta` : `generated`, `methodology`, `counts`, `category_order`, `sections`
- `nodes[]` : personne (`type: person`) ou organisation (`type: org`)
  - `id`, `name`, `role`, `description` (neutres)
  - `category`, `subcategory`, `sections` (`gaza`, `france`)
  - `sphere` (coulisses) : `partis`, `medias`, `argent`, `idees`, `edition`, `institutions`
  - `statements[]` : `quote`, `date` (`AAAA-MM-JJ`), `medium`, `url`, `theme`, `section`, parfois `archive_url`, `archived`, `video`
  - `parcours[]` : étape datée (`date`, `title`, `text`, `url`, `source`, parfois `by` / `verb` si la source dit qui a nommé)
  - `image` + `image_credit`, ou `logo` + `logo_credit`
- `edges[]` : `source`, `target`, `relation`, `url`, `date`, `section`, `nature`, parfois `stories`, `archive_url`

Natures de lien, affichées telles quelles :

- `ascension` : poste, investiture, soutien public, financement ou contrôle documenté
- `opposition` : sanction, procédure, critique, rupture, dissolution
- `coulisses` : lien fixé à la main dans `v24_content.py` (nominations, argent, médias). Ne pas laisser `_nature()` le reclasser : le champ est déjà posé
- `autre` : le reste (ouvrage, réaction, événement)

Thèmes usuels : `Gaza – déclarations`, `France – normalisation de l'extrême droite`, `Proximité extrême droite`, `Médias – structure`, `Nuance / contexte`, `France – montée des violences`. Un thème nouveau apparaît dans les filtres.

### Vues

`#/` accueil · `#/sections` et `#/chronologie` (onglet Citations) · `#/reseau`, `#/pouvoir`, `#/coulisses` (onglet Liens) · `#/enquete` et `#/enquete/<id>` · `#/methodologie` · `#/methode` · `#/contribuer` · `#/credits` · `#/personne/<id>` · `#/organisation/<id>`

La barre du bas a quatre onglets : Accueil, Citations, Liens, Enquête. Méthode est au pied de page et sur l'accueil. Les anciennes adresses continuent d'ouvrir la même vue. `#/enquete/relier/<id>/<id>` montre le plus court chemin documenté.

Onglet Liens (depuis v57) : style épuré, filets fins (`--lx-line`), segments compacts à 13 px, chiffres en chasse fixe (`--lx-mono`), une seule couleur d'accent. Ces règles sont dans le bloc « 23/11 » en fin de `style.css` et ne visent que `#/reseau`, `#/pouvoir` et `#/coulisses`. Garde des cibles de 44 px.

`enquete.json` est produit par `python3 tools/hatvp_sync.py` (liste CSV et XML publics de la HATVP, licence ouverte). Le script ne recopie pas l'adresse, la date de naissance, le patrimoine, les enfants, ni le nom du conjoint. L'activité du conjoint n'entre que si la HATVP la publie. Les propriétaires de médias repris dans le fichier viennent des liens déjà datés et sourcés du site. Un montant d'argent n'est ajouté dans `argent` que avec une date et une URL.

### Mode clair / sombre

Par défaut, le système décide (`prefers-color-scheme`). Le bouton `#theme-btn` (barre du haut) force l'autre mode : attribut `data-theme="light"` ou `"dark"` sur `<html>`, gardé dans `localStorage` sous `onrecord-theme`. Le script du `<head>` (`index.html`, `admin.html`) l'applique avant l'affichage et règle `theme-color`. Dans `style.css`, chaque bloc `@media (prefers-color-scheme: light)` est écrit deux fois : dans le `@media`, sélecteurs précédés de `:where(:root:not([data-theme="dark"]))` ; juste après, la copie précédée de `:where(:root[data-theme="light"])`. Si tu ajoutes une règle pour le mode clair, fais les deux. L'événement `onrecord:theme` redessine le graphe. Les pages `c/…` suivent seulement le système.

### Service worker

`sw.js` met en cache la coque, `data.json`, `config.js` et, à l'installation, chaque `image` et `logo` lu dans `data.json`.

- `data.json` et `config.js` : réseau d'abord, cache en secours
- navigation : réseau d'abord, `index.html` en secours
- le reste : cache, puis mise à jour

**Règle de version.** Dès que le contenu, le style, le script ou une image change, passer `var VERSION = "onrecord-vN"` au numéro suivant (`onrecord-v26`, puis `v27`, etc.). L'activation efface les anciens caches. Oublier le bump laisse d'anciennes fiches sur les téléphones déjà installés.

### `config.js`

`CORRECTION_EMAIL` est **vide**. Les pages `#/methode` et `#/contribuer` demandent alors de copier le message. Ne pas inventer d'adresse.

## 3. Règles éditoriales

Elles viennent du droit français de la diffamation. Aucune exception, y compris pour une « petite » mise à jour ou un brouillon.

1. **Citation exacte**, telle que la source la publie, **datée** (`AAAA-MM-JJ`), **URL vérifiée** (la page répond et contient la phrase). `[ ]` = coupure ou reformulation de contexte par la source, pas par nous.
2. **Formulation neutre** dans `role`, `description`, `relation`, `medium`. Interdit, pour qualifier quelqu'un : « complice », « génocidaire », « pantin », « infiltré ». Également exclus des textes rédigés par le site : « marionnette », « protégé », « copinage », « occulte ». Si la personne a elle-même prononcé un de ces mots, on peut le citer entre guillemets, pas l'employer.
3. **Pas de causalité** que les sources n'écrivent pas. « A nommé », « a financé », « a fait dire » : seulement si la source le dit.
4. **Pas de particuliers.** Personnalités publiques, organisations, décisions d'institutions.
5. **Contexte et démentis** sur la même fiche (thème `Nuance / contexte`, ou précision dans `medium`).
6. **Ne rien inventer.** Si aucune source fiable ne donne une phrase exacte sur les thèmes du site, la fiche reste sans citation nouvelle. Le dire dans le compte rendu.
7. **Photos.** Commons d'abord, licence libre seulement : CC BY, CC BY-SA, CC0, domaine public. Vérifier sur la page du fichier via l'API (`imageinfo` + `extmetadata`) : `LicenseShortName`, auteur, `NonFree` absent. Refuser CC BY-NC, CC BY-ND, fair use. Ensuite, portrait officiel dont le texte autorise la réutilisation : Parlement européen, avec « © European Union » et lien vers https://www.europarl.europa.eu/legal-notice/ . Assemblée nationale et Sénat : seulement si leurs conditions, lues ce jour-là, autorisent la réutilisation ; citer cette condition dans `image_credit`. Jamais : photo de presse, Google Images, capture X ou Instagram, image générée. Héberger un webp d'environ 400 px dans `img/people/`, crédit dans `tools/people_images.json` (auteur, licence, `license_url`, `source_url`). Le crédit s'affiche sur la fiche. L'image à partager (carré et story) reprend cette photo en fondu si le fichier est déjà hébergé ; sinon monogramme. CC BY et la mention « © European Union » sont recopiés en petit sur la carte. CC0 et le domaine public n'ajoutent pas de ligne. S'il y a un contexte ou un démenti, l'image indique « Contexte sur Onrecord ».
8. **Logos.** Uniquement si le fichier Commons a une licence ou un statut qui l'autorise (domaine public, PD-textlogo, CC BY, CC BY-SA, CC0). Sinon monogramme. Pas de logo « à peu près » : un sigle historique d'un autre parti ne remplace pas le bon.
9. **Sans photo libre :** monogramme (initiales, dégradé selon la sphère, sinon selon le type). Pas d'initiales nues sur un aplat.
10. **Vidéos** : diffuseur d'origine ou compte officiel seulement, lien vérifié. YouTube via `youtube-nocookie`, chargé au clic.
11. **Wikipédia n'est jamais la source unique** d'une citation ou d'un fait. On peut s'en servir pour trouver une page Commons, puis vérifier la licence sur Commons.
12. Source primaire (décision, compte officiel, compte rendu) ou média reconnu. Pas un blog partisan comme seule source.
13. Mettre à jour `docs/JOURNAL.md` pour ne pas republier deux fois la même phrase.

## 4. Procédure du jour

À lancer depuis la racine du dépôt.

```bash
git pull origin main
```

Une grosse modification de `app.js`, `style.css` ou `index.html` enregistre toute seule la version d'avant (tag `version-…-avant-modif`). Tu peux aussi en poser une à la main avant de commencer : page `/admin.html`, « Enregistrer la version actuelle ». Détail en section 11.

1. Lire `docs/JOURNAL.md` pour ne pas refaire la veille.
2. Chercher les **48 dernières heures** : presse française et internationale, décisions Arcom, Conseil d'État, justice, comptes vérifiés des personnes déjà sur le site, et d'autres personnalités publiques françaises. Deux sujets seulement : (a) propos publics sur la campagne israélienne à Gaza ; (b) faits qui documentent la normalisation ou la montée de l'extrême droite en France. Repérer aussi une vidéo officielle du moment cité.
3. Si rien ne passe les règles de la section 3 : **ne rien publier.** Le compte rendu dit qu'il n'y a rien.
4. Sinon, ajouter les phrases dans un module du type `v26_content.py` (fonction `apply` branchée dans `build.py`), ou dans `build.py` si c'est le style du passage. Ne pas réécrire les citations déjà en ligne.
5. Archiver les URL nouvelles, puis reconstruire :

```bash
python3 tools/archive.py "https://exemple.fr/article" "https://autre.fr/article"
python3 build.py
python3 -m json.tool data.json > /dev/null
```

`tools/archive.py` interroge la Wayback Machine, demande une capture si besoin, et écrit `tools/archives.json`. Relancer plus tard les URL encore en `"status": "failed"`. `build.py` recopie `archive_url` dans `data.json`.

6. Monter la version du service worker (`sw.js`, `onrecord-vN` → N+1). Les tests `test_v13`, `test_v22`, `test_v23`, `test_v24` comparent cette chaîne : les aligner sur la nouvelle version.
7. Servir le site et lancer les tests (sauf `test_v8`, voir plus bas) :

```bash
python3 -m http.server 8765
# autre terminal, depuis la racine :
ln -sfn . site   # les anciens tests lisent site/data.json et site/sw.js
python3 tests/test_v24.py
python3 tests/test_v22.py
python3 tests/test_v23.py
python3 tests/test_v15.py
python3 tests/test_v14.py
python3 tests/test_v13.py
# puis les autres tests/test_v*.py, sauf test_v8.py
rm site   # ne pas committer ce lien
```

Notes sur les tests (14/11/2026) :

- Les tests écrivent des captures dans `/opt/cursor/artifacts` : créer ce dossier s'il manque (`sudo mkdir -p /opt/cursor/artifacts && sudo chown $USER /opt/cursor/artifacts`). Sans Playwright installé : `python3 -m venv /tmp/pw && /tmp/pw/bin/pip install playwright pillow && /tmp/pw/bin/python -m playwright install chromium`, puis lancer les tests avec `/tmp/pw/bin/python`.
- `tests/test_v22.py` compte les fiches par étage de l'Échelle du pouvoir (`EXPECT`) : une fiche nouvelle demande d'ajuster le chiffre de son étage (ex. « gouv » pour un ministre).
- `tests/test_v5.py` échoue déjà sur « graph built lazily on Réseau » (4 cas, depuis la vue 3D) : échec connu, comme `test_v8.py`.
- Si la machine n'a pas de droit de push (pas de jeton GitHub), la publication passe par un agent cloud Cursor lancé sur le dépôt : lui donner un patch (`git diff --binary`, sans `data.json`) à appliquer, puis `python3 build.py`, commit et push sur `main`.

8. Une ligne dans `docs/JOURNAL.md`.
9. Commit et push :

```bash
git add -A
git commit -m "Mise à jour du JJ/MM : …"
git push origin main
```

Le message est en français. `JJ/MM` est le jour de Paris.

10. Vérifier le site en ligne (le déploiement Vercel prend souvent une minute) :

```bash
curl -fsS https://onrecord-fr.vercel.app/sw.js | head -n 8
curl -fsS https://onrecord-fr.vercel.app/data.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['meta']['generated'], d['meta']['counts'])"
```

Le `sw.js` servi doit contenir la version que tu viens de pousser, et `counts.statements` doit coller au dépôt.

Le relevé du matin peut déjà avoir tourné tout seul. Voir la section 10. Une phrase déjà en ligne, ou déjà dans `tools/auto_published.json`, ne se republie pas.

11. Compte rendu court, en français, tutoiement : pour chaque ajout, la personne, la date, une ligne, le lien. Lien du site. S'il n'y a rien de nouveau : le dire, et s'arrêter.

## 5. Prompt quotidien

À coller tel quel dans n'importe quel agent ou bot planifié. Il ne dépend d'aucun assistant nommé.

```
Chaque jour, mets à jour Onrecord.
Dépôt farahei-create/cartographie-gaza-extreme-droite, branche main.
Site : https://onrecord-fr.vercel.app/
Publication directe : commit sur main, push, pas de pull request.
Lis d'abord AGENTS.md et docs/REPRISE.md. Respecte toutes les règles éditoriales qui s'y trouvent.

1. Cherche les ~48 dernières heures (presse française et internationale, décisions et textes officiels, Arcom, juridictions, comptes vérifiés des intéressés) : nouveaux propos publics ou faits documentés, par les personnes et organisations déjà sur le site ou par d'autres personnalités publiques françaises, sur (a) des déclarations publiques au sujet de la campagne d'Israël à Gaza ; (b) des faits qui documentent la normalisation ou la montée de l'extrême droite en France. Repère aussi les vidéos officielles des moments cités.
2. Règles de publication (droit français de la diffamation), sans exception : citation exacte, datée, URL qui répond ; formulation neutre ; pas de lien de causalité que les sources n'écrivent pas ; jamais de particuliers ; contexte et démentis ; ne rien inventer ; photos seulement sous licence libre ou portrait officiel réutilisable ; vidéos seulement du diffuseur d'origine ou d'un compte officiel ; Wikipédia jamais comme source unique. Si rien ne qualifie, ne rien publier.
3. Travailler dans le dépôt. Lancer tools/archive.py sur les URL nouvelles et réessayer les archives manquantes. python3 build.py. Valider data.json. Tests Playwright (test_v8.py échoue déjà : ne pas le réparer en remettant une clé votes). Monter la version du cache dans sw.js. Compléter docs/JOURNAL.md. Commit « Mise à jour du JJ/MM : … », git pull, puis push. Vérifier en ligne avec curl que sw.js et data.json servent la nouvelle version.
4. Compte rendu en français, avec « tu » : liste courte (personne, date, résumé d'une ligne, lien source) et lien du site. S'il n'y a rien de nouveau, dis-le et n'ajoute rien.
5. Ne casse pas le relevé du matin ni les workflows de versions. Pas de force-push. Une grosse modification de app.js, style.css ou index.html enregistre la version d'avant. Le retour se fait avec « Revenir à une version ».
```

## 6. Versions

Le numéro vivant du cache est celui de `sw.js`. Les tags `version-…` sont les points de restauration (section 11), pas ces numéros. Il n'y a pas de tag git `v11`, `v17`, `v19`, `v20`, `v21` : ces numéros n'ont pas été publiés comme version du site. `tools/build.v11.py` et les scripts voisins sont d'anciens générateurs, pas la version en ligne.

| Version | Commit | Quoi |
|---|---|---|
| v4 | `711db2f` | Photos, logos, vidéos, section France |
| v5 | `101d3b8` | Accueil, fiches, chronologie, PWA |
| v7 | `889be48` | Carte de citation, page Méthode, Avant / maintenant |
| v8 | `c0c5c7e` | Section « Déclarations et votes », retirée le jour même (`9201279`) |
| v10 | `d91cb81` | Hanouna, Némésis, ISSEP, M6 |
| v12 | `cc95b3c` | Groupes dissous (GI, Zouaves, Civitas, Remparts, GUD), Pnat |
| v13 | `b38be66` | Leetchi, citation du jour, explorer, reprendre |
| v14 | `04c4e30` | Huit candidats 2027 et Macron |
| v15 | `7a2545b` | Cartes Partager avec portrait |
| v16 | `5fc1fac` | Page « Proposer une mise à jour » |
| v18 | `6b10389` | Bouton Soutenir, animation au tap |
| v22 | `53904cc` | Échelle du pouvoir |
| v23 | `f451506` | Parcours d'ascension, liens par nature |
| v24 | `33f9c07` | Parcours pour tous, vue Coulisses |
| v25 | `d45e741` | Mise à jour du 09/11 (Marine Le Pen, 60 Minutes) |
| v26 | `a5f4f04` | Citations des fiches pauvres, portraits libres, monogrammes, crédits, ce guide |
| v27 | Mise à jour du 10/11 | CNews (pétition classée), Knafo, Boëll à Grasset ; module `v27_content.py` |
| v28 | Mise à jour du 11/11 | Instituts de sondage (Ifop, OpinionWay, CSA, Harris/Toluna, Elabe), récit « Suivre les sondages » ; module `v28_content.py` |
| v29 | Mise à jour du 11/11 | Marine Le Pen, Éric Zemmour et Bruno Retailleau dans « Candidats à la présidentielle 2027 » |
| v30 | Mise à jour du 11/11 | Début de frise : études et premier métier, repère Formation |
| v31 | Mise à jour du 11/11 | Louise Montangon et l'UNI ; accueil centré. Module `v31_content.py` |
| v32 | Mise à jour du 11/11 | Haut de l'accueil : le rôle du site, trois accès, réseau en fond |
| v33 | Mise à jour du 11/11 | Accueil : le mot Onrecord reprend le titre, promesse en deux lignes |
| v34 | Mise à jour du 11/11 | Accueil : enseigne néon (Anton), réseau visible derrière le titre |
| v35 | Mise à jour du 11/11 (soir) | Pfeffer (prêt RN), Bardella (Face à BFM, X), Zemmour (TF1), France terre d'asile (saisine Arcom) ; module `v35_content.py` |
| v36 | Mise à jour du 12/11 | Accueil : couleurs d'origine (violet, blush, lavande), animation de l'enseigne conservée |
| v37 | Mise à jour du 12/11 | Accueil : réseau du hero flouté, voile dépoli derrière la punchline et la ligne d'explication |
| v38 | Mise à jour du 12/11 | Accueil : hero sombre violet, phrases surlignées, constellation 3D visible |
| v39 | Mise à jour du 12/11 | Ambiance néon sur tout le site, Réseau en 3D activable (canvas, sans librairie tierce) |
| v40 | Mise à jour du 12/11 | Accueil : espacement du hero, trait violet sous ONRECORD. Page admin privée (`admin.html`) |
| v41 | `bd2d4b7` | Mise à jour du 14/11 : Mélenchon, Barrot, primaire (Zemmour, Attal), Maréchal, Tondelier, Stérin. Module `v41_content.py` |
| v42 | Mise à jour du 16/11 | Rousseau, Portelli, réponse de Tondelier. Module `v42_content.py` |
| v43 | Mise à jour du 16/11 (complément) | Retailleau (4V), Le Pen (priorité nationale), Bardella (X), Sarkozy (primaire). Module `v43_content.py` |
| v44 | Mise à jour du 16/11 (relevé X) | 52 posts du 13 au 16/11, quinze fiches nouvelles. Module `v44_content.py` |
| v45 | Mise à jour du 16/11 (matin) | AJC, Anne-Sophie Sebban-Bécache, Olivier Rioult, Sarkozy (CNews et interdiction du RN). Module `v45_content.py` |
| v46 | Mise à jour du 17/11 | Débat LCI (Le Pen, Attal, Glucksmann, Mélenchon, Retailleau), Mélenchon et Arfi sur l'enquête de l'AJC, Rodwell sur Europe 1, Bruno Le Maire sur CNews. Module `v46_content.py` |
| v47 | Mise à jour du 18/11 | Relevé automatique du matin (GitHub Actions, Gemini gratuit). Aucune phrase nouvelle. |
| v48 | Mise à jour du 18/11 | La file d'attente est `auto_pending.json`, à la racine : le dossier `tools/` n'est pas servi par le site. |
| v49 | Mise à jour du 18/11 | Versions enregistrées et retour en arrière. Cartes de citation carrée et story, monogramme, lien `/c/…`. Tag de départ : `version-2026-11-18-avant-cartes`. |
| v50 | Mise à jour du 18/11 | Photo déjà hébergée, en fondu, sur les cartes carrée et story. Crédit si la licence l'exige. |
| v51 | Mise à jour du 18/11 | Barre à quatre onglets, réseau en cartes, enquête HATVP. Tag `version-2026-11-18-avant-enquete`. |
| v56 | Mise à jour du 22/11 (soir) | Contributions des lecteurs, validées dans l'admin. Tag `version-2026-11-22-avant-contributions`. Section 14 |
| v57 | Mise à jour du 23/11 | Onglet Liens épuré : filets fins, segments compacts, cartes du Réseau plus petites, détail en liste. Tag `version-2026-11-23-avant-liens`. Styles en fin de `style.css` (bloc « 23/11 »), limités aux vues Réseau, Coulisses et Échelle |
| v58 | Mise à jour du 23/11 (nuit) | Bouton mode clair / sombre dans la barre du haut. Tag `version-2026-11-23-avant-theme`. Voir « Mode clair / sombre » (section 2) |

Mises à jour de contenu entre les versions : voir `docs/JOURNAL.md`.

## 7. Points en suspens

- **Archive Le Parisien (Nantes).** L'URL `https://www.leparisien.fr/faits-divers/alcool-solitude-et-cnews-en-boucle-un-technicien-de-45-ans-condamne-apres-ses-menaces-de-mort-racistes-sur-facebook-03-11-2026-J4YLXBPWUVEEPFJLRLRLUVL22Q.php` est dans `tools/archives.json` avec `"status": "failed"` (`HTTP Error 520`). France 3 et Ouest-France, sur la même affaire, ont une copie. Réessayer `python3 tools/archive.py` avec cette URL seule. Ne pas retirer la source d'origine. Toujours en échec le 11/11/2026 au soir (520), comme les deux autres pages du Parisien.
- **`tests/test_v22.py`** compte les fiches par groupe (`EXPECT`) : l'aligner quand tu ajoutes une fiche (v35 : `asso` 19). `test_v22`, `test_v23` et `test_v24` écrivent une capture dans `/opt/cursor/artifacts` : hors de cet environnement, lance une copie qui écrit ailleurs.
- **`tests/test_v5.py`** : quatre échecs « graph built lazily on Réseau » existaient déjà avant v35.
- **`tests/test_v8.py` échoue** : il lit `data["votes"]`. La section a été retirée (`9201279`). Ne pas la remettre pour faire passer le test. Les autres tests doivent passer.
- **`CORRECTION_EMAIL`** dans `config.js` est une chaîne vide. Ne pas en inventer une.

## 8. Contrôle rapide avant de pousser

- La phrase nouvelle est dans la page, mot pour mot.
- Aucun mot interdit dans un texte rédigé par le site.
- `python3 build.py` affiche des compteurs cohérents.
- `sw.js` a changé de version.
- `docs/JOURNAL.md` a une entrée du jour.
- `curl` du `sw.js` en ligne montre cette version.

## 9. Page admin

Adresse : https://onrecord-fr.vercel.app/admin.html (la réécriture `/admin` mène au même fichier). Elle n'est liée nulle part dans `index.html`. `noindex, nofollow` est dans la page et dans `X-Robots-Tag` (`vercel.json`). `robots.txt` interdit `/admin.html` et `/admin`. Il n'y a pas de sitemap : n'y ajoute pas cette URL si tu en crées un.

La page sert à la propriétaire, depuis son iPhone, sans nouvel outil. Elle colle une fois un jeton GitHub **fine-grained**, limité au dépôt `farahei-create/cartographie-gaza-extreme-droite`, permission **Contents : Read and write**, rien d'autre. Le jeton reste dans le `localStorage` de l'appareil (`onrecord:admin-token`). « Se déconnecter » l'efface. Il n'est envoyé qu'à `https://api.github.com`. Le guide pas à pas est sur la page.

Créer le jeton :

1. github.com, compte **@farahei-create**.
2. Settings → Developer settings → Personal access tokens → Fine-grained tokens, ou https://github.com/settings/personal-access-tokens/new
3. Nom : Onrecord. Expiration au choix (90 jours est un bon défaut).
4. Resource owner : farahei-create. Repository access : seulement `cartographie-gaza-extreme-droite`.
5. Repository permissions → Contents → Read and write. Le reste reste sur No access.
6. Generate token, copier le `github_pat_…` (GitHub ne le réaffiche pas), le coller sur la page.

Formulaires : personnalité (nom, fonction, parti ou organisation, catégorie, section, photo facultative), déclaration (personne, citation exacte, date, média, URL, vidéo officielle, contexte, démenti), lien du réseau (deux entités, relation, source). La photo est réduite à 400 px et passée en WebP dans le navigateur. Sans photo : monogramme. Avec photo : auteur, licence libre ou portrait officiel, page Commons ou page officielle.

« Voir l'aperçu », puis « Publier ». Le commit `admin: ajout …` écrit `tools/admin_additions.json` (et, s'il y a une photo, `tools/people_images.json` plus `img/people/<id>.webp`) via l'API Git. En cas de conflit de sha, la page relit la branche et réessaie. Un jeton refusé s'affiche clairement.

`build.py` applique ce fichier à la fin, par `admin_content.py`, après les modules `v35_content.py` et suivants. Même format que le reste : citation, date, média, URL, thème, section ; lien avec `nature` déjà posée pour que `_nature()` ne la reclasse pas. Une personne nouvelle reçoit une étape de parcours tirée de sa première déclaration, sinon `tests/test_v24.py` échoue.

Vercel ne lance pas `build.py` (le site est statique, `data.json` est dans le dépôt). Le workflow `.github/workflows/build-data.yml` part sur un push des sources, lance `python3 build.py`, et `tools/commit_data_if_content.py` ne commit `data.json` que si le contenu change. Si seule la date de génération change, pas de commit. Ce second push redéploie Vercel. `data.json` est en réseau d'abord dans `sw.js` : le téléphone récupère le fichier nouveau sans geste de plus. Compte environ une minute.

Les règles éditoriales de la section 3 s'appliquent aussi à ce qui entre par cette page. Une URL Wikipédia, un mot interdit dans un texte rédigé par le site, ou une licence NC/ND, font échouer `build.py` : le `data.json` en ligne ne bouge pas.

Le relevé du matin écrit `tools/auto_published.json`. `auto_content.py` l'applique juste avant `admin_content.py`. La page admin affiche aussi la file d'attente (`auto_pending.json`, à la racine du site), qui n'est pas une publication.

## 10. Automatisation

Le workflow `.github/workflows/daily-update.yml` (« Relevé du matin ») fait la mise à jour du jour sans personne aux commandes. Il ne part que sur l'horloge, ou quand tu le lances à la main. Un push ordinaire ne le déclenche pas.

### Heure

Le cron est `17 5 * * *`, donc **05:17 UTC**.

- En hiver (CET, UTC+1) : 6 h 17 à Paris.
- En été (CEST, UTC+2) : 7 h 17 à Paris.

GitHub ne connaît pas l'heure de Paris, et un cron peut partir en retard. Avec `30 6 * * *`, les runs du 18 au 22/11/2026 sont partis vers 15 h UTC, plus de huit heures après l'heure prévue : les minutes rondes sont les plus chargées chez GitHub. D'où une minute creuse, tôt. La fenêtre des phrases est d'environ 48 heures, plus 6 heures de marge pour une dépêche du matin.

### Activer

1. Ouvre [Google AI Studio](https://aistudio.google.com/apikey) avec un compte Google. Crée une clé API. Ne lie pas de compte de facturation au projet : le relevé est prévu pour le quota gratuit. Le modèle appelé est `gemini-3.5-flash-lite` (gratuit au 18 novembre 2026). S'il disparaît, le programme essaie `gemini-2.5-flash-lite`, puis `gemini-3.1-flash-lite`.
2. Sur GitHub, dépôt `farahei-create/cartographie-gaza-extreme-droite` : **Settings → Secrets and variables → Actions → New repository secret**. Nom exact : `GEMINI_API_KEY`. Valeur : la clé. Rien d'autre.
3. Le lendemain matin, le workflow part tout seul. Pour le lancer tout de suite : onglet **Actions → Relevé du matin → Run workflow**. Coche « À blanc » pour un essai qui n'écrit rien et ne pousse pas. L'essai à blanc lit quand même les flux et appelle Gemini : il consomme un peu du quota.

Sans ce secret, le workflow écrit un résumé, s'arrête avec un succès, et ne modifie pas `main`. Une clé refusée (401 ou 403) arrête aussi le run, sans push.

### Ce qu'il fait

1. Il lit des flux RSS qui répondaient le 18 novembre 2026 (franceinfo, BFMTV, CNews, Europe 1, France Inter, Sud Radio, Le Monde, Le Figaro, Libération, le JDD, le HuffPost, LCP, l'Arcom, le Conseil d'État, Public Sénat) et quatre recherches Google News des dernières 48 heures. Google News ne sert qu'à trouver l'article : la phrase est relue sur la page de l'éditeur. RTL, LCI, TF1 Info et l'Assemblée nationale n'avaient pas de flux stable ce jour-là ; ils entrent quand Google News résout leur page.
2. Il ne télécharge que les pages dont le titre ou le chapeau touche aux deux sujets, ou nomme une fiche déjà en ligne (score d'au moins 3). Les pages index (fiche personnalité BFMTV `_DN-…`, émission, tag) sont écartées. Une page bloquée (403, 402, délai) ou un mur anti-robot (« Client Challenge », « Accès restreint ») ne prend pas de place : on passe à la suivante. Le Monde, Libération, Mediapart, L'Express et Le Point, qui bloquent les robots, sont essayés en dernier. Le modèle reçoit les paragraphes de l'article (balises `p`, `blockquote`, `h1`), pas les menus : avant le 22/11, l'extrait commençait par 3 500 caractères de menu, et le modèle ne trouvait aucune citation. Les 24 lectures sont réparties : au plus deux pages par personne et trois par média, en prenant d'abord celles qui ne sont pas encore couvertes. Plafond ensuite : deux phrases publiées par personne et quatre par média. Le surplus va dans la file, il n'est pas jeté. Douze liens Google News au plus, 60 requêtes au modèle au plus (retries compris). Cinq secondes entre chaque requête. Un 429, un 5xx ou un délai dépassé est réessayé trois fois avec attente croissante ; ensuite la page passe au modèle de secours. Un 429 retire le modèle pour la suite du run. Le run ne s'arrête que si les trois modèles sont en 429 ; le reste va dans la file. Un flux en échec est nommé dans le résumé, avec l'erreur.
3. Le modèle propose des phrases. Il ne décide pas. Le programme publie seulement si, après normalisation des espaces et des apostrophes : la phrase est dans la page, entre guillemets, et elle n'est pas coupée au milieu d'un mot ou d'une phrase. Une ellipse `[…]` ne passe que si chaque morceau est dans la page, dans l'ordre, sur des mots entiers. Le programme n'ajoute pas de points de suspension et ne raccourcit pas une phrase pour l'afficher. La date est dans la fenêtre et dans la page (ou, à défaut, celle du flux). L'URL est en https et n'est ni Wikipédia, ni X, ni Google News. Aucun mot interdit dans les champs écrits, y compris dans la citation. La personne est déjà dans l'archive, ou la page la présente avec une fonction publique recopiée (député, ministre, candidat, journaliste…). Le sujet est dans la phrase ou juste à côté. Ce n'est pas un doublon : une phrase déjà en ligne, même plus courte (« ramassis de gauchistes »), bloque une reprise qui la contient. Un doute du modèle, un particulier, une causalité absente de la page : file d'attente, pas le site. Pas de photo (monogramme). Pas de lien de réseau créé tout seul. Une vidéo seulement si son URL est déjà dans la page et vient du diffuseur.
4. Ce qui passe est ajouté à `tools/auto_published.json`. `build.py` reconstruit `data.json`. Les URL nouvelles passent par `tools/archive.py`. `sw.js` monte d'un numéro, ainsi que les tests qui citent cette version. `tests/test_v22.py` recalcule `EXPECT` avec la même règle que l'échelle du pouvoir. Le journal reçoit une entrée.
5. Les tests Playwright tournent. Un test ne doit jamais écrire un numéro de cache en dur sans être dans la liste de `tools/daily/store.py` : du 18 au 21/11, `tests/test_enquete.py` attendait `onrecord-v52` exactement, et chaque run qui publiait (donc montait le cache) échouait sans push. Il vérifie maintenant « v52 ou plus ». `tests/test_v8.py` est ignoré. Dans `tests/test_v5.py`, seuls les échecs « graph built lazily on Réseau » sont admis. Tout autre échec annule le push. Le site en ligne doit répondre avant le push. Après le push, le workflow attend que `sw.js` serve la nouvelle version.
6. Le commit, en français, est `Mise à jour du JJ/MM : relevé automatique, N phrases`, ou `Mise à jour du JJ/MM : file d'attente, rien publié`. Il est poussé sur `main`.

Le résumé du run est dans l'onglet Actions, en tête de la page (GITHUB_STEP_SUMMARY) : publié, écarté, flux en échec, nombre de requêtes.

### File d'attente

`auto_pending.json` (à la racine, le site ne sert pas le dossier `tools/`), et le bloc « File d'attente du matin » sur https://onrecord-fr.vercel.app/admin.html . Ce n'est pas une publication : `noindex`, et `robots.txt` l'interdit. Une phrase qui contient un mot interdit, et un particulier, n'y sont pas recopiés : la raison et l'URL restent, pour que tu ouvres la source. Le fichier est dans le dépôt, qui est public : n'y mets pas à la main une phrase que tu ne montrerais pas.

Tu peux reprendre un élément à la main, depuis la page admin, si tu le juges publiable. Le programme ne le republiera pas tant que la phrase exacte est déjà en ligne.

### Arrêter, relancer

- Arrêter : Actions → Relevé du matin → les trois points → **Disable workflow**. Ou supprime le secret `GEMINI_API_KEY` : le run du matin s'arrête proprement.
- Relancer : **Enable workflow**, ou Run workflow. Décoche « À blanc » pour publier.
- Essai local, sans clé et sans écrire : `python3 -m tools.daily.run --mock --dry-run`. Les garde-fous seuls : `python3 tests/test_daily.py`.

### Limites

Ce n'est pas une revue humaine.

- La télé et la radio n'entrent que si un article en reprend la phrase mot pour mot. Un direct sans article est absent.
- L'API X n'est pas utilisée. Un post n'est publié que si une page de presse qui répond le cite tel quel, et l'URL publiée est celle de cette page.
- Le quota gratuit est court : au plus 24 pages relues par matin. Le reste attend, ou n'est pas ouvert. Un 429 sur les trois modèles arrête la relecture.
- Si un compte de facturation est lié au projet Google, le plafond de 60 requêtes limite la dépense, mais le seul moyen d'être certain de ne rien payer est de ne pas lier de facturation. Les extraits de pages sont envoyés à Google, qui peut s'en servir pour améliorer ses modèles sur l'offre gratuite.
- Certains sites bloquent les serveurs de GitHub. La page est alors « inaccessible » et rien n'est publié.
- Le programme rate l'ironie, un second degré, un démenti publié sur une autre page que celle qu'il a lue, et une personne publique dont la fonction n'est pas écrite à côté de la phrase. Ces cas vont dans la file, ou passent à côté.
- Il ne crée pas de fiche sans fonction publique lue dans la page, pas d'organisation nouvelle, pas de photo, pas de lien du réseau.
- Une phrase qui contient « complice », « génocidaire », « pantin », « infiltré », « marionnette », « protégé », « copinage » ou « occulte » n'est pas publiée, même si la personne l'a dite. Tu peux la reprendre à la main si la section 3 le permet.
- Google News sert d'index. Son flux est réservé par Google à un lecteur personnel et non commercial : on n'en recopie pas le texte, seulement l'adresse de l'éditeur quand elle se résout.
- `CORRECTION_EMAIL` reste vide. Le programme n'y touche pas.

Un retour à une version remet aussi `tools/auto_published.json`. Les phrases parues après cette version quittent le site, et le prochain `build.py` ne les réinjecte pas. Si l'une d'elles est encore dans les 48 heures, le relevé du lendemain peut la retrouver : les mêmes contrôles s'appliquent. `auto_pending.json` n'est pas remis en arrière : la file d'attente reste celle d'aujourd'hui. Le code du relevé, ses workflows et `tests/test_daily.py` non plus.

## 11. Versions et retour en arrière

Le numéro `onrecord-vN` de `sw.js` est le cache du téléphone. Une **version** est autre chose : un tag git annoté `version-AAAA-MM-JJ-…`, que l'on peut remettre en ligne.

Le premier tag, posé avant ces changements, est `version-2026-11-18-avant-cartes` (commit `cbc87d2`, cache `onrecord-v48`).

Tout se fait depuis GitHub, sans serveur payant et sans jeton dans la page. Le dépôt est public : `/admin.html` lit les tags par l'API publique, et `versions.json` sert de secours. GitHub ne préremplit pas les champs d'un workflow. Le bouton copie le nom, ouvre la page, et le mode d'emploi dit quoi coller.

### Enregistrer

Workflow **Enregistrer une version** (`.github/workflows/enregistrer-version.yml`).

- À la main : Actions → Enregistrer une version → Run workflow. Note facultative, mot court facultatif (`avant-cartes`). Le tag est `version-AAAA-MM-JJ-mot`, ou avec l'heure s'il n'y a pas de mot.
- Chaque dimanche, 18 h UTC (19 h à Paris en hiver, 20 h en été), si ce commit n'a pas déjà une version.
- À chaque push sur `main` qui touche `app.js`, `style.css` ou `index.html` : tag du commit d'avant, `version-…-avant-modif`. Pas de second tag si ce commit en a déjà un.

Le tag est annoté. Rien n'est écrasé s'il existe déjà.

### Revenir

Workflow **Revenir à une version**. Il faut le nom exact, et le mot `REVENIR`.

1. Il enregistre l'état courant (`version-…-avant-retour`).
2. Il crée un **nouveau** commit sur `main` qui remet le site public à ce tag : pages, style, script, `data.json`, modules de contenu, images, `tools/auto_published.json`.
3. Il ne fait pas de force-push. L'historique reste. Le retour se défait en revenant au tag `avant-retour`.
4. Il monte le cache `sw.js` d'un cran, pour que les téléphones prennent la copie remise.

Il ne remet pas en arrière :

- la file `auto_pending.json` ;
- le code et les workflows du relevé du matin, ni `tests/test_daily.py` ;
- la page admin, `AGENTS.md`, `docs/REPRISE.md` (le journal reçoit une ligne, il n'est pas effacé).

Ainsi un retour ne casse pas le geste qui permet d'en faire un autre, ni le relevé du lendemain. Les phrases automatiques d'après la version choisie ne sont pas réinjectées par `build.py`, parce que `tools/auto_published.json` revient avec elles. Voir la fin de la section 10.

Le site en ligne ne montre qu'une version à la fois (celle de `main`). Le lien « Voir les fichiers » ouvre l'arbre GitHub du tag. Ce n'est pas le site tel que les visiteurs le voient : pour le revoir en ligne, il faut revenir à cette version.

### Essai

`tests/test_versions.py` joue un retour dans un dépôt temporaire. Il ne pousse pas, et il ne touche pas à `main`.

## 12. Cartes à partager

Chaque citation a « Partager ». Le navigateur dessine deux images, sans service extérieur :

- carré, 1080×1080, pour un post ;
- verticale, 1080×1920, pour une story.

Sur l'image : la citation entière, le nom, la fonction, la date, le média, `onrecord-fr.vercel.app`, et le monogramme. Si la fiche a déjà une photo dans `img/`, elle est en fondu derrière le texte (fichier du site, pas une adresse distante, pour que le canvas reste lisible par le navigateur). CC BY et « © European Union » sont écrits en petit. CC0 et le domaine public ne le sont pas. Pas de commentaire ajouté. S'il y a un contexte ou un démenti (thème « Nuance / contexte », ou les mots « Contexte », « démenti », « Précision ou réponse » dans le média), une ligne dit « Contexte sur Onrecord ».

La taille du texte baisse pour que la phrase tienne. Si elle ne tient pas en entier, même en story, le bouton d'image est éteint et le texte le dit. On ne coupe pas la citation avec des points de suspension inventés.

« Copier le lien » copie `https://onrecord-fr.vercel.app/c/<id>/<n>.html`. Cette page, écrite par `build.py`, montre la citation entière et les balises Open Graph (titre, description, icône du site). Les applications qui ne lisent pas le JavaScript s'en servent. L'image dessinée dans le navigateur n'est pas l'aperçu du lien : elle part par le partage du téléphone, ou par le téléchargement. Sur ordinateur, le bouton télécharge le PNG. Sur téléphone, si le partage de fichier existe, il s'ouvre.

`build.py` régénère `c/` seulement quand il écrit le vrai `data.json`. Le relevé du matin commit ces pages avec le reste, s'il y en a de nouvelles.

## 13. Premier jour pour reprendre

1. Compte GitHub avec le droit d'écrire sur `farahei-create/cartographie-gaza-extreme-droite`, branche `main`. La publication est un commit poussé sur `main`. Pas de pull request. Vercel (équipe valladeaus-projects) redéploie.
2. Lis `AGENTS.md`, puis ce fichier en entier, puis le haut de `docs/JOURNAL.md`.
3. Ouvre https://onrecord-fr.vercel.app/ et `curl -fsS https://onrecord-fr.vercel.app/sw.js | head -n 8`. Le numéro doit être celui de `sw.js` dans `main`.
4. Règles, sans exception : citation exacte, datée, URL qui répond ; ton neutre ; mots à ne pas employer pour qualifier quelqu'un : complice, génocidaire, pantin, infiltré, marionnette, protégé, copinage, occulte ; pas de lien causal que la source n'écrit pas ; pas de personnes privées ; contexte et démenti sur la même fiche ; Wikipédia jamais seule source ; pas de photo hors licence libre ou portrait officiel réutilisable.
5. `config.js` : `CORRECTION_EMAIL` reste `""`. N'invente pas d'adresse.
6. Relevé du matin : secret `GEMINI_API_KEY` (clé gratuite, sans facturation). Sans cette clé, le workflow de 6 h 30 UTC s'arrête et ne touche pas à `main`. Garde-fous, file d'attente, plafonds : section 10. Essai : `python3 tests/test_daily.py` et `python3 -m tools.daily.run --mock --dry-run`.
7. Versions : la liste est sur https://onrecord-fr.vercel.app/admin.html . Enregistrer ou revenir se fait sur GitHub (Actions), pas dans la page. Le tag de secours d'avant les cartes est `version-2026-11-18-avant-cartes`.
8. Pour publier : `git pull`, sources (pas `data.json` à la main), `python3 tools/archive.py` sur les URL nouvelles, `python3 build.py`, monter `sw.js`, tests (sauf `tests/test_v8.py`, et les quatre échecs « graph built lazily on Réseau » de `tests/test_v5.py`), `docs/JOURNAL.md`, commit `Mise à jour du JJ/MM : …`, push, vérifier `sw.js` en ligne.
9. Si un changement casse le site : admin → Revenir à cette version → coller le nom → écrire REVENIR → Run workflow. Attendre une minute. Pour annuler ce retour, revenir au tag `avant-retour` créé juste avant.

## 14. Contributions des lecteurs

Section gratuite, sans Supabase. Un lecteur s'inscrit avec son e-mail, reçoit un code, choisit un pseudonyme, puis dépose une note sur une fiche existante : titre, texte, date des faits (facultative), liens `https://`, jusqu'à quatre photos (5 Mo) ou vidéos (50 Mo). **Rien ne paraît sans validation** dans `/admin.html`. Chaque contribution affichée porte : « Contenu publié par un contributeur, sous sa seule responsabilité. Onrecord ne l'a pas vérifié comme ses propres sources. Signaler un contenu ». Le pseudonyme et l'heure du dépôt (heure de Paris) sont affichés, jamais l'e-mail.

### Comment c'est fait

- Une seule fonction Vercel : `api/contrib/[action].js` (actions `status`, `me`, `send-code`, `verify`, `logout`, `upload`, `submit`, `report`, `admin`). La logique est dans `lib/contrib/core.js`, testée sans réseau.
- Code e-mail : six chiffres, valable 15 minutes, cinq essais, usage unique. Une minute entre deux codes, cinq par heure et par adresse, vingt par heure et par réseau. Le défi est signé (HMAC, `SESSION_SECRET`). Rien n'est stocké en clair.
- Adresses jetables : `lib/contrib/disposable_domains.json` (liste CC0 disposable-email-domains, copie du 22/11/2026, plus quelques domaines français), sous-domaines compris. Un domaine qui n'existe pas (DNS) est refusé.
- Session : cookie `onrecord_s` signé, `HttpOnly`, `Secure`, `SameSite=Lax`, 30 jours.
- Fichiers : envoyés directement du navigateur vers **Vercel Blob** (`vendor/blob-upload.js`, chargé seulement au moment de l'envoi). Types acceptés : JPEG, PNG, WebP, GIF ; MP4, WebM, MOV. Vingt fichiers par jour et par compte.
- File d'attente et signalements : JSON dans Blob (`contrib/pending/`, `contrib/reports/`), noms à suffixe aléatoire, e-mail chiffré (AES-GCM, clé tirée de `SESSION_SECRET`). Cinq dépôts par jour et par compte.
- Mots interdits (section 3) et indices de données privées (téléphone, e-mail, adresse postale) : signalés en rouge dans l'admin, pas refusés automatiquement. C'est toi qui décides.
- Modération : la section « Contributions des lecteurs » de `/admin.html` utilise le **jeton GitHub déjà enregistré** sur la page. La fonction vérifie côté serveur que ce jeton ouvre le dépôt en écriture. Pas de mot de passe de plus.
  - **Publier** écrit `contributions.json` sur `main` par l'API GitHub (commit `contributions: publication …`). Vercel redéploie en une minute environ. Une trace privée (`contrib/archive/`) garde l'e-mail chiffré de l'auteur : la LCEN impose de pouvoir l'identifier sur réquisition.
  - **Refuser et effacer** supprime la contribution et ses fichiers.
  - **Retirer** enlève une contribution publiée de `contributions.json` et efface ses fichiers.
  - **Classer** ferme un signalement.
- Un retour à une version (section 11) ne touche pas à `contributions.json`, `api/`, `lib/contrib/`, `admin-contrib.js` : un contenu retiré ne revient pas, un contenu validé ne disparaît pas.
- Sans les variables ci-dessous, tout répond « Bientôt disponible » (code 503), sans erreur.

### Ouvrir la section (dans Vercel, une fois)

1. Vercel → projet Onrecord (équipe valladeaus-projects) → **Storage** → **Create Database** → **Blob** → accès **Public** → **Connect** au projet. Vercel ajoute seul `BLOB_READ_WRITE_TOKEN`.
2. **Settings → Environment Variables**, pour Production (et Preview si tu veux tester) :
   - `SESSION_SECRET` : une longue phrase au hasard, 32 caractères ou plus. Ne la change pas ensuite (sinon les sessions et les e-mails chiffrés deviennent illisibles).
   - `RESEND_API_KEY` : clé Resend (`re_…`).
   - `MAIL_FROM` : facultatif avec Resend (par défaut `Onrecord <onboarding@resend.dev>`).
3. **Deployments → Redeploy** pour que les variables soient lues.
4. Vérifier : `https://onrecord-fr.vercel.app/api/contrib/status` doit afficher `"enabled":true`.

### Envoyeur d'e-mails gratuit

- **Resend** (gratuit : 3 000 e-mails par mois, 100 par jour). resend.com → Sign up → API Keys → Create API Key (permission Sending access) → copier `re_…` dans Vercel. Limite : avec l'adresse de test `onboarding@resend.dev`, Resend n'envoie **qu'à l'adresse du compte Resend**. Pour écrire aux lecteurs, il faut un nom de domaine à toi vérifié dans Resend (Domains → Add Domain, puis les enregistrements DNS), et `MAIL_FROM` = `Onrecord <code@ton-domaine.fr>`. Un domaine `vercel.app` ne peut pas être vérifié.
- **Sans nom de domaine : Brevo** (gratuit : 300 e-mails par jour). brevo.com → compte gratuit → Senders → ajouter et confirmer ton adresse e-mail d'envoi → SMTP & API → API Keys → créer une clé. Dans Vercel : `BREVO_API_KEY` = la clé, `MAIL_FROM` = `Onrecord <ton-adresse@…>` (l'adresse confirmée), et **pas** de `RESEND_API_KEY` (Resend est pris en premier s'il est présent). Les codes peuvent arriver dans les indésirables.

### Limites

- Vercel Blob gratuit (Hobby) : environ 1 Go stocké et un quota mensuel d'opérations. Les marqueurs de débit (`rl/`) sont nettoyés au fil de l'eau. Une vidéo de 50 Mo prend vite de la place : refuse ce qui n'est pas utile.
- Fonctions Vercel Hobby : une seule fonction ici, loin de la limite de 12.
- Une publication attend le redéploiement (une minute environ).
- Pas de modification par l'auteur après dépôt : il redépose, tu refuses l'ancienne.
- Demandes de retrait : bouton « Signaler un contenu » (motif, e-mail facultatif). Retire promptement tout contenu manifestement illicite.

### Essai

`node --test tests/test_contributions.mjs` (code, jetables, débit, dépôt, modération, fonction sans variables). `python3 tests/test_contributions_ui.py` avec le serveur local sur `:8765` (bloc des fiches, bandeau, heure de Paris, « bientôt disponible », captures dans `shots/`).

