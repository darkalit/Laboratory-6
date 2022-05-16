import pygame
import random
from math import *


def reflect(bullet):
    if not bullet.ref_count == 0:
        if bullet.coords[0] <= 0 or bullet.coords[0] >= 400:
            bullet.angle = -(bullet.angle % 180)
            bullet.ref_count -= 1
        if bullet.coords[1] <= 0 or bullet.coords[1] >= 430:
            bullet.angle = -(bullet.angle % 360)
            bullet.ref_count -= 1


def reflect_add(bullets, bullet):
    reflect(bullet)
    if bullet.counter % 30 == 0:
        temp = BBullet(1, random.randint(1, 361), 2,
                       (bullet.coords[0],
                        bullet.coords[1]), None)
        temp.func = lambda: reflect(temp)
        bullets.append(temp)


def gungnir_shot1(boss, bullets):
    boss.shot1.play()
    angle = 315 if boss.rev else 225
    temp = BBullet(0, angle, 4,
                   (boss.rect.centerx,
                    boss.rect.centery), None)
    temp.func = lambda: reflect_add(bullets, temp)
    boss.rev = not boss.rev
    bullets.append(temp)


def nova_shot(boss, bullets):
    if boss.retire_f:
        boss.retire += 1
    if boss.retire >= 180:
        boss.retire_f = False
    if boss.retire <= 0:
        boss.retire_f = True
    if boss.counter % 15 == 0 and not boss.retire_f:
        boss.shot2.play()
        temp = [30, 150, 210, 330]
        for i in range(4):
            bullets.append(BBullet(0, (i - 1.5) * 50 - 90 + boss.shift, 4,
                                   (boss.rect.centerx,
                                    boss.rect.centery), None))
            bullets.append(BBullet(3, temp[i] - boss.shift * 0.5, 3,
                                   (boss.rect.centerx,
                                    boss.rect.centery), None))
        for i in range(3):
            bullets.append(BBullet(4, i * 8 - boss.shift * 1.5, 4,
                                   (boss.rect.centerx,
                                    boss.rect.centery), None))

        boss.shift += 20
        boss.shift %= 360
        boss.retire -= 3


def gungnir_shot2(boss, bullets):
    if boss.retire_f:
        boss.retire += 1
    if boss.retire >= 80:
        boss.retire_f = False
    if boss.counter % 10 == 0 and not boss.retire_f:
        boss.shot1.play()
        for i in range(12):
            angle_t = random.randint(boss.shift - 50, boss.shift + 50)
            bullets.append(BBullet(2, angle_t, 3,
                                   (boss.rect.centerx + random.randint(-50, 50),
                                    boss.rect.centery + random.randint(-50, 50)), None))
        for i in range(4):
            angle_t = random.randint(boss.shift - 5, boss.shift + 5)
            bullets.append(BBullet(1, angle_t, 5,
                                   (boss.rect.centerx + random.randint(-30, 30),
                                    boss.rect.centery + random.randint(-30, 30)), None))
        bullets.append(BBullet(0, boss.shift, 7,
                               (boss.rect.centerx,
                                boss.rect.centery), None))
        boss.shift += (30 * (-1 if boss.rev else 1))
        boss.shift %= 360
    if boss.shift == 180 and boss.rev:
        boss.retire_f = True
        boss.retire = 0
        boss.rev = False
    if boss.shift == 0 and not boss.rev:
        boss.retire_f = True
        boss.retire = 0
        boss.rev = True


def knife_nova(boss, bullets):
    if boss.retire_f:
        boss.retire += 1
    if boss.retire >= 120:
        boss.retire_f = False
        boss.rev = not boss.rev
    if boss.retire <= 0:
        boss.retire_f = True
    if boss.counter % 3 == 0 and not boss.retire_f:
        boss.shot3.play()
        im = 5 if boss.rev else 6
        for i in range(4):
            bullets.append(BBullet(im, i * 90 - 90 + boss.shift, 3,
                                   (boss.rect.centerx,
                                    boss.rect.centery), None))
            bullets.append(BBullet(im, i * 90 - 90 + boss.shift, 4,
                                   (boss.rect.centerx,
                                    boss.rect.centery), None))

        boss.shift += 5 * (-1 if boss.rev else 1)
        boss.shift %= 360
        boss.retire -= 3


