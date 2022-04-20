from typing import Callable, Any
import pygame
import time
import kelvin452.systems as systems


class Game:
    """
    Représente l'état du jeu et gère les systèmes du jeu.
    """

    def __init__(self):
        pygame.init()
        uninitialized: Any = None
        self.renderer: systems.RenderingSystem = uninitialized
        "Le système de rendu, qui gère les sprites à mettre sur l'écran"
        self.world: systems.WorldSystem = uninitialized
        "Le système du monde, qui gère les entités présentes à l'écran"
        self.on_start_funcs = []
        self.delta_time = 1 / 60  # assume some start time
        "Le temps (en secondes) passé entre la frame précédente et la frame actuelle."

    def initialize_game(self):
        """
        Initialise les systèmes du jeu.
        """
        self.renderer = systems.RenderingSystem()
        self.world = systems.WorldSystem()

    def on_start(self, func: Callable):
        """Ajoute une fonction à lancer lorsque le jeu commence.

        Args:
            func (Callable): La fonction à lancer
        """
        self.on_start_funcs.append(func)

    def start(self):
        """
        Lance le jeu avec la boucle initiale de pygame.
        Appelle les fonctions on_start. 
        """
        pygame.display.set_caption("Kelvin 452")
        # Fênetre 1280x720
        screen = pygame.display.set_mode((1280, 720))

        for start_func in self.on_start_funcs:
            start_func()

        # Boucle du jeu
        running = True
        while running:
            start_time = time.time_ns()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.world.tick() # Lancer le tick des entités
            self.renderer.render(screen) # Faire le rendu des sprites.
            
            # Met à jour le delta time (conversion de nanosecondes en secondes)
            self.delta_time = (time.time_ns() - start_time) / 1_000_000_000

            # Écrire les FPS dans la console
            ms_elapsed = self.delta_time * 1000
            print(f"frame ms: {ms_elapsed :.2f}ms ({1000 / ms_elapsed:.1f} FPS)")

    @property
    def viewport(self):
        """Retourne un tuple avec les dimensions de la fenêtre.

        Returns:
            (int, int): Les dimensions de la fenêtre en pixels, largeur x hauteur
        """
        return pygame.display.get_window_size()


game = Game()
