import pygame as pg

# local files
from tileset import Tileset

# GLOBAL
SCREEN_SIZE = 800, 640
CENTER = SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2
NAME = "Bomb Finder"

# TILES
TILE_SCALE = 4

def main():
    tileset_path = "./assets/basic-tileset.png"
    tileset = pg.image.load(tileset_path)

    scaled_tileset = pg.transform.scale(tileset, (160 * 4, 96 * 4))

    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption(NAME)

    scaled_tileset_rect = scaled_tileset.get_rect(center=CENTER)

    screen.blit(scaled_tileset, scaled_tileset_rect)
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
