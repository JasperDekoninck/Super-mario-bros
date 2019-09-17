import numpy as np
from CONSTANTS import *
from sprite_loader import BACKGROUNDS
import pickle

pygame.init()


class World:
    def __init__(self, size=None, background_image=None, load_file=None):
        assert (size is not None and background_image is not None) or load_file is not None
        if size is not None:
            # creates an empty world with the given background and size
            self.size = size
            self.string_background_image = background_image  # for saving purposes
            self.background_image = BACKGROUNDS[background_image]
            self.background_size = self.background_image.get_size()
            factor = self.size[1] / self.background_size[1]
            self.background_size = (int(self.background_size[0] * factor), self.size[1])
            self.background_image = pygame.transform.scale(self.background_image, self.background_size)
            self.tiles_fast_access = [[None for _ in range(self.size[1] // TILE_SIZE[1] + 1)]
                                      for _ in range(self.size[0] // TILE_SIZE[0] + 1)]
            self.save_list = None
            self.top_score = 0

        # All objects in different places, this is for speed
        self.player = None
        self.game_objects = []
        self.tiles = []
        self.background_objects = []
        self.top_score = 0

        # on the surface, the background (with tiles etc.) will be blitted. This speeds up the entire thing
        # a lot.
        self.surface = None

        self.camera_pos = np.zeros(2)

        self.gameover = False
        self.won = False

        if load_file is not None:
            # load the world that is asked
            self.load(load_file)

    def get_all_game_objects(self):
        """
        gets all game objects including tiles and background images
        """
        game_objects = []
        if self.player is not None:
            game_objects = [self.player]
        return game_objects + self.game_objects + self.background_objects + self.tiles

    def get_all_game_objects_no_tiles(self):
        """
        gets all game objects excluding tiles and background images
        """
        game_objects = []
        if self.player is not None:
            game_objects = [self.player]
        return game_objects + self.game_objects

    def render_tiles_and_basic(self, screen, size, camera_pos=np.zeros(2)):
        """
        This function renders the tiles, background, background objects and objects that dont change but do collide
        on the given screen of given size.
        """
        for i in range(self.size[0] // self.background_size[0] + 1):
            pos = (i * self.background_size[1] - camera_pos[0].astype(np.int32), - camera_pos[1].astype(np.int32))
            screen.blit(self.background_image, pos)
        for tile in self.tiles:
            tile.render(screen, camera_pos, size)
        for game_object in self.background_objects:
            game_object.render(screen, camera_pos, size)

    def render(self, screen, fast=True):
        """
        Renders the entire world. fast=True will allow the world to use the faster blitting method with self.surface
        This is not possible when a world is under construction, like in the level creator menu.
        """
        if fast:
            if self.surface is None:
                # if self.surface is not already created, blit everything that doesnt change through the entire
                # game on self.surface
                self.surface = pygame.Surface(self.size)
                self.render_tiles_and_basic(self.surface, self.size)
            screen.blit(
                self.surface.subsurface((self.camera_pos[0], self.camera_pos[1], SCREEN_SIZE[0], SCREEN_SIZE[1])),
                (0, 0))
        else:
            self.render_tiles_and_basic(screen, SCREEN_SIZE, camera_pos=self.camera_pos)

        for game_object in  self.game_objects:
            game_object.render(screen, self.camera_pos)
        if self.player is not None:
            self.player.render(screen, self.camera_pos)

    def allowed_game_object(self, game_object):
        if game_object.type == "tile" or game_object.passable:
            return True
        for game_object2 in self.get_all_game_objects_no_tiles():
            if game_object.collides(game_object2):
                return False
        return True

    def add_gameobject(self, game_object):
        """
        Adds a game object to the correct list of game objects
        """
        game_object.world = self
        if game_object.type == "player":
            if self.player is None:
                self.player = game_object
            else:
                game_object.world = None
                raise ValueError("World already has a player.")
        elif game_object.type == "tile":
            self.tiles.append(game_object)
            pos = game_object.pos.astype(np.int32)
            self.tiles_fast_access[pos[0] // TILE_SIZE[0]][pos[1] // TILE_SIZE[1]] = game_object
            if self.surface is not None:
                self.surface.blit(game_object.image, pos)
        elif game_object.type == "background":
            self.background_objects.append(game_object)
        else:
            self.game_objects.append(game_object)

    def remove_gameobject(self, game_object):
        """
        Removes a game object from the correct list
        """
        game_object.world = None
        if game_object.type == "player":
            if self.player == game_object:
                self.player = None
            else:
                raise ValueError("This player doesn't belong to the world.")
        elif game_object.type == "tile":
            self.tiles.remove(game_object)
            pos = game_object.pos.astype(np.int32)
            self.tiles_fast_access[pos[0] // TILE_SIZE[0]][pos[1] // TILE_SIZE[1]] = None
        elif game_object.type == "background":
            self.background_objects.remove(game_object)
        else:
            self.game_objects.remove(game_object)

    def update_handle_keys(self):
        """
        handles key movements, allowing the user to move the player
        """
        if self.player is not None:
            keys = pygame.key.get_pressed()  # checking pressed keys
            if keys[pygame.K_LEFT]:
                self.player.horizontal_move(direction=-1)
            elif keys[pygame.K_RIGHT]:
                self.player.horizontal_move(direction=1)
            else:
                self.player.horizontal_move(direction=0)
            if keys[pygame.K_UP] and not self.player.jumping:
                self.player.jump()
            elif not keys[pygame.K_UP] and self.player.jumping:
                self.player.end_jump()
            if keys[pygame.K_DOWN]:
                self.player.duck()
            else:
                self.player.stop_ducking()

    def one_update(self, time):
        self.update_handle_keys()
        if self.player is not None:
            self.player.update(time)

        for game_object in self.game_objects:
            game_object.update(time)

    def update(self, time):
        passed_time = 0
        while time > passed_time:
            # Not allowing the update to be too high, because the game would glitch if this happened
            new_passed_time = np.minimum(0.02, time - passed_time)
            self.one_update(new_passed_time)
            passed_time += new_passed_time

        if self.player is not None:
            # updates the camera position based on the position of the player
            player_pos_x = self.player.pos[0] + self.player.size[0] // 2
            player_pos_y = self.player.pos[1] + self.player.size[1] // 2
            x_camera_pos = np.minimum(np.maximum(0, player_pos_x + CAMERA_POS[0]), self.size[0] - SCREEN_SIZE[0])
            y_camera_pos = np.minimum(np.maximum(0, player_pos_y + CAMERA_POS[1]), self.size[1] - SCREEN_SIZE[1])
            self.camera_pos = np.array([x_camera_pos, y_camera_pos])

            if self.gameover:
                if self.player.score > self.top_score:
                    self.top_score = self.player.score

    def save_top_score(self, file):
        """
        Saves the initial state of the world to the given file.
        """
        self.save_list[2] = self.top_score
        pickle.dump(self.save_list, open(file, "wb"))

    def save(self, file):
        """
        Saves the world to the given file.
        """
        save_list = [self.size, self.string_background_image, 0]
        game_objects = self.get_all_game_objects()

        for game_object in game_objects:
            save_list += [[game_object.__class__, game_object.input_parameters]]

        pickle.dump(save_list, open(file, "wb"))

    def load(self, file):
        """
        Loads the world from the given file
        """
        save_list = pickle.load(open(file, "rb"))
        self.save_list = save_list
        self.camera_pos = np.zeros(2)
        self.gameover = False
        self.won = False

        self.player = None
        self.game_objects = []
        self.tiles = []

        self.size = save_list[0]

        self.tiles_fast_access = [[None for _ in range(self.size[1] // TILE_SIZE[1] + 1)]
                                  for _ in range(self.size[0] // TILE_SIZE[0] + 1)]

        # set background image and resizes it so it fits the screen better.
        self.background_image = BACKGROUNDS[save_list[1]]
        self.string_background_image = save_list[1]
        self.background_size = self.background_image.get_size()
        factor = self.size[1] / self.background_size[1]
        self.background_size = (int(self.background_size[0] * factor), self.size[1])
        self.background_image = pygame.transform.scale(self.background_image, self.background_size)
        self.top_score = save_list[2]
        # loads all game objects
        for element in save_list[3:]:
            game_object = element[0](*element[1])
            self.add_gameobject(game_object)
