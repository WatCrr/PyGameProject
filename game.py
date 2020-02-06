import os
import pygame


def load_image(name, colorkey=None):
    # функция загрузки изображения
    # загружаем изображение, убираем alpha values формат записи пикселей, если таковой используется
    fullname = os.path.join("data", name)
    image = pygame.image.load(fullname).convert()
    # устанавливаем colorkey для обрезания фона
    if colorkey != None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class BarrierBox(pygame.sprite.Sprite):
    # класс коробки, ограничивающей перемещение игроков
    def __init__(self, group, side="left"):
        super().__init__(group)
        self.image = load_image("barrier_box.png", colorkey=-1)
        self.rect = self.image.get_rect()
        self.rect.y = 50
        if side == "left":
            self.rect.x = 50
        if side == "right":
            self.rect.x = 400


class Fencer(pygame.sprite.Sprite):
    # класс игрока
    def __init__(self, group, side="left"):
        # базовая инициализация
        super().__init__(group)
        # выбор того, какой из двух игроков это будет
        self.side = side
        # загрузка картинки игрока
        self.image = load_image(side + "_mid_stance.png", colorkey=-1)
        # установка состояний
        self.stance = 2
        self.attacking = 0
        self.walking = 0
        # установка координат
        self.rect = self.image.get_rect()
        self.rect.y = 50
        if side == "left":
            self.rect.x = 150
        if side == "right":
            self.rect.x = 300

    def react(self, key):
        # реакция на нажатие клавиши
        if self.attacking == 0:
            if (key == pygame.K_w) or (key == pygame.K_o):
                # смена стойки на более верхнюю
                if self.stance < 3:
                    self.stance += 1
            if (key == pygame.K_s) or (key == pygame.K_l):
                # смена стойки на более нижнюю
                if self.stance > 1:
                    self.stance -= 1
            if (key == pygame.K_LALT) or (key == pygame.K_RALT):
                self.attacking = 24


    def next_state(self):
        # обноление состояния
        if self.attacking == 0:
            if self.stance == 1:
                self.image = load_image(self.side + "_down_stance.png", colorkey=-1)
            if self.stance == 2:
                self.image = load_image(self.side + "_mid_stance.png", colorkey=-1)
            if self.stance == 3:
                self.image = load_image(self.side + "_up_stance.png", colorkey=-1)
        else:
            if self.stance == 1:
                self.image = load_image(self.side + "_down_attack.png", colorkey=-1).\
                    subsurface(pygame.Rect(50 - self.attacking // 19 * 50, 0, 50, 50))
            if self.stance == 2:
                self.image = load_image(self.side + "_mid_attack.png", colorkey=-1).\
                    subsurface(pygame.Rect(50 - self.attacking // 19 * 50, 0, 50, 50))
            if self.stance == 3:
                self.image = load_image(self.side + "_up_attack.png", colorkey=-1).\
                    subsurface(pygame.Rect(50 - self.attacking // 19 * 50, 0, 50, 50))
            self. attacking -= 1
           

pygame.init()
# создаем окно
size = (500, 150)
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
# создаем группу всех спрайтов
all_sprites = pygame.sprite.Group()
# создаем спрайты игроков
left_fencer = Fencer(all_sprites)
right_fencer = Fencer(all_sprites, "right")
left_box = BarrierBox(all_sprites)
right_box = BarrierBox(all_sprites, "right")
# игровой цикл
# таймер
clock = pygame.time.Clock()
fps = 24
running = True
while running:
    for event in pygame.event.get():
        # закрытие окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_o) or (event.key == pygame.K_l) or (event.key == pygame.K_RALT):
                right_fencer.react(event.key)
            if (event.key == pygame.K_w) or (event.key == pygame.K_s) or (event.key == pygame.K_LALT):
                left_fencer.react(event.key)
    right_fencer.next_state()
    left_fencer.next_state()
    # отрисовываем спрайты
    screen.fill((120, 60, 30))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
# закрыаем окно
pygame.quit()