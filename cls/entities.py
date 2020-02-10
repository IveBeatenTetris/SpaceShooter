import pygame as pg
import utils as u

class Asteroid(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        self.cfg = kwargs
        pg.sprite.Sprite.__init__(self)
        self.original_image = pg.image.load(self.cfg["image"])
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
class Player(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        self.cfg = kwargs
        pg.sprite.Sprite.__init__(self)
        self.original_image = pg.image.load(self.cfg["image"])
        self.bow = None
        self.image = self.create_image()
        self.rect = self.image.get_rect()
        self.speed = self.cfg["speed"]
    def tilt(self, direction=None):
        if not direction:
            self.bow = None
        else:
            if direction == "up":
                self.bow = "up"
            elif direction == "down":
                self.bow = "down"
            elif direction == "left":
                self.bow = "left"
            elif direction == "right":
                self.bow = "right"

        self.image = self.create_image()
    def create_image(self):
        img = self.original_image.copy()

        if self.cfg["rotation"] > 0:
            img = pg.transform.rotate(img, self.cfg["rotation"])

        if self.bow:
            width = int(self.rect.width)
            height = int(self.rect.height)

            if self.bow == "left" or self.bow == "right":
                width -= 3
            if self.bow == "up" or self.bow == "down":
                height -= 5

            img = pg.transform.scale(img, (width, height))

        return img
