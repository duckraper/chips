import pygame as pg
from mainmenu import MainMenu
from time import time
from sys import exit
from resources import FPS, game_icon, game_title
from game import Game
from traceback import print_exc

pg.init()
clock = pg.time.Clock()

pg.display.set_icon(game_icon)
pg.display.set_caption(game_title)

if __name__ == "__main__":
    try:
        main_menu = MainMenu()
        game = Game()

        frame_count = 0
        start_time = time()

        while main_menu.running:
            main_menu.get_input()
            main_menu.draw_menu()
            pg.display.flip()
            clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        if main_menu.selected_option == 0:
                            game.running = True
                            main_menu.running = False

        while game.running:
            game.run()
            pg.display.flip()
            clock.tick(FPS)

        pg.quit()
        exit(0)

    except Exception as error:
        print("Error:", error)
        print_exc()
        pg.quit()
        exit(1)
        