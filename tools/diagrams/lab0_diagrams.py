"""Schémas du Lab 0 (PNG) : vue d'ensemble, Docker, VM, Kubernetes, IaC, Git, flux du lab.

Régénérer (depuis la racine du repo) :
    uv run --no-project --with matplotlib python tools/diagrams/lab0_diagrams.py
Sortie : labs/m0-setup/img/*.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "labs" / "m0-setup" / "img"
NAVY, TEAL, ORANGE, INK, MUTED = "#0B1E3F", "#14B8A6", "#F59E0B", "#0F172A", "#64748B"
LIGHT, PALE_TEAL, PALE_ORANGE, PALE_NAVY, WHITE = (
    "#F1F5F9",
    "#E6F7F5",
    "#FEF3C7",
    "#E8EEF5",
    "#FFFFFF",
)
plt.rcParams["font.family"] = "DejaVu Sans"


def canvas(w=16, h=9):
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    ax.set_xlim(0, w * 10)
    ax.set_ylim(0, h * 10)
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    return fig, ax


def box(
    ax,
    x,
    y,
    w,
    h,
    title="",
    sub="",
    fill=WHITE,
    edge=NAVY,
    tcolor=INK,
    tsize=13,
    ssize=10.5,
    lw=1.6,
    title_top=False,
    radius=1.5,
    dashed=False,
):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle=f"round,pad=0,rounding_size={radius}",
            facecolor=fill,
            edgecolor=edge,
            linewidth=lw,
            linestyle="--" if dashed else "-",
        )
    )
    if title_top:
        ax.text(
            x + 1.5,
            y + h - 1.6,
            title,
            ha="left",
            va="top",
            fontsize=tsize,
            color=tcolor,
            fontweight="bold",
        )
        if sub:
            ax.text(x + 1.5, y + h - 5.2, sub, ha="left", va="top", fontsize=ssize, color=MUTED)
    else:
        n = sub.count("\n") + 1 if sub else 0
        dy = 1.6 + 1.1 * (n - 1) if sub else 0
        ax.text(
            x + w / 2,
            y + h / 2 + dy,
            title,
            ha="center",
            va="center",
            fontsize=tsize,
            color=tcolor,
            fontweight="bold",
        )
        if sub:
            ax.text(
                x + w / 2,
                y + h / 2 + dy - 3.0,
                sub,
                ha="center",
                va="top",
                fontsize=ssize,
                color=MUTED,
                linespacing=1.3,
            )


def arrow(
    ax, x1, y1, x2, y2, label="", color=NAVY, lw=2, rad=0.0, lsize=10.5, loff=(0, 1.6), both=False
):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="<|-|>" if both else "-|>",
            mutation_scale=16,
            color=color,
            linewidth=lw,
            connectionstyle=f"arc3,rad={rad}",
        )
    )
    if label:
        ax.text(
            (x1 + x2) / 2 + loff[0],
            (y1 + y2) / 2 + loff[1],
            label,
            ha="center",
            va="bottom",
            fontsize=lsize,
            color=color,
            fontweight="bold",
        )


def title(ax, text, sub=""):
    ax.text(
        3,
        ax.get_ylim()[1] - 3,
        text,
        ha="left",
        va="top",
        fontsize=19,
        color=NAVY,
        fontweight="bold",
    )
    if sub:
        ax.text(3, ax.get_ylim()[1] - 8, sub, ha="left", va="top", fontsize=12, color=MUTED)


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=150, facecolor=WHITE)
    plt.close(fig)


# 1. Vue d'ensemble ------------------------------------------------------------------
def vue_ensemble():
    fig, ax = canvas(16, 10)
    title(
        ax,
        "Votre poste pendant le cours",
        "Sous Windows : tout tourne dans une VM Linux. Sous Linux / macOS : "
        "le cadre « VM » disparaît, le reste est identique.",
    )
    box(
        ax,
        2,
        3,
        156,
        80,
        "Votre PC (Windows)",
        "VirtualBox + Vagrant installés",
        fill=LIGHT,
        edge=MUTED,
        title_top=True,
        tsize=14,
    )
    box(
        ax,
        4,
        46,
        28,
        22,
        "Navigateur",
        "localhost:5000 → MLflow\nlocalhost:8888 → fichiers S3",
        fill=WHITE,
        edge=MUTED,
        ssize=10,
    )
    box(
        ax,
        4,
        14,
        28,
        18,
        "PowerShell",
        "vagrant up\nvagrant ssh",
        fill=WHITE,
        edge=MUTED,
        ssize=10.5,
    )
    box(
        ax,
        42,
        6,
        114,
        70,
        "VM « mlops-vm » — Ubuntu 24.04",
        "créée par Vagrant, configurée par Ansible ; votre repo : ~/mlops-cours-2026",
        fill=PALE_NAVY,
        edge=NAVY,
        title_top=True,
        tsize=14,
    )
    box(
        ax,
        45,
        9,
        108,
        55,
        "Docker",
        "fait tourner des conteneurs",
        fill=WHITE,
        edge=TEAL,
        title_top=True,
        tcolor=TEAL,
        tsize=13,
    )
    box(
        ax,
        48,
        12,
        80,
        42,
        "Cluster Kubernetes « mlops-lab » (kind)",
        "3 nœuds = 3 conteneurs Docker",
        fill=PALE_TEAL,
        edge=TEAL,
        title_top=True,
        tsize=12,
    )
    box(
        ax,
        50,
        15,
        36,
        25,
        "namespace storage",
        "",
        fill=WHITE,
        edge=MUTED,
        title_top=True,
        tsize=10.5,
        dashed=True,
    )
    box(
        ax,
        52,
        17,
        32,
        13,
        "SeaweedFS",
        "stockage S3 (buckets)",
        fill=PALE_ORANGE,
        edge=ORANGE,
        ssize=9.5,
    )
    box(
        ax,
        90,
        15,
        36,
        25,
        "namespace mlflow",
        "",
        fill=WHITE,
        edge=MUTED,
        title_top=True,
        tsize=10.5,
        dashed=True,
    )
    box(
        ax,
        92,
        17,
        32,
        13,
        "MLflow",
        "suivi des expériences\n(artefacts rangés dans S3)",
        fill=PALE_ORANGE,
        edge=ORANGE,
        ssize=9.5,
    )
    arrow(ax, 92, 23.5, 84, 23.5, "", color=ORANGE)
    box(ax, 132, 36, 18, 16, "registry", "localhost:5001\n(images)", fill=WHITE, edge=TEAL, ssize=9)
    box(ax, 132, 13, 18, 18, "Python", "uv · DVC\nclient MLflow", fill=WHITE, edge=NAVY, ssize=9)
    arrow(ax, 32, 57, 48, 44, "", color=TEAL)
    ax.text(
        4, 43, "make pf + relais (ports 5000, 8888)", fontsize=10, color=TEAL, fontweight="bold"
    )
    arrow(ax, 32, 23, 42, 23, "", color=NAVY)
    ax.text(
        4,
        11,
        "vagrant ssh : ouvre un terminal dans la VM",
        fontsize=10,
        color=NAVY,
        fontweight="bold",
    )
    save(fig, "00-vue-ensemble.png")


# 2. Docker --------------------------------------------------------------------------
def docker():
    fig, ax = canvas(16, 7.5)
    title(
        ax,
        "Docker : image et conteneur",
        "Une image est une recette figée ; un conteneur est un plat préparé "
        "à partir de cette recette. On peut en préparer plusieurs.",
    )
    box(
        ax,
        4,
        22,
        28,
        28,
        "Dockerfile",
        "fichier texte :\nFROM python:3.12\nCOPY app.py .\nCMD python app.py",
        fill=WHITE,
        edge=MUTED,
        ssize=10,
    )
    box(
        ax,
        54,
        22,
        30,
        28,
        "Image",
        "paquet figé : système\n+ librairies + code\n(ex. mlflow:v3.16.1)",
        fill=PALE_TEAL,
        edge=TEAL,
        ssize=10,
    )
    for i, y in enumerate((44, 30, 16)):
        box(
            ax,
            110,
            y,
            34,
            11,
            f"Conteneur {i + 1}",
            "processus isolé en marche",
            fill=PALE_ORANGE,
            edge=ORANGE,
            ssize=9.5,
            tsize=11.5,
        )
        arrow(ax, 84, 36, 110, y + 5.5, "", color=ORANGE, rad=0.0)
    ax.text(92, 46, "docker run", fontsize=10.5, color=ORANGE, fontweight="bold", rotation=0)
    arrow(ax, 32, 36, 54, 36, "docker build", color=NAVY)
    box(
        ax,
        50,
        2,
        38,
        12,
        "Registry",
        "Docker Hub, ghcr.io, localhost:5001",
        fill=LIGHT,
        edge=MUTED,
        ssize=9.5,
        tsize=11.5,
    )
    arrow(ax, 69, 14, 69, 22, "", color=MUTED, both=True)
    ax.text(72, 17, "docker pull / push", fontsize=10, color=MUTED, fontweight="bold", va="center")
    save(fig, "01-docker.png")


# 3. VM vs conteneur -------------------------------------------------------------------
def vm_vs_conteneur():
    fig, ax = canvas(16, 8)
    title(
        ax,
        "Machine virtuelle et conteneur : deux niveaux d'isolation",
        "La VM émule un ordinateur complet (avec son propre système) ; "
        "le conteneur partage le noyau Linux.",
    )

    def stack(x, label, layers):
        ax.text(x + 32, 63, label, ha="center", fontsize=14, color=NAVY, fontweight="bold")
        y = 6
        for name, fill, edge, h in layers:
            box(ax, x, y, 64, h, name, fill=fill, edge=edge, tsize=11)
            y += h + 1.2

    stack(
        6,
        "Machine virtuelle (VirtualBox)",
        [
            ("Matériel du PC", LIGHT, MUTED, 7),
            ("Windows", PALE_NAVY, NAVY, 7),
            ("VirtualBox (hyperviseur)", WHITE, NAVY, 7),
            ("Ubuntu 24.04 complet (noyau + système)", PALE_TEAL, TEAL, 9),
            ("Vos outils et applications", PALE_ORANGE, ORANGE, 9),
        ],
    )
    stack(
        88,
        "Conteneurs (Docker)",
        [
            ("Matériel", LIGHT, MUTED, 7),
            ("Linux (noyau partagé)", PALE_NAVY, NAVY, 7),
            ("Docker", WHITE, TEAL, 7),
        ],
    )
    for i, name in enumerate(("SeaweedFS", "MLflow", "nœud kind")):
        box(
            ax,
            88 + i * 21.6,
            30.6,
            20,
            18,
            name,
            "librairies\n+ appli",
            fill=PALE_ORANGE,
            edge=ORANGE,
            tsize=10.5,
            ssize=9,
        )
    ax.text(
        80,
        2.2,
        "Dans le cours : la VM (gauche) héberge Docker, qui héberge les conteneurs (droite).",
        ha="center",
        fontsize=11,
        color=MUTED,
        style="italic",
    )
    save(fig, "02-vm-vs-conteneur.png")


# 4. Kubernetes ------------------------------------------------------------------------
def kubernetes():
    fig, ax = canvas(16, 9)
    title(
        ax,
        "Kubernetes en une image",
        "Vous décrivez l'état voulu (YAML) ; Kubernetes le crée et le maintient. "
        "kind fait tourner chaque nœud dans un conteneur Docker.",
    )
    box(
        ax,
        3,
        52,
        24,
        16,
        "Vous",
        "kubectl apply -f\nstorage.yaml",
        fill=LIGHT,
        edge=MUTED,
        ssize=10,
    )
    box(
        ax,
        3,
        24,
        24,
        16,
        "k9s",
        "tableau de bord\ndans le terminal",
        fill=LIGHT,
        edge=MUTED,
        ssize=10,
    )
    box(
        ax,
        34,
        4,
        122,
        72,
        "Cluster « mlops-lab »",
        "",
        fill=PALE_NAVY,
        edge=NAVY,
        title_top=True,
        tsize=14,
    )
    box(
        ax,
        38,
        46,
        30,
        22,
        "control-plane",
        "le « cerveau » : API,\nplanificateur",
        fill=WHITE,
        edge=NAVY,
        ssize=9.5,
        tsize=11.5,
    )
    arrow(ax, 27, 60, 38, 58, "", color=NAVY)
    arrow(ax, 27, 32, 38, 50, "", color=MUTED, rad=-0.2)
    for i, nx in enumerate((74, 116)):
        box(
            ax,
            nx,
            26,
            38,
            42,
            f"nœud worker{'' if i == 0 else '2'}",
            "conteneur Docker (kind)",
            fill=WHITE,
            edge=TEAL,
            title_top=True,
            tsize=11.5,
            tcolor=TEAL,
            ssize=9,
        )
    box(
        ax,
        77,
        32,
        32,
        18,
        "Pod seaweedfs",
        "1 conteneur",
        fill=PALE_ORANGE,
        edge=ORANGE,
        ssize=9.5,
        tsize=11,
    )
    box(
        ax,
        119,
        32,
        32,
        18,
        "Pod mlflow",
        "1 conteneur",
        fill=PALE_ORANGE,
        edge=ORANGE,
        ssize=9.5,
        tsize=11,
    )
    box(
        ax,
        74,
        7,
        38,
        13,
        "Service « s3 »",
        "s3.storage:8333",
        fill=PALE_TEAL,
        edge=TEAL,
        ssize=9.5,
        tsize=11,
    )
    box(
        ax,
        116,
        7,
        38,
        13,
        "Service « mlflow »",
        "mlflow.mlflow:5000",
        fill=PALE_TEAL,
        edge=TEAL,
        ssize=9.5,
        tsize=11,
    )
    arrow(ax, 93, 20, 93, 32, "", color=TEAL)
    arrow(ax, 135, 20, 135, 32, "", color=TEAL)
    ax.text(
        38,
        36,
        "Pod : la plus petite unité,\n1 ou plusieurs conteneurs ;"
        "\nle planificateur choisit\nson nœud",
        fontsize=10,
        color=INK,
        va="center",
    )
    ax.text(
        38,
        22,
        "Deployment : « toujours\n1 pod seaweedfs »\n→ recréé s'il tombe",
        fontsize=10,
        color=INK,
        va="center",
    )
    ax.text(
        38,
        10,
        "Service : adresse stable,\nvalable dans tout le cluster\nNamespace : « dossier »",
        fontsize=10,
        color=INK,
        va="center",
    )
    save(fig, "03-kubernetes.png")


# 5. Infrastructure as Code ------------------------------------------------------------
def iac():
    fig, ax = canvas(16, 6.5)
    title(
        ax,
        "Infrastructure as Code : trois commandes, trois couches",
        "Chaque couche est décrite dans un fichier versionné dans le repo : "
        "tout le monde obtient la même chose.",
    )
    steps = [
        ("vagrant up", "Vagrantfile", "crée la VM\nUbuntu 24.04", NAVY, PALE_NAVY),
        (
            "Ansible (automatique)",
            "playbook.yml",
            "installe Docker, kind,\nkubectl, helm, k9s, uv",
            NAVY,
            PALE_NAVY,
        ),
        (
            "make up",
            "Makefile + infra/",
            "crée le cluster kind\n+ SeaweedFS + MLflow",
            TEAL,
            PALE_TEAL,
        ),
    ]
    for i, (cmd, file, what, edge, fill) in enumerate(steps):
        x = 4 + i * 52
        box(ax, x, 10, 44, 38, cmd, "", fill=fill, edge=edge, title_top=True, tsize=14)
        ax.text(x + 22, 33, file, ha="center", fontsize=11.5, color=edge, family="DejaVu Sans Mono")
        ax.text(
            x + 22, 21, what, ha="center", va="center", fontsize=11.5, color=INK, linespacing=1.4
        )
        if i < 2:
            arrow(ax, x + 44, 29, x + 52, 29, "", color=MUTED)
    ax.text(
        4,
        4,
        "Sous Linux / macOS, les deux premières couches sont remplacées par l'installation directe "
        "des outils (étapes 1 et 2 du lab).",
        fontsize=10.5,
        color=MUTED,
        style="italic",
    )
    save(fig, "04-iac.png")


# 6. Git et GitHub ----------------------------------------------------------------------
def git():
    fig, ax = canvas(16, 7.5)
    title(
        ax,
        "Git et GitHub : le circuit d'un lab",
        "Git garde l'historique de vos fichiers ; GitHub héberge les "
        "repos et les pull requests (relecture avant fusion).",
    )
    box(
        ax,
        3,
        36,
        30,
        22,
        "Repo du cours",
        "firaskhl/\nmlops-cours-2026",
        fill=LIGHT,
        edge=MUTED,
        ssize=10.5,
    )
    box(
        ax,
        48,
        36,
        32,
        22,
        "Votre copie",
        "VOTRE_USER/\nmlops-cours-2026\n(GitHub)",
        fill=PALE_NAVY,
        edge=NAVY,
        ssize=10.5,
    )
    arrow(ax, 33, 47, 48, 47, "fork", color=NAVY)
    box(
        ax,
        98,
        36,
        58,
        22,
        "Dans la VM : ~/mlops-cours-2026",
        "",
        fill=PALE_TEAL,
        edge=TEAL,
        title_top=True,
        tsize=12,
    )
    arrow(ax, 80, 50, 98, 50, "git clone", color=NAVY)
    chain = [("main", 100, 12), ("branche\nlab/m0-setup", 115, 20), ("git commit", 138, 16)]
    for name, x, w in chain:
        box(ax, x, 38.5, w, 11, name, fill=WHITE, edge=TEAL, tsize=9.5)
    arrow(ax, 112, 44, 115, 44, "", color=TEAL, lw=1.4)
    arrow(ax, 135, 44, 138, 44, "", color=TEAL, lw=1.4)
    box(
        ax,
        48,
        6,
        32,
        20,
        "Pull request",
        "relue par le binôme\npuis « Merge » dans main",
        fill=PALE_ORANGE,
        edge=ORANGE,
        ssize=10,
    )
    arrow(ax, 146, 36, 80, 18, "git push", color=ORANGE, rad=-0.15)
    arrow(ax, 64, 26, 64, 36, "fusion", color=ORANGE, loff=(6, -2))
    box(
        ax,
        3,
        6,
        38,
        20,
        "Clé SSH",
        "prouve à GitHub que\nc'est vous (ssh-keygen\ndans la VM)",
        fill=WHITE,
        edge=MUTED,
        ssize=10,
    )
    save(fig, "05-git-github.png")


# 7. Ce que teste le Lab 0 ---------------------------------------------------------------
def flux_lab0():
    fig, ax = canvas(16, 7)
    title(
        ax,
        "Ce que vérifient les smoke tests du Lab 0 (étape 7)",
        "Deux chemins vers le même stockage S3 : MLflow (via le serveur) et DVC (directement).",
    )
    box(
        ax,
        3,
        36,
        36,
        18,
        "smoke_mlflow.py",
        "logge un paramètre,\ndes métriques, un fichier",
        fill=LIGHT,
        edge=MUTED,
        ssize=10,
    )
    box(
        ax,
        62,
        36,
        34,
        18,
        "Serveur MLflow",
        "localhost:5000\n(make pf)",
        fill=PALE_ORANGE,
        edge=ORANGE,
        ssize=10,
    )
    box(
        ax,
        120,
        22,
        36,
        40,
        "SeaweedFS (S3)",
        "",
        fill=PALE_TEAL,
        edge=TEAL,
        title_top=True,
        tsize=12,
    )
    box(ax, 123, 42, 30, 10, "mlflow-artifacts", fill=WHITE, edge=TEAL, tsize=10)
    box(ax, 123, 27, 30, 10, "mlops-test", fill=WHITE, edge=TEAL, tsize=10)
    arrow(ax, 39, 45, 62, 45, "HTTP", color=NAVY)
    arrow(ax, 96, 45, 123, 47, "S3", color=ORANGE)
    box(
        ax,
        3,
        8,
        36,
        18,
        "dvc push",
        "depuis /tmp/dvc-smoke\n(fichier sample.txt)",
        fill=LIGHT,
        edge=MUTED,
        ssize=10,
    )
    arrow(ax, 39, 17, 123, 31, "S3 : localhost:8333 (make pf)", color=NAVY, loff=(0, 2.5))
    box(
        ax,
        62,
        2,
        50,
        10,
        "Navigateur : localhost:5000 et localhost:8888/buckets/",
        fill=WHITE,
        edge=MUTED,
        tsize=10,
    )
    save(fig, "06-lab0-flux.png")


if __name__ == "__main__":
    for f in (vue_ensemble, docker, vm_vs_conteneur, kubernetes, iac, git, flux_lab0):
        f()
    print("Schémas écrits dans", OUT)
