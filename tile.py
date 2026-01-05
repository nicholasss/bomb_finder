import pygame as pg


class Tile:
    def __init__(self, is_empty=False):
        # manage tile state and change tile image on demand
        self.__clicked = False
        self.__is_empty = is_empty

    def click(self) -> bool:
        self.__clicked = True
        return self.__is_empty
