import os
import sys
import numpy as np
import pygame as pg
from pygame import time
import random


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
        self.rect = self.image.get_rect().move(tile_width * pos_x + 5,
                                               100 + tile_height * pos_y)
        self.coins = None
        self.sum_coins = 0

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 5,
                                               100 + tile_height * self.pos[1])

    def update(self):
        coins_hit_list = pg.sprite.spritecollide(self, self.coins, False)
        for coin in coins_hit_list:
            self.sum_coins += 1
            coin.kill()


used_coins = [1, 2, 3, 4, 5, 6, 7]


class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(coins_group)
        k = random.choice(used_coins)
        print(k)
        self.image = load_image(f'coin{k}.png')
        del used_coins[used_coins.index(k)]
        self.rect = self.image.get_rect().move(tile_width * y,
                                               100 + tile_height * x)


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               100 + tile_height * pos_y)


def load_level(filename):
    filename = os.path.join('data', filename)
    with open(filename, 'r') as mapfile:
        levelmap = np.array([list(i) for i in [line.strip() for line in mapfile]])
        while len(coins_coord) < 7:
            k1 = random.randint(0, 24)
            k2 = random.randint(0, 45)
            if levelmap[k1, k2] == '.' and [k1, k2] not in coins_coord:
                coins_coord.append([k1, k2])
                print(k1, k2, levelmap[k1, k2])
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
        'wall': load_image('box1.png')
    }
    tile_width = 26
    tile_height = 28

    player_group = pg.sprite.Group()
    tiles_group = pg.sprite.Group()

    coins_coord = []
    levelmap = load_level('level-01.map')
    player, level_x, level_y = generate_level(levelmap)

    coins_group = pg.sprite.Group()
    for coord in coins_coord:
        coin = Coin(coord[0], coord[1])
        coins_group.add(coin)

    player.coins = coins_group

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
        sun_surf = load_image('fon.png')
        sun_rect = sun_surf.get_rect()
        screen.blit(sun_surf, sun_rect)
        tiles_group.draw(screen)
        player_group.draw(screen)
        coins_group.draw(screen)
        player.update()
        pg.display.flip()
        time.Clock().tick(fps)
    terminate()