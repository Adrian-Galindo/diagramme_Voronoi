"""
Module de calcul des diagrammes de Voronoï.
"""

from typing import List, Tuple, Optional
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy.typing as npt


class VoronoiError(Exception):
    """Exception personnalisée pour les erreurs de calcul de Voronoï."""
    pass


class VoronoiGenerator:
    """
    Classe pour générer des diagrammes de Voronoï à partir de points.
    
    Utilise scipy.spatial.Voronoi pour les calculs géométriques.
    """
    
    def __init__(self, points: List[Tuple[float, float]]):
        """
        Initialise le générateur avec une liste de points.
        
        Args:
            points: Liste de tuples (x, y) représentant les coordonnées
            
        Raises:
            VoronoiError: Si les points ne sont pas valides
        """
        self.points = np.array(points, dtype=np.float64)
        self._validate_points()
        self._voronoi: Optional[Voronoi] = None
    
    def _validate_points(self) -> None:
        """
        Valide les points d'entrée.
        
        Raises:
            VoronoiError: Si les points ne sont pas valides
        """
        # Vérification des dimensions AVANT le nombre de points
        if len(self.points.shape) != 2 or self.points.shape[1] != 2:
            raise VoronoiError(
                f"Chaque point doit avoir exactement 2 coordonnées (x, y). "
                f"Forme reçue : {self.points.shape}"
            )
        
        if self.points.shape[0] < 3:
            raise VoronoiError(
                f"Au moins 3 points sont nécessaires pour un diagramme de Voronoï. "
                f"Reçu : {self.points.shape[0]}"
            )
        
        # Vérification des valeurs NaN ou infinies
        if np.any(~np.isfinite(self.points)):
            raise VoronoiError(
                "Les coordonnées des points doivent être des nombres finis."
            )
    
    def compute(self) -> Voronoi:
        """
        Calcule le diagramme de Voronoï.
        
        Returns:
            Objet Voronoi de scipy contenant le diagramme calculé
            
        Raises:
            VoronoiError: Si le calcul échoue
        """
        try:
            self._voronoi = Voronoi(self.points)
            return self._voronoi
        except Exception as e:
            raise VoronoiError(f"Erreur lors du calcul du diagramme de Voronoï : {e}")
    
    @property
    def voronoi(self) -> Voronoi:
        """
        Retourne le diagramme de Voronoï calculé.
        
        Returns:
            Objet Voronoi
            
        Raises:
            VoronoiError: Si le diagramme n'a pas encore été calculé
        """
        if self._voronoi is None:
            raise VoronoiError(
                "Le diagramme n'a pas encore été calculé. "
                "Appelez d'abord la méthode compute()."
            )
        return self._voronoi
    
    def get_points(self) -> npt.NDArray[np.float64]:
        """
        Retourne les points d'entrée.
        
        Returns:
            Array numpy des coordonnées des points
        """
        return self.points
    
    def get_vertices(self) -> npt.NDArray[np.float64]:
        """
        Retourne les sommets du diagramme de Voronoï.
        
        Returns:
            Array numpy des coordonnées des sommets
            
        Raises:
            VoronoiError: Si le diagramme n'a pas encore été calculé
        """
        return self.voronoi.vertices
    
    def get_regions(self) -> List[List[int]]:
        """
        Retourne les régions du diagramme de Voronoï.
        
        Returns:
            Liste de listes d'indices de sommets pour chaque région
            
        Raises:
            VoronoiError: Si le diagramme n'a pas encore été calculé
        """
        return self.voronoi.regions
    
    def get_bounded_regions(self) -> List[Tuple[int, List[int]]]:
        """
        Retourne uniquement les régions bornées (fermées) du diagramme.
        
        Returns:
            Liste de tuples (point_index, vertex_indices) pour chaque région bornée
            
        Raises:
            VoronoiError: Si le diagramme n'a pas encore été calculé
        """
        bounded_regions = []
        
        for point_idx, region_idx in enumerate(self.voronoi.point_region):
            region = self.voronoi.regions[region_idx]
            
            # Une région est bornée si elle ne contient pas -1
            # et si elle n'est pas vide
            if region and -1 not in region:
                bounded_regions.append((point_idx, region))
        
        return bounded_regions
    
    def get_statistics(self) -> dict:
        """
        Retourne des statistiques sur le diagramme de Voronoï.
        
        Returns:
            Dictionnaire contenant diverses statistiques
            
        Raises:
            VoronoiError: Si le diagramme n'a pas encore été calculé
        """
        bounded_regions = self.get_bounded_regions()
        
        return {
            "num_points": len(self.points),
            "num_vertices": len(self.voronoi.vertices),
            "num_regions": len(self.voronoi.regions),
            "num_bounded_regions": len(bounded_regions),
            "num_unbounded_regions": len(self.points) - len(bounded_regions),
            "points_bounds": {
                "x_min": float(np.min(self.points[:, 0])),
                "x_max": float(np.max(self.points[:, 0])),
                "y_min": float(np.min(self.points[:, 1])),
                "y_max": float(np.max(self.points[:, 1])),
            }
        }