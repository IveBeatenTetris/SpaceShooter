import pygame as pg
import utils as u
import sys

# default values for constructing a window without user given parameters
defaults = {
    "size": (320*2, 240*2),
    "title": "Space Shooter",
    "fps": 60
}

class Window(object):
    """window object for displaying all visuals."""
    def __init__(self, **kwargs):
        """
        'cfg'               'dict' with building instructions. made out of user
                            given parameters and default ones for this object.
        'display'           'pg.surface' holds all visuals drawn to it.
        'clock'             'pg.clock' object to keep track of time ran by.
        """
        pg.init()
        self.cfg = u.validateDict(kwargs, defaults)
        self.display = self.get_display()
        self.clock = pg.time.Clock()
        self.set_title(self.cfg["title"])
    def get_display(self):# pg.surface
        """recreates the display and returns it."""
        return pg.display.set_mode(self.cfg["size"])
    def set_title(self, title):
        """sets the new given title to the window."""
        pg.display.set_caption(title)
    def quit(self):
        """exits the app."""
        pg.quit()
        sys.exit()
    def update(self):
        """updates visuals within the window. called at every main-loop end."""
        pg.display.update()
        self.clock.tick(self.cfg["fps"])
