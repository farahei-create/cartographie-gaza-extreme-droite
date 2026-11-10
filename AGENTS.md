# Onrecord — consignes pour tout agent

Lis `docs/REPRISE.md` avant de modifier le dépôt. Ce fichier-ci rappelle seulement ce qu'il ne faut pas rater.

Onrecord est une archive citoyenne statique (PWA, sans CDN) : déclarations publiques sur Gaza et sur la normalisation de l'extrême droite en France. Site : https://onrecord-fr.vercel.app/ . Dépôt `farahei-create/cartographie-gaza-extreme-droite`, branche `main`. Un push sur `main` redéploie Vercel (équipe valladeaus-projects). Publication directe : commit sur `main`, pas de pull request.

## Règles qui ne se négocient pas

Droit français de la diffamation. Si une source ne les respecte pas, on ne publie pas.

- Citation **exacte**, datée, URL qui répond. Les crochets `[ ]` signalent une coupure. Pas de paraphrase présentée comme une citation.
- Formulation **neutre**. Jamais : « complice », « génocidaire », « pantin », « infiltré », ni « marionnette », « protégé », « copinage », « occulte ».
- Pas de lien de causalité que la source n'écrit pas.
- Pas de particuliers. Personnes publiques et organisations seulement.
- Contexte, nuances et démentis dans la même fiche.
- Photos : Commons (CC BY, CC BY-SA, CC0, domaine public) ou portrait officiel dont la réutilisation est explicite (Parlement européen, mention « © European Union »). Jamais de photo de presse, Google Images, capture X/Instagram, image générée. Crédit auteur + licence + lien, sur la fiche et en petit sur la carte de partage.
- Logos d'organisations : Commons seulement, si la licence ou le statut l'autorise (y compris PD-textlogo). Sinon monogramme.
- Vidéos : compte du diffuseur d'origine ou compte officiel uniquement.
- Wikipédia n'est jamais la source unique d'une citation.
- `config.js` : `CORRECTION_EMAIL` reste vide tant qu'aucune adresse n'est choisie. Ne pas en inventer.

## À chaque changement publié

1. `git pull origin main`
2. Modifier les sources (`build.py`, `v26_content.py` ou un fichier du même genre), pas `data.json` à la main.
3. `python3 tools/archive.py` sur les URL nouvelles.
4. `python3 build.py`
5. Monter `onrecord-vN` dans `sw.js` (une version de plus).
6. Tests Playwright. `tests/test_v8.py` échoue déjà (clé `votes` retirée) : ne pas le « réparer » en réintroduisant la section.
7. Commit `Mise à jour du JJ/MM : …`, push `origin main`.
8. Vérifier que le `sw.js` en ligne porte la nouvelle version.
9. Ajouter une ligne à `docs/JOURNAL.md`. Compte rendu court, en français, avec « tu ».

Le détail, les commandes et le prompt quotidien sont dans `docs/REPRISE.md`.
