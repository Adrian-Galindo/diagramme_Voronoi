"""
Module d'interface en ligne de commande.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .file_reader import FileReader, FileReaderError
from .voronoi import VoronoiGenerator, VoronoiError
from .visualizer import VoronoiVisualizer, VisualizerError


class CLI:
    """
    Interface en ligne de commande pour le générateur de diagrammes de Voronoï.
    """
    
    def __init__(self):
        """Initialise l'interface CLI."""
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Crée le parser d'arguments en ligne de commande.
        
        Returns:
            ArgumentParser configuré
        """
        parser = argparse.ArgumentParser(
            description="Générateur de diagrammes de Voronoï",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Exemples d'utilisation :
  python main.py --input points.txt
  python main.py --input points.txt --output diagram.svg
  python main.py --input points.txt --output diagram.png --width 1920 --height 1080
  python main.py --input points.txt --no-show --output result.png
            """
        )
        
        parser.add_argument(
            '-i', '--input',
            type=str,
            help="Chemin vers le fichier d'entrée contenant les points"
        )
        
        parser.add_argument(
            '-o', '--output',
            type=str,
            help="Chemin du fichier de sortie (SVG, PNG ou JPG)"
        )
        
        parser.add_argument(
            '--width',
            type=int,
            default=10,
            help="Largeur de la figure en pouces (défaut: 10)"
        )
        
        parser.add_argument(
            '--height',
            type=int,
            default=10,
            help="Hauteur de la figure en pouces (défaut: 10)"
        )
        
        parser.add_argument(
            '--dpi',
            type=int,
            default=300,
            help="Résolution en DPI pour PNG/JPG (défaut: 300)"
        )
        
        parser.add_argument(
            '--no-show',
            action='store_true',
            help="Ne pas afficher le graphique (utile pour l'export uniquement)"
        )
        
        parser.add_argument(
            '--no-points',
            action='store_true',
            help="Ne pas afficher les points générateurs"
        )
        
        parser.add_argument(
            '--show-vertices',
            action='store_true',
            help="Afficher les sommets du diagramme"
        )
        
        parser.add_argument(
            '--point-color',
            type=str,
            default='red',
            help="Couleur des points (défaut: red)"
        )
        
        parser.add_argument(
            '--line-color',
            type=str,
            default='blue',
            help="Couleur des lignes (défaut: blue)"
        )
        
        parser.add_argument(
            '--stats',
            action='store_true',
            help="Afficher les statistiques du diagramme"
        )
        
        return parser
    
    def run(self, args: Optional[list] = None) -> int:
        """
        Exécute l'application CLI.
        
        Args:
            args: Liste d'arguments (None pour utiliser sys.argv)
            
        Returns:
            Code de sortie (0 = succès, 1 = erreur)
        """
        parsed_args = self.parser.parse_args(args)
        
        # Mode interactif si aucun fichier spécifié
        if not parsed_args.input:
            return self._interactive_mode()
        
        # Mode ligne de commande
        return self._command_mode(parsed_args)
    
    def _interactive_mode(self) -> int:
        """
        Mode interactif pour entrer le chemin du fichier.
        
        Returns:
            Code de sortie
        """
        print("╔════════════════════════════════════════════════════════════╗")
        print("║     Générateur de Diagrammes de Voronoï - Mode Interactif ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        
        # Demander le chemin du fichier
        file_path = input("Entrez le chemin du fichier de points : ").strip()
        
        if not file_path:
            print("❌ Aucun fichier spécifié.")
            return 1
        
        # Demander le chemin de sortie (optionnel)
        output_path = input("Chemin de sortie (optionnel, Entrée pour ignorer) : ").strip()
        output_path = output_path if output_path else None
        
        # Créer un objet args simulé
        class Args:
            input = file_path
            output = output_path
            width = 10
            height = 10
            dpi = 300
            no_show = False
            no_points = False
            show_vertices = False
            point_color = 'red'
            line_color = 'blue'
            stats = True  # Toujours afficher les stats en mode interactif
        
        return self._command_mode(Args())
    
    def _command_mode(self, args) -> int:
        """
        Exécute le traitement en mode ligne de commande.
        
        Args:
            args: Arguments parsés
            
        Returns:
            Code de sortie
        """
        try:
            # Lecture du fichier
            print(f"\n📂 Lecture du fichier : {args.input}")
            points = FileReader.read_points(args.input)
            print(f"✓ {len(points)} points chargés")
            
            # Validation
            print("🔍 Validation des points...")
            FileReader.validate_points(points)
            print("✓ Points valides")
            
            # Calcul du diagramme
            print("🔧 Calcul du diagramme de Voronoï...")
            generator = VoronoiGenerator(points)
            voronoi = generator.compute()
            print("✓ Diagramme calculé")
            
            # Statistiques
            if args.stats:
                self._print_statistics(generator)
            
            # Visualisation
            print("🎨 Création de la visualisation...")
            visualizer = VoronoiVisualizer(voronoi)
            visualizer.create_plot(
                figsize=(args.width, args.height),
                show_points=not args.no_points,
                show_vertices=args.show_vertices,
                point_color=args.point_color,
                line_color=args.line_color
            )
            print("✓ Visualisation créée")
            
            # Sauvegarde
            if args.output:
                print(f"💾 Sauvegarde du diagramme...")
                visualizer.save(args.output, dpi=args.dpi)
            
            # Affichage
            if not args.no_show:
                print("👁  Affichage du diagramme...")
                visualizer.show()
            else:
                visualizer.close()
            
            print("\n✅ Traitement terminé avec succès !")
            return 0
            
        except (FileReaderError, VoronoiError, VisualizerError) as e:
            print(f"\n❌ Erreur : {e}", file=sys.stderr)
            return 1
        except KeyboardInterrupt:
            print("\n\n⚠️  Opération annulée par l'utilisateur.")
            return 1
        except Exception as e:
            print(f"\n❌ Erreur inattendue : {e}", file=sys.stderr)
            return 1
    
    def _print_statistics(self, generator: VoronoiGenerator) -> None:
        """
        Affiche les statistiques du diagramme.
        
        Args:
            generator: Générateur de Voronoï avec diagramme calculé
        """
        stats = generator.get_statistics()
        
        print("\n" + "="*60)
        print("📊 STATISTIQUES DU DIAGRAMME")
        print("="*60)
        print(f"Nombre de points        : {stats['num_points']}")
        print(f"Nombre de sommets       : {stats['num_vertices']}")
        print(f"Nombre de régions       : {stats['num_regions']}")
        print(f"  - Régions bornées     : {stats['num_bounded_regions']}")
        print(f"  - Régions non bornées : {stats['num_unbounded_regions']}")
        
        bounds = stats['points_bounds']
        print(f"\nLimites des points :")
        print(f"  X : [{bounds['x_min']:.2f}, {bounds['x_max']:.2f}]")
        print(f"  Y : [{bounds['y_min']:.2f}, {bounds['y_max']:.2f}]")
        print("="*60 + "\n")