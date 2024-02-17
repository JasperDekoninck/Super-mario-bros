from .game_object import GameObject
from .specials import *
import numpy as np
from .sprite_loader import *
from .constants import *


class Tile(GameObject):
    def __init__(self, pos, sprite, world=None, autoset=True):
        """
        Initialize a Tile object.

        Args:
            pos (tuple): The position of the tile.
            sprite: The sprite of the tile.
            world: The world the tile belongs to.
            autoset (bool): Whether to automatically adjust the position of the tile.

        Returns:
            None
        """
        if autoset:
            pos = np.array([pos[0] - pos[0] % TILE_SIZE[0], pos[1] - pos[1] % TILE_SIZE[1]])
        super(Tile, self).__init__(pos, np.zeros(2), sprite, world=world, type="tile", horizontal_movable=False,
                                   vertical_movable=False, resize=TILE_SIZE)


class MysteryBox(Tile):
    def __init__(self, pos, color="yellow", world=None, autoset=True):
        """
        Initialize a MysteryBox object.

        Args:
            pos (tuple): The position of the MysteryBox in the world.
            color (str, optional): The color of the MysteryBox. Defaults to "yellow".
            world (World, optional): The world in which the MysteryBox exists. Defaults to None.
            autoset (bool, optional): Whether to automatically set the MysteryBox in the world. Defaults to True.
        """
        assert color == "yellow" or color == "blue" or color == "red"
        self.input_parameters = (pos, color)
        self.color = color
        sprite = TILES_SPECIAl[color]
        super(MysteryBox, self).__init__(pos, sprite, world, autoset=autoset)
        self.type = "change passive collide"

    def special_reaction_collision(self, side, other):
        """
        Handles special reactions when colliding with other objects.

        Args:
            side (str): The side of the collision ("vertical" or "horizontal").
            other (object): The object colliding with.

        Returns:
            None
        """
        # when hit by the player in a certain way, a Mushroom will pop out and the object will be changed
        # into a Solid with the appropriate color
        if side == "vertical" and other.type == "player" and (other.ducking or self.pos[1] < other.pos[1]):
            color_solid = self.color
            if self.color == "yellow":
                color_solid = "brown"
            solid = NormalTile(self.pos, sprite_name=color_solid + " solid", world=None)
            if self.pos[1] < other.pos[1]:
                mushroom = Mushroom((self.pos[0], self.pos[1] - TILE_SIZE[1] - 1), color=np.random.choice(["red", "blue"]),
                                        direction=np.random.choice([1, -1]))
            else:
                mushroom = Mushroom((self.pos[0], self.pos[1] + TILE_SIZE[1] + 1), color=np.random.choice(["red", "blue"]),
                                    direction=np.random.choice([1, -1]))
            world = self.world
            self.world.remove_gameobject(self)
            world.add_gameobject(solid)
            world.add_gameobject(mushroom)
            if SettingsMenu.SETTINGS["Sound"] == "on":
                POWERUP_APPEARS_SOUND.play()

    def __str__(self):
        return "mystery box"


class NormalTile(Tile):
    def __init__(self, pos, sprite_name, world=None, autoset=True):
        """
        Initializes a NormalTile object.

        Args:
            pos (tuple): The position of the tile.
            sprite_name (str): The name of the sprite for the tile.
            world (World, optional): The world object the tile belongs to. Defaults to None.
            autoset (bool, optional): Whether to automatically set the tile in the world. Defaults to True.
        """
        self.input_parameters = (pos, sprite_name)
        sprite = TILES[sprite_name]
        super(NormalTile, self).__init__(pos, sprite, world, autoset=autoset)
