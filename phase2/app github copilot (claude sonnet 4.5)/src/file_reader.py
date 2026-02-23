"""
Module de lecture et validation de fichiers de points.
"""

from typing import List, Tuple
import re
from pathlib import Path


class FileReaderError(Exception):
    """Exception personnalisée pour les erreurs de lecture de fichier."""
    pass


class FileReader:
    """
    Classe pour lire et valider des fichiers contenant des coordonnées de points.
    
    Le format attendu est une paire de coordonnées par ligne, séparées par
    une virgule ou un point-virgule.
    """
    
    # Pattern regex pour valider les lignes de coordonnées
    COORDINATE_PATTERN = re.compile(
        r'^\s*(-?\d+\.?\d*)\s*[,;]\s*(-?\d+\.?\d*)\s*$'
    )
    
    @staticmethod
    def read_points(file_path: str) -> List[Tuple[float, float]]:
        """
        Lit un fichier et extrait les coordonnées des points.
        
        Args:
            file_path: Chemin vers le fichier à lire
            
        Returns:
            Liste de tuples (x, y) représentant les coordonnées
            
        Raises:
            FileReaderError: Si le fichier n'existe pas, est vide, 
                           ou contient des données invalides
        """
        path = Path(file_path)
        
        # Vérification de l'existence du fichier
        if not path.exists():
            raise FileReaderError(f"Le fichier '{file_path}' n'existe pas.")
        
        if not path.is_file():
            raise FileReaderError(f"'{file_path}' n'est pas un fichier valide.")
        
        # Lecture du fichier
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except IOError as e:
            raise FileReaderError(f"Erreur lors de la lecture du fichier : {e}")
        
        # Filtrage des lignes vides et commentaires
        lines = [
            line.strip() 
            for line in lines 
            if line.strip() and not line.strip().startswith('#')
        ]
        
        if not lines:
            raise FileReaderError("Le fichier est vide ou ne contient aucune donnée valide.")
        
        # Parsing des coordonnées
        points = []
        for i, line in enumerate(lines, start=1):
            match = FileReader.COORDINATE_PATTERN.match(line)
            if not match:
                raise FileReaderError(
                    f"Ligne {i} : format invalide. "
                    f"Format attendu : 'x,y' ou 'x;y' (ex: '2.5,3.7'). "
                    f"Reçu : '{line}'"
                )
            
            try:
                x = float(match.group(1))
                y = float(match.group(2))
                points.append((x, y))
            except ValueError as e:
                raise FileReaderError(
                    f"Ligne {i} : impossible de convertir les coordonnées en nombres : {e}"
                )
        
        return points
    
    @staticmethod
    def validate_points(points: List[Tuple[float, float]], 
                       min_points: int = 3) -> None:
        """
        Valide que la liste de points est utilisable pour un diagramme de Voronoï.
        
        Args:
            points: Liste de coordonnées à valider
            min_points: Nombre minimum de points requis
            
        Raises:
            FileReaderError: Si les points ne sont pas valides
        """
        if len(points) < min_points:
            raise FileReaderError(
                f"Au moins {min_points} points sont nécessaires. "
                f"Seulement {len(points)} point(s) trouvé(s)."
            )
        
        # Vérification des doublons
        unique_points = set(points)
        if len(unique_points) < len(points):
            duplicates = len(points) - len(unique_points)
            raise FileReaderError(
                f"Le fichier contient {duplicates} point(s) dupliqué(s). "
                f"Chaque point doit être unique."
            )
        
        # Vérification que tous les points ne sont pas colinéaires
        if len(points) >= 3:
            if FileReader._are_collinear(points):
                raise FileReaderError(
                    "Tous les points sont colinéaires. "
                    "Un diagramme de Voronoï nécessite des points non colinéaires."
                )
    
    @staticmethod
    def _are_collinear(points: List[Tuple[float, float]]) -> bool:
        """
        Vérifie si tous les points sont colinéaires.
        
        Args:
            points: Liste de coordonnées
            
        Returns:
            True si tous les points sont colinéaires, False sinon
        """
        if len(points) < 3:
            return True
        
        # Prendre les deux premiers points comme référence
        x1, y1 = points[0]
        x2, y2 = points[1]
        
        # Vérifier si tous les autres points sont sur la même ligne
        tolerance = 1e-10
        for x3, y3 in points[2:]:
            # Calcul du produit vectoriel (déterminant)
            # Si non nul, les points ne sont pas colinéaires
            cross_product = abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))
            if cross_product > tolerance:
                return False
        
        return True