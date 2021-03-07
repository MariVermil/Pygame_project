import pygame as pg
import numpy as np
import os
from random import randint


def load_image(name):
    filename = os.path.join('data', name)
    try:
        image = pg.image.load(filename)
    except pg.error as error:
        raise SystemExit(error)
    return image


def draw_text(text, font, x, y):
    img = font.render(text, True, (230, 248, 245))
    screen.blit(img, (x, y))


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
            if self.board[0][0] == 2 and self.board[1][1] == 2 and self.board[2][2] == 2:
                self.winner = 2
            elif self.board[0][0] == 1 and self.board[1][1] == 1 and self.board[2][2] == 2:
                self.winner = 1
        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == 2 and self.board[1][1] == 2 and self.board[2][0] == 2:
                self.winner = 2
            elif self.board[0][2] == 1 and self.board[1][1] == 1 and self.board[2][0] == 1:
                self.winner = 1
        # горизонтали
        if self.board[0][0] == self.board[0][1] == self.board[0][2]:
            if self.board[0][0] == 2 and self.board[0][1] == 2 and self.board[0][2] == 2:
                self.winner = 2
            elif self.board[0][0] == 1 and self.board[0][1] == 1 and self.board[0][2] == 1:
                self.winner = 1
        if self.board[1][0] == self.board[1][1] == self.board[1][2]:
            if self.board[1][0] == 2 and self.board[1][1] == 2 and self.board[1][2] == 2:
                self.winner = 2
            elif self.board[1][0] == 1 and self.board[1][1] == 1 and self.board[1][2] == 1:
                self.winner = 1
        if self.board[2][0] == self.board[2][1] == self.board[2][2]:
            if self.board[2][0] == 2 and self.board[2][1] == 2 and self.board[2][2] == 2:
                self.winner = 2
            elif self.board[2][0] == 1 and self.board[2][1] == 1 and self.board[2][2] == 1:
                self.winner = 1
        # вертикали
        if self.board[0][0] == self.board[1][0] == self.board[2][0]:
            if self.board[0][0] == 2 and self.board[1][0] == 2 and self.board[2][0] == 2:
                self.winner = 2
            elif self.board[0][0] == 1 and self.board[1][0] == 1 and self.board[2][0] == 1:
                self.winner = 1
        if self.board[0][1] == self.board[1][1] == self.board[2][1]:
            if self.board[0][1] == 2 and self.board[1][1] == 2 and self.board[2][1] == 2:
                self.winner = 2
            elif self.board[0][1] == 1 and self.board[1][1] == 1 and self.board[2][1] == 1:
                self.winner = 1
        if self.board[0][2] == self.board[1][2] == self.board[2][2]:
            if self.board[0][2] == 2 and self.board[1][2] == 2 and self.board[2][2] == 2:
                self.winner = 2
            elif self.board[0][2] == 1 and self.board[1][2] == 1 and self.board[2][2] == 1:
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
            draw_text('вы выиграли :)', pg.font.SysFont('Comic Sans', 60), 60, 710)
            if self.timer == 100:
                self.count += 1
                self.reset()
        elif self.winner == 1:
            self.timer += 1
            draw_text('вы проиграли :(', pg.font.SysFont('Comic Sans', 60), 60, 710)
            if self.timer == 100:
                self.reset()
        elif self.winner == 3:
            self.timer += 1
            draw_text('ничья!', pg.font.SysFont('Comic Sans', 60), 60, 710)
            if self.timer == 100:
                self.reset()
        else:
            draw_text('', pg.font.SysFont('Comic Sans', 60), 60, 710)

    def render(self):
        # прорисовка
        if not self.end:
            for i in range(self.row):
                for j in range(self.col):
                    if self.board[i][j] == 2:
                        screen.blit(self.o_pic, (j * self.cell_size + self.left, i * self.cell_size + self.top, 100, 100))
                    elif self.board[i][j] == 1:
                        screen.blit(self.x_pic, (j * self.cell_size + self.left, i * self.cell_size + self.top, 100, 100))
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
            choise = [randint(0, 2), randint(0, 2)]
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


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Roota`s Adventure')
    pic = load_image('board.png')
    size = width, height = 1200, 800
    screen = pg.display.set_mode(size)
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
        draw_text(f'{board.count}/3', pg.font.SysFont('Comic Sans', 100), 1000, 100)
        if board.count == 3:
            running = False
        board.render()
        pg.display.flip()
    pg.quit()
