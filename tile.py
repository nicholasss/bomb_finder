from enum import Enum
import pygame as pg
from tileset import TileType


class Flag(Enum):
    NO_FLAG = 0
    UNCERTAIN_FLAG = 1
    CERTAIN_FLAG = 2


class Tile:
    """Tile instances should store whether there is a bomb,
    whether it is clicked, whether there is a bomb, what type of flag,
    and how many neighboring bombs there are.
    We should know at initialization whether the tile has a bomb or not."""

    def __init__(self, has_bomb: bool = False):
        self.__has_bomb = has_bomb
        self.__neighboring_bombs = 0
        self.__flag_state = Flag.NO_FLAG
        self.__tile_type = TileType.UNCLICKED

        self.is_revealed = False

    def reveal(self) -> bool:
        """Perfroms a click on the tile.
        This will first mark the tile as clicked,"""

        # mark tile as revealed
        self.is_revealed = True

        # a tile cannot be flagged if it is revealed
        self.__flag_state = Flag.NO_FLAG

        # return whether there is a bomb or not
        return self.__has_bomb

    def get_state(self) -> TileType:
        return self.__tile_type

    def set_number(self, new_num: int):
        pass

    def place_bomb(self):
        self.__has_bomb = True

    def has_bomb(self) -> bool:
        return self.__has_bomb

    def cycle_flag(self) -> Flag:
        # 0 -> 1 -> 2 -> 3 ...
        self.__flag_state = Flag((self.__flag_state.value + 1) % 3)
        return self.__flag_state
