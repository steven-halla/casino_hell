import pygame
from pygame.locals import *
import math
import keyboard


clock = pygame.time.Clock()

pygame.init()
X = 400
Y = 400
WINDOWS_SIZE: [int, int] = [500, 500]
display = pygame.display.set_mode(WINDOWS_SIZE)
pygame.display.set_caption("Shooter")
GREEN: (int, int, int) = (0, 255, 0)
WHITE: (int, int, int) = (255, 255, 255)
BLUE: (int, int, int) = (0, 0, 255)
RED: (int, int, int) = (255, 0, 0)
TILE_SIZE = 32
isLeftPressed = False
isRightPressed = False
isUpPressed = False
isDownPressed = False
isExitPressed = False
isAPressed = False
running = True


font = pygame.font.Font('freesansbold.ttf', 32)

text_surface = font.render('GeeksForGeeks', True, GREEN, BLUE)
textRect = text_surface.get_rect()

# textRect = text.get_rect()
# textRect.center = (X // 2, Y // 1.3)




class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def toTuple(self):
        return (self.x, self.y, self.width, self.height)

    #           ---------- (x2+width,y2+height)
    # (x,y+height)        |
    #   -------------     |
    #  |        |    |    |
    #  |        -----|---- (x2+width2,y2)
    #  |    (x2,y2)  |
    #   -------------
    # (x,y)         (x+width,y)

    #  r: Rectangle =>
    def isOverlap(self, r):
        # print("hi")

        return self.x < r.x + r.width and self.x + self.width > r.x \
               and self.y < r.y + r.height and self.y + self.height > r.y

    # def touching(self, r

class Entity:
    def __init__(self, x, y, width, height):
        self.position = Vector(x, y)
        self.velocity = Vector(0, 0)
        self.collision = Rectangle(x, y, width, height)

    def draw(self, display):
        pygame.draw.rect(display, RED, self.collision.toTuple())

    def update(self):
        self.setPosition(self.position.x + self.velocity.x, self.position.y + self.velocity.y)
        # print("update entity")
        # print(self.position)
        # print(self.velocity)

    def undoLastMove(self):
        self.setPosition(self.position.x - self.velocity.x, self.position.y - self.velocity.y)

    def setPosition(self, x: float, y: float):
        self.position.x = x
        self.position.y = y
        self.collision.x = x
        self.collision.y = y

    def isOverlap(self, entity):
        return self.collision.isOverlap(entity.collision)


# class Controller:
#     def __init__(self):
#         self.keys = pygame.key.get_pressed()
#         self.isLeftPressed = False
#         self.isRightPressed = False
#         self.isUpPressed = False
#         self.isDownPressed = False
#         self.isExitPressed = False
#         self.isAPressed = False
#         #might need to delete this bottom line pygame.init()
#         pygame.init()
#
#     def is_pressed(self,key):
#         return self.keys[key]
#
#
#     def update(self):
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         self.isExitPressed = True
        #
        #
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT:
        #             self.isLeftPressed = True
        #         elif event.key == pygame.K_RIGHT:
        #             self.isRightPressed = True
        #         if event.key == pygame.K_UP:
        #             self.isUpPressed = True
        #         elif event.key == pygame.K_DOWN:
        #             self.isDownPressed = True
        #         #
        #         # elif event.key == pygame.K_a:
        #         #     if self.isAPressed == False:
        #         #         self.isAPressed = True
        #         #     else:
        #         #         if self.isAPressed == True:
        #         #             self.isAPressed = False
        #         if event.key == pygame.K_a:
        #             # If isAPressed is currently False, set it to True
        #             # Otherwise, set it to False
        #             self.isAPressed = not self.isAPressed
        #
        #             # if event.key == pygame.K_a:
        #             #     self.isAPressed = False
        #
        #
        #     elif event.type == pygame.KEYUP:
        #         if event.key == pygame.K_LEFT:
        #             self.isLeftPressed = False
        #         elif event.key == pygame.K_RIGHT:
        #             self.isRightPressed = False
        #         if event.key == pygame.K_UP:
        #             self.isUpPressed = False
        #         elif event.key == pygame.K_DOWN:
        #             self.isDownPressed = False
        #
        #



