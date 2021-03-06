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


x_end, y_end = 0, 0


class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.pos = (pos_x, pos_y)
        self.rect = self.image.get_rect().move(tile_width * pos_x + 5,
                                               100 + tile_height * pos_y)
        self.coins = None
        self.sum_coins = 0
        self.enemies = None
        self.alive = True

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 5,
                                               100 + tile_height * self.pos[1])
        global x_end, y_end
        x_end, y_end = x, y

    def update(self):
        coins_hit_list = pg.sprite.spritecollide(self, self.coins, False)
        for coin in coins_hit_list:
            self.sum_coins += 1
            coin.kill()

        if pg.sprite.spritecollideany(self, self.enemies):
            self.alive = False


class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(coins_group)
        k = random.choice(used_coins)
        self.image = load_image(f'coin{k}.png').convert_alpha()
        del used_coins[used_coins.index(k)]
        self.rect = self.image.get_rect().move(tile_width * y,
                                               100 + tile_height * x)


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, end_x, end_y):
        super().__init__()
        self.image = load_image('enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = tile_width * y
        self.rect.y = 100 + tile_height * x
        self.start_x = tile_width * y
        self.start_y = 100 + tile_height * x
        self.end_x = end_y * tile_width
        self.end_y = end_x * tile_height + 100
        self.direction = 1

    def update(self):
        if self.end_y > self.start_y:
            if self.rect.y >= self.end_y:
                self.rect.y = self.end_y
                self.direction = -1
            if self.rect.y <= self.start_y:
                self.rect.y = self.start_y
                self.direction = 1
            self.rect.y += tile_height * self.direction
        else:
            if self.rect.x >= self.end_x:
                self.rect.x = self.end_x
                self.direction = -1
            if self.rect.x <= self.start_x:
                self.rect.x = self.start_x
                self.direction = 1
            self.rect.x += tile_width * self.direction


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
        while len(coins_coord) < 10:
            k1 = random.randint(0, 24)
            k2 = random.randint(0, 45)
            if levelmap[k1, k2] == '.' and [k1, k2] not in coins_coord:
                coins_coord.append([k1, k2])
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


def count_time():
    if sec // 300 < 2:
        pass_surf = load_image('gold.png')
        pass_rect = pass_surf.get_rect(bottomright=(1190, 90))
        screen.blit(pass_surf, pass_rect)
    elif sec // 300 < 4:
        pass_surf = load_image('silver.png')
        pass_rect = pass_surf.get_rect(bottomright=(1190, 90))
        screen.blit(pass_surf, pass_rect)
    else:
        pass_surf = load_image('bronze.png')
        pass_rect = pass_surf.get_rect(bottomright=(1190, 90))
        screen.blit(pass_surf, pass_rect)


def terminate():
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Лабиринт')
    size = width, height = 1200, 800
    screen = pg.display.set_mode(size)

    pg.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()

    player_image = load_image('stand.png')

    tile_images = {
        'wall': load_image('box1.png')
    }
    tile_width = 26
    tile_height = 28

    player_group = pg.sprite.Group()
    tiles_group = pg.sprite.Group()

    pg.mixer.music.load('data/music1.wav')
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(-1, 0.0, 5000)

    used_coins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    coins_coord = []
    levelmap = load_level('level-01.map')
    player, level_x, level_y = generate_level(levelmap)

    coins_group = pg.sprite.Group()
    for coord in coins_coord:
        coin = Coin(coord[0], coord[1])
        coins_group.add(coin)

    player.coins = coins_group

    enemy_group = pg.sprite.Group()
    player.enemies = enemy_group
    enemies_coord = [[1, 1, 23, 1], [1, 44, 23, 44], [3, 18, 21, 18], [3, 28, 21, 28], [8, 5, 8, 14],
                     [17, 5, 17, 14], [8, 32, 8, 40], [17, 32, 17, 40]]
    for coord in enemies_coord:
        enemy = Enemy(coord[0], coord[1], coord[2], coord[3])
        enemy_group.add(enemy)

    pg.key.set_repeat(200, 70)

    fps = 60
    sec = 0

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

        if not player.alive:
            pass_surf = load_image('pass.png')
            pass_rect = pass_surf.get_rect()
            screen.blit(pass_surf, pass_rect)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()
                elif event.type == pg.KEYDOWN or \
                        event.type == pg.MOUSEBUTTONDOWN:
                    player.alive = True
                    player_group = pg.sprite.Group()
                    tiles_group = pg.sprite.Group()

                    used_coins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    coins_coord = []
                    levelmap = load_level('level-01.map')
                    player, level_x, level_y = generate_level(levelmap)

                    coins_group = pg.sprite.Group()
                    for coord in coins_coord:
                        coin = Coin(coord[0], coord[1])
                        coins_group.add(coin)

                    player.coins = coins_group

                    enemy_group = pg.sprite.Group()
                    player.enemies = enemy_group
                    enemies_coord = [[1, 1, 23, 1], [1, 44, 23, 44], [3, 18, 21, 18], [3, 28, 21, 28], [8, 5, 8, 14],
                                     [17, 5, 17, 14], [8, 32, 8, 40], [17, 32, 17, 40]]
                    for coord in enemies_coord:
                        enemy = Enemy(coord[0], coord[1], coord[2], coord[3])
                        enemy_group.add(enemy)

                    pg.key.set_repeat(200, 70)

                    fps = 60
                    sec = 0
        elif x_end == 21 and y_end == 0:
            if sec // 180 < 2:
                pass_surf = load_image('end1.png')
                pass_rect = pass_surf.get_rect()
                screen.blit(pass_surf, pass_rect)
            elif sec // 180 < 4:
                pass_surf = load_image('end2.png')
                pass_rect = pass_surf.get_rect()
                screen.blit(pass_surf, pass_rect)
            else:
                pass_surf = load_image('end3.png')
                pass_rect = pass_surf.get_rect()
                screen.blit(pass_surf, pass_rect)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()
                elif event.type == pg.KEYDOWN or \
                        event.type == pg.MOUSEBUTTONDOWN:
                    terminate()
        else:
            fon_surf = load_image('fon.png')
            fon_rect = fon_surf.get_rect()
            screen.blit(fon_surf, fon_rect)
            tiles_group.draw(screen)
            player_group.draw(screen)
            coins_group.draw(screen)
            enemy_group.draw(screen)
            enemy_group.update()
            player.update()
            draw_text(f'Прошло времени  {str(sec // 300)} : {str((sec // 5) % 60)}', 775, 25)
            draw_text(f'Собрано предметов:  {str(player.sum_coins)} / 10', 12, 25)
            count_time()
        pg.display.flip()
        sec += 1
        pg.time.Clock().tick(fps)
    terminate()