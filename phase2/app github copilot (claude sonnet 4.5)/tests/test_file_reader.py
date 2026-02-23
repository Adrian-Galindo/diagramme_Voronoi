"""
Tests unitaires pour le module file_reader.
"""

import pytest
import tempfile
from pathlib import Path
from src.file_reader import FileReader, FileReaderError


class TestFileReader:
    """Tests pour la classe FileReader."""
    
    def test_read_valid_points_comma(self, tmp_path):
        """Test lecture de points valides avec virgule."""
        file_path = tmp_path / "points.txt"
        file_path.write_text("1,2\n3,4\n5,6\n")
        
        points = FileReader.read_points(str(file_path))
        
        assert len(points) == 3
        assert points[0] == (1.0, 2.0)
        assert points[1] == (3.0, 4.0)
        assert points[2] == (5.0, 6.0)
    
    def test_read_valid_points_semicolon(self, tmp_path):
        """Test lecture de points valides avec point-virgule."""
        file_path = tmp_path / "points.txt"
        file_path.write_text("1;2\n3;4\n5;6\n")
        
        points = FileReader.read_points(str(file_path))
        
        assert len(points) == 3
        assert points[0] == (1.0, 2.0)
    
    def test_read_points_with_decimals(self, tmp_path):
        """Test lecture de points avec décimales."""
        file_path = tmp_path / "points.txt"
        file_path.write_text("1.5,2.7\n3.14,4.28\n")
        
        points = FileReader.read_points(str(file_path))
        
        assert len(points) == 2
        assert points[0] == (1.5, 2.7)
        assert points[1] == (3.14, 4.28)
    
    def test_read_points_with_negative(self, tmp_path):
        """Test lecture de points avec coordonnées négatives."""
        file_path = tmp_path / "points.txt"
        file_path.write_text("-1.5,2.7\n3.14,-4.28\n-5,-6\n")
        
        points = FileReader.read_points(str(file_path))
        
        assert len(points) == 3
        assert points[0] == (-1.5, 2.7)
        assert points[2] == (-5.0, -6.0)
    
    def test_read_points_with_spaces(self, tmp_path):
        """Test lecture de points avec espaces."""
        file_path = tmp_path / "points.txt"
        file_path.write_text(" 1 , 2 \n  3  ,  4  \n")
        
        points = FileReader.read_points(str(file_path))
        
        assert len(points) == 2
        assert points[0] == (1.0, 2.0)
        assert points[1] == (3.0, 4.0)
    
    def test_read_points_with_comments(self, tmp_path):
        """Test lecture avec commentaires."""
        file_path = tmp_path / "points.txt"
        file_path.write_text("# Commentaire\n1,2\n# Autre commentaire\n3,4\n")
        
        points = FileReader.read_points(str(file_path))
        
        assert len(points) == 2
    
    def test_read_points_with_empty_lines(self, tmp_path):
        """Test lecture avec lignes vides."""
        file_path = tmp_path / "points.txt"
        file_path.write_text("1,2\n\n3,4\n\n\n5,6\n")
        
        points = FileReader.read_points(str(file_path))
        
        assert len(points) == 3
    
    def test_file_not_found(self):
        """Test avec fichier inexistant."""
        with pytest.raises(FileReaderError, match="n'existe pas"):
            FileReader.read_points("nonexistent.txt")
    
    def test_empty_file(self, tmp_path):
        """Test avec fichier vide."""
        file_path = tmp_path / "empty.txt"
        file_path.write_text("")
        
        with pytest.raises(FileReaderError, match="vide"):
            FileReader.read_points(str(file_path))
    
    def test_invalid_format(self, tmp_path):
        """Test avec format invalide."""
        file_path = tmp_path / "invalid.txt"
        file_path.write_text("1,2\ninvalid\n3,4\n")
        
        with pytest.raises(FileReaderError, match="format invalide"):
            FileReader.read_points(str(file_path))
    
    def test_validate_points_success(self):
        """Test validation de points valides (triangle)."""
    #    Points formant un triangle (non colinéaires)
        points = [(0, 0), (1, 0), (0, 1)]  # ✅ Points non colinéaires !
        FileReader.validate_points(points)  # Ne devrait pas lever d'exception
    
    def test_validate_points_too_few(self):
        """Test validation avec trop peu de points."""
        points = [(1, 2), (3, 4)]
        
        with pytest.raises(FileReaderError, match="Au moins 3 points"):
            FileReader.validate_points(points)
    
    def test_validate_points_duplicates(self):
        """Test validation avec doublons."""
        points = [(1, 2), (3, 4), (1, 2)]
        
        with pytest.raises(FileReaderError, match="dupliqué"):
            FileReader.validate_points(points)
    
    def test_validate_points_collinear(self):
        """Test validation avec points colinéaires."""
        points = [(0, 0), (1, 1), (2, 2), (3, 3)]
        
        with pytest.raises(FileReaderError, match="colinéaires"):
            FileReader.validate_points(points)
    
    def test_are_collinear_true(self):
        """Test détection de points colinéaires."""
        points = [(0, 0), (1, 1), (2, 2)]
        assert FileReader._are_collinear(points) is True
    
    def test_are_collinear_false(self):
        """Test détection de points non colinéaires."""
        points = [(0, 0), (1, 1), (2, 0)]
        assert FileReader._are_collinear(points) is False