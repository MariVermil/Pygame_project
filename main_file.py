import os
import sys
import numpy as np
import pygame as pg
import random
from pygame import mixer
from datetime import datetime


def return_screen(name):
    # заставка
    start_screen_background = load_image(name)
    screen.blit(start_screen_background, (0, 0))
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return  # Начинаем игру
        pg.display.flip()


def end_screen():
    # конечная картинка
    end_pic = load_image('end.png')
    screen.blit(end_pic, (0, 0))
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
        pg.display.flip()


# функция для прорисовки текста
def draw_text(text, x, y, font=None):
    if font is None:
        font = pg.font.SysFont('Franklin Gothic Heavy', 35)
        img = font.render(text, True, (255, 79, 0))
        screen.blit(img, (x, y))
    else:
        img = font.render(text, True, (0, 5, 5))
        run.screen.blit(img, (x, y))


def load_image(name):  # Проверка фото на наличие
    filename = os.path.join('data', name)
    try:
        image = pg.image.load(filename)
    except pg.error as error:
        print('Не могу загрузить изображение:', name)
        raise SystemExit(error)
    return image


class Board_puzzle:
    def __init__(self, row, col):
        self.row = row  # кол-во строк
        self.col = col  # кол-во столбцов
        self.map = [[random.randint(1, 3) for j in range(5)] for i in range(3)]
        self.top = 100  # отступ сверху
        self.left = 100  # отступ слева
        self.cell_size = 200  # размер ячейки
        self.map_number = random.randint(1, 3)

    def draw_picture(self):
        fon_surf1 = load_image(f'map{self.map_number}.png')
        for i in range(100, 901, 200):
            for j in range(100, 501, 200):
                t = fon_surf1.copy()
                t = t.subsurface((i - 100, j - 100, 200, 200))
                if self.map[(j - 100) // 200][(i - 100) // 200] == 0:
                    t = pg.transform.flip(t, False, False)
                elif self.map[(j - 100) // 200][(i - 100) // 200] == 1:
                    t = pg.transform.flip(t, True, False)
                elif self.map[(j - 100) // 200][(i - 100) // 200] == 2:
                    t = pg.transform.flip(t, True, True)
                else:
                    t = pg.transform.flip(t, False, True)
                screen.blit(t, t.get_rect(topleft=(i, j)))

    def get_click(self, mouse_pos):
        status = self.get_cell(mouse_pos)
        if status != 'None':
            self.map[status[0]][status[1]] = \
                (self.map[status[0]][status[1]] + 1) % 4

    def get_cell(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]
        i = (y - self.top) // self.cell_size
        j = (x - self.left) // self.cell_size
        if i < 0 or i >= self.row or j < 0 or j >= self.col:
            return 'None'
        else:
            return i, j


def paint_fish():
    for elem in coords_fish:
        screen.blit(load_image(f'fish{elem[4]}.png'),
                    load_image(f'fish{elem[4]}.png').get_rect(
                        bottomright=(elem[0], elem[1])))
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


x_end, y_end = 0, 0  # Координаты


class Player_labirint(pg.sprite.Sprite):
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

    def update(self):  # Проверка на столкновение с предметом или врагом
        coins_hit_list = pg.sprite.spritecollide(self, self.coins, False)
        for coin in coins_hit_list:
            self.sum_coins += 1
            coin.kill()

        if pg.sprite.spritecollideany(self, self.enemies):
            self.alive = False


class Thing(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(coins_group)
        k = random.choice(used_coins)
        self.image = load_image(f'thing{k}.png').convert_alpha()
        del used_coins[used_coins.index(k)]
        self.rect = self.image.get_rect().move(tile_width * y,
                                               100 + tile_height * x)


class Enemy_labirint(pg.sprite.Sprite):
    def __init__(self, x, y, end_x, end_y):
        super().__init__()
        self.image = load_image('enemy1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = tile_width * y
        self.rect.y = 100 + tile_height * x
        self.start_x = tile_width * y
        self.start_y = 100 + tile_height * x
        self.end_x = end_y * tile_width
        self.end_y = end_x * tile_height + 100
        self.direction = 1

    def update(self):  # Движение врагов
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


class Tile1(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               100 + tile_height * pos_y)


def load_level1(filename):
    filename = os.path.join('data', filename)
    with open(filename, 'r') as mapfile:
        levelmap = np.array([list(i) for i in
                             [line.strip() for line in mapfile]])
        while len(coins_coord) < 10:
            k1 = random.randint(0, 24)
            k2 = random.randint(0, 45)
            if levelmap[k1, k2] == '.' and [k1, k2] not in coins_coord:
                coins_coord.append([k1, k2])
    return levelmap


def generate_level1(level):
    player, x, y = None, None, None
    row, col = level.shape
    for y in range(row):
        for x in range(col):
            if level[y, x] == '#':
                Tile1('wall', x, y)
            elif level[y, x] == '@':
                level[y, x] = '.'
                player = Player_labirint(x, y)
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


def count_time(time):  # Расчёт того, какой сейчас кубок
    if time // 60 < 2:
        pass_surf = load_image('gold.png')
        pass_rect = pass_surf.get_rect(bottomright=(1190, 90))
        screen.blit(pass_surf, pass_rect)
    elif time // 60 < 4:
        pass_surf = load_image('silver.png')
        pass_rect = pass_surf.get_rect(bottomright=(1190, 90))
        screen.blit(pass_surf, pass_rect)
    else:
        pass_surf = load_image('bronze.png')
        pass_rect = pass_surf.get_rect(bottomright=(1190, 90))
        screen.blit(pass_surf, pass_rect)


def labirint_run():
    pg.display.set_caption('Лабиринт')
    global player_image, tile_images, tile_width, \
        tile_height, used_coins, levelmap, level_x, level_y, \
        coins_coord, tiles_group, coins_group, player_group, run

    # включаем музыку
    try:
        pg.mixer.music.load('data/music1.wav')
    except:
        pg.mixer.music.load('data/music1.mp3')
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(-1, 0.0, 5000)

    return_screen('2pic.png')

    # спрайты
    player_image = load_image('stand1.png')
    tile_images = {
        'wall': load_image('box1.png')
    }
    tile_width = 26
    tile_height = 28
    player_group = pg.sprite.Group()
    tiles_group = pg.sprite.Group()

    # создание карты и предметов на ней
    used_coins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    coins_coord = []
    levelmap = load_level1('level-02.map')
    player, level_x, level_y = generate_level1(levelmap)

    coins_group = pg.sprite.Group()
    for coord in coins_coord:
        coin = Thing(coord[0], coord[1])
        coins_group.add(coin)
    player.coins = coins_group

    # создание врагов
    enemy_group = pg.sprite.Group()
    player.enemies = enemy_group
    enemies_coord = [[1, 1, 23, 1], [1, 44, 23, 44], [3, 18, 21, 18],
                     [3, 28, 21, 28], [8, 5, 8, 14],
                     [17, 5, 17, 14], [8, 32, 8, 40], [17, 32, 17, 40]]
    for coord in enemies_coord:
        enemy = Enemy_labirint(coord[0], coord[1], coord[2], coord[3])
        enemy_group.add(enemy)

    pg.key.set_repeat(200, 70)
    fps = 60
    data_now = datetime.today()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
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
        sec = datetime.today() - data_now
        time = int(str(sec.seconds))

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
                    levelmap = load_level1('level-02.map')
                    player, level_x, level_y = generate_level1(levelmap)

                    coins_group = pg.sprite.Group()
                    for coord in coins_coord:
                        coin = Thing(coord[0], coord[1])
                        coins_group.add(coin)

                    player.coins = coins_group

                    enemy_group = pg.sprite.Group()
                    player.enemies = enemy_group
                    enemies_coord = [[1, 1, 23, 1], [1, 44, 23, 44],
                                     [3, 18, 21, 18], [3, 28, 21, 28],
                                     [8, 5, 8, 14], [17, 5, 17, 14],
                                     [8, 32, 8, 40], [17, 32, 17, 40]]
                    for coord in enemies_coord:
                        enemy = Enemy_labirint(coord[0], coord[1],
                                               coord[2], coord[3])
                        enemy_group.add(enemy)

                    pg.key.set_repeat(100, 70)

                    fps = 60
                    data_now = datetime.today()
        elif x_end == 21 and y_end == 0 and player.sum_coins == 10:
            if time // 60 < 2:
                pass_surf = load_image('end1.png')
                pass_rect = pass_surf.get_rect()
                screen.blit(pass_surf, pass_rect)
            elif time // 60 < 4:
                pass_surf = load_image('end2.png')
                pass_rect = pass_surf.get_rect()
                screen.blit(pass_surf, pass_rect)
            else:
                pass_surf = load_image('end3.png')
                pass_rect = pass_surf.get_rect()
                screen.blit(pass_surf, pass_rect)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    terminate()
                elif event.type == pg.KEYDOWN or \
                        event.type == pg.MOUSEBUTTONDOWN:
                    run = Game()
                    while run.running:
                        run.new()
                    pg.quit()
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
            draw_text(f'Прошло времени  '
                      f'{str(time // 60)} : {str(time % 60)}', 775, 25)
            draw_text(f'Собрано предметов:  '
                      f'{str(player.sum_coins)} / 10', 12, 25)
            count_time(time)
        pg.display.flip()
        pg.time.Clock().tick(fps)
    terminate()


def load_level(filename):
    filename = os.path.join('data', filename)
    # Читаем уровень
    with open(filename, 'r') as mapfile:
        levelmap = np.array([list(i) for i in [line.strip() for line in mapfile]])
    return levelmap


def generate_level(level):
    # элементы игрового поля, мобов
    data_lst = list()
    row, col = level.shape
    for y in range(row):
        for x in range(col):
            if level[y, x] == '/':
                data_lst.append(Tile('dirt', x, y))
            elif level[y, x] == '3':
                data_lst.append(Tile('grass_plate_edge_r', x, y))
            elif level[y, x] == '4':
                data_lst.append(Tile('grass_plate_edge_l', x, y))
            elif level[y, x] == '5':
                data_lst.append(Tile('grass_plate', x, y))
            elif level[y, x] == '6':
                data_lst.append(Tile('half', x, y))
            elif level[y, x] == '7':
                data_lst.append(Tile('half2', x, y))
            elif level[y, x] == '#':
                data_lst.append(Tile('wall', x, y))
            elif level[y, x] == 's':
                s = School(x, y)
                run.all_sprites.add(s)
            elif level[y, x] == 'c':
                c = Coin(x, y)
                run.all_sprites.add(c)
                run.coin_group.add(c)
            elif level[y, x] == 'l':
                lava_block = Lava(x, y)
                run.lava_group.add(lava_block)
                run.all_sprites.add(lava_block)
            elif level[y, x] == 'f':
                data_lst.append(Tile('lava_fill', x, y))
            elif level[y, x] == '@':
                enem = Enemy(x, y)
                run.mobs.add(enem)
                run.all_sprites.add(enem)
    return data_lst


class School(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image('house.png')
        self.rect = self.image.get_rect().move(pos_x * run.tile_width,
                                               (pos_y * run.tile_height) - 400)


# разрезание листа с картинками на отдельные кадры
def animasprite(sheet, cols, rows):
    frames = []
    rect = pg.Rect(0, 0, sheet.get_width() // cols, sheet.get_height() // rows)
    for j in range(rows):
        for i in range(cols):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pg.Rect(frame_location, rect.size)))
    return frames


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.image = run.tile_images[tile_type]
        self.rect = self.image.get_rect().move(run.tile_width * pos_x,
                                               run.tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)
        self.out()

    def out(self):
        return self.abs_pos[0], self.abs_pos[1], 70, 70


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(run.width / 2.2)
        y = -target.rect.y + int(run.height / 2.2)
        # лимит
        x = min(0, x)  # лево
        y = min(0, y)  # верх
        self.camera = pg.Rect(x, y, self.width, self.height)


class Button:
    def __init__(self, image, pressed):
        self.press_img = load_image(pressed)
        self.img = load_image(image)
        self.image = self.img
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 430, 530

    def draw(self):
        self.act = False
        # позиция мыши, нажатие левой кнопки мыши
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = self.press_img
        else:
            self.image = self.img
        run.screen.blit(self.image, self.rect)


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.reset(game)

    def reset(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        # спрайт игрока
        self.stand = load_image('stand.png')
        self.image = self.stand
        self.dead_image = load_image('ded.png')
        self.dead_gravity_count = 0
        self.rect = pg.rect.Rect((5, 880), (70, 148))
        self.on_ground = False
        # трение
        self.friction = -0.12
        # скорость передвижения игрока
        self.vel = vec(0, 0)
        # ускорение
        self.acc = vec(0, 0)
        # переменные для анимации, списки с кадрами
        self.walking = False
        self.walk_r_lst = animasprite(load_image('walk.png'), 4, 1)
        self.walk_l_lst = list()
        for frame in self.walk_r_lst:
            self.walk_l_lst.append(pg.transform.flip(frame, True, False))
        # счетчик кадров
        self.current_frame = 0
        self.last_update = 0
        # в какую сторону смотрит игрок
        self.look = 0

    def jump(self):
        # стоит ли игрок на поверхности
        if self.on_ground:
            self.vel.y = -20

    def update(self):
        self.animate()
        self.acc = vec(0, 0.7)
        # считывание нажатий кнопок передвижения
        if self.game.game_over == 0:
            key = pg.key.get_pressed()
            if key[pg.K_LEFT] or key[pg.K_a]:
                self.acc.x = -0.95
                self.look = 1
            if key[pg.K_RIGHT] or key[pg.K_d]:
                self.acc.x = 0.95
                self.look = 0
            if key[pg.K_SPACE]:
                if self.on_ground:
                    self.game.jump_fx.play()
                self.jump()
            # обновление координат игрока, применение трения
            self.acc.x += self.vel.x * self.friction
            # выравнивание скорости + инерция
            self.vel.x += self.acc.x
            if abs(self.vel.x) < 0.1:
                self.vel.x = 0
            if not self.on_ground:
                self.vel.y += self.acc.y
            self.on_ground = False

            self.rect.y += self.vel.y + 0.5 * self.acc.y
            self.collide(0, self.vel.y)
            self.rect.x += self.vel.x + 0.5 * self.acc.x
            self.collide(self.vel.x, 0)
        elif self.game.game_over == 1:
            if self.look == 0:
                self.image = self.dead_image
            else:
                self.image = pg.transform.flip(self.dead_image, True, False)
            self.dead_gravity_count += 1
            if self.dead_gravity_count <= 17:
                self.rect.y -= 24
            if self.dead_gravity_count > 20:
                if self.dead_gravity_count < 70:
                    self.rect.y += 25

    def collide(self, xvel, yvel):
        for tile in self.game.tiles_group:
            if pg.sprite.collide_rect(self, tile):
                if xvel > 0:
                    self.rect.right = tile.rect.left
                if xvel < 0:
                    self.rect.left = tile.rect.right
                if yvel < 0:
                    self.rect.top = tile.rect.bottom
                    self.vel.y = 0
                if yvel > 0:
                    self.rect.bottom = tile.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                # столкновение с лавой/врагом
                if pg.sprite.spritecollide(self, self.game.mobs, False) or \
                        pg.sprite.spritecollide(self,
                                                self.game.lava_group, False):
                    self.game.game_over = 1
                    self.game.game_over_fx.play()

    def animate(self):
        current = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # анимация ходьбы
        if self.walking:
            if current - self.last_update > 190:
                self.last_update = current
                self.current_frame = (self.current_frame + 1) % len(self.walk_r_lst)
                if self.vel.x > 0:
                    self.image = self.walk_r_lst[self.current_frame]
                else:
                    self.image = self.walk_l_lst[self.current_frame]
        if not self.walking:
            if self.look == 0:
                self.image = self.stand
            else:
                self.image = pg.transform.flip(self.stand, True, False)


class Enemy(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image('enemy.png')
        self.rect = self.image.get_rect().move(run.tile_width * pos_x,
                                               (run.tile_height * pos_y) + 13)
        # списки с кадрами
        self.move_l = animasprite(load_image('enemy_move.png'), 2, 1)
        self.move_r = list()
        for frame in self.move_l:
            self.move_r.append(pg.transform.flip(frame, True, False))
        # счетчик кадров
        self.current_frame = 0
        self.last_update = 0
        # в какую сторону движется/смотрит
        self.look = 2
        self.count = 0

    def update(self):
        self.animate()
        self.rect.x += self.look
        self.count += 1
        if self.count > 90:
            self.look *= -1
            self.count *= -1

    def animate(self):
        current = pg.time.get_ticks()
        if current - self.last_update > 190:
            self.last_update = current
            self.current_frame = (self.current_frame + 1) % len(self.move_l)
            if self.look > 0:
                self.image = self.move_r[self.current_frame]
            else:
                self.image = self.move_l[self.current_frame]


class Coin(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image('coin1.png')
        self.rect = self.image.get_rect().move(run.tile_width * pos_x,
                                               (run.tile_height * pos_y))
        self.animation = animasprite(load_image('coin.png'), 4, 1)
        self.current_frame = 0
        self.last_update = 0

    def update(self):
        self.animate()

    def animate(self):
        current = pg.time.get_ticks()
        if current - self.last_update > 300:
            self.last_update = current
            self.current_frame = (self.current_frame + 1) % len(self.animation)
            self.image = self.animation[self.current_frame]


class Lava(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image('lava.png')
        self.rect = self.image.get_rect().move(run.tile_width * pos_x,
                                               (run.tile_height * pos_y))
        self.animation = animasprite(load_image('lava_move.png'), 2, 1)
        self.current_frame = 0
        self.last_update = 0

    def update(self):
        self.animate()

    def animate(self):
        current = pg.time.get_ticks()
        if current - self.last_update > 1300:
            self.last_update = current
            self.current_frame = (self.current_frame + 1) % len(self.animation)
            self.image = self.animation[self.current_frame]


# вектор
vec = pg.math.Vector2


class Game:
    def __init__(self):
        self.running = True
        pg.init()
        pg.mixer.pre_init(44100, -16, 2, 512)
        mixer.init()
        # параметры для draw_text
        self.font = pg.font.SysFont('Comic Sans', 35)
        pg.display.set_caption('Roota`s adventure')
        size = self.width, self.height = 1200, 800
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(size)
        self.fps = 60
        self.background, self.background_rect = load_image('background.png'), \
                                                load_image('background.png').get_rect()

    def new(self):
        # Тайлы
        self.tile_images = {
            'wall': load_image('grass.png'),
            'dirt': load_image('dark_dirt.png'),
            'grass_plate_edge_r': load_image('grass_edge_plate_right.png'),
            'grass_plate_edge_l': load_image('grass_edge_plate_left.png'),
            'grass_plate': load_image('grass_plate.png'),
            'half': load_image('dark_dirt_half.png'),
            'half2': load_image('dark_dirt_half2.png'),
            'lava': load_image('lava.png'),
            'lava_fill': load_image('lava_fill.png'),
            'school': load_image('house.png')}
        # размер тайлов:
        self.tile_width = self.tile_height = 70
        # кнопки
        self.restart_button = Button('try_unpressed.png', 'try_pressed.png')
        self.restart_check = False
        # Группы:
        self.tiles_group = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.lava_group = pg.sprite.Group()
        self.coin_group = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        # звуки
        try:
            self.coin_fx = pg.mixer.Sound('data/coin_pick.mp3')
            self.jump_fx = pg.mixer.Sound('data/jump.mp3')
            self.game_over_fx = pg.mixer.Sound('data/ded.mp3')
            pg.mixer.music.load('data/theme.mp3')
        except:
            self.coin_fx = pg.mixer.Sound('data/coin_pick.wav')
            self.jump_fx = pg.mixer.Sound('data/jump.wav')
            self.game_over_fx = pg.mixer.Sound('data/ded.wav')
            pg.mixer.music.load('data/theme.wav')
        self.coin_fx.set_volume(0.6)
        self.jump_fx.set_volume(0.05)
        self.game_over_fx.set_volume(0.8)
        pg.mixer.music.set_volume(0.4)
        pg.mixer.music.play(-1, 0.0, 5000)
        # генерация уровня
        self.levelmap = load_level('level_1.map')
        data_lst = generate_level(self.levelmap)
        # помещение тайлов в группы
        for tile in data_lst:
            self.all_sprites.add(tile)
            self.tiles_group.add(tile)
        # камера
        self.camera = Camera(len(self.levelmap), len(self.levelmap[0]))
        # переменная для проверки проигрыша, счёт
        self.score = 0
        self.game_over = 0
        # спавн игрока с референсом к классу Game
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.run()

    def run(self):
        return_screen('3pic.png')
        self.running = True
        while self.running:
            self.playing = True
            while self.playing:
                self.clock.tick(self.fps)
                self.events()
                self.update()
                self.draw()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def events(self):
        # цикл с событиями
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                self.restart_check = True
            else:
                self.restart_check = False
            if pg.Rect.colliderect(self.player.rect, (9630, 750, 150, 100)):
                if self.score == 15:
                    self.playing = False
                    self.running = False
                    return_screen('4pic.png')
                    pg.display.set_caption('Roota`s Adventure')
                    pic = load_image('board.png')
                    board = Board()
                    board.set_view(300, 100, 200)
                    running = True
                    while running:
                        for event in pg.event.get():
                            if event.type == pg.QUIT:
                                running = False
                            if event.type == pg.MOUSEBUTTONDOWN:
                                board.get_click(event.pos)
                        screen.blit(pic, pic.get_rect())
                        # отрисовка счетчика, выход после получения 3 очков
                        draw_text(f'{board.count}/3',
                                  1000, 100, pg.font.SysFont('Comic Sans',
                                                             100))
                        if board.count == 3:
                            running = False
                            end_screen()
                        board.render()
                        pg.display.flip()
                    pg.quit()

    def draw(self):
        # прорисовка всего
        self.screen.blit(self.background, self.background_rect)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # проверка столкновенния с монетами, обновление счетчика
        if pg.sprite.spritecollide(self.player, self.coin_group, True):
            self.score += 1
            self.coin_fx.play()
        draw_text(f'монет:  {str(self.score)} / 15', 12, 10, self.font)
        # рестарт
        if self.game_over == 1:
            self.restart_button.draw()
            if self.restart_check:
                self.player.reset(self)
                self.game_over = 0
        pg.display.flip()


class Board:
    def __init__(self):
        self.count = 0
        self.reset()

    def reset(self):
        self.row = 3
        self.col = 3
        self.board = np.zeros((self.row, self.col), dtype=int)
        self.x_pic = load_image('x.png')
        self.o_pic = load_image('o.png')
        self.top = 100
        self.left = 300
        self.cell_size = 200
        self.status = 2
        self.timer = 0
        self.end = False
        self.winner = 0

    def win_check(self):
        # диагонали
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == 2 and self.board[1][1] == 2 and \
                    self.board[2][2] == 2:
                self.winner = 2
            elif self.board[0][0] == 1 and self.board[1][1] == 1 and \
                    self.board[2][2] == 2:
                self.winner = 1
        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == 2 and self.board[1][1] == 2 and \
                    self.board[2][0] == 2:
                self.winner = 2
            elif self.board[0][2] == 1 and self.board[1][1] == 1 and \
                    self.board[2][0] == 1:
                self.winner = 1
        # горизонтали
        if self.board[0][0] == self.board[0][1] == self.board[0][2]:
            if self.board[0][0] == 2 and self.board[0][1] == 2 and \
                    self.board[0][2] == 2:
                self.winner = 2
            elif self.board[0][0] == 1 and self.board[0][1] == 1 and \
                    self.board[0][2] == 1:
                self.winner = 1
        if self.board[1][0] == self.board[1][1] == self.board[1][2]:
            if self.board[1][0] == 2 and self.board[1][1] == 2 and \
                    self.board[1][2] == 2:
                self.winner = 2
            elif self.board[1][0] == 1 and self.board[1][1] == 1 and \
                    self.board[1][2] == 1:
                self.winner = 1
        if self.board[2][0] == self.board[2][1] == self.board[2][2]:
            if self.board[2][0] == 2 and self.board[2][1] == 2 and \
                    self.board[2][2] == 2:
                self.winner = 2
            elif self.board[2][0] == 1 and self.board[2][1] == 1 and \
                    self.board[2][2] == 1:
                self.winner = 1
        # вертикали
        if self.board[0][0] == self.board[1][0] == self.board[2][0]:
            if self.board[0][0] == 2 and self.board[1][0] == 2 and \
                    self.board[2][0] == 2:
                self.winner = 2
            elif self.board[0][0] == 1 and self.board[1][0] == 1 and \
                    self.board[2][0] == 1:
                self.winner = 1
        if self.board[0][1] == self.board[1][1] == self.board[2][1]:
            if self.board[0][1] == 2 and self.board[1][1] == 2 and \
                    self.board[2][1] == 2:
                self.winner = 2
            elif self.board[0][1] == 1 and self.board[1][1] == 1 and \
                    self.board[2][1] == 1:
                self.winner = 1
        if self.board[0][2] == self.board[1][2] == self.board[2][2]:
            if self.board[0][2] == 2 and self.board[1][2] == 2 and \
                    self.board[2][2] == 2:
                self.winner = 2
            elif self.board[0][2] == 1 and self.board[1][2] == 1 and \
                    self.board[2][2] == 1:
                self.winner = 1
        # ничья
        check = False
        row = 0
        for i in self.board:
            if 0 not in i:
                row += 1
                if row == 3:
                    check = True
        if check:
            self.winner = 3
        self.win_draw()

    def win_draw(self):
        # вывод сообщения о выигрыше/проигрыше
        if self.winner == 2:
            self.timer += 1
            draw_text('вы выиграли :)', 60, 710, pg.font.SysFont('Comic Sans', 60))
            if self.timer == 100:
                self.count += 1
                self.reset()
        elif self.winner == 1:
            self.timer += 1
            draw_text('вы проиграли :(', 60, 710, pg.font.SysFont('Comic Sans', 60))
            if self.timer == 100:
                self.reset()
        elif self.winner == 3:
            self.timer += 1
            draw_text('ничья!', 60, 710, pg.font.SysFont('Comic Sans', 60))
            if self.timer == 100:
                self.reset()
        else:
            draw_text('', 60, 710, pg.font.SysFont('Comic Sans', 60))

    def render(self):
        # прорисовка
        if not self.end:
            for i in range(self.row):
                for j in range(self.col):
                    if self.board[i][j] == 2:
                        screen.blit(self.o_pic,
                                    (j * self.cell_size + self.left, i *
                                     self.cell_size + self.top, 100, 100))
                    elif self.board[i][j] == 1:
                        screen.blit(self.x_pic,
                                    (j * self.cell_size + self.left, i *
                                     self.cell_size + self.top, 100, 100))
                    pg.draw.rect(screen,
                                 pg.Color('white'),
                                 (j * self.cell_size + self.left,
                                  i * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)
        self.win_check()

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]
        i = (y - self.top) // self.cell_size
        j = (x - self.left) // self.cell_size
        if i < 0 or i >= self.row or j < 0 or j >= self.col:
            return None
        return i, j

    def on_click(self, cell):
        choise = 0
        # распаковка координат, смена цвета ячейки, ход противника
        i, j = cell
        flag = True
        while flag:
            # выбор случайной клетки для противника
            choise = [random.randint(0, 2), random.randint(0, 2)]
            if self.board[choise[0]][choise[1]] == 0:
                flag = False
        if self.status == 2:
            if self.board[i, j] == 0:
                self.board[i, j] = 2
                self.status = 1
        elif self.status == 1:
            self.board[choise[0], choise[1]] = 1
            self.status = 2

    def get_click(self, mouse_pos):
        # получение координат нажатой клетки
        cell_coords = self.get_cell(mouse_pos)
        if cell_coords:
            self.on_click(cell_coords)
            for i in self.board:
                for x in i:
                    if x == 0:
                        self.on_click(cell_coords)
                        break


def terminate():
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Пазл')
    size = width, height = 1200, 800
    screen = pg.display.set_mode(size)
    board = Board_puzzle(3, 5)
    pg.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()
    try:
        pg.mixer.music.load('data/story.mp3')
    except:
        pg.mixer.music.load('data/story.wav')
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(-1, 0.0, 5000)
    return_screen('start-screen.png')

    # включаем музыку
    try:
        pg.mixer.music.load('data/sea.mp3')
    except:
        pg.mixer.music.load('data/sea.wav')
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(-1, 0.0, 5000)

    return_screen('1pic.png')

    coords_fish = []
    for _ in range(10):
        coords_fish.append([random.randint(100, 1150), random.
                           randint(100, 750), -1, -1, random.randint(1, 6)])
    v = 200
    clock = pg.time.Clock()

    pg.key.set_repeat(100, 70)
    fps = 60
    data_now = datetime.today()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        sec = datetime.today() - data_now
        time = int(str(sec.seconds))
        win = True
        for i in range(3):
            for j in range(5):
                if board.map[i][j] != 0:
                    win = False
        if win:
            pass_surf = load_image('end_puzzle.png')
            pass_rect = pass_surf.get_rect()
            screen.blit(pass_surf, pass_rect)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()
                elif event.type == pg.KEYDOWN or \
                        event.type == pg.MOUSEBUTTONDOWN:
                    running = False
                    labirint_run()
        elif time >= 90:
            pass_surf = load_image('pass_puzzle.png')
            pass_rect = pass_surf.get_rect()
            screen.blit(pass_surf, pass_rect)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()
                elif event.type == pg.KEYDOWN or \
                        event.type == pg.MOUSEBUTTONDOWN:
                    board = Board_puzzle(3, 5)
                    data_now = datetime.today()
        else:
            screen.fill(pg.Color('black'))
            fon_surf = load_image('main.png')
            fon_rect = fon_surf.get_rect()
            screen.blit(fon_surf, fon_rect)
            paint_fish()
            board.draw_picture()
            draw_text(f'Прошло времени  {str(time // 60)} : '
                      f'{str(time % 60)} из 1 : 30', 750, 40)
        pg.display.flip()
        pg.time.Clock().tick(fps)
    terminate()
