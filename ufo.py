# Ryan Chen
# 893219394
# Implementation of the UFO class

import pygame
from pygame.sprite import Sprite


class UFO(Sprite):
    def __init__(self, settings, screen, width, height):
        super(UFO, self).__init__()
        self.settings = settings
        self.screen = screen

        self.image = pygame.transform.scale(pygame.image.load("Images/ufo0.png"), (width, height))
        self.images = []
        self.images.append(pygame.transform.scale(pygame.image.load("Images/ufo0.png"), (width, height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/ufo1.png"), (width, height)))

        self.last_tick = 0
        self.index = 0

        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        time = pygame.time.get_ticks() - self.last_tick

        if time > 500:
            self.index += 1
            self.last_tick = 0
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]

        self.rect.x += 10

    def check_edges(self):
        if self.rect.left >= self.screen.get_rect().right:
            return True
