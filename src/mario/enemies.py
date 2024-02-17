from .sprite_loader import *
from .constants import *
from .game_object import GameObject
import numpy as np


class Enemy(GameObject):
    def __init__(self, pos, sprites, death_sprite=None, dir=1, world=None):
        """
        Initializes an Enemy object.

        Args:
            pos (tuple): The position of the enemy.
            sprites (list): A list of sprites for the enemy.
            death_sprite (optional): The sprite of the enemy when it is dead but not yet removed from the world.
            dir (int, optional): The direction of the enemy. Default is 1.
            world (optional): The world object the enemy belongs to.

        Attributes:
            direction (int): The direction of the enemy.
            speed (int): The speed of the enemy.
            current_sprite_int (int): The index of the current sprite in use.
            time_since_sprite_change (int): The time since the sprite was last changed.
            time_death (int): The time since the enemy died.
            death_sprite (optional): The sprite of the enemy when it is dead but not yet removed from the world.
            sprites (list): A list of sprites for the enemy.
        """
        self.direction = dir
        self.speed = SPEED_ENEMY
        self.current_sprite_int = 0
        self.time_since_sprite_change = 0
        self.time_death = 0
        self.death_sprite = death_sprite
        self.sprites = sprites
        sprite = self.sprites[0]
        if self.direction == -1:
            sprite = pygame.transform.flip(sprite, True, False)
        super(Enemy, self).__init__(pos, np.array([dir * SPEED_ENEMY, 0]), sprite, world=world, type="enemy")

    def special_reaction_collision(self, side, other):
        """
        Handles special reaction collision with other objects.

        Args:
            side (str): The side of the collision ("horizontal" or "vertical").
            other (object): The other object involved in the collision.

        Returns:
            None
        """
        if side == "horizontal" and not other.passable:
            self.direction *= -1
            self.vel[0] = self.speed * self.direction

    def handle_outside_world_size(self):
        """
        Handles the behavior of the enemy when it reaches the edge of the world.

        This method is called to check if the enemy has reached the left or right edge of the world.
        If so, it changes the enemy's direction and updates its velocity accordingly.

        Returns:
            None
        """
        super(Enemy, self).handle_outside_world_size()
        if self.world is not None and (self.pos[0] == 0 or self.pos[0] == self.world.size[0]):
            self.direction *= -1
            self.vel[0] = self.direction * self.speed

    def change_sprite(self):
        """
        Changes the sprite of the enemy character based on its current state and direction.
        """
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
        """
        Update the enemy's state based on the elapsed time.

        Args:
            time (float): The elapsed time since the last update.

        Returns:
            None
        """
        super(Enemy, self).update(time)
        if self.alive:
            self.time_since_sprite_change += time
            self.vel[0] = self.direction * self.speed
        else:
            self.time_death += time

        self.change_sprite()


class Goomba(Enemy):
    def __init__(self, pos, dir=1, world=None):
        """
        Initializes a Goomba enemy object.

        Args:
            pos (tuple): The position of the Goomba in the world.
            dir (int, optional): The direction the Goomba is facing. Defaults to 1.
            world (World, optional): The world object the Goomba belongs to. Defaults to None.
        """
        self.input_parameters = (pos, dir)
        self.time_death = 0
        super(Goomba, self).__init__(pos, GOOMBA, GOOMBA_DEATH, dir=dir, world=world)

    def update(self, time):
        """
        Update the Goomba's state based on the elapsed time.

        Args:
            time (float): The elapsed time since the last update.

        Returns:
            None
        """
        super(Goomba, self).update(time)

        if self.time_death >= GOOMBA_SECONDS_REMOVED_AFTER_DEATH:
            self.world.remove_gameobject(self)

    def __str__(self):
        return "goomba"


class KoopaTroopa(Enemy):
    def __init__(self, pos, dir=1, color="blue", world=None):
        """
        Initialize a KoopaTroopa object.

        Args:
            pos (tuple): The initial position of the KoopaTroopa.
            dir (int, optional): The initial direction of the KoopaTroopa. Defaults to 1.
            color (str, optional): The color of the KoopaTroopa. Defaults to "blue".
            world (World, optional): The world in which the KoopaTroopa exists. Defaults to None.
        """
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
        """
        Performs actions when the KoopaTroopa enemy is killed.
        Creates a KoopTroopaTurtle object, adjusts its position, and adds it to the game world.
        """
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
        """
        Initializes a KoopTroopaTurtle object.

        Args:
            pos (tuple): The initial position of the turtle.
            dir (int, optional): The initial direction of the turtle. Defaults to 0.
            color (str, optional): The color of the turtle. Defaults to "blue".
            world (World, optional): The world object the turtle belongs to. Defaults to None.
        """
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
        """
        Change the sprite of the KoopTroopaTurtle enemy.

        This method is called when the enemy's direction is not 0.
        It calls the parent class's change_sprite method to update the sprite.
        """
        if self.direction != 0:
            super(KoopTroopaTurtle, self).change_sprite()

    def on_death(self):
        """
        Performs actions when the enemy dies.
        """
        super(KoopTroopaTurtle, self).on_death()
        if not self.alive:
            self.world.remove_gameobject(self)

    def special_reaction_collision(self, side, other):
        """
        Perform special reaction collision with another object.

        Args:
            side (str): The side of the collision.
            other (object): The other object involved in the collision.

        Returns:
            None
        """
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
