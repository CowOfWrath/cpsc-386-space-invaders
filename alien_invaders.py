# Ryan Chen
# 893219394
# Implementation of the initialization and game loop

import pygame
import sys
import time
import random
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from ship import Ship
from alien import Alien
from ufo import UFO
from alien_explosion import Alien_Explosion
import game_functions as gf


def run():
    # Initialization
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
    pygame.mixer.music.load("Sounds/ominous_ambience.wav")
    pygame.mixer.music.play(-1)
    settings = Settings()
    stats = GameStats(settings)
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(settings, screen, "Play")
    bg_color = settings.bg_color

    sb = Scoreboard(settings, screen, stats)

    ship = Ship(screen, settings.ship_width, settings.ship_height)
    bullets = Group()
    alien_bullets = Group()
    ufos = Group()
    aliens = Group()
    alien_explosions = Group()

    gf.create_fleet(settings, screen, aliens)

    clock = pygame.time.Clock()

    # Game loop
    running = True
    while stats.running:
        clock.tick(60)
        gf.check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.active:
            ship.update(settings)
            if not ship.explode:
                if ship.hit:
                    gf.ship_hit(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
                    ship.hit = False
                    ship.explode = False
                else:
                    if random.randint(1,1000) == 1000 and len(ufos.sprites()) == 0:
                        ufo = UFO(settings, screen, settings.alien_width, settings.alien_height)
                        ufos.add(ufo)
                        pygame.mixer.Sound("Sounds/cartoon_flying_ufo.wav").play()
                    gf.update_bullets(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, ufos, alien_explosions)
                    gf.update_aliens(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, ufos, alien_explosions)




        # Draw objects
        gf.update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button, alien_bullets, ufos, alien_explosions)

    sys.exit()


run()
