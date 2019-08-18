from CONSTANTS import *
from Menus.Button import TextButton


class GameOverMenu:
    """
    Menu for when the player dies or wins the level.
    """
    def __init__(self, screen):
        self.screen = screen
        self.report_button = TextButton((10, 10), "You won!", FONT_BIG, pygame.Color("White"))
        self.play_button = TextButton((10, 70), "Play again", FONT_BIG, pygame.Color("white"), pygame.Color("red"))
        self.main_button = TextButton((10, 130), "Main menu", FONT_BIG, pygame.Color("white"), pygame.Color("red"))
        self.clock = pygame.time.Clock()

        # A variable registering how long the user has been in the menu. Not allowing anything to happen before
        # this variable gets to a certain size, makes sure it is not possible to accidently click and go two menus
        # further
        self.time_after_creation = 0

    def render(self, world):
        world.render(self.screen)
        self.report_button.render(self.screen)
        self.play_button.render(self.screen)
        self.main_button.render(self.screen)

    def mouse_update(self):
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