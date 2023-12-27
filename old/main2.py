# import pygame
# import sys
# import random
# import math
# # https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
#
# # example of a way to handle our images
# # images = {
# # "player" : {
# #     "run"  :  [pygame.image.load("player_run_1.png"), pygame.image.load("player_run_2.png"), pygame.image.load("player_run_3.png"),]
# #     "jump" : [pygame.image.load("player_jump_1.png"),pygame.image.load("player_jump_2.png"),]
# #     }
# # }
#
#
#
# pygame.init()
#
# # this is the display for the game screen
# # display = pygame.display.set_mode((800, 600))
#
# white = (255, 255, 255)
# green = (0, 255, 0)
# blue = (0, 0, 128)
#
# #new code
# X = 400
# Y = 400
#
# #order of display is important!
# display_surface = pygame.display.set_mode((X,Y))
# display = pygame.display.set_mode((800, 600))
#
#
# #set the pygame window name
# pygame.display.set_caption('Show Text')
# font = pygame.font.Font('freesansbold.ttf', 32)
# text = font.render("Hi there Im the shop keeper", True, green, blue)
# textRect = text.get_rect()
#
# #cordinates of our tet
# textRect.center = (X // 1, Y // 2)
#
#
# clock = pygame.time.Clock()
#
# player_walk_images = [pygame.image.load("images/player_walk_0.png"), pygame.image.load("images/player_walk_1.png"),
#                       pygame.image.load("images/player_walk_2.png"), pygame.image.load("images/player_walk_3.png")]
#
#
# class Player:
#     def __init__(self, x, y, width, height):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.animation_count = 0
#         self.moving_right = False
#         self.moving_left = False
#     def main(self, display):
#         if self.animation_count + 1 >= 16:
#             self.animation_count = 0
#         self.animation_count += 1
#         if self.moving_right:
#             display.blit(pygame.transform.scale(player_walk_images[self.animation_count//4], (32, 42)), (self.x, self.y))
#         elif self.moving_left:
#             display.blit(pygame.transform.scale(pygame.transform.flip(player_walk_images[self.animation_count//4], True, False), (32, 42)), (self.x, self.y))
#         else:
#             display.blit(pygame.transform.scale(player_walk_images[0], (32, 42)), (self.x, self.y))
#         self.moving_right = False
#         self.moving_left = False
#
# class SlimeNpc:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         # self.animation_images = [pygame.image.load("images/slime_animation_0.png"),pygame.image.load("images/slime_animation_1.png"),
#         #                          pygame.image.load("images/slime_animation_2.png"),pygame.image.load("images/slime_animation_3.png")
#         #                          ]
#         self.animation_count = 0
#         self.reset_offset = 0
#         self.offset_x = random.randrange(-300, 300)
#         self.offset_y = random.randrange(-300, 300)
#
#     def main(self, display):
#         if self.animation_count + 1 == 16:
#             self.animation_count = 0
#         self.animation_count += 1
#         display_surface.blit(text, textRect)
#
#         # display.blit(pygame.transform.scale(self.animation_images[self.animation_count//4], (32, 30)), (self.x - display_scroll[0], self.y - display_scroll[1]))
#
#
#
#
# enemies = [SlimeNpc(500, 400)]
#
# player = Player(400, 300, 32, 32)
#
# display_scroll = [0,0]
#
#
#
# # this is the game loop
#
# while True:
#     #background color
#     display.fill((124,164,114))
#     #
#     # display_surface.blit(text, textRect)
#
#
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             #quits pygame library
#             pygame.quit()
#             #quiet the program
#             quit()
#
#
#
#     keys = pygame.key.get_pressed()
#
#
#     if keys[pygame.K_a]:
#         display_scroll[0] -= 5
#
#         player.moving_left = True
#
#     if keys[pygame.K_f]:
#         display_surface.blit(text,textRect)
#
#
#
#     if keys[pygame.K_d]:
#         display_scroll[0] += 5
#
#         player.moving_right = True
#
#
#     if keys[pygame.K_w]:
#         display_scroll[1] -= 5
#
#
#
#     if keys[pygame.K_s]:
#         display_scroll[1] += 5
#
#
#     player.main(display)
#
#     for Npc in enemies:
#         Npc.main(display)
#
#     clock.tick(60)
#     pygame.display.update()
#
# import pygame
#
# # define a class to represent the rectangle
# class Rectangle:
#     def __init__(self, x, y, width, height):
#         # initialize the position and size of the rectangle
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.speed = 5
#
#     def move_left(self):
#         # move the rectangle to the left by subtracting the speed from its x position
#         self.x -= self.speed
#
#     def draw(self, screen):
#         # draw the rectangle on the screen
#         pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
#
# # initialize Pygame and create a screen
# pygame.init()
# screen = pygame.display.set_mode((800, 600))
#
# # create a new rectangle and set its initial position
# rect = Rectangle(100, 100, 50, 50)
#
# # game loop
# running = True
# while running:
#     # check for events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#         # check if the left arrow key is pressed
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
#             rect.move_left()
#
#     # fill the screen with white
#     screen.fill((255, 255, 255))
#
#     # draw the rectangle on the screen
#     rect.draw(screen)
#
#     # update the screen
#     pygame.display.update()
#
# # close Pygame when the game loop is finished
# pygame.quit()


# import pygame module in this program
import pygame

# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# define the RGB value for white,
#  green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

# assigning values to X and Y variable
X = 400
Y = 400

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y))

# set the pygame window name
pygame.display.set_caption('Show Text')

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)

# create a text surface object,
# on which text is drawn on it.
text = font.render('GeeksForGeeks', True, green, blue)

# create a rectangular object for the
# text surface object
textRect = text.get_rect()

# set the center of the rectangular object.
textRect.center = (X // 2, Y // 1.3)

# infinite loop
while True:

    # completely fill the surface object
    # with white color
    display_surface.fill(white)

    # copying the text surface object
    # to the display surface object
    # at the center coordinate.



    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                display_surface.blit(text, textRect)


        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
            # deactivates the pygame library
            pygame.quit()

            # quit the program.
            quit()

        # Draws the surface object to the screen.
        pygame.display.update()