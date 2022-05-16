import pygame
from math import *

bullet_imgs = ["Bullets/bullet.png", "Bullets/bullet_sup.png"]


class Bullet:
    def __init__(self, pos, variation):
        self.image = pygame.image.load(bullet_imgs[variation]).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.y -= 20

    def draw(self, viewport: pygame.Surface):
        viewport.blit(self.image, self.rect)


class Support:
    def __init__(self, pos, displacement):
        self.image = pygame.image.load("Player/support.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.coords = [pos[0], pos[1]]
        self.counter = displacement
        self.radi = 60

    def update(self, player):
        self.counter %= 628
        if player.slow and self.radi > 20:
            self.radi -= 4
        elif player.slow:
            self.radi = 20
        elif self.radi <= 60:
            self.radi += 4
        self.coords[0] = self.radi * cos(self.counter / 100) + player.rect.centerx
        self.coords[1] = self.radi * sin(self.counter / 100) + player.rect.centery

        self.rect.centerx = self.coords[0]
        self.rect.centery = self.coords[1]

        self.counter += 6

    def shoot(self, bullets):
        bullets.append(Bullet((self.rect.centerx, self.rect.centery - 10), 1))

    def draw(self, viewport: pygame.Surface):
        viewport.blit(self.image, self.rect)


class Player:
    def __init__(self, pos, dims):
        self.stance = {'still': True, 'left': False, 'right': False,
                       'up': False, 'down': False}
        self.dims = dims
        self.slow = False
        self.invis = False
        self.dead = False
        self.blink = False
        self.invis_time = 240.0
        self.power_unit = 0.0
        self.pu_count = 0
        self.slow_img = pygame.image.load("Player/pl_dot.png").convert_alpha()
        self.texs = [pygame.image.load("Player/still.png").convert_alpha(),
                       pygame.image.load("Player/left.png").convert_alpha(),
                       pygame.image.load("Player/right.png").convert_alpha()]
        self.image = self.texs[0]
        self.slow_rect = self.slow_img.get_rect(center=pos)
        self.rect = self.image.get_rect(center=pos)
        self.blink_img = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.blink_img.set_alpha(200)
        self.blink_img_rect = self.blink_img.get_rect(center=pos)

        self.sups = []
        self.sup_displ = 0

        self.startpos = pos

        self.shot_s = pygame.mixer.Sound("SFX/plst00.wav")
        self.shot_s.set_volume(0.05)

    def update(self):
        for sup in self.sups:
            sup.update(self)

        self.pu_count = min(floor(self.power_unit), 4)
        self.power_unit = min(self.power_unit, 4)

        if self.pu_count > len(self.sups):
            self.sups.append(Support((self.rect.centerx, self.rect.centery), 0))
            for i, sup in enumerate(self.sups):
                sup.counter = i / self.pu_count * 628
        elif self.pu_count < len(self.sups):
            self.sups.pop()
            for i, sup in enumerate(self.sups):
                sup.counter = i / self.pu_count * 628

        speed = 2 if self.slow else 5
        if self.dead and not self.startpos[1] + 0.1 > self.rect.centery > self.startpos[1] - 0.1:
            self.rect.centery -= 2
            for stance in self.stance:
                self.stance[stance] = False
            self.stance['still'] = True
        else:
            self.dead = False

        if self.stance['still']:
            self.image = self.texs[0]

        if self.stance['up']:
            if self.rect.centery > 0:
                self.rect.centery -= speed
            self.image = self.texs[0]

        if self.stance['down']:
            if self.rect.centery < self.dims[1]:
                self.rect.centery += speed
            self.image = self.texs[0]

        if self.stance['left']:
            if self.rect.centerx > 0:
                self.rect.centerx -= speed
            self.image = self.texs[1]

        if self.stance['right']:
            if self.rect.centerx < self.dims[0]:
                self.rect.centerx += speed
            self.image = self.texs[2]

        if self.invis and self.invis_time > 0.0:
            self.invis_time -= 1
            self.blink = not self.blink
        else:
            self.invis_time = 240.0
            self.invis = False

    def shoot(self, bullets):
        self.shot_s.play()
        bullets.append(Bullet((self.rect.centerx + 10, self.rect.centery - 5), 0))
        bullets.append(Bullet((self.rect.centerx - 10, self.rect.centery - 5), 0))
        for sup in self.sups:
            sup.shoot(bullets)

    def draw(self, viewport: pygame.Surface):
        viewport.blit(self.image, self.rect)
        for sup in self.sups:
            sup.draw(viewport)
        if self.blink:
            self.blink_img.fill((255, 255, 255))
            self.blink_img_rect.centerx = self.rect.centerx
            self.blink_img_rect.centery = self.rect.centery
            viewport.blit(self.blink_img, self.blink_img_rect)

        if self.slow:
            self.slow_rect.centerx = self.rect.centerx
            self.slow_rect.centery = self.rect.centery
            viewport.blit(self.slow_img, self.slow_rect)
