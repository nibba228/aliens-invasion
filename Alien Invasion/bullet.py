import pygame as pg
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Класс для управления пулями, выпущенными кораблем"""

    def __init__(self, settings, screen, ship):
        """Создает пули в текущей позиции корабля"""
        super().__init__()

        self.screen = screen

        self.rect = pg.Rect(0, 0,
                            settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Позиция пули хранится в вещественном формате
        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        """Перемещает пулю вверх по экрану"""

        # Обновление позиции пули в вещественном формате
        self.y -= self.speed_factor
        # Обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        """Вывод пули на экран"""
        pg.draw.rect(self.screen, self.color, self.rect)
