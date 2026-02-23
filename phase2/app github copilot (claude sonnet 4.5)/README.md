# Générateur de Diagrammes de Voronoï

Application Python complète pour générer et visualiser des diagrammes de Voronoï à partir de fichiers de points.

## 📋 Fonctionnalités

- ✅ Lecture de fichiers texte contenant des coordonnées de points
- ✅ Calcul automatique du diagramme de Voronoï
- ✅ Visualisation interactive avec matplotlib
- ✅ Export en formats SVG, PNG et JPG
- ✅ Interface en ligne de commande conviviale
- ✅ Gestion robuste des erreurs
- ✅ Tests automatisés complets

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip

### Étapes d'installation

1. Clonez ou téléchargez ce dépôt

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 📖 Utilisation

### Mode interactif simple

```bash
python main.py
```

### Mode ligne de commande

```bash
# Générer et afficher un diagramme
python main.py --input points.txt

# Exporter en SVG
python main.py --input points.txt --output diagram.svg

# Exporter en PNG avec dimensions personnalisées
python main.py --input points.txt --output diagram.png --width 1920 --height 1080

# Sans affichage interactif
python main.py --input points.txt --output diagram.png --no-show
```

### Format du fichier d'entrée

Le fichier doit contenir une paire de coordonnées par ligne :

```
2,4
5.3,4.5
-1.2,3.8
10,15
```

Formats acceptés :
- Séparateur virgule ou point-virgule : `x,y` ou `x;y`
- Espaces autorisés : `x, y` ou ` x , y `
- Nombres entiers ou décimaux

## 🧪 Tests

Exécuter tous les tests :

```bash
python -m pytest tests/ -v
```

Exécuter avec couverture de code :

```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## 📁 Structure du projet

```
voronoi-generator/
├── src/
│   ├── __init__.py
│   ├── file_reader.py      # Lecture et validation des fichiers
│   ├── voronoi.py          # Calcul du diagramme de Voronoï
│   ├── visualizer.py       # Visualisation et export
│   └── cli.py              # Interface ligne de commande
├── tests/
│   ├── __init__.py
│   ├── test_file_reader.py
│   ├── test_voronoi.py
│   └── test_visualizer.py
├── examples/
│   └── sample_points.txt   # Exemple de fichier de points
├── main.py                 # Point d'entrée principal
├── requirements.txt        # Dépendances Python
└── README.md              # Cette documentation
```

## 🛠️ Architecture technique

### Modules principaux

1. **file_reader.py** : Gestion de la lecture des fichiers
   - Validation du format
   - Parsing des coordonnées
   - Gestion des erreurs de format

2. **voronoi.py** : Calcul du diagramme
   - Utilisation de scipy.spatial.Voronoi
   - Calcul des régions bornées
   - Validation des points d'entrée

3. **visualizer.py** : Visualisation et export
   - Rendu matplotlib
   - Export SVG, PNG, JPG
   - Configuration des styles

4. **cli.py** : Interface utilisateur
   - Arguments en ligne de commande
   - Mode interactif
   - Validation des entrées

### Gestion des erreurs

L'application gère les cas suivants :
- Fichier inexistant ou illisible
- Format de coordonnées invalide
- Nombre de points insuffisant (< 3)
- Points colinéaires ou identiques
- Erreurs d'export

## 📊 Exemples

### Exemple 1 : Points aléatoires

Créez un fichier `random_points.txt` :
```
10.5,20.3
45.2,67.8
23.1,89.4
78.9,12.6
56.7,45.3
```

Générez le diagramme :
```bash
python main.py --input random_points.txt --output voronoi.svg
```

### Exemple 2 : Grille régulière

```
0,0
0,10
0,20
10,0
10,10
10,20
20,0
20,10
20,20
```

## 🤝 Contribution

Les contributions sont bienvenues ! Assurez-vous que :
- Le code respecte PEP 8
- Les tests passent tous
- La couverture de code est maintenue
- La documentation est à jour

## 📝 Licence

Ce projet est libre d'utilisation pour des fins éducatives et commerciales.

## 👤 Auteur

Maxime-LointierDéveloppe

## 🐛 Support

Pour signaler un bug ou demander une fonctionnalité, créez une issue sur le dépôt du projet.
```