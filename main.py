import pygame as pg

pg .init()
screen = pg.display.set_mode((700, 500))
pg.display.set_caption("Space Shooter")
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()
    clock.tick(60)

pg.quit()
