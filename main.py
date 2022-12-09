
import pygame

pygame.init()

windowSize = [500, 500]
display = pygame.display.set_mode(windowSize)
pygame.display.set_caption("Shooter")
Green = (0,255,0)
Blue = (0,0,255)
Red = (255, 0, 0)

class PlayerRed(pygame.sprite.Sprite):
    def __init__(self, x,y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.direction = 1
        self.width = width
        self.height = height

    def move(self, moving_left, moving_right):
        if moving_left:
            self.direction = - 1
        if moving_right:
            self.direction = + 1

player = PlayerRed(10, 10, 50, 50)



while True:
    display.fill((124, 164, 114))
    # pygame.draw.rect(display,Red, [10,10,50,50])
    pygame.draw.rect(display,Blue, [170,70,50,50])





    for event in pygame.event.get():

        # keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True

        if event.type == pygame.QUIT:
            # quits pygame library
            pygame.quit()

            # quiet the program
            quit()

    pygame.display.update()