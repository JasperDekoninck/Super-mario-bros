from CONSTANTS import *


class PlayMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

    def loop(self, world):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "game over"

            get_fps = self.clock.get_fps()
            if get_fps > 10:
                world.update(1 / get_fps)

            world.render(self.screen)

            if world.gameover:
                return "game over"

            text = FONT_MEDIUM.render("FPS: " + str(round(get_fps, 2)), True, pygame.Color('white'))
            self.screen.blit(text, (10, 10))
            if world.player is not None:
                coins_total = FONT_MEDIUM.render("Coins: " + str(world.player.coins), True, pygame.Color('white'))
                self.screen.blit(coins_total, (10, 50))
            pygame.display.update()
