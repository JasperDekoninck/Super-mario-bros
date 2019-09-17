from sprite_loader import *
from GameObject import GameObject
from Menus.SettingsMenu import SettingsMenu
import numpy as np


class Mushroom(GameObject):
    def __init__(self, pos, size=TILE_SIZE, color="red", direction=1, world=None):
        assert color == "red" or color == "blue"
        self.input_parameters = (pos, size, color, direction)
        sprite = SPECIALS[color + " mushroom"]
        self.direction = direction
        self.speed = SPEED_MUSHROOM
        super(Mushroom, self).__init__(pos, np.array([self.direction * SPEED_MUSHROOM, 0]), sprite, resize=size,
                                       world=world, type="mushroom special")

    def special_reaction_collision(self, side, other):
        if other.type == "player":
            other.lives = 2
            self.world.remove_gameobject(self)
            if SettingsMenu.SETTINGS["Sound"] == "on":
                POWERUP_SOUND.play()
        elif other.type == "enemy":
            self.world.remove_gameobject(self)
        else:
            if side == "horizontal" and not other.passable:
                self.direction *= -1
                self.vel[0] = self.direction * self.speed


class Flagpole(GameObject):
    def __init__(self, pos, size=FLAGPOLE_SIZE, world=None):
        self.input_parameters = (pos, size)
        super(Flagpole, self).__init__(pos, np.zeros(2), FLAGPOLE, resize=size, world=world, type="goal",
                                       vertical_movable=False, horizontal_movable=False)

    def special_reaction_collision(self, side, other):
        if other.type == "player":
            # the constants here are quite arbirary but give the best view when playing
            if other.pos[0] > self.pos[0] + self.size[0] // 3:
                other.pos[0] = self.pos[0] + 4 * self.size[0] // 7
            if other.pos[1] + other.size[1] >= self.pos[1] + self.size[1] - 20:
                other.pos[1] = self.pos[1] + self.size[1] - other.size[1] - 20
                self.world.gameover = True
                self.world.won = True
                if SettingsMenu.SETTINGS["Sound"] == "on":
                    STAGE_CLEAR_SOUND.play()
            elif other.pos[1] < self.pos[1]:
                other.pos[1] = self.pos[1]

    def __str__(self):
        return "flagpole"


class BackgroundSprites(GameObject):
    def __init__(self, pos, sprite_name, size=None, world=None):
        self.input_parameters = (pos, sprite_name, size)
        sprite = BACKGROUND_SPRITES[sprite_name]
        super(BackgroundSprites, self).__init__(pos, np.zeros(2), sprite=sprite, world=world, type="background", resize=size,
                                                passable=True, vertical_movable=False, horizontal_movable=False)


class Pipe(GameObject):
    def __init__(self, pos, size, dir=0, world=None, autoset=True):
        # NOTE: pipe is the only object which should not be created with its real size, but with its size
        # relative to the TILE_SIZE.
        if autoset:
            pos = np.array([pos[0] - pos[0] % TILE_SIZE[0], pos[1] - pos[1] % TILE_SIZE[1]])
        self.input_parameters = (pos, size, dir)
        size = (TILE_SIZE[0] * size[0], TILE_SIZE[1] * size[1])

        # the following code is to allow different sizes and directions of the pipe using only one sprite
        sprite = PIPE
        sprite_size = sprite.get_size()
        x_size, y_size = size
        if dir == 1 or dir == 3:
            x_size, y_size = y_size, x_size

        factor = sprite_size[1] / y_size
        x_within_factor = factor * x_size
        if x_within_factor > sprite_size[0]:
            x_within_factor = sprite_size[0]

        sprite = sprite.subsurface((sprite_size[0] - x_within_factor, 0, x_within_factor, sprite_size[1]))
        sprite = pygame.transform.rotate(sprite, dir * 90)
        sprite = pygame.transform.scale(sprite, size)

        super(Pipe, self).__init__(pos, np.zeros(2), sprite=sprite, world=world, type="dont change passive collide",
                                   resize=None, vertical_movable=False, horizontal_movable=False)


class Coin(GameObject):
    def __init__(self, pos, world=None, autoset=True):
        self.input_parameters = (pos,)
        if autoset:
            pos = np.array([pos[0] - pos[0] % TILE_SIZE[0], pos[1] - pos[1] % TILE_SIZE[1]])
        sprite = COINS[0]
        super(Coin, self).__init__(pos, np.zeros(2), sprite=sprite, world=world, type="change passive collide",
                                   resize=TILE_SIZE, passable=True, vertical_movable=False, horizontal_movable=False)
        self.time_since_sprite_change = 0
        self.current_sprite_int = 0

    def special_reaction_collision(self, side, other):
        if other.type == "player":
            other.coins += 1
            other.score += 100
            self.world.remove_gameobject(self)
            if SettingsMenu.SETTINGS["Sound"] == "on":
                COIN_SOUND.play()

    def update(self, time):
        super(Coin, self).update(time)
        self.time_since_sprite_change += time
        if self.time_since_sprite_change > TIME_SPRITE_CHANGE_COINS:
            self.time_since_sprite_change = 0
            self.current_sprite_int = (self.current_sprite_int + 1) % len(COINS)
            self.set_sprite(COINS[self.current_sprite_int], TILE_SIZE)
