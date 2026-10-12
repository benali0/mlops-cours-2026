# Poster — contenu et mise en page

<!--
Ce fichier est le GABARIT du poster. Mettez-le en page avec l'outil de votre choix
(PowerPoint, LibreOffice Impress, Inkscape, LaTeX, Figma, Canva…) et rendez un PDF :
docs/poster.pdf, format A1 portrait (594 × 841 mm), présent au tag `final`.
Le poster est le support de vos 5 minutes communes en soutenance. Il se lit à 1,5 m :
peu de texte, de grands schémas, des chiffres. En option B, le même fichier dans les deux repos.
-->

## Règles de lisibilité

| Élément | Taille conseillée |
|---|---|
| Titre | 90 à 120 pt |
| Titres de blocs | 48 à 60 pt |
| Texte courant | 28 à 36 pt (jamais moins de 24 pt) |
| QR codes | au moins 5 cm de côté, URL en clair dessous |

Une idée par bloc, des phrases courtes, des chiffres avec leur contexte. Pas de capture de code.

## Blocs attendus (de haut en bas)

1. **En-tête** : titre du projet, noms et pseudos GitHub du binôme, groupe, option (A ou B).
2. **Le problème et les données** : une phrase chacun ; la matrice de coûts ; l'attribut
   sensible surveillé.
3. **Architecture de bout en bout** : un grand schéma, du dataset au projet déployé (DVC,
   pipeline et gates, registre MLflow, image, KServe, monitoring, CI/CD, fournisseur cloud).
4. **Résultats** : métrique primaire, coût métier au seuil retenu, équité par groupe (un petit
   tableau ou graphique).
5. **Exploitation** : une capture lisible du tableau de bord Grafana, les alertes, un incident
   rencontré et sa résolution en une ligne.
6. **Extensions** : un encadré par membre (nom de l'extension, niveau, ce qu'elle apporte, un
   chiffre ou une capture).
7. **QR codes** : projet déployé (page `/docs` de l'API) et repo GitHub ; en option B, un
   troisième pour le second repo. Chacun avec sa légende et l'URL en clair.

## Générer les QR codes

```bash
uvx --from "qrcode[pil]" qr "https://votre-projet-deploye/docs" > docs/qr-projet.png
uvx --from "qrcode[pil]" qr "https://github.com/votre-user/mlops-cours-2026" > docs/qr-repo.png
```

## Avant le tag `final`

| ☐ | Vérification |
|---|---|
| ☐ | `docs/poster.pdf` au format A1 portrait (`make check-m10` vérifie le format) |
| ☐ | QR codes testés avec deux téléphones différents, hors du Wi-Fi de l'école |
| ☐ | Le projet déployé répond depuis le QR code (`/docs`, puis une prédiction) |
| ☐ | Aucun nom de personne réelle dans les données affichées, aucun secret |
