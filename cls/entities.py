import pygame as pg
import utils as u
import random

class Projectile(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        self.cfg = kwargs
        pg.sprite.Sprite.__init__(self)
        self.image = kwargs["image"]
        if kwargs["rotation"] > 0:
            self.image = pg.transform.rotate(self.image, kwargs["rotation"])
        self.rect = pg.Rect(kwargs["position"], self.image.get_rect().size)
    def update(self):
        self.rect.left += u.DEFAULT["player"]["shooting_speed"]
class Explosion(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        self.cfg = kwargs
        pg.sprite.Sprite.__init__(self)
        self.original_image = pg.image.load(kwargs["image"])
        self.rect = self.original_image.get_rect()
        self.rect.center = kwargs["position"]
        self.cooldown = [100, 100]
    @property
    def image(self):
        image = pg.Surface(self.original_image.get_rect().size, pg.SRCALPHA)
        img = self.original_image.copy()
        img.set_colorkey((102, 255, 0))
        img.set_alpha(self.cooldown[0])
        image.blit(img, (0, 0))

        return image
    def update(self):
        self.cooldown[0] -= 1
class Asteroid(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        self.cfg = kwargs
        pg.sprite.Sprite.__init__(self)
        self.original_image = pg.image.load(kwargs["image"])
        self.rotation = [0, 360, random.random()]
        self.image = self.original_image.copy()
        #self.image = u.drawBorder(self.image, size=1, color=(255,0,0))
        self.rect = self.image.get_rect()
    def update(self):
        self.image = self.original_image.copy()
        self.image = pg.transform.rotate(self.image, self.rotation[0])
        #self.image = u.drawBorder(self.image, size=1, color=(255,0,0))
        self.rect.size = self.image.get_rect().size

        if self.rotation[0] == self.rotation[1]: self.rotation[0] = 0
        else: self.rotation[0] += self.rotation[2]
class Player(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        self.cfg = kwargs
        pg.sprite.Sprite.__init__(self)
        self.original_image = pg.image.load(kwargs["image"])
        self.bow = None
        self.image = self.create_image()
        self.rect = self.image.get_rect()
        self.speed = kwargs["speed"]
        self.standard_shot = pg.image.load(kwargs["default_shot"])
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
