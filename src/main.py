import random
import pygame as pg

from tileset import Tileset
from game import Game

# General
NAME = "Bomb Finder"

# Graphics
SCREEN_SIZE = 800, 800
SCREEN_CENTER = SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2
TILE_SCALE = 4
TILE_SIZE = (16, 16)
TILE_RENDER_SIZE = (TILE_SIZE[0] * TILE_SCALE, TILE_SIZE[1] * TILE_SCALE)
TILE_PATH = "assets/asperite_files/basic-tileset.png"
FPS = 120

# Font
SOURCE_FONT_PATH = "./assets/fonts/SourceSansPro/SourcingSansPro-Regular.ttf"

# Debug
DEBUG_GAME = True

# Games
DEFAULT_GRID_SIZE = (6, 6)
DEFAULT_GRID_TOPLEFT = (200, 200)
DEFAULT_SEED = 0xABCDEF1234  # All seeds should be a 10 digit hexadecimal number
DEFAULT_NUMBER_BOMBS = 3


def main():
    # Initialization
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()
    font = pg.font.Font(SOURCE_FONT_PATH, 30)

    # Start rendering
    pg.display.set_caption(NAME)
    pg.display.update()

    tileset = Tileset(TILE_PATH, TILE_SIZE, TILE_SCALE)

    game = Game(
        tileset,
        TILE_RENDER_SIZE,
        screen,
        DEFAULT_NUMBER_BOMBS,
        random.Random(DEFAULT_SEED),
        font,
        DEFAULT_GRID_SIZE,
        DEFAULT_GRID_TOPLEFT,
        DEBUG_GAME,
    )

    # TESTING FOR NEW GRID CLASS
    # grid = Grid(
    #     tileset,
    #     TILE_RENDER_SIZE,
    #     screen,
    #     DEFAULT_NUMBER_BOMBS,
    #     random.Random(DEFAULT_SEED),
    #     font,
    #     DEFAULT_GRID_SIZE,
    #     grid_top_left_corner,
    #     DEBUG_GAME,
    # )

    # test_running = True
    # while test_running:
    #     pg.display.set_caption(f"FPS {int(clock.get_fps())} | {clock.get_time()}")

    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             test_running = False

    #     screen.fill("black")

    #     # call update and draw
    #     grid.all_tiles.update()
    #     grid.all_tiles.draw(screen)
    #     #

    #     pg.display.flip()
    #     clock.tick(FPS)

    # create new game screen

    # select difficulty or mode

    # load the tile types

    # Main game loop
    game.start_game(clock, FPS)

    # exiting event loop to exit
    pg.quit()


if __name__ == "__main__":
    main()
