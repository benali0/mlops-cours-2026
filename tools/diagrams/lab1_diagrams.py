"""Schémas du Lab 1 (PNG) : DVC, MLflow, pipeline DVC, Feast, flux du lab.

Régénérer (depuis la racine du repo) :
    uv run --no-project --with matplotlib python tools/diagrams/lab1_diagrams.py
Sortie : labs/m1-versioning/img/*.png
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lab0_diagrams import (  # noqa: E402
    LIGHT,
    MUTED,
    NAVY,
    ORANGE,
    PALE_NAVY,
    PALE_ORANGE,
    PALE_TEAL,
    TEAL,
    WHITE,
    arrow,
    box,
    canvas,
    plt,
    title,
)

OUT = Path(__file__).resolve().parents[2] / "labs" / "m1-versioning" / "img"


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=150, facecolor=WHITE)
    plt.close(fig)


# 1. DVC : Git garde l'empreinte, S3 garde le contenu ----------------------------------------
def dvc():
    fig, ax = canvas(16, 8)
    title(
        ax,
        "DVC : Git garde l'étiquette, S3 garde le contenu",
        "Comme un vestiaire : Git garde le ticket (l'empreinte), le stockage S3 garde le manteau "
        "(le fichier).",
    )
    box(
        ax,
        4,
        44,
        40,
        18,
        "data/raw/dataset.csv",
        "le vrai fichier\n(ignoré par Git)",
        fill=LIGHT,
        edge=NAVY,
    )
    arrow(ax, 44, 53, 62, 53, "md5", color=NAVY)
    box(ax, 62, 44, 40, 18, "24b8e38b…", "empreinte unique\ndu contenu", fill=PALE_NAVY, edge=NAVY)
    box(
        ax,
        4,
        6,
        64,
        24,
        "Git → GitHub",
        "dvc.yaml, dvc.lock : quelques lignes de texte\n"
        "qui contiennent l'empreinte\n(git add / commit / push)",
        fill=PALE_TEAL,
        edge=TEAL,
    )
    box(
        ax,
        88,
        6,
        68,
        24,
        "Remote S3 (SeaweedFS)",
        "s3://dvc-store/scoring/files/md5/24/b8e38b…\n"
        "le contenu, rangé par empreinte\n(dvc push / dvc pull)",
        fill=PALE_ORANGE,
        edge=ORANGE,
    )
    arrow(ax, 76, 44, 40, 30, "dans dvc.lock", color=TEAL, loff=(-8, 0))
    arrow(ax, 88, 44, 118, 30, "dvc push", color=ORANGE, loff=(8, 0))
    box(
        ax,
        112,
        44,
        44,
        18,
        "Règle d'or",
        "même contenu = même empreinte\nun octet change =\nnouvelle version",
        fill=WHITE,
        edge=MUTED,
        ssize=10,
    )
    save(fig, "01-dvc-empreinte.png")


# 2. MLflow : expérience, runs, registry, alias -----------------------------------------------
def mlflow():
    fig, ax = canvas(16, 8.5)
    title(
        ax,
        "MLflow : des runs au modèle servi",
        "Chaque entraînement est un run ; seuls les meilleurs entrent dans le registry ; "
        "les alias désignent la version à servir.",
    )
    box(
        ax,
        3,
        6,
        56,
        62,
        "Expérience « scoring »",
        "",
        fill=LIGHT,
        edge=MUTED,
        title_top=True,
        tsize=12,
    )
    runs = [
        ("run : logistic_regression C=0.1", "roc_auc 0.81 · coût 113"),
        ("run : random_forest n=200", "roc_auc 0.80 · coût 102"),
        ("run : dummy (référence naïve)", "roc_auc 0.50 · coût 140"),
    ]
    for k, (name, sub) in enumerate(runs):
        box(ax, 6, 46 - k * 15, 50, 12, name, sub, fill=WHITE, edge=TEAL, tsize=10.5, ssize=9.5)
    ax.text(31, 9, "+ ~20 autres runs (grid search)", ha="center", fontsize=10, color=MUTED)
    arrow(ax, 56, 52, 78, 52, "promote.py", color=NAVY, loff=(0, 1.2))
    box(
        ax,
        78,
        6,
        50,
        62,
        "Registry « scoring-model »",
        "",
        fill=PALE_NAVY,
        edge=NAVY,
        title_top=True,
        tsize=12,
    )
    vers = [
        ("version 1", "@champion", TEAL),
        ("version 2", "@challenger", ORANGE),
        ("version 3", "", MUTED),
    ]
    for k, (v, alias, col) in enumerate(vers):
        box(ax, 82, 46 - k * 15, 22, 12, v, fill=WHITE, edge=NAVY, tsize=10.5)
        if alias:
            box(ax, 106, 47 - k * 15, 19, 10, alias, fill=col, edge=col, tcolor=WHITE, tsize=10)
    box(
        ax,
        134,
        34,
        24,
        22,
        "API (Lab 4)",
        "charge\nmodels:/scoring-model\n@champion",
        fill=WHITE,
        edge=TEAL,
        ssize=9,
    )
    arrow(ax, 125, 52, 134, 47, "", color=TEAL)
    ax.text(
        103,
        1.5,
        "Seuil de qualité : @champion seulement si roc_auc ≥ 0,70 (dataset.yaml)",
        ha="center",
        fontsize=10.5,
        color=NAVY,
        fontweight="bold",
    )
    save(fig, "02-mlflow-registry.png")


# 3. Le pipeline DVC ----------------------------------------------------------------------------
def pipeline():
    fig, ax = canvas(16, 7)
    title(
        ax,
        "Le pipeline DVC : dvc repro ne relance que ce qui a changé",
        "Chaque stage déclare ce qu'elle lit (deps, params) et ce qu'elle produit (outs, metrics).",
    )
    stages = [
        ("download", "src/download.py\n→ data/raw/"),
        ("prepare", "params: prepare\n→ data/processed/"),
        ("train", "params: train\n→ models/ + run MLflow"),
        ("evaluate", "→ reports/\nmetrics.json"),
    ]
    for k, (name, sub) in enumerate(stages):
        x = 4 + k * 39
        box(
            ax,
            x,
            26,
            32,
            20,
            name,
            sub,
            fill=PALE_TEAL if k < 3 else PALE_ORANGE,
            edge=TEAL if k < 3 else ORANGE,
            ssize=10,
        )
        if k:
            arrow(ax, x - 7, 36, x, 36, "", color=NAVY)
    box(
        ax,
        4,
        4,
        72,
        14,
        "params.yaml modifié (train.class_weight)",
        "→ train et evaluate relancés ;\ndownload et prepare : « skipping »",
        fill=WHITE,
        edge=MUTED,
        ssize=10,
    )
    box(
        ax,
        84,
        4,
        72,
        14,
        "Rien n'a changé",
        "→ tout est « skipping » ; dvc.lock garde\nl'empreinte de chaque entrée et sortie",
        fill=WHITE,
        edge=MUTED,
        ssize=10,
    )
    save(fig, "03-pipeline-dvc.png")


# 4. Feast -------------------------------------------------------------------------------------
def feast():
    fig, ax = canvas(16, 7.5)
    title(
        ax,
        "Feast : une seule définition des features, deux accès",
        "Le même calcul sert à l'entraînement (hors ligne) et aux prédictions (en ligne) : "
        "pas de training/serving skew.",
    )
    box(
        ax,
        56,
        30,
        48,
        22,
        "features/definitions.py",
        "entité, vue de features,\nservice scoring_v1\n(feast apply)",
        fill=PALE_NAVY,
        edge=NAVY,
        ssize=10,
    )
    box(
        ax,
        4,
        4,
        58,
        22,
        "Hors ligne : entraînement",
        "get_historical_features()\nun DataFrame complet, à la bonne date",
        fill=PALE_TEAL,
        edge=TEAL,
        ssize=10,
    )
    box(
        ax,
        98,
        4,
        58,
        22,
        "En ligne : prédiction",
        "feast materialize, puis\nget_online_features() : une ligne, vite",
        fill=PALE_ORANGE,
        edge=ORANGE,
        ssize=10,
    )
    arrow(ax, 62, 30, 40, 26, "", color=TEAL)
    arrow(ax, 98, 30, 120, 26, "", color=ORANGE)
    box(
        ax,
        4,
        34,
        46,
        16,
        "data/processed/",
        "les features calculées\npar prepare.py",
        fill=LIGHT,
        edge=MUTED,
        ssize=10,
    )
    arrow(ax, 50, 42, 56, 42, "", color=MUTED)
    save(fig, "04-feast.png")


# 5. Le circuit du lab ---------------------------------------------------------------------------
def flux_lab1():
    fig, ax = canvas(16, 7)
    title(
        ax,
        "Le Lab 1 en un coup d'œil",
        "Dix étapes, un seul fil : le credit scoring, du fichier brut au modèle promu "
        "et reproductible.",
    )
    steps = [
        ("1-2", "Données", "dataset.yaml,\nDVC + S3"),
        ("3-6", "Expériences", "train.py,\n20+ runs MLflow"),
        ("7", "Registry", "@champion\n@challenger"),
        ("8", "Pipeline", "dvc.yaml,\ndvc repro"),
        ("9", "Features", "Feast"),
        ("10", "Preuve", "clone + dvc pull\n+ dvc repro"),
    ]
    for k, (num, name, sub) in enumerate(steps):
        x = 3 + k * 26
        box(
            ax,
            x,
            18,
            22,
            28,
            f"{name}",
            sub,
            fill=PALE_TEAL if k % 2 == 0 else PALE_NAVY,
            edge=TEAL if k % 2 == 0 else NAVY,
            ssize=9.5,
            tsize=12,
        )
        ax.text(x + 11, 49, f"étape {num}", ha="center", fontsize=10, color=MUTED)
        if k:
            arrow(ax, x - 4, 32, x, 32, "", color=NAVY, lw=1.6)
    ax.text(
        80,
        8,
        "Fin : pull request lab/m1-versioning relue par le binôme, make check-m1 vert",
        ha="center",
        fontsize=11.5,
        color=ORANGE,
        fontweight="bold",
    )
    save(fig, "00-lab1-flux.png")


if __name__ == "__main__":
    for f in (flux_lab1, dvc, mlflow, pipeline, feast):
        f()
    print("Schémas écrits dans", OUT)
