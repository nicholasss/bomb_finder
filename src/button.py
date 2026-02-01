from collections.abc import Callable
import pygame as pg


class Button(pg.sprite.Sprite):
    """
    Button creates a generic button class that can be
    instantiated for use across the game.
    """

    def __init__(
        self,
        font: pg.Font,
        x: int,
        y: int,
        height: int,
        width: int,
        callback: Callable,
        text_color: pg.typing.ColorLike = (255, 255, 255, 255),
        button_color: pg.typing.ColorLike = (180, 180, 180, 255),
        button_hover_color: pg.typing.ColorLike = (165, 165, 165, 235),
        button_down_color: pg.typing.ColorLike = (190, 190, 190, 255),
        text: str = "",
    ):
        super().__init__()
        self.__font = font
        self.__position = x, y
        self.__size = width, height
        self.__callback = callback
        self.__text = text
        self.__callback = callback
        self.__button_down = False
        self.__text_color = text_color

        # Button colors
        self.__button_normal_color = button_color
        self.__button_hover_color = button_hover_color
        self.__button_down_color = button_down_color

        # Sprite properties
        self.image: pg.Surface = pg.Surface(self.__size)
        self.image.fill(self.__button_normal_color)
        self.rect: pg.Rect = self.image.get_rect()
        self.rect.topleft = self.__position

        # Render and place font
        self.__render_font()

    def handle_event(self, event: pg.Event):
        """
        This method is called to handle events as they occur.
        This can be hundreds of events every frame.
        """

        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # change self.image to instance's image_down
                self.image.fill(self.__button_down_color)
                self.__render_font()
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

                self.__button_down = True
        elif event.type == pg.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.__button_down:
                self.__callback()
                # change self.image to instance's image_hover
                self.image.fill(self.__button_hover_color)
                self.__render_font()
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

            self.__button_down = False
        elif event.type == pg.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.__button_down:
                # change self.image to instance's image_hover
                self.image.fill(self.__button_hover_color)
                self.__render_font()
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

            elif not collided:
                # change self.image to instance's image_normal
                self.image.fill(self.__button_normal_color)
                self.__render_font()
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    def __render_font(self):
        button_center = self.image.get_rect().center
        text_surf = self.__font.render(self.__text, True, self.__text_color)
        text_rect = text_surf.get_rect(center=button_center)
        self.image.blit(text_surf, text_rect)
