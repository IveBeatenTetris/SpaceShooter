import pygame as pg
from cls.entities import *
import utils as u

# default values for construction without user given parameters
defaults = {
    "size": "full",
    "position": (0, 0),
    "background": None
}

class Scene(pg.Surface):
    """stores specific information for displaying it only for this set scene."""
    def __init__(self, **kwargs):
        """
        'cfg'               'dict' with building instructions. made out of user
                            given parameters and default ones for this object.
        'rect'              'pg.rect' this object's dimensions.
        'background'        'pg.surface' for redrawing the background of this
                            object when needed.
        """
        self.cfg = u.validateDict(kwargs, defaults)
        # determining size of the scene
        if self.cfg["size"] == "full":
            self.cfg["size"] = pg.display.get_surface().get_rect()
        # initializing surface
        pg.Surface.__init__(self, self.cfg["size"], pg.SRCALPHA)
        self.rect = pg.Rect(self.cfg["position"], self.cfg["size"])
        self.background = self.create_background()
        # first time drawing background to surface
        self.blit(self.background, self.rect)
    def create_background(self):# pg.surface
        """
        recreates the background depending on 'cfg["background"]' and returns
        it.
        """
        background = pg.Surface(self.rect.size, pg.SRCALPHA)

        if self.cfg["background"]:
            bg = self.cfg["background"]
            background.fill(bg)

        return background
    def update(self):
        """updates visuals within the scene. called at every main-loop end."""
        pass
