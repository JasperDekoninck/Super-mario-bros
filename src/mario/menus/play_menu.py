from ..constants import *
from .menu import Menu


class PlayMenu(Menu):
    def __init__(self, screen):
        """
        Initializes a new instance of the PlayMenu class.

        Args:
            screen: The screen object to display the menu on.
        """
        super(PlayMenu, self).__init__(screen)

    def loop(self, world, file=None):
        """
        Main loop for the play menu.

        Args:
            world (World): The game world.
            file (str, optional): The file to save the top score. Defaults to None.

        Returns:
            str: The result of the loop, either "game over" or None.
        """
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
                if file is not None:
                    world.save_top_score(file)
                return "game over"

            text = FONT_MEDIUM.render("FPS: " + str(round(get_fps, 2)), True, pygame.Color('white'))
            self.screen.blit(text, (10, 10))
            if world.player is not None:
                coins_total = FONT_MEDIUM.render("Coins: " + str(world.player.coins), True, pygame.Color('white'))
                score_total = FONT_MEDIUM.render("Score: " + str(world.player.score), True, pygame.Color('white'))
                top_score = FONT_MEDIUM.render("Top Score: " + str(world.top_score), True, pygame.Color('white'))
                self.screen.blit(coins_total, (10, 50))
                self.screen.blit(score_total, (10, 90))
                self.screen.blit(top_score, (10, 130))
            pygame.display.update()
