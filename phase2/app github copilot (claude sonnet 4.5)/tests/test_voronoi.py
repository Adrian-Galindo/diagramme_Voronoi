"""
Tests unitaires pour le module voronoi.
"""

import pytest
import numpy as np
from src.voronoi import VoronoiGenerator, VoronoiError


class TestVoronoiGenerator:
    """Tests pour la classe VoronoiGenerator."""
    
    def test_init_valid_points(self):
        """Test initialisation avec points valides."""
        points = [(0, 0), (1, 0), (0, 1)]
        generator = VoronoiGenerator(points)
        
        assert generator.points.shape == (3, 2)
        assert np.array_equal(generator.points, np.array([[0, 0], [1, 0], [0, 1]]))
    
    def test_init_too_few_points(self):
        """Test initialisation avec trop peu de points."""
        points = [(0, 0), (1, 0)]
        
        with pytest.raises(VoronoiError, match="Au moins 3 points"):
            VoronoiGenerator(points)
    
    def test_init_invalid_dimensions(self):
        """Test initialisation avec dimensions invalides."""
        points = [(0, 0, 0), (1, 1, 1), (2, 2, 2)]  # 3D au lieu de 2D avec 3 points
        
        with pytest.raises(VoronoiError, match="2 coordonnées"):
            VoronoiGenerator(points)
    
    def test_init_nan_values(self):
        """Test initialisation avec valeurs NaN."""
        points = [(0, 0), (np.nan, 1), (2, 2)]
        
        with pytest.raises(VoronoiError, match="nombres finis"):
            VoronoiGenerator(points)
    
    def test_init_infinite_values(self):
        """Test initialisation avec valeurs infinies."""
        points = [(0, 0), (np.inf, 1), (2, 2)]
        
        with pytest.raises(VoronoiError, match="nombres finis"):
            VoronoiGenerator(points)
    
    def test_compute_success(self):
        """Test calcul réussi du diagramme."""
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        generator = VoronoiGenerator(points)
        
        voronoi = generator.compute()
        
        assert voronoi is not None
        assert len(voronoi.points) == 4
        assert generator._voronoi is voronoi
    
    def test_voronoi_property_before_compute(self):
        """Test accès à la propriété voronoi avant calcul."""
        points = [(0, 0), (1, 0), (0, 1)]
        generator = VoronoiGenerator(points)
        
        with pytest.raises(VoronoiError, match="pas encore été calculé"):
            _ = generator.voronoi
    
    def test_voronoi_property_after_compute(self):
        """Test accès à la propriété voronoi après calcul."""
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        generator = VoronoiGenerator(points)
        generator.compute()
        
        voronoi = generator.voronoi
        assert voronoi is not None
    
    def test_get_points(self):
        """Test récupération des points."""
        points = [(0, 0), (1, 0), (0, 1)]
        generator = VoronoiGenerator(points)
        
        retrieved_points = generator.get_points()
        
        assert np.array_equal(retrieved_points, np.array([[0, 0], [1, 0], [0, 1]]))
    
    def test_get_vertices(self):
        """Test récupération des sommets."""
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        generator = VoronoiGenerator(points)
        generator.compute()
        
        vertices = generator.get_vertices()
        
        assert vertices is not None
        assert len(vertices) > 0
    
    def test_get_regions(self):
        """Test récupération des régions."""
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        generator = VoronoiGenerator(points)
        generator.compute()
        
        regions = generator.get_regions()
        
        assert regions is not None
        assert isinstance(regions, list)
    
    def test_get_bounded_regions(self):
        """Test récupération des régions bornées."""
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        generator = VoronoiGenerator(points)
        generator.compute()
        
        bounded_regions = generator.get_bounded_regions()
        
        assert isinstance(bounded_regions, list)
        for point_idx, region in bounded_regions:
            assert isinstance(point_idx, (int, np.integer))
            assert isinstance(region, list)
            assert -1 not in region
    
    def test_get_statistics(self):
        """Test récupération des statistiques."""
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        generator = VoronoiGenerator(points)
        generator.compute()
        
        stats = generator.get_statistics()
        
        assert stats["num_points"] == 4
        assert "num_vertices" in stats
        assert "num_regions" in stats
        assert "num_bounded_regions" in stats
        assert "points_bounds" in stats
        
        bounds = stats["points_bounds"]
        assert bounds["x_min"] == 0
        assert bounds["x_max"] == 1
        assert bounds["y_min"] == 0
        assert bounds["y_max"] == 1
    
    def test_compute_with_random_points(self):
        """Test calcul avec points aléatoires."""
        np.random.seed(42)
        points = np.random.rand(10, 2) * 100
        
        generator = VoronoiGenerator(points.tolist())
        voronoi = generator.compute()
        
        assert voronoi is not None
        assert len(voronoi.points) == 10