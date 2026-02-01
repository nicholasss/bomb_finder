from enum import Enum
import pygame as pg

NUMBER_IMAGE_PATH = "./../assets/asperite_files/numbers.png"
NUMBER_PX_HEIGHT = 64
NUMBER_PX_WIDTH = 32

# The file is 64px tall & 1024px wide
# Each tile is 64px tall & 32px wide
#
# The first three tiles should be combined into a 64px tall & 96px wide
#
# Then, the numbers, three digits wide, need to be put together onto the faux digital display
# and returned as a pg.Surface


class SegmentType(Enum):
    EMPTY = 0
    MINUS = 1
    ZERO = 2
    ONE = 3
    TWO = 4
    THREE = 5
    FOUR = 6
    FIVE = 7
    SIX = 8
    SEVEN = 9
    EIGHT = 10
    NINE = 11


class NumberSet:
    def __init__(self, scale: int = 2):
        self.scale: int = scale

        self.__numbers: list[pg.Surface]
        self.__background: pg.Surface

        # Loading and processing
        self.__image: pg.Surface = pg.image.load(NUMBER_IMAGE_PATH).convert_alpha()
        self.__rect: pg.Rect = self.__image.get_rect()

        # Making the tiles
        self.__make_background()
        self.__make_numbers()

    def __make_background(self):
        """
        Take the raw image and create the __background instance.
        """

        background_size = (96, 64)
        self.__background = pg.Surface(background_size)
        self.__background.blit(self.__image, area=(0, 0, *background_size))
        pg.transform.scale(
            self.__background,
            (
                int(self.__background.get_width() * self.scale),
                int(self.__background.get_height() * self.scale),
            ),
        ).convert_alpha()

    def __make_numbers(self):
        """
        Take the raw image and create the __numbers instances.
        """

        self.__numbers = []

        # Surface sizes
        numbers_px_left = 96
        numbers_size = (NUMBER_PX_WIDTH, NUMBER_PX_HEIGHT)

        num_of_numbers = 12  # un-lit 8-segment, a minus, and 0 through 9
        for col in range(numbers_px_left, self.__rect.width, NUMBER_PX_WIDTH):
            new_number = pg.Surface(numbers_size)

            new_number.blit(self.__image, area=(col, 0, *numbers_size))
            pg.transform.scale(
                new_number,
                (
                    int(new_number.get_width() * self.scale),
                    int(new_number.get_height() * self.scale),
                ),
            ).convert_alpha()

            self.__numbers.append(new_number)

            # Do not create more than the 11 numbers
            num_of_numbers = -1
            if num_of_numbers <= 0:
                return

    def get_background(self) -> pg.Surface:
        return self.__background

    def get_segment(self, number: SegmentType) -> pg.Surface:
        return self.__numbers[number.value]


class NumberDisplay:
    """
    NumberDisplay needs to have an instantiated NumberSet passed in.
    NumberSet is a number tile set.
    """

    def __init__(self, number_set: NumberSet):
        self.__display: pg.Surface
        self.__number_set: NumberSet = number_set

        self.__make_display()
        self.__reset_display()

    def __make_display(self):
        scale = self.__number_set.scale
        display_size = (96 * scale, 64 * scale)
        self.__display = pg.Surface(display_size)
        self.__display.blit(self.__number_set.get_background())

    def __reset_display(self):
        empty_segment = self.__number_set.get_segment(SegmentType.EMPTY)
        for col in range(3):
            self.__display.blit(empty_segment, (NUMBER_PX_WIDTH * col, 0))

    def get_display(self) -> pg.Surface:
        return self.__display

    def update_number(self, number: int):
        if number < -99:
            raise ValueError("Unable to display below -99")
        elif number > 999:
            raise ValueError("Unable to display above 999")

        number_is_negative = False
        if number < -1:
            number_is_negative = True

        # TODO:
        # Turn into string
        # Split into individual characters
        # Convert to integers
        # Place the numbers onto the display
