# Ryan Chen
# 893219394
# Implementation of the ship class

import pygame
from pygame.sprite import Sprite


class Alien_Explosion(Sprite):
    def __init__(self, screen, width, height, center):
        super(Alien_Explosion, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("Images/black.png"), (width, height))
        self.images = []
        self.images.append(pygame.transform.scale(pygame.image.load("Images/explode0.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/explode1.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/explode2.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/explode3.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/black.png"), (width, height)))

        self.last_tick = 0
        self.index = 0
        self.done = False

        self.rect = self.image.get_rect()
        self.rect.center = center

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        time = pygame.time.get_ticks() - self.last_tick

        if time > 250:
            self.last_tick = pygame.time.get_ticks()
            self.image = self.images[self.index]
            self.index += 1
            if self.index >= len(self.images):
                self.done = True
                self.index = 0
