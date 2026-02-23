"""
Tests unitaires pour le module visualizer.
"""

import pytest
import numpy as np

# Configurer matplotlib AVANT de l'importer
import matplotlib
matplotlib.use('Agg')  # Backend non-interactif pour les tests

import matplotlib.pyplot as plt
from pathlib import Path
from scipy.spatial import Voronoi
from src.visualizer import VoronoiVisualizer, VisualizerError



@pytest.fixture
def sample_voronoi():
    """Fixture créant un diagramme de Voronoï simple."""
    points = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
    return Voronoi(points)


class TestVoronoiVisualizer:
    """Tests pour la classe VoronoiVisualizer."""
    
    def test_init(self, sample_voronoi):
        """Test initialisation."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        
        assert visualizer.voronoi is sample_voronoi
        assert visualizer.fig is None
        assert visualizer.ax is None
    
    def test_create_plot_default(self, sample_voronoi):
        """Test création de graphique avec paramètres par défaut."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        
        fig, ax = visualizer.create_plot()
        
        assert fig is not None
        assert ax is not None
        assert visualizer.fig is fig
        assert visualizer.ax is ax
        
        plt.close(fig)
    
    def test_create_plot_custom_size(self, sample_voronoi):
        """Test création de graphique avec taille personnalisée."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        
        fig, ax = visualizer.create_plot(figsize=(8, 6))
        
        assert fig.get_size_inches()[0] == 8
        assert fig.get_size_inches()[1] == 6
        
        plt.close(fig)
    
    def test_create_plot_custom_colors(self, sample_voronoi):
        """Test création de graphique avec couleurs personnalisées."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        
        fig, ax = visualizer.create_plot(
            point_color='green',
            line_color='purple'
        )
        
        assert fig is not None
        
        plt.close(fig)
    
    def test_create_plot_no_points(self, sample_voronoi):
        """Test création de graphique sans afficher les points."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        
        fig, ax = visualizer.create_plot(show_points=False)
        
        assert fig is not None
        
        plt.close(fig)
    
    def test_create_plot_with_vertices(self, sample_voronoi):
        """Test création de graphique avec sommets visibles."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        
        fig, ax = visualizer.create_plot(show_vertices=True)
        
        assert fig is not None
        
        plt.close(fig)
    
    def test_show_without_plot(self, sample_voronoi):
        """Test affichage sans créer de graphique."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        
        with pytest.raises(VisualizerError, match="n'a pas été créé"):
            visualizer.show()
    
    def test_save_without_plot(self, sample_voronoi, tmp_path):
        """Test sauvegarde sans créer de graphique."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        output_path = tmp_path / "output.svg"
        
        with pytest.raises(VisualizerError, match="n'a pas été créé"):
            visualizer.save(str(output_path))
    
    def test_save_svg(self, sample_voronoi, tmp_path):
        """Test sauvegarde en format SVG."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        visualizer.create_plot()
        
        output_path = tmp_path / "diagram.svg"
        visualizer.save(str(output_path))
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        
        plt.close(visualizer.fig)
    
    def test_save_png(self, sample_voronoi, tmp_path):
        """Test sauvegarde en format PNG."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        visualizer.create_plot()
        
        output_path = tmp_path / "diagram.png"
        visualizer.save(str(output_path))
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        
        plt.close(visualizer.fig)
    
    def test_save_jpg(self, sample_voronoi, tmp_path):
        """Test sauvegarde en format JPG."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        visualizer.create_plot()
        
        output_path = tmp_path / "diagram.jpg"
        visualizer.save(str(output_path))
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        
        plt.close(visualizer.fig)
    
    def test_save_unsupported_format(self, sample_voronoi, tmp_path):
        """Test sauvegarde avec format non supporté."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        visualizer.create_plot()
        
        output_path = tmp_path / "diagram.txt"
        
        with pytest.raises(VisualizerError, match="Format non supporté"):
            visualizer.save(str(output_path))
        
        plt.close(visualizer.fig)
    
    def test_save_creates_directory(self, sample_voronoi, tmp_path):
        """Test que la sauvegarde crée le répertoire parent si nécessaire."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        visualizer.create_plot()
        
        output_path = tmp_path / "subdir" / "nested" / "diagram.svg"
        visualizer.save(str(output_path))
        
        assert output_path.exists()
        
        plt.close(visualizer.fig)
    
    def test_save_custom_dpi(self, sample_voronoi, tmp_path):
        """Test sauvegarde avec DPI personnalisé."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        visualizer.create_plot()
        
        output_path = tmp_path / "diagram.png"
        visualizer.save(str(output_path), dpi=150)
        
        assert output_path.exists()
        
        plt.close(visualizer.fig)
    
    def test_close(self, sample_voronoi):
        """Test fermeture de la figure."""
        visualizer = VoronoiVisualizer(sample_voronoi)
        visualizer.create_plot()
        
        assert visualizer.fig is not None
        
        visualizer.close()
        
        assert visualizer.fig is None
        assert visualizer.ax is None
    
    def test_quick_plot_show_only(self, sample_voronoi):
        """Test méthode quick_plot pour affichage uniquement."""
        # On ne peut pas vraiment tester l'affichage interactif
        # Mais on peut vérifier que la méthode ne lève pas d'exception
        # En utilisant show=False
        VoronoiVisualizer.quick_plot(sample_voronoi, show=False)
    
    def test_quick_plot_save_only(self, sample_voronoi, tmp_path):
        """Test méthode quick_plot pour sauvegarde uniquement."""
        output_path = tmp_path / "quick.svg"
        
        VoronoiVisualizer.quick_plot(
            sample_voronoi,
            output_path=str(output_path),
            show=False
        )
        
        assert output_path.exists()
    
    def test_quick_plot_with_custom_params(self, sample_voronoi, tmp_path):
        """Test méthode quick_plot avec paramètres personnalisés."""
        output_path = tmp_path / "custom.png"
        
        VoronoiVisualizer.quick_plot(
            sample_voronoi,
            output_path=str(output_path),
            show=False,
            figsize=(12, 12),
            point_color='blue',
            line_color='red'
        )
        
        assert output_path.exists()