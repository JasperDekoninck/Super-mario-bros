from ..constants import *
from .button import TextButton
from .menu import Menu

class GameOverMenu(Menu):
    """
    Menu for when the player dies or wins the level.
    """
    def __init__(self, screen):
        """
        Initializes a GameOverMenu object.

        Args:
            screen: The screen surface to render the menu on.

        Attributes:
            report_button: A TextButton object representing the "You won!" button.
            play_button: A TextButton object representing the "Play again" button.
            main_button: A TextButton object representing the "Main menu" button.
        """
        super(GameOverMenu, self).__init__(screen)
        self.report_button = TextButton((10, 10), "You won!", FONT_BIG, pygame.Color("White"))
        self.play_button = TextButton((10, 70), "Play again", FONT_BIG, pygame.Color("white"), pygame.Color("red"))
        self.main_button = TextButton((10, 130), "Main menu", FONT_BIG, pygame.Color("white"), pygame.Color("red"))

    def render(self, world):
        """
        Renders the game over menu on the screen.

        Args:
            world: The game world to render.

        Returns:
            None
        """
        world.render(self.screen)
        self.report_button.render(self.screen)
        self.play_button.render(self.screen)
        self.main_button.render(self.screen)

    def mouse_update(self):
        """
        Updates the state of the mouse and handles button clicks.

        Returns:
            str: The action to be performed based on the button clicked.
                    Possible values are "level" or "main".
                    Returns None if no button is clicked.
        """
        mouse_buttons = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        self.play_button.update_selected(pos)
        self.main_button.update_selected(pos)
        if mouse_buttons[0] and self.time_after_creation > 0.1:
            if self.play_button.selected:
                return "level"
            elif self.main_button.selected:
                return "main"

        return None

    def loop(self, world):
        """
        Main loop for the game over menu.

        Args:
            world: The game world object.

        Returns:
            The selected menu option.
        """
        self.time_after_creation = 0
        if not world.won:
            self.report_button.set_text("You lost")
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            selected_menu = self.mouse_update()
            if selected_menu is not None:
                return selected_menu

            get_fps = self.clock.get_fps()
            if get_fps != 0:
                self.time_after_creation += 1 / get_fps

            self.render(world)
            pygame.display.update()