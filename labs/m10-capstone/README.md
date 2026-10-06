---
module: 10
lab: 10
title: "Mini-projet MLOps"
subtitle: "Le repo construit lab après lab, une extension par étudiant, une soutenance avec défi en direct"
running_title: "Module 10 — Mini-projet MLOps"
duree: "Travail continu de S1 à S12 · lancement des extensions en S8 · soutenance de 25 min par binôme"
format: "Binôme · un repo commun, un cluster par membre · Linux / macOS / WSL2"
prerequis: "Labs 0 à 8 (le socle) ; Lab 9 recommandé pour l'extension RAG"
livrable: "Repo taggé j0 / j1 / j2 / final + rapport (10 p. max) + slides + vidéo de 3 min + soutenance"
stack: "Toute la stack du cours : DVC · MLflow · KFP · KServe · GitHub Actions · Argo CD · Prometheus · Evidently · Fairlearn"
---

# Module 10 — Mini-projet MLOps

*Faire passer un modèle du notebook à la production, à deux, et le défendre en direct.*

## Pourquoi ce mini-projet ?

Ce mini-projet ne cherche pas à évaluer votre capacité à entraîner un modèle performant. Il
évalue votre capacité à faire passer un modèle **du notebook à la production**, de manière
reproductible, observable, auditable et éthique. Une régression logistique qui traverse toutes
les étapes du cours vaut plus qu'un réseau de neurones seul dans un notebook Jupyter.

Il n'y a pas de « projet de fin de cours » à démarrer en S8 : **le mini-projet est le repo que
votre binôme construit lab après lab**, depuis le Lab 0. Chaque lab ajoute une brique au même
système ; à la fin du semestre, ce système complet, que nous appelons le **socle**, est évalué
comme un projet. Chaque membre du binôme y ajoute ensuite **une extension personnelle**, puis le
défend en soutenance, y compris face à un **incident provoqué en direct**.

> [!NOTE]
> **Les quatre principes directeurs**
>
> - **La prod, pas le notebook** : on juge le déploiement et l'exploitation, pas l'accuracy.
> - **La complétude, pas la sophistication** : un modèle simple qui traverse tous les labs gagne.
> - **La reproductibilité, pas la performance** : `git clone` + `make up` + `uv sync` +
>   `dvc repro` doivent suffire à reconstruire votre système, sur n'importe quel poste.
> - **Les compromis documentés, pas la perfection** : un compromis assumé et expliqué (dans un
>   ADR) vaut plus qu'une solution parfaite non justifiée.

## Le mini-projet en une page

| Élément | En bref |
|---|---|
| Équipe | Binôme, un seul repo `mlops-cours-2026`, chacun son cluster kind |
| Cas d'usage | Credit scoring (Statlog German Credit) par défaut, ou dataset libre validé avant le Lab 1 |
| Socle (commun) | Les Labs 0 à 8 appliqués à votre cas d'usage, vérifiés par `make check-m0` … `make check-m8` |
| Extension (individuelle) | Une par étudiant, choisie dans un catalogue de 16 (ou hors catalogue validée), niveau ★ à ★★★ |
| Jalons | `j0` Setup (fin S3) · `j1` MVP (fin S8) · `j2` Production (fin S11) · `final` 48 h avant la soutenance |
| Soutenance (S12) | 25 min : démo du socle, deux extensions, deux défis en direct, questions |
| Note | /40 : socle 12 + livrables écrits 6 (communs), extension 12 + défi et questions 10 (individuels) |
| Poids | 40 % de la note finale ; 8/20 minimum au mini-projet, sans compensation |

## Règles du jeu

### Un pipeline pour toute la promo

Tout le monde construit **le même pipeline** : mêmes labs, mêmes outils, mêmes noms
(expérience MLflow `scoring`, modèle `scoring-model@champion`, image `scoring-api`, namespace
`scoring`, pipeline `scoring-pipeline`…). Ce qui change d'un binôme à l'autre, c'est le jeu de
données, décrit dans un seul fichier : **`dataset.yaml`**. Aucun nom de colonne, de cible, de
classe ou de seuil n'est écrit en dur dans le code, les manifests, les tests ou les `check.sh` :
tout est lu dans `dataset.yaml` via `src/dataset_config.py`. Changer de dataset, c'est réécrire
`dataset.yaml` et `src/download.py`, rien d'autre.

### Le cas d'usage par défaut : credit scoring

| Élément | Valeur |
|---|---|
| Dataset | [Statlog German Credit](https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data) (UCI), licence CC BY 4.0 |
| Volume | 1 000 demandes de crédit, 20 variables (7 numériques, 13 catégorielles) |
| Cible | `credit_risk` ∈ {`good`, `bad`}, classe positive `bad` (30 %) |
| Attributs sensibles | âge (`<25` / `>=25`), statut personnel et sexe (`personal_status`), travailleur étranger (`foreign_worker`) |
| Matrice de coûts | faux négatif (accorder un crédit à un mauvais payeur) = **5**, faux positif (refuser un bon payeur) = **1** |
| Baseline de référence | régression logistique, ROC AUC ≈ 0,80 (split 80/20 stratifié, graine 42) |

C'est un cas d'usage à **haut risque** au sens de l'AI Act (annexe III : évaluation de la
solvabilité des personnes physiques) : l'équité, l'explicabilité et la traçabilité y sont des
exigences, pas des options.

### Choisir son propre dataset

Vous pouvez remplacer le credit scoring par votre propre jeu de données, **à condition qu'il
soit validé avant la séance du Lab 1 (S2)**. Conditions, toutes obligatoires :

| Condition | Pourquoi |
|---|---|
| Tabulaire, classification supervisée (binaire de préférence) | Le pipeline, les tests et le monitoring du cours sont écrits pour ce cas |
| 1 000 à 100 000 lignes | Assez pour valider et surveiller, assez peu pour entraîner sur un portable |
| Moins de 50 Mo | DVC, CI et cluster kind restent rapides |
| Licence ouverte | Le repo et les rapports sont publics |
| Téléchargeable par un script (`src/download.py`) | Reproductibilité : pas de téléchargement à la main |
| Au moins un attribut sensible | Le Lab 8 (équité) et le monitoring par groupe doivent avoir un objet |
| Aucune donnée identifiante | Ni nom, ni adresse, ni e-mail, ni numéro d'identité ou de téléphone |

