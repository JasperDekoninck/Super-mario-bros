from mario import MainMenu, LevelMenu, PlayMenu, GameOverMenu, LevelCreatorMenu, AboutMenu, SettingsMenu, SCREEN_SIZE, mixer
import pygame

pygame.init()


def main():
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Super mario Bros")

    main_menu = MainMenu(screen)
    level_menu = LevelMenu(screen)
    play_menu = PlayMenu(screen)
    game_over_menu = GameOverMenu(screen)
    level_creator_menu = LevelCreatorMenu(screen)
    about_menu = AboutMenu(screen)
    settings_menu = SettingsMenu(screen)
    current_menu = "main"
    world = None
    mixer.music.play(-1, 0.0)
    if SettingsMenu.SETTINGS["Music"] == "off":
        mixer.music.pause()
    while True:
        if current_menu == "main":
            current_menu = main_menu.loop()
        elif current_menu == "level":
            current_menu, world, path = level_menu.loop()
        elif current_menu == "play":
            current_menu = play_menu.loop(world, path)
        elif current_menu == "game over":
            current_menu = game_over_menu.loop(world)
        elif current_menu == "creator":
            current_menu = level_creator_menu.loop()
        elif current_menu == "about":
            current_menu = about_menu.loop()
        elif current_menu == "settings":
            current_menu = settings_menu.loop()
        else:
            quit()


if __name__ == "__main__":
    main()