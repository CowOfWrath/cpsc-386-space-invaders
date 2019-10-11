# Ryan Chen
# 893219394
# Implementation of the ship class

import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, screen, width, height):
        # Initialize ship and start position
        super(Ship, self).__init__()
        self.screen = screen

        self.image = pygame.transform.scale(pygame.image.load("Images/ship.png"), (width, height))
        self.default_image = pygame.transform.scale(pygame.image.load("Images/ship.png"), (width, height))
        self.images = []
        self.images.append(pygame.transform.scale(pygame.image.load("Images/se0.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/se1.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/se2.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/se3.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/se4.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/se5.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/se6.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/se7.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/se8.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/se9.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/se10.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/black.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/black.png"), (width, height)))

        self.explode = False
        self.hit = False
        self.index = 0
        self.last_tick = 0

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def center_ship(self):
        self.center = self.screen_rect.centerx

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self, settings):
        time = pygame.time.get_ticks() - self.last_tick

        # Animation

        if not self.explode:
            if settings.ship_move_right and self.rect.right < settings.screen_width:
                self.rect.centerx += 1 * settings.ship_speed
            elif settings.ship_move_left and self.rect.left > 0:
                self.rect.centerx -= 1 * settings.ship_speed
        else:
            if time > 100:
                self.last_tick = pygame.time.get_ticks()
                self.image = self.images[self.index]
                self.index += 1
                if self.index >= len(self.images):
                    self.explode = False
                    self.index = 0



