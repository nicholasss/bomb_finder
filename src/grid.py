import time
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
        self.__grid_topleft = grid_topleft
        self.__debug_mode = debug_mode

        # Tile groups
        self.all_tiles = pg.sprite.Group()

        # Grid
        self.__grid_left, self.__grid_top = self.__grid_topleft
        self.__grid_size = grid_size
        self.__grid_cols = self.__grid_size[0]
        self.__grid_rows = self.__grid_size[1]
        self.__tile_grid: list[list[TileSprite]] = []

        # Win state
        self.remaining_tiles_to_reveal = (
            self.__grid_cols * self.__grid_rows
        ) - self.__num_of_bombs
        self.flags_remaining = self.__num_of_bombs
        self.game_was_won: bool = False

        # Game timer
        self.first_click_occured_at: float | None = None
        self.__game_ended_at: float | None = None

        self.__first_click_occured: bool = False

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

        if not self.__first_click_occured:
            self.__first_click_occured = True
            self.first_click_occured_at = time.time()

        col, row = col_row_clicked
        tile_clicked = self.__tile_grid[col][row]

        if tile_clicked.has_flag() or tile_clicked.was_clicked:
            # Unable to reveal due to flag blocking reveal
            return True

        elif tile_clicked.has_bomb:
            # Reveal the bomb and end the game
            tile_clicked.reveal()
            self.__end_game(False)
            return False

        elif tile_clicked.no_neighboring_bombs():
            # Reveal many tiles and decrement tiles left to reveal
            num_tiles_revealed = self.__flood_tiles(col_row_clicked)
            # NOTE: the private method itself could handle decrementing num_tiles_revealed
            self.remaining_tiles_to_reveal -= num_tiles_revealed

        else:
            # Reveal single tile and decrement tiles left to reveal
            tile_clicked.reveal()
            self.remaining_tiles_to_reveal -= 1

        # Tile was revealed. Was it the last tile?
        if self.remaining_tiles_to_reveal <= 0:
            self.__end_game(True)

        return True

    def flag_click(self, col_row_clicked: tuple[int, int]):
        """
        Provided the column and row of the tile being flagged (or unflagged), cycle through the flag types on the tile.
        """

        col, row = col_row_clicked
        tile_clicked = self.__tile_grid[col][row]

        update_flag_count, tile_now_has_flag = tile_clicked.cycle_flag()

        if update_flag_count:
            if tile_now_has_flag:
                self.flags_remaining -= 1
            else:
                self.flags_remaining += 1

    def press_tile(self, col_row_clicked: tuple[int, int]):
        """
        Provided the column and row of a tile, change the tile to be "pressed".
        """

        col, row = col_row_clicked
        tile_clicked = self.__tile_grid[col][row]

        if tile_clicked.was_clicked or tile_clicked.has_flag():
            return

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

        Return how many tiles were revealed
        """

        num_revealed_tiles = 0

        to_visit_list: list[tuple[int, int]] = [first_tile]
        while len(to_visit_list) > 0:
            # 1. Always reveal the tile being visited, and increment the counter
            col, row = to_visit_list.pop()
            self.__tile_grid[col][row].reveal()
            num_revealed_tiles += 1

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

        return num_revealed_tiles

    def __end_game(self, player_won: bool) -> float:
        """
        End the game by calculating the time to clear the level.
        """

        self.__game_ended_at = time.time()
        if player_won:
            self.game_was_won = True
        else:
            return 0.0

        # Type guarding
        if type(self.first_click_occured_at) is not float:
            raise TypeError("Time of first click was not saved.")

        # calcluate and return game time
        game_time = self.__game_ended_at - self.first_click_occured_at

        print(f"DEBUG: Game Won!\nDEBUG: Grid took {game_time:.2f}s to complete.")
        return game_time
