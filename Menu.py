import pygame


class Button:
    def __init__(self, pos, image, function=None):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.bg = pygame.Surface((self.rect.width, self.rect.height))
        self.func = function
        self.highlight = False

    def run(self):
        self.func()

    def draw(self, viewport: pygame.Surface):
        self.bg.fill((255, 255, 255) if self.highlight else (0, 0, 0))
        viewport.blit(self.bg, self.rect)
        viewport.blit(self.image, self.rect)


class Menu:
    def __init__(self):
        self.buttons = []
        self.index_bt = 0

        self.select_s = pygame.mixer.Sound("SFX/se_select00.wav")
        self.select_s.set_volume(0.05)

        self.switch_s = pygame.mixer.Sound("SFX/se_ok00.wav")
        self.switch_s.set_volume(0.05)

        self.pause_s = pygame.mixer.Sound("SFX/se_pause.wav")
        self.pause_s.set_volume(0.05)

    def append(self, pos, image, function=None):
        self.buttons.append(Button(pos, image, function))
        self.buttons[self.index_bt].highlight = True

    def switch(self, direction):
        self.select_s.play()
        self.index_bt = max(0, min(self.index_bt + direction, len(self.buttons) - 1))
        for button in self.buttons:
            button.highlight = False
        self.buttons[self.index_bt].highlight = True

    def select(self):
        self.switch_s.play()
        self.buttons[self.index_bt].run()

    def draw(self, viewport: pygame.Surface):
        for button in self.buttons:
            button.draw(viewport)
