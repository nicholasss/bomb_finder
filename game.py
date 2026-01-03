import pygame as pg
from tileset import Tileset, TileType
from tile import Tile


class Game():
    def __init__(self, tileset: Tileset, tile_size: tuple[int, int], screen: pg.Surface):
        self.__tileset: Tileset = tileset
        self.__tile_size: tuple[int, int] = tile_size
        self.__screen: pg.Surface = screen

        # Tile surfaces
        self.__unclicked_tile = tileset.get_tile(TileType.UNCLICKED)

        self.grid = [[]]
        for i in range(5):
            for j in range(5):
                tile_location = [self.__tile_size[0] * i, self.__tile_size[1] * j]
                self.__screen.blit(self.__unclicked_tile, tile)


        # draw the map
            # put in number of bombs into the 

        # perform animations if you lose the game

        # show redo game seed/new game
        tile = Tile(is_empty=True)
        item_found = tile.click()

        pass

    def play_round(self):
        pass
        # create the grid, shuffle the items, and draw
        # process events

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.MOUSEBUTTONUP:
                    print("Clicked!")
                    print(event.pos, "\n")


    def click(self, pos: tuple[int, int]):
        pass
        
    