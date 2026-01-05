import pygame as pg
from tileset import Tileset, TileType
from tile import Tile


class Game:
    def __init__(
        self,
        tileset: Tileset,
        tile_render_size: tuple[int, int],
        screen: pg.Surface,
        seed: int,
        grid_size: tuple[int, int],
        grid_top_left_corner: tuple[int, int] = (0, 0),
    ):
        """A game instance should returned a fully setup game, ready to play."""
        self.__tileset: Tileset = tileset
        self.__tile_render_size: tuple[int, int] = tile_render_size
        self.__screen: pg.Surface = screen
        self.__seed: int = seed

        self.__grid_cols = grid_size[0]
        self.__grid_rows = grid_size[1]
        self.__tile_grid: list[list[Tile]] = []

        # x, y of the top left corner of the grid
        self.__grid_location_x, self.__grid_location_y = grid_top_left_corner

        # create grid
        for x in range(self.__grid_cols):
            self.__tile_grid.append([])
            for y in range(self.__grid_rows):
                self.__tile_grid[x].append(Tile())

        # seeding bombs

        pg.display.flip()
        print("Game Initialized")

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

            # 2. Update game state

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

    def __handle_left_click(self, coord: tuple[int, int]):
        """Take the click, call the calculation method, then pass the click to the tile.
        The tile will change state, and then any changes to the grid should be made."""
        tile_clicked = self.__find_tile_from_click(coord)

        # left click was outside grid, do nothing
        if not self.__click_was_inside_grid(tile_clicked):
            print("NYI: Left click outside of tile grid")
            return

        print(f"left click on tile ({tile_clicked[0]}, {tile_clicked[1]})")

    def __handle_right_click(self, coord: tuple[int, int]):
        """Take the click, call the calculation method, then pass the click to the tile.
        The tile will change state, and then any changes to the grid should be made."""
        tile_clicked = self.__find_tile_from_click(coord)

        # right click was outside grid, do nothing
        if not self.__click_was_inside_grid(tile_clicked):
            print("NYI: Right click outside of tile grid")
            return

        print(f"right click on tile ({tile_clicked[0]}, {tile_clicked[1]})")

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
