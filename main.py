import pygame
import sys
import random
import math

# example of a way to handle our images
# images = {
# "player" : {
#     "run"  :  [pygame.image.load("player_run_1.png"), pygame.image.load("player_run_2.png"), pygame.image.load("player_run_3.png"),]
#     "jump" : [pygame.image.load("player_jump_1.png"),pygame.image.load("player_jump_2.png"),]
#     }
# }



pygame.init()


display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player_walk_images = [pygame.image.load("images/player_walk_0.png"), pygame.image.load("images/player_walk_1.png"),
                      pygame.image.load("images/player_walk_2.png"), pygame.image.load("images/player_walk_3.png")]


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.moving_right = False
        self.moving_left = False
    def main(self, display):
        if self.animation_count + 1 >= 16:
            self.animation_count = 0



        self.animation_count += 1

        if self.moving_right:
            display.blit(pygame.transform.scale(player_walk_images[self.animation_count//4], (32, 42)), (self.x, self.y))
        elif self.moving_left:
            display.blit(pygame.transform.scale(pygame.transform.flip(player_walk_images[self.animation_count//4], True, False), (32, 42)), (self.x, self.y))
        else:
            display.blit(pygame.transform.scale(player_walk_images[0], (32, 42)), (self.x, self.y))

        self.moving_right = False
        self.moving_left = False





class SlimeEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_images = [pygame.image.load("images/slime_animation_0.png"),pygame.image.load("images/slime_animation_1.png"),
                                 pygame.image.load("images/slime_animation_2.png"),pygame.image.load("images/slime_animation_3.png")
                                 ]
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-300, 300)
        self.offset_y = random.randrange(-300, 300)

    def main(self, display):
        if self.animation_count + 1 == 16:
            self.animation_count = 0
        self.animation_count += 1



        display.blit(pygame.transform.scale(self.animation_images[self.animation_count//4], (32, 30)), (self.x - display_scroll[0], self.y - display_scroll[1]))



enemies = [SlimeEnemy(500, 400)]

player = Player(400, 300, 32, 32)

display_scroll = [0,0]



while True:
    display.fill((24,164,86))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.QUIT



    keys = pygame.key.get_pressed()


    if keys[pygame.K_a]:
        display_scroll[0] -= 5

        player.moving_left = True



    if keys[pygame.K_d]:
        display_scroll[0] += 5

        player.moving_right = True


    if keys[pygame.K_w]:
        display_scroll[1] -= 5



    if keys[pygame.K_s]:
        display_scroll[1] += 5


    player.main(display)




    for enemy in enemies:
        enemy.main(display)

    clock.tick(60)
    pygame.display.update()