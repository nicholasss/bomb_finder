from tileset import TileType, Tileset
import pygame as pg


class TileSprite(pg.sprite.Sprite):
    """
    Tile Sprite is a subclass of the pygame Sprite class.

    Instead of being a container for state that the game class uses, these tiles manage their own
    image (`pygame.Surface`) and its own rect (`pygame.Rect`). This design means we use simple methods
    to update state, and then utilize the `update` method to update the image (`pygame.Surface`).
    """

    def __init__(self, tileset: Tileset, x: float, y: float):
        super().__init__()
        # Tileset to use
        self.__tileset = tileset

        # Tile internal state
        self.__num_neighbors = 0
        self.has_bomb = False
        self.was_clicked = False
        self.__is_pressed = False
        self.__tile_type = TileType.UNCLICKED

        # Location of tile on screen
        self.__x = x
        self.__y = y

        # Sprite properties and placing on screen
        self.image: pg.Surface = self.__tileset.get_tile(self.__tile_type)
        self.rect: pg.Rect = self.image.get_rect()
        self.rect.topleft = self.__x, self.__y

    def update(self):
        """
        Every frame this will be called. It should take the state of the tile, and update
        `self.image` to the appropriate tile from the tileset. This is done by updating the
        `self.__tile_type`.
        """

        if self.__is_pressed:
            self.image = self.__tileset.get_tile(TileType.CLICKED_EMPTY)

        else:
            self.image = self.__tileset.get_tile(self.__tile_type)

    def reveal(self):
        """
        Reveal the tile, utilizing the internal state to change the TileType to render within the same frame.

        Revealing a tile will only show an empty tile, a number, or a bomb. It will remove any flags that were on it.
        """

        # Only is set to true below, prevents running the same method again
        if self.was_clicked:
            return

        # adjust simple state first
        self.was_clicked = True

        if self.has_bomb:
            # TODO: Only the first frame of the bomb, needs to kick off animation somehow?
            # Unsure where to trigger and perform the animation
            self.__tile_type = TileType.BOMB_A
            return

        # Warning debug
        if self.__num_neighbors > 8:
            print(
                f"WARNING: neighboring bombs of cell at {(self.__x, self.__y)} is more than 8. neigbors with bombs->{self.__num_neighbors}"
            )
        # NOTE: Could add additional warninga here to check for known state?

        # Tile does not have a bomb
        if self.__num_neighbors == 0:
            self.__tile_type = TileType.CLICKED_EMPTY

        elif self.__num_neighbors >= 1:
            self.__tile_type = TileType(self.__num_neighbors + 1)

    def cycle_flag(self):
        """
        Cycle the flag state of the tile. Certain Flag -> Uncertain Flag -> Unflagged -> Certain Flag, etc.

        12 = Certain Flag
        13 = Uncertain Flag
        0  = Unflagged
        """

        if self.__tile_type == TileType.UNCLICKED_CERTAIN:
            self.__tile_type = TileType.UNCLICKED_UNCERTAIN

        elif self.__tile_type == TileType.UNCLICKED_UNCERTAIN:
            self.__tile_type = TileType.UNCLICKED

        elif self.__tile_type == TileType.UNCLICKED:
            self.__tile_type = TileType.UNCLICKED_CERTAIN

    def has_flag(self) -> bool:
        """
        Whether the tile has a Certain Flag on it.
        """

        return self.__tile_type == TileType.UNCLICKED_CERTAIN

    def flag_is_on_mine(self) -> bool:
        """
        Whether the tile is correctly flagged or not.
        """

        return self.__tile_type == TileType.UNCLICKED_CERTAIN and self.has_bomb

    def press(self):
        self.__is_pressed = True

    def unpress(self):
        self.__is_pressed = False

    def place_bomb(self):
        self.has_bomb = True

    def has_no_bomb(self) -> bool:
        return not self.has_bomb

    def set_neighbors(self, num_neighbors: int):
        self.__num_neighbors = num_neighbors

    def no_neighboring_bombs(self) -> bool:
        if self.__num_neighbors == 0:
            return True
        else:
            return False
