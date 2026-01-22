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
        self.__prev_type = TileType.UNCLICKED
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

        # if self.__is_selected:
        #     self.__tile_type = TileType.CLICKED_EMPTY
        # elif not self.__is_selected and not self.__was_clicked:
        #     self.__tile_type = TileType.UNCLICKED

        self.image = self.__tileset.get_tile(self.__tile_type)

    def reveal(self):
        """
        Reveal the tile, utilizing the internal state to change the TileType to render within the same frame.

        Revealing a tile will only show an empty tile, a number, or a bomb. It will remove any flags that were on it.
        """

        # Warning debug
        if self.__num_neighbors > 8:
            print(
                f"WARNING: neighboring bombs of cell at {(self.__x, self.__y)} is more than 8. neigbors with bombs->{self.__num_neighbors}"
            )
        # NOTE: Could add additional warninga here to check for known state?

        if self.__has_bomb:
            # TODO: Only the first frame of the bomb, needs to kick off animation somehow?
            # Unsure where to trigger and perform the animation
            self.__tile_type = TileType.BOMB_A
            return

        # Tile does not have a bomb
        if self.__num_neighbors == 0:
            self.__tile_type = TileType.CLICKED_EMPTY

        elif self.__num_neighbors >= 1:
            self.__tile_type = TileType(self.__num_neighbors + 1)

    def cycle_flag(self):
        """
        Cycle the flag state of the tile. Certain Flag -> Uncertain Flag -> Unflagged -> Certain Flag, etc.

        12 = Certain Flag
        13 = Uncertain Flag
        0  = Unflagged
        """

        if self.__tile_type == TileType.UNCLICKED_CERTAIN:
            self.__tile_type = TileType.UNCLICKED_UNCERTAIN

        elif self.__tile_type == TileType.UNCLICKED_UNCERTAIN:
            self.__tile_type = TileType.UNCLICKED

        elif self.__tile_type == TileType.UNCLICKED:
            self.__tile_type = TileType.UNCLICKED_CERTAIN

    def perform_select(self):
        # do not show blank tile if the tile was already revealed
        if self.__was_clicked:
            return
        # self.__is_selected = True

        self.__prev_type = self.__tile_type
        self.__tile_type = TileType.CLICKED_EMPTY

    def perform_deselect(self):
        # self.__is_selected = False

        self.__tile_type = self.__prev_type

    def place_bomb(self):
        self.__has_bomb = True

    def has_bomb(self) -> bool:
        return self.__has_bomb

    def has_no_bomb(self) -> bool:
        return not self.__has_bomb

    def set_neighbors(self, num_neighbors: int):
        self.__num_neighbors = num_neighbors

    def has_no_neighbors(self) -> bool:
        if self.__num_neighbors == 0:
            return True
        else:
            return False
