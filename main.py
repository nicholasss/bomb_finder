import pygame as pg

# local files
from tileset import Tileset, TileType
from game import Game

# GLOBAL
SCREEN_SIZE = 800, 640
CENTER = SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2
NAME = "Bomb Finder"

# TILESET
TILE_SCALE = 4
TILE_SIZE = (16, 16)
TILE_PATH = "assets/asperite_files/basic-tileset.png"

# GAME
SCREEN_TILE = (TILE_SIZE[0] * TILE_SCALE, TILE_SIZE[1] * TILE_SCALE)
FPS = 60


def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption(NAME)
    clock = pg.time.Clock()
    pg.display.update()

    tileset = Tileset(TILE_PATH, TILE_SIZE, TILE_SCALE)
    game = Game(tileset, SCREEN_TILE, screen)
    pg.display.update()

    # create new game screen

    # select difficulty or mode

    # load the tile types
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONUP:
                print("Click at", event.pos)

        clock.tick(FPS)

    # exiting event loop to exit
    pg.quit()


if __name__ == "__main__":
    main()
