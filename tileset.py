from enum import Enum
import pygame as pg


class TileType(Enum):
    # First row
    UNCLICKED = 0  # Not clicked yet
    CLICKED_EMTPY = 1  # Clicked with no number
    CLICKED_ONE = 2
    CLICKED_TWO = 3
    CLICKED_THREE = 4
    CLICKED_FOUR = 5
    CLICKED_FIVE = 6

    # Second row

    CLICKED_FOUND = 10
    CLICKED_CLUE = 11
    UNCLICKED_FOUND = 12
    UNCLICKED_CLUE = 13


class Tileset:
    def __init__(self, path, tile_size=(16, 16), scale=4):
        self.path: str = path
        self.tile_size: tuple[int, int] = tile_size
        self.tiles: list[pg.Surface] = []
        self.scale: int = scale

        # processing
        self.image: pg.Surface = pg.image.load(self.path)
        self.rect: pg.Rect = self.image.get_rect()
        self.og_height_px: int = self.image.height
        self.og_width_px: int = self.image.width

        # calling methods
        self.make_tiles()
        self.scale_by(scale)

    def make_tiles(self):
        self.tiles = []
        tile_width = self.tile_size[0]
        tile_height = self.tile_size[1]

        for x in range(0, self.rect.width, tile_width):
            for y in range(0, self.rect.height, tile_height):
                tile = pg.Surface(self.tile_size)
                tile.blit(self.image, (0, 0), (x, y, *self.tile_size))
                self.tiles.append(tile)

    def scale_by(self, scale):
        self.tiles = [
            pg.transform.scale(
                tile, (int(tile.get_width() * scale), int(tile.get_height() * scale))
            )
            for tile in self.tiles
        ]

    def get_tile(self, type: TileType) -> pg.Surface:
        return self.tiles[type.value]
