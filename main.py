
import pygame

pygame.init()

windowSize = [500, 500]
display = pygame.display.set_mode(windowSize)
pygame.display.set_caption("Shooter")
Green = (0,255,0)
Blue = (0,0,255)
Red = (255, 0, 0)

Class

while True:
    display.fill((124, 164, 114))
    pygame.draw.rect(display,Red, [10,10,50,50])
    pygame.draw.rect(display,Blue, [170,70,50,50])

    for event in pygame.event.get():



        if event.type == pygame.QUIT:
            # quits pygame library
            pygame.quit()

            # quiet the program
            quit()

    pygame.display.update()