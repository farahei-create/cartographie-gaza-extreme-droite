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
| `v24_content.py`, `v26_content.py`, `v27_content.py`, `v28_content.py` | Ajouts branchés à la fin de `build.py` |
| `config.js` | `DONATION_URL`, `CORRECTION_EMAIL` |
| `sw.js` | Service worker. La constante `VERSION` doit monter à chaque publication |
| `manifest.webmanifest`, `icons/` | PWA |
| `img/people/`, `img/orgs/` | Portraits et logos hébergés (webp, environ 400 px) |
| `tools/people_images.json`, `tools/org_logos.json` | Crédits (auteur, licence, lien). `build.py` les recopie sur les fiches |
| `tools/archive.py`, `tools/archives.json` | Copies Wayback |
| `tools/build.v*.py` | Anciens scripts, conservés pour l'historique. Ne pas les lancer |
| `tests/test_v*.py` | Playwright |
| `docs/JOURNAL.md` | Journal daté des mises à jour |

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

`#/` accueil · `#/sections` · `#/chronologie` · `#/reseau` · `#/pouvoir` échelle · `#/coulisses` · `#/methodologie` · `#/methode` · `#/contribuer` · `#/credits` · `#/personne/<id>` · `#/organisation/<id>`

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
7. **Photos.** Commons d'abord, licence libre seulement : CC BY, CC BY-SA, CC0, domaine public. Vérifier sur la page du fichier via l'API (`imageinfo` + `extmetadata`) : `LicenseShortName`, auteur, `NonFree` absent. Refuser CC BY-NC, CC BY-ND, fair use. Ensuite, portrait officiel dont le texte autorise la réutilisation : Parlement européen, avec « © European Union » et lien vers https://www.europarl.europa.eu/legal-notice/ . Assemblée nationale et Sénat : seulement si leurs conditions, lues ce jour-là, autorisent la réutilisation ; citer cette condition dans `image_credit`. Jamais : photo de presse, Google Images, capture X ou Instagram, image générée. Héberger un webp d'environ 400 px dans `img/people/`, crédit dans `tools/people_images.json` (auteur, licence, `license_url`, `source_url`). Le crédit s'affiche sur la fiche et, en petit, sur la carte de partage.
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
```

## 6. Versions

Le numéro vivant est celui de `sw.js`. Il n'y a pas de tag git `v11`, `v17`, `v19`, `v20`, `v21` : ces numéros n'ont pas été publiés comme version du site. `tools/build.v11.py` et les scripts voisins sont d'anciens générateurs, pas la version en ligne.

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

Mises à jour de contenu entre les versions : voir `docs/JOURNAL.md`.

## 7. Points en suspens

- **Archive Le Parisien (Nantes).** L'URL `https://www.leparisien.fr/faits-divers/alcool-solitude-et-cnews-en-boucle-un-technicien-de-45-ans-condamne-apres-ses-menaces-de-mort-racistes-sur-facebook-03-11-2026-J4YLXBPWUVEEPFJLRLRLUVL22Q.php` est dans `tools/archives.json` avec `"status": "failed"` (`HTTP Error 520`). France 3 et Ouest-France, sur la même affaire, ont une copie. Réessayer `python3 tools/archive.py` avec cette URL seule. Ne pas retirer la source d'origine.
- **`tests/test_v8.py` échoue** : il lit `data["votes"]`. La section a été retirée (`9201279`). Ne pas la remettre pour faire passer le test. Les autres tests doivent passer.
- **`CORRECTION_EMAIL`** dans `config.js` est une chaîne vide. Ne pas en inventer une.

## 8. Contrôle rapide avant de pousser

- La phrase nouvelle est dans la page, mot pour mot.
- Aucun mot interdit dans un texte rédigé par le site.
- `python3 build.py` affiche des compteurs cohérents.
- `sw.js` a changé de version.
- `docs/JOURNAL.md` a une entrée du jour.
- `curl` du `sw.js` en ligne montre cette version.
