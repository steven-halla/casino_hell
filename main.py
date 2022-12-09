
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
        self.speed = 5
        self.width = width
        self.height = height


    def draw(self, display):
        pygame.draw.rect(display, Red, (self.x, self.y, self.width, self.height))


    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed


player = PlayerRed(20, 30, 50, 50)


running = True
while running:

    display.fill((124,164,114))
    pygame.draw.rect(display,Blue, [170,70,50,50])


    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check if the left arrow key is pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            player.move_left()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            player.move_right()


    # fill the screen with white

    # draw the rectangle on the screen
    player.draw(display)


    # update the screen
    pygame.display.update()

# close Pygame when the game loop is finished
pygame.quit()

