import os
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey != None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
    return image


class fencer(pygame.sprite.Sprite):
    def __init__(self, group, side="left"):
        super().__init__(group)
        self.side = side
        self.image = load_image(side + "_mid_stance.png", colorkey=-1)
        self.stance = 2
        self.rect = self.image.get_rect()
        self.rect.y = 50
        if side == "left":
            self.rect.x = 150
        if side == "right":
            self.rect.x = 300


pygame.init()
size = (500, 150)
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
all_sprites = pygame.sprite.Group()
left_fencer = fencer(all_sprites)
right_fencer = fencer(all_sprites, "right")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()