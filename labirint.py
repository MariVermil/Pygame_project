import os
import sys
import numpy as np
import pygame as pg
from pygame import time


def load_image(name):  # Проверка фото на наличие
    filename = os.path.join('data', name)
    try:
        image = pg.image.load(filename)
    except pg.error as error:
        print('Не могу загрузить изображение:', name)
        raise SystemExit(error)
    return image


class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.pos = (pos_x, pos_y)
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15,
                                               tile_height * pos_y + 5)

    def move(self, x, y):

        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


def load_level(filename):
    filename = os.path.join('data', filename)
    with open(filename, 'r') as mapfile:
        levelmap = np.array([list(i) for i in [line.strip() for line in mapfile]])
    return levelmap


def generate_level(level):
    player, x, y = None, None, None
    row, col = level.shape
    for y in range(row):
        for x in range(col):
            if level[y, x] == '#':
                Tile('wall', x, y)
            elif level[y, x] == '@':
                level[y, x] = '.'
                player = Player(x, y)
    return player, x, y


def move_player(player, movement):  # Движение персонажа
    x, y = player.pos
    if movement == 'up':
        if y > 0 and levelmap[y - 1, x] == '.':
            player.move(x, y - 1)
    elif movement == 'down':
        if y < level_y - 1 and levelmap[y + 1, x] == '.':
            player.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and levelmap[y, x - 1] == '.':
            player.move(x - 1, y)
    elif movement == 'right':
        if x < level_x - 1 and levelmap[y, x + 1] == '.':
            player.move(x + 1, y)


def terminate():
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Лабиринт')
    size = width, height = 1200, 800
    screen = pg.display.set_mode(size)

    player_image = load_image('stand.png')

    tile_images = {
        'wall': load_image('box.png')
    }
    tile_width = tile_height = 24

    player_group = pg.sprite.Group()
    tiles_group = pg.sprite.Group()

    levelmap = load_level('level-01.map')

    player, level_x, level_y = generate_level(levelmap)

    pg.key.set_repeat(200, 70)

    fps = 60
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    move_player(player, 'up')
                elif event.key == pg.K_DOWN:
                    move_player(player, 'down')
                elif event.key == pg.K_LEFT:
                    move_player(player, 'left')
                elif event.key == pg.K_RIGHT:
                    move_player(player, 'right')
        screen.fill(pg.Color('black'))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pg.display.flip()
        time.Clock().tick(fps)
    terminate()