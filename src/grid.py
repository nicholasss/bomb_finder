import random
import pygame as pg
from tileset import TileType, Tileset
from tile_sprite import TileSprite
from utility import calculate_neighbors


# TODO: Test out rendering

# TODO: Once a tile has been clicked, remove it the group of unclicked tiles to stop rendered every frame


class Grid:
    """
    Grid is a sub-class of the pygame Group class, and will handle creation of the grid, management of the tile sprites,
    and will be created and used within a instance of the Game class.

    Many of the arguments within this constructor need to be instanciated before being passed in.
    """

    def __init__(
        self,
        tileset: Tileset,
        tile_render_size: tuple[float, float],
        screen: pg.Surface,
        numb_of_bombs: int,
        rng: random.Random,
        font: pg.Font,
        grid_size: tuple[int, int],
        grid_topleft: tuple[float, float] = (0, 0),
        debug_mode: bool = False,
    ):
        if debug_mode:
            print("DEBUG: Creating instance of Grid")

        # Properties
        self.__tileset = tileset
        self.__tile_render_width, self.__tile_render_height = tile_render_size
        self.__screen = screen
        self.__num_of_bombs = numb_of_bombs
        self.__rng = rng
        self.__grid_size = grid_size
        self.__font = font
        self.__grid_topleft = grid_topleft
        self.__debug_mode = debug_mode

        # Tile groups
        self.all_tiles = pg.sprite.Group()
        self.revealed_tiles = pg.sprite.Group()
        self.unrevealed_tiles = pg.sprite.Group()

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

    def __create_grid(self):
        """
        Creates the grid of tile sprites.

        In order to create a new TileSprite instance, we must calculate and provide the topleft corner as an argument.
        We do not need to provide a width and height to the tiles individually, the tileset has the same as the TileSprites.
        """

        for col in range(self.__grid_cols):
            self.__tile_grid.append([])
            for row in range(self.__grid_rows):
                tile_x = self.__grid_left + ((col + 1) * self.__tile_render_width)
                tile_y = self.__grid_top + ((row + 1) * self.__tile_render_height)
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
            if tile.is_empty():
                tile.place_bomb()
                placed_bombs += 1
            elif tile.has_bomb():
                continue

        # WARNING
        if placed_bombs != self.__num_of_bombs:
            print("WARNING: Error with number of bombs placed.")

    def __count_bombs(self):
        """
        For every tile in the grid, call the `calculate_neighbors` function and provide the tile with the number of neighbors.
        """

        for col in range(self.__grid_cols):
            for row in range(self.__grid_rows):
                num_neighbors = calculate_neighbors(
                    (col, row), self.__grid_cols, self.__grid_rows, self.__tile_grid
                )
                self.__tile_grid[col][row].set_neighbors(num_neighbors)
