import pygame as pg
import utils as u

# default values for construction without user given parameters
defaults = {
    "size": "full",
    "position": (0, 0)
}

class Scene(pg.Surface):
    """stores specific information for displaying it only for this set scene."""
    def __init__(self, **kwargs):
        """
        'cfg'               'dict' with building instructions. made out of user
                            given parameters and default ones for this object.
        """
        self.cfg = u.validateDict(kwargs, defaults)
        # determining size of the scene
        if self.cfg["size"] == "full":
            self.cfg["size"] = pg.display.get_surface().get_rect()
        # initializing surface
        pg.Surface.__init__(self, self.cfg["size"], pg.SRCALPHA)
        self.rect = pg.Rect(self.cfg["position"], self.get_rect().size)
