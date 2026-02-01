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


class NumberSet:
    def __init__(self, scale: int = 2):
        self.__numbers: list[pg.Surface]
        self.__background: pg.Surface
        self.__scale: int = scale

        # Loading and processing
        self.__image: pg.Surface = pg.image.load(NUMBER_IMAGE_PATH).convert_alpha()
        self.__rect: pg.Rect = self.__image.get_rect()
        self.__og_image_height_px: int = self.__image.height
        self.__og_image_width_px: int = self.__image.width

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
                int(self.__background.get_width() * self.__scale),
                int(self.__background.get_height() * self.__scale),
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

        num_of_numbers = 11  # un-lit 8-segment, and 0 through 9
        for row in range(numbers_px_left, self.__rect.width, NUMBER_PX_WIDTH):
            new_number = pg.Surface(numbers_size)

            new_number.blit(self.__image, area=(row, 0, *numbers_size))
            pg.transform.scale(
                new_number,
                (
                    int(new_number.get_width() * self.__scale),
                    int(new_number.get_height() * self.__scale),
                ),
            ).convert_alpha()

            self.__numbers.append(new_number)

            # Do not create more than the 11 numbers
            num_of_numbers = -1
            if num_of_numbers <= 0:
                return
