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


class fencer(pygame.sprite.Sprite):
    # класс игрока
    def __init__(self, group, side="left"):
        # базовая инициализация
        super().__init__(group)
        # выбор того, какой из двух игроко это будет
        self.side = side
        # загрузка картинки игрока
        self.image = load_image(side + "_mid_stance.png", colorkey=-1)
        # установка стойки
        self.stance = 2
        # установка координат
        self.rect = self.image.get_rect()
        self.rect.y = 50
        if side == "left":
            self.rect.x = 150
        if side == "right":
            self.rect.x = 300


pygame.init()
# создаем окно
size = (500, 150)
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
# создаем группу всех спрайтов
all_sprites = pygame.sprite.Group()
# создаем спрайты игроков
left_fencer = fencer(all_sprites)
right_fencer = fencer(all_sprites, "right")
# игровой цикл
running = True
while running:
    for event in pygame.event.get():
        # закрытие окна
        if event.type == pygame.QUIT:
            running = False
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()