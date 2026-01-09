from enum import Enum
from tileset import TileType


class Flag(Enum):
    NO_FLAG = 0
    UNCERTAIN_FLAG = 1
    CERTAIN_FLAG = 2


class Tile:
    """
    Tile instances should store whether there is a bomb,
    whether it is clicked, whether there is a bomb, what type of flag,
    and how many neighboring bombs there are.
    We should know at initialization whether the tile has a bomb or not.
    """

    def __init__(self, has_bomb: bool = False):
        self.__has_bomb = has_bomb
        self.__neighboring_bombs = 0
        self.__flag_state = Flag.NO_FLAG
        self.__tile_type = TileType.UNCLICKED
        self.__was_clicked = False
        self.__is_selected = False

    def __update_type(self):
        """
        Update the tiles 'TileType', at self.__tile_type, to reflect its current internal state.
        This method should be called every time a method is called that changes state.
        """
        # 1. look at non-clicked tile states
        if self.__is_selected:
            self.__tile_type = TileType.CLICKED_EMTPY

            return

        # 2. check hidden states and return early if its hidden
        if not self.__was_clicked:
            if self.__flag_state == Flag.NO_FLAG:
                self.__tile_type = TileType.UNCLICKED

            elif self.__flag_state == Flag.CERTAIN_FLAG:
                self.__tile_type = TileType.UNCLICKED_CERTAIN

            elif self.__flag_state == Flag.UNCERTAIN_FLAG:
                self.__tile_type = TileType.UNCLICKED_UNCERTAIN

            return

        # then looking at clicked tile states without bomb
        # 3. check clicked states without bomb
        if not self.__has_bomb:
            # print(
            #     f"DEBUG: nbombs={self.__neighboring_bombs} new_type={TileType(self.__neighboring_bombs + 1)}"
            # )
            self.__tile_type = TileType(self.__neighboring_bombs + 1)

            return

        # 3. clicked states with bomb
        # set to bomb first frame
        self.__tile_type = TileType.BOMB_A

    def perform_left_select(self):
        """
        Selects the tile, before the click is done.
        Should show as a blank tile.
        """
        self.__is_selected = True
        self.__update_type()

    def perform_left_deselect(self):
        """
        Deselects the tile.
        """
        self.__is_selected = False
        self.__update_type()

    def perform_left_click(self):
        """
        Perfroms a left click on the tile.
        We will first mark the tile as clicked and then update its state.
        """
        self.__was_clicked = True
        self.__flag_state = Flag.NO_FLAG
        self.__update_type()

    def perform_right_click(self):
        """
        Perfroms a right click on the tile.
        This will cycle through the flags.
        """
        self.__cycle_flag()
        self.__update_type()

        # print(
        #     f"DEBUG: tile updated to tile {self.__tile_type.value}: {self.__tile_type.name}"
        # )

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
