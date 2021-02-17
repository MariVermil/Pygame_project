import os
import pygame as pg
from pygame import time


def load_image(name):
    filename = os.path.join('data', name)
    try:
        image = pg.image.load(filename)
    except pg.error as error:
        print('Не могу загрузить изображение:', name)
        raise SystemExit(error)
    return image


class AnimaSprite(pg.sprite.Sprite):
    def __init__(self, sheet, cols, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, cols, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, cols, rows):
        self.rect = pg.Rect(0, 0, sheet.get_width() // cols, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(cols):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pg.Rect(frame_location, self.rect.size)))
                print(self.frames)

    def update(self):
        """Смена кадра спрайта"""
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Анимация спрайта')
    size = width, height = 200, 200
    screen = pg.display.set_mode(size)
    all_sprites = pg.sprite.Group()
    sheet_dragon = load_image('enemy_move.png')
    cols, rows = (2, 1)
    x, y = (0, 0)
    sprite_ = AnimaSprite(sheet_dragon, 2, 1, 0, 0)
    fps = 5
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill(pg.Color('white'))
        all_sprites.draw(screen)
        all_sprites.update()
        pg.display.flip()
        time.Clock().tick(fps)
    pg.quit()