**Proposer un dataset** : ouvrez une issue sur le repo du cours
([https://github.com/ORG_COURS/mlops-cours-2026](https://github.com/ORG_COURS/mlops-cours-2026),
bouton **Issues** > **New issue** > **Mini-projet : proposer un dataset libre**). Le formulaire
demande le **lien, la licence, la taille, la cible, les attributs sensibles et le contexte en
5 lignes** (qui utiliserait le modèle, pour quelle décision, ce que coûte chaque type d'erreur).
L'enseignant répond par le label `validé` ou `refusé`. Une fois validé, adaptez `dataset.yaml`
(mêmes clés, nouvelles valeurs) et `src/download.py`, puis lancez `uv run pytest
tests/test_dataset_config.py`.

**Retour au credit scoring possible à tout moment** : si votre dataset vous pose trop de
problèmes, revenez au fil rouge sans pénalité (restaurez `dataset.yaml` et `src/download.py`
depuis `upstream/main`, notez-le dans le journal et dans un ADR).

Exemples de datasets qui respectent les conditions (vérifiés sur l'UCI, octobre 2026) :

| Dataset | Lignes | Cible | Attributs sensibles | Point d'attention |
|---|---|---|---|---|
| [Adult (Census Income)](https://archive.ics.uci.edu/dataset/2/adult) | 48 842 | revenu > 50 k$ | sexe, origine, âge | valeurs manquantes codées `?` |
| [Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank+marketing) | 45 211 | souscription d'un dépôt | âge, statut marital | la variable `duration` n'est connue qu'après l'appel : fuite de cible à exclure |
| [Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) | 30 000 | défaut de paiement | sexe, âge, statut marital, éducation | fichier Excel, codes à décoder dans `src/download.py` |

Et des contre-exemples, tirés des anciens sujets du capstone :

| Ancien sujet | Statut | Raison |
|---|---|---|
| A — Scoring crédit RGPD | ✅ C'est le fil rouge | — |
| B — Fraude carte (Kaggle Credit Card Fraud) | ❌ | 284 807 lignes, environ 150 Mo, aucun attribut sensible (variables anonymisées par ACP), compte Kaggle requis. Alternative proche : *Default of Credit Card Clients* ci-dessus |
| C — RAG sur documentation interne | ↪️ Devient l'extension `rag-projet` | Pas tabulaire, mais excellent comme extension (voir le catalogue) |
| D — Contrôle visuel industriel (MVTec AD) | ❌ | Images, pas tabulaire ; licence non commerciale ; GPU recommandé |

### Travail en binôme

- **Un repo par binôme.** Un seul membre crée le repo `mlops-cours-2026` depuis le repo modèle
  du cours (Lab 0, étape 3.2 : fork ou *Use this template*) et ajoute son **partenaire et
  l'enseignant comme collaborateurs**. Le partenaire **clone** ce repo (il ne crée pas le sien).
- **Chacun son cluster.** Les deux membres font tourner le socle complet sur leur propre poste
  (`make up`, `make pf`, puis les installations de chaque lab). Le jour de la soutenance, l'un
  ou l'autre doit pouvoir faire la démo. Après chaque lab, celui qui n'a pas piloté remet son
  cluster à niveau à partir de `main` avec l'encadré « Second membre du binôme » de l'énoncé
  (`dvc repro` et non `dvc pull` : le remote DVC est propre à chaque cluster). À partir du
  Lab 6, la production est commune (Argo CD suit le même `main` sur les deux clusters) mais
  chaque MLflow a ses propres numéros de version : le modèle servi vient du MLflow d'un seul
  des deux membres, et c'est sur son cluster que tous les checks sont verts.
- **`main` est protégée contre les accidents** (pas de force-push, pas de suppression) et le
  travail humain passe par des branches `lab/mX-…` (un lab) et `ext/<nom>` (une extension),
  fusionnées par **pull request relue par le partenaire**. Seuls les commits automatiques du
  bot GitOps (Lab 6) arrivent directement sur `main`.
- **Pilote / copilote alterné** : à chaque lab, l'un tape (pilote), l'autre relit, anticipe,
  cherche dans la doc (copilote) ; on inverse au lab suivant. Les deux doivent savoir tout
  expliquer : le défi en direct est individuel.
- **Chacun commite depuis son propre compte GitHub** : l'historique Git sert à individualiser la
  note. Une session à deux sur un seul poste se commite avec un *trailer*
  `Co-authored-by: Prénom Nom <email>`.
- **Journal de bord** : `docs/journal.md`, 3 à 5 lignes par séance (qui a piloté, ce qui est
  fait, ce qui bloque, la suite).
- **Décisions** : au moins **3 ADR** dans `docs/adr/` au rendu final (voir « Livrables écrits »).
- **Rattrapage** : une correction est publiée après chaque rendu de lab. Un binôme en retard
  peut la reprendre pour remettre son socle à niveau ; il le fait **de façon traçable** (commit
  « reprise de la correction mX », ligne dans le journal) et adapte ce qui doit l'être à son
  dataset.

## Mettre en place le repo du binôme

À faire une fois, en S1 ou S2, par le membre qui possède le repo (sauf mention contraire).

### Collaborateurs et protection de `main`

1. **Settings** > **Collaborators** > **Add people** : le partenaire (rôle *Write*) et
   l'enseignant (compte communiqué en cours).
2. **Settings** > **Rules** > **Rulesets** > **New branch ruleset** : cible *Default branch*,
   activer **Block force pushes** et **Restrict deletions**, statut *Active*. N'activez **pas**
   *Require a pull request before merging* : le bot GitOps du Lab 6 (CI et `gitops … --push`)
   commite directement sur `main` et serait bloqué. La règle « tout passe par une PR relue »
   reste une convention du binôme, vérifiée au rendu (branches `ext/*` fusionnées par PR,
   historique Git).
   Ajoutez un second ruleset, **New tag ruleset**, ciblant les tags `j*` et `final` :
   **Restrict updates** et **Restrict deletions** (un tag de jalon ne se déplace plus).
3. **Settings** > **General** > **Pull Requests** : garder **Allow merge commits** et **Allow
   squash merging** (message par défaut : *Pull request title*), **décocher Allow rebase
   merging** : un rebase efface le nom de la branche `ext/<nom>` de l'historique, et le
   pré-contrôle de rendu ne retrouverait plus votre extension.

> [!WARNING]
> **Repo privé : protection de branche payante… sauf pour les étudiants**
> Sur un repo **public** (cas du fork), les règles de protection sont gratuites. Sur un repo
> **privé**, elles demandent GitHub Pro, offert avec le *GitHub Student Developer Pack*
> (GitHub Education). Sans l'un ni l'autre, restez en public.

### Fichiers du mini-projet déjà présents dans le repo

Le repo du cours contient déjà les gabarits du mini-projet :

```text
mlops-cours-2026/
├── README.md                     # à REMPLACER par le README de votre projet (au plus tard J1)
├── dataset.yaml  src/download.py # le contrat de données (à adapter si dataset libre)
├── docs/
│   ├── journal.md                # journal de bord (gabarit)
│   ├── adr/README.md             # règles et index des ADR
│   ├── adr/0000-modele.md        # modèle d'ADR
│   ├── dataset-card.md           # fiche du dataset, pré-remplie pour German Credit
│   ├── rapport-technique.md      # plan du rapport (le PDF rendu : docs/rapport.pdf)
│   └── soutenance.md             # déroulé de la soutenance et checklist de préparation
├── model-card/model-card.md      # produite au Lab 8
├── .github/
│   ├── ISSUE_TEMPLATE/           # formulaires : proposition de dataset, déclaration d'extension
│   ├── pull_request_template.md  # modèle de PR (titre « lab/… » ou « ext/<nom> : … »)
│   └── CODEOWNERS.exemple        # optionnel : relecteurs automatiques
└── labs/m10-capstone/            # cet énoncé + check.sh (pré-contrôle de rendu)
```

### Premier tour de piste

```bash
# Membre 2 (le partenaire) : cloner le repo du binôme
cd ~
git clone git@github.com:PROPRIETAIRE/mlops-cours-2026.git
cd ~/mlops-cours-2026
git remote add upstream https://github.com/ORG_COURS/mlops-cours-2026.git

# Les deux : son propre cluster et son propre .env
cp .env.example .env
make up && make pf

# Première PR : le journal de bord
git switch -c lab/m0-journal
$EDITOR docs/journal.md          # en-tête + entrée S1
git add docs/journal.md
git commit -m "lab/m0 : journal de bord"
git push -u origin lab/m0-journal
```

> **Sortie attendue :** GitHub propose d'ouvrir la PR ; le modèle de PR s'affiche. Le bouton
> **Merge** n'est pas bloqué (la règle *Require a pull request* n'est pas activée, voir
> « Collaborateurs et protection de `main` ») : par convention, le partenaire relit et approuve
> avant que vous ne fusionniez.

## Feuille de route sur 12 semaines

| Semaines | Phase | Labs | Ce que fait le binôme | Jalon |
|---|---|---|---|---|
| S1-S3 | Fondations | M0, M1 | Repo, clusters, choix du dataset (validé **avant S2**), `dataset.yaml`, DVC, MLflow | **J0 Setup** fin S3, tag `j0` |
| S4-S6 | Pipeline et qualité | M2, M3, M4 | Pipeline orchestré, gates de validation, image de service | — |
| S7-S8 | Mise en service | M5 | Modèle servi par KServe ; **chaque membre déclare son extension** | **J1 MVP** fin S8, tag `j1` |
| S9-S11 | Industrialisation | M6, M7, M8 (M9 hors socle) | CI/CD, monitoring, gouvernance ; extensions développées puis fusionnées | **J2 Production** fin S11, tag `j2` |
| S12 − 48 h | Rendu | — | Rapport, slides, vidéo, journal et ADR à jour | tag `final` |
| S12 | Soutenance | M10 | 25 min par binôme | — |

Ce que chaque jalon contient :

| Tag | Quand | Contenu attendu | Vérifié par |
|---|---|---|---|
| `j0` | fin S3 | `dataset.yaml` (validé si dataset libre), données versionnées par DVC, runs dans MLflow, `make check-m0` et `make check-m1` verts | `make check-m10 JALON=j0` |
| `j1` | fin S8 | pipeline avec gate de validation, modèle servi par KServe, `make check-m2` à `make check-m5` verts, extensions déclarées | `make check-m10 JALON=j1` |
| `j2` | fin S11 | CI/CD, monitoring, model card, `make check-m6` à `make check-m8` verts, **extensions fusionnées** | `make check-m10 JALON=j2` |
| `final` | 48 h avant la soutenance | tout ce qui précède + rapport PDF (10 p. max), slides, vidéo de démo (3 min), journal, ADR | `make check-m10` |

> [!IMPORTANT]
> **J0 et J1 ne sont pas notés**
> Ils servent à repérer tôt les binômes en difficulté pour les aider. Un tag absent ou un
> pré-contrôle très rouge à J0 ou J1 déclenche un point avec l'enseignant, pas une pénalité.
> Seul l'état au tag `final` est évalué.

**Format intensif** (4 jours) : les jalons tombent en fin de J1 (`j0`), de J2 (`j1`, extensions
déclarées) et de J3 (`j2`, socle complet), puis 2 à 3 semaines de finalisation (extensions
fusionnées, livrables écrits) avant le tag `final` et une soutenance à distance. Le dataset
libre doit alors être validé avant le premier jour.

## Rendre un jalon

Un jalon se rend en posant un **tag Git** sur le commit de `main` qui fait foi, puis en le
poussant. Rien d'autre à envoyer : l'enseignant lit le tag.

```bash
git switch main && git pull
make check-m10 JALON=j1          # pré-contrôle (voir la fin de l'énoncé)
git tag -a j1 -m "J1 MVP : pipeline avec gate, modèle servi par KServe"
git push origin j1
```

> **Sortie attendue :** `* [new tag] j1 -> j1`, et le tag apparaît sur GitHub dans **Code** >
> **Tags**.

> [!WARNING]
> **Un tag poussé ne se déplace pas**
> Si vous devez corriger après coup, ne réécrivez pas le tag (`git tag -f` et `git push -f`
> sont refusés par le *tag ruleset* et se voient dans l'historique) : poussez un correctif sur
> `main` et prévenez l'enseignant. Pour le tag `final`, l'heure du push sur GitHub fait foi.

## Le socle : ce qui est attendu

Le socle, c'est **l'ensemble des Labs 0 à 8 appliqués à votre cas d'usage**, dans votre repo,
au tag `final`. Chaque lab se termine par une vérification automatique `make check-mX` ; ces
mêmes vérifications servent à noter le socle.

| Lab | Brique du socle | Vérification |
|---|---|---|
| M0 | Cluster kind, registry, SeaweedFS (S3), MLflow | `make check-m0` |
| M1 | Données versionnées (DVC), expériences et registre MLflow (`scoring-model`) | `make check-m1` |
| M2 | Pipeline orchestré `scoring-pipeline` (KFP ; Airflow en comparaison) | `make check-m2` |
| M3 | Gates de validation des données et du modèle (GX, Evidently, tests comportementaux) | `make check-m3` |
| M4 | Image de service `scoring-api`, export ONNX, benchmark | `make check-m4` |
| M5 | InferenceService `scoring-model` (namespace `scoring`), autoscaling, canary | `make check-m5` |
| M6 | CI GitHub Actions, GitOps Argo CD, ré-entraînement déclenché | `make check-m6` |
| M7 | Prometheus, Grafana, alertes, drift Evidently | `make check-m7` |
| M8 | Scans (Trivy, ModelScan), équité (Fairlearn), explicabilité (SHAP), model card | `make check-m8` |
| M9 | LLMOps (RAG) — **hors socle** : non exigé, base de l'extension `rag-projet` | — |

Trois critères notent le socle (voir la grille) :

1. **Les checks sont verts** : `make check-m0` … `make check-m8` au tag `final`, sur le cluster
   qui sert à la démo.
2. **Reproductibilité** : depuis un poste qui n'a jamais vu le projet, `git clone`, `make up`,
   `uv sync` puis `dvc repro` suffisent à reconstruire les données et le modèle, et
   `dvc push` remplit le remote DVC de ce poste. `dvc pull` ne suffit pas : le remote DVC
   (`s3://dvc-store/scoring` sur `localhost:8333`) est le SeaweedFS **du cluster de chaque
   poste**, vide sur un cluster neuf (Lab 1, étape 10.4). L'enseignant peut le faire refaire en
   direct sur le poste du partenaire.
3. **Adaptation au cas d'usage** : le système sert *votre* problème et pas un exemple générique.
   Le seuil de promotion et le seuil de décision sont justifiés par la matrice de coûts ;
   l'équité est analysée et surveillée sur vos attributs sensibles ; les alertes ont un sens
   métier ; rien n'est écrit en dur (tout vient de `dataset.yaml`).

## L'extension personnelle

### Règles

- **Une extension par étudiant**, choisie dans le catalogue ci-dessous ou hors catalogue.
- Les **deux membres d'un binôme choisissent deux extensions différentes**.
- **Au plus 3 binômes par extension et par groupe** : premier déclaré, premier servi (la date
  de l'issue fait foi).
- Le **niveau plafonne** la note d'extension : ★ → **8/12**, ★★ → **11/12**, ★★★ → **12/12**.
  Une extension ★ parfaitement réussie vaut donc 8 ; une ★★★ inaboutie peut valoir moins.
- **Livrables** de chaque extension :
  - une branche `ext/<nom>` fusionnée dans `main` par une **PR relue** par le partenaire, dont
    le titre commence par `ext/<nom>` ;
  - des **tests** automatisés (pytest, CI ou script de vérification rejouable) ;
  - un **ADR** (la décision structurante de l'extension) ;
  - **une page** dans le rapport technique.
- **Hors catalogue** : possible si l'extension est validée **avant la fin de S8** (même issue,
  option « hors-catalogue », avec niveau proposé, compétences visées et critères de réussite).
- L'extension **s'appuie sur le socle** (elle l'étend, elle ne le remplace pas) et ne doit pas
  le casser : les `make check-mX` restent verts après la fusion.

### Déclarer son extension

1. Lisez le catalogue et vérifiez les déclarations existantes : repo du cours > **Issues**,
   filtre `label:extension` (et votre groupe dans le titre).
2. **New issue** > **Mini-projet : déclarer mon extension**. Une issue **par étudiant**.
   Renseignez groupe, repo, partenaire, extension (liste déroulante), objectif, plan
   (étapes, tests, ADR, RAM supplémentaire estimée) et cochez les engagements.
3. L'enseignant répond par le label `validé` (ou propose une alternative si le quota du groupe
   est atteint).
4. Dans le repo du binôme : `git switch -c ext/<nom>`, premier commit (squelette + ADR au statut
   « proposé »), puis ouvrez tout de suite une PR en brouillon (*Draft*) : votre partenaire suit
   l'avancement et la relecture finale sera plus rapide.

Date limite : **fin de S8** (jalon J1) pour toutes les déclarations.

> [!TIP]
> **Pensez mémoire**
> Votre cluster kind héberge déjà tout le socle. Avant de choisir une extension qui installe
> une brique lourde (LLM local, contrôleur d'admission, base de données), vérifiez la RAM libre
> (`docker stats`, `kubectl top nodes`) et prévoyez de suspendre ce qui ne sert pas (Airflow,
> par exemple, après le Lab 2).

### Catalogue

| Nom de branche `ext/…` | Extension | Niveau | Compétences |
|---|---|---|---|
| `feature-store` | Feature store en ligne | ★★ | C1, C3 |
| `hpo` | Optimisation d'hyperparamètres orchestrée (Optuna/Katib, MLflow) | ★★ | C1, C2 |
| `retrain-planifie` | Ré-entraînement planifié | ★★ | C2, C4 |
| `batch-scoring` | Scoring batch | ★★ | C3 |
| `onnx-quantifie` | Inférence optimisée ONNX quantifié | ★★ | C3 |
| `scale-to-zero` | Scale-to-zero | ★★ | C3 |
| `shadow` | Déploiement shadow | ★★★ | C3, C5 |
| `ab-test` | Test A/B | ★★★ | C3, C5 |
| `tests-comportementaux` | Tests comportementaux en CI | ★★ | C4 |
| `gate-equite` | Gate d'équité Fairlearn en CI | ★★ | C4, C6 |
| `drift-predictions` | Drift sur les prédictions | ★★★ | C5 |
| `tracing` | Tracing de bout en bout OpenTelemetry/Jaeger | ★★ | C5 |
| `explain-api` | Explicabilité en production `/explain` (SHAP) | ★★ | C6 |
| `supply-chain` | Chaîne de confiance cosign + admission | ★★★ | C6 |
| `model-card-auto` | Model card automatique | ★ | C6 |
| `rag-projet` | Assistant RAG du projet + Ragas en CI | ★★★ | C4, C6 |

Rappel des compétences du cours : **C1** pipeline reproductible et versionné ; **C2**
orchestration sur Kubernetes ; **C3** déploiement selon différents patterns (latence, débit,
coût) ; **C4** CI/CD/CT avec tests de données et de modèles ; **C5** monitoring, drift,
alerting, rollback, canary ; **C6** sécurité, gouvernance, équité, explicabilité.

Pour chaque extension ci-dessous : les **attendus minimaux** définissent ce qui doit exister
pour que l'extension soit considérée comme « fonctionnelle et intégrée » ; les **critères de
réussite** sont ce que le jury vérifie en démo et dans le repo. Dans tous les cas, rien n'est
écrit en dur : colonnes, cible, groupes sensibles et seuils viennent de `dataset.yaml` ou d'un
fichier de configuration versionné.

### `feature-store` — Feature store en ligne ★★ (C1, C3)

Les features ne sont plus envoyées dans la requête : l'API les récupère à la volée dans un
magasin en ligne, à partir d'un identifiant.

**Attendus minimaux**

- Feast (`features/`) avec un *online store* déployé dans le cluster (Redis ou PostgreSQL) et un
  registre partagé. Si votre dataset n'a pas d'identifiant, créez un identifiant stable et un
  horodatage dans l'étape de préparation.
- Matérialisation planifiée (`feast materialize-incremental` dans un CronJob ou une étape du
  pipeline).
- Une route de prédiction qui accepte un identifiant et appelle `get_online_features` ; la liste
  des features vient de `dataset.yaml`.
- Un test de cohérence entraînement / service : pour un échantillon d'identifiants, les
  features en ligne sont égales à celles de l'entraînement (jointure *point-in-time*).

**Critères de réussite**

- Démo : une valeur change dans la source, on matérialise, la prédiction change sans
  redéployer le modèle.
- Le test de *skew* échoue si l'on modifie la transformation d'un seul côté.
- Latence ajoutée mesurée (P95 avec et sans feature store) et discutée dans l'ADR (choix du
  magasin en ligne).

### `hpo` — Optimisation d'hyperparamètres orchestrée ★★ (C1, C2)

La recherche d'hyperparamètres devient une étape du pipeline, tracée et bornée, au lieu d'une
boucle dans un notebook.

**Attendus minimaux**

- Espace de recherche versionné (`params.yaml`) ; Optuna avec une étude persistée (SQLite sur
  volume ou PostgreSQL) exécutée dans le pipeline KFP (essais parallèles via `dsl.ParallelFor`
  ou plusieurs workers), ou Katib si votre poste le permet.
- Chaque essai est un run MLflow enfant d'un run parent (paramètres, métrique primaire, coût
  métier).
- Objectif aligné sur `dataset.yaml` (métrique primaire, ou coût métier au seuil optimal) ;
  budget paramétrable (nombre d'essais ou durée) ; élagage (*pruner*) actif.
- Le meilleur modèle est enregistré comme `challenger` et ne devient `champion` qu'en passant
  la gate existante.

**Critères de réussite**

- Relancer avec la même graine redonne le même meilleur essai (ou l'écart est expliqué).
- Gain mesuré par rapport au modèle du socle sur le jeu de **test** (pas de validation), avec
  validation croisée ou intervalle de confiance.
- Importance des hyperparamètres visible (graphique Optuna enregistré dans MLflow) ; ADR :
  Optuna, grid search ou Katib, et le coût en temps de calcul.

### `retrain-planifie` — Ré-entraînement planifié ★★ (C2, C4)

Le modèle se ré-entraîne seul à intervalle régulier, et ne remplace le champion que s'il fait
mieux.

**Attendus minimaux**

- Exécution récurrente du pipeline (*recurring run* KFP, CronJob Kubernetes ou DAG Airflow
  planifié) sur une fenêtre de données paramétrée.
- Simulation de « nouvelles données » : des lots versionnés par DVC ajoutés au fil des
  exécutions (tranches du dataset, rééchantillonnage).
- Comparaison champion / challenger sur un jeu d'évaluation commun ; promotion automatique de
  l'alias `champion` uniquement si le challenger est meilleur **et** que les gates sont vertes ;
  sinon le run est marqué « rejeté » avec la raison.
- Idempotence (rejouer la même date ne crée pas de doublon) et traçabilité (version des
  données et commit dans les tags du run MLflow).

**Critères de réussite**

- Démo : déclenchement manuel de la planification, nouveau challenger promu ou rejeté avec une
  raison visible.
- Un lot de données dégradé ne remplace pas le champion (test automatisé).
- ADR : ré-entraînement planifié ou déclenché par le drift (Lab 6), fréquence et coût.

### `batch-scoring` — Scoring batch ★★ (C3)

Scorer un fichier entier de demandes en une fois, à côté du service en ligne.

**Attendus minimaux**

- Un Job Kubernetes (ou CronJob, ou composant KFP) qui charge
  `models:/scoring-model@champion`, lit un fichier d'entrée sur S3 et écrit sur S3 les
  prédictions, probabilités, version du modèle et horodatage (Parquet ou CSV).
- Traitement par morceaux pour borner la mémoire ; autant de lignes en sortie qu'en entrée ;
  lignes invalides isolées dans un fichier de rejet, avec la validation du Lab 3.
- Métriques du job (durée, lignes par seconde, rejets) exposées (Pushgateway ou logs
  structurés).

**Critères de réussite**

- Test de cohérence : sur un échantillon, prédictions batch identiques à celles de l'API.
- Démo : dépôt d'un fichier, exécution du job, résultats lisibles ; rejouer donne la même
  sortie.
- Débit mesuré sur un fichier 100 fois plus gros (rééchantillonné) ; ADR : Job Kubernetes,
  pipeline KFP ou appels à l'API ligne à ligne.

### `onnx-quantifie` — Inférence optimisée ONNX quantifié ★★ (C3)

Aller au-delà de l'export ONNX du Lab 4 : optimiser, quantifier, servir et prouver que la
qualité tient.

**Attendus minimaux**

- Optimisations de graphe ONNX Runtime et quantification INT8 (dynamique avec
  `onnxruntime.quantization.quantize_dynamic`, ou statique avec un jeu de calibration).
- Le modèle optimisé est servi dans KServe (runtime ONNX, Triton, ou votre image avec
  ONNX Runtime).
- Banc d'essai reproductible (même machine, même charge Locust) : taille, latence P50/P95,
  métrique primaire, coût métier, taux de prédictions différentes de scikit-learn.
- Gate en CI : écart de métrique au-delà d'un seuil versionné = échec.

**Critères de réussite**

- Tableau scikit-learn / ONNX FP32 / ONNX INT8 dans le rapport.
- Démo du gate qui refuse une quantification trop agressive.
- ADR honnête : sur un petit modèle tabulaire, le gain de latence peut être faible ; on le
  mesure et on conclut (le gain peut être ailleurs : mémoire, image, démarrage).

### `scale-to-zero` — Scale-to-zero ★★ (C3)

Ne payer aucune ressource quand personne n'appelle le modèle, et maîtriser le prix à payer au
réveil.

**Attendus minimaux**

- InferenceService en mode Knative avec `minReplicas: 0`, annotations d'autoscaling réglées
  (fenêtre de stabilité, durée de rétention).
- Mesure du démarrage à froid sur au moins 10 cycles (P50/P95), décomposée : planification du
  pod, tirage de l'image, chargement du modèle, première inférence.
- Au moins une optimisation du démarrage à froid (image allégée, modèle embarqué plutôt que
  téléchargé, préchargement, `initial-scale`, rétention) mesurée avant / après.
- Panneau Grafana montrant les passages à zéro et les démarrages à froid.

**Critères de réussite**

- Démo : service à zéro pod, une requête, réponse correcte, temps affiché.
- Démarrage à froid réduit et chiffré. Si votre socle M5 utilise déjà `minReplicas: 0`,
  l'extension porte entièrement sur la mesure et l'optimisation.
- ADR : ressources économisées contre latence (SLO), avec une recommandation par
  environnement (staging, prod).

### `shadow` — Déploiement shadow ★★★ (C3, C5)

Le challenger voit tout le trafic réel, mais ses réponses ne servent à personne : on compare
sans risque.

**Attendus minimaux**

- Duplication de 100 % des requêtes de production vers le challenger, sans renvoyer sa réponse
  au client (proxy ou *transformer* qui duplique de façon asynchrone, ou *mirroring* d'un
  maillage de services si vous en installez un).
- La latence du champion n'est pas dégradée : appel au challenger non bloquant, avec délai
  maximal.
- Journalisation des paires (identifiant de requête, prédiction champion, prédiction
  challenger, latences) ; tableau de bord du taux de désaccord et des écarts de latence.
- Critère de sortie du shadow écrit à l'avance (taux de désaccord, P95, nombre de requêtes),
  suivi d'une bascule en canary.

**Critères de réussite**

- Démo : trafic simulé, le tableau de désaccord se remplit ; on arrête le challenger, le client
  ne voit aucune différence.
- Test automatisé : challenger en panne ou lent sans impact sur la réponse ni sur la latence.
- ADR : shadow ou canary (risque, coût, duplication de données personnelles).

### `ab-test` — Test A/B ★★★ (C3, C5)

Deux modèles en production, une décision statistique sur une métrique métier fixée à l'avance.

**Attendus minimaux**

- Deux modèles servis simultanément ; affectation déterministe et « collante » par unité
  (hachage d'un identifiant), proportion paramétrable.
- Chaque prédiction journalise sa variante ; la vérité terrain arrive en différé (labels du jeu
  de test réinjectés plus tard).
- Métrique de décision fixée **avant** le test (par exemple le coût métier moyen par demande,
  d'après la matrice de coûts), taille d'échantillon calculée, test statistique (bootstrap ou
  test de proportions) avec intervalle de confiance.
- Tableau de bord par variante.

**Critères de réussite**

- Démo : conclusion statistique (« B gagne » ou « pas de différence détectable ») avec son
  intervalle.
- Test automatisé : une même unité reçoit toujours la même variante.
- ADR : A/B, canary ou bandit ; risques éthiques (traiter différemment des demandeurs) ; durée
  minimale du test.

### `tests-comportementaux` — Tests comportementaux en CI ★★ (C4)

Transformer les quelques tests comportementaux du Lab 3 en une suite systématique, générée et
bloquante.

**Attendus minimaux**

- Suite de type CheckList (Ribeiro et al., 2020) **générée à partir de `dataset.yaml`** : tests
  minimaux de fonctionnement (MFT), d'invariance (INV : attributs sensibles et variables sans
  effet attendu) et directionnels (DIR : monotonies déclarées dans un fichier de
  configuration).
- Exécution en CI GitHub Actions sur le modèle candidat (téléchargé depuis MLflow ou entraîné
  en CI sur un échantillon), bloquante pour la PR ou la promotion.
- Tolérances explicites (par exemple au plus 2 % de décisions qui basculent en INV) et rapport
  lisible (taux d'échec par test, exemples) en artefact CI et dans MLflow.

**Critères de réussite**

- Un modèle volontairement défectueux (variable permutée, modèle biaisé) fait échouer la CI :
  on teste les tests.
- Ajouter une variable dans `dataset.yaml` ajoute automatiquement ses tests.
- ADR : quelles propriétés exiger, et pourquoi (lien avec la matrice de coûts et l'équité).

### `gate-equite` — Gate d'équité Fairlearn en CI ★★ (C4, C6)

L'analyse d'équité du Lab 8 devient une condition de promotion, comme la performance.

**Attendus minimaux**

- Métriques Fairlearn (écart de parité démographique, écart d'*equalized odds*, taux de
  sélection, TPR et FPR par groupe) pour chaque attribut sensible de `dataset.yaml`, calculées
  dans le pipeline ou en CI.
- Seuils dans un fichier versionné, gate bloquante (promotion ou PR) avec un message qui dit
  quel groupe et quelle métrique échouent.
- Rapport par groupe (MLflow et artefact CI) avec effectifs et intervalles (bootstrap) : un petit
  groupe ne doit pas faire échouer la gate au hasard.
- Une stratégie d'atténuation (`ThresholdOptimizer` ou repondération) essayée et documentée.

**Critères de réussite**

- Démo : un modèle volontairement biaisé est bloqué ; après atténuation, il passe, et le coût
  en performance est chiffré.
- ADR : choix de la métrique d'équité (parité ou égalité des chances) au regard du cas d'usage
  et de l'AI Act.

### `drift-predictions` — Drift sur les prédictions ★★★ (C5)

Surveiller ce que le modèle répond et ce qu'il vaut réellement, pas seulement ce qu'il reçoit.

**Attendus minimaux**

- Journalisation de chaque prédiction (features, score, version du modèle, identifiant,
  horodatage) vers S3 ou une base.
- Drift de la distribution des scores et du taux de décision (Evidently, fenêtres glissantes),
  en plus du drift des features du Lab 7.
- Boucle de vérité terrain différée : labels simulés arrivant avec retard, jointure par
  identifiant, performance réelle (métrique primaire, coût métier) au fil du temps.
- Alertes Prometheus distinctes « drift des prédictions » et « dégradation de performance »,
  avec runbook ; déclenchement possible du ré-entraînement du Lab 6.

**Critères de réussite**

- Démo : une dérive injectée déclenche l'alerte sur les prédictions avant que la vérité terrain
  ne confirme la baisse.
- Fausses alertes discutées (seuils, taille de fenêtre).
- ADR : quels signaux surveiller en l'absence de labels, et quand se fier à la vérité terrain.

### `tracing` — Tracing de bout en bout OpenTelemetry/Jaeger ★★ (C5)

Suivre une requête à travers tous les composants, et trouver en une minute où elle perd son
temps.

**Attendus minimaux**

- Instrumentation OpenTelemetry de l'API de prédiction (auto-instrumentation FastAPI + spans
  manuels « validation », « prétraitement », « inférence ») et propagation du contexte vers les
  appels sortants.
- Collecte OTLP (OpenTelemetry Collector, ou Grafana Alloy installé au Lab 7) vers Jaeger
  (*all-in-one*) ou Tempo.
- Identifiant de trace dans les logs (corrélation Loki et traces) et dans un en-tête de réponse.
- Échantillonnage configuré (par exemple 10 % des requêtes et 100 % des erreurs).

**Critères de réussite**

- Démo : une requête lente ou en erreur, sa trace, le span responsable identifié en moins d'une
  minute.
- Surcoût de l'instrumentation mesuré (P95 avec et sans).
- ADR : Jaeger ou Tempo, stratégie d'échantillonnage.

### `explain-api` — Explicabilité en production `/explain` (SHAP) ★★ (C6)

Le demandeur refusé a droit à une explication : l'API la fournit, vite et de façon vérifiable.

**Attendus minimaux**

- Une route `/explain` (ou un *explainer* KServe) qui renvoie les contributions SHAP des k
  variables les plus influentes et une phrase lisible (« Principaux facteurs de la décision :
  … »).
- L'explication porte sur le modèle servi (même version, même prétraitement) et parle en
  variables d'origine (pas en colonnes one-hot).
- Budget de latence défini et respecté (explainer construit une seule fois, données de fond
  résumées).
- Tests : additivité (somme des contributions + valeur de base = sortie du modèle, à une
  tolérance près), stabilité, erreur 4xx sur une entrée invalide.

**Critères de réussite**

- Démo : deux demandes proches aux décisions opposées, explications cohérentes avec l'écart.
- P95 de `/explain` mesuré ; aucune donnée individuelle d'autres personnes exposée (données de
  fond agrégées).
- ADR : SHAP local ou alternatives (contrefactuels, règles), lien avec l'article 22 du RGPD.

### `supply-chain` — Chaîne de confiance cosign + admission ★★★ (C6)

Seules les images construites et signées par votre CI peuvent tourner dans le namespace
`scoring`.

**Attendus minimaux**

- Signature de l'image `scoring-api` en CI avec cosign (*keyless* via l'OIDC de GitHub Actions,
  ou paire de clés dont la clé privée est un secret de CI) ; SBOM (Trivy ou Syft) attaché comme
  attestation.
- Politique d'admission dans le cluster (Sigstore *policy-controller* ou Kyverno) sur le
  namespace `scoring` : une image non signée, ou signée par une autre identité, est refusée.
- Vérification documentée pour le registre utilisé (GHCR au Lab 6, registry local
  `localhost:5001`).
- En bonus apprécié : empreinte ou signature de l'artefact du modèle vérifiée au chargement.

**Critères de réussite**

- Démo : une image signée est admise ; une image modifiée ou non signée est refusée avec le
  message du contrôleur d'admission.
- Procédure de rotation et de révocation écrite.
- ADR : *keyless* ou clés, menaces couvertes, niveau SLSA visé.

### `model-card-auto` — Model card automatique ★ (C6)

La model card du Lab 8 se met à jour toute seule à chaque nouveau champion.

**Attendus minimaux**

- Un script (`python -m …`) qui génère `model-card/model-card.md` à partir de MLflow (version,
  run, paramètres, métriques globales et par groupe), de `dataset.yaml` et des rapports
  d'équité, via un gabarit (Jinja2).
- Les sections rédigées à la main (usage prévu, limites, considérations éthiques) sont
  conservées d'une génération à l'autre.
- Exécution automatique (pipeline ou CI) à chaque nouveau champion, avec le diff visible dans
  une PR.

**Critères de réussite**

- Promotion d'un nouveau modèle : la model card est régénérée sans intervention et ses chiffres
  sont identiques à ceux de MLflow (test automatisé).
- ADR : ce qui peut être automatisé dans une model card, et ce qui ne doit pas l'être.

### `rag-projet` — Assistant RAG du projet + Ragas en CI ★★★ (C4, C6)

L'ancien sujet « RAG sur documentation interne », appliqué à votre propre projet : un assistant
d'exploitation qui connaît votre README, vos ADR et votre runbook.

**Attendus minimaux**

- À partir du Lab 9 : un assistant qui répond aux questions d'exploitation du projet
  (README, ADR, runbook, énoncés des labs, model card) en citant ses sources.
- Ingestion versionnée et rejouable : ré-indexation à chaque modification de `docs/`.
- Jeu de référence (*golden set*) d'au moins 20 questions et réponses attendues, versionné ;
  évaluation Ragas (fidélité, pertinence des réponses).
- Gate : fidélité au-dessus d'un seuil pour fusionner. Si la CI GitHub ne peut pas faire tourner
  le LLM, l'évaluation tourne dans le cluster ou sur un runner auto-hébergé et publie un statut
  de commit. Garde-fou contre l'injection de prompt, avec au moins 10 tentatives documentées.

**Critères de réussite**

- Démo : une question d'incident (« comment revenir au modèle précédent ? ») obtient une
  réponse juste et sourcée ; on modifie un document, la réponse suit.
- Une régression volontaire (mauvais découpage des documents) fait échouer la gate.
- Ressources mesurées (RAM du LLM local) ; ADR : modèle et taille retenus.

## La soutenance

**25 minutes par binôme**, en S12, sur le cluster de l'un des deux membres :

| Durée | Qui | Contenu |
|---|---|---|
| 5 min | Binôme | **Démo du socle de bout en bout** : une modification (code, données ou paramètre) traverse la chaîne jusqu'au modèle servi, et se voit dans le monitoring |
| 2 × 5 min | Chacun | **Son extension** : objectif, démonstration en direct, tests, ADR |
| 2 × 4 min | Chacun | **Défi en direct** : un incident tiré au sort est provoqué sur le socle ; vous le diagnostiquez et le corrigez à voix haute |
| 2 min | Binôme | **Questions** du jury |

Le **défi** est tiré au sort parmi six familles d'incidents : **données invalides**, **drift**,
**service qui ne répond plus**, **déploiement bloqué**, **modèle dégradé**, **secret
manquant**. Le partenaire ne souffle pas. On évalue la **démarche** : hypothèses formulées,
outils choisis pour les vérifier, lecture des signaux, correction (ou, faute de temps, la
correction que vous appliqueriez et comment vous vérifieriez qu'elle marche).

**Plan B** si votre cluster ne démarre pas le jour J : la vidéo de démo de 3 minutes remplace
la démo du socle, et le défi se fait sur le cluster de l'enseignant, avec votre repo
reconstruit par `dvc repro` (le remote DVC de votre cluster n'est pas joignable d'un autre
poste) : d'où l'importance du test de reproductibilité avant le tag `final`.

Le déroulé détaillé et la checklist de préparation (J-7, J-2, veille et jour J) sont dans
`docs/soutenance.md`.

## Préparer le défi en direct

Le défi ne se révise pas la veille : il se prépare en **cassant votre propre socle**, souvent,
et à deux. L'objectif n'est pas de connaître les incidents à l'avance (ils ne sont pas
publiés), mais d'avoir une **méthode** et des **réflexes d'outils**.

### Le jeu du chaos en binôme

À partir de J1, une fois par semaine, 15 minutes :

1. **A** casse le socle de **B** en secret (une seule perturbation, réversible, notée sur un
   papier), sur le cluster de B ou dans une branche.
2. **B** a **4 minutes chronométrées** pour diagnostiquer à voix haute, puis corriger.
3. **A** explique ce qu'il a fait ; on note dans le journal le temps, la piste suivie, l'outil
   qui a donné la réponse.
4. On inverse les rôles la semaine suivante.

Idées de perturbations, une famille à la fois (à vous d'inventer les détails) :

| Famille | Idées de perturbations à vous infliger | Signaux à apprendre à lire |
|---|---|---|
| Données | Altérer une **copie** des données : types, domaines de valeurs, colonnes, proportion de manquants, modalités inconnues | Quelle gate s'arrête, avec quel message ; `dvc status` ; rapport GX |
| Drift | Rejouer du trafic dont la distribution s'écarte de celle de l'entraînement, sur une ou plusieurs variables | Rapport Evidently, alerte, tableau de bord : quelle variable, depuis quand |
| Service | Toucher aux ressources, au nombre de répliques, à la sonde de santé, au réseau ou à l'image d'un service | `kubectl get/describe`, événements, `logs --previous`, statut de l'InferenceService |
| Déploiement | Introduire une erreur dans un manifest, une valeur Kustomize, un tag d'image, une étape de CI | Argo CD (*sync*, *diff*), onglet Actions, `kubectl rollout status` |
| Modèle | Promouvoir un mauvais modèle, mélanger des versions, dégrader un entraînement | MLflow (alias, runs, métriques), gates, métriques de prédiction |
| Secrets | Supprimer, renommer ou corrompre un identifiant dont un composant a besoin | Pods en erreur de démarrage, messages d'authentification dans les logs |

> [!CAUTION]
> **On casse ce qu'on sait réparer**
> Ne jouez au chaos que sur des choses versionnées ou recréables (`git`, Argo CD, `make`).
> Jamais de `make down`, de suppression de PVC ou de bucket : vous perdriez MLflow, les données
> DVC et une soirée.

### Une méthode en cinq temps (à dire à voix haute)

1. **Observer** le symptôme précis : qu'est-ce qui ne marche pas, depuis quand, pour qui ?
2. **Formuler une hypothèse** (« le pod ne démarre pas parce que… »).
3. **Vérifier** avec l'outil le plus direct (pas en relisant tout le code).
4. **Corriger** par le chemin normal (commit + Argo CD, pipeline, `dvc`), pas par un
   bricolage invisible.
5. **Vérifier la correction** (`make check-mX`, requête de prédiction, alerte résolue) et dire
   comment on empêcherait le retour de l'incident (test, alerte, gate).

Commandes qui reviennent souvent :

```bash
kubectl get pods -A | grep -v Running                    # ce qui ne va pas, partout
kubectl -n scoring get events --sort-by=.lastTimestamp   # le récit de ce qui s'est passé
kubectl -n scoring describe pod <pod>                    # conditions, sondes, montages
kubectl -n scoring logs <pod> --previous                 # les logs du conteneur qui a planté
kubectl -n scoring get inferenceservice scoring-model    # READY, URL, révision
make check-m5                                            # l'état attendu, item par item
```

> [!TIP]
> **Écrivez votre runbook**
> Chaque incident rencontré (provoqué ou non) mérite trois lignes dans `docs/runbook.md` :
> symptôme, diagnostic, correction. C'est aussi une excellente source pour l'extension
> `rag-projet`.

## Grille d'évaluation (sur 40)

| Bloc | Pts | Qui | Critère | Pts |
|---|---|---|---|---|
| **Socle** | **12** | Binôme | `make check-m0` → `make check-m8` verts au tag `final` | 6 |
| | | | Reproductibilité : `git clone`, `make up`, `uv sync`, `dvc repro` (+ `dvc push`) | 3 |
| | | | Adaptation au cas d'usage (seuils et coûts, équité, alertes, rien en dur) | 3 |
| **Extension** | **12** | Individuel | Fonctionne et est intégrée au socle (attendus minimaux) | 5 |
| | | | Tests, ADR, documentation (page du rapport) | 3 |
| | | | Maîtrise à l'oral (démo, questions sur les choix) | 4 |
| | | | *Plafond selon le niveau : ★ → 8, ★★ → 11, ★★★ → 12* | |
| **Défi et questions** | **10** | Individuel | Diagnostic de l'incident | 4 |
| | | | Démarche et outils | 3 |
| | | | Correction et réponses aux questions | 3 |
| **Livrables écrits** | **6** | Binôme | README, dataset card, model card | 3 |
| | | | Rapport technique (10 pages max) | 2 |
| | | | Journal de bord et historique Git | 1 |
| **Total** | **40** | | | |

- **Note finale du cours** : labs 30 %, mini-projet 40 %, examen 30 %.
- **Mini-projet ≥ 8/20 obligatoire** (soit 16/40), sans compensation possible. Présence
  obligatoire à la soutenance.
- Les blocs « socle » et « livrables écrits » sont communs au binôme ; l'historique Git et le
  journal permettent de les individualiser si un membre n'a visiblement pas contribué.

## Livrables écrits

Tous sont dans le repo, au tag `final`.

| Livrable | Emplacement | Gabarit |
|---|---|---|
| README du projet | `README.md` (racine) | section suivante |
| Dataset card | `docs/dataset-card.md` | pré-remplie pour German Credit |
| Model card | `model-card/model-card.md` | Lab 8 |
| ADR (3 minimum) | `docs/adr/NNNN-*.md` | `docs/adr/0000-modele.md` |
| Journal de bord | `docs/journal.md` | gabarit fourni |
| Rapport technique | `docs/rapport.pdf` (10 pages max) | plan : `docs/rapport-technique.md` |
| Slides | `docs/slides.pdf` (ou `.pptx`, `.odp`, `.html`) | libre |
| Vidéo de démo (3 min) | lien dans la section « Démo » du README (ou `docs/demo.mp4`) | libre |

### README du projet

Le README racine est, au départ, celui du cours : **remplacez-le par celui de votre projet au
plus tard au jalon J1** (les énoncés restent dans `labs/`). Un lecteur doit pouvoir démarrer
votre système en cinq commandes, sans lire 200 lignes d'histoire. Le pré-contrôle cherche ces
titres de section et les commandes `make up` et `dvc repro` :

```markdown
# Scoring de crédit — binôme Alice Martin & Bob Durand

Une phrase : quel problème, pour qui, quel résultat.

## Démarrage rapide
    git clone git@github.com:PROPRIETAIRE/mlops-cours-2026.git && cd mlops-cours-2026
    cp .env.example .env && make up && make pf
    uv sync && dvc repro && dvc push
    (commande qui lance le pipeline, puis commande qui déploie)
    (requête de prédiction d'exemple)

## Cas d'usage
## Données            (5 lignes + lien vers docs/dataset-card.md)
## Architecture       (schéma de bout en bout + liens vers les ADR)
## Modèle et résultats (métrique primaire, coût métier, lien vers la model card)
## Extensions         (qui a fait quoi, lien vers chaque PR ext/*)
## Équipe             (noms, pseudos GitHub)
## Démo               (lien de la vidéo de 3 minutes)
```

### Dataset card

Fiche descriptive du jeu de données, inspirée des *Datasheets for Datasets* (Gebru et al.).
Le gabarit `docs/dataset-card.md` est **pré-rempli pour German Credit**, y compris ses limites
connues (période 1973-1975, sur-échantillonnage des mauvais payeurs, erreurs de codage
documentées par Grömping en 2019, `personal_status` qui ne permet pas de retrouver le sexe) ; à
vous de le relire, de compléter les champs `[À compléter]` et d'y ajouter vos propres constats.
Sur un dataset libre, réécrivez-la entièrement en gardant ses sections :

| Section | Contenu |
|---|---|
| En-tête | nom (`dataset.yaml`), source, licence, obtention (`src/download.py`), version DVC, taille, tâche, cible |
| 1. Motivation | pourquoi ce dataset, qui l'a créé, pour quel usage |
| 2. Composition | une ligne = ?, variables, répartition de la cible, qualité, données personnelles |
| 3. Attributs sensibles | groupes, effectifs, taux de classe positive par groupe, limites |
| 4. Collecte et biais connus | période, échantillonnage, biais de sélection, erreurs connues |
| 5. Prétraitement | ce que font `src/download.py` et le préprocesseur, découpage |
| 6. Usages | prévus, déconseillés, matrice de coûts, cadre réglementaire |
| 7. Distribution et maintenance | licence, stockage, évolution |
| Citation | références à citer |

### ADR

Un ADR (*Architecture Decision Record*) fige une décision : contexte, options, choix,
conséquences. Au moins **3** au rendu final : **un sur le socle au minimum, et un par
extension**. Règles et idées de sujets : `docs/adr/README.md`. Le modèle à copier :

```markdown
<!-- Fichier : docs/adr/0000-modele.md -->
# ADR-0000 — Titre court de la décision, à l'infinitif

<!--
Modèle d'Architecture Decision Record (inspiré de M. Nygard, 2011, et du format MADR).
Copier ce fichier en docs/adr/NNNN-titre-en-kebab-case.md (NNNN = numéro suivant, 0001, 0002…),
remplacer chaque [À compléter], supprimer ces commentaires. Une décision par fichier,
une page maximum. Un ADR accepté ne se réécrit pas : s'il est remis en cause, on en écrit
un nouveau qui le remplace (« Statut : remplacé par ADR-0007 »).
Ce fichier 0000 n'est pas compté par le pré-contrôle (make check-m10).
-->

- **Statut :** [À compléter : proposé | accepté | remplacé par ADR-NNNN | abandonné]
- **Date :** [À compléter : AAAA-MM-JJ]
- **Auteur(s) :** [À compléter : @pseudo-github]
- **Relu par :** [À compléter : @pseudo-github du partenaire]
- **Périmètre :** [À compléter : socle (Lab N) | extension ext/<nom>]
- **Liens :** [À compléter : PR #N, issue #N, ADR liés]

## Contexte

[À compléter : le problème à résoudre et les contraintes qui pèsent sur la décision, en 3 à 8
lignes. Contraintes typiques : ressources du poste (RAM, pas de GPU), délai, compétences du
binôme, exigences du cas d'usage (coût d'un faux négatif, explicabilité, latence), outils
imposés par le socle.]

## Options envisagées

| Option | Avantages | Inconvénients |
|---|---|---|
| [À compléter : option A] | | |
| [À compléter : option B] | | |
| [À compléter : ne rien faire / statu quo] | | |

## Décision

[À compléter : l'option retenue, formulée de façon affirmative (« Nous utilisons… »), et la
raison principale. Si un chiffre a guidé le choix (latence mesurée, taille d'image, ROC AUC,
coût métier), le donner avec la façon dont il a été obtenu (run MLflow, rapport, commande).]

## Conséquences

- **Positives :** [À compléter]
- **Négatives / dette acceptée :** [À compléter : ce qu'on s'interdit ou ce qu'il faudra
  reprendre, et à quel signal on rouvrira la décision]
- **Vérification :** [À compléter : comment on sait que la décision tient — test, check,
  alerte, métrique suivie]
```

### Journal de bord

Une entrée par séance, la plus récente en bas, titre au format exact
`## S<n> — AAAA-MM-JJ — <sujet>` (le pré-contrôle compte les entrées datées) :

```markdown
## S5 — 2026-10-13 — Lab 3 : validation

- **Pilote / copilote :** @bob / @alice
- **Fait :** suite GX sur les 20 variables, gate branchée dans le pipeline (#18).
- **Bloqué / appris :** le drift Evidently se déclenchait sur `age` à chaque run (graine du
  rééchantillonnage), corrigé ; ADR 0002 ouvert sur le seuil.
- **Prochaine étape :** Alice pilote le Lab 4 ; relire la PR #18.
```

### Rapport technique

**10 pages maximum** hors page de garde et annexes, en PDF (`docs/rapport.pdf`). Le jury le lit
**avant** la soutenance : il y cherche vos choix et vos chiffres, pas le récit des labs. Plan
détaillé dans `docs/rapport-technique.md` :

| Section | Pages |
|---|---|
| 1. Résumé exécutif | ½ |
| 2. Cas d'usage et données | 1 |
| 3. Architecture du socle | 1 ½ |
| 4. Modèle et validation | 1 |
| 5. Mise en service et SLO | 1 |
| 6. Exploitation : CI/CD, monitoring, incidents | 1 |
| 7. Gouvernance (équité, explicabilité, sécurité, AI Act) | 1 |
| 8. Extension du membre 1 | 1 |
| 9. Extension du membre 2 | 1 |
| 10. Compromis, difficultés, améliorations | 1 |

La section 10 est souvent la plus appréciée : les choix faits « faute de mieux », les problèmes
rencontrés et la façon dont vous les avez contournés.

## Conseils

### Ce qui démarque un excellent projet

1. La démo marche du premier coup sur un poste qui n'a jamais vu votre code.
2. Chaque choix technique est justifié (ADR), y compris les compromis.
3. Les tests et les gates permettent de toucher au code sans peur.
4. Le tableau de bord Grafana est lisible : un non-spécialiste comprend en 10 secondes si le
   système va bien.
5. La model card et la dataset card sont franches sur les limites : pas de promesse, pas de
   cache-misère.
6. Le README commence par un démarrage rapide en cinq commandes.
7. L'historique Git raconte une histoire : des PR petites et relues, des messages clairs, deux
   contributeurs.

### Pièges à éviter

> [!CAUTION]
> **À éviter absolument**
>
> - **Le projet piloté par notebook** : le code final vit dans `src/` et `pipelines/`, pas dans
>   `notebooks/`.
> - **Les valeurs en dur** : un nom de colonne dans le code, et votre socle ne marche plus que
>   pour un dataset. Tout passe par `dataset.yaml`.
> - **Des métriques sans contexte** : « accuracy 0,89 » ne veut rien dire sans baseline, coût
>   métier, sous-groupes.
> - **« Aucun biais détecté »** dans la model card : c'est forcément faux, surtout sur
>   German Credit.
> - **Des secrets dans Git** : `.env`, `.dvc/config.local`, jetons. Le pré-contrôle les
>   cherche ; un secret poussé doit être changé, pas seulement supprimé.
> - **Le binôme en série** : l'un fait les labs pairs, l'autre les impairs. Le défi est
>   individuel et porte sur tout le socle.
> - **La démo jamais répétée** : répétez au moins trois fois, dont une sur un poste neuf.
> - **L'extension fusionnée la veille** : sans relecture, sans tests, elle casse souvent le
>   socle (et les checks).

> [!TIP]
> **Le bon réflexe**
> Avant le tag `final`, relancez vous-même `git clone` + `make up` + `uv sync` + `dvc repro`
> (puis `dvc push`) et le pipeline sur un poste (ou un compte utilisateur) vierge, sans aucun
> artefact local. Les projets qui passent ce test réussissent la démo ; ceux qui ne le passent
> pas la ratent.

## FAQ

**Peut-on travailler seul ou à trois ?**
Le binôme est la règle. Un étudiant seul (effectif impair) est possible avec l'accord de
l'enseignant : même socle, une seule extension (`EXT_MIN=1` pour le pré-contrôle). Pas de
trinôme.

**Mon partenaire abandonne en cours de semestre. Que se passe-t-il ?**
Prévenez l'enseignant tout de suite. Vous gardez le repo et poursuivez seul (une extension) ;
le journal et l'historique Git documentent qui a fait quoi.

**Les deux membres peuvent-ils faire la même extension ?**
Non. Deux extensions différentes, et au plus 3 binômes par extension et par groupe.

**Puis-je changer d'extension après l'avoir déclarée ?**
Oui jusqu'à la fin de S8, en mettant à jour votre issue (et sous réserve du quota). Au-delà,
seulement avec l'accord de l'enseignant.

**Notre dataset libre nous pose trop de problèmes. Peut-on revenir au credit scoring ?**
Oui, à tout moment, sans pénalité. Restaurez `dataset.yaml` et `src/download.py` depuis
`upstream/main`, relancez `dvc repro`, notez-le dans le journal et dans un ADR.

**Nous avons pris du retard sur un lab. Comment rattraper ?**
Après chaque date de rendu, la correction du lab X est publiée sur le repo du cours sous deux
formes : la branche `solution/mX` (état du repo en fin de lab X, labs précédents compris) et le
tag `start/m(X+1)` (le même état, point de départ du lab suivant). Récupérez-la de façon
ciblée, puis adaptez-la :

```bash
git fetch upstream                                  # ou le remote indiqué par l'enseignant
git switch -c lab/m4-rattrapage
git checkout upstream/solution/m4 -- packaging/     # seulement les fichiers du lab
git commit -m "lab/m4 : reprise de la correction m4"
```

Ouvrez une PR comme d'habitude et notez la reprise dans le journal. Rejouez ensuite le lab sur
votre cluster avec l'encadré « Second membre du binôme » de son énoncé. Cas du Lab 1 : la
correction ne contient ni `.dvc/config` (propre à chaque binôme) ni `dvc.lock` ; refaites les
étapes 2.1 (`dvc init`) et 2.3 (remote) du Lab 1, puis `dvc repro` et `git add dvc.lock`. Les labs
(30 %) restent notés à leur date de rendu ; le socle du mini-projet est évalué au tag `final`.

**Le Lab 9 (LLMOps) fait-il partie du socle ?**
Non. Il n'est pas vérifié par le pré-contrôle et ne compte pas dans le bloc « socle ». Il sert
de base à l'extension `rag-projet`.

**Mes métriques de performance sont basses. C'est grave ?**
Non. L'évaluation porte sur le système MLOps, pas sur l'accuracy. Un modèle à ROC AUC 0,75 avec
un socle complet et un seuil justifié par le coût métier vaut bien plus qu'un modèle à 0,85
sans infrastructure. Montrez que vous savez *pourquoi* il plafonne.

**Peut-on utiliser un cloud public au lieu de kind ?**
Le socle doit tourner sur kind (c'est ce que vérifient les checks, et ce qu'utilise le plan B).
Une extension peut utiliser un service externe gratuit si elle reste reproductible et si une
alternative locale est documentée.

**Faut-il un GPU ?**
Non, aucune extension n'en exige. L'extension `rag-projet` tourne sur CPU avec un petit modèle
local (Lab 9) ; mesurez sa consommation mémoire.

**Le pré-contrôle est tout vert. Avons-nous la note maximale ?**
Non : il vérifie que les livrables **existent et fonctionnent**. La qualité (choix,
justifications, maîtrise à l'oral, défi) est évaluée par le jury. À l'inverse, un pré-contrôle
rouge au tag `final` coûte des points certains.

**Qui voit nos issues de déclaration ?**
Elles sont sur le repo public du cours : n'y mettez aucune donnée personnelle au-delà des
pseudos GitHub et du groupe.

## Vérification automatique

```bash
make check-m10                                      # jalon « final » (tout)
make check-m10 JALON=j1                             # ce qui est attendu au jalon J1
./labs/m10-capstone/check.sh --sans-cluster         # repo seul : docs, Git, tags
./labs/m10-capstone/check.sh --gh                   # + relectures des PR ext/* (gh CLI)
```

Ce **pré-contrôle de rendu** ne note pas : il vérifie que les livrables existent et
fonctionnent, et sert à l'enseignant (sur votre poste, cluster démarré et `make pf` actif, ou sur
un simple clone avec `--sans-cluster`) comme à vous avant chaque tag. Il ne s'arrête pas au
premier échec et ne modifie rien. Il vérifie :

| Bloc | Vérifications |
|---|---|
| Socle | `make check-m0` … `make check-m8` (selon le jalon), chacun avec son nombre d'items verts ; journaux complets dans `/tmp/mlops-precontrole/` |
| Contrat de données | `dataset.yaml` valide (`load_config`), licence, source et attribut sensible déclarés ; données brutes conformes (colonnes, 1 000 à 100 000 lignes, moins de 50 Mo) ; avertissement si le nom de la cible est écrit en dur dans le code |
| Dépôt et reproductibilité | `dvc.yaml`, `dvc.lock`, remote DVC par défaut ; aucun secret ni donnée brute dans Git ; sections du README et commandes `make up` / `dvc repro` ; au moins deux auteurs dans l'historique |
| Livrables écrits | journal (entrées datées), ADR complets (hors `0000`), dataset card et model card sans `[À compléter]`, et au rendu final rapport PDF, slides, lien de la vidéo |
| Jalons | tags `j0`, `j1`, `j2`, `final` présents et dans l'ordre ; avec `SOUTENANCE="AAAA-MM-JJ HH:MM"`, tag `final` posé au moins 48 h avant |
| Extensions | branches `ext/<nom>` retrouvées dans l'historique de `main` (fusion ou squash dont le titre commence par `ext/<nom>`), auteurs, présence de tests et d'ADR ; au moins deux extensions ; avec `--gh`, PR approuvées par un autre compte que l'auteur |

Variables utiles : `JALON` (`j0`, `j1`, `j2`, `final`), `JOURNAL_MIN`, `EXT_MIN`,
`AUTEURS_MIN`, `CHECK_TIMEOUT`, `SOUTENANCE`, `LOG_DIR`.

> **Sortie attendue :** pour un rendu final complet, un récapitulatif entièrement vert :

```text
════════ Récapitulatif — jalon « final » ════════
✅   9/9  Socle — make check-m* (labs 0, 1, 2, 3, 4, 5, 6, 7, 8)
✅   2/2  Contrat de données — dataset.yaml
✅   4/4  Dépôt et reproductibilité
✅   7/7  Livrables écrits
✅   4/4  Jalons — tags Git (j0, j1, j2, final)
✅   1/1  Extensions — branches ext/* fusionnées dans l'historique

🎉 27/27 vérifications OK, 0 avertissement(s) — rendu « final » complet.
```
