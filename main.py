import pygame as pg
from cls.window import Window
from cls.scene import Scene
from cls.entities import *
import utils as u

player = Player(**u.DEFAULT["player"])
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
        # overall key events
        for evt in pg.event.get():
            # quitting the game
            if evt.type is pg.QUIT:
                self.app.quit()
            if evt.type is pg.KEYDOWN and evt.key is pg.K_ESCAPE:
                self.app.quit()
            # transforming starship on moving up/down
            if evt.type is pg.KEYDOWN:
                if evt.key is pg.K_w:
                    player.tilt("up")
                elif evt.key is pg.K_s:
                    player.tilt("down")
            elif evt.type is pg.KEYUP:
                player.tilt()
        # controlling the spaceship
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_d] or keys[pg.K_w] or keys[pg.K_s]:
            self.scene.blit(self.scene.background, player.rect, player.rect)
            if keys[pg.K_a]: player.rect.left -= player.speed
            if keys[pg.K_d]: player.rect.left += player.speed
            if keys[pg.K_w]: player.rect.top -= player.speed
            if keys[pg.K_s]: player.rect.top += player.speed
    def loop(self):
        """pygame main loop."""
        while self.running:
            # events
            self.handle_events()
            # drawing
            self.scene.blit(self.scene.background, player.rect, player.rect)
            self.scene.blit(player.image, player.rect)
            self.app.draw(self.scene)
            # updating
            self.scene.update()
            self.app.update()

if __name__ == '__main__':
    Main()
