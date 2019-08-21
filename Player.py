from sprite_loader import *
from GameObject import GameObject
from Menus.SettingsMenu import SettingsMenu
import numpy as np
from CONSTANTS import *


class Mario(GameObject):
    def __init__(self, pos, size=None, world=None):
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

        # keeps time after a hit, the player is invulnerable while self.hit > 0
        self.hit = 0
        # The number of coins the player has taken
        self.coins = 0
        self.goal_reached = False
        self.jumping = False

    def collision_set_good(self, collision_object, side_index):
        if collision_object.type != "goal":
            super(Mario, self).collision_set_good(collision_object, side_index)

    def special_reaction_collision(self, side, other):
        if other.type == "enemy" and other.alive:
            if side == "vertical" and self.pos[1] < other.pos[1] and self.ducking and \
                    (str(other) != "turtle" or other.vel[0] == 0):
                if str(other) != "turtle":
                    other.set_lives(other.lives - 1)
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
                self.goal_reached = True
                self.world.won = True
                self.current_sprite_int = 0
        elif side == "vertical" and not other.passable and self.pos[1] < other.pos[1]:
            self.able_to_jump = True

    def change_sprite(self):
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

    def duck(self):
        if not self.ducking:
            self.ducking = True
            if self.vel[1] != 0:
                self.vel[1] += self.ducking_speed
        self.vel[0] = 0

    def stop_ducking(self):
        self.ducking = False

    def jump(self):
        if self.able_to_jump and not self.jumping:
            self.able_to_jump = False
            self.vel[1] = - self.jump_speed
            self.change_sprite()
            self.jumping = True

    def end_jump(self):
        if self.jumping:
            self.vel[1] = np.maximum(0, self.vel[1])
            self.jumping = False

    def horizontal_move(self, direction=0):
        self.vel[0] = direction * self.horizontal_speed

        if direction != 0:
            self.direction = direction
            if self.current_sprite_int == -1:
                self.current_sprite_int = 0
        else:
            self.time_since_sprite_change = 0
        self.change_sprite()

    def on_death(self):
        super(Mario, self).on_death()
        self.world.gameover = True
        if SettingsMenu.SETTINGS["Sound"] == "on":
            DIE_SOUND.play()

    def update(self, time):
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
