from ..world import World
from ..constants import *
from .button import TextButton
from .menu import Menu


class MainMenu(Menu):
    """
    Main menu
    """
    def __init__(self, screen):
        """
        Initializes the Main Menu object.

        Args:
            screen: The screen object to display the main menu on.
        """
        super(MainMenu, self).__init__(screen)
        # Loading the background world for the main menu
        self.background_world = World(load_file=os.path.join("Worlds", "MarioBros"))
        self.play_button = TextButton((10, 10), "Play game", FONT_BIG, pygame.Color("white"), pygame.Color("red"))
        self.level_button = TextButton((10, 60), "Level Creator", FONT_BIG, pygame.Color("white"), pygame.Color("red"))
        self.about_button = TextButton((10, 110), "About", FONT_BIG, pygame.Color("white"), pygame.Color("red"))
        self.settings_button = TextButton((10, 160), "Settings", FONT_BIG, pygame.Color("white"), pygame.Color("red"))

    def reset(self):
        """
        Resets the main menu by loading the background world from the specified file.
        """
        self.background_world = World(load_file=os.path.join("Worlds", "MarioBros"))

    def render(self):
        """
        Renders the main menu on the screen.
        """
        self.background_world.render(self.screen)
        self.play_button.render(self.screen)
        self.level_button.render(self.screen)
        self.about_button.render(self.screen)
        self.settings_button.render(self.screen)

    def loop(self):
        """
        Executes the main menu loop, handling user input and updating the display.
        
        Returns:
            str: The next state to transition to based on user input.
        """
        self.time_since_creation = 0
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            mouse_buttons = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()
            self.play_button.update_selected(pos)
            self.level_button.update_selected(pos)
            self.about_button.update_selected(pos)
            self.settings_button.update_selected(pos)
            if mouse_buttons[0] and self.time_since_creation > 0.1:
                if self.play_button.selected:
                    return "level"
                elif self.level_button.selected:
                    return "creator"
                elif self.about_button.selected:
                    return "about"
                elif self.settings_button.selected:
                    return "settings"

            self.render()
            get_fps = self.clock.get_fps()
            if get_fps != 0:
                # this small line allows a user to play the game in the main menu!
                self.background_world.update(1 / get_fps)
                self.time_since_creation += 1 / get_fps

            pygame.display.update()
