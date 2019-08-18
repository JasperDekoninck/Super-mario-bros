import pygame
import os
from pygame import mixer

pygame.init()
mixer.pre_init(channels=12)
mixer.init()

# A list of all constants used in the game, you can change them at will (changing TILE_SIZE will change the saved
# worlds in ways you probably don't want, so this is not advised)

GRAVITY = 500
FPS = 60
SCREEN_SIZE = (1200, 600)
TILE_SIZE = (15, 15)
CAMERA_POS = (-100, -300)
TIME_SPRITE_CHANGE = 0.075
TIME_SPRITE_CHANGE_PLAYER = 0.01
TIME_SPRITE_CHANGE_COINS = 0.07
SPEED_DOWN_FLAGPOLE = 150
SPEED_PLAYER = 100
JUMP_SPEED_PLAYER = 300
DUCK_SPEED_PLAYER = 450
SPEED_ENEMY = 60
SPEED_MUSHROOM = 60
SPEED_TURTLE = 120
INVULNERABLE_TIME = 0.6
FLAGPOLE_SIZE = (60, 150)
GOOMBA_SECONDS_REMOVED_AFTER_DEATH = 1

SPRITE_PATH = os.path.join("assets", "sprites")
SOUND_PATH = os.path.join("assets", "sounds")

FONT_BIG = pygame.font.Font(os.path.join("assets", "ARCADE_N.TTF"), 30)
FONT_MEDIUM = pygame.font.Font(os.path.join("assets", "ARCADE_N.TTF"), 20)
FONT_SMALL = pygame.font.Font(os.path.join("assets", "ARCADE_N.TTF"), 15)
FONT_MINI = pygame.font.Font(os.path.join("assets", "ARCADE_N.TTF"), 10)
FONT_STANDARD = pygame.font.Font(None, 30)

# Loading all sounds
mixer.music.load(os.path.join(SOUND_PATH, "SuperMarioBros.mp3"))
mixer.music.set_volume(0.3)
COIN_SOUND = mixer.Sound(os.path.join(SOUND_PATH, "smb_coin.wav"))
JUMP_SOUND = mixer.Sound(os.path.join(SOUND_PATH, "smb_jump-super.wav"))
KICK_SOUND = mixer.Sound(os.path.join(SOUND_PATH, "smb_kick.wav"))
DIE_SOUND = mixer.Sound(os.path.join(SOUND_PATH, "smb_mariodie.wav"))
POWERUP_SOUND = mixer.Sound(os.path.join(SOUND_PATH, "smb_powerup.wav"))
POWERUP_APPEARS_SOUND = mixer.Sound(os.path.join(SOUND_PATH, "smb_powerup_appears.wav"))
STAGE_CLEAR_SOUND = mixer.Sound(os.path.join(SOUND_PATH, "smb_stage_clear.wav"))