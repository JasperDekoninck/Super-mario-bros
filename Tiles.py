from GameObject import GameObject
from Specials import *
import numpy as np
from sprite_loader import *
from CONSTANTS import *


class Tile(GameObject):
    def __init__(self, pos, sprite, world=None, autoset=True):
        if autoset:
            pos = np.array([pos[0] - pos[0] % TILE_SIZE[0], pos[1] - pos[1] % TILE_SIZE[1]])
        super(Tile, self).__init__(pos, np.zeros(2), sprite, world=world, type="tile", horizontal_movable=False,
                                   vertical_movable=False, resize=TILE_SIZE)


class MysteryBox(Tile):
    def __init__(self, pos, color="yellow", world=None, autoset=True):
        assert color == "yellow" or color == "blue" or color == "red"
        self.input_parameters = (pos, color)
        self.color = color
        sprite = TILES_SPECIAl[color]
        super(MysteryBox, self).__init__(pos, sprite, world, autoset=autoset)
        self.type = "change passive collide"

    def special_reaction_collision(self, side, other):
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
        self.input_parameters = (pos, sprite_name)
        sprite = TILES[sprite_name]
        super(NormalTile, self).__init__(pos, sprite, world, autoset=autoset)
