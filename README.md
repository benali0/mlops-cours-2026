# Cours MLOps — repo du cours (2026)

Repo de travail du cours **Machine Learning Operations** (18 h : 9 séances de 2 h, cycle ingénieur
informatique).
Vous le copiez au Lab 0 et vous y travaillez **jusqu'à la soutenance** : chaque lab y ajoute
une brique, et le résultat final est votre mini-projet.

> [!NOTE]
> **En binôme**, deux organisations au choix : un repo commun (un membre le crée à partir de
> celui-ci, bouton **Use this template** ou fork, l'autre le clone) ou deux repos coordonnés
> (chacun crée le sien). Ajoutez votre partenaire et l'enseignant (`firaskhl`) comme
> collaborateurs.
> Détails : Lab 0, étape 3.

## Démarrage

1. **Créer la VM du cours** (Lab 0, étape 1) : VirtualBox 7.2 + Vagrant 2.4.9 sur le poste, puis
   dans PowerShell, depuis le dossier [`infra/vagrant/`](infra/vagrant/README.md) de ce repo
   téléchargé (**Code** > **Download ZIP**) : `vagrant up` puis `vagrant ssh`. Docker, kind,
   kubectl, helm, k9s et uv y sont déjà installés (Linux / macOS sans VM : annexe A du Lab 0).
2. **Dans la VM**, avec votre propre copie de ce repo (Lab 0, étape 3) :

```bash
git clone git@github.com:VOTRE_USER/mlops-cours-2026.git && cd mlops-cours-2026
uv sync          # environnement Python du cours (Python 3.12)
make prefetch    # avant la séance : images du socle (~3 Go)
make up          # cluster kind + registry + stockage S3 (SeaweedFS) + MLflow
make pf          # accès depuis le poste : S3 :8333, filer :8888, MLflow :5000
```

Puis suivez le [Lab 0](labs/m0-setup/README.md) jusqu'au bout : `make check-m0` n'est vert
qu'une fois toutes ses étapes faites (bucket de test, smoke tests, premier commit).

**16 Go de RAM requis** à partir du Lab 2 (8 Go suffisent pour les Labs 0 et 1) : sinon,
prévenez l'enseignant dès la première séance (poste de l'école, VM, ou binôme équipé).

## Contenu

| Dossier | Rôle |
|---|---|
| `labs/` | Énoncés des 10 labs (0 à 9) et du mini-projet, scripts `check.sh` ([sommaire](labs/README.md)) |
| `infra/` | Installation des briques (`versions.env` = versions de référence) |
| `dataset.yaml`, `src/` | Contrat de données et code socle (credit scoring par défaut) |
| `docs/` | Gabarits du mini-projet : journal, ADR, dataset card, rapport, soutenance, syllabus |
| `rag/` | Projet Python isolé du Lab 9 (LLMOps) |
| `tools/` | Générateur PDF des énoncés, vérificateur énoncé ↔ fichiers |

Le reste (pipelines, API, manifests, monitoring…) est créé par vous, lab après lab.

## Le mini-projet en bref

Socle vérifié par `make check-m0` … `make check-m8` + une **extension personnelle** par étudiant
+ soutenance de 25 minutes avec **défi en direct** (séance 9). Jalons : J0 (fin S3), extensions
déclarées (fin S5), J1 (fin S7), J2 (fin S8), tag `final` 48 h avant la soutenance. Tout est dans
[`labs/m10-capstone/README.md`](labs/m10-capstone/README.md).

> [!TIP]
> Au jalon J1, remplacez ce README par celui de votre projet (le sommaire du cours reste dans
> `labs/README.md`).

## Signaler une erreur

Ouvrez une *issue* sur le repo du cours (`firaskhl/mlops-cours-2026`) ; les corrections par
pull request sont bienvenues, en particulier pour le troubleshooting et les versions d'outils.
