import pygame as pg
from pygame.sprite import Sprite


class Alien(Sprite):
    """Пришелец"""

    def __init__(self, screen, settings):
        """Инициализирует пришельца и задает его начальную позицию."""

        super().__init__()
        self.screen = screen
        self.settings = settings

        # Загрузка изображения пришельца и назначение атрибута rect
        self.image = pg.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной позиции пришельца
        self.x = float(self.rect.x)

    def blit(self):
        """Выводит пришельца в текущем положении"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Перемещает пришельца влево или вправо"""

        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        else:
            return False
