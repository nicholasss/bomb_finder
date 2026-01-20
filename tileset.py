from enum import Enum
import pygame as pg


class TileType(Enum):
    # First row
    UNCLICKED = 0  # Not clicked yet
    CLICKED_EMPTY = 1  # Clicked with no number
    CLICKED_ONE = 2
    CLICKED_TWO = 3
    CLICKED_THREE = 4
    CLICKED_FOUR = 5
    CLICKED_FIVE = 6
    CLICKED_SIX = 7
    CLICKED_SEVEN = 8
    CLICKED_EIGHT = 9
    # Second row
    CLICKED_CERTAIN = 10
    CLICKED_UNCERTAIN = 11
    UNCLICKED_CERTAIN = 12
    UNCLICKED_UNCERTAIN = 13
    # Third row
    BOMB_A = 20
    BOMB_B = 21
    BOMB_C = 22
    BOMB_D = 23
    BOMB_E = 24
    BOMB_F = 25
    BOMB_G = 26
    BOMB_H = 27
    BOMB_I = 28
    BOMB_J = 29
    BOMB_K = 38
    BOMB_L = 39
    BOMB_M = 48
    BOMB_N = 49


class Tileset:
    def __init__(self, path, tile_size=(16, 16), scale=4):
        self.path: str = path
        self.tile_size: tuple[int, int] = tile_size
        self.tiles: list[pg.Surface] = []
        self.scale: int = scale

        # processing
        self.image: pg.Surface = pg.image.load(self.path).convert()
        self.rect: pg.Rect = self.image.get_rect()
        self.og_height_px: int = self.image.height
        self.og_width_px: int = self.image.width

        # calling methods
        self.__make_tiles()
        self.__scale_by(scale)

    def __make_tiles(self):
        self.tiles = []
        tile_width = self.tile_size[0]
        tile_height = self.tile_size[1]

        # iterates from top left corner, to top right corner, then down a row
        for row in range(0, self.rect.height, tile_height):
            for col in range(0, self.rect.width, tile_width):
                tile_image = pg.Surface(self.tile_size)
                tile_image.blit(self.image, (0, 0), (col, row, *self.tile_size))
                self.tiles.append(tile_image.convert())

    def __scale_by(self, scale):
        self.tiles = [
            pg.transform.scale(
                tile, (int(tile.get_width() * scale), int(tile.get_height() * scale))
            ).convert()
            for tile in self.tiles
        ]

    def get_tile(self, type: TileType) -> pg.Surface:
        return self.tiles[type.value]
