# Ryan Chen
# 893219394
# Implementation of the Alien class

import pygame
from pygame.sprite import Sprite

class Bunker(Sprite):
    def __init__(self, settings, screen, width, height):
        super(Bunker, self).__init__()
        self.settings = settings
        self.screen = screen

        self.image = pygame.transform.scale(pygame.image.load("Images/white.png"), (width, height))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height