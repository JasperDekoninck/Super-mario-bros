import pygame
from CONSTANTS import *
import os

pygame.init()

# This file is a bit different from all the rest: it is soly created to extract sprite images from the different
# sprite sheets used.

# LOADING BACKGROUNDS
background_images1 = pygame.image.load(os.path.join(SPRITE_PATH, "background.png"))
SIZE_BACKGROUND1 = (510, 492)
background_images2 = pygame.image.load(os.path.join(SPRITE_PATH, "background_snow.png"))
background_images3 = pygame.image.load(os.path.join(SPRITE_PATH, "background_castle.png"))

BACKGROUNDS = {
    "Grey1": background_images1.subsurface((3, 0, SIZE_BACKGROUND1[0] - 6, SIZE_BACKGROUND1[1] - 6)),
    "Sky1": background_images1.subsurface((9 + 2 * SIZE_BACKGROUND1[0], 0, SIZE_BACKGROUND1[0] - 7,
                                           SIZE_BACKGROUND1[1] - 9)),
    "Sky2": background_images1.subsurface((9 + 3 * SIZE_BACKGROUND1[0], 0, SIZE_BACKGROUND1[0] - 6,
                                           SIZE_BACKGROUND1[1] - 9)),
    "Grey2": background_images1.subsurface((3, SIZE_BACKGROUND1[1], SIZE_BACKGROUND1[0] - 6, SIZE_BACKGROUND1[1] - 6)),
    "Sky3": background_images1.subsurface((9 + 2 * SIZE_BACKGROUND1[0], SIZE_BACKGROUND1[1], SIZE_BACKGROUND1[0] - 7,
                                           SIZE_BACKGROUND1[1] - 9)),
    "Sky4": background_images1.subsurface((9 + 3 * SIZE_BACKGROUND1[0], SIZE_BACKGROUND1[1], SIZE_BACKGROUND1[0] - 6,
                                           SIZE_BACKGROUND1[1] - 9)),
    "Snow1": background_images2.subsurface((2, 3, SIZE_BACKGROUND1[0] - 4, SIZE_BACKGROUND1[1] - 4)),
    "Snow2": background_images2.subsurface((6 + SIZE_BACKGROUND1[0], 3, SIZE_BACKGROUND1[0] - 6, SIZE_BACKGROUND1[1] - 4)),
    "Snow3": background_images2.subsurface((6 + 2 * SIZE_BACKGROUND1[0], 3, SIZE_BACKGROUND1[0] - 6, SIZE_BACKGROUND1[1] - 4)),
    "Snow4": background_images2.subsurface((4, 4 + SIZE_BACKGROUND1[1], SIZE_BACKGROUND1[0] - 6, SIZE_BACKGROUND1[1] - 4)),
    "Snow5": background_images2.subsurface((6 + SIZE_BACKGROUND1[0], 4 + SIZE_BACKGROUND1[1], SIZE_BACKGROUND1[0] - 6, SIZE_BACKGROUND1[1] - 4))
}

