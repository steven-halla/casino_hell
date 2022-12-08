import pygame

pygame.init()

windowSize = [500, 500]
screen = pygame.display.set_mode(windowSize)

while True :
    screen.fill('#000000')


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #quits pygame library
            pygame.quit()
            #quiet the program
            quit()