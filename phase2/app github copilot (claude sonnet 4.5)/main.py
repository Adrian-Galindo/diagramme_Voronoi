#!/usr/bin/env python3
"""
Point d'entrée principal de l'application de génération de diagrammes de Voronoï.
"""

import sys
from src.cli import CLI


def main() -> int:
    """
    Fonction principale.
    
    Returns:
        Code de sortie du programme
    """
    cli = CLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())