import pygame as pg


class Tile:
    """Tile instances should store whether there is a bomb,
    whether it is clicked, and how many neighboring bombs there are."""

    def __init__(self, has_bomb=False):
        self.clicked = False
        self.__has_bomb = has_bomb
        self.__neighboring_bombs = 0

    def click(self) -> bool:
        """Perfroms a click on the tile.
        This will first mark the tile as clicked,"""
        self.clicked = True
        return self.__has_bomb
