import os
import sys
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


def paint_fish():
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


def draw_picture():
    fon_surf1 = load_image('map1.png')
    for i in range(100, 901, 200):
        for j in range(100, 501, 200):
            t = fon_surf1.copy()
            t = t.subsurface((i - 100, j - 100, 200, 200))
            if map[(j - 100) // 200][(i - 100) // 200] == 0:
                t = pg.transform.flip(t, False, False)
            elif map[(j - 100) // 200][(i - 100) // 200] == 1:
                t = pg.transform.flip(t, True, False)
            elif map[(j - 100) // 200][(i - 100) // 200] == 2:
                t = pg.transform.flip(t, True, True)
            else:
                t = pg.transform.flip(t, False, True)
            screen.blit(t, t.get_rect(topleft=(i, j)))


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

    map = [[random.randint(1, 3) for j in range(5)] for i in range(3)]
    coords_fish = []
    for _ in range(10):
        coords_fish.append([random.randint(100, 1150), random.randint(100, 750), -1, -1, random.randint(1, 6)])
    v = 300
    map_number = random.randint(1, 3)
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
        paint_fish()
        draw_picture()

        pg.display.flip()
        pg.time.Clock().tick(fps)
    terminate()