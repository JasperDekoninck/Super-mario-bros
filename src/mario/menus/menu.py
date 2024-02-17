import pygame

class Menu:
    """
    A menu, which can be used to create different menus in the game.
    """
    def __init__(self, screen):
        self.screen = screen
        # A variable registering how long the user has been in the menu. Not allowing anything to happen before
        # this variable gets to a certain size, makes sure it is not possible to accidently click and go two menus
        # further
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