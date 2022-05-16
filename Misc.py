import pygame
from math import *


powerups = ["Misc/pu.png", "Misc/1up.png"]


class PowerUp:
    def __init__(self, pos, variation):
        self.pos = pos
        self.var = variation
        self.y_vel = -0.5
        self.x_cord = pos[0]
        self.y_cord = pos[1]
        self.image = pygame.image.load(powerups[variation]).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def update(self, player):
        dir = (-self.rect.centerx + player.rect.centerx, self.rect.centery - player.rect.centery)
        abs_dir = sqrt(dir[0] * dir[0] + dir[1] * dir[1])
        norm = (dir[0] / (abs_dir + 0.00001),
                dir[1] / (abs_dir + 0.00001))
        if abs_dir < (70 if player.slow else 40):
            self.x_cord += norm[0] * 5.0
            self.y_cord -= norm[1] * 10.0
        self.y_cord += self.y_vel
        self.rect.centerx = self.x_cord
        self.rect.centery = self.y_cord
        self.y_vel += 0.02

    def draw(self, viewport: pygame.Surface):
        viewport.blit(self.image, self.rect)
