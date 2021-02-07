import os
import sys
import numpy as np
import pygame as pg
from pygame import time


# import pyganim
# import arcade


def load_image(name):
    filename = os.path.join('data', name)
    try:
        image = pg.image.load(filename)
    except pg.error as error:
        print('Не могу загрузить изображение:', name)
        raise SystemExit(error)
    return image


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


def start_screen():
    # Выводим изображение заставки:
    start_screen_background = load_image('start-screen.jpg')
    screen.blit(start_screen_background, (0, 0))
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                return  # Начинаем игру
        pg.display.flip()


def load_level(filename):
    filename = os.path.join('data', filename)
    # Читаем уровень
    with open(filename, 'r') as mapfile:
        levelmap = np.array([list(i) for i in [line.strip() for line in mapfile]])
    return levelmap


def generate_level(level):
    # Создаём элементы игрового поля:
    x, y = None, None
    row, col = level.shape
    for y in range(row):
        for x in range(col):
            if level[y, x] == '.':
                Tile('empty', x, y)
            elif level[y, x] == '/':
                Tile('dirt', x, y)
            elif level[y, x] == '?':
                Tile('dirt_edge', x, y)
            elif level[y, x] == '!':
                Tile('edge', x, y)
            elif level[y, x] == '2':
                Tile('dirt_edge2', x, y)
            elif level[y, x] == '1':
                Tile('edge1', x, y)
            elif level[y, x] == '#':
                Tile('wall', x, y)
    # Возвращаем клеточный размер игрового поля:
    return x, y


class Player:
    def __init__(self, x, y):
        self.stand_img = load_image('stand.png')
        self.img = self.stand_img
        # списки с кадрами анимации
        self.walk_r = list()
        self.walk_l = list()
        self.index = 0
        self.fps_counter = 0
        # занесение кадров в список
        for i in range(1, 5):
            img = load_image(f'walk{i}.png')
            img_left = pg.transform.flip(img, True, False)
            self.walk_l.append(img_left)
            self.walk_r.append(img)
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = x, y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):
        # дельта для коллюжена
        dx = 0
        dy = 0
        walk_cooldown = 10
        # считывание нажатий кнопок передвижения
        key = pg.key.get_pressed()
        if key[pg.K_SPACE] and self.jumped is False:
            self.vel_y = -20
            self.jumped = True
        if not key[pg.K_SPACE]:
            self.jumped = False
        if key[pg.K_LEFT] or key[pg.K_a]:
            dx -= 8
            self.direction = -1
            self.fps_counter += 1
        if key[pg.K_d]:
            dx += 8
            self.fps_counter += 1
            self.direction = 1
        if not key[pg.K_d] and not key[pg.K_a]:
            self.fps_counter = 0
            # куда смотрит игрок (право или лево)
            if self.direction == -1:
                self.img = pg.transform.flip(self.stand_img, True, False)
            if self.direction == 1:
                self.img = self.stand_img
        # анимация
        if self.fps_counter >= walk_cooldown:
            self.fps_counter = 0
            if self.direction == -1:
                self.img = self.walk_l[self.index]
            if self.direction == 1:
                self.img = self.walk_r[self.index]
            self.index += 1
            if self.index > 3:
                self.index = 0
        # прыжок + гравитация
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        # проверка коллюжена

        # обновление координат игрока
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.bottom > height:
            self.rect.bottom = height
        # рисуем игрока на экране
        screen.blit(self.img, self.rect)


def terminate():
    # Определяем отдельную функцию выхода из игры
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('test')
    size = width, height = 1000, 700
    screen = pg.display.set_mode(size)
    # Тайлы
    tile_images = {
        'wall': load_image('grass.png'),
        'empty': load_image('sky_test.png'),
        'dirt': load_image('dark_dirt.png'),
        'edge': load_image('grass2.png'),
        'edge1': load_image('grass2.png'),
        'dirt_edge': load_image('dark_dirt_edge_right.png'),
        'dirt_edge2': load_image('dark_dirt_edge_left.png'),
    }
    # Задаём размер тайлов:
    tile_width = tile_height = 70
    # Группа:
    tiles_group = pg.sprite.Group()
    all_sprites = pg.sprite.Group()

    ##print(tiles_group)

    start_screen()
    # генерация уровня
    levelmap = load_level('level-01.map')
    level_x, level_y = generate_level(levelmap)
    player = Player(100, 100)
    fps = 60
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill(pg.Color(201, 232, 255))
        ##for sprite in tiles_group:
        ##    screen.blit(sprite.image, camera.apply(sprite))
        tiles_group.draw(screen)
        player.update()
        pg.display.flip()
        time.Clock().tick(fps)
    terminate()
