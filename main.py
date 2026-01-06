import pygame as pg

from tileset import Tileset, TileType
from game import Game

# General
NAME = "Bomb Finder"

# Graphics
SCREEN_SIZE = 1200, 1200
SCREEN_CENTER = SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2
TILE_SCALE = 4
TILE_SIZE = (16, 16)
TILE_RENDER_SIZE = (TILE_SIZE[0] * TILE_SCALE, TILE_SIZE[1] * TILE_SCALE)
TILE_PATH = "assets/asperite_files/basic-tileset.png"
FPS = 60

# Games
DEFAULT_GRID_SIZE = (4, 4)
DEFAULT_SEED = 0xABCDEF1234  # All seeds should be a 10 digit hexadecimal number
DEFAULT_NUMBER_BOMBS = 3


def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption(NAME)
    clock = pg.time.Clock()
    pg.display.update()

    grid_top_left_corner = (100, 100)
    tileset = Tileset(TILE_PATH, TILE_SIZE, TILE_SCALE)
    game = Game(
        tileset,
        TILE_RENDER_SIZE,
        screen,
        DEFAULT_NUMBER_BOMBS,
        DEFAULT_SEED,
        DEFAULT_GRID_SIZE,
        grid_top_left_corner,
    )

    # create new game screen

    # select difficulty or mode

    # load the tile types

    # Main game loop
    game.start_game(clock, FPS)

    # exiting event loop to exit
    pg.quit()


if __name__ == "__main__":
    main()