class Player(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.color = RED
        # self.controller = Controller()


    def draw(self, display):
        pygame.draw.rect(display, self.color, self.collision.toTuple())
        # if self.controller.isAPressed == True:
        #     display.blit(text_surface, textRect)

            # distance = math.sqrt((self.collision.x - self.npc.collision.x) ** 2 + (
            #         self.collision.y - self.npc.collision.y) ** 2)
            # # Check if distance is within the sum of the widths and heights of the rectangles
            # if 40 >= distance <= self.collision.width + self.collision.height + self.npc.collision.width + self.npc.collision.height:
            #     print("hey you how you do")



    # def speaking(self, player, npc):
    #     if npc.collision.x < player.collision.x:
    #         print("Nice")

    def update(self):
        self.controller.update()

        if self.controller.isExitPressed:
            global running
            running = False

        if self.controller.isLeftPressed:
            self.velocity.x = -4
        elif self.controller.isRightPressed:
            self.velocity.x = 4
        else:
            # hard stop
            # self.velocity.x = 0  # default velocity to zero unless key pressed
            # slow stop
            self.velocity.x *= 0.65 # gradually slow the x velocity down
            if abs(self.velocity.x) < 0.15: # if x velocity is close to zero, just set to zero
                self.velocity.x = 0


        if self.controller.isUpPressed:
            self.velocity.y = -4
        elif self.controller.isDownPressed:
            self.velocity.y = 4
        else:
            # hard stop
            # self.velocity.y = 0  # default velocity to zero unless key pressed
            # slow stop
            self.velocity.y *= 0.65 # gradually slow the y velocity down
            if abs(self.velocity.y) < 0.15: # if y velocity is close to zero, just set to zero
                self.velocity.y = 0

        # move player by velocity
        # note that if we have any collisions later we will undo the movements.
        # TODO test collision BEFORE moving
        self.setPosition(self.position.x + self.velocity.x, self.position.y + self.velocity.y)


class Npc(Entity):
    def __init__(self, x: int, y: int):
        super(Npc, self).__init__(x, y, 32, 32)

        self.color = BLUE
        self.speaking = False

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.collision.toTuple())
        # if self.player.controller.isAPressed == True:
        #     display.blit(text_surface, textRect)

    # def speaking(self,player):
    #     if player.collision.x < self.collision.x:
    #         print("Nice")


    def update(self):
        super().update()


class Obstacle(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 32, 32)
        self.color = GREEN

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.collision.toTuple())

    def update(self):
        super().update()


class Game:
    def __init__(self):
        self.player = Player(50, 100)
        self.npc = Npc(170, 170)

        self.obstacle = Obstacle(22, 22)


    def start(self):
        while running:

            # keys = pygame.key.get_pressed()
            #


            # for event in pygame.event.get():
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_a:
            #             display.blit(text, textRect)
            # collide = pygame.Rect.colliderect(self.player, self.Npc)
            #
            # if collide:
            #     self.player.velocity = 0


            # update entities and handle collision
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isExitPressed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.isLeftPressed = True
                    elif event.key == pygame.K_RIGHT:
                        self.isRightPressed = True
                    if event.key == pygame.K_UP:
                        self.isUpPressed = True
                    elif event.key == pygame.K_DOWN:
                        self.isDownPressed = True
                    #
                    # elif event.key == pygame.K_a:
                    #     if self.isAPressed == False:
                    #         self.isAPressed = True
                    #     else:
                    #         if self.isAPressed == True:
                    #             self.isAPressed = False
                    if event.key == pygame.K_a:
                        # If isAPressed is currently False, set it to True
                        # Otherwise, set it to False
                        self.isAPressed = not self.isAPressed

                        # if event.key == pygame.K_a:
                        #     self.isAPressed = False


                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.isLeftPressed = False
                        elif event.key == pygame.K_RIGHT:
                            self.isRightPressed = False
                        if event.key == pygame.K_UP:
                            self.isUpPressed = False
                        elif event.key == pygame.K_DOWN:
                            self.isDownPressed = False

            self.player.update()
            self.npc.update()
            self.obstacle.update()
            self.player.controller.update()
            # for event in pygame.event.get():
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_a:
            #             display.blit(text, textRect)


            if self.player.isOverlap(self.npc):

                self.player.undoLastMove()


            elif self.player.isOverlap(self.obstacle):
                self.player.undoLastMove()

            distance = math.sqrt((self.player.collision.x - self.npc.collision.x) ** 2 + (
                    self.player.collision.y - self.npc.collision.y) ** 2)
            # Check if distance is within the sum of the widths and heights of the rectangles
            if 40 >= distance <= self.player.collision.width + self.player.collision.height + self.npc.collision.width + self.npc.collision.height :
                if self.player.controller.isAPressed:
                    pygame.display.get_surface().blit(text_surface, (100, 100))
                    pygame.display.update()
                    # text_surface.blit(text_surface, (100, 100))
                    # pygame.display.update()


            display.fill(WHITE)

            self.player.draw(display)
            self.npc.draw(display)
            self.obstacle.draw(display)







            # update the screen
            # for event in pygame.event.get():
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_a:
            #             display.blit(text, textRect)
            pygame.display.update()

        # close Pygame when the game loop is finished
        pygame.quit()


game = Game()
game.start()