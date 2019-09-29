import pygame as pg
from pygame.sprite import Group

from ship import Ship
from settings import Settings
import game_functions as gf
from game_stats import GameStats
from button import Button


def run_game():
    pg.init()
    settings = Settings()
    stats = GameStats(settings)

    screen = pg.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pg.display.set_caption('Alien Invasion')
    play_button = Button(settings, screen, 'Play')

    ship = Ship(screen, settings)
    aliens = Group()
    bullets = Group()

    gf.create_fleet(settings, screen, aliens, ship)

    while True:
        gf.check_events(settings, screen, stats, play_button,  ship, bullets,
                        aliens)

        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, screen, ship, bullets, aliens)
            gf.update_aliens(aliens, ship, bullets, screen, stats, settings)

        gf.update_screen(settings, screen, stats, ship, aliens, bullets,
                         play_button)


run_game()
