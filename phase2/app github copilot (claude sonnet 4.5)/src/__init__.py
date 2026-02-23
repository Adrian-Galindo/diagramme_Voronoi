"""
Générateur de Diagrammes de Voronoï

Package Python pour la génération et la visualisation de diagrammes de Voronoï.
"""

__version__ = "1.0.0"
__author__ = "Maxime-LointierDéveloppe"

from .file_reader import FileReader, FileReaderError
from .voronoi import VoronoiGenerator, VoronoiError
from .visualizer import VoronoiVisualizer, VisualizerError
from .cli import CLI

__all__ = [
    "FileReader",
    "FileReaderError",
    "VoronoiGenerator",
    "VoronoiError",
    "VoronoiVisualizer",
    "VisualizerError",
    "CLI",
]