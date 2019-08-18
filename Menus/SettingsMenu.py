from CONSTANTS import *
from Menus.Button import TextButton


class SettingsMenu:
    """
    Menu to adjust settings.
    """
    SETTINGS = {
        "Music": "on",
        "Sound": "on"
    }

    def __init__(self, screen):
        self.screen = screen
        self.settings_button = TextButton((10, 10), "Settings", FONT_BIG, pygame.Color("White"))
        self.options = dict()
        self.position = [10, 70]
        self.load_options()
        self.main_button = TextButton(self.position, "Main menu", FONT_BIG, pygame.Color("white"), pygame.Color("red"))
        self.clock = pygame.time.Clock()

        # A variable registering how long the user has been in the menu. Not allowing anything to happen before
        # this variable gets to a certain size, makes sure it is not possible to accidently click and go two menus
        # further
        self.time_after_creation = 0

    def load_options(self):
        """
        Loads all options from the settings file.
        """
        with open(os.path.join("Menus", "settings"), "r") as file:
            for line in file.read().splitlines():
                option_name, different_options = line.split(":")
                different_options, selected_option = different_options.split(" | ")
                different_options = different_options.split(" ")
                selected_option = selected_option.replace(" ", "")
                self.options[option_name] = [
                    TextButton(self.position[:], option_name + ": ", FONT_MEDIUM, pygame.Color("white")),
                ]
                SettingsMenu.SETTINGS[option_name] = selected_option
                current_pos = self.position[:]
                for option in different_options:
                    current_pos[0] += 10 + self.options[option_name][-1].size[0]
                    self.options[option_name].append(TextButton(current_pos[:], option, FONT_MEDIUM, pygame.Color("white"),
                                                                pygame.Color("red")))
                    if option == selected_option:
                        self.options[option_name][-1].selected = True

                self.position[1] += self.options[option_name][0].size[1] + 10

    def save_options(self):
        with open(os.path.join("Menus", "settings"), "w") as f:
            for option_name in self.options:
                string_option = option_name + ":"
                selected_option = None
                for option in self.options[option_name][1:]:
                    string_option += option.message + " "
                    if option.selected:
                        selected_option = option.message
                string_option += "| " + selected_option + "\n"
                f.write(string_option)

    def render(self):
        self.settings_button.render(self.screen)
        self.main_button.render(self.screen)
        for option_name in self.options:
            for button in self.options[option_name]:
                button.render(self.screen)

    def update_options(self):
        pos = pygame.mouse.get_pos()
        for option in self.options:
            for button in self.options[option][1:]:
                if button.is_selected(pos) and not button.selected:
                    for button2 in self.options[option][1:]:
                        button2.selected = False
                    button.selected = True
                    SettingsMenu.SETTINGS[option] = button.message
                self.save_options()

    def loop(self):
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
                self.update_options()

                if self.main_button.selected:
                    return "main"

            if SettingsMenu.SETTINGS["Music"] == "off":
                mixer.music.pause()
            elif SettingsMenu.SETTINGS["Music"] == "on":
                mixer.music.unpause()

            get_fps = self.clock.get_fps()
            if get_fps != 0:
                self.time_after_creation += 1 / get_fps

            self.render()

            pygame.display.update()