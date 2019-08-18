from World import World
from CONSTANTS import *
from Menus.Button import TextButton


class MainMenu:
    """
    Main menu
    """
    def __init__(self, screen):
        self.screen = screen
        # Loading the background world for the main menu
        self.background_world = World(load_file=os.path.join("Worlds", "MarioBros"))
        self.play_button = TextButton((10, 10), "Play game", FONT_BIG, pygame.Color("white"), pygame.Color("red"))
        self.level_button = TextButton((10, 60), "Level Creator", FONT_BIG, pygame.Color("white"), pygame.Color("red"))
        self.about_button = TextButton((10, 110), "About", FONT_BIG, pygame.Color("white"), pygame.Color("red"))
        self.settings_button = TextButton((10, 160), "Settings", FONT_BIG, pygame.Color("white"), pygame.Color("red"))
        self.clock = pygame.time.Clock()
        self.time_since_creation = 0

    def reset(self):
        self.background_world = World(load_file=os.path.join("Worlds", "MarioBros"))

    def render(self):
        self.background_world.render(self.screen)
        self.play_button.render(self.screen)
        self.level_button.render(self.screen)
        self.about_button.render(self.screen)
        self.settings_button.render(self.screen)

    def loop(self):
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