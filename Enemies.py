from sprite_loader import *
from CONSTANTS import *
from GameObject import GameObject
import numpy as np


class Enemy(GameObject):
    def __init__(self, pos, sprites, death_sprite=None, dir=1, world=None):
        self.direction = dir
        self.speed = SPEED_ENEMY
        # Integer keeping track of which of the sprites is currently in use
        self.current_sprite_int = 0
        self.time_since_sprite_change = 0
        # time since object died
        self.time_death = 0
        # the sprite of the object when it is death but not yet removed from the world
        self.death_sprite = death_sprite
        self.sprites = sprites
        sprite = self.sprites[0]
        if self.direction == -1:
            sprite = pygame.transform.flip(sprite, True, False)
        super(Enemy, self).__init__(pos, np.array([dir * SPEED_ENEMY, 0]), sprite, world=world, type="enemy")

    def special_reaction_collision(self, side, other):
        if side == "horizontal" and not other.passable:
            self.direction *= -1
            self.vel[0] = self.speed * self.direction

    def handle_outside_world_size(self):
        super(Enemy, self).handle_outside_world_size()
        if self.world is not None and (self.pos[0] == 0 or self.pos[0] == self.world.size[0]):
            self.direction *= -1
            self.vel[0] = self.direction * self.speed

    def change_sprite(self):
        if self.time_since_sprite_change > TIME_SPRITE_CHANGE:
            self.current_sprite_int = (self.current_sprite_int + 1) % len(self.sprites)
            self.time_since_sprite_change = 0

        if self.alive:
            sprite = self.sprites[self.current_sprite_int]
        elif self.death_sprite is not None:
            sprite = self.death_sprite
        else:
            sprite = self.sprites[0]

        if self.direction == 1:
            sprite = pygame.transform.flip(sprite, True, False)

        self.set_sprite(sprite)

    def update(self, time):
        super(Enemy, self).update(time)
        if self.alive:
            self.time_since_sprite_change += time
            self.vel[0] = self.direction * self.speed
        else:
            self.time_death += time

        self.change_sprite()


class Goomba(Enemy):
    def __init__(self, pos, dir=1, world=None):
        self.input_parameters = (pos, dir)
        self.time_death = 0
        super(Goomba, self).__init__(pos, GOOMBA, GOOMBA_DEATH, dir=dir, world=world)

    def update(self, time):
        super(Goomba, self).update(time)

        if self.time_death >= GOOMBA_SECONDS_REMOVED_AFTER_DEATH:
            self.world.remove_gameobject(self)

    def __str__(self):
        return "goomba"


class KoopaTroopa(Enemy):
    def __init__(self, pos, dir=1, color="blue", world=None):
        self.input_parameters = (pos, dir, color)
        self.color = color
        if color == "blue":
            sprites = KOOPA["blue"]
        elif color == "green":
            sprites = KOOPA["green"]
        else:
            sprites = KOOPA["red"]

        super(KoopaTroopa, self).__init__(pos, sprites, None, dir=dir, world=world)

    def on_death(self):
        super(KoopaTroopa, self).on_death()
        turtle = KoopTroopaTurtle(self.pos, color=self.color)
        turtle.pos[1] += self.size[1] - turtle.size[1]
        world = self.world
        self.world.remove_gameobject(self)
        world.add_gameobject(turtle)

    def __str__(self):
        return "koopa"


class KoopTroopaTurtle(Enemy):
    def __init__(self, pos, dir=0, color="blue", world=None):
        self.input_parameters = (pos, dir, color)

        if color == "blue":
            sprites = KOOPA_TURTLE["blue"]
        elif color == "green":
            sprites = KOOPA_TURTLE["green"]
        else:
            sprites = KOOPA_TURTLE["red"]

        super(KoopTroopaTurtle, self).__init__(pos, sprites, None, dir=dir, world=world)

        self.vel = np.zeros(2)
        self.speed = SPEED_TURTLE
        self.direction = 0

    def change_sprite(self):
        if self.direction != 0:
            super(KoopTroopaTurtle, self).change_sprite()

    def on_death(self):
        super(KoopTroopaTurtle, self).on_death()
        if not self.alive:
            self.world.remove_gameobject(self)

    def special_reaction_collision(self, side, other):
        super(KoopTroopaTurtle, self).special_reaction_collision(side, other)

        if self.direction == 0 and not "tile" in other.type and not other.passable:
            if other.pos[0] <= self.pos[0]:
                self.direction = 1
            else:
                self.direction = -1
        elif self.direction != 0 and other.type == "enemy" and str(other) != "turtle":
            other.set_lives(other.lives - 1)
            if other.alive:
                self.direction *= -1

    def __str__(self):
        return "turtle"
