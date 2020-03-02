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
        # загрузка картинки коробки
        self.image = load_image("barrier_box.png", colorkey=-1)
        # установка координат
        self.rect = self.image.get_rect()
        self.rect.y = 50
        if side == "left":
            self.rect.x = 50
        if side == "right":
            self.rect.x = 400


class Fencer(pygame.sprite.Sprite):
    # класс игрока
    def __init__(self, group, side="left"):
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
            if (key == pygame.K_d) or (key == pygame.K_SEMICOLON):
                self.walking = 12
            if (key == pygame.K_a) or (key == pygame.K_k):
                self.walking = -12


    def next_state(self):
        # обноление состояния
        if self.attacking == 0:
            if self.walking == 0:
                if self.stance == 1:
                    self.image = load_image(self.side + "_down_stance.png", colorkey=-1)
                if self.stance == 2:
                    self.image = load_image(self.side + "_mid_stance.png", colorkey=-1)
                if self.stance == 3:
                    self.image = load_image(self.side + "_up_stance.png", colorkey=-1)
            else:
                if self.stance == 1:
                    self.image = load_image(self.side + "_down_walk.png", colorkey=-1).\
                        subsurface(pygame.Rect(50 * (abs(self.walking) // (-4) + 3), 0, 50, 50))
                if self.stance == 2:
                    self.image = load_image(self.side + "_mid_walk.png", colorkey=-1).\
                        subsurface(pygame.Rect(50 * (abs(self.walking) // (-4) + 3), 0, 50, 50))
                if self.stance == 3:
                    self.image = load_image(self.side + "_up_walk.png", colorkey=-1).\
                        subsurface(pygame.Rect(50 * (abs(self.walking) // (-4) + 3), 0, 50, 50))
                if self.walking > 0:
                    self.walking -= 1
                    self.rect.x += 1
                else:
                    self.walking += 1
                    self.rect.x -= 1
        else:
            self.walking = 0
            if self.stance == 1:
                self.image = load_image(self.side + "_down_attack.png", colorkey=-1).\
                    subsurface(pygame.Rect(50 - self.attacking // 19 * 50, 0, 50, 50))
            if self.stance == 2:
                self.image = load_image(self.side + "_mid_attack.png", colorkey=-1).\
                    subsurface(pygame.Rect(50 - self.attacking // 19 * 50, 0, 50, 50))
            if self.stance == 3:
                self.image = load_image(self.side + "_up_attack.png", colorkey=-1).\
                    subsurface(pygame.Rect(50 - self.attacking // 19 * 50, 0, 50, 50))
            self.attacking -= 1
           

pygame.init()
# создаем окно
size = (500, 200)
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
right_wins = 0
left_wins = 0
while running:
    for event in pygame.event.get():
        # закрытие окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if ((event.key == pygame.K_o) or (event.key == pygame.K_l) or
                (event.key == pygame.K_RALT) or
                (event.key == pygame.K_k) or (event.key == pygame.K_SEMICOLON)):
                right_fencer.react(event.key)
            if ((event.key == pygame.K_w) or (event.key == pygame.K_s) or
                (event.key == pygame.K_LALT) or
                (event.key == pygame.K_a) or (event.key == pygame.K_d)):
                left_fencer.react(event.key)
    right_fencer.next_state()
    left_fencer.next_state()
    if pygame.sprite.collide_mask(left_fencer, left_box):
        left_fencer.rect.x += 1
    if pygame.sprite.collide_mask(right_fencer, right_box):
        right_fencer.rect.x -= 1
    if pygame.sprite.collide_mask(right_fencer, left_fencer):
        if (right_fencer.attacking > 0) and (right_fencer.attacking < 13) and\
            (right_fencer.stance != left_fencer.stance):
            right_wins += 1
            right_fencer.rect.x = 300
            left_fencer.rect.x = 150
            right_fencer.stance = 2
            left_fencer.stance = 2
        if (left_fencer.attacking > 0) and (left_fencer.attacking < 13) and\
            (right_fencer.stance != left_fencer.stance):
            left_wins +=1
            right_fencer.rect.x = 300
            left_fencer.rect.x = 150
            right_fencer.stance = 2
            left_fencer.stance = 2
        right_fencer.rect.x += 1
        left_fencer.rect.x -= 1
    # отрисовываем
    screen.fill((120, 60, 30))
    num_font = pygame.font.Font(None, 40)
    left_wins_table = num_font.render(str(left_wins), 0, (255, 0, 255))
    right_wins_table = num_font.render(str(right_wins), 0, (255, 0, 255))
    screen.blit(left_wins_table, (5, 5))
    screen.blit(right_wins_table, (500 - 25 * len(str(right_wins)), 5)) 
    rules_font = pygame.font.Font(None, 15)
    rules = rules_font.render("Упраление:", 0, (255, 0, 255))
    screen.blit(rules, (50, 104))
    rules = rules_font.render("Передвижние: A и D, K и ;. Атака: левый, правый Alt." +
                              "Смена стойки W и S, O и L",
                              0, (255, 0, 255))
    screen.blit(rules, (50, 119))
    rules = rules_font.render("Правила:", 0, (255, 0, 255))
    screen.blit(rules, (50, 134))
    rules = rules_font.render("Чтоб заработать очко, нужно ударить соперника.",
                              0, (255, 0, 255))
    screen.blit(rules, (50, 149))
    rules = rules_font.render("Чтобы заблокировать удар, нужно принять ту же стойку, что и соперник",
                              0, (255, 0, 255))
    screen.blit(rules, (50, 164))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
# закрыаем окно
pygame.quit()
# пельмешки