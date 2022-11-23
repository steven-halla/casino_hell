import pygame


pygame.init()


display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

while True:
    display.fill((0,0,0))
    clock.tick(60)
    pygame.display.update()