def circles_center(boss, bullets):
    if boss.retire_f:
        boss.retire += 1
    if boss.retire >= 120:
        boss.retire_f = False
    if boss.retire <= 0:
        boss.retire_f = True
    if boss.counter % 15 == 0 and not boss.retire_f:
        boss.shot2.play()
        for i in range(9):
            angle = degrees(atan2(boss.rect.centerx - boss.dims[0] / 2, boss.rect.centery - boss.dims[1] - 100)) + 90
            bullets.append(BBullet(0, angle + 20 * (4 - i), 7,
                                   (boss.rect.centerx,
                                    boss.rect.centery), None))
        boss.retire -= 3


def gungnir_nova(boss, bullets):
    if boss.retire_f:
        boss.retire += 1
    if boss.retire >= 80:
        boss.retire_f = False
    if boss.counter % 50 == 0 and not boss.retire_f:
        boss.shot1.play()
        slices = 6
        step = 360 // slices
        for i in range(slices):
            for j in range(12):
                angle_t = random.randint(-step * i - 50, -step * i + 50)
                bullets.append(BBullet(2, angle_t, 3,
                                       (5 * cos(radians(step * i)) + boss.rect.centerx + random.randint(-50, 50),
                                        5 * sin(radians(step * i)) + boss.rect.centery + random.randint(-50, 50)), None))
            for j in range(4):
                angle_t = random.randint(-step * i - 5, -step * i + 5)
                bullets.append(BBullet(1, angle_t, 4,
                                       (5 * cos(radians(step * i)) + boss.rect.centerx + random.randint(-30, 30),
                                        5 * sin(radians(step * i)) + boss.rect.centery + random.randint(-30, 30)), None))
            bullets.append(BBullet(0, -step * i, 7,
                                   (5 * cos(radians(step * i)) + boss.rect.centerx,
                                    5 * sin(radians(step * i)) + boss.rect.centery), None))


bbullets_imgs = ["Bullets/boss1b.png", "Bullets/boss2b.png", "Bullets/boss3b.png",
                 "Bullets/boss4b.png", "Bullets/boss5b.png", "Bullets/boss6b.png",
                 "Bullets/boss7b.png"]


class BBullet:
    def __init__(self, num, angle, speed, pos, func=None):
        self.angle = angle
        self.speed = speed

        self.func = func

        self.coords = [pos[0], pos[1]]
        self.ref_count = 2
        self.counter = 0
        self.no_rot_img = pygame.image.load(bbullets_imgs[num]).convert_alpha()
        self.dims = (self.no_rot_img.get_rect(center=pos).width, self.no_rot_img.get_rect(center=pos).height)
        self.image = pygame.transform.rotate(self.no_rot_img,
                                             angle - 90)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.coords[0] += self.speed * cos(radians(self.angle))
        self.coords[1] -= self.speed * sin(radians(self.angle))
        self.rect.centerx = self.coords[0]
        self.rect.centery = self.coords[1]

        if self.func is not None:
            self.func()

        self.counter += 1

    def draw(self, viewport: pygame.Surface):
        viewport.blit(self.image, self.rect)


