import random
import pygame as pg
from tileset import Tileset
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
        self.__pressed_tile: None | tuple[int, int] = None
        self.__bg_color = pg.Color(132, 126, 135)

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

    # == Public Methods ==
    def start_game(self, clock: pg.time.Clock, fps: int):
        """
        Start the main game loop.

        Since this function performs rendering, we are passing in a pygame clock, and an fps variable.
        """
        continue_game = True
        debug_timer = 0
        while continue_game:
            # A: Debug mode operations
            if self.__debug_mode:
                debug_timer += clock.get_time()
                if debug_timer > 500:
                    pg.display.set_caption(
                        f"FPS {int(clock.get_fps())} | {clock.get_time()}"
                    )
                    debug_timer = 0

                # print(
                #     f"DEBUG:\n\tTiles remaining: {self.__grid.remaining_tiles_to_reveal}\n\tFlags remaining: {self.__grid.flags_remaining}"
                # )

            # B: Get mouse position
            mouse_pos = pg.mouse.get_pos()
            mouse_col_row = click_to_tile_coord(
                mouse_pos, self.__grid_topleft, self.__tile_render_size
            )
            is_inside_grid = click_was_inside_grid(mouse_col_row, self.__grid_size)

            # C: Get continuous state
            left_click_held, _, _ = pg.mouse.get_pressed()

            # D: Handle all events from during last tick
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # TODO: Exit straight away, instead of showing game over screen
                    continue_game = False

                # Click started from in grid
                if (
                    event.type == pg.MOUSEBUTTONDOWN
                    and event.button == 1
                    and is_inside_grid
                ):
                    self.__pressed_tile = mouse_col_row

                # Click ended
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        if is_inside_grid:
                            bomb_not_clicked = self.__grid.reveal_click(mouse_col_row)

                            # Bomb was clicked!
                            if not bomb_not_clicked and not self.__grid.game_was_won:
                                # TODO: Write game over menu
                                print(f"GAME OVER: Bomb was clicked at {mouse_col_row}")
                                continue_game = False

                            elif bomb_not_clicked and self.__grid.game_was_won:
                                # TODO: Write game won menu
                                print("DEBUG: [game.py] Game Won!")
                                continue_game = False

                            # Always reset if left mouse button was pressed
                            self.__pressed_tile = None
                            left_click_held = False

                    # Flaging tiles
                    elif event.button == 3 and is_inside_grid:
                        self.__grid.flag_click(mouse_col_row)

            # E: Manage "held press" tile state
            if left_click_held and is_inside_grid:
                self.__pressed_tile = mouse_col_row

            # F: Pass pressed_tile state to grid
            if self.__pressed_tile is not None and is_inside_grid:
                self.__grid.press_tile(self.__pressed_tile)

                # Reset pressed_tile if mouse is outside grid
                if not is_inside_grid:
                    self.__pressed_tile = None

            # TODO: Clear the screen with a tileset specified background color
            #
            # G: Render frame
            self.__screen.fill(self.__bg_color)

            # G-1: Render GUI
            self.__update()
            self.__draw_gui()

            # G-1: Render grid
            self.__grid.all_tiles.update()
            self.__grid.all_tiles.draw(self.__screen)

            # H: Render debug overlay, if enabled
            if self.__debug_mode:
                # self.__render_debug_overlay()
                pass

            # I: Update display
            pg.display.flip()

            # J: Unpress the tile after rendering
            if self.__pressed_tile is not None and is_inside_grid:
                self.__grid.unpress_tile(self.__pressed_tile)

            # K. Limit the frame rate
            clock.tick(fps)

    # == Private Methods ==
    def __update(self):
        """
        Every frame this will be called to update the state of the game class.
        """

        pass

    def __draw_gui(self):
        """
        Every frame this will be called to draw the GUI onto the screen.
        """

        #
        # Static GUI
        # draw box across the top, left, right, and bottom of the grid.

        # Above the grid
        # top_bar_size = self.__screen.width, self.__screen.height
        # top_bar_surf = pg.Surface(top_bar_size)
        # top_bar_surf.fill("gray")

        # top_bar_rect = top_bar_surf.get_rect()

        # self.__screen.blit(top_bar_surf, top_bar_rect)

        #
        # Dynamic GUI

        pass

    # Debug data and text
    #
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
