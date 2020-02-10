import pygame as pg
from cls.window import Window
from cls.entity import Entity

class Main(object):
    """main class. will be called on execute."""
    def __init__(self):
        """."""
        self.app = Window(
            size = ((800, 500)),
            title = "Space Shooter 0.1",
            fps = 70
        )
        self.starship = Entity(
            type = "hero"
        )
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

            # updating
            self.app.update()

if __name__ == '__main__':
    Main()
