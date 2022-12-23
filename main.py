import math
import time
import random
from typing import *

import pygame



clock = pygame.time.Clock()

pygame.init()
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
WINDOWS_SIZE: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
DISPLAY: pygame.Surface = pygame.display.set_mode(WINDOWS_SIZE)
pygame.display.set_caption("Casino Man")
GREEN: Tuple[int, int, int] = (0, 255, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
BLUE: Tuple[int, int, int] = (0, 0, 255)
RED: Tuple[int, int, int] = (255, 0, 0)
PURPLE: Tuple[int, int, int] = (200, 0, 125)
TILE_SIZE: int = 32

# nextScreen = false

font = pygame.font.Font('freesansbold.ttf', 32)
text_surface = font.render('Casino', True, GREEN, BLUE)
speech_bubble = font.render('We"re adding here', True, GREEN, BLUE)
textRect = text_surface.get_rect()
speechRect = speech_bubble.get_rect()


def nowMilliseconds() -> int:
    return round(time.time() * 1000)


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

    def update(self, state: "GameState"):
        self.setPosition(self.position.x + self.velocity.x, self.position.y + self.velocity.y)

    def draw(self, state: "GameState"):
        pygame.draw.rect(DISPLAY, RED, self.collision.toTuple())

    def undoLastMove(self):
        self.setPosition(self.position.x - self.velocity.x, self.position.y - self.velocity.y)

    def setPosition(self, x: float, y: float):
        self.position.x = x
        self.position.y = y
        self.collision.x = x
        self.collision.y = y

    def isOverlap(self, entity: "Entity") -> bool:
        return self.collision.isOverlap(entity.collision)


# class Item:


class Controller:
    def __init__(self):
        self.isLeftPressed: bool = False
        self.isRightPressed: bool = False
        self.isUpPressed: bool = False
        self.isDownPressed: bool = False
        self.isExitPressed: bool = False
        self.isAPressed: bool = False
        self.isQPressed: bool = False
        self.isLPressed: bool = False
        self.isKPressed: bool = False
        self.isJPressed: bool = False
        self.keyPressedTimes: Dict[int, int] = {}  # Map<key number, key pressed millisecond
        self.keyReleasedTimes: Dict[int, int] = {}  # Map<key number, key pressed millisecond
        # might need to delete this bottom line pygame.init()
        pygame.init()

    def timeSinceKeyPressed(self, key: int):
        if key not in self.keyPressedTimes:
            return -1
        return nowMilliseconds() - self.keyPressedTimes[key]

    def timeSinceKeyReleased(self, key: int):
        if key not in self.keyReleasedTimes:
            return -1
        return nowMilliseconds() - self.keyReleasedTimes[key]

    def update(self, state: "GameState"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isExitPressed = True

            if event.type == pygame.KEYDOWN:
                self.keyPressedTimes[event.key] = nowMilliseconds()
                print(self.keyPressedTimes)

                if event.key == pygame.K_LEFT:
                    self.isLeftPressed = True
                elif event.key == pygame.K_RIGHT:
                    self.isRightPressed = True
                elif event.key == pygame.K_UP:
                    self.isUpPressed = True
                elif event.key == pygame.K_DOWN:
                    self.isDownPressed = True
                elif event.key == pygame.K_a:
                    self.isAPressed = True
                elif event.key == pygame.K_q:
                    self.isQPressed = True
                if event.key == pygame.K_j:
                    self.isJPressed = True




            elif event.type == pygame.KEYUP:
                self.keyReleasedTimes[event.key] = nowMilliseconds()
                # print(self.keyReleasedTimes)

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
                elif event.key == pygame.K_q:
                    self.isQPressed = False
                elif event.key == pygame.K_j:
                    self.isJPressed = False

            # elif state.currentScreen == state.coinFlipScreen:
            #
            #     if event.type == pygame.KEYDOWN:
            #         print("key pressed on coinflip screen")
            #         if event.key == pygame.K_j:
            #             self.isJPressed = True
            #
            #             self.low_bet = True
            #             self.med_bet = False
            #             self.high_bet = False
            #             print("you took the low bet")
            #
            #             # self.bet = 50
            #             self.bet_sequence = False
            #         elif event.key == pygame.K_k:
            #             self.isKPressed = True
            #
            #             self.low_bet = False
            #             self.med_bet = True
            #             self.high_bet = False
            #             print("you took the med bet")
            #
            #             # self.bet = 50
            #             self.bet_sequence = False
            #
            #         elif event.key == pygame.K_l:
            #             self.isLPressed = True
            #
            #             self.low_bet = False
            #             self.med_bet = False
            #             self.high_bet = True
            #             print("you took the high bet")
            #
            #             # self.bet = 50
            #             self.bet_sequence = False
            #
            #     elif event.type == pygame.KEYUP:
            #         if event.key == pygame.K_j:
            #             self.isJPressed = False
            #             self.bet_sequence = False
            #         elif event.key == pygame.K_k:
            #             self.isKPressed = False
            #             self.bet_sequence = False
            #         elif event.key == pygame.K_l:
            #             self.isLPressed = False
            #             self.bet_sequence = False


class Money(Entity):
    def __init__(self, total: int, x: float, y: float):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.total: int = total
        self.textSurface: pygame.Surface = font.render(str(total), True, GREEN, PURPLE)
        self.textRectangle: pygame.Rect = self.textSurface.get_rect()
        self.color: Tuple[int, int, int] = PURPLE

    def update(self, state: "GameState"):
        super().update(state)

    def draw(self, state: "GameState"):
        pygame.draw.rect(DISPLAY, self.color, self.collision.toTuple())

        pygame.display.get_surface().blit(self.textSurface, (self.position.x, self.position.y))

    def add(self, total: int):
        print("We're adding here")
        print(str(total))

        self.total += total
        self.textSurface = font.render(str(self.total), True, GREEN, PURPLE)

    #     # print(str(total))

    # def remove(self, total: int):
    #     self.total -= total

    def get_total(self) -> int:
        print(str(self.total))
        return self.total


class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.color: Tuple[int, int, int] = RED
        self.walkSpeed = 3.5
        # self.getMoney: bool = False

    # def speaking(self, player, npc):
    #     if npc.collision.x < player.collision.x:
    #         print("Nice")

    def update(self, state: "GameState"):
        controller = state.controller
        controller.update(state)

        canMove = not state.npc.isSpeaking

        if canMove:
            if controller.isLeftPressed:
                self.velocity.x = -self.walkSpeed
            elif controller.isRightPressed:
                self.velocity.x = self.walkSpeed
            else:
                # hard stop
                # self.velocity.x = 0  # default velocity to zero unless key pressed
                # slow stop
                self.velocity.x *= 0.65  # gradually slow the x velocity down
                if abs(self.velocity.x) < 0.15:  # if x velocity is close to zero, just set to zero
                    self.velocity.x = 0

            if controller.isUpPressed:
                self.velocity.y = -self.walkSpeed
            elif controller.isDownPressed:
                self.velocity.y = self.walkSpeed
            else:
                # hard stop
                # self.velocity.y = 0  # default velocity to zero unless key pressed
                # slow stop
                self.velocity.y *= 0.65  # gradually slow the y velocity down
                if abs(self.velocity.y) < 0.15:  # if y velocity is close to zero, just set to zero
                    self.velocity.y = 0

        else:  # if can not move, set velocity to zero
            self.velocity.x = 0
            self.velocity.y = 0

        # move player by velocity
        # note that if we have any collisions later we will undo the movements.
        # TODO test collision BEFORE moving
        self.setPosition(self.position.x + self.velocity.x, self.position.y + self.velocity.y)

        if self.isOverlap(state.npc) or self.isOverlap(state.obstacle) or self.isOutOfBounds():
            self.undoLastMove()

        if controller.isQPressed:
            state.currentScreen = state.coinFlipScreen
            state.coinFlipScreen.start(state)

        elif controller.isAPressed:
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            state.money.add(100)

    def isOutOfBounds(self) -> bool:
        return self.collision.x + self.collision.width > SCREEN_WIDTH or self.collision.x < 0 or self.collision.y + self.collision.height > SCREEN_HEIGHT or self.collision.y < 0

    def draw(self, state):
        pygame.draw.rect(DISPLAY, self.color, self.collision.toTuple())


class Npc(Entity):
    def __init__(self, x: int, y: int):
        super(Npc, self).__init__(x, y, 32, 32)
        self.color: Tuple[int, int, int] = BLUE
        self.speakStartTime: int = 0
        self.isSpeaking: bool = False

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

    def draw(self, state):
        pygame.draw.rect(DISPLAY, self.color, self.collision.toTuple())
        if self.isSpeaking:
            pygame.display.get_surface().blit(text_surface, (
                self.position.x + self.collision.width / 2, self.position.y - self.collision.height))


class Obstacle(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 32, 32)
        self.color: (int, int, int) = GREEN

    def update(self, state):
        super().update(state)

    def draw(self, state):
        pygame.draw.rect(DISPLAY, self.color, self.collision.toTuple())


class Screen:
    def __init__(self, screenName: str):
        self.screenName = screenName
        self.startedAt = nowMilliseconds()


    def start(self, state: "GameState"):
        self.startedAt = nowMilliseconds()

        pygame.display.set_caption(self.screenName)


    def update(self, state: "GameState"):
        pass

    def draw(self, state: "GameState"):
        pass


class MainScreen(Screen):
    def __init__(self):
        super().__init__("Casino MainScreen")

    def update(self, state: "GameState"):
        controller = state.controller
        player = state.player
        npc = state.npc
        obstacle = state.obstacle
        money = state.money
        controller.update(state)

        if controller.isExitPressed is True:
            state.isRunning = False

        player.update(state)
        npc.update(state)
        obstacle.update(state)
        money.update(state)

    def draw(self, state: "GameState"):
        DISPLAY.fill(WHITE)
        state.player.draw(state)
        state.npc.draw(state)
        state.obstacle.draw(state)
        state.money.draw(state)
        pygame.display.update()


class CoinFlipScreen(Screen):
    def __init__(self):
        super().__init__("Casino Coin flip  Screen")

        self.new_font = pygame.font.Font(None, 36)

        self.welcome_text = self.new_font.render(
            f"Welcome to Coin Flip! your bet is 50 SMACKERS.",
            True, (255, 255, 255))
        self.choose_bet_display = self.new_font.render("Enter your bet amount press j or k or l", True, (255, 255, 255))

        self.game_state = "welcome"


        self.balance = 0
        self.font = pygame.font.Font(None, 36)

        # Display the starting message
    def welcomeText(self, state: "GameState"):
        if self.game_state == "welcome":
            DISPLAY.fill((0, 0, 0))
            DISPLAY.blit(self.welcome_text, (10, 10))
            pygame.display.flip()

            # Transition to the choose bet state
            if state.controller.isJPressed == True:
                self.game_state = "choose_bet"
            else:
                pass

        elif self.game_state == "choose_bet":
            print("choose bet portion")
            DISPLAY.fill((0, 0, 0))
            DISPLAY.blit(self.choose_bet_display, (10, 10))
            pygame.display.flip()
            clock.tick(60)  # Limit the frame rate to 60 fps

    def flipCoin(self):
        # Generate a random number between 0 and 1 to simulate the coin flip
        coin = random.random()
        if coin < 0.5:
            return "heads"
        else:
            return "tails"

    def update(self, state: "GameState"):
        self.welcomeText(state)
        controller = state.controller
        player = state.player
        money = state.money
        controller.update(state)

        if controller.isAPressed is True:
            state.currentScreen = state.mainScreen
            state.currentScreen.start(state)

        if controller.isExitPressed is True:
            state.isRunning = False

        if controller.isJPressed is True:
            print("hi")

        player.update(state)
        money.update(state)

    def draw(self, state: "GameState"):
        print("white me")
        # DISPLAY.fill(WHITE)
        # state.money.draw(state)
        # pygame.display.update()


class TestScreen(Screen):
    def __init__(self):
        super().__init__("Casino Test Screen")

    def update(self, state: "GameState"):
        controller = state.controller
        player = state.player
        npc = state.npc
        obstacle = state.obstacle
        money = state.money
        controller.update(state)

        if controller.isExitPressed is True:
            state.isRunning = False

        player.update(state)
        npc.update(state)
        obstacle.update(state)
        money.update(state)

    def draw(self, state: "GameState"):
        DISPLAY.fill(GREEN)

        state.player.draw(state)
        state.npc.draw(state)
        state.obstacle.draw(state)
        state.money.draw(state)

        pygame.display.update()


class GameState:
    def __init__(self):
        self.controller: Controller = Controller()
        self.player: Player = Player(50, 100)
        self.money: Money = Money(23, 50, 50)
        self.npc: Npc = Npc(170, 170)
        self.obstacle: Obstacle = Obstacle(22, 22)
        self.isRunning: bool = True
        self.isPaused: bool = False

        self.mainScreen = MainScreen()
        self.testScreen = TestScreen()
        self.coinFlipScreen = CoinFlipScreen()
        self.currentScreen = self.mainScreen  # assign a value to currentScreen here


# old code, if q pressed:
# NO EXTRA LOGIC IN CONTROLLER CLASS
# state.money.add(20)
# coinFlipScreen = CoinFlipScreen() # defined in GameState
# from MainScreen, if we want to enter the coinFlipScreen, then:
# state.currentScreen = state.coinFlipScreen
# state.currentScreen.start()

class Game:
    def __init__(self):
        self.state = GameState()  # create a new GameState()

    def start(self):
        self.state.currentScreen.start(self.state)

        while self.state.isRunning:
            # will need to move this to Screen class

            self.state.currentScreen.update(self.state)
            self.state.currentScreen.draw(self.state)

        pygame.quit()


game = Game()
game.start()

# CoinFlipScreen().start()

