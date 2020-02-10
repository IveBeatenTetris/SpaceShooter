import pygame as pg
import utils as u

# default values for construction without user given parameters
defaults = {
    "type": "npc"
}

class Entity(pg.sprite.Sprite):
    """entity representing a ship, char, enemy and so on."""
    def __init__(self, **kwargs):
        """
        'cfg'               'dict' with building instructions. made out of user
                            given parameters and default ones for this object.
        'image'             'pg.surface' of this sprite.
        """
        self.cfg = u.validateDict(kwargs, defaults)
        pg.sprite.Sprite.__init__(self)
        self.image = self.create_image()
    def create_image(self):# pg.surface
        """creates and returns a pygame-surface."""
        if self.cfg["type"] == "hero":
            img = pg.image.load(u.PATH_IMG + "starship.png")

        return img