class Boss:
    def __init__(self, viewport_dims):

        self.coords = [viewport_dims[0] / 2 + 100, -20]
        self.dims = viewport_dims
        self.dir_a = 0
        self.dir = [0, 0]
        self.start_coords = [self.coords[0], self.coords[1]]

        self.move_f = False

        self.prepare = True
        self.dead = False
        self.dead_timer = 120

        self.texs = [pygame.image.load("Bosses/Boss1/still.png"),
                     pygame.image.load("Bosses/Boss1/move.png")]

        self.image = self.texs[0]
        self.rect = self.image.get_rect(center=self.coords)

        self.shot1 = pygame.mixer.Sound("SFX/tan00.wav")
        self.shot1.set_volume(0.03)
        self.shot2 = pygame.mixer.Sound("SFX/tan01.wav")
        self.shot2.set_volume(0.03)
        self.shot3 = pygame.mixer.Sound("SFX/tan02.wav")
        self.shot3.set_volume(0.03)

        self.counter = 1
        self.speed = 1.0
        self.phase = 6
        self.hp = 2400
        self.shift = 0

        self.next_phase = False

        self.retire = 120
        self.retire_f = False

        self.rev = True

        pygame.mixer.music.stop()
        pygame.mixer.music.load("Music/Boss1.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()

    def random_move(self, length):
        self.start_coords = [self.coords[0], self.coords[1]]
        self.dir_a = radians(random.randint(-25, 206))
        self.dir = [length * cos(self.dir_a), -length * sin(self.dir_a)]
        if self.coords[0] <= 100 and self.dir[0] < 0:
            self.dir[0] *= -1
        if self.coords[0] >= 300 and self.dir[0] > 0:
            self.dir[0] *= -1
        if self.coords[1] <= length + 20 and self.dir[1] < 0:
            self.dir[1] *= -1
        if self.coords[1] >= 200 and self.dir[0] > 0:
            self.dir[1] *= -1
        self.move_f = True

    def update(self, bullets):

        if self.prepare and not (95 <= self.coords[1] <= 105):
            self.move_f = True
            self.coords[0] -= self.speed
            self.coords[1] += self.speed
        if self.prepare and (95 <= self.coords[1] <= 105):
            self.move_f = False
            self.prepare = False

        if not self.move_f:
            self.image = self.texs[0]

        elif self.move_f:
            self.image = self.texs[1]

        if not (self.start_coords[0] + self.dir[0] - 1 <= self.coords[0] <= self.start_coords[0] + self.dir[0] + 1 and
                self.start_coords[1] + self.dir[1] - 1 <= self.coords[1] <= self.start_coords[1] + self.dir[1] + 1):
            self.coords[0] += self.dir[0] / 40
            self.coords[1] += self.dir[1] / 40
        else:
            self.move_f = False

        self.rect.centerx = self.coords[0]
        self.rect.centery = self.coords[1]

        if self.phase != 0:
            temp = self.phase
            self.phase = floor(6 - self.hp / 400) + 1
            if self.phase > temp:
                self.retire = 60
                self.retire_f = False
                self.shift = 0
                bullets.clear()

        if self.phase == 1:
            if self.counter % 120 == 0 and self.counter > 200 and not self.move_f:
                self.random_move(50)
                gungnir_shot1(self, bullets)

        if self.phase == 2:
            self.start_coords = [self.coords[0], self.coords[1]]

            self.dir = [self.dims[0] / 2 - self.start_coords[0],
                        100 - self.start_coords[1]]
            self.move_f = True
            nova_shot(self, bullets)

        if self.phase == 3:
            if self.counter % 120 == 0 and not self.move_f:
                self.random_move(50)
            gungnir_shot2(self, bullets)

        if self.phase == 4:
            if self.counter % 220 == 0 and not self.move_f:
                self.random_move(50)
            knife_nova(self, bullets)

        if self.phase == 5:
            if self.counter % 10 == 0 and not self.move_f:
                self.random_move(70)
            circles_center(self, bullets)

        if self.phase == 6:
            if self.counter % 50 == 0 and not self.move_f:
                self.random_move(70)
            gungnir_nova(self, bullets)

        self.counter += 1

    def draw(self, viewport: pygame.Surface):
        viewport.blit(self.image, self.rect)
