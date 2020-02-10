import pygame as pg
from cls.window import Window
from cls.scene import Scene
from cls.entities import *

player = Player()
scenes = {
    "startup": Scene(
        size = (800, 500),
        position = (0, 0),
        background = (5, 5, 10)
    )
}

class Main(object):
    """main class. will be called on execute."""
    def __init__(self):
        """
        'app'               'window' the window object to display scenes in.
        'starship'          'entity' represents the controllable spaceship.
        'scene'             'scene' based on this, the related scene will be
                            used for displaying it in the window object.
        'running'           'bool' used to evaluate running process.
        """
        self.app = Window(
            size = scenes["startup"].rect.size,
            title = "Space Shooter 0.1",
            fps = 70
        )
        self.scene = scenes["startup"]
        self.running = True

        self.loop()
    def handle_events(self):
        """returns a list of pygame-events."""
        for evt in pg.event.get():
            # quitting the game
            if evt.type is pg.QUIT:
                self.app.quit()
            if evt.type is pg.KEYDOWN and evt.key is pg.K_ESCAPE:
                self.app.quit()
    def loop(self):
        """pygame main loop."""
        while self.running:
            # events
            self.handle_events()
            # drawing
            self.app.draw(self.scene)
            # updating
            self.app.update()

if __name__ == '__main__':
    Main()
