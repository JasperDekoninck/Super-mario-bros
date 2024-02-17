from ..enemies import *
from ..player import *
from ..tiles import *
from ..world import World
from .level_menu import LevelMenu
from .play_menu import PlayMenu
from ..specials import *
from .button import ImageButton, TextButton
from .menu import Menu


class QuestionScreen(Menu):
    """
    A screen that poses a question to the user, the question can have two answers or the answer can be the input
    of the user.
    """
    def __init__(self, screen, question, answer1=None, answer2=None):
        super(QuestionScreen, self).__init__(screen)

        pos_question = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3)
        self.question_button = TextButton(pos_question, question, FONT_SMALL, pygame.Color("white"), center_pos=True)
        self.answer1_button = None
        self.answer2_button = None
        self.answer_button = None
        if answer1 is not None:
            pos = (SCREEN_SIZE[0] // 2 - 130, SCREEN_SIZE[1] // 3 + 50)
            self.answer1_button = TextButton(pos, answer1, FONT_BIG, pygame.Color("white"), pygame.Color("red"),
                                             center_pos=True)
            pos = (SCREEN_SIZE[0] // 2 + 130, SCREEN_SIZE[1] // 3 + 50)
            self.answer2_button = TextButton(pos, answer2, FONT_BIG, pygame.Color("white"), pygame.Color("red"),
                                             center_pos=True)
        else:
            pos = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3 + 50)
            self.answer_button = TextButton(pos, "", FONT_BIG, pygame.Color("white"), center_pos=True)

    def render(self):
        self.question_button.render(self.screen)
        if self.answer_button is not None:
            self.answer_button.render(self.screen)
        else:
            self.answer1_button.render(self.screen)
            self.answer2_button.render(self.screen)

    def answer_update(self, event):
        if event.type == pygame.KEYDOWN and self.answer_button is not None:
            if event.key == pygame.K_BACKSPACE:
                if len(self.answer_button.message) > 0:
                    self.answer_button.set_text(self.answer_button.message[:-1])
            elif event.key == pygame.K_RETURN:
                return self.answer_button.message
            else:
                self.answer_button.set_text(self.answer_button.message + event.unicode)

        return None

    def mouse_update(self):
        mouse_buttons = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        if self.answer1_button is not None:
            self.answer1_button.update_selected(pos)
            self.answer2_button.update_selected(pos)
        if mouse_buttons[0] and self.time_after_creation > 0.1 and self.answer1_button is not None:
            if self.answer1_button.selected:
                return self.answer1_button.message
            elif self.answer2_button.selected:
                return self.answer2_button.message

        return None

    def loop(self):
        self.time_after_creation = 0
        while True:
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                answer = self.answer_update(event)
                if answer is not None:
                    return answer

            selected_answer = self.mouse_update()
            if selected_answer is not None:
                return selected_answer

            get_fps = self.clock.get_fps()
            if get_fps != 0:
                self.time_after_creation += 1 / get_fps

            self.render()
            pygame.display.update()


class BackgroundSelectScreen(Menu):
    """
    Selection of the background screen, asks which background the user wants and shows all possibilities
    """
    def __init__(self, screen):
        super(BackgroundSelectScreen, self).__init__(screen)
        self.question_button = TextButton((SCREEN_SIZE[0] // 2, 10), "What background do you want?", FONT_MEDIUM,
                                          pygame.Color("white"), center_pos=True)
        self.n_backgrounds = len(BACKGROUNDS)
        self.n_backgrounds_row = 4
        self.start_first_row = 100
        self.camera_pos = np.zeros(2)
        self.background_buttons = []
        self.background_size = 2 * (SCREEN_SIZE[0] // self.n_backgrounds_row - 3,)
        for i, background in enumerate(BACKGROUNDS):
            pos = ((self.background_size[0] + 3) * (i % self.n_backgrounds_row),
                   (self.background_size[1] + 3) * (i // self.n_backgrounds_row) + self.start_first_row)
            image = pygame.transform.scale(BACKGROUNDS[background], self.background_size)
            self.background_buttons.append(ImageButton(pos, image, background))

    def render(self):
        self.question_button.render(self.screen, self.camera_pos)
        for button in self.background_buttons:
            button.render(self.screen, self.camera_pos)

    def handle_mouse(self):
        mouse_buttons = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos() + self.camera_pos
        for button in self.background_buttons:
            button.update_selected(pos)
        if mouse_buttons[0] and self.time_after_creation > 0.1:
            for button in self.background_buttons:
                if button.selected:
                    return button.description
        return None

    def loop(self):
        self.time_after_creation = 0
        while True:
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.camera_pos[1] = np.maximum(self.camera_pos[1] - 30, 0)
                    elif event.button == 5:
                        self.camera_pos[1] += 30

            clicked = self.handle_mouse()
            if clicked is not None:
                return clicked

            get_fps = self.clock.get_fps()
            if get_fps != 0:
                self.time_after_creation += 1 / get_fps

            self.render()
            pygame.display.update()


class ChangeScreen(Menu):
    """
    This screen is where the actual changing happens: here a user can change a world to his / her liking.
    """
    def __init__(self, screen, world=None):
        super(ChangeScreen, self).__init__(screen)
        self.world = world

        # The information menu at the right shows all possible objects the user can add.
        # There are different tabs (teh user can change tabs by clicking on arrow1 or arrow2)
        self.size_information = (400, SCREEN_SIZE[1])
        self.pos_information = (SCREEN_SIZE[0] - self.size_information[0], 0)
        self.camera_pos = - np.array(self.pos_information)
        self.tab = 0
        # Once the user selects a class, the current class will be stored in this variable, as soon
        # as the user once again clicks, an instance will be created
        self.current_class = None

        # The two arrows for changing tabs
        self.arrow1_pos = (self.pos_information[0] + self.size_information[0] // 2 - 20, 10)
        self.arrow1_size = (20, 20)
        self.points_arrow1 = [
            (self.arrow1_pos[0], self.arrow1_pos[1] + self.arrow1_size[1] // 2),
            (self.arrow1_pos[0] + self.arrow1_size[0], self.arrow1_pos[1]),
            (self.arrow1_pos[0] + self.arrow1_size[0], self.arrow1_pos[1] + self.arrow1_size[1])
        ]
        self.arrow2_pos = (self.pos_information[0] + self.size_information[0] // 2 + 20, 10)
        self.arrow2_size = (20, 20)
        self.points_arrow2 = [
            (self.arrow2_pos[0] + self.arrow2_size[0], self.arrow2_pos[1] + self.arrow1_size[1] // 2),
            (self.arrow2_pos[0], self.arrow2_pos[1]),
            (self.arrow2_pos[0], self.arrow2_pos[1] + self.arrow2_size[1])
        ]

        # Loading in all different tiles for the tile tab
        self.tiles = [
            MysteryBox((15, 45), color="yellow", autoset=False),
            MysteryBox((35, 45), color="red", autoset=False),
            MysteryBox((55, 45), color="blue", autoset=False),
        ]

        # adding all tiles
        x_pos = 75
        y_pos = 45
        for tilename in TILES:
            self.tiles.append(NormalTile((x_pos, y_pos), tilename, autoset=False))
            x_pos += TILE_SIZE[0] + 5
            if x_pos + TILE_SIZE[0] + 5 >= self.size_information[0]:
                x_pos = TILE_SIZE[0]
                y_pos += TILE_SIZE[0] + 5

        # Loading all enemies and players
        self.enemies_and_player = [
            Mario((15, 45)),
            Goomba((40, 45), dir=1),
            Goomba((65, 45), dir=-1),
            KoopaTroopa((90, 45), dir=1, color="blue"),
            KoopaTroopa((115, 45), dir=-1, color="blue"),
            KoopaTroopa((140, 45), dir=1, color="red"),
            KoopaTroopa((165, 45), dir=-1, color="red"),
            KoopaTroopa((190, 45), dir=1, color="green"),
            KoopaTroopa((215, 45), dir=-1, color="green"),
        ]

        # Loading all special types
        self.specials = [
            Flagpole((15, 45)),
            Mushroom((90, 45), color="red"),
            Mushroom((120, 45), color="blue"),
            BackgroundSprites((150, 45), "big bush", size=(60, 30)),
            BackgroundSprites((220, 45), "small bush 1", size=(35, 30)),
            BackgroundSprites((260, 45), "small bush 2", size=(35, 25)),
            BackgroundSprites((300, 45), "flower 1", size=(27, 30)),
            BackgroundSprites((90, 95), "flower 2", size=(30, 30)),
            BackgroundSprites((130, 95), "flower 3", size=(30, 22)),
            BackgroundSprites((170, 95), "mushroom", size=(36, 12)),
            BackgroundSprites((210, 95), "fence", size=(35, 20)),
            BackgroundSprites((250, 95), "castle", size=(100, 100)),
            Coin((90, 135), autoset=False),
            BackgroundSprites((90, 170), "cloud", size=(85, 35))

        ]

        # Loading different size of pipes
        self.pipes = [
            Pipe((15, 45), (3, 2), 0, autoset=False),
            Pipe((70, 45), (6, 2), 0, autoset=False),
            Pipe((170, 45), (6, 3), 0, autoset=False),
            Pipe((270, 45), (7, 3), 0, autoset=False),
            Pipe((15, 225), (2, 3), 1, autoset=False),
            Pipe((55, 225), (2, 6), 1, autoset=False),
            Pipe((95, 225), (3, 6), 1, autoset=False),
            Pipe((150, 225), (3, 7), 1, autoset=False),
            Pipe((15, 130), (3, 2), 2, autoset=False),
            Pipe((70, 130), (6, 2), 2, autoset=False),
            Pipe((170, 130), (6, 3), 2, autoset=False),
            Pipe((270, 130), (7, 3), 2, autoset=False),
            Pipe((200, 225), (2, 3), 3, autoset=False),
            Pipe((240, 225), (2, 6), 3, autoset=False),
            Pipe((280, 225), (3, 6), 3, autoset=False),
            Pipe((330, 225), (3, 7), 3, autoset=False),
            Pipe((15, 340), (4, 3), 1, autoset=False),
            Pipe((85, 340), (3, 2), 1, autoset=False),
            Pipe((140, 340), (4, 6), 1, autoset=False)
        ]

        # A variable registering how long the user has been in the tab. Not allowing anything to happen before
        # this variable gets to a certain size, makes sure it is not possible to accidently click and go two tabs
        # further
        self.time_since_selected_new_tab = 9999

        self.tabs = [self.tiles, self.enemies_and_player, self.specials, self.pipes]

        self.play_screen = PlayMenu(self.screen)

    def render_grid(self):
        """renders the gridlines such that it easier to see for the player what he / she is doing"""
        for i in range(-self.world.camera_pos[0].astype(np.int32) % TILE_SIZE[0], self.pos_information[0], TILE_SIZE[0]):
            pygame.draw.line(self.screen, pygame.Color("black"), (i, 0), (i, SCREEN_SIZE[1]))
        for j in range(-self.world.camera_pos[1].astype(np.int32) % TILE_SIZE[1], SCREEN_SIZE[1], TILE_SIZE[1]):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, j), (self.pos_information[0], j))

    def render(self):
        """Renders the screen, including the grid, the world and the sidebar information with its game objects"""
        self.world.render(self.screen, fast=False)
        self.render_grid()
        pygame.draw.rect(self.screen, pygame.Color("grey"), self.pos_information + self.size_information)
        pygame.draw.polygon(self.screen, pygame.Color("black"), self.points_arrow1)
        pygame.draw.polygon(self.screen, pygame.Color("black"), self.points_arrow2)
        for game_object in self.tabs[self.tab]:
            game_object.render(self.screen, self.camera_pos)

    def mouse_on_button(self, pos_mouse, pos_button, size_button):
        return pos_button[0] <= pos_mouse[0] <= pos_button[0] + size_button[0] and \
               pos_button[1] <= pos_mouse[1] <= pos_button[1] + size_button[1]

    def game_object_at_pos(self, pos):
        """
        Checks whether or not there is a game object at the position selected
        """
        for game_object in self.world.get_all_game_objects():
            if self.mouse_on_button(pos, game_object.pos, game_object.size):
                return game_object

        return None

    def tab_change(self):
        # Changing tabs if player clicks on arrows
        pos = pygame.mouse.get_pos()
        if self.mouse_on_button(pos, self.arrow1_pos, self.arrow1_size) and \
                self.time_since_selected_new_tab > 0.1:
            self.tab = (self.tab - 1) % len(self.tabs)
            self.time_since_selected_new_tab = 0
        elif self.mouse_on_button(pos, self.arrow2_pos, self.arrow2_size) and \
                self.time_since_selected_new_tab > 0.1:
            self.time_since_selected_new_tab = 0
            self.tab = (self.tab + 1) % len(self.tabs)

    def create_new_gameobject(self):
        pos = pygame.mouse.get_pos()
        if pos[0] < self.pos_information[0]:  # only allowing new creations if the mouse is in the world
            # and not on the sidebar
            pos = np.array(pos).astype(np.int32) + self.world.camera_pos
            if self.game_object_at_pos(pos) is None and self.current_class is not None:
                input_parameters = self.current_class[1]
                input_parameters = (pos,) + input_parameters[1:]
                game_object = self.current_class[0](*input_parameters)
                try:
                    if self.world.allowed_game_object(game_object):
                        self.world.add_gameobject(game_object)
                        game_object.check_collision_update("vertical")
                        game_object.check_collision_update("horizontal")
                        game_object.input_parameters = (game_object.pos,) + game_object.input_parameters[1:]
                except ValueError:  # you can't add an invalid object
                    pass

    def handle_mouse(self):
        """
        Handles the clicks of the mouse
        """
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.time_after_creation > 0.1:
            pos = pygame.mouse.get_pos()
            for game_object in self.tabs[self.tab]:
                if self.mouse_on_button(pos, game_object.pos - self.camera_pos, game_object.size):
                    self.current_class = (game_object.__class__, game_object.input_parameters)

            self.tab_change()
            self.create_new_gameobject()

        # deleting a game object at the given position
        elif mouse_buttons[2] and self.time_after_creation > 0.1:
            pos = pygame.mouse.get_pos() + self.world.camera_pos
            game_object = self.game_object_at_pos(pos)
            if game_object is not None:
                self.world.remove_gameobject(game_object)

    def handle_keys(self):
        """
        Handle keys such that the user is able to move through his world.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.world.camera_pos[0] = np.maximum(0, self.world.camera_pos[0] - 5)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.world.camera_pos[0] = np.minimum(self.world.size[0] - self.pos_information[0],
                                                  self.world.camera_pos[0] + 5)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.world.camera_pos[1] = np.maximum(0, self.world.camera_pos[1] - 5)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.world.camera_pos[1] = np.minimum(self.world.size[1] - SCREEN_SIZE[1],
                                                  self.world.camera_pos[1] + 5)

    def loop(self):
        self.time_after_creation = 0
        while True:
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.world
                    if event.key == pygame.K_ESCAPE:
                        # if the player wants to play in his world, first save the current world, then play
                        # and then load the world again (if movement happens while playing the game, this movement
                        # is reset)
                        self.world.save(os.path.join("TempWorlds", "TempWorld"))
                        self.world.surface = None
                        self.play_screen.loop(self.world)
                        self.world.load(os.path.join("TempWorlds", "TempWorld"))

            self.handle_mouse()
            self.handle_keys()
            get_fps = self.clock.get_fps()
            if get_fps != 0:
                self.time_after_creation += 1 / get_fps
                self.time_since_selected_new_tab += 1 / get_fps

            self.render()
            pygame.display.update()


class LevelCreatorMenu(Menu):
    def __init__(self, screen):
        super(LevelCreatorMenu, self).__init__(screen)
        self.question1 = QuestionScreen(screen, "Do you want to change a world or create one?", "Change", "Create")
        self.level_screen = LevelMenu(screen)
        self.question2 = QuestionScreen(screen, "What is the horizontal size of your world (in pixels)?")
        self.question3 = QuestionScreen(screen, "What is the vertical size of your world (in pixels)?")
        self.question4 = BackgroundSelectScreen(screen)
        self.question5 = QuestionScreen(screen, "What is the name of your world?")
        self.adaption_screen = ChangeScreen(screen)

    def loop(self):
        answer1 = self.question1.loop()
        name = None
        if answer1 == "Change":
            _, world, name = self.level_screen.loop()
        else:
            answer2 = max(int(self.question2.loop()), SCREEN_SIZE[0])
            answer3 = max(int(self.question3.loop()), SCREEN_SIZE[1])
            background = self.question4.loop()
            world = World((answer2, answer3), background)

        self.adaption_screen.world = world
        self.adaption_screen.loop()
        if answer1 == "Create":
            name = self.question5.loop()
            name = os.path.join("Worlds", name)
        self.adaption_screen.world.save(name)

        return "main"
