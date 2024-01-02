import pygame as pg
from data.gui.mainmenu import MainMenu
from time import time
from sys import exit
from resources import FPS, game_icon, game_title
from game import Game
from traceback import print_exc
from debug import debug

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
            main_menu.update()
            main_menu.draw_menu()
            if main_menu.get() is not None:
                # START
                if main_menu.get() == "PvP":
                    game.running = True
                    main_menu.running = False
                # OPTIONS
                elif main_menu.get() == "Options":
                    pass
                # EXIT
                elif main_menu.get() == "Quit":
                    main_menu.running = False
                    break

            pg.display.flip()
            clock.tick(FPS)

        if game.running:
            game.countdown()
            pg.event.clear()

            while game.running:
                game.run()
                pg.display.flip()
                clock.tick(FPS)
                debug(clock.get_fps())

        pg.quit()
        exit(0)

    except Exception as error:
        print("Error:", error)
        print_exc()
        pg.quit()
        exit(1)
