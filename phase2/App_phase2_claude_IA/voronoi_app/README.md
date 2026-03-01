# Générer un diagramme de Voronoï — SAÉ S6

Dans le cadre de la SAÉ du semestre 6 de BUT 3 Informatique, nous devions réaliser un projet qui permet de générer des diagrammes de Voronoï à partir de fichiers qui contiennent une liste de points sous forme de paire de nombres qui correspondent aux coordonnées. L'application est une interface graphique développée en Python permettant de charger ces fichiers, de visualiser le diagramme interactivement et de l'exporter en SVG ou en image et réalisé à l'aide de L'IA générative CLAUDE.

---

## Structure du projet

```
voronoi_app/
├── main.py                  # Point d'entrée de l'application
├── requirements.txt         # Dépendances Python
├── core/
│   ├── parser.py            # Lecture et validation du fichier de points
│   └── voronoi.py           # Calcul du diagramme de Voronoi
├── ui/
│   ├── app.py               # Fenêtre principale
│   ├── canvas.py            # Zone de visualisation interactive
│   └── toolbar.py           # Barre d'outils
├── export/
│   ├── svg_exporter.py      # Export en SVG
│   └── image_exporter.py    # Export en PNG / JPEG
├── tests/                   # Tests unitaires (pytest)
└── data/                    # Fichiers de points d'exemple
```

---

## Technique de génération

Le diagramme de Voronoi est calculé via la bibliothèque **SciPy** (`scipy.spatial.Voronoi`), qui implémente l'algorithme de **Fortune** (balayage de plan). Avant le calcul, les points sont validés : doublons détectés par comparaison directe, colinéarité vérifiée par décomposition en valeurs singulières (SVD). Un minimum de 3 points non colinéaires est requis.

Le fichier d'entrée accepte les coordonnées séparées par une virgule, un point-virgule ou un espace (ex : `2,4` ou `2 4`). Les lignes vides et les commentaires (`#`) sont ignorés.

---

## Installation et prérequis

**Prérequis :** Python 3.10 ou supérieur

> **Linux :** Tkinter n'est pas toujours inclus par défaut. Si l'application ne démarre pas, installez-le d'abord :
> ```bash
> sudo apt-get install python3-tk   # Debian / Ubuntu
> ```

**Se placer dans le dossier du projet :**

```bash
cd phase2/App_phase2_claude_IA/voronoi_app
```


**Installer les dépendances :**

```bash
pip install -r requirements.txt
```

**Lancer l'application :**

```bash
python main.py
```

**Lancer les tests :**

```bash
pytest tests/
```

**Couverture de tests** (nécessite `pytest-cov`) :

```bash
pip install pytest-cov
pytest --cov=. tests/ --cov-report=term-missing
```

---

## Auteur

**Anouar Rouibi** — BUT 3 Informatique, SAÉ Semestre 6
