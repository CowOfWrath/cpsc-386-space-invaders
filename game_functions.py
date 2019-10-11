# Ryan Chen
# 893219394
# Implementation of various game functions used in checking and updating the state of the game

import sys
import pygame
import random
from time import sleep
from bullet import Bullet
from alien import Alien
from alien_bullet import Alien_Bullet
from alien_explosion import Alien_Explosion


def create_alien(settings, screen, aliens, alien_num, row, type):
    alien = Alien(settings, screen, settings.alien_width, settings.alien_height, type)
    alien.rect.x = settings.alien_width + 2 * settings.alien_width * alien_num
    alien.rect.y = settings.alien_height + 2 * settings.alien_height * row
    # still not sure if i want to use this  alien.rect.x = alien.x
    aliens.add(alien)


def create_fleet(settings, screen, aliens):
    space_x = settings.screen_width - 2 * (settings.alien_width)
    num_aliens_x = int(space_x / (2 * (settings.alien_width)))

    space_y = settings.screen_height - 3 * settings.alien_height - settings.ship_height
    num_rows = int(space_y / (2 * settings.alien_height))

    for row in range(num_rows):
        for alien_num in range(num_aliens_x):
            create_alien(settings, screen, aliens, alien_num, row, (row * 2) + ((row + alien_num) % 2))


def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullet_max:
        pygame.mixer.Sound("Sounds/laser4.wav").play()
        b = Bullet(settings, screen, ship)
        bullets.add(b)


def check_keydown(settings, stats, event, screen, ship, bullets):
    if event.key == pygame.K_ESCAPE:
        stats.running = False

    # Ship movement events
    elif event.key == pygame.K_RIGHT:
        settings.ship_move_right = True
        settings.ship_move_left = False
    elif event.key == pygame.K_LEFT:
        settings.ship_move_left = True
        settings.ship_move_right = False
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)


def check_keyup(settings, event):
    if event.key == pygame.K_RIGHT:
        settings.ship_move_right = False
    elif event.key == pygame.K_LEFT:
        settings.ship_move_left = False


def check_play_button(settings, screen, stats, sb, play_button, mouse_x, mouse_y, ship, aliens, bullets):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.active:
        pygame.mouse.set_visible(False)
        settings.init_dynamic_settings()
        stats.reset_stats()
        stats.active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()
        create_fleet(settings, screen, aliens)
        ship.center_ship()


def check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # Check key and mouse events
    for event in pygame.event.get():
        # Quit game events
        if event.type == pygame.QUIT:
            stats.running = False
        elif event.type == pygame.KEYDOWN:
            check_keydown(settings, stats, event, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup(settings, event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, sb, play_button, mouse_x, mouse_y, ship, aliens, bullets)


def change_fleet_direction(settings, aliens):
    for a in aliens.sprites():
        a.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1
    aliens.update()


def check_fleet_edges(settings, aliens):
    for a in aliens.sprites():
        if a.check_edges():
            change_fleet_direction(settings, aliens)


def check_bullet_alien_collisions(settings, screen, stats, sb, aliens, bullets, ufos, alien_explosions):
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)
    if collisions:
        for a in collisions:
            pygame.mixer.Sound("Sounds/retro_video_game_sfx_explode.wav").play()
            ae = Alien_Explosion(screen, settings.alien_width, settings.alien_height, a.rect.center)
            alien_explosions.add(ae)
            if a.type == 0 or a.type == 1:
                stats.score += settings.alien_points_type01
            elif a.type == 2 or a.type == 3:
                stats.score += settings.alien_points_type23
            else:
                stats.score += settings.alien_points_type45
    collisions = pygame.sprite.groupcollide(ufos, bullets, True, True)
    for a in collisions:
        pygame.mixer.Sound("retro_video_game_sfx_explode.wav").play()
        stats.score += random.randint(200, 1000)
        ae = Alien_Explosion(screen, settings.alien_width, settings.alien_height, a.rect.center)
        alien_explosions.add(ae)
    sb.prep_score()
    check_high_score(stats, sb)
    if len(aliens) == 0:
        settings.speedup()
        stats.level += 1
        sb.prep_level()
        bullets.empty()
        create_fleet(settings, screen, aliens)


def ship_explode(ship):
    pygame.mixer.Sound("Sounds/retro_video_game_sfx_explode.wav").play()
    ship.explode = True
    ship.hit = True


def ship_hit(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
    if stats.ship_lives > 0:
        stats.ship_lives -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()
        ship.center_ship()
        ship.image = ship.default_image
        create_fleet(settings, screen, aliens)
        ship.explode = False
        ship.hit = False
    else:
        stats.active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(settings, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for a in aliens.sprites():
        if a.rect.bottom >= screen_rect.bottom:
            ship_explode(ship)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_aliens(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, ufos, alien_explosions):
    check_fleet_edges(settings, aliens)
    aliens.update()
    alien_explosions.update()
    check_aliens_bottom(settings, screen, stats, sb, ship, aliens, bullets)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_explode(ship)

    for e in alien_explosions:
        if e.done:
            e.kill()

    for u in ufos:
        u.update()
        if u.check_edges():
            u.kill()

    for a in aliens:
        if a.shoot == True:
            pygame.mixer.Sound("Sounds/laser4.wav").play()
            b = Alien_Bullet(settings, screen, a)
            alien_bullets.add(b)


def check_bullet_ship_collisions(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
    for b in alien_bullets:
        if pygame.sprite.collide_rect(ship, b):
            ship_explode(ship)
            sb.prep_score()
            check_high_score(stats, sb)


def update_bullets(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, ufos, alien_explosions):
    bullets.update()
    alien_bullets.update()

    # Manage objects
    for b in bullets:
        if b.rect.bottom <= 0:
            bullets.remove(b)
    for b in alien_bullets:
        if b.rect.bottom <= 0:
            alien_bullets.remove(b)
    check_bullet_alien_collisions(settings, screen, stats, sb, aliens, bullets, ufos, alien_explosions)
    check_bullet_ship_collisions(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)


def update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button, alien_bullets, ufos,
                  alien_explosions):
    # update images on screen and display screen
    screen.fill(settings.bg_color)
    ship.draw()
    aliens.draw(screen)
    ufos.draw(screen)
    alien_explosions.draw(screen)

    for bullet in bullets.sprites():
        bullet.draw()

    for bullet in alien_bullets.sprites():
        bullet.draw()

    sb.draw()

    if not stats.active:
        play_button.draw()

    # Update Screen
    pygame.display.flip()
