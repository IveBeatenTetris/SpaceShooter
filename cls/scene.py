import pygame as pg
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
        """
        self.cfg = u.validateDict(kwargs, defaults)
        # determining size of the scene
        if self.cfg["size"] == "full":
            self.cfg["size"] = pg.display.get_surface().get_rect()
        # initializing surface
        pg.Surface.__init__(self, self.cfg["size"], pg.SRCALPHA)
        self.rect = pg.Rect(self.cfg["position"], self.cfg["size"])
        self.create_background()
    def create_background(self):
        """recreates the background depending on 'cfg["background"]'."""
        bg = self.cfg["background"]

        if bg:
            # filling with solid color
            if type(bg) is tuple or type(bg) is list:
                if len(bg) == 3:
                    self.fill(self.cfg["background"])
