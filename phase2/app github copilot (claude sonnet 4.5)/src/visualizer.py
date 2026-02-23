"""
Module de visualisation et export des diagrammes de Voronoï.
"""

from typing import Optional, Tuple
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np
from pathlib import Path
from scipy.spatial import Voronoi, voronoi_plot_2d


class VisualizerError(Exception):
    """Exception personnalisée pour les erreurs de visualisation."""
    pass


class VoronoiVisualizer:
    """
    Classe pour visualiser et exporter des diagrammes de Voronoï.
    
    Supporte l'affichage interactif et l'export en SVG, PNG et JPG.
    """
    
    SUPPORTED_FORMATS = {'.svg', '.png', '.jpg', '.jpeg'}
    
    def __init__(self, voronoi: Voronoi):
        """
        Initialise le visualiseur avec un diagramme de Voronoï.
        
        Args:
            voronoi: Objet Voronoi de scipy à visualiser
        """
        self.voronoi = voronoi
        self.fig: Optional[Figure] = None
        self.ax: Optional[Axes] = None
    
    def create_plot(self, 
                   figsize: Tuple[int, int] = (10, 10),
                   show_points: bool = True,
                   show_vertices: bool = False,
                   point_size: int = 50,
                   point_color: str = 'red',
                   line_color: str = 'blue',
                   line_width: float = 1.0) -> Tuple[Figure, Axes]:
        """
        Crée le graphique du diagramme de Voronoï.
        
        Args:
            figsize: Taille de la figure (largeur, hauteur) en pouces
            show_points: Afficher les points générateurs
            show_vertices: Afficher les sommets du diagramme
            point_size: Taille des points
            point_color: Couleur des points
            line_color: Couleur des lignes du diagramme
            line_width: Épaisseur des lignes
            
        Returns:
            Tuple (figure, axes) matplotlib
        """
        # Création de la figure
        self.fig, self.ax = plt.subplots(figsize=figsize)
        
        # Tracer le diagramme de Voronoï
        voronoi_plot_2d(
            self.voronoi,
            ax=self.ax,
            show_points=show_points,
            show_vertices=show_vertices,
            line_colors=line_color,
            line_width=line_width,
            point_size=point_size
        )
        
        # Personnalisation des points si affichés
        if show_points:
            self.ax.plot(
                self.voronoi.points[:, 0],
                self.voronoi.points[:, 1],
                'o',
                markersize=np.sqrt(point_size),
                color=point_color,
                markeredgecolor='black',
                markeredgewidth=0.5,
                zorder=3
            )
        
        # Configuration du graphique
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_title(
            f'Diagramme de Voronoï ({len(self.voronoi.points)} points)',
            fontsize=14,
            fontweight='bold'
        )
        self.ax.set_xlabel('X', fontsize=12)
        self.ax.set_ylabel('Y', fontsize=12)
        self.ax.grid(True, alpha=0.3, linestyle='--')
        
        # Ajuster les limites pour voir tout le diagramme
        self._adjust_limits()
        
        return self.fig, self.ax
    
    def _adjust_limits(self, margin: float = 0.1) -> None:
        """
        Ajuste les limites du graphique pour inclure tous les points avec une marge.
        
        Args:
            margin: Pourcentage de marge à ajouter (0.1 = 10%)
        """
        if self.ax is None:
            return
        
        points = self.voronoi.points
        x_min, y_min = points.min(axis=0)
        x_max, y_max = points.max(axis=0)
        
        x_range = x_max - x_min
        y_range = y_max - y_min
        
        # Gestion du cas où tous les points sont sur une ligne
        if x_range == 0:
            x_range = 1
        if y_range == 0:
            y_range = 1
        
        self.ax.set_xlim(
            x_min - margin * x_range,
            x_max + margin * x_range
        )
        self.ax.set_ylim(
            y_min - margin * y_range,
            y_max + margin * y_range
        )
    
    def show(self) -> None:
        """
        Affiche le graphique de manière interactive.
        
        Raises:
            VisualizerError: Si le graphique n'a pas été créé
        """
        if self.fig is None:
            raise VisualizerError(
                "Le graphique n'a pas été créé. "
                "Appelez d'abord la méthode create_plot()."
            )
        
        plt.show()
    
    def save(self, 
             output_path: str,
             dpi: int = 300,
             transparent: bool = False) -> None:
        """
        Sauvegarde le graphique dans un fichier.
        
        Args:
            output_path: Chemin du fichier de sortie
            dpi: Résolution en points par pouce (pour PNG/JPG)
            transparent: Fond transparent (pour PNG)
            
        Raises:
            VisualizerError: Si le graphique n'a pas été créé ou 
                           si le format n'est pas supporté
        """
        if self.fig is None:
            raise VisualizerError(
                "Le graphique n'a pas été créé. "
                "Appelez d'abord la méthode create_plot()."
            )
        
        path = Path(output_path)
        
        # Vérification du format
        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise VisualizerError(
                f"Format non supporté : {path.suffix}. "
                f"Formats supportés : {', '.join(self.SUPPORTED_FORMATS)}"
            )
        
        # Création du répertoire parent si nécessaire
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarde
        try:
            self.fig.savefig(
                output_path,
                dpi=dpi,
                bbox_inches='tight',
                transparent=transparent,
                format=path.suffix[1:]  # Enlever le point du suffix
            )
            print(f"✓ Diagramme sauvegardé : {output_path}")
        except Exception as e:
            raise VisualizerError(f"Erreur lors de la sauvegarde : {e}")
    
    def close(self) -> None:
        """Ferme la figure matplotlib pour libérer les ressources."""
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
    
    @staticmethod
    def quick_plot(voronoi: Voronoi, 
                   output_path: Optional[str] = None,
                   show: bool = True,
                   **kwargs) -> None:
        """
        Méthode utilitaire pour créer et afficher/sauvegarder rapidement un diagramme.
        
        Args:
            voronoi: Objet Voronoi à visualiser
            output_path: Chemin de sortie optionnel pour sauvegarder
            show: Afficher le graphique de manière interactive
            **kwargs: Arguments supplémentaires pour create_plot()
        """
        visualizer = VoronoiVisualizer(voronoi)
        visualizer.create_plot(**kwargs)
        
        if output_path:
            visualizer.save(output_path)
        
        if show:
            visualizer.show()
        else:
            visualizer.close()