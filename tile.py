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

        self.was_clicked = False

    def __update_type(self):
        # 1. check hidden states and return early if its hidden
        if not self.was_clicked:
            if self.__flag_state == Flag.NO_FLAG:
                self.__tile_type = TileType.UNCLICKED

            elif self.__flag_state == Flag.CERTAIN_FLAG:
                self.__tile_type = TileType.UNCLICKED_CERTAIN

            elif self.__flag_state == Flag.UNCERTAIN_FLAG:
                self.__tile_type = TileType.UNCLICKED_UNCERTAIN

            return

        # 2. check clicked states, tile is not hidden
        # 2a. first render bombs

    def perform_left_click(self) -> bool:
        """Perfroms a left click on the tile. This will first mark the tile as revealed,
        then will update internal flag state.
        Finally it will return whether the click was on a bomb."""
        self.was_clicked = True
        # a tile cannot be flagged if it is revealed
        self.__flag_state = Flag.NO_FLAG

        # update type
        self.__update_type()

        # NOTE: I think the logic for the following two should be in Game class, but unsure of how to provide the 'trigger'
        if self.__has_bomb:
            print("NYI: Game over due to clicking on bomb")
            return True

        if self.__neighboring_bombs == 0:
            print("NYI: Flood all empty tiles, and surrounding number tiles.")

        # not clicked on bomb
        return False

    def perform_right_click(self):
        """Perfroms a right click on the tile.
        This will cycle through the flags."""
        self.__cycle_flag()
        self.__update_type()

        print(
            f"DEBUG: tile updated to tile {self.__tile_type.value}: {self.__tile_type.name}"
        )

    def get_state(self) -> TileType:
        return self.__tile_type

    def set_number(self, new_num: int):
        self.__neighboring_bombs = new_num

    def get_number(self) -> int:
        return self.__neighboring_bombs

    def place_bomb(self):
        self.__has_bomb = True

    def has_bomb(self) -> bool:
        return self.__has_bomb

    def __cycle_flag(self) -> Flag:
        # 0 -> 1 -> 2 -> 3 ...
        self.__flag_state = Flag((self.__flag_state.value - 1) % 3)
        return self.__flag_state
