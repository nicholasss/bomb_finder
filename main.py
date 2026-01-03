import pygame as pg

# local files
from tileset import Tileset, TileType

# GLOBAL
SCREEN_SIZE = 800, 640
CENTER = SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2
NAME = "Bomb Finder"

# TILES
TILE_SCALE = 4
TILE_SIZE = (16, 16)
TILE_PATH = 'assets/basic-tileset.png'

def main():
    # initialization
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption(NAME)

    tileset = Tileset(TILE_PATH, TILE_SIZE, TILE_SCALE)

    unlicked_tile = tileset.get_tile(TileType.UNCLICKED)
    screen.blit(unlicked_tile, screen.get_rect())
    pg.display.update()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONUP:
                print("Clicked!")

    # exiting event loop
    pg.quit()


if __name__ == "__main__":
    main()
