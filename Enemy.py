import random

import pygame
from math import *


# patterns
def random_bullets(enemy, player_cords, bullets):
    if enemy.counter % enemy.a_speed == 0:
        enemy.shot_s.play()
        if enemy.a_speed < 0:
            enemy.attack = False
        for i in range(random.randint(2, 5)):
            bullets.append(EBullet(enemy.b_type, random.randint(1, 361), random.randint(1, 4),
                                   (random.randint(-10, 11) + enemy.rect.centerx,
                                    random.randint(-10, 11) + enemy.rect.centery)))


def circular_array(enemy, player_cords, bullets):
    if enemy.counter % enemy.a_speed == 0:
        enemy.shot_s.play()
        if enemy.a_speed < 0:
            enemy.attack = False
        slices = enemy.b_count
        step = 360 // slices
        for i in range(slices):
            for j in range(1, 6):
                bullets.append(EBullet(enemy.b_type, -step * i, j,
                                       (5 * cos(radians(step * i)) + enemy.rect.centerx,
                                        5 * sin(radians(step * i)) + enemy.rect.centery)))


def circular_wshift(enemy, player_cords, bullets):
    if enemy.counter % enemy.a_speed == 0:
        enemy.shot_s.play()
        if enemy.a_speed < 0:
            enemy.attack = False
        slices = enemy.b_count
        step = 360 / slices
        for i in range(slices):
            bullets.append(EBullet(enemy.b_type, -step * i + enemy.shift, 2,
                                   (50 * cos(radians(step * i + enemy.shift)) + enemy.rect.centerx,
                                    50 * sin(radians(step * i + enemy.shift)) + enemy.rect.centery)))
        enemy.shift += 5
        enemy.shift %= 360


def circular(enemy, player_cords, bullets):
    if enemy.counter % enemy.a_speed == 0:
        enemy.shot_s.play()
        if enemy.a_speed < 0:
            enemy.attack = False
        slices = enemy.b_count
        step = 360 // slices
        for i in range(slices):
            bullets.append(EBullet(enemy.b_type, -step * i, 3,
                                   (5 * cos(radians(step * i)) + enemy.rect.centerx,
                                    5 * sin(radians(step * i)) + enemy.rect.centery)))


def to_player(enemy, player_cords, bullets):
    cordx = enemy.rect.centerx - player_cords[0]
    cordy = enemy.rect.centery - player_cords[1]
    angle = degrees(atan2(cordx, cordy)) + 90
    if enemy.counter % enemy.a_speed == 0:
        if enemy.a_speed < 0:
            enemy.attack = False
        enemy.counter = 0
        for i in range(enemy.b_count):
            bullets.append(EBullet(enemy.b_type, angle + enemy.shift * (enemy.b_count // 2 - i), 2,
                                   (enemy.rect.centerx, enemy.rect.centery)))


patterns = [to_player, to_player, circular_wshift, circular, circular_array, random_bullets]
enemiesL = ["Enemies/e1.png", "Enemies/e2.png", "Enemies/e3.png", "Enemies/e4.png", "Enemies/e4.png", "Enemies/e3.png"]
bullet_imgs = ["Bullets/e3b.png", "Bullets/e4b.png", "Bullets/e5b.png", "Bullets/e6b.png", "Bullets/e7b.png"]
expl_imgs = ["Enemies/ex1.png", "Enemies/ex2.png", "Enemies/ex3.png"]


class EBullet:
    def __init__(self, num, angle, speed, pos):
        self.angle = angle
        self.speed = speed
        self.coords = [pos[0], pos[1]]
        self.no_rot_img = pygame.image.load(bullet_imgs[num]).convert_alpha()
        self.dims = (self.no_rot_img.get_rect(center=pos).width, self.no_rot_img.get_rect(center=pos).height)
        self.image = pygame.transform.rotate(self.no_rot_img,
                                             angle - 90)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.coords[0] += self.speed * cos(radians(self.angle))
        self.coords[1] -= self.speed * sin(radians(self.angle))
        self.rect.centerx = self.coords[0]
        self.rect.centery = self.coords[1]

    def draw(self, viewport: pygame.Surface):
        viewport.blit(self.image, self.rect)


class Explosion:
    def __init__(self, pos):
        self.pos = pos
        self.dead = False
        self.counter = 0
        self.image = pygame.image.load("Enemies/expl.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        self.expl_s = pygame.mixer.Sound("SFX/enep00.wav")
        self.expl_s.set_volume(0.05)

    def update(self):
        if not self.dead:
            if self.counter > 60:
                self.dead = True
                self.expl_s.play()
                return
            self.image = pygame.transform.scale(self.image, (
                32 + self.counter, 32 + self.counter))
            self.rect = self.image.get_rect(center=self.pos)
            self.counter += 5

    def draw(self, viewport: pygame.Surface):
        viewport.blit(self.image, self.rect)


# Type (Attack Pattern), Speed, Attack Speed, Bullet Count, Bullet Type, Bullet Displacement, Hp, Movement Pattern,
# Starting Pos, Destination Pos (4 arguments for M. Pat. 1), Time
# Enemy(0, 15, 30, 1, 0, 2, 1, (0, 100), (180, 150, 40, 200), 60)
class Enemy:
    def __init__(self, variation, speed, a_speed, b_count, b_type, shift, hitpoints, movement_pattern, pos, destination):
        self.var = variation
        self.speed = speed
        self.a_speed = a_speed
        self.b_type = b_type
        self.mp = movement_pattern
        self.hp = hitpoints
        self.dest = destination
        self.coords = [pos[0], pos[1]]
        self.start = [pos[0], pos[1]]
        self.b_count = b_count
        self.counter = 0
        self.time = 0.0
        self.shift = shift
        self.attack = True
        self.image = pygame.image.load(enemiesL[variation]).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        self.shot_s = pygame.mixer.Sound("SFX/tan00.wav")
        self.shot_s.set_volume(0.05)

    def update(self):
        self.counter += 1
        if not ((self.dest[0] + 4 >= self.rect.centerx >= self.dest[0] - 4)
                and (self.dest[1] + 4 >= self.rect.centery >= self.dest[1] - 4)):
            if self.mp == 0:
                dir = (-self.rect.centerx + self.dest[0], self.rect.centery - self.dest[1])
                abs_dir = sqrt(dir[0] * dir[0] + dir[1] * dir[1])
                norm = (dir[0] / abs_dir,
                        dir[1] / abs_dir)
                self.coords[0] += self.speed * norm[0]
                self.coords[1] -= self.speed * norm[1]
                self.rect.centerx = self.coords[0]
                self.rect.centery = self.coords[1]

            if self.mp == 1:
                # Bezier curve: (p_0 - 2 p_1 + p_2) t^2 + (-2 p_0 + 2 p_1) t + p_0
                self.time += self.speed * 0.001
                self.rect.centerx = (self.start[0] - 2 * self.dest[2] + self.dest[0]) * pow(self.time, 2) + (
                        -2 * self.start[0] + 2 * self.dest[2]) * self.time + self.start[0]
                self.rect.centery = (self.start[1] - 2 * self.dest[3] + self.dest[1]) * pow(self.time, 2) + (
                        -2 * self.start[1] + 2 * self.dest[3]) * self.time + self.start[1]

    def shoot(self, player_cords, bullets):
        if self.attack:
            patterns[self.var](self, player_cords, bullets)

    def draw(self, viewport: pygame.Surface):
        viewport.blit(self.image, self.rect)
