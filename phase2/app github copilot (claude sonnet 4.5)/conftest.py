"""
Configuration pytest pour les tests.
"""

import matplotlib
import pytest

# Configurer matplotlib pour utiliser un backend non-interactif
matplotlib.use('Agg')

# Importer pyplot après avoir configuré le backend
import matplotlib.pyplot as plt


@pytest.fixture(autouse=True)
def cleanup_matplotlib():
    """Nettoie les figures matplotlib après chaque test."""
    yield
    plt.close('all')