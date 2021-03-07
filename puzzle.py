import os
import sys
import numpy as np
import pygame as pg
import random
from pygame import mixer


# функция для прорисовки текста
def draw_text(text, x, y):
    font = pg.font.SysFont('Franklin Gothic Heavy', 35)
    img = font.render(text, True, (255, 79, 0))
    screen.blit(img, (x, y))


def load_image(name):  # Проверка фото на наличие
    filename = os.path.join('data', name)
    try:
        image = pg.image.load(filename)
    except pg.error as error:
        print('Не могу загрузить изображение:', name)
        raise SystemExit(error)
    return image


def terminate():
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Пазл')
    size = width, height = 1200, 800
    screen = pg.display.set_mode(size)

    pg.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()

    pg.mixer.music.load('data/sea.wav')
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(-1, 0.0, 5000)

    coords_fish = []
    for _ in range(10):
        coords_fish.append([random.randint(50, 1150), random.randint(50, 750), -1, -1, random.randint(1, 6)])
    v = 100
    clock = pg.time.Clock()

    pg.key.set_repeat(200, 70)

    fps = 60

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill(pg.Color('black'))
        fon_surf = load_image('main.png')
        fon_rect = fon_surf.get_rect()
        screen.blit(fon_surf, fon_rect)
        for elem in coords_fish:
            screen.blit(load_image(f'fish{elem[4]}.png'),
                        load_image(f'fish{elem[4]}.png').get_rect(bottomright=(elem[0], elem[1])))
            elem[0] += (v * clock.tick(60) / 1000) * elem[2]
            elem[1] += (v * clock.tick(60) / 1000) * elem[3]

            if elem[0] <= 10:
                elem[2] = 1
            elif elem[0] >= 490:
                elem[2] = -1

            if elem[1] <= 10:
                elem[3] = 1
            elif elem[1] >= 490:
                elem[3] = -1

        pg.display.flip()
        pg.time.Clock().tick(fps)
    terminate()