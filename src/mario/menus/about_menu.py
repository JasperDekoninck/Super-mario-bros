from ..constants import *
from .button import TextButton
from .menu import Menu

class AboutMenu(Menu):
    """
    Menu wiht some information about the game, mainly on how to create a new world.
    """
    def __init__(self, screen):
        """
        Initializes the AboutMenu object.

        Args:
            screen: The pygame screen surface.

        Attributes:
            phrases (list): A list of strings representing the phrases to be displayed in the menu.
            buttons (list): A list of TextButton objects representing the buttons in the menu.
            main_button (TextButton): The main menu button.
        """
        
        super().__init__(screen)
        self.phrases = [
            "This game was made by Jasper Dekoninck.",
            "You can use the code for whatever you want, no permission is required.",
            "Most sprites are copied from http://www.mariouniverse.com/sprites-ds-nsmb/.",
            "",
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
        self.buttons = []
        y_pos = 10
        for phrase in self.phrases:
            self.buttons.append(TextButton((10, y_pos), phrase, FONT_STANDARD, pygame.Color("white")))
            y_pos += self.buttons[-1].size[1] + 2

        pos_main = (10, y_pos + self.buttons[-1].size[1] + 10)
        self.main_button = TextButton(pos_main, "Main menu", FONT_BIG, pygame.Color("white"), pygame.Color("red"))

    def render(self):
        """
        Renders the about menu on the screen.
        """
        for button in self.buttons:
            button.render(self.screen)
        self.main_button.render(self.screen)

    def loop(self):
        """
        Main loop for the about menu.

        This method continuously updates the screen, handles events, and checks for user input.
        It returns "main" if the main button is clicked.

        Returns:
            str: The next menu to be displayed.
        """
        self.time_after_creation = 0
        while True:
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            mouse_buttons = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()
            self.main_button.update_selected(pos)
            if mouse_buttons[0] and self.time_after_creation > 0.1:
                if self.main_button.selected:
                    return "main"

            self.render()
            get_fps = self.clock.get_fps()
            if get_fps != 0:
                self.time_after_creation += 1 / get_fps

            pygame.display.update()
