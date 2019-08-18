from CONSTANTS import *


class AboutMenu:
    """
    Menu wiht some information about the game, mainly on how to create a new world.
    """
    def __init__(self, screen):
        self.screen = screen
        self.phrases = [
            "This game was made by Jasper Dekoninck.",
            "You can use the code for whatever you want, no permission is required.",
            "Most sprites are copied from http://www.mariouniverse.com/sprites-ds-nsmb/.",
            "",
            "A small guide for the creation of new levels is probably required.",
            "If you click on 'Level Creator' in main menu, you will be able to create new worlds yourself.",
            "Just follow the steps, when you're doing the actual creating, you can do the following things:",
            "1. Select a game object at the right side by pressing your left mouse button on it.",
            "     Once selected, you can place the game object in your world by again pressing the left mouse button.",
            "     You can create multiple instances of the same object by keeping the mouse pressed.",
            "2. You can delete game objects by clicking on them with your right mouse button.",
            "3. You can move the screen up / down / left / right by using the arrow keys.",
            "4. You can play your world in creation by pressing the escape key.",
            "     If you press the key again, you stop playing.",
            "You can save your world by pressing enter."
        ]
        self.texts = []
        self.pos = []
        y_pos = 10
        for phrase in self.phrases:
            text = FONT_STANDARD.render(phrase, True, pygame.Color("white"))
            self.texts.append(text)
            self.pos.append((10, y_pos))
            y_pos += self.texts[-1].get_size()[1] + 2

        self.main_text = FONT_BIG.render("Main Menu", True, pygame.Color("White"))
        self.size_main = self.main_text.get_size()
        self.pos_main = (10, y_pos + self.texts[-1].get_size()[1] + 10)

        # A variable registering how long the user has been in the menu. Not allowing anything to happen before
        # this variable gets to a certain size, makes sure it is not possible to accidently click and go two menus
        # further
        self.time_after_creation = 0
        self.clock = pygame.time.Clock()

    def render(self):
        for pos, text in zip(self.pos, self.texts):
            self.screen.blit(text, pos)

        self.screen.blit(self.main_text, self.pos_main)

    def mouse_on_button(self, pos_mouse, pos_button, size_button):
        return pos_button[0] <= pos_mouse[0] <= pos_button[0] + size_button[0] and \
               pos_button[1] <= pos_mouse[1] <= pos_button[1] + size_button[1]

    def loop(self):
        self.time_after_creation = 0
        while True:
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0] and self.time_after_creation > 0.1:
                pos = pygame.mouse.get_pos()
                if self.mouse_on_button(pos, self.pos_main, self.size_main):
                    return "main"

            self.render()
            get_fps = self.clock.get_fps()
            if get_fps != 0:
                self.time_after_creation += 1 / get_fps

            pygame.display.update()
