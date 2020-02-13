import pygame as pg
import utils as u

pg.font.init()

class Text(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        pg.sprite.Sprite.__init__(self)
        self.text = self.create_text()
        self.image = self.text.copy()
        self.rect = self.image.get_rect()
        self.rect.center = kwargs["center"]
    def create_text(self):# pg.surface
        if "bold" in self.kwargs:
            bold = self.kwargs["bold"]
        else:
            bold = False
        return u.createText(
            text = self.kwargs["text"],
            size = self.kwargs["size"],
            bold = bold
        )
class Button(Text):
    def __init__(self, **kwargs):
        Text.__init__(self, **kwargs)
        self.__stil_hovering = False
        self.recreate_image()
    @property
    def click(self):
        click = False

        if self.hover:
            for event in pg.event.get():
                if event.type is pg.MOUSEBUTTONDOWN and event.button == 1:
                    click = True

        return click
    @property
    def hover(self):
        hover = False
        mouse_position = pg.mouse.get_pos()

        if self.rect.collidepoint(mouse_position):
            hover = True
            self.__stil_hovering = True

        return hover
    def recreate_image(self):
        text_position = (0, 0)
        self.image = self.text.copy()
        self.rect = self.image.get_rect()

        if "padding" in self.kwargs:
            padding = self.kwargs["padding"]
            self.rect.size = (
                self.rect.width + padding[1] + padding[3],
                self.rect.height + padding[0] + padding[2]
            )
            self.rect.center = self.kwargs["center"]
            self.image = pg.Surface(self.rect.size)
            text_position = (padding[3], padding[0])
        if "background" in self.kwargs:
            if "hover" in self.kwargs and self.hover:
                background = self.kwargs["hover"]
            else:
                background = self.kwargs["background"]

            self.image.fill(background)
        if "border" in self.kwargs:
            border = self.kwargs["border"]
            self.image = u.drawBorder(
                self.image,
                size = border[0],
                color = border[1]
            )

        self.image.blit(self.text, text_position)
    def update(self):
        if self.hover:
            self.recreate_image()
        elif not self.hover and self.__stil_hovering:
            self.recreate_image()
            self.__stil_hovering = False
