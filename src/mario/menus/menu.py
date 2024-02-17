import pygame

class Menu:
    """
    A menu, which can be used to create different menus in the game.
    """
    def __init__(self, screen):
        """
        Initializes a Menu object.

        Args:
            screen: The screen surface to render the menu on.
        """
        self.screen = screen
        self.time_after_creation = 0
        self.clock = pygame.time.Clock()

    def render(self):
        """
        Renders the menu.
        """
        raise NotImplementedError

    def loop(self):
        """
        The loop of the menu.
        """
        raise NotImplementedError