for i in range(18):
    pos_ = ((i % 9) * SIZE_BACKGROUND1[0] + 10, (i // 9)* SIZE_BACKGROUND1[1] + 10)
    BACKGROUNDS["Castle" + str(i)] = background_images3.subsurface(pos_ + (SIZE_BACKGROUND1[0] - 12, SIZE_BACKGROUND1[1] - 12))

all = pygame.image.load(os.path.join(SPRITE_PATH, "all.png"))
tiles = pygame.image.load(os.path.join(SPRITE_PATH, "tiles transparent.png"))
mario = pygame.image.load(os.path.join(SPRITE_PATH, "Mario-2.png"))
goomba = pygame.image.load(os.path.join(SPRITE_PATH, "goomba.png"))
specials = pygame.image.load(os.path.join(SPRITE_PATH, "specials.png"))
koopatroopa_blue = pygame.image.load(os.path.join(SPRITE_PATH, "koopablue.gif"))
koopatroopa_green = pygame.image.load(os.path.join(SPRITE_PATH, "koopagreen.gif"))
koopatroopa_red = pygame.image.load(os.path.join(SPRITE_PATH, "koopared.gif"))

TILES_SPECIAl = {
    "yellow": tiles.subsurface((186, 23, 15, 15)),
    "blue": tiles.subsurface((203, 23, 15, 15)),
    "red": tiles.subsurface((220, 23, 15, 15))
}

TILES = {
    "brown brick": tiles.subsurface((186, 40, 15, 15)),
    "blue brick": tiles.subsurface((203, 40, 15, 15)),
    "red brick": tiles.subsurface((220, 40, 15, 15)),
    "brown solid": tiles.subsurface((186, 57, 15, 15)),
    "blue solid": tiles.subsurface((203, 57, 15, 15)),
    "grass 1": tiles.subsurface((17, 56, 15, 15)),
    "grass 2": tiles.subsurface((34, 56, 15, 15)),
    "grass 3": tiles.subsurface((51, 56, 15, 15)),
    "grass 4": tiles.subsurface((68, 56, 15, 15)),
    "subgrass 1": tiles.subsurface((17, 73, 15, 15)),
    "red solid": tiles.subsurface((220, 57, 15, 15)),
    "gold block": tiles.subsurface((169, 23, 15, 15)),
    "ruby block": tiles.subsurface((169, 40, 15, 15)),
    "white block": tiles.subsurface((169, 57, 15, 15)),
    "green angry block": tiles.subsurface((169, 74, 15, 15)),
    "ice normal": tiles.subsurface((217, 234, 15, 15)),
    "ice corner 1": tiles.subsurface((201, 218, 15, 15)),
    "ice corner 2": tiles.subsurface((252, 269, 15, 15)),
    "ice corner 3": tiles.subsurface((253, 218, 15, 15)),
    "ice corner 4": tiles.subsurface((201, 269, 15, 15)),
    "ice side 1": tiles.subsurface((201, 234, 15, 15)),
    "ice side 2": tiles.subsurface((217, 218, 15, 15)),
    "ice side 3": tiles.subsurface((252, 234, 15, 15)),
    "ice side 4": tiles.subsurface((217, 269, 15, 15)),
    "sky grass 1": tiles.subsurface((322, 152, 15, 15)),
    "sky grass 2": tiles.subsurface((339, 152, 15, 15)),
    "sky grass 3": tiles.subsurface((356, 152, 15, 15)),
    "sky grass 4": tiles.subsurface((373, 152, 15, 15)),
    "sky ground 1": tiles.subsurface((322, 167, 15, 15)),
    "sky ground 2": tiles.subsurface((339, 167, 15, 15)),
    "sky ground 3": tiles.subsurface((356, 167, 15, 15)),
    "sky ground 4": tiles.subsurface((373, 167, 15, 15)),
    "snow 1": tiles.subsurface((191, 562, 15, 15)),
    "snow 2": tiles.subsurface((208, 562, 15, 15)),
    "snow 3": tiles.subsurface((225, 562, 15, 15)),
    "snow 4": tiles.subsurface((242, 562, 15, 15)),
    "snow ground": tiles.subsurface((191, 579, 15, 15)),
    "purple 1": tiles.subsurface((161, 305, 15, 15)),
    "purple 2": tiles.subsurface((178, 305, 15, 15)),
    "purple 3": tiles.subsurface((178, 322, 15, 15)),
    "brown 1": tiles.subsurface((298, 305, 15, 15)),
    "brown 2": tiles.subsurface((315, 305, 15, 15)),
    "brown 3": tiles.subsurface((315, 322, 15, 15)),
    "mud 1": tiles.subsurface((100, 470, 15, 15)),
    "mud 2": tiles.subsurface((100, 487, 15, 15))
}

PIPE = all.subsurface((67, 76, 200, 33))

GOOMBA = [
    all.subsurface((297 + 19 * i, 122, 19, 20)) for i in range(4)
]

for i in range(5, 9):
    GOOMBA.append(all.subsurface((298 + 19 * i, 122, 19, 20)))

GOOMBA_DEATH = all.subsurface((297, 153, 25, 10))

KOOPA = {
    "blue": [
        koopatroopa_blue.subsurface((0, 2 + 32 * i, 16, 31)) for i in range(16)
    ],
    "green": [
        koopatroopa_green.subsurface((0, 2 + 32 * i, 16, 31)) for i in range(16)
    ],
    "red": [
        koopatroopa_red.subsurface((0, 2 + 32 * i, 16, 31)) for i in range(16)
    ]
}

FLYING_KOOPA = {
    "blue": {

    },
    "red": {

    },
    "green": {

    }
}

KOOPA_TURTLE = {
    "blue": [
        koopatroopa_blue.subsurface((0, 513 + 16 * i, 16, 16)) for i in range(3)
    ],
    "green": [
        koopatroopa_green.subsurface((0, 513 + 16 * i, 16, 16)) for i in range(3)
    ],
    "red": [
        koopatroopa_red.subsurface((0, 513 + 16 * i, 16, 16)) for i in range(3)
    ]
}

MARIO_STILL = mario.subsurface((697, 10, 15, 32))
MARIO_DUCK = mario.subsurface((551, 106, 18, 18))
MARIO_RUNNING = []

begin_image = None
for i in range(0, 645):
    all_black = True
    for j in range(51, 85):
        if sum(mario.get_at((i, j))) > 255:
            all_black = False
            break
    if all_black and begin_image is not None:
        MARIO_RUNNING.append(mario.subsurface((begin_image, 51, i - begin_image, 34)))
        begin_image = None
    elif not all_black and begin_image is None:
        begin_image = i

MARIO_FLAGPOLE = []

begin_image = None
for i in range(388, 668):
    all_black = True
    for j in range(185, 220):
        if sum(mario.get_at((i, j))) > 255:
            all_black = False
            break
    if all_black and begin_image is not None:
        MARIO_FLAGPOLE.append(mario.subsurface((begin_image, 185, i - begin_image, 31)))
        begin_image = None
    elif not all_black and begin_image is None:
        begin_image = i

FLAGPOLE = pygame.image.load(os.path.join(SPRITE_PATH, "flagpole.png"))

SPECIALS = {
    "red mushroom": specials.subsurface((1, 1, 38, 38)),
    "blue mushroom": specials.subsurface((40, 1, 38, 38)),
    "flower": specials.subsurface((1, 40, 38, 38)),
    "star": specials.subsurface((40, 40, 38, 38))
}

COINS = [
    tiles.subsurface((291, 1291, 15, 16)),
    tiles.subsurface((308, 1291, 15, 16)),
    tiles.subsurface((325, 1291, 15, 16))
]

BACKGROUND_SPRITES = {
    "big bush": tiles.subsurface((3, 98, 90, 45)),
    "small bush 1": tiles.subsurface((2, 20, 35, 30)),
    "small bush 2": tiles.subsurface((96, 113, 35, 25)),
    "flower 1": tiles.subsurface((40, 20, 27, 30)),
    "flower 2": tiles.subsurface((70, 22, 30, 30)),
    "flower 3": tiles.subsurface((104, 38, 30, 22)),
    "mushroom": tiles.subsurface((101, 22, 36, 12)),
    "fence": tiles.subsurface((101, 60, 35, 20)),
    "castle": mario.subsurface((310, 465, 100, 100)),
    "cloud": pygame.transform.rotate(tiles.subsurface((278, 254, 82, 32)), 180)
}

if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 800))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            print(pygame.mouse.get_pos())

        #screen.blit(mario, (0, 0))
        pygame.draw.rect(screen, 255, (0, 0, 60, 100))
        screen.blit(pygame.transform.scale(MARIO_STILL, (60, 100)), (0, 0))

        pygame.display.update()
