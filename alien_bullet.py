# Ryan Chen
# 893219394
# Implementation of the bullet

import pygame
from pygame.sprite import Sprite


class Alien_Bullet(Sprite):
    def __init__(self, settings, screen, alien):
        super(Alien_Bullet, self).__init__()
        self.settings = settings
        self.screen = screen

        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        self.color = settings.bullet_color

    def update(self):
        self.rect.top += 1 * self.settings.bullet_speed

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
