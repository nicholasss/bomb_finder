import pygame as pg
from tileset import Tileset, TileType
from tile import Tile


class Game:
    def __init__(
        self,
        tileset: Tileset,
        tile_size: tuple[int, int],
        screen: pg.Surface,
        seed: str,
    ):
        """A game instance should returned a fully setup game, ready to play."""
        self.__tileset: Tileset = tileset
        self.__tile_size: tuple[int, int] = tile_size
        self.__screen: pg.Surface = screen
        self.__seed: str = seed

        # create grid
        self.grid = [[int]]
        for i in range(5):
            for j in range(5):
                tile_location = [self.__tile_size[0] * i, self.__tile_size[1] * j]

                # TODO:
                # new_tile = Tile()
                # use tile class instead of just tile image

                self.__screen.blit(
                    self.__tileset.get_tile(TileType.UNCLICKED), tile_location
                )

        # use seed to place bombs

        pg.display.flip()
        print("Game Initialized")

    def start_game(self):
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

    def handle_click(self, coord: tuple[int, int]):
        """Take the click, call the calculation method, then pass the click to the tile.
        The tile will change state, and then any changes to the grid should be made."""
        pass

    def find_tile_from_click(self, coord: tuple[int, int]):
        """ """
        pass
