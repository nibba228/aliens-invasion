import pygame as pg


class Ship:

    def __init__(self, screen, settings):
        """Инициализирует корабль и задает его начальную позицию"""
        self.moving_right = False
        self.moving_left = False

        self.settings = settings
        self.screen = screen

        # Загрузка изображения корабля и получение прямоугольника
        self.image = pg.image.load('images/ship.bmp')

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Каждый новый корабль появляется у нижнего края экрана; выравнивание
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

    def update(self):
        """Управляет движением корабля"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.ship_speed_factor

        self.rect.centerx = self.center

    def blit(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль в центре нижней стороны"""
        self.center = self.screen_rect.centerx
