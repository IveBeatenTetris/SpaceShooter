import pygame as pg
from cls.window import Window
from cls.scene import Scene
from cls.entities import *
import utils as u
import random

screen_size = (800, 500)
render_list = pg.sprite.RenderUpdates()

player = Player(
    #box = True,
    scale = 2
)
player.rect.topleft = (50, 200)

count = 0
asteroids = []
while count != 25:
    pivot = (
        random.randint(0, screen_size[0]),
        random.randint(-24, screen_size[1] + 24)
    )
    asteroids.append(Asteroid(
        size = (
            random.randint(15, 68),
            random.randint(25, 60)
        ),
        position = pivot,
        moving = "left",
        speed = random.uniform(0.7, 1.7),
        health = 32
        #box = True,
    ))
    count += 1
render_list.add(*asteroids)

scenes = {
    "startup": Scene(
        size = screen_size,
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
        keys = pg.key.get_pressed()
        # overall key events
        for evt in pg.event.get():
            # quitting the game
            if evt.type is pg.QUIT:
                self.app.quit()
            if evt.type is pg.KEYDOWN and evt.key is pg.K_ESCAPE:
                self.app.quit()
            # tilting starship on moving up/down
            if evt.type is pg.KEYDOWN:
                if evt.key is pg.K_w:
                    player.tilt("up")
                elif evt.key is pg.K_s:
                    player.tilt("down")
                elif evt.key is pg.K_a:
                    player.tilt("left")
                elif evt.key is pg.K_d:
                    player.tilt("right")
            # resetting tilt image
            elif evt.type is pg.KEYUP:
                player.tilt()
            elif evt.type is pg.MOUSEBUTTONDOWN:
                # shooting
                if evt.button == 1:
                    render_list.add(Projectile(
                        image = player.standard_shot,
                        rotation = player.cfg["rotation"],
                        position = player.rect.topright
                    ))
        # moving the spaceship
        if keys[pg.K_a] or keys[pg.K_d] or keys[pg.K_w] or keys[pg.K_s]:
            self.scene.blit(self.scene.background, player.rect, player.rect)
            if keys[pg.K_a]: player.rect.left -= player.speed
            if keys[pg.K_d]: player.rect.left += player.speed
            if keys[pg.K_w]: player.rect.top -= player.speed
            if keys[pg.K_s]: player.rect.top += player.speed
        # handling collisions and explosions
        for each in render_list:
            if type(each) is Projectile:
                for asteroid in asteroids:
                    if each.rect.colliderect(asteroid.rect):
                        render_list.add(Explosion(
                            image = u.DEFAULT["explosion"]["image"],
                            position = each.rect.midright
                        ))
                        render_list.remove(each)

                        asteroid.hit(2)
                        if asteroid.health < 1:
                            asteroids.remove(asteroid)
                            render_list.remove(asteroid)
            elif type(each) is Explosion:
                if each.cooldown[0] == 0:
                    render_list.remove(each)
        # restarting sprites going out of bounds
        for each in render_list:
            if type(each) is Projectile:
                if each.rect.left > self.app.size[0]:
                    render_list.remove(each)
            elif type(each) is Asteroid:
                if each.moving:
                    if each.moving == "left":
                        if each.rect.right < 0:
                            each.reposition((
                                self.app.size[0] + each.rect.width,
                                random.randint(-24, screen_size[1] + 24)
                            ))
                    elif each.moving == "right":
                        if each.rect.left > self.app.size[0]:
                            each.reposition((
                                -each.rect.width,
                                random.randint(-24, screen_size[1] + 24)
                            ))
    def loop(self):
        """pygame main loop."""
        while self.running:
            # events
            self.handle_events()
            # drawing
            render_list.clear(self.scene, self.scene.background)
            changes = render_list.draw(self.scene)
            self.scene.blit(player.image, player.rect)
            self.app.draw(self.scene)
            self.app.draw(
                u.createText(
                    text = "fps: {}".format(int(self.app.clock.get_fps()))
                )
            )
            # updating
            for each in render_list: each.update()
            self.scene.update()
            self.app.update(changes)

if __name__ == '__main__':
    Main()
