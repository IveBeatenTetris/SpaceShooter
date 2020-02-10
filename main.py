import pygame as pg
from cls.window import Window

class Main(object):
    """main class. will be called on execute."""
    def __init__(self):
        """."""
        self.app = Window(
            size = ((800, 500)),
            title = "Space Shooter 0.1",
            fps = 70
        )
        self.running = True
        self.loop()
    def loop(self):
        """pygame main loop."""
        while self.running:
            # events
            for evt in pg.event.get():
                # quitting the game
                if evt.type is pg.QUIT:
                    self.app.quit()
                if evt.type is pg.KEYDOWN and evt.key is pg.K_ESCAPE:
                    self.app.quit()
            # updating
            self.app.update()

if __name__ == '__main__':
    Main()
