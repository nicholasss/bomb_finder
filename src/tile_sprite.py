from tileset import TileType, Tileset
import pygame as pg
from enum import Enum


# TODO:
# Move this Enum to the Tileset class file? or integrate into TileType?
class Flag(Enum):
    NO_FLAG = 0
    UNCERTAIN_FLAG = 1
    CERTAIN_FLAG = 2


class TileSprite(pg.sprite.Sprite):
    """
    Tile Sprite is a subclass of the pygame Sprite class.

    Instead of being a container for state that the game class uses, these tiles manage their own
    image (`pygame.Surface`) and its own rect (`pygame.Rect`). This design means we use simple methods
    to update state, and then utilize the `update` method to update the image (`pygame.Surface`).
    """

    def __init__(self, tileset: Tileset, x: float, y: float):
        super().__init__()
        # Tileset to use
        self.__tileset = tileset

        # Tile internal state
        self.__num_neighbors = 0
        self.__has_bomb = False
        self.__was_clicked = False
        self.__is_selected = False
        self.__flag_state = Flag.NO_FLAG
        self.__tile_type = TileType.UNCLICKED

        # Location of tile on screen
        self.__x = x
        self.__y = y

        # Sprite properties and placing on screen
        self.image: pg.Surface = self.__tileset.get_tile(self.__tile_type)
        self.rect: pg.Rect = self.image.get_rect()
        self.rect.topleft = self.__x, self.__y

    def update(self):
        """
        Every frame this will be called. It should take the state of the tile, and update
        `self.image` to the appropriate tile from the tileset. This is done by updating the
        `self.__tile_type`.
        """

        if self.__was_clicked:
            self.__tile_type = TileType.CLICKED_EMPTY

        self.image = self.__tileset.get_tile(self.__tile_type)

    def perform_select(self):
        # do not show blank tile if the tile was already revealed
        if self.__was_clicked:
            return
        self.__is_selected = True

    def perform_left_deselect(self):
        self.__is_selected = False

    def place_bomb(self):
        self.__has_bomb = True

    def has_bomb(self):
        return self.__has_bomb

    def is_empty(self):
        return not self.__has_bomb

    def set_neighbors(self, num_neighbors: int):
        self.__num_neighbors = num_neighbors
