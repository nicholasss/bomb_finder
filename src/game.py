import random
import pygame as pg
from tileset import TileType, Tileset
from tile import Tile
from tile_sprite import TileSprite
from grid import Grid
from utility import click_to_tile_coord, click_was_inside_grid


class Game:
    """
    Game handles the creation of the grid, and relays events to sprites and grids.
    Additionally, it manages the game loop, saves previous moves, etc.
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
        grid_topleft: tuple[int, int] = (0, 0),
        debug_mode: bool = False,
    ):
        """
        A game instance should returned a fully setup game, ready to play.
        """

        if debug_mode:
            print("DEBUG: Creating instance of Game")

        # Properties
        self.__tileset = tileset
        self.__tile_render_size = tile_render_size
        self.__tile_render_width, self.__tile_render_height = tile_render_size
        self.__screen = screen
        self.__num_of_bombs = num_of_bombs
        self.__rng = rng
        self.__font = font
        self.__grid_size = grid_size
        self.__grid_topleft = grid_topleft
        self.__debug_mode = debug_mode

        # Mouse status
        self.__mouse_is_down = False
        self.__mouse_is_down_on: tuple[int, int] = (-1, -1)

        # Bomb grid
        self.__grid = Grid(
            self.__tileset,
            (self.__tile_render_width, self.__tile_render_height),
            self.__screen,
            self.__num_of_bombs,
            self.__rng,
            self.__font,
            self.__grid_size,
            self.__grid_topleft,
            self.__debug_mode,
        )

        # complete iniialization
        print("DEBUG: Game Initialized")

    def start_game(self, clock: pg.time.Clock, fps: int):
        """
        Start the main game loop.

        Since this function performs rendering, we are passing in a pygame clock, and an fps variable.
        """
        continue_game = True
        while continue_game:
            # A: Debug mode operations
            if self.__debug_mode:
                pg.display.set_caption(
                    f"FPS {int(clock.get_fps())} | {clock.get_time()}"
                )
                if self.__mouse_is_down:
                    print(f"DEBUG: Tile selected->{self.__mouse_is_down_on}")

            # TODO: Rewrite the tile selection using mouse_pos and collision detection?
            #
            # B: Reset tile selection
            if self.__mouse_is_down and click_was_inside_grid(
                self.__mouse_is_down_on, self.__grid_size
            ):
                self.__grid.deselect_tile(self.__mouse_is_down_on)

            # C: Handle single events
            for event in pg.event.get():
                # Quit game
                if event.type == pg.QUIT:
                    # TODO: Exit straight away, instead of showing game over screen
                    continue_game = False

                # Mouse click has started
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.__mouse_is_down = True

                # Mouse click is complete
                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        col_row_clicked = click_to_tile_coord(
                            event.pos, self.__grid_topleft, self.__tile_render_size
                        )
                        if click_was_inside_grid(col_row_clicked, self.__grid_size):
                            bomb_not_clicked = self.__grid.reveal_click(col_row_clicked)
                            if not bomb_not_clicked:
                                print(
                                    f"GAME OVER!\n\tBomb was clicked at {col_row_clicked}"
                                )

                        self.__mouse_is_down = False

                    elif event.button == 3:
                        col_row_clicked = click_to_tile_coord(
                            event.pos, self.__grid_topleft, self.__tile_render_size
                        )
                        if click_was_inside_grid(col_row_clicked, self.__grid_size):
                            self.__grid.flag_click(col_row_clicked)

            # D: Handle 'ongoing' events
            if self.__mouse_is_down:
                self.__mouse_is_down_on = click_to_tile_coord(
                    pg.mouse.get_pos(), self.__grid_topleft, self.__tile_render_size
                )

                if click_was_inside_grid(self.__mouse_is_down_on, self.__grid_size):
                    self.__grid.select_tile(self.__mouse_is_down_on)

            # TODO: Clear the screen with a tileset specified background color
            # E: Clear the screen
            self.__screen.fill("black")

            # F: Render the grid
            self.__grid.all_tiles.update()
            self.__grid.all_tiles.draw(self.__screen)

            # G: Debug rendering
            if self.__debug_mode:
                # self.__render_debug_overlay()
                pass

            # H. Update display
            pg.display.flip()

            # I. Limit the frame rate
            clock.tick(fps)

    # def __render_grid(self):
    #    """
    #    Renders the grid during every frame
    #    """
    #    for x in range(self.__grid_cols):
    #        for y in range(self.__grid_rows):
    #            tile_corner_x, tile_corner_y = (
    #                (self.__tile_render_size[0] * x),
    #                (self.__tile_render_size[1] * y),
    #            )

    #            # offset the grid by the topleft corner
    #            tile_loc = (
    #                tile_corner_x + self.__grid_location_x,
    #                tile_corner_y + self.__grid_location_y,
    #            )

    #            tile_state = self.__tile_grid[x][y].get_state()

    #            self.__screen.blit(self.__tileset.get_tile(tile_state), tile_loc)

    #            # debug mode
    #            if self.__debug_mode:
    #                text = f"{self.__tile_grid[x][y].get_number()}"
    #                if self.__tile_grid[x][y].has_bomb():
    #                    text = "B"

    #                num_text = self.__font.render(text, True, "black")
    #                num_rect = num_text.get_rect()

    #                margin = 15
    #                num_loc = tile_loc[0] + margin, tile_loc[1] + margin
    #                self.__screen.blit(num_text, num_loc, num_rect)

    # def __render_debug_overlay(self):
    #    # NOTE: gave up on window position calculations
    #    # top left corner
    #    win_left = 350
    #    win_top = 30
    #    win_width = 750
    #    win_height = 400

    #    # pg.Rect(x, y, width, height)
    #    window_rect = pg.Rect(win_left, win_top, win_width, win_height)
    #    window_surf = pg.Surface((win_width, win_height), pg.SRCALPHA)

    #    overlay_color = (255, 255, 255, 80)
    #    pg.draw.rect(window_surf, overlay_color, window_rect)

    #    # debug info
    #    mouse_loc = pg.mouse.get_pos()
    #    grid_loc = self.__find_tile_from_coord(mouse_loc)
    #    if self.__click_was_inside_grid(grid_loc):
    #        tile_state = self.__tile_grid[grid_loc[0]][grid_loc[1]].get_state()
    #        atlas_name = tile_state.name
    #        atlas_num = tile_state.value
    #    else:
    #        placeholder = "not in grid"
    #        grid_loc = placeholder
    #        atlas_name = placeholder
    #        atlas_num = placeholder

    #    text = f"""DEBUG MODE

    # game seed = {self.__seed}
    # bombs on map = {self.__number_of_bombs}
    #
    # mouse_loc = {mouse_loc}
    # grid_loc = {grid_loc}
    # tile type = {atlas_name}
    # atlas number = {atlas_num}
    # """

    # render text
    # text_surf = self.__font.render(text, True, (255, 255, 255))
    # text_rect = (window_rect.topleft[0] + 5, window_rect.topleft[1] + 5)

    # window_surf.blit(text_surf, text_rect)

    # self.__screen.blit(window_surf, (win_left, win_top))

    def __make_tile_flood_reveal_list(
        self, first_tile: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """
        From a starting coordinate of 'first_tile', find all adjascent tiles that need to be revealed.
        Utilizing a DFS algorithm.
        """
        tiles_to_visit: list[tuple[int, int]] = [first_tile]
        tiles_to_reveal: list[tuple[int, int]] = [first_tile]
        while len(tiles_to_visit) > 0:
            tile_being_visited = tiles_to_visit.pop()
            tile_visit_x, tile_visit_y = tile_being_visited

            # 1. check if empty tile
            if self.__tile_grid[tile_visit_x][tile_visit_y].get_number() <= 0:
                # 1a. IF it is tile with 0, then add to to_visit and...
                if tile_being_visited not in tiles_to_reveal:
                    tiles_to_reveal.append(tile_being_visited)

                # TODO: make into some kind of iterator function
                #
                # 1b. iterate through and add surrounding tiles to_reveal list
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        tile_x, tile_y = tile_visit_x + x, tile_visit_y + y
                        # print("")
                        # print(f"Should we reveal {(tile_x, tile_y)}?")

                        # skip looking at the center tile itself
                        if x == 0 and y == 0:
                            # print("\tNo, its the tile itself")
                            continue

                        # check if tile is too low outside grid
                        elif tile_x < 0 or tile_y < 0:
                            # print("\tNo, its too low outside grid (negative)")
                            continue

                        # check if tile is too high outside grid
                        elif tile_x >= self.__grid_cols or tile_y >= self.__grid_rows:
                            # print(
                            #     "\tNo, its too high outside grid (greater than rows/cols)"
                            # )
                            continue

                        # add to to_reveal list
                        # print("\tYes, its valid.")
                        tile_coord = (tile_x, tile_y)
                        if tile_coord not in tiles_to_reveal:
                            tiles_to_reveal.append(tile_coord)
                            tiles_to_visit.append(tile_coord)

            # its not an empty tile, only add to tiles_to_reveal, do not check surrounding tiles
            if tile_being_visited not in tiles_to_reveal:
                tiles_to_reveal.append(tile_being_visited)

        return tiles_to_reveal

    # def __handle_reveal_click(self, coord: tuple[int, int]) -> bool:
    #     """
    #     Take the click, call the calculation method, then pass the click to the tile.
    #     The tile will change state, and then any changes to the grid should be made.

    #     This method will return a boolean, to indicate whether to continue the game or not.
    #     True: continue the game
    #     False: game is over
    #     """
    #     clicked_tile_coord = self.__find_tile_from_coord(coord)

    #     # left click was outside grid, do nothing
    #     if not self.__click_was_inside_grid(clicked_tile_coord):
    #         print("NYI: Left click outside of tile grid")

    #         # Continue game
    #         return True

    #     clicked_x, clicked_y = clicked_tile_coord
    #     clicked_tile = self.__tile_grid[clicked_x][clicked_y]
    #     tile_number = clicked_tile.get_number()

    #     # Print debugging
    #     # print(f"left click on tile ({clicked_x}, {clicked_y})")

    #     if clicked_tile.has_bomb():
    #         print("NYI: Game over due to clicking on bomb")
    #         clicked_tile.reveal_click()

    #         # End game
    #         return False

    #     # Perform flood of empty tiles
    #     if tile_number == 0:
    #         tiles_to_flood = self.__make_tile_flood_reveal_list(clicked_tile_coord)
    #         for tile_x, tile_y in tiles_to_flood:
    #             self.__tile_grid[tile_x][tile_y].reveal_click()
    #     # Normal Click
    #     else:
    #         clicked_tile.reveal_click()

    #     # Continue game, since no bomb
    #     return True

    # def __handle_flag_click(self, coord: tuple[int, int]):
    #     """
    #     Take the right click, call the calculation method, then pass the click to the tile.

    #     The tile will then change its flag state to cycle through the two types of flags, and the blank tile.
    #     """
    #     tile_clicked = self.__find_tile_from_coord(coord)

    #     # right click was outside grid, do nothing
    #     if not self.__click_was_inside_grid(tile_clicked):
    #         print("NYI: Right click outside of tile grid")
    #         return

    #     clicked_x, clicked_y = tile_clicked
    #     clicked_tile = self.__tile_grid[clicked_x][clicked_y]

    #     # send flag event to the tile
    #     clicked_tile.flag_click()
