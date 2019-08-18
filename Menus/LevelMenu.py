from World import World
from CONSTANTS import *
from Menus.Button import TextButton


class LevelMenu:
    """
    A menu that shows all levels.
    """
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        # A variable registering how long the user has been in the menu. Not allowing anything to happen before
        # this variable gets to a certain size, makes sure it is not possible to accidently click and go two menus
        # further
        self.time_after_creation = 0
        self.clock = pygame.time.Clock()
        self.check_levels()

    def check_levels(self):
        """
        Loads all levels and creates buttons for each one of them.
        """
        self.buttons = []
        x_pos = 10
        y_pos = 10
        for i, file in enumerate(os.listdir("Worlds")):
            pos = (x_pos, y_pos)
            self.buttons.append(TextButton(pos, file, FONT_SMALL, pygame.Color("white"), pygame.Color("red")))
            x_pos += self.buttons[-1].size[0] + 10
            if x_pos + self.buttons[-1].size[0] > SCREEN_SIZE[0]:
                x_pos = 10
                y_pos = y_pos + self.buttons[-1].size[1] + 10

    def mouse_on_button(self, pos_mouse, pos_button, size_button):
        return pos_button[0] <= pos_mouse[0] <= pos_button[0] + size_button[0] and \
               pos_button[1] <= pos_mouse[1] <= pos_button[1] + size_button[1]

    def render(self):
        for button in self.buttons:
            button.render(self.screen)

    def loop(self):
        self.time_after_creation = 0
        self.check_levels()
        while True:
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            mouse_buttons = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.update_selected(pos)
            if mouse_buttons[0] and self.time_after_creation > 0.1:
                for button in self.buttons:
                    if button.selected:
                        path = os.path.join("Worlds", button.message)
                        return "play", World(load_file=path), path

            get_fps = self.clock.get_fps()
            if get_fps != 0:
                self.time_after_creation += 1 / get_fps

            self.render()
            pygame.display.update()