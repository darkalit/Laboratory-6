from Player import *
from Enemy import *
from Misc import *
from Menu import *
from EnemiesList import *
from Boss import *


def ellipse_point(rectDims, rectCenter, rectRotation, point):
    tx = (point[0] - rectCenter[0]) * cos(rectRotation) - (point[1] - rectCenter[1]) * sin(rectRotation)
    ty = (point[0] - rectCenter[0]) * sin(rectRotation) + (point[1] - rectCenter[1]) * cos(rectRotation)

    return pow(2 * tx / rectDims[0], 2) + pow(2 * ty / rectDims[1], 2) < 1


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.viewport = (400, 430)
        self.screen = pygame.display.set_mode((640, 480), pygame.SCALED | pygame.FULLSCREEN)
        self.background = pygame.Surface(self.viewport)
        self.bg = pygame.image.load("Misc/bg.png").convert_alpha()
        self.bgY1 = 0
        self.bgY2 = self.bg.get_height()

        pygame.display.set_caption("Touhou crap clone")
        self.running = True
        self.clock = pygame.time.Clock()
        self.counter = 1

        self.menu_f = True
        self.inf_mode = False
        self.pause_f = False
        self.win_f = False
        self.lose_f = False

        self.win_img = Button((self.screen.get_width() / 2, 200), "Menu/gm_win.png", None)
        self.lose_img = Button((self.screen.get_width() / 2, 200), "Menu/gm_lose.png", None)

        self.menu_bg = pygame.image.load("Menu/bg.png").convert_alpha()
        self.menu = Menu()
        self.menu.append((self.screen.get_width() / 2, 100), "Menu/gm_start.png", self.start_no_inf_game)
        self.menu.append((self.screen.get_width() / 2, 200), "Menu/gm_inf.png", self.start_inf_game)
        self.menu.append((self.screen.get_width() / 2, 300), "Menu/gm_quit.png", self.quit_game)

        self.pause = Menu()
        self.pause.append((self.screen.get_width() / 2, 200), "Menu/gm_continue.png", self.continue_game)
        self.pause.append((self.screen.get_width() / 2, 300), "Menu/gm_quit.png", self.return_menu)

        self.win = Menu()
        self.win.append((self.screen.get_width() / 2, 300), "Menu/gm_quit.png", self.return_menu)

        self.lose = Menu()
        self.lose.append((self.screen.get_width() / 2, 300), "Menu/gm_quit.png", self.return_menu)

        self.font = pygame.font.Font("font.ttf", 16)
        self.score_txt = self.font.render(f"{0}", True, "white")
        self.power_txt = self.font.render(f"{0.00}/4.00", True, "white")
        self.gui_score = pygame.image.load("Misc/gui_score.png").convert_alpha()

        self.score = 0
        self.power_u = 0.1

        self.lives = 4
        self.max_lives = 7
        self.max_lives_img = pygame.image.load("Misc/HP_n.png").convert_alpha()
        self.lives_img = pygame.image.load("Misc/HP_p.png").convert_alpha()

        self.player = Player((self.viewport[0] / 2, self.viewport[1] - 40), self.viewport)
        self.b_shooting = False
        self.bullets = []

        self.enemies = []
        self.e_bullets = []
        self.deaths = []
        self.power_ups = []

        self.boss1_f = False
        self.boss1 = None

    def start_no_inf_game(self):
        self.menu_f = False
        self.inf_mode = False
        pygame.mixer.music.load("Music/Stage1.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

    def start_inf_game(self):
        self.menu_f = False
        self.inf_mode = True
        pygame.mixer.music.load("Music/Inf_Mode.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def quit_game(self):
        self.running = False

    def continue_game(self):
        pygame.mixer.music.unpause()
        self.pause_f = False

    def return_menu(self):
        # temp = self.score
        self.__init__()
        self.menu_f = True
        self.pause_f = False
        self.lose_f = False
        self.win_f = False

    def input_menu(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            if event.key == pygame.K_UP:
                self.menu.switch(-1)
            if event.key == pygame.K_DOWN:
                self.menu.switch(1)
            if event.key == pygame.K_RETURN or event.key == pygame.K_z or event.key == pygame.K_x:
                self.menu.select()

    def show_menu(self):
        self.screen.blit(self.menu_bg, (0, 0))
        self.menu.draw(self.screen)

    def input_pause(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pause_f = False
                pygame.mixer.music.unpause()
            if event.key == pygame.K_UP:
                self.pause.switch(-1)
            if event.key == pygame.K_DOWN:
                self.pause.switch(1)
            if event.key == pygame.K_RETURN or event.key == pygame.K_z or event.key == pygame.K_x:
                self.pause.select()

    def show_pause(self):
        self.pause.draw(self.screen)

    def input_win(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_z or event.key == pygame.K_x:
                self.win.select()

    def show_win(self):
        self.win_img.draw(self.screen)
        self.win.draw(self.screen)

    def input_lose(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_z or event.key == pygame.K_x:
                self.lose.select()

    def show_lose(self):
        self.lose_img.draw(self.screen)
        self.lose.draw(self.screen)

    def input_game(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pause_f = True
                pygame.mixer.music.pause()
                self.pause.pause_s.play()
            if event.key == pygame.K_LEFT:
                self.player.stance['left'] = True
            if event.key == pygame.K_RIGHT:
                self.player.stance['right'] = True
            if event.key == pygame.K_UP:
                self.player.stance['up'] = True
            if event.key == pygame.K_DOWN:
                self.player.stance['down'] = True
            if event.key == pygame.K_LSHIFT:
                self.player.slow = True
            if event.key == pygame.K_z:
                self.b_shooting = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.player.stance['left'] = False
            if event.key == pygame.K_RIGHT:
                self.player.stance['right'] = False
            if event.key == pygame.K_UP:
                self.player.stance['up'] = False
            if event.key == pygame.K_DOWN:
                self.player.stance['down'] = False
            if event.key == pygame.K_LSHIFT:
                self.player.slow = False
            if event.key == pygame.K_z:
                self.b_shooting = False

    def update_game(self):
        if self.bgY1 >= self.bg.get_height():
            self.bgY1 = -self.bg.get_height()

        if self.bgY2 >= self.bg.get_height():
            self.bgY2 = -self.bg.get_height()

        self.bgY1 += 1
        self.bgY2 += 1

        self.player.update()
        for bullet in self.bullets:
            bullet.update()

        if self.b_shooting and self.counter % 5 == 0:
            self.player.shoot(self.bullets)

        if self.inf_mode:
            # if self.counter % int(floor(40*(pow(e, pow(-(self.counter/3000), 2)) - 1/(self.counter + 60))) + 20) == 0:
            if round(2 * cos(pow(floor(self.counter + 0.1) / 40, 2)), 1) == 0:
                while True:
                    enemy = Level1[random.randint(0, len(Level1) - 7)]
                    if enemy[6] < 40:
                        break
                self.enemies.append(Enemy(enemy[0], enemy[1], enemy[2], enemy[3], enemy[4],
                                          enemy[5], enemy[6], enemy[7], enemy[8], enemy[9]))
        else:
            if self.counter > 3300 and self.boss1 is None:
                self.boss1 = Boss(self.viewport)
            else:
                for enemy in Level1:
                    if enemy[10] == self.counter:
                        self.enemies.append(Enemy(enemy[0], enemy[1], enemy[2], enemy[3], enemy[4],
                                                  enemy[5], enemy[6], enemy[7], enemy[8], enemy[9]))

        for bullet in self.e_bullets:
            bullet.update()
            dir = (-bullet.rect.centerx + self.player.rect.centerx, bullet.rect.centery - self.player.rect.centery)
            abs_dir = sqrt(dir[0] * dir[0] + dir[1] * dir[1])
            if self.counter % 20 and abs_dir < 14:
                self.score += 1
            if ellipse_point(bullet.dims,
                             (bullet.rect.centerx, bullet.rect.centery),
                             radians(bullet.angle - 90),
                             (self.player.rect.centerx, self.player.rect.centery)) and not self.player.invis:
                minus = 0.6
                self.player.power_unit -= minus
                self.player.power_unit = max(self.player.power_unit, 0.0)
                for i in range(int(min(minus, self.player.power_unit) / self.power_u) - 2):
                    self.power_ups.append(PowerUp((self.player.rect.centerx + random.randint(-100, 100),
                                                     self.player.rect.centery + random.randint(-20, 20)), 0))
                self.player.rect.centerx = self.player.startpos[0]
                self.player.rect.centery = self.viewport[1]
                self.lives -= 1
                self.player.invis = True
                self.player.dead = True

            if bullet.rect.centery > self.viewport[1] + 50 or bullet.rect.centery < -50 or \
                    bullet.rect.centerx > self.viewport[0] + 50 or bullet.rect.centerx < -50:
                self.e_bullets.remove(bullet)

        for enemy in self.enemies:
            enemy.update()
            enemy.shoot((self.player.rect.centerx, self.player.rect.centery),
                        self.e_bullets)
            if enemy.rect.centery > self.viewport[1] + 50 or enemy.rect.centery < -50 or \
                    enemy.rect.centerx > self.viewport[0] + 50 or enemy.rect.centerx < -50:
                self.enemies.remove(enemy)

        for enemy in self.enemies:
            for bullet in self.bullets:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.hp -= 1
                    self.bullets.remove(bullet)
                    if enemy.hp <= 0:
                        self.score += 100
                        self.power_ups.append(PowerUp((enemy.rect.centerx, enemy.rect.centery), 0))

                        if random.randint(1, 1000) == 500:
                            self.power_ups.append(PowerUp((enemy.rect.centerx, enemy.rect.centery), 1))

                        self.deaths.append(Explosion((enemy.rect.centerx, enemy.rect.centery)))
                        self.enemies.remove(enemy)
                        break

        for death in self.deaths:
            death.update()
            if death.dead:
                self.deaths.remove(death)

        for powerup in self.power_ups:
            powerup.update(self.player)
            if self.player.rect.centerx + 3 >= powerup.rect.centerx >= self.player.rect.centerx - 3 \
                    and self.player.rect.centery + 3 >= powerup.rect.centery >= self.player.rect.centery - 3:
                self.power_ups.remove(powerup)
                if powerup.var == 0:
                    self.player.power_unit += self.power_u
                    if self.player.pu_count >= 4:
                        self.score += 50
                if powerup.var == 1:
                    self.lives += 1
            if powerup.rect.centery > self.viewport[1] + 50:
                self.power_ups.remove(powerup)

        if self.boss1 is not None:
            if not self.boss1.dead:
                self.boss1.update(self.e_bullets)
                if self.boss1.counter > 200:
                    for bullet in self.bullets:
                        if self.boss1.rect.colliderect(bullet.rect):
                            self.boss1.hp -= 1
                            self.score += 50
                            self.bullets.remove(bullet)
                            if self.boss1.hp <= 0:
                                self.boss1.dead = True
                                self.e_bullets.clear()
                                self.boss1.phase = 0
                                pygame.mixer.music.stop()
                                break

            if self.boss1.dead and self.boss1.dead_timer > 0:
                self.deaths.append(Explosion((self.boss1.rect.centerx, self.boss1.rect.centery)))
                self.boss1.dead_timer -= 1
            elif self.boss1.dead and self.boss1.dead_timer <= 0:
                del self.boss1
                self.win_f = True

        if self.lives < 0:
            self.lose_f = True
            pygame.mixer.music.stop()

        self.score_txt = self.font.render(f"{self.score}", True, "white")
        self.power_txt = self.font.render("%.2f/4.00" % self.player.power_unit, True, "white")

        self.counter += 1

    def show_game(self):
        self.screen.fill((128, 0, 64))

        self.screen.blit(self.background, (25, 25))
        self.background.fill((255, 255, 255))

        self.background.blit(self.bg, (0, self.bgY1))
        self.background.blit(self.bg, (0, self.bgY2))

        for death in self.deaths:
            death.draw(self.background)

        for powerup in self.power_ups:
            powerup.draw(self.background)

        for bullet in self.bullets:
            bullet.draw(self.background)
        self.player.draw(self.background)

        if self.boss1 is not None:
            self.boss1.draw(self.background)

        for enemy in self.enemies:
            enemy.draw(self.background)

        for bullet in self.e_bullets:
            bullet.draw(self.background)

        self.screen.blit(self.score_txt, self.score_txt.get_rect(topleft=(self.viewport[0] + 100, 30)))
        self.screen.blit(self.power_txt, self.power_txt.get_rect(topleft=(self.viewport[0] + 100, 70)))
        self.screen.blit(self.gui_score, self.gui_score.get_rect(topleft=(self.viewport[0] + 40, 30)))
        for i in range(self.max_lives):
            self.screen.blit(self.max_lives_img, self.max_lives_img.get_rect(
                topleft=(self.viewport[0] + 100 + 16 * i, 52)))

        for i in range(self.lives):
            self.screen.blit(self.lives_img, self.lives_img.get_rect(
                topleft=(self.viewport[0] + 100 + 16 * i, 52)))

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.menu_f:
                self.input_menu(event)
            elif self.pause_f:
                self.input_pause(event)
            elif self.win_f:
                self.input_win(event)
            elif self.lose_f:
                self.input_lose(event)
            else:
                self.input_game(event)

    def update(self):
        if self.menu_f:
            pass
        elif self.pause_f:
            pass
        elif self.win_f:
            pass
        elif self.lose_f:
            pass
        else:
            self.update_game()

    def display(self):
        if self.menu_f:
            self.show_menu()
        elif self.pause_f:
            self.show_pause()
        elif self.win_f:
            self.show_win()
        elif self.lose_f:
            self.show_lose()
        else:
            self.show_game()

        self.clock.tick(60)
        pygame.display.flip()

    def is_running(self):
        return self.running
