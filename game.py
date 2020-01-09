
import pygame


pygame.init()
size = (350, 150)
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
fps = (24)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()