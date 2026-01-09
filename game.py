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
        """
        A game instance should returned a fully setup game, ready to play.
        """
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
        """
        Start the main game loop
        """
        continue_game = True
        while continue_game:
            # 1. Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    continue_game = False

                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        # if there is a bomb at tile, the game will end
                        continue_game = self.__handle_left_click(event.pos)
                    elif event.button == 3:
                        self.__handle_right_click(event.pos)

            # 2. clear the screen
            self.__screen.fill("black")

            # 3. Render the grid
            self.__render_grid()

            # 4. Update display
            pg.display.flip()

            # 5. Limit the frame rate
            game_clock.tick(fps)

    def __render_grid(self):
        """
        Renders the grid during every frame
        """
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
        """
        Counts the bombs surrounding the tile in the center.
        """
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
        """
        Places bombs pseudo-randomly, determined by seed and number of bombs requested.
        """
        bomb_coord_list = self.__make_bomb_list()
        for row, col in bomb_coord_list:
            self.__tile_grid[row][col].place_bomb()

    def __make_bomb_list(self) -> list[tuple[int, int]]:
        """
        Returns a list of coordinates where bombs will be placed, without duplicates.
        """
        bomb_coords = []
        while len(bomb_coords) < self.__number_of_bombs:
            new_bomb_coord = (
                random.randint(0, self.__grid_rows - 1),
                random.randint(0, self.__grid_cols - 1),
            )

            if new_bomb_coord not in bomb_coords:
                bomb_coords.append(new_bomb_coord)

        return bomb_coords

    def __make_tile_flood_reveal_list(
        self, first_tile: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """
        From a starting coordinate of 'first_tile', find all adjascent tiles that need to be revealed.
        Utilizing a DFS algorithm.
        """

        # tiles_to_visit and tiles_to_reveal start with the first_tile
        tiles_to_visit: list[tuple[int, int]] = [first_tile]
        tiles_to_reveal: list[tuple[int, int]] = [first_tile]

        # TODO: write DFS algo
        #
        # remove last (fifo) tile from to_visit list and visit it
        while len(tiles_to_visit) > 0:
            tile_being_visited = tiles_to_visit.pop()
            tile_visit_x, tile_visit_y = tile_being_visited

            # 1. check if empty tile
            if self.__tile_grid[tile_visit_x][tile_visit_y].get_number() <= 0:
                # 2. IF it is tile with 0, then add to to_visit and...
                if tile_being_visited not in tiles_to_reveal:
                    tiles_to_reveal.append(tile_being_visited)

                # iterate through and add surrounding tiles to_reveal list
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        # iterate through the surrounding tiles
                        tile_x, tile_y = tile_visit_x + x, tile_visit_y + y

                        # skip looking at the center tile itself
                        if x == 0 and y == 0:
                            continue

                        # check if tile is too low outside grid
                        elif tile_x < 0 or tile_y < 0:
                            continue

                        # check if tile is too high outside grid
                        elif tile_x >= self.__grid_rows or tile_y >= self.__grid_cols:
                            continue

                        # add to to_reveal list
                        tile_coord = (tile_x, tile_y)
                        if tile_coord not in tiles_to_reveal:
                            tiles_to_reveal.append(tile_coord)
                            tiles_to_visit.append(tile_coord)

            # its not an empty tile, only add to tiles_to_reveal, do not check surrounding tiles
            if tile_being_visited not in tiles_to_reveal:
                tiles_to_reveal.append(tile_being_visited)

        return tiles_to_reveal

    def __handle_left_click(self, coord: tuple[int, int]) -> bool:
        """
        Take the click, call the calculation method, then pass the click to the tile.
        The tile will change state, and then any changes to the grid should be made.

        This method will return a boolean, to indicate whether to continue the game or not.
        True: continue the game
        False: game is over
        """
        clicked_tile_coord = self.__find_tile_from_click(coord)

        # left click was outside grid, do nothing
        if not self.__click_was_inside_grid(clicked_tile_coord):
            print("NYI: Left click outside of tile grid")

            # Continue game
            return True

        clicked_x, clicked_y = clicked_tile_coord
        clicked_tile = self.__tile_grid[clicked_x][clicked_y]
        tile_number = clicked_tile.get_number()

        # Print debugging
        # print(f"left click on tile ({clicked_x}, {clicked_y})")

        if clicked_tile.has_bomb():
            print("NYI: Game over due to clicking on bomb")
            clicked_tile.perform_left_click()

            # End game
            return False

        # Perform flood of empty tiles
        if tile_number == 0:
            tiles_to_flood = self.__make_tile_flood_reveal_list(clicked_tile_coord)
            for tile_x, tile_y in tiles_to_flood:
                self.__tile_grid[tile_x][tile_y].perform_left_click()
        # Normal Click
        else:
            clicked_tile.perform_left_click()

        # Continue game, since no bomb
        return True

    def __handle_right_click(self, coord: tuple[int, int]):
        """
        Take the right click, call the calculation method, then pass the click to the tile.

        The tile will then change its flag state to cycle through the two types of flags, and the blank tile.
        """
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
        """
        Converts screen coordinates to tile grid coordinates.
        """
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
