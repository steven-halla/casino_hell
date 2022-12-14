import pygame
from pygame.locals import *
import math
import keyboard
import time
from typing import *

clock = pygame.time.Clock()

pygame.init()
X: int = 400
Y: int = 400
WINDOWS_SIZE: Tuple[int, int] = (500, 500)
display = pygame.display.set_mode(WINDOWS_SIZE)
pygame.display.set_caption("Shooter4")
GREEN: Tuple[int, int, int] = (0, 255, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
BLUE: Tuple[int, int, int] = (0, 0, 255)
RED: Tuple[int, int, int] = (255, 0, 0)
PURPLE: Tuple[int, int, int] = (200, 0, 125)
TILE_SIZE: int = 32
running: bool = True


font = pygame.font.Font('freesansbold.ttf', 32)

text_surface = font.render('GeeksForGeeks', True, GREEN, BLUE)
textRect = text_surface.get_rect()

# textRect = text.get_rect()
# textRect.center = (X // 2, Y // 1.3)


class Vector:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def toTuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

    
    
class Rectangle:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height

    def toTuple(self) -> Tuple[float, float, float, float]:
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
    def isOverlap(self, r: "Rectangle") -> bool:
        # print("hi")

        return self.x < r.x + r.width and self.x + self.width > r.x \
               and self.y < r.y + r.height and self.y + self.height > r.y


class Entity:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.position: Vector = Vector(x, y)
        self.velocity: Vector = Vector(0, 0)
        self.collision: Rectangle = Rectangle(x, y, width, height)

    def draw(self, display, state):
        pygame.draw.rect(display, RED, self.collision.toTuple())

    def update(self, state):
        self.setPosition(self.position.x + self.velocity.x, self.position.y + self.velocity.y)

    def undoLastMove(self):
        self.setPosition(self.position.x - self.velocity.x, self.position.y - self.velocity.y)

    def setPosition(self, x: float, y: float):
        self.position.x = x
        self.position.y = y
        self.collision.x = x
        self.collision.y = y

    def isOverlap(self, entity: "Entity") -> bool:
        return self.collision.isOverlap(entity.collision)





class Controller:
    def __init__(self):
        self.keys: List[bool] = pygame.key.get_pressed()
        self.isLeftPressed: bool = False
        self.isRightPressed: bool = False
        self.isUpPressed: bool = False
        self.isDownPressed: bool = False
        self.isExitPressed: bool = False
        self.isAPressed: bool = False
        #might need to delete this bottom line pygame.init()
        pygame.init()

    def is_pressed(self, key) -> bool:
        return self.keys[key]


    def update(self, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isExitPressed = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.isLeftPressed = True
                    if state.npc.isSpeaking == True:
                        self.isLeftPressed = False
                elif event.key == pygame.K_RIGHT:
                    self.isRightPressed = True
                    if state.npc.isSpeaking == True:
                        self.isRightPressed = False
                elif event.key == pygame.K_UP:
                    self.isUpPressed = True
                    if state.npc.isSpeaking == True:
                        self.isUpPressed = False
                elif event.key == pygame.K_DOWN:
                    self.isDownPressed = True
                    if state.npc.isSpeaking == True:
                        self.isDownPressed = False
                elif event.key == pygame.K_a:
                    self.isAPressed = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.isLeftPressed = False
                elif event.key == pygame.K_RIGHT:
                    self.isRightPressed = False
                elif event.key == pygame.K_UP:
                    self.isUpPressed = False
                elif event.key == pygame.K_DOWN:
                    self.isDownPressed = False
                elif event.key == pygame.K_a:
                    self.isAPressed = False

                    
                    




class Money(Entity):
    def __init__(self, total: int, x: float, y: float):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.total: int = total
        self.textSurface: pygame.Surface = font.render(str(total), True, GREEN, PURPLE)
        self.textRectangle: pygame.Rect = self.textSurface.get_rect()
        self.color: Tuple[int, int, int] = PURPLE

    def update(self, state: List[int]):
        super().update(state)

    def draw(self, display: pygame.Surface, state):
        pygame.draw.rect(display, self.color, self.collision.toTuple())

        pygame.display.get_surface().blit(self.textSurface, (self.position.x, self.position.y))

    def add(self, total: int):
        self.total += total

    def remove(self, total: int):
        self.total -= total

    def get_total(self) -> int:
        return self.total



                    



class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.color = RED

    # def speaking(self, player, npc):
    #     if npc.collision.x < player.collision.x:
    #         print("Nice")

    def update(self, state):
        controller = state.controller
        controller.update(state)

        if controller.isLeftPressed:
            self.velocity.x = -4
        elif controller.isRightPressed:
            self.velocity.x = 4
        else:
            # hard stop
            # self.velocity.x = 0  # default velocity to zero unless key pressed
            # slow stop
            self.velocity.x *= 0.65 # gradually slow the x velocity down
            if abs(self.velocity.x) < 0.15: # if x velocity is close to zero, just set to zero
                self.velocity.x = 0


        if controller.isUpPressed:
            self.velocity.y = -4
        elif controller.isDownPressed:
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

    def draw(self, display:pygame.Surface, state):
        pygame.draw.rect(display, self.color, self.collision.toTuple())



class Npc(Entity):
    def __init__(self, x: int, y: int):
        super(Npc, self).__init__(x, y, 32, 32)
        self.color = BLUE
        self.speakStartTime = 0
        self.isSpeaking = False

    def update(self, state):
        super().update(state)

        player = state.player
        # print(time.process_time() - self.speakStartTime)
        if state.controller.isAPressed and (time.process_time() - self.speakStartTime) > 0.05:
            distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (player.collision.y - self.collision.y) ** 2)
            # Check if distance is within the sum of the widths and heights of the rectangles
            if 48 >= distance <= player.collision.width + player.collision.height + self.collision.width + self.collision.height:
                self.isSpeaking = not self.isSpeaking
                self.speakStartTime = time.process_time()

    def draw(self, display: pygame.Surface, state):
        pygame.draw.rect(display, self.color, self.collision.toTuple())
        if self.isSpeaking:
            pygame.display.get_surface().blit(text_surface, (
            self.position.x + self.collision.width / 2, self.position.y - self.collision.height))


class Obstacle(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 32, 32)
        self.color: (int, int, int) = GREEN

    def update(self, state):
        super().update(state)
        
    def draw(self, display: pygame.Surface, state):
        pygame.draw.rect(display, self.color, self.collision.toTuple())



class GameState:
    def __init__(self):
        self.controller: Controller = Controller()
        self.player: Player = Player(50, 100)
        self.money: Money = Money(25, 50,50)
        self.npc: NPC = Npc(170, 170)
        self.obstacle: Obstacle = Obstacle(22, 22)
        self.isRunning: bool = True
        self.isPaused: bool = False
        

class Game:
    def __init__(self):
        self.state = GameState() # create a new GameState()
        
    def start(self):
        state = self.state
        controller = state.controller
        player = state.player
        npc = state.npc
        obstacle = state.obstacle
        money = state.money
        
        while state.isRunning:
            controller.update(state)
            
            if controller.isExitPressed is True:
                state.isRunning = False

            player.update(state)
            npc.update(state)
            obstacle.update(state)
            money.update(state)

            if player.isOverlap(npc) or player.isOverlap(obstacle):
                player.undoLastMove()

            display.fill(WHITE)

            player.draw(display, state)
            npc.draw(display, state)
            obstacle.draw(display, state)
            money.draw(display, state)

            pygame.display.update()

        # close Pygame when the game loop is finished
        pygame.quit()


game = Game()
game.start()
