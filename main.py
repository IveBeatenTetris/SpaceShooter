import pygame as pg

class Main(object):
    """main class. will be called on execute."""
    def __init__(self):
        """."""
        pg.init()
        self.screen = pg.display.set_mode((700, 500))
        pg.display.set_caption("Space Shooter")
        self.clock = pg.time.Clock()
        self.running = True
        self.loop()
    def loop(self):
        """pygame main loop."""
        while self.running:
            # events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            # updating
            pg.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    Main()
