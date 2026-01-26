import random
import pygame as pg
from tileset import Tileset
from tile_sprite import TileSprite
from utility import calculate_neighbors


class Grid:
    """
    Grid will handle creation of the grid, management of the tile sprites, and manage the tile grid.
    and will be created and used within a instance of the Game class.

    Many of the arguments within this constructor need to be instantiated before being passed in.
    """

    def __init__(
        self,
        tileset: Tileset,
        tile_render_size: tuple[int, int],
        screen: pg.Surface,
        num_of_bombs: int,
        rng: random.Random,
        font: pg.Font,
        grid_size: tuple[int, int],
        grid_topleft: tuple[int, int],
        debug_mode: bool = False,
    ):
        if debug_mode:
            print("DEBUG: Creating instance of Grid")

        # Properties
        self.__tileset = tileset
        self.__tile_render_width, self.__tile_render_height = tile_render_size
        self.__screen = screen
        self.__num_of_bombs = num_of_bombs
        self.__rng = rng
        self.__font = font
        self.__grid_size = grid_size
        self.__grid_topleft = grid_topleft
        self.__debug_mode = debug_mode

        # Tile groups
        self.all_tiles = pg.sprite.Group()

        # Grid
        self.__grid_left, self.__grid_top = self.__grid_topleft
        self.__grid_cols = grid_size[0]
        self.__grid_rows = grid_size[1]
        self.__tile_grid: list[list[TileSprite]] = []

        # Initialization methods
        if self.__debug_mode:
            print("DEBUG: Beginning initialization")
        self.__create_grid()
        self.__place_bombs()
        self.__count_bombs()

        # DEBUG
        if self.__debug_mode:
            print("DEBUG: Grid has been initialized successfully.")

    # == Public Methods ==
    def reveal_click(self, col_row_clicked: tuple[int, int]) -> bool:
        """
        Provided the column and row of the tile revealed, perform the reveal of the tile, flooding neighboring tiles if empty,
        updating the TileSprite's state as needed.

        Returning `False` if the game is over due to revealing a bomb, or returning `True` if a bomb was **not** revealed
        and the game can continue.
        """

        col, row = col_row_clicked
        tile_clicked = self.__tile_grid[col][row]

        if tile_clicked.no_neighboring_bombs():
            if self.__debug_mode:
                print("DEBUG: Flood tiles")
            self.__flood_tiles(col_row_clicked)
        else:
            tile_clicked.reveal()
        return tile_clicked.has_no_bomb()

    def flag_click(self, col_row_clicked: tuple[int, int]):
        """
        Provided the column and row of the tile being flagged (or unflagged), cycle through the flag types on the tile.
        """

        col, row = col_row_clicked
        tile_clicked = self.__tile_grid[col][row]

        tile_clicked.cycle_flag()

    def press_tile(self, col_row_clicked: tuple[int, int]):
        """
        Provided the column and row of a tile, change the tile to be "pressed".
        """

        col, row = col_row_clicked
        tile_clicked = self.__tile_grid[col][row]

        if not tile_clicked.was_clicked:
            tile_clicked.press()

    def unpress_tile(self, col_row_clicked: tuple[int, int]):
        """
        Resets the "pressed" state tile at column and row
        """

        col, row = col_row_clicked
        tile_clicked = self.__tile_grid[col][row]

        tile_clicked.unpress()

    # == Private Methods ==
    def __create_grid(self):
        """
        Creates the grid of tile sprites.

        In order to create a new TileSprite instance, we must calculate and provide the topleft corner as an argument.
        We do not need to provide a width and height to the tiles individually, the tileset has the same as the TileSprites.
        """

        for col in range(self.__grid_cols):
            self.__tile_grid.append([])
            for row in range(self.__grid_rows):
                tile_x = self.__grid_left + (col * self.__tile_render_width)
                tile_y = self.__grid_top + (row * self.__tile_render_height)
                new_tile = TileSprite(self.__tileset, tile_x, tile_y)

                self.all_tiles.add(new_tile)
                self.__tile_grid[col].append(new_tile)

    def __place_bombs(self):
        """
        Places bombs across the grid utilizing the provided `self.__rng` instance, shared across the entire game.
        """

        placed_bombs = 0
        while placed_bombs < self.__num_of_bombs:
            # DEBUG
            if self.__debug_mode:
                print(
                    f"DEBUG: Bombs needed: {self.__num_of_bombs}, Bombs placed: {placed_bombs}"
                )

            # should never calculate outside of grid
            bomb_col, bomb_row = (
                self.__rng.randint(0, self.__grid_cols - 1),
                self.__rng.randint(0, self.__grid_rows - 1),
            )

            tile = self.__tile_grid[bomb_col][bomb_row]
            if tile.has_no_bomb():
                tile.place_bomb()
                placed_bombs += 1
            elif tile.has_bomb:
                continue

        # WARNING
        if placed_bombs != self.__num_of_bombs:
            print("WARNING: Error with number of bombs placed.")

    def __count_bombs(self):
        """
        For every tile in the grid, call the `calculate_neighbors` function and provide the tile with the number of neighbors.
        """

        # TODO: Optimize by skipping calculations for tiles that have bombs

        for col in range(self.__grid_cols):
            for row in range(self.__grid_rows):
                num_neighbors = calculate_neighbors(
                    (col, row), self.__grid_cols, self.__grid_rows, self.__tile_grid
                )
                self.__tile_grid[col][row].set_neighbors(num_neighbors)

    def __flood_tiles(self, first_tile: tuple[int, int]):
        """
        Starting at the first tile, that will not have any neighbors, this algorithm will reveal any tile that is
        neighboring the empty tiles.
        """

        print("DEBUG: Flood tiles function")

        to_visit_list: list[tuple[int, int]] = [first_tile]
        while len(to_visit_list) > 0:
            print(f"DEBUG: tiles to visit: {len(to_visit_list)}")

            # 1. Always reveal the tile being visited
            col, row = to_visit_list.pop()
            self.__tile_grid[col][row].reveal()

            print(f"DEBUG: Checking neighbors of {(col, row)}")

            # 2. Then check if we look at its neighbors
            if self.__tile_grid[col][row].no_neighboring_bombs():
                for col_change in range(-1, 2):
                    for row_change in range(-1, 2):
                        check_col, check_row = col + col_change, row + row_change

                        # A. Don't recheck the same tile
                        if col_change == 0 and row_change == 0:
                            continue

                        # B. Don't look outside of the grid
                        outside_grid = (
                            check_col < 0
                            or check_row < 0
                            or check_col >= self.__grid_cols
                            or check_row >= self.__grid_rows
                        )
                        if outside_grid:
                            continue

                        # C. Don't add it if its already in the list
                        next_tile_visit = (check_col, check_row)
                        if next_tile_visit in to_visit_list:
                            continue

                        # D. Don't add it if its already revealed
                        if self.__tile_grid[check_col][check_row].was_clicked:
                            continue

                        # E. Add to the list
                        to_visit_list.append((check_col, check_row))
