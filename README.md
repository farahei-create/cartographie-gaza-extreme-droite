# Onrecord — Leurs mots, datés et sourcés

*Gaza et extrême droite en France : cartographie des déclarations et des liens publics.*

Site statique (HTML/CSS/JavaScript, **sans étape de build**) qui présente :

- une page d'**Accueil** (présentation, chiffres clés calculés depuis les données, recherche, dernières déclarations) ;
- une vue **Sections** (Gaza / France / communs) organisée par **catégories** et **sous-catégories** ;
- une **fiche** par personne ou organisation (`#/personne/<id>`, `#/organisation/<id>`) : photo et crédit, fonction, frise datée des déclarations (citation, média, thème, source, copie archivée, vidéo), relations, bouton Partager ;
- une **Chronologie** de toutes les déclarations et de tous les liens datés, filtrable par section, catégorie, thème et année ;
- le **Réseau** interactif des relations (avec plein écran) ;
- une section **Méthodologie** (critères d'inclusion, neutralité, archivage, citation, absence de qualification juridique, droit de réponse) ;
- un format **application installable** (manifeste + service worker : écran d'accueil iPhone via Safari › Partager › « Sur l'écran d'accueil »).

Les citations sont reproduites telles que publiées. Le site ne porte aucune qualification juridique sur les personnes citées.

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `index.html` | Page unique (vues : Accueil, Sections, fiche, Chronologie, Réseau, Méthodologie) |
| `style.css` | Mise en forme (sobre, responsive) |
| `app.js` | Chargement de `data.json`, routage `#/…`, accueil, sections, fiches, chronologie, graphe |
| `manifest.webmanifest`, `icons/` | Application installable (nom, couleurs, icônes 180/192/512 et « maskable ») |
| `sw.js` | Service worker : coque + données + images en cache (réseau d'abord pour `data.json`) |
| `data.json` | Jeu de données (seule source de contenu) |
| `vendor/vis-network.min.js` | Bibliothèque [vis-network](https://github.com/visjs/vis-network) 9.1.9 embarquée localement (licence Apache-2.0 / MIT), aucune dépendance à un CDN |

## Tester en local

`data.json` est chargé avec `fetch`, il faut donc passer par un petit serveur web (l'ouverture directe du fichier `index.html` ne fonctionne pas) :

```bash
cd site
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

## Mettre à jour les données (`data.json`)

Structure :

```json
{
  "meta": { "generated": "AAAA-MM-JJ", "methodology": "…", "counts": { "persons": 0, "orgs": 0, "edges": 0, "statements": 0 } },
  "nodes": [
    {
      "id": "identifiant-unique",
      "name": "Nom affiché",
      "type": "person | org",
      "role": "Fonction publique (pour une organisation : « Parti politique », « Hebdomadaire », « Association », « Événement »…)",
      "description": "Description neutre et factuelle",
      "category": "Responsables politiques", "subcategory": "Parlementaires & élus",
      "statements": [
        { "quote": "Citation exacte, telle que publiée", "date": "AAAA-MM-JJ", "medium": "Média / support", "url": "https://…", "theme": "Gaza – déclarations", "section": "gaza | france", "archive_url": "https://web.archive.org/web/…", "archived": "AAAA-MM-JJ" }
      ]
    }
  ],
  "edges": [
    { "source": "id-source", "target": "id-cible", "relation": "nature du lien", "url": "https://…", "date": "AAAA-MM-JJ" }
  ]
}
```

Règles à respecter :

1. **Toute déclaration et toute relation doit avoir une URL source** consultable et une date (laisser `""` si la source ne permet pas de dater ; le site affiche alors « date non précisée »).
2. Reproduire les citations **mot pour mot**. Utiliser `[ ]` pour une reformulation de contexte ou une coupure.
3. Thèmes utilisés par les filtres : `Gaza – déclarations`, `Proximité extrême droite`, `Nuance / contexte` (un nouveau thème ajouté dans les données apparaît automatiquement dans les filtres).
4. Ajouter les **nuances, rectifications et démentis** publiés par les personnes concernées.
5. Rédiger `role` et `description` de façon neutre, sans qualificatif accusatoire.
6. Le sous-type d'une organisation (parti, média, association, événement) est déduit automatiquement du champ `role` (mots-clés : « parti », « mouvement politique », « groupe parlementaire » → parti ; « radio », « chaîne », « hebdomadaire », « magazine », « média » → média ; « association », « organisation » → association ; « événement » → événement).
7. Mettre à jour `meta.generated` (date de dernière mise à jour affichée sur le site) et `meta.counts`.
8. Vérifier les liens avant publication et valider le JSON, par exemple : `python3 -m json.tool data.json > /dev/null`.

## Publication sur GitHub Pages

Placer le contenu du dossier à la racine du dépôt (ou dans `docs/`), puis activer GitHub Pages dans *Settings → Pages* sur la branche choisie. Aucun build n'est nécessaire.

## Signaler une erreur / droit de réponse

Pour signaler une erreur ou demander un droit de réponse : ouvrir une issue sur le dépôt GitHub.
