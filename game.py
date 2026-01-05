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

        # x, y of the top left corner of the grid
        self.__grid_location_x, self.__grid_location_y = grid_top_left_corner

        # create grid
        tile_width = self.__tile_render_size[0]
        tile_height = self.__tile_render_size[1]
        self.__grid = [[int]]
        for i in range(self.__grid_cols):
            for j in range(self.__grid_rows):
                grid_coord = [tile_width * i, tile_height * j]

                # TODO:
                # new_tile = Tile()
                # use tile class instead of just tile image

                self.__screen.blit(
                    self.__tileset.get_tile(TileType.UNCLICKED), grid_coord
                )

        # use seed to place bombs

        pg.display.flip()
        print("Game Initialized")

    def start_game(self, game_clock: pg.time.Clock, fps: int):
        """Start the main game loop"""

        # Main game loop
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.MOUSEBUTTONUP:
                    print("Clicked!")
                    print(event.pos, "\n")
                    # pass coord to some kind of 'handle_click'

            game_clock.tick(fps)

    def handle_click(self, coord: tuple[int, int]):
        """Take the click, call the calculation method, then pass the click to the tile.
        The tile will change state, and then any changes to the grid should be made."""
        pass

    def find_tile_from_click(self, coord: tuple[int, int]):
        """ """
        pass
