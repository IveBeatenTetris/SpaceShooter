import pygame as pg
import utils as u

class Player(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        pg.sprite.Sprite.__init__(self)
        self.image = self.create_image()
    def create_image(self):
        img = pg.image.load(u.DEFAULT["player"]["image"])

        return img
