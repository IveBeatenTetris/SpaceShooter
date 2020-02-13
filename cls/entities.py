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
        self.cfg = u.validateDict(kwargs, u.DEFAULT["explosion"])
        pg.sprite.Sprite.__init__(self)
        self.original_image = pg.image.load(kwargs["image"])
        self.rect = self.original_image.get_rect()
        self.rect.center = self.cfg["position"]
        self.cooldown = self.cfg["cooldown"]
        self.rotation = random.randint(0, 360)
        self.size = [*self.rect.size]
    # dynamic attributes
    @property# pg.surface
    def image(self):
        image = pg.Surface(self.original_image.get_rect().size, pg.SRCALPHA)
        # rotating image
        img = pg.transform.rotate(self.original_image.copy(), self.rotation)
        # updating transparency of the image nearing the end of cooldown
        img.set_colorkey((102, 255, 0))
        alpha = int(self.cooldown * 255 / 100)
        img.set_alpha(alpha)

        if self.size[0] == 0 or self.size[0] == 0:
            self.size[0], self.size[1] = 0, 0
            img.set_alpha(0)
        else:
            if not alpha % 3:
                self.size[0] += 1
                self.size[1] += 1
            img = u.scale(img, self.size)
            self.rect.size = img.get_rect().size
            self.rect.center = self.cfg["position"]
            image = pg.Surface(self.rect.size, pg.SRCALPHA)
        # drawing created image to returning surface
        image.blit(img, (0, 0))

        return image
    # basic operations
    def update(self):
        self.cooldown -= 1
class Asteroid(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        self.cfg = u.validateDict(kwargs, u.DEFAULT["asteroid_43x43"])
        pg.sprite.Sprite.__init__(self)
        self.original_image = pg.image.load(self.cfg["image"])
        self.rect = pg.Rect((0, 0), self.cfg["size"])
        self.position = self.cfg["position"]
        self.rect.center = self.position
        self.health = self.cfg["health"]
        self.damage = self.cfg["damage"]
        self.rotation = [0, 360, random.random()]
        self.moving = self.cfg["moving"]
        self.image = self.create_image()
        if self.cfg["box"]:
            self.image = u.drawBorder(self.image, size=1, color=(255,0,0))
    @property# pg.surface
    def healthbar(self):
        color = (200, 15, 25)
        healthbar = pg.Surface((self.health, 3), pg.SRCALPHA)
        rect = [0, 0, self.health, 3]

        healthbar.fill(color, rect)

        return healthbar

    def hit(self, damage):
        if not self.health - damage < 0:
            self.health -= damage
        else:
            self.health = 0
    def create_image(self):# pg.surface
        surface = pg.Surface(self.cfg["size"], pg.SRCALPHA)
        image = self.original_image.copy()
        if bool(random.getrandbits(1)):
            pg.transform.flip(
                image,
                bool(random.getrandbits(1)),
                bool(random.getrandbits(1))
            )
        image = u.scale(image, self.cfg["size"])

        surface.blit(image, (0, 0))

        return surface
    def move(self):
        if self.moving:
            if self.moving == "left":
                left = self.position[0] - self.cfg["speed"]
            elif self.moving == "right":
                left = self.position[0] + self.cfg["speed"]

            self.position = (left, self.position[1])
            self.rect.center = self.position

        self.rect.center = self.position
    def reposition(self, position):
        self.rect.center = position
        self.position = position
    def rotate(self):
        self.image = self.create_image()
        self.image = pg.transform.rotate(self.image, self.rotation[0])
        if self.cfg["box"]:
            self.image = u.drawBorder(self.image, size=1, color=(255,0,0))
        self.rect.size = self.image.get_rect().size

        if self.moving:
            self.rect.center = self.position

        if self.rotation[0] == self.rotation[1]:
            self.rotation[0] = 0
        else:
            self.rotation[0] += self.rotation[2]
    def update(self):
        self.rotate()
        self.move()
        self.image.blit(self.healthbar, (0, 0))
class Player(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        self.cfg = u.validateDict(kwargs, u.DEFAULT["player"])
        pg.sprite.Sprite.__init__(self)
        self.original_image = pg.image.load(self.cfg["image"])
        self.bow = None
        self.image = self.create_image()
        self.rect = self.image.get_rect()
        self.speed = self.cfg["speed"]
        self.standard_shot = pg.image.load(self.cfg["default_shot"])
        self.damage = self.cfg["damage"]
    def create_image(self):
        img = self.original_image.copy()

        if self.cfg["scale"]:
            img = u.scale(
                img,
                (
                    int(img.get_rect().width * self.cfg["scale"]),
                    int(img.get_rect().height * self.cfg["scale"]),
                )
            )

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

        if self.cfg["box"]:
            img = u.drawBorder(img, size=1, color=(255,0,0))

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
class PlayerHealthBar(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        self.cfg = u.validateDict(kwargs, u.DEFAULT["player_healthbar"])
        pg.sprite.Sprite.__init__(self)
        self.health = kwargs["health"]
        self.rect = self.image.get_rect()
        self.rect.midbottom = kwargs["midbottom"]
    @property# pg.surface
    def image(self):
        image = pg.Surface(self.cfg["size"])
        image_rect = image.get_rect()
        border_rect = pg.Rect(
            1,
            1,
            image_rect.width - 2,
            image_rect.height - 2,
        )
        healthbar_width = border_rect.width * self.health / 100
        health_rect = pg.Rect(
            2,
            2,
            healthbar_width - 2,
            border_rect.height - 2,
        )

        red = (200, 50, 45)
        black = (5, 5, 15)
        white = (185, 195, 200)

        image.fill(white)
        image.fill(black, border_rect)
        image.fill(red, health_rect)

        return image
