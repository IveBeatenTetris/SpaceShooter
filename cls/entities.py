import pygame as pg
import utils as u

class Player(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        self.cfg = kwargs
        pg.sprite.Sprite.__init__(self)
        self.image = self.create_image()
        self.rect = self.image.get_rect()
        self.speed = self.cfg["speed"]
    def create_image(self):
        img = pg.image.load(self.cfg["image"])

        if self.cfg["rotation"] > 0:
            img = pg.transform.rotate(img, self.cfg["rotation"])

        return img
