import pygame as pg

class Tileset:
    def __init__(self, path, tile_size=(16, 16)):
        self.path = path
        self.tile_size = tile_size
        self.tiles = []

        # processing
        self.image = pg.image.load(self.path)
        self.rect = self.image.get_rect()
        self.og_height_px = self.image.height
        self.og_width_px = self.image.width

        # calling methods
        self.make_tiles()

    def scale_by(self, amount=4):
        self.tiles = list(map(lambda x: pg.transform.scale(x, amount)))

    def make_tiles(self):
        self.tiles = []
        tile_width = self.size[0]
        tile_height = self.size[1]

        for x in range(0, self.rect.width, tile_width):
            for y in range(0, self.rect.height, tile_height):
                tile = pg.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)
