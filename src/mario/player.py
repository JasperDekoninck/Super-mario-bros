from .sprite_loader import *
from .game_object import GameObject
from .menus.settings_menu import SettingsMenu
import numpy as np
from .constants import *


class Mario(GameObject):
    def __init__(self, pos, size=None, world=None):
        """
        Initializes a Mario object.

        Args:
            pos (tuple): The position of the Mario object.
            size (tuple, optional): The size of the Mario object. Defaults to None.
            world (World, optional): The world in which the Mario object exists. Defaults to None.
        """
        self.input_parameters = (pos, size)
        super(Mario, self).__init__(pos, np.zeros(2), MARIO_STILL, resize=size, type="player", world=world)
        self.horizontal_speed = SPEED_PLAYER
        self.jump_speed = JUMP_SPEED_PLAYER
        self.able_to_jump = False
        self.ducking = False
        self.ducking_speed = DUCK_SPEED_PLAYER
        self.current_sprite_int = -1
        self.direction = 1
        self.time_since_sprite_change = 0
        self.basic_size = np.copy(self.size)
        self.score = 0

        # keeps time after a hit, the player is invulnerable while self.hit > 0
        self.hit = 0
        # The number of coins the player has taken
        self.coins = 0
        self.goal_reached = False
        self.jumping = False

    def collision_set_good(self, collision_object, side_index):
        """
        Handles collision with objects that are not goals or mushrooms.
        Calls the parent class's collision_set_good method.

        Args:
            collision_object (object): The object that Mario collides with.
            side_index (int): The index of the side of the collision.

        Returns:
            None
        """
        if collision_object.type != "goal" and "mushroom" not in collision_object.type:
            super(Mario, self).collision_set_good(collision_object, side_index)

    def special_reaction_collision(self, side, other):
        """
        Handles special reactions when the player collides with other objects.

        Args:
            side (str): The side of the collision ("vertical" or "horizontal").
            other (object): The object the player collided with.

        Returns:
            None
        """
        if other.type == "enemy" and other.alive:
            if side == "vertical" and self.pos[1] < other.pos[1] and self.ducking and \
                    (str(other) != "turtle" or other.vel[0] == 0):
                if str(other) != "turtle":
                    other.set_lives(other.lives - 1)
                    self.score += 100
                if SettingsMenu.SETTINGS["Sound"] == "on":
                    KICK_SOUND.play()
                self.able_to_jump = True
                self.jump()
                # This makes sure that a full jump is performed, otherwise the program will call end_jump()
                # and set te velocity back to 0
                self.jumping = False
            elif self.hit <= 0:
                self.set_lives(self.lives - 1)
                self.hit = INVULNERABLE_TIME
        elif other.type == "goal":
            if not self.goal_reached and self.pos[0] >= other.pos[0] + 4 * other.size[0] // 7:
                self.score += 1000
                self.goal_reached = True
                self.world.won = True
                self.current_sprite_int = 0
        elif side == "vertical" and not other.passable and self.pos[1] < other.pos[1]:
            self.able_to_jump = True

    def change_sprite(self):
        """
        Changes the sprite of the player character based on its current state and conditions.

        The sprite is updated based on the player's movement, goal status, ducking state, and direction.
        The size of the sprite is also adjusted based on the player's lives.

        Returns:
            None
        """
        if self.time_since_sprite_change > TIME_SPRITE_CHANGE_PLAYER and not self.goal_reached:
            self.current_sprite_int = (self.current_sprite_int + 1) % len(MARIO_RUNNING)
            self.time_since_sprite_change = 0
        elif self.time_since_sprite_change > TIME_SPRITE_CHANGE_PLAYER:
            self.current_sprite_int = (self.current_sprite_int + 1) % len(MARIO_FLAGPOLE)
            self.time_since_sprite_change = 0
        if np.abs(self.vel[0]) <= 0 and not self.goal_reached:
            self.current_sprite_int = -1

        if not self.alive:
            self.current_sprite_int = -1

        if self.current_sprite_int == -1 and not self.ducking:
            sprite = MARIO_STILL
        elif self.goal_reached:
            sprite = MARIO_FLAGPOLE[self.current_sprite_int]
        elif self.ducking:
            sprite = MARIO_DUCK
        else:
            sprite = MARIO_RUNNING[self.current_sprite_int]

        if self.direction == -1 and self.alive:
            sprite = pygame.transform.flip(sprite, True, False)

        # changing size of the player. If it has hit a Mushroom, it lives will increase, so will its size
        if self.lives <= 1:
            size = (int(np.round(1 / 1.3 * sprite.get_size()[0])), int(np.round((1 / 1.3 * sprite.get_size()[1]))))
        else:
            size = (int(np.round(1 / 1.1 * sprite.get_size()[0])), int(np.round((1 / 1.1 * sprite.get_size()[1]))))

        self.set_sprite(sprite, size)

    def collides(self, other):
        """
        Checks for collision between the player and another object.

        Parameters:
        - other: The object to check for collision with.

        Returns:
        - A list of sprites that collide with the player, if any.
        """
        if "tile" not in other.type:
            if super(Mario, self).collides(other):
                self.mask = pygame.mask.from_surface(self.image)
                other.mask = pygame.mask.from_surface(other.image)
                self.rect = self.image.get_rect()
                other.rect = other.image.get_rect()
                return pygame.sprite.spritecollide(self, [other], False, pygame.sprite.collide_mask)
        return super(Mario, self).collides(other)

    def duck(self):
        """
        Duck method is used to make the player character duck.
        It reduces the horizontal velocity and increases the vertical velocity if the player is already in motion.
        """
        self.vel[0] *= 0.985
        if np.abs(self.vel[0]) < 5:
            self.vel[0] = 0
        if not self.ducking:
            self.ducking = True
            if self.vel[1] != 0:
                self.vel[1] += self.ducking_speed

    def stop_ducking(self):
        """
        Stops the player from ducking.
        """
        self.ducking = False

    def jump(self):
        """
        Makes the player character jump if able to.

        If the player is able to jump and is not currently jumping, this method sets the vertical velocity
        to a negative value to make the player character jump. It also updates the sprite and sets the
        jumping flag to True.

        """
        if self.able_to_jump and not self.jumping:
            self.able_to_jump = False
            self.vel[1] = - self.jump_speed
            self.change_sprite()
            self.jumping = True

    def end_jump(self):
        """
        Ends the jump of the player.

        If the player is currently jumping, this method sets the vertical velocity
        to the maximum of 0 and the current vertical velocity, effectively stopping
        the upward movement. It also sets the `jumping` attribute to False.

        Parameters:
            None

        Returns:
            None
        """
        if self.jumping:
            self.vel[1] = np.maximum(0, self.vel[1])
            self.jumping = False

    def horizontal_move(self, direction=0):
        """
        Move the player horizontally.

        Args:
            direction (int): The direction of movement. 
                -1 for left, 1 for right, and 0 for no movement.

        Returns:
            None
        """
        if not self.ducking:
            self.vel[0] = direction * self.horizontal_speed

        if direction != 0:
            self.direction = direction
            if self.current_sprite_int == -1:
                self.current_sprite_int = 0
        else:
            self.time_since_sprite_change = 0
        self.change_sprite()

    def on_death(self):
        """
        Handles the actions to be taken when the player dies.
        """
        super(Mario, self).on_death()
        self.world.gameover = True
        if SettingsMenu.SETTINGS["Sound"] == "on":
            DIE_SOUND.play()

    def update(self, time):
        """
        Updates the player's position and behavior based on the given time.

        Parameters:
            time (float): The time elapsed since the last update.

        Returns:
            None
        """
        if self.vertical_movable:
            if not self.goal_reached:
                self.pos[1] += time * self.vel[1]
            else:
                self.pos[1] += time * SPEED_DOWN_FLAGPOLE

            self.check_collision_update("vertical")
            self.able_to_jump = self.vel[1] == 0
            self.vel[1] += GRAVITY * time
        if self.horizontal_movable:
            self.pos[0] += time * self.vel[0]
            self.check_collision_update("horizontal")
            self.handle_outside_world_size()
            self.change_sprite()
            self.time_since_sprite_change += time
        self.hit -= time

    def __str__(self):
        return "mario"
