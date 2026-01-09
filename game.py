import random
import pygame as pg
from tileset import Tileset, TileType
from tile import Tile


class Game:
    def __init__(
        self,
        tileset: Tileset,
        tile_render_size: tuple[int, int],
        screen: pg.Surface,
        number_of_bombs: int,
        seed: int,
        grid_size: tuple[int, int],
        grid_top_left_corner: tuple[int, int] = (0, 0),
    ):
        """A game instance should returned a fully setup game, ready to play."""
        self.__tileset: Tileset = tileset
        self.__tile_render_size: tuple[int, int] = tile_render_size
        self.__screen: pg.Surface = screen

        self.__grid_cols = grid_size[0]
        self.__grid_rows = grid_size[1]
        self.__tile_grid: list[list[Tile]] = []

        # x, y of the top left corner of the grid
        self.__grid_location_x, self.__grid_location_y = grid_top_left_corner

        # number of bombs
        self.__seed: int = seed
        self.__number_of_bombs = number_of_bombs

        # create grid
        for x in range(self.__grid_cols):
            self.__tile_grid.append([])
            for _ in range(self.__grid_rows):
                self.__tile_grid[x].append(Tile())

        # seeding bombs
        random.seed(self.__seed)
        self.__place_bombs()

        # calculate numbers
        self.__count_all_bombs()

        # complete iniialization
        print("DEBUG: Game Initialized")

    def start_game(self, game_clock: pg.time.Clock, fps: int):
        """Start the main game loop"""

        # Main game loop
        running = True
        while running:
            # 1. Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.MOUSEBUTTONUP:
                    # left click
                    if event.button == 1:
                        self.__handle_left_click(event.pos)
                    # right click
                    elif event.button == 3:
                        self.__handle_right_click(event.pos)

            # 2. Update game state (game logic)
            # i.e. whether game won, game lost, tile flood occurs

            # 3. Render the game, after clearing it with a fill
            self.__screen.fill("black")
            self.__render_grid()

            # 4. Update display
            pg.display.flip()

            # 5. Limit the frame rate
            game_clock.tick(fps)

    def __render_grid(self):
        """Renders the grid during every frame"""
        for x in range(self.__grid_cols):
            for y in range(self.__grid_rows):
                tile_corner_x, tile_corner_y = (
                    (self.__tile_render_size[0] * x),
                    (self.__tile_render_size[1] * y),
                )

                # offset the grid by the topleft corner
                tile_loc = (
                    tile_corner_x + self.__grid_location_x,
                    tile_corner_y + self.__grid_location_y,
                )

                tile_state = self.__tile_grid[x][y].get_state()

                self.__screen.blit(self.__tileset.get_tile(tile_state), tile_loc)

    def __count_all_bombs(self):
        for x in range(self.__grid_cols):
            for y in range(self.__grid_rows):
                number_of_bombs = self.__count_bombs_one_tile((x, y))
                self.__tile_grid[x][y].set_number(number_of_bombs)

    def __count_bombs_one_tile(self, center_tile: tuple[int, int]) -> int:
        """Counts the bombs surrounding the tile in the center."""
        number_of_bombs = 0
        center_x, center_y = center_tile

        for x in range(-1, 2):
            for y in range(-1, 2):
                # iterate through the surrounding tiles
                tile_x, tile_y = center_x + x, center_y + y

                # skip looking at the center tile itself
                if x == 0 and y == 0:
                    continue

                # check if tile is too low outside grid
                elif tile_x < 0 or tile_y < 0:
                    continue

                # check if tile is too high outside grid
                elif tile_x >= self.__grid_rows or tile_y >= self.__grid_cols:
                    continue

                # check for bomb
                if self.__tile_grid[tile_x][tile_y].has_bomb():
                    number_of_bombs += 1

        return number_of_bombs

    def __place_bombs(self):
        """Places bombs pseudo-randomly, determined by seed and number of bombs requested."""
        bomb_coord_list = self.__make_bomb_list()
        for row, col in bomb_coord_list:
            self.__tile_grid[row][col].place_bomb()

    def __make_bomb_list(self) -> list[tuple[int, int]]:
        """Returns a list of coordinates where bombs will be placed, without duplicates."""
        bomb_coords = []
        while len(bomb_coords) < self.__number_of_bombs:
            new_bomb_coord = (
                random.randint(0, self.__grid_rows - 1),
                random.randint(0, self.__grid_cols - 1),
            )

            if new_bomb_coord not in bomb_coords:
                bomb_coords.append(new_bomb_coord)

        return bomb_coords

    def __handle_left_click(self, coord: tuple[int, int]):
        """Take the click, call the calculation method, then pass the click to the tile.
        The tile will change state, and then any changes to the grid should be made."""
        tile_clicked = self.__find_tile_from_click(coord)

        # left click was outside grid, do nothing
        if not self.__click_was_inside_grid(tile_clicked):
            print("NYI: Left click outside of tile grid")
            return

        clicked_x, clicked_y = tile_clicked
        clicked_tile = self.__tile_grid[clicked_x][clicked_y]

        # Print debugging
        # print(f"left click on tile ({clicked_x}, {clicked_y})")
        # if clicked_tile.has_bomb():
        #     print("DEBUG: tile has bomb")
        # else:
        #     print(f"DEBUG: tile has {clicked_tile.get_number()} bomb(s) next to it")

        # send click event to the tile
        clicked_tile.perform_left_click()

    def __handle_right_click(self, coord: tuple[int, int]):
        """Take the click, call the calculation method, then pass the click to the tile.
        The tile will change state, and then any changes to the grid should be made."""
        tile_clicked = self.__find_tile_from_click(coord)

        # right click was outside grid, do nothing
        if not self.__click_was_inside_grid(tile_clicked):
            print("NYI: Right click outside of tile grid")
            return

        clicked_x, clicked_y = tile_clicked
        clicked_tile = self.__tile_grid[clicked_x][clicked_y]

        # Print debugging
        # print(f"DEBUG: right click on tile ({clicked_x}, {clicked_y})")

        # if clicked_tile.has_bomb():
        #     print("DEBUG: tile has bomb")
        # else:
        #     print(f"DEBUG: tile has {clicked_tile.get_number()} bomb(s) next to it")

        # send click event to the tile
        clicked_tile.perform_right_click()

    def __click_was_inside_grid(self, tile_clicked: tuple[int, int]) -> bool:
        if tile_clicked[0] < 0 or tile_clicked[1] < 0:
            return False
        elif tile_clicked[0] >= self.__grid_cols or tile_clicked[1] >= self.__grid_rows:
            return False

        # if neither, then it is inside the grid
        return True

    def __find_tile_from_click(self, click_coord: tuple[int, int]) -> tuple[int, int]:
        """Converts screen coordinates to tile grid coordinates."""
        # click on the tile grid
        click_x, click_y = (
            click_coord[0] - self.__grid_location_x,
            click_coord[1] - self.__grid_location_y,
        )

        # tile number, floor divide the tile rendering size
        tile_x, tile_y = (
            click_x // self.__tile_render_size[0],
            click_y // self.__tile_render_size[1],
        )

        return (tile_x, tile_y)
