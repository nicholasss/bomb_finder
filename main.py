import pygame

# local files
from tileset import Tileset


SCREEN_SIZE = 800, 640
CENTER = SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2
NAME = "Bomb Finder"


def main():
    tileset_path = "./assets/basic-tileset.png"
    tileset = pygame.image.load(tileset_path)
    scaled_tileset = pygame.transform.scale(tileset, (160 * 4, 96 * 4))

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(NAME)

    scaled_tileset_rect = scaled_tileset.get_rect(center=CENTER)

    screen.blit(scaled_tileset, scaled_tileset_rect)
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                print("Clicked!")

    # exiting event loop
    pygame.quit()


if __name__ == "__main__":
    main()
