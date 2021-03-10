import os
import sys
import pygame as pg
import random
from pygame import mixer
from datetime import datetime


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


class Board:
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
            self.map[status[0]][status[1]] = (self.map[status[0]][status[1]] + 1) % 4

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


def terminate():
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Пазл')
    size = width, height = 1200, 800
    screen = pg.display.set_mode(size)
    board = Board(3, 5)

    # включаем музыку
    pg.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()
    try:
        pg.mixer.music.load('data/sea.mp3')
    except:
        pg.mixer.music.load('data/sea.wav')
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(-1, 0.0, 5000)

    coords_fish = []
    for _ in range(10):
        coords_fish.append([random.randint(100, 1150), random.randint(100, 750), -1, -1, random.randint(1, 6)])
    v = 200
    clock = pg.time.Clock()

    pg.key.set_repeat(200, 70)
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
                    terminate()
        elif time >= 90:
            pass_surf = load_image('pass_puzzle.png')
            pass_rect = pass_surf.get_rect()
            screen.blit(pass_surf, pass_rect)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()
                elif event.type == pg.KEYDOWN or \
                        event.type == pg.MOUSEBUTTONDOWN:
                    board = Board(3, 5)
                    data_now = datetime.today()
        else:
            screen.fill(pg.Color('black'))
            fon_surf = load_image('main.png')
            fon_rect = fon_surf.get_rect()
            screen.blit(fon_surf, fon_rect)
            paint_fish()
            board.draw_picture()
            draw_text(f'Прошло времени  {str(time // 60)} : {str(time % 60)} из 1 : 30', 750, 40)

        pg.display.flip()
        pg.time.Clock().tick(fps)
    terminate()