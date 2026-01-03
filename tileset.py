import pygame


class Tileset:
    def __init__(self, path, tile_size=(16, 16)):
        self.path = path
        self.tile_size = tile_size

        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect()

        self.tiles = []
        self.make_tiles()

    def make_tiles(self):
        self.tiles = []
        tile_width = self.size[0]
        tile_height = self.size[1]

        for x in range(0, self.rect.width, tile_width):
            for y in range(0, self.rect.height, tile_height):
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)
