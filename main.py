import pygame as pg
from cls.window import Window
from cls.scene import Scene
from cls.entities import *
from cls.ui import *
import utils as u
import random

pg.init()

def create_asteroid():
    pivot1 = (
        random.randint(0, screen_size[0]),
        random.randint(-24, screen_size[1] + 24)
    )
    pivot2 = (screen_size[0] + 32, random.randint(-24, screen_size[1] + 24))

    return Asteroid(
        size = (
            random.randint(15, 68),
            random.randint(25, 60)
        ),
        position = pivot1,
        moving = "left",
        speed = random.uniform(0.7, 1.7),
        health = 30
        #box = True,
    )

screen_size, screen_center = (800, 500), (400, 250)
render_list = pg.sprite.RenderUpdates()

player = Player(
    #box = True,
    scale = 2,
    speed = 3,
    damage = 5,
    center = (50, 200)
)
render_list.add(player)

boss1 = Boss(
    center = (650, 250),
    box = True
)
render_list.add(boss1)

count = 0
asteroids = []
while count != 25:
    asteroids.append(create_asteroid())
    count += 1
render_list.add(*asteroids)

healthbar = PlayerHealthBar(
    health = 100,
    midbottom = (int(screen_size[0] / 2), screen_size[1])
)
render_list.add(healthbar)

gameover_text = Text(
    text = "Game Over",
    size = 40,
    center = (screen_center[0], screen_center[1] - 180),
    bold = True
)
tryagain_button = Button(
    text = "Try again",
    size = 30,
    center = (screen_center[0], screen_center[1]),
    background = (35, 35, 45),
    hover = (55, 55, 65),
    padding = [15, 25, 15, 25],
    border = (3, (75, 75, 85))
)

scenes = {
    "startup": Scene(
        size = screen_size,
        position = (0, 0),
        background = (5, 5, 10)
    ),
    "game_over": Scene(
        size = screen_size,
        position = (0, 0),
        background = (5, 5, 10)
    )
}

class Main(object):
    def __init__(self):
        self.app = Window(
            size = scenes["startup"].rect.size,
            title = "Space Shooter 0.1",
            fps = 70
        )
        self.scene = scenes["startup"]
        self.running = True
        self.pause = False
        self.blow_up = Explosion(
            image = u.DEFAULT["explosion"]["image"],
            position = player.rect.center,
            cooldown = 100
        )
        self.loop()
    def handle_events(self):
        blow_up = None
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
                        position = player.rect.topright,
                        direction = "left",
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
                for i, asteroid in enumerate(asteroids):
                    if each.rect.colliderect(asteroid.rect):
                        render_list.add(Explosion(
                            image = u.DEFAULT["explosion"]["image"],
                            position = each.rect.midright,
                            cooldown = 65
                        ))
                        render_list.remove(each)

                        asteroid.hit(player.damage)

                        if asteroid.health <= 0:
                            render_list.remove(asteroid)
                            asteroids[i] = create_asteroid()
                            asteroids[i].reposition((
                                self.app.size[0] + 44,
                                random.randint(-24, screen_size[1] + 24)
                            ))
                            render_list.add(asteroids[i])
            # removing explosion form render list after cooldown reached 0
            elif type(each) is Explosion:
                if each.cooldown == 0:
                    render_list.remove(each)
            elif type(each) is Asteroid:
                if each.rect.colliderect(player.rect):
                    healthbar.health -= each.damage
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
        # game over
        if healthbar.health <= 0:
            render_list.add(self.blow_up)
            if self.blow_up.cooldown > 0:
                self.blow_up.cooldown -= 1
                self.blow_up.rect.center = player.rect.center
            elif self.blow_up.cooldown <= 0:
                self.blow_up = Explosion(
                    image = u.DEFAULT["explosion"]["image"],
                    position = player.rect.center,
                    cooldown = 100,
                    scale = 2
                )
        if self.blow_up.cooldown <= 1:
            render_list.remove(self.blow_up)
            self.blow_up = Explosion(
                image = u.DEFAULT["explosion"]["image"],
                position = player.rect.center,
                cooldown = 100,
                scale = 2
            )
            self.scene = scenes["game_over"]
        # boss shooting
        time_stamps = [*str(pg.time.get_ticks())]
        if random.randint(1, 25) == 12:
            render_list.add(Projectile(
                image = player.standard_shot,
                rotation = player.cfg["rotation"],
                direction = "right",
                position = boss1.rect.topleft,
            ))
    def loop(self):
        """pygame main loop."""
        while self.running:
            if self.scene is scenes["startup"]:
                # events
                self.handle_events()
                # drawing
                render_list.clear(self.scene, self.scene.background)
                changes = render_list.draw(self.scene)
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
            elif self.scene is scenes["game_over"]:
                for evt in pg.event.get():
                    if evt.type is pg.QUIT:
                        self.app.quit()
                    if evt.type is pg.KEYDOWN and evt.key is pg.K_ESCAPE:
                        self.app.quit()

                self.scene.blit(self.scene.background, (0, 0))
                self.scene.blit(gameover_text.image, gameover_text.rect)
                self.scene.blit(tryagain_button.image, tryagain_button.rect)
                self.app.draw(self.scene)

                self.scene.update()
                tryagain_button.update()
                self.app.update()
                # start over
                if tryagain_button.click:
                    self.scene = scenes["startup"]
                    self.scene.blit(self.scene.background, (0, 0))
                    healthbar.health = 100

if __name__ == '__main__':
    Main()
