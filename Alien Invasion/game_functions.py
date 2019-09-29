import sys
import pygame as pg

from alien import Alien
from bullet import Bullet
from time import sleep


def check_events(settings, screen, stats, play_button, ship, bullets, aliens):
    """Прослушивание событий"""

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()  # Если использовать pg.quit(),
            # то будет грязный вывод в консоль, а так - нет

        elif event.type == pg.KEYDOWN:
            check_keydown_events(event, settings, stats, aliens,
                                 screen, ship, bullets)

        elif event.type == pg.KEYUP:
            check_keyup_events(event, ship)

        # elif event.type == pg.MOUSEBUTTONDOWN:
            # mouse_x, mouse_y = pg.mouse.get_pos()
            # check_play_button(stats, screen, settings, play_button, ship,
            #                   mouse_x, mouse_y, bullets, aliens)


def check_keydown_events(event, settings, stats, aliens, screen, ship, bullets):
    if event.key == pg.K_RIGHT:
        ship.moving_right = True

    if event.key == pg.K_LEFT:
        ship.moving_left = True

    if event.key == pg.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)

    if event.key == pg.K_q:
        sys.exit()

    if event.key == pg.K_p:
        check_play_button(stats, screen, settings, None, ship, None, None,
                          bullets, aliens)


def check_keyup_events(event, ship):
    if event.key == pg.K_RIGHT:
        ship.moving_right = False

    if event.key == pg.K_LEFT:
        ship.moving_left = False


def start_game(stats, settings, screen, bullets, aliens, ship):
    stats.reset_stats()
    bullets.empty()
    aliens.empty()

    create_fleet(settings, screen, aliens, ship)
    ship.center_ship()


def check_play_button(stats, screen, settings,  play_button, ship,  mouse_x,
                      mouse_y, bullets, aliens):
    """Запускает новую игру при нажатии кнопки Play."""
    # button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if not stats.game_active:
        pg.mouse.set_visible(False)
        stats.game_active = True

        start_game(stats, settings, screen, bullets, aliens, ship)


def update_screen(settings, screen, stats, ship, aliens, bullets, play_button):
    """Обновление изображений на экране и его новое отображение"""
    screen.fill(settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blit()
    aliens.draw(screen)

    # if not stats.game_active:
    #     play_button.draw_button()

    pg.display.flip()  # Отображение последнего прорисованного экрана,
    # обновление экрана


def update_bullets(settings, screen, ship, bullets, aliens):
    """Обновляет позиции пуль и уничтожает старые пули."""

    # Обновление позиций пуль
    bullets.update()

    # Удаление пуль, вышедших за край экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(settings, screen, ship, bullets, aliens)


def check_bullet_alien_collisions(settings, screen, ship, bullets, aliens):
    # Проверка попаданий в пришельцев.
    # При обнаружении попадания удалить пулю и пришельца.
    collisions = pg.sprite.groupcollide(bullets, aliens, True, True)

    # После уничтожения всего флота создать новый и обновить магазин пуль
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(settings, screen, aliens, ship)


def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullets_allowed:
        # Создание новой пули и включение ее в группу bullets
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(settings, screen, aliens, ship):
    """Создает флот пришельцев"""

    alien = Alien(screen, settings)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    ship_height = ship.rect.height

    aliens_number = get_number_aliens(settings, alien_width)
    number_rows = get_number_rows(settings, ship_height, alien_height)

    # Создание первого ряда пришельцев
    for row_number in range(number_rows):
        for alien_number in range(aliens_number):
            alien = create_alien(settings, screen, alien_number, row_number)
            aliens.add(alien)


def create_alien(settings, screen, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""

    alien = Alien(screen, settings)
    alien_width = alien.rect.width
    alien_height = alien.rect.height

    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien_height + 2 * alien_height * row_number
    alien.rect.x = alien.x

    return alien


def get_number_aliens(settings, alien_width):
    """Вычисляет количество пришельцев в ряду."""
    # Создание пришельца и вычисление количества пришельцев в ряду.
    # Интервал между соседними пришельцами равен одной ширине пришельца.

    alien_available_space_x = settings.screen_width - 2 * alien_width
    aliens_number = int(alien_available_space_x / (2 * alien_width))
    return aliens_number


def get_number_rows(settings, ship_height, alien_height):
    available_space_y = settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(aliens, ship, bullets, screen, stats, settings):
    """
    Проверяет, достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте.
    """
    check_fleet_edges(aliens, settings)
    aliens.update()

    if pg.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, screen, ship, aliens, bullets)

    check_aliens_bottom(settings, stats, screen, ship, aliens, bullets)


def ship_hit(settings, stats, screen, ship, aliens, bullets):
    """Обрабатывает столкновение корабля с пришельцем"""
    # Уменьшение количества кораблей
    if stats.ship_left > 0:
        stats.ship_left -= 1

        # Очистка списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре
        create_fleet(settings, screen, aliens, ship)
        ship.center_ship()

        # Пауза
        sleep(.5)
    else:
        stats.game_active = False
        pg.mouse.set_visible(True)


def check_aliens_bottom(settings, stats, screen, ship, aliens, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана"""
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, stats, screen, ship, aliens, bullets)
            break


def check_fleet_edges(aliens, settings):
    """Реагирует на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings, aliens):
    """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += settings.drop_speed

    settings.fleet_direction *= -1
