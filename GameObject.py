import numpy as np
from CONSTANTS import *
import pygame

pygame.init()


class GameObject(pygame.sprite.Sprite):
    def __init__(self, pos, vel, sprite, world=None, type=None, resize=None,
                 passable=False, horizontal_movable=True, vertical_movable=True):
        super(GameObject, self).__init__()
        self.world = None
        """
        There are different type of kinds, type can be anything but here are some types that are already used in the
        code:
        "player": for the player character
        "enemy": for all enemies
        "tile": for all tiles
        "goal": as soon as the player hits an object of type goal, the game is won
        
        Note: the following options are only implemented for more speed, their use is optional
        "change dont collide": this is for game objects that change during the game, but cant collide with other objects
        "change passive collide": These are for gae objects that change, but collision should only be checked passively
                                  For example: coins change their appearance, but don't move so collision is only passive
        "background": for background images
        "dont change passive collide: for images that dont change their appearance or position, but with which objects 
                                     can collide"
                                     
        Any other type name will be handled as a game object that can actively collide and does move
        
        """
        self.type = type
        self.lives = 1
        self.alive = True
        self.pos = np.array(pos).astype(np.float64)
        self.vel = np.array(vel).astype(np.float64)

        # The input parameters attribute is necessary for saving the world, it is advised to create this variable
        # in your game object itself
        if not hasattr(self, "input_parameters"):
            self.input_parameters = (pos, )

        self.passable = passable
        self.horizontal_movable = horizontal_movable
        self.vertical_movable = vertical_movable
        self.image = sprite
        # Whether or not it collided at the bottom in the last update
        self.collided_down = False

        if resize is not None:
            self.image = pygame.transform.scale(self.image, resize)

        # the sprite with wich the game object is initialized
        self.start_sprite = self.image
        self.size = self.image.get_size()

        if world is not None:
            world.add_gameobject(self)

    def set_sprite(self, new_sprite, resize=None):
        self.image = new_sprite
        size = self.image.get_size()
        if resize is not None and (resize[0] != size[0] or resize[1] != size[1]):
            self.image = pygame.transform.scale(self.image, resize)
        old_size = self.size
        self.size = self.image.get_size()
        self.pos[1] += (old_size[1] - self.size[1])
        self.pos[0] += (old_size[0] - self.size[0])

    def render(self, screen, pos_camera, size_screen=SCREEN_SIZE):
        position = np.round(self.pos - pos_camera).astype(np.int32)
        if 0 <= position[0] + self.size[0] and position[0] <= size_screen[0] and \
                0 <= position[1] + self.size[1] and position[1] <= size_screen[1]:
            screen.blit(self.image, position)

    def collides(self, other):
        """
        Returns whether or not it touches the other object (for now, its just rectangular collision detection).
        If objects don't collide, returns False. If objects collide, returns at which side of this object they collide:
        "up", "down", "left", "right". (thus "left" means that this object is hit on the left side)
        """
        if other == self:
            return False, 0
        if self.pos[1] < other.pos[1]:
            side_overlap = self.pos[1] + self.size[1] - other.pos[1]
        else:
            side_overlap = other.pos[1] + other.size[1] - self.pos[1]
        if side_overlap <= 0:
            return False, 0

        if self.pos[0] < other.pos[0]:
            top_down_overlap = self.pos[0] + self.size[0] - other.pos[0]
        else:
            top_down_overlap = other.pos[0] + other.size[0] - self.pos[0]
        if top_down_overlap <= 0:
            return False, 0

        if side_overlap > top_down_overlap:
            if self.pos[0] < other.pos[0]:
                return "right", side_overlap
            return "left", side_overlap
        else:
            if self.pos[1] <= other.pos[1]:
                return "down", top_down_overlap
            return "up", top_down_overlap

    def handle_special_reaction(self, side, other):
        """
        Handles special reactions for a certain type of collision between game objects
        """
        if side == "left":
            other.special_reaction_collision("right", self)
        elif side == "right":
            other.special_reaction_collision("left", self)
        elif side == "down":
            other.special_reaction_collision("up", self)
        else:
            other.special_reaction_collision("down", self)
        self.special_reaction_collision(side, other)

    def collision_reaction(self, side, other):
        """
        Handles the reaction of a game object and the other game object to a collision.
        """
        if not self.passable and not other.passable:
            if side == "down" or side == "up":
                self.vel[1] = 0
                other.vel[1] = 0
            else:
                self.vel[0] = 0
                other.vel[0] = 0

            if side == "down":
                self.collided_down = True
                if self.vertical_movable:
                    self.pos[1] = other.pos[1] - self.size[1]
                elif other.vertical_movable:
                    other.pos[1] = self.pos[1] + self.size[1]
                else:
                    return ValueError("Two non vertical movable object collide vertical.")
            elif side == "up":
                if self.vertical_movable:
                    self.pos[1] = other.pos[1] + other.size[1]
                elif other.vertical_movable:
                    other.pos[1] = self.pos[1] - other.size[1]
                else:
                    return ValueError("Two non vertical movable object collide vertical.")
            elif side == "right":
                if self.horizontal_movable:
                    self.pos[0] = other.pos[0] - self.size[0]
                elif other.horizontal_movable:
                    other.pos[0] = self.pos[0] + self.size[0]
                else:
                    return ValueError("Two non horizontal movable object collide horizontal.")
            elif side == "left":
                if self.horizontal_movable:
                    self.pos[0] = other.pos[0] + other.size[0]
                elif other.horizontal_movable:
                    other.pos[0] = self.pos[0] - other.size[0]
                else:
                    return EnvironmentError("Two non horizontal movable object collide horizontal.")

        self.handle_special_reaction(side, other)

    def special_reaction_collision(self, side, other):
        """
        Collision specific method that handles special collisions of the game object, should be overwritten in the
        game object.
        """
        pass

    def collision_tiles(self, tiles):
        """
        Check with which tiles it collides, the code looks a bit complicated but that's to ensure a bit more speed
        """
        for i in range(int(np.floor(self.pos[0] - self.pos[0] % TILE_SIZE[0])),
                       int(np.ceil(self.pos[0] + self.size[0])), TILE_SIZE[0]):
            for j in range(int(np.floor(self.pos[1] - self.pos[1] % TILE_SIZE[1])),
                           int(np.ceil(self.pos[1] + self.size[1])), TILE_SIZE[1]):
                try:
                    tile = tiles[i // TILE_SIZE[0]][j // TILE_SIZE[1]]
                    if tile is not None:
                        side, size_overlap = self.collides(tile)
                        if side:
                            self.collision_reaction(side, tile)
                except IndexError:
                    pass

    def collides_fast_check(self, other):
        """
        Checks whether two objects collide in a fast way. This is used to detect collision between two non-tiles:
        most of the time these objects will not collide so it is faster to first check this and then run the long
        code of colllides
        """
        return not (self.pos[0] + self.size[0] < other.pos[0] or other.pos[0] + other.size[0] < self.pos[0] or
                    self.pos[1] + self.size[1] < other.pos[1] or other.pos[1] + other.size[1] < self.pos[1])

    def collision_game_objects(self, game_objects):
        """
        Handles the collision between this game object and all other game objects given as parameter
        """
        for other in game_objects:
            if self.collides_fast_check(other):
                side, size_overlap = self.collides(other)
                if side:
                    self.collision_reaction(side, other)

    def collision_all(self, game_objects, tiles):
        """
        checks collision with the tiles given and the game objects given
        """
        self.collision_game_objects(game_objects)
        self.collision_tiles(tiles)

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
        :return:
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

    def update(self, time):
        """
        Updates everything of the given object for the given amount of time
        :return:
        """
        if self.horizontal_movable:
            self.pos[0] += time * self.vel[0]
        if self.vertical_movable:
            self.pos[1] += time * self.vel[1]
            if not self.collided_down:
                self.vel[1] += GRAVITY * time
        self.collided_down = False
        if self.horizontal_movable or self.vertical_movable:
            self.handle_outside_world_size()

    def __str__(self):
        return "game object"
