import numpy as np
from .constants import *
import pygame

pygame.init()


class GameObject(pygame.sprite.Sprite):
    def __init__(self, pos, vel, sprite, world=None, type=None, resize=None,
                     passable=False, horizontal_movable=True, vertical_movable=True):
        """
        Initializes a game object.

        Args:
            pos (tuple): The position of the game object.
            vel (tuple): The velocity of the game object.
            sprite (pygame.Surface): The sprite image of the game object.
            world (World, optional): The world in which the game object exists. Defaults to None.
            type (str, optional): The type of the game object. Defaults to None.
            resize (tuple, optional): The size to resize the sprite image. Defaults to None.
            passable (bool, optional): Whether the game object is passable. Defaults to False.
            horizontal_movable (bool, optional): Whether the game object is horizontally movable. Defaults to True.
            vertical_movable (bool, optional): Whether the game object is vertically movable. Defaults to True.
        """
        super(GameObject, self).__init__()
        self.world = None
        self.type = type
        self.lives = 1
        self.alive = True
        self.pos = np.array(pos).astype(np.float64)
        self.vel = np.array(vel).astype(np.float64)
        if not hasattr(self, "input_parameters"):
            self.input_parameters = (pos,)
        self.passable = passable
        self.horizontal_movable = horizontal_movable
        self.vertical_movable = vertical_movable
        self.image = sprite
        self.rect, self.mask = None, None
        if resize is not None:
            self.image = pygame.transform.scale(self.image, resize)
        self.start_sprite = self.image
        self.size = self.image.get_size()
        if world is not None:
            world.add_gameobject(self)

    def set_sprite(self, new_sprite, resize=None):
        """
        Set the sprite image for the game object.

        Args:
            new_sprite (pygame.Surface): The new sprite image.
            resize (tuple, optional): The desired size of the sprite image. Defaults to None.
        """
        self.image = new_sprite
        size = self.image.get_size()
        if resize is not None and (resize[0] != size[0] or resize[1] != size[1]):
            self.image = pygame.transform.scale(self.image, resize)
        old_size = self.size
        new_size = self.image.get_size()
        self.size = list(self.size)
        self.size[0] = new_size[0]
        self.pos[0] += (old_size[0] - self.size[0])
        self.check_collision_update("horizontal")
        self.size[1] = new_size[1]
        self.pos[1] += (old_size[1] - self.size[1])
        self.check_collision_update("vertical")

    def render(self, screen, pos_camera, size_screen=SCREEN_SIZE):
        """
        Renders the game object on the screen.

        Args:
            screen (pygame.Surface): The surface to render the game object on.
            pos_camera (numpy.ndarray): The position of the camera.
            size_screen (tuple, optional): The size of the screen. Defaults to SCREEN_SIZE.
        """
        position = np.round(self.pos - pos_camera).astype(np.int32)
        if 0 <= position[0] + self.size[0] and position[0] <= size_screen[0] and \
                0 <= position[1] + self.size[1] and position[1] <= size_screen[1]:
            screen.blit(self.image, position)

    def special_reaction_collision(self, side, other):
        """
        Collision specific method that handles special collisions of the game object, should be overwritten in the
        game object.
        """
        pass

    def collides(self, other):
        """
        Checks whether two objects collide.
        """
        return not (self.pos[0] + self.size[0] <= other.pos[0] or other.pos[0] + other.size[0] <= self.pos[0] or
                    self.pos[1] + self.size[1] <= other.pos[1] or other.pos[1] + other.size[1] <= self.pos[1])

    def collision_tiles(self):
        """
        Returns the first tile that the game object collides with.

        Returns:
            The tile object that the game object collides with, or None if there is no collision.
        """
        for i in range(int(np.floor(self.pos[0] - self.pos[0] % TILE_SIZE[0])),
                       int(np.ceil(self.pos[0] + self.size[0])), TILE_SIZE[0]):
            for j in range(int(np.floor(self.pos[1] - self.pos[1] % TILE_SIZE[1])),
                           int(np.ceil(self.pos[1] + self.size[1])), TILE_SIZE[1]):
                try:
                    tile = self.world.tiles_fast_access[i // TILE_SIZE[0]][j // TILE_SIZE[1]]
                    if tile is not None and self.collides(tile) and tile != self:
                        return tile
                except IndexError:
                    pass

        return None

    def collides_all(self):
        """Checks for collisions with all game objects.

        Returns:
            list: A list of game objects that collide with the current game object.
        """
        collisions = []
        tile = self.collision_tiles()
        if tile is not None:
            collisions.append(tile)

        for game_object in self.world.get_all_game_objects_no_tiles():
            if self != game_object and self.collides(game_object):
                collisions.append(game_object)

        return collisions

    def on_death(self):
        """
        Function that is performed when dying
        """
        self.alive = False
        self.horizontal_movable = False
        self.vertical_movable = False

    def set_lives(self, lives):
        """
        Sets the lives of the game object to the given lives
        """
        self.lives = lives
        if self.lives <= 0 and self.alive:
            self.on_death()

    def handle_outside_world_size(self):
        """
        If a game object is outside the world (position is greater or lower than allowed, this function will handle
        this. If an object tries to go out of screen at the left or the right, it will just be corrected.
        If however it falls down, the object will die.
        """
        if self.world is not None:
            if self.pos[0] + self.size[0] > self.world.size[0]:
                self.pos[0] = self.world.size[0] - self.size[0]
            elif self.pos[0] < 0:
                self.pos[0] = 0
            if self.pos[1] > self.world.size[1]:
                self.set_lives(0)
            elif self.pos[1] < 0:
                self.pos[1] = 0

    def collision_set_good(self, collision_object, side_index):
        """
        Adjusts the position and velocity of the game object when a collision occurs with a non-passable object.

        Args:
            collision_object (GameObject): The object that the game object collided with.
            side_index (int): The index representing the side of the collision.

        Returns:
            None
        """
        if collision_object is not None and not collision_object.passable:
            if self.pos[side_index] < collision_object.pos[side_index]:
                self.pos[side_index] = collision_object.pos[side_index] - self.size[side_index]
            else:
                self.pos[side_index] = collision_object.pos[side_index] + collision_object.size[side_index]
            self.vel[side_index] = 0

    def check_collision_update(self, side):
        """
        :param side: "horizontal" if x direction, "vertical" if y direction
        """
        side_index = 0
        if side == "vertical":
            side_index = 1

        if not self.passable and self.world is not None:
            collision_objects = self.collides_all()
            for collision_object in collision_objects:
                self.collision_set_good(collision_object, side_index)

                if collision_object is not None:
                    self.special_reaction_collision(side, collision_object)
                    collision_object.special_reaction_collision(side, self)

    def update(self, time):
        """
        Updates everything of the given object for the given amount of time
        """
        if self.vertical_movable:
            self.pos[1] += time * self.vel[1]
            self.check_collision_update("vertical")
            self.vel[1] += GRAVITY * time

        if self.horizontal_movable:
            self.pos[0] += time * self.vel[0]
            self.check_collision_update("horizontal")

        if self.horizontal_movable or self.vertical_movable:
            self.handle_outside_world_size()

    def __str__(self):
        return "game object"
