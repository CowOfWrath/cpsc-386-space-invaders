# Ryan Chen
# 893219394
# Implementation of the Alien class

import pygame
import random as random
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, settings, screen, width, height, type):
        super(Alien, self).__init__()
        self.settings = settings
        self.screen = screen

        self.image = pygame.transform.scale(pygame.image.load("Images/black.png"), (width, height))
        self.images = []
        self.type = type
        if type == 0:
            self.images.append(pygame.transform.scale(pygame.image.load("Images/alien31.png"), (width, height)))
            self.images.append(pygame.transform.scale(pygame.image.load("Images/alien30.png"), (width, height)))
        elif type == 1:
            self.images.append(pygame.transform.scale(pygame.image.load("Images/alien30.png"), (width, height)))
            self.images.append(pygame.transform.scale(pygame.image.load("Images/alien31.png"), (width, height)))
        elif type == 2:
            self.images.append(pygame.transform.scale(pygame.image.load("Images/alien20.png"), (width, height)))
            self.images.append(pygame.transform.scale(pygame.image.load("Images/alien21.png"), (width, height)))
        elif type == 3:
            self.images.append(pygame.transform.scale(pygame.image.load("Images/alien21.png"), (width, height)))
            self.images.append(pygame.transform.scale(pygame.image.load("Images/alien20.png"), (width, height)))
        elif type == 4:
            self.images.append(pygame.transform.scale(pygame.image.load("Images/alien10.png"), (width, height)))
            self.images.append(pygame.transform.scale(pygame.image.load("Images/alien11.png"), (width, height)))
        elif type == 5:
            self.images.append(pygame.transform.scale(pygame.image.load("Images/alien11.png"), (width, height)))
            self.images.append(pygame.transform.scale(pygame.image.load("Images/alien10.png"), (width, height)))
        else:
            if type % 2 == 0:
                self.images.append(pygame.transform.scale(pygame.image.load("Images/alien10.png"), (width, height)))
                self.images.append(pygame.transform.scale(pygame.image.load("Images/alien11.png"), (width, height)))
            else:
                self.images.append(pygame.transform.scale(pygame.image.load("Images/alien11.png"), (width, height)))
                self.images.append(pygame.transform.scale(pygame.image.load("Images/alien10.png"), (width, height)))

        self.shoot = False

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # not sure if i want this
        self.x = float(self.rect.x)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.shoot = False
        self.rect.x += self.settings.alien_speed * self.settings.fleet_direction
        time = pygame.time.get_ticks() - self.settings.alien_tick

        # Animation
        if time > 1000:
            self.settings.alien_index += 1
            self.settings.alien_tick = pygame.time.get_ticks()
        if self.settings.alien_index >= len(self.images):
            self.settings.alien_index = 0
        self.image = self.images[self.settings.alien_index]

        # shoot
        if time > 995:
            if random.randint(1, 100) >= 95:
                self.shoot = True;

    def check_edges(self):
        if self.rect.right >= self.screen.get_rect().right:
            return True
        elif self.rect.left <= 0:
            return True
