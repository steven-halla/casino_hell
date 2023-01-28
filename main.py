import math
import sys
import time
import random
from typing import *
import textwrap

import pytmx
# from pytmx.util_pygame import load_pygame



import pygame
from pygame import mixer

#Instantiate mixer
#this is where we get our music:
# https://soundimage.org/chiptunes-2/

from pygame.surface import Surface

clock = pygame.time.Clock()
FPS = 60
# might need to put this back in later to Deck class
player_cards_list = []
enemy_cards_list = []
pygame.init()
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
WINDOWS_SIZE: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
DISPLAY: pygame.Surface = pygame.display.set_mode(WINDOWS_SIZE)
pygame.display.set_caption("Casino Man")
GREEN: Tuple[int, int, int] = (0, 255, 0)
BLACK: Tuple[int, int, int] = (0,0,0)

WHITE: Tuple[int, int, int] = (255, 255, 255)
BLUE: Tuple[int, int, int] = (0, 0, 255)
RED: Tuple[int, int, int] = (255, 0, 0)
PURPLE: Tuple[int, int, int] = (200, 0, 125)
TILE_SIZE: int = 16

# nextScreen = false


font = pygame.font.Font('freesansbold.ttf', 24)
text_surface = font.render('Casino', True, GREEN, BLUE)
speech_bubble = font.render('We"re adding here', True, GREEN, BLUE)
textRect = text_surface.get_rect()
speechRect = speech_bubble.get_rect()


wrap_width = 200



# pygame.time.get_ticks()
# def nowMilliseconds() -> int:
#     return round(time.time() * 1000)


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
        # self.rect = pygame.Rect(x, y, width, height)

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
        self.isRPressed: bool = False
        self.isEPressed: bool = False
        self.isWPressed: bool = False
        self.is1Pressed: bool = False
        self.isTPressed: bool = False
        self.isPPressed: bool = False
        self.isOPressed: bool = False
        self.is1Pressed: bool = False
        self.isBPressed: bool = False
        self.keyPressedTimes: Dict[int, int] = {}  # Map<key number, key pressed millisecond
        self.keyReleasedTimes: Dict[int, int] = {}  # Map<key number, key pressed millisecond
        # might need to delete this bottom line pygame.init()
        pygame.init()

    def timeSinceKeyPressed(self, key: int):
        if key not in self.keyPressedTimes:
            return -1
        return pygame.time.get_ticks() - self.keyPressedTimes[key]

    def timeSinceKeyReleased(self, key: int):
        if key not in self.keyReleasedTimes:
            return -1
        return pygame.time.get_ticks() - self.keyReleasedTimes[key]

    def update(self, state: "GameState"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isExitPressed = True

            if event.type == pygame.KEYDOWN:
                self.keyPressedTimes[event.key] = pygame.time.get_ticks()
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
                elif event.key == pygame.K_j:
                    self.isJPressed = True
                elif event.key == pygame.K_k:
                    self.isKPressed = True
                elif event.key == pygame.K_l:
                    self.isLPressed = True
                elif event.key == pygame.K_r:
                    self.isRPressed = True
                elif event.key == pygame.K_e:
                    self.isEPressed = True
                elif event.key == pygame.K_t:
                    self.isTPressed = True
                elif event.key == pygame.K_w:
                    self.isWPressed = True
                elif event.key == pygame.K_1:
                    self.is1Pressed = True
                elif event.key == pygame.K_p:
                    self.isPPressed = True
                elif event.key == pygame.K_o:
                    self.isOPressed = True
                elif event.key == pygame.K_1:
                    self.is1Pressed = True
                elif event.key == pygame.K_b:
                    self.isBPressed = True


            elif event.type == pygame.KEYUP:
                self.keyReleasedTimes[event.key] = pygame.time.get_ticks()
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
                elif event.key == pygame.K_k:
                    self.isKPressed = False
                elif event.key == pygame.K_l:
                    self.isLPressed = False
                elif event.key == pygame.K_r:
                    self.isRPressed = False
                elif event.key == pygame.K_e:
                    self.isEPressed = False
                elif event.key == pygame.K_t:
                    self.isTPressed = False
                elif event.key == pygame.K_w:
                    self.isWPressed = False
                elif event.key == pygame.K_1:
                    self.is1Pressed = False
                elif event.key == pygame.K_p:
                    self.isPPressed = False
                elif event.key == pygame.K_o:
                    self.isOPressed = False
                elif event.key == pygame.K_1:
                    self.is1Pressed = False
                elif event.key == pygame.K_b:
                    self.isBPressed = False

class Dice:
    def __init__(self, sides: int):
        self.sides = sides
        self.rolls = []
        self.one_hundred_rolls = [0]
    #rename roll method to roll 2d6 method
    def roll_two_d_six(self) -> List[int]:
        self.sides = 6
        roll1 = random.randint(1, self.sides)
        roll2 = random.randint(1, self.sides)
        # roll1 = 1
        # roll2 = 1

        self.rolls = [roll1, roll2]
        print(self.rolls)
        return self.rolls


    def roll_one_d_hundred(self) -> List[int]:
        self.sides = 76

        roll1 = random.randint(1, self.sides)
        self.one_hundred_rolls = [roll1 + 24]
        return self.one_hundred_rolls


    def add(self):
        # print(str(self.rolls))
        return self.rolls[0] + self.rolls[1]



class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.color: Tuple[int, int, int] = RED
        self.walkSpeed = 3.5
        self.playerMoney = 5000
        self.image = pygame.image.load("/Users/steven/code/games/casino/casino_sprites/Boss.png")
        self.stamina_points = 100
        self.focus_points = 50
        self.exp = 0
        self.level = 1
        self.health = 0
        self.intelligence = 0
        self.charisma = 0
        self.luck = 0
        self.perception = 0


    def update(self, state: "GameState"):
        controller = state.controller
        controller.update(state)
        if self.exp > 1000:
            self.level = 2

        if self.exp >= 3000:
            self.level = 3
            print(self.exp)
            if self.exp > 3000:
                self.exp = 3000


        # Define canMove before the for loop
        canMove = True
        for npc in state.npcs:
            if npc.isSpeaking:
                canMove = False
                break

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

        # if self.isOverlap(state.npc) or self.isOverlap(state.obstacle) or self.isOutOfBounds():
        #     self.undoLastMove()
        if self.isOverlap(state.obstacle) or self.isOutOfBounds():
            self.undoLastMove()

        for npc in state.npcs:
            if self.collision.isOverlap(npc.collision):
                self.undoLastMove()




        if controller.isQPressed:
            state.currentScreen = state.coinFlipScreen
            state.coinFlipScreen.start(state)

        elif controller.isPPressed:
            state.currentScreen = state.opossumInACanScreen
            state.opossumInACanScreen.start(state)


        elif controller.isAPressed:

            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)

    def isOutOfBounds(self) -> bool:
        return self.collision.x + self.collision.width > SCREEN_WIDTH or self.collision.x < 0 or self.collision.y + self.collision.height > SCREEN_HEIGHT or self.collision.y < 0

    def draw(self, state):
        # Get the current dimensions of the image
        original_width, original_height = self.image.get_size()

        # Calculate the new dimensions of the image
        new_width = original_width * 1.7
        new_height = original_height * 1.7

        # Scale the image
        scaled_image = pygame.transform.scale(self.image, (new_width, new_height))

        # Calculate the center of the image
        image_center_x = new_width // 2
        image_center_y = new_height // 2

        # Define an offset that will be used to draw the image at the center of the player
        offset_x = self.collision.x + self.collision.width // 2 - image_center_x
        offset_y = self.collision.y + self.collision.height // 2 - image_center_y

        # Draw the image on the display surface
        DISPLAY.blit(scaled_image, (offset_x, offset_y))


class Npc(Entity):
    def __init__(self, x: int, y: int):
        super(Npc, self).__init__(x, y, 16, 16)
        self.color: Tuple[int, int, int] = BLUE
        self.speakStartTime: int = 0
        self.isSpeaking: bool = False

    def update(self, state):
        super().update(state)

        player = state.player
        # print(time.process_time() - self.speakStartTime)
        if state.controller.isAPressed and (time.process_time() - self.speakStartTime) > .20:
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


class CoinFlipExplanationGuy(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.current_message_index = -1
        self.messages = ["Hi there I'm the coin flip guy. ", "I'm here to tell you about the coinflip game", "You get 3 kinds of bets: High, Medium, and Low.", "Set your own pace for this game.Play it safe or bet big.", "Was my explanation  boring?", " If you think that was boring, wait till you play coin flip!", "Since you stuck around this long I'll give you a tip:", "Coin flip fred is using a weighted coin,"," not sure which side he favors", "If you give me a sandwhich It might jar my memory"]
        self.message = font.render(self.messages[self.current_message_index], True, GREEN, BLUE)
        self.start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_delay = 500  # input delay in milliseconds
        self.input_time = 0  # time when input was last read

    def update(self, state):
        super().update(state)

        # Get the current time in milliseconds
        current_time = pygame.time.get_ticks()

        # If the T key is pressed and the input delay has passed
        if self.isSpeaking and state.controller.isAPressed and current_time - self.input_time >= self.input_delay:

            self.input_time = current_time  # update the input time

            # Update the current message
            self.current_message_index += 1
            if self.current_message_index >= len(self.messages):
                self.current_message_index = 0
            self.message = font.render(self.messages[self.current_message_index], True, GREEN, BLUE)

    def draw(self, state):
        pygame.draw.rect(DISPLAY, self.color, self.collision.toTuple())

        # Display the current message if self.isSpeaking is True
        if self.isSpeaking:
            message = pygame.display.get_surface().blit(self.message, (10,10))



class CoinFlipFred(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.current_message_index = -1
        self.messages = ["You need at least 50 Hell coins to play","Did you hear I use a weighted coin? It's a lie. ", "Press the T key in order to start a battle with me."]
        self.message = font.render(self.messages[self.current_message_index], True, GREEN, BLUE)
        self.start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_delay = 500  # input delay in milliseconds
        self.input_time = 0  # time when input was last read


    def update(self, state):
        super().update(state)
        distance = math.sqrt(
            (state.player.collision.x - self.collision.x) ** 2 + (state.player.collision.y - self.collision.y) ** 2)

        # Get the current time in milliseconds
        current_time = pygame.time.get_ticks()

        # If the T key is pressed and the input delay has passed
        if self.isSpeaking and state.controller.isAPressed and current_time - self.input_time >= self.input_delay:

            self.input_time = current_time  # update the input time

            # Update the current message
            self.current_message_index += 1
            if self.current_message_index >= len(self.messages):
                self.current_message_index = 0
            self.message = font.render(self.messages[self.current_message_index], True, GREEN, BLUE)

        elif 48 >= distance <= state.player.collision.width + state.player.collision.height + self.collision.width + self.collision.height and state.controller.isTPressed and current_time - self.input_time >= self.input_delay and state.coinFlipScreen.coinFlipFredMoney > 0:
            state.currentScreen = state.coinFlipScreen
            state.coinFlipScreen.start(state)
        elif state.coinFlipScreen.coinFlipFredMoney <= 0:
            print("coin flip freddy is defeated already move on you vulture")

    def draw(self, state):
        pygame.draw.rect(DISPLAY, self.color, self.collision.toTuple())

        # Display the current message if self.isSpeaking is True
        if self.isSpeaking:
            message = pygame.display.get_surface().blit(self.message, (10,10))


class SalleyOpossum(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.current_message_index = -1
        self.messages = ["Are you sure you want to play opossum in a can?.","My opossums have Rabies that'll wear down your stamina","Press T to start the game", "Unlike Coinflip Freddy , I work for the boss", "so If I go below 0, he will cover the winnings"]
        self.message = font.render(self.messages[self.current_message_index], True, GREEN, BLUE)
        self.start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_delay = 500  # input delay in milliseconds
        self.input_time = 0  # time when input was last read
        self.sallyOpossumMoney = 1000

    def update(self, state):
        super().update(state)
        distance = math.sqrt(
            (state.player.collision.x - self.collision.x) ** 2 + (state.player.collision.y - self.collision.y) ** 2)

        # Get the current time in milliseconds
        current_time = pygame.time.get_ticks()

        # If the T key is pressed and the input delay has passed
        if self.isSpeaking and state.controller.isAPressed and current_time - self.input_time >= self.input_delay:

            self.input_time = current_time  # update the input time

            # Update the current message
            self.current_message_index += 1
            if self.current_message_index >= len(self.messages):
                self.current_message_index = 0
            self.message = font.render(self.messages[self.current_message_index], True, GREEN, BLUE)

        elif 48 >= distance <= state.player.collision.width + state.player.collision.height + self.collision.width + self.collision.height and state.controller.isTPressed and current_time - self.input_time >= self.input_delay and state.player.playerMoney > 319 and state.opossumInACanScreen.sallyOpossumMoney > 0:
            state.player.playerMoney -= 220
            state.currentScreen = state.opossumInACanScreen
            state.opossumInACanScreen.start(state)
        elif state.opossumInACanScreen.sallyOpossumMoney <= 0:
            print("Sally Opossum is defeated already move on you vulture")

    def draw(self, state):
        pygame.draw.rect(DISPLAY, self.color, self.collision.toTuple())

        # Display the current message if self.isSpeaking is True
        if self.isSpeaking:
            message = pygame.display.get_surface().blit(self.message, (10,10))



class OposumInACanExplainGirl(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.current_message_index = -1
        self.messages = ["Hi there I'm the Opossum in a can  girl. ", "I'm here to tell you all about Opposum in a can", "which some refer to it as 'devil roulette'." , "There are 5 win cans and  3 opossum cans.", "You'll need to put down 300 ante for your insurance ",
                         "If you get an X3 star you triple your next bet", "if you get an lucky star you double your insurance", "if you get an rabid Opossum, that is red" , "you lose everything",
                         "The blue opossums, which also have rabies", " eat your insurance. Get two blues and its gameover","you can leave the match anytime and", " keep your current winnings, or go big for the jackpot.","We load the opossum cans in the can shaker.", "That way they are nice and angry when you are unlucky.","are there any Opossums down here without rabies?", " I don't think so?"]
        self.message = font.render(self.messages[self.current_message_index], True, GREEN, BLUE)
        self.start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_delay = 500  # input delay in milliseconds
        self.input_time = 0  # time when input was last read

    def update(self, state):
        super().update(state)

        # Get the current time in milliseconds
        current_time = pygame.time.get_ticks()

        # If the T key is pressed and the input delay has passed
        if self.isSpeaking and state.controller.isAPressed and current_time - self.input_time >= self.input_delay:

            self.input_time = current_time  # update the input time

            # Update the current message
            self.current_message_index += 1
            if self.current_message_index >= len(self.messages):
                self.current_message_index = 0
            self.message = font.render(self.messages[self.current_message_index], True, GREEN, BLUE)

    def draw(self, state):
        pygame.draw.rect(DISPLAY, self.color, self.collision.toTuple())

        # Display the current message if self.isSpeaking is True
        if self.isSpeaking:
            message = pygame.display.get_surface().blit(self.message, (10,10))

class ChiliWilley(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.current_message_index = -1
        self.messages = ["It's a 1000 coin bet I hope your ready to lose.","I wont take it easy on you.","You'll end up just like the others.", "I'm the boss of this level you better run away", "I'm the boss for a reason, you better get ready for a fight!"]
        self.message = font.render(self.messages[self.current_message_index], True, GREEN, BLUE)
        self.start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_delay = 500  # input delay in milliseconds
        self.input_time = 0  # time when input was last read

    def update(self, state):
        super().update(state)
        distance = math.sqrt(
            (state.player.collision.x - self.collision.x) ** 2 + (state.player.collision.y - self.collision.y) ** 2)

        # Get the current time in milliseconds
        current_time = pygame.time.get_ticks()

        # If the T key is pressed and the input delay has passed
        if self.isSpeaking and state.controller.isAPressed and current_time - self.input_time >= self.input_delay:

            self.input_time = current_time  # update the input time

            # Update the current message
            self.current_message_index += 1
            if self.current_message_index >= len(self.messages):
                self.current_message_index = 0
            self.message = font.render(self.messages[self.current_message_index], True, GREEN, BLUE)

        elif 48 >= distance <= state.player.collision.width + state.player.collision.height + self.collision.width + self.collision.height and state.controller.isTPressed and current_time - self.input_time >= self.input_delay and state.player.playerMoney >= 500 and state.diceGameScreen.chiliWilleyMoney > 0:
            state.currentScreen = state.diceGameScreen
            state.diceGameScreen.start(state)

        elif state.diceGameScreen.chiliWilleyMoney <= 0:
            print("Chilli Willey is defeated already move on you vulture")

    def draw(self, state):
        pygame.draw.rect(DISPLAY, self.color, self.collision.toTuple())

        # Display the current message if self.isSpeaking is True
        if self.isSpeaking:
            message = pygame.display.get_surface().blit(self.message, (10,10))



class NuclearAnnilationGeneralExplainGuy(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.current_message_index = -1
        self.messages = ["I'm the general, so show me some respect. ", "I'm here to tell you all about my favorite game: Nuke em.", "Wait what, you want me to actually explain the rules?" , "I'm the general I'm too busy for that, read the Docs.", "In the future we'll have a tear sheet for you to look at.",
                         "The game is currently in medical.", "Once it's all patched up it'll be released."]
        self.message = font.render(self.messages[self.current_message_index], True, GREEN, BLUE)
        self.start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_delay = 500  # input delay in milliseconds
        self.input_time = 0  # time when input was last read

    def update(self, state):
        super().update(state)

        # Get the current time in milliseconds
        current_time = pygame.time.get_ticks()

        # If the T key is pressed and the input delay has passed
        if self.isSpeaking and state.controller.isAPressed and current_time - self.input_time >= self.input_delay:

            self.input_time = current_time  # update the input time

            # Update the current message
            self.current_message_index += 1
            if self.current_message_index >= len(self.messages):
                self.current_message_index = 0
            self.message = font.render(self.messages[self.current_message_index], True, GREEN, BLUE)

    def draw(self, state):
        pygame.draw.rect(DISPLAY, self.color, self.collision.toTuple())

        # Display the current message if self.isSpeaking is True
        if self.isSpeaking:
            message = pygame.display.get_surface().blit(self.message, (10,10))




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
        self.startedAt = pygame.time.get_ticks()


    def start(self, state: "GameState"):
        self.startedAt = pygame.time.get_ticks()

        pygame.display.set_caption(self.screenName)


    def update(self, state: "GameState"):
        pass

    def draw(self, state: "GameState"):
        pass

class MainScreen(Screen):
    def __init__(self):
        super().__init__("Casino MainScreen")
        # Load the Tiled map file
        self.tiled_map = pytmx.load_pygame("/Users/steven/code/games/casino/casino_sprites/beta_floor1_casino.tmx")

    def update(self, state: "GameState"):
        controller = state.controller
        player = state.player
        npc = state.npcs
        obstacle = state.obstacle
        controller.update(state)

        if controller.isExitPressed is True:
            state.isRunning = False

        player.update(state)
        # npc.update(state)
        for npc in state.npcs:
            npc.update(state)
        obstacle.update(state)

    def draw(self, state: "GameState"):
        # Clear the screen
        DISPLAY.fill(WHITE)
        # Draw the player money
        DISPLAY.blit(font.render(
            f" player Money: {state.player.playerMoney}",
            True, (5, 5, 5)), (10, 10))

        for npc in state.npcs:
            npc.draw(state)

        # Check if the Tiled map has any layers
        if self.tiled_map.layers:
            # Get the size of a single tile in pixels
            tile_width = self.tiled_map.tilewidth
            tile_height = self.tiled_map.tileheight

            # Iterate over the tiles in the first layer
            for x, y, image in self.tiled_map.layers[0].tiles():
                # Calculate the position of the tile in pixels
                pos_x = x * tile_width
                pos_y = y * tile_height

                scaled_image = pygame.transform.scale(image, (tile_width * 1.3, tile_height * 1.3))

                # Blit the tile image to the screen at the correct position
                DISPLAY.blit(scaled_image, (pos_x, pos_y))

            for x, y, image in self.tiled_map.layers[1].tiles():
                # Calculate the position of the tile in pixels
                pos_x = x * tile_width
                pos_y = y * tile_height
                scaled_image = pygame.transform.scale(scaled_image, (tile_width * 1.3, tile_height * 1.3))

                tile_rect = Rectangle(pos_x, pos_y, tile_width, tile_height)

                if state.player.collision.isOverlap(tile_rect):
                    state.player.undoLastMove()

                # Blit the tile image to the screen at the correct position
                DISPLAY.blit(image, (pos_x, pos_y))

        # Draw the player, NPCs, and obstacles
        state.player.draw(state)
        # state.npc.draw(state)

        state.obstacle.draw(state)
        # Update the display
        pygame.display.update()

class CoinFlipTedScreen(Screen):
    def __init__(self):
        super().__init__("Casino Coin flip  Screen")

        self.result = ""
        self.play_again = True
        self.players_side = ""
        self.new_font = pygame.font.Font(None, 36)
        self.message_display = ""
        self.second_message_display = ""
        self.third_message_display = ""
        self.magic_player_message_display = ""
        self.magic_enemy_message_display = ""
        self.choices = ["Heads", "Tails", "Magic"]
        self.yes_or_no_menu = ["Yes", "No"]
        self.magic_menu_selector = ["Bluff", "Reveal", "Lucky", "Back"]
        self.game_state = "welcome_screen"
        self.choice_sequence = True
        self.bet = 0
        self.font = pygame.font.Font(None, 36)
        self.coinFlipSandyMoney = 700
        self.coinFlipSandyDefeated = False
        self.current_index = 0
        self.yes_no_current_index = 0
        self.magic_menu_index = 0
        self.leave_or_replay_index = 0
        self.high_exp = False
        self.low_exp = False

        self.bluff_text_list = ["I bet you triple my bet that your coin will land on tails 3 times in a row","Hehehe, your on sucker"]
        self.luck_activated = 0
        self.sandy_focus_points = 30
        self.reveal_hand = False
        self.cheating_alert = False

    def giveExp(self, state: "GameState"):
        if state.player.level == 1:
            if self.high_exp == True:
                state.player.exp += 15
            elif self.low_exp == True:
                state.player.exp += 50
        elif state.player.level == 2:
            if self.high_exp == True:
                state.player.exp += 5
            elif self.low_exp == True:
                state.player.exp += 15
        else:
            print("your level is too high no exp for you")





    def place_bet(self, state: "GameState"):
        controller = state.controller
        controller.update(state)

        if controller.isUpPressed:
            self.bet += 10
            pygame.time.delay(200)
            self.isUpPressed = False

        elif controller.isDownPressed:
            self.bet -= 10
            pygame.time.delay(200)
            self.isDownPressed = False

        if self.bet < 10:
            self.bet = 10

        if self.bet > 100:
            self.bet = 100


    def flipCoin(self):
        # currently at .6 because heads is favored
        # in the future will have states to handle coin flip percentages
        # an item can add .1 to your rolls for heads, or -.1 for tails
        coin = random.random()
        if coin < 0.5:
            print("coin landed on heads")
            self.result = "heads"
        else:
            print("coin landed on tails")
            self.result = "tails"

    def cheatCoin(self):
        coin=random.random()
        if coin < 0.3:
            print("coin landed on heads")
            self.result = "heads"
        else:
            print("coin landed on tails")
            self.result = "tails"

    def update(self, state: "GameState"):
        if self.coinFlipSandyMoney <= 0:
            self.coinFlipSandyDefeated = True
        # Update the controller
        controller = state.controller
        controller.update(state)

        if state.player.stamina_points < 3:
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)

        if self.game_state == "welcome_screen" :

            self.message_display = "This is the welcome screen. Press R to continue"
            self.second_message_display = ""
            self.third_message_display = ""
            self.reveal_hand = False

            if controller.isRPressed:
                state.player.stamina_points -= 3

                self.game_state = "bet_screen"

        elif self.game_state == "bet_screen":
            self.message_display = "This is the bet screen. Press up and down to change your bet."
            self.second_message_display = "When you are ready press T to continue."
            controller = state.controller
            self.place_bet(state)
            if controller.isTPressed:
                print("t pressed")
                self.game_state = "coin_flip_time"


        elif self.game_state == "coin_flip_time":
            self.message_display = "I'm flipping the coin now."
            pygame.time.delay(500)
            if self.bet < 80:
                self.flipCoin()
                self.game_state = "choose_heads_or_tails_message"
            elif self.bet > 70:
                self.cheatCoin()
                self.game_state = "choose_heads_or_tails_message"






        elif self.game_state == "choose_heads_or_tails_message":
            self.message_display = "Now Choose heads or tails. Make your choice"
            if controller.isUpPressed:
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) - 1
                else:
                    self.current_index -= 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) + 1
                else:
                    self.current_index += 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isDownPressed = False


            if self.current_index == 0:
                if controller.isTPressed:
                    self.players_side = "heads"
                    self.game_state = "results_screen"

            elif self.current_index == 1:
                if controller.isTPressed:
                    self.players_side = "tails"
                    self.game_state = "results_screen"


            elif self.current_index == 2:
                if controller.isTPressed:
                    print("This is how you pick magic")
                    self.game_state = "magic_menu"



#534534543535353525532535353354

        elif self.game_state == "magic_menu":
            self.message_display = "Pick a magic spell and wreck havic. Press K to cast"

            if controller.isUpPressed:
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) - 1
                else:
                    self.magic_menu_index -= 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) + 1
                else:
                    self.magic_menu_index += 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isDownPressed = False


            if self.magic_menu_index == 0:
                if controller.isKPressed:
                    if self.luck_activated < 1 and self.reveal_hand == False:
                        if state.player.focus_points >= 10:
                            state.player.focus_points -= 10

                            print("You cast bluff")
                            self.game_state = "bluff_state"

                        else:
                            self.third_message_display = "Sorry but you dont have enough focus points to cast"
                    elif self.luck_activated > 0 or self.reveal_hand == True:
                        self.third_message_display = "sorry but you can't stack magic spells"


            elif self.magic_menu_index == 1:
                if controller.isKPressed:
                    if self.luck_activated < 1:
                        print("You cast reveal")
                        if controller.isKPressed:
                            if state.player.focus_points >= 10:
                                state.player.focus_points -= 10
                                self.reveal_hand = True

                                print("You cast bluff")
                                self.game_state = "reveal_state"

                            elif state.player.focus_points < 10:
                                self.third_message_display = "Sorry but you dont have enough focus points to cast"
                    elif self.luck_activated > 0:
                        self.third_message_display = "sorry but you can't stack magic spells"





##########################have a message state reserved for buff states

            ##### boss enemies will use magic under more strict conditions
            elif self.magic_menu_index == 2:
                if controller.isKPressed:
                    print("you cast avatar of luck")
                    self.third_message_display = "Your luck is now increased for 3 losses"
                    self.luck_activated = 3
                    state.player.focus_points -= 20
                    self.game_state = "choose_heads_or_tails_message"


            elif self.magic_menu_index == 3:
                if controller.isKPressed:
                    print("going back")
                    self.game_state = "choose_heads_or_tails_message"

        elif self.game_state == "reveal_state":
            self.message_display = "time to reveal your coin"
            self.third_message_display = f"The coin will be on the {self.result}"
            if state.controller.isAPressed:
                self.game_state = "choose_heads_or_tails_message"
                state.controller.isAPressed = False




        elif self.game_state == "bluff_state":
            self.message_display = "Triple my bet that tails will land 3 times in a  row."
            bluffalo = random.random()

            if bluffalo < 0.7:
                print("you win tripple bet")
                state.player.playerMoney += self.bet * 3
                self.game_state = "welcome_screen"


            else:
                print("your bet lost")
                state.player.playerMoney -= self.bet
                self.game_state = "welcome_screen"






        elif self.game_state == "results_screen":
            self.second_message_display = " "
            if self.result == self.players_side:
                # self.third_message_display = "You won"
                state.player.playerMoney += self.bet
                self.coinFlipSandyMoney -= self.bet
                pygame.time.delay(1000)

                self.game_state = "you_won_the_toss"

                if self.coinFlipSandyMoney <= 0 or state.player.playerMoney <= 0:
                    print("At 0 ending match")
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)





            elif self.result != self.players_side:
                if self.luck_activated > 0:
                    lucky_draw = random.random()
                    if lucky_draw < 0.9:
                        self.third_message_display = f"Your feeling lucky.{self.luck_activated}remains. Push A"

                        if controller.isAPressed:
                            self.luck_activated -= 1
                            state.player.playerMoney += self.bet
                            self.coinFlipSandyMoney -= self.bet
                            self.result = self.players_side

                            self.game_state = "you_won_the_toss"
                    else:
                        # self.third_message_display = f"Your luck didn't pan out.{self.luck_activated}remains. Push A"
                        if controller.isAPressed:
                            self.luck_activated -= 1

                            state.player.playerMoney -= self.bet
                            self.coinFlipSandyMoney += self.bet

                            self.game_state = "you_lost_the_toss"

                elif self.luck_activated == 0:
                    pygame.time.delay(500)
                    state.player.playerMoney -= self.bet
                    self.coinFlipSandyMoney += self.bet

                    self.game_state = "you_lost_the_toss"











        elif self.game_state == "you_won_the_toss" :
            self.message_display = f"choice  {self.players_side} coin landed  {self.result} You WON"
            self.second_message_display = f"Play again? Press T on your choice"

            if self.coinFlipSandyMoney <= 0 or state.player.playerMoney <= 0:
                print("At 0 ending match")
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)





            elif controller.isUpPressed:
                if not hasattr(self, "leave_or_replay_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) - 1
                else:
                    self.leave_or_replay_index -= 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "yes_no_current_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) + 1
                else:
                    self.leave_or_replay_index += 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isDownPressed = False

            if self.leave_or_replay_index == 0:
                if controller.isTPressed:
                    self.game_state = "welcome_screen"

            elif self.leave_or_replay_index == 1:
                if controller.isTPressed:
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)



        elif self.game_state == "you_lost_the_toss" :

            self.message_display = f"choice  {self.players_side} coin landed  {self.result} lost! "
            self.second_message_display = f"Play again?Yes to continue and No to exi. Press T on your choice"
            if self.coinFlipSandyMoney <= 0 or state.player.playerMoney <= 0:
                print("At 0 ending match")
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)




            elif controller.isUpPressed:
                if not hasattr(self, "leave_or_replay_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) - 1
                else:
                    self.leave_or_replay_index -= 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "yes_no_current_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) + 1
                else:
                    self.leave_or_replay_index += 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isDownPressed = False

            if self.leave_or_replay_index == 0:
                if controller.isTPressed:
                    self.game_state = "welcome_screen"

            elif self.leave_or_replay_index == 1:
                if controller.isTPressed:
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)







    ########################we want up and down arrows on bet. have arrow disapear when an item is not in use

    def draw(self, state: "GameState"):
        # Fill the screen with a solid color
        DISPLAY.fill((0, 0, 0))

        DISPLAY.blit(self.new_font.render(
            f" CoinFlipSandysMoney: {self.coinFlipSandyMoney}",
            True, (255, 255, 255)), (10, 150))
        DISPLAY.blit(self.new_font.render(
            f" player Money: {state.player.playerMoney}",
            True, (255, 255, 255)), (10, 190))

        # Draw the welcome message or choose bet message based on the game state

        DISPLAY.blit(self.font.render(f"{self.message_display}", True, (255, 255, 255)), (10, 10))
        DISPLAY.blit(self.font.render(f"{self.second_message_display}", True, (255, 255, 255)), (10, 50))
        DISPLAY.blit(self.font.render(f"{self.third_message_display}", True, (255, 255, 255)), (10, 230))
        DISPLAY.blit(self.font.render(f"Your current bet is:{self.bet}", True, (255, 255, 255)), (10, 260))
        DISPLAY.blit(self.font.render(f"player health:{state.player.stamina_points}", True, (255, 255, 255)), (10, 290))
        DISPLAY.blit(self.font.render(f"player magic:{state.player.focus_points}", True, (255, 255, 255)), (10, 320))

        if self.game_state == "magic_menu" :
            if self.magic_menu_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.magic_menu_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))




            elif self.magic_menu_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 255))

            elif self.magic_menu_index == 3:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 305))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[1]}", True, (255, 255, 255)),
                (700, 210))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[2]}", True, (255, 255, 255)),
                (700, 260))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[3]}", True, (255, 255, 255)),
                (700, 310))

        elif self.game_state != "you_won_the_toss" and self.game_state != "you_lost_the_toss":
            DISPLAY.blit(
                self.font.render(f"{self.choices[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.choices[1]}", True, (255, 255, 255)),
                (700, 210))

            DISPLAY.blit(
                self.font.render(f"{self.choices[2]}", True, (255, 255, 255)),
                (700, 260))


        if self.game_state == "bet_screen":

            DISPLAY.blit(self.font.render(f"^", True, (255, 255, 255)), (240, 235))
            DISPLAY.blit(self.font.render(f"v", True, (255, 255, 255)), (240, 288))


        elif self.game_state == "choose_heads_or_tails_message":

            if self.current_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.current_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))




            elif self.current_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 255))

        elif self.game_state == "you_won_the_toss" or self.game_state == "you_lost_the_toss":
            DISPLAY.blit(
                self.font.render(f"{self.yes_or_no_menu[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.yes_or_no_menu[1]}", True, (255, 255, 255)),
                (700, 210))


            if self.yes_no_current_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.yes_no_current_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))







        pygame.display.flip()


class CoinFlipFredScreen(Screen):
    def __init__(self):
        super().__init__("Casino Coin flip  Screen")

        self.result = ""
        self.play_again = True
        self.players_side = ""
        self.new_font = pygame.font.Font(None, 36)
        self.message_display = ""
        self.second_message_display = ""
        self.third_message_display = ""
        self.magic_player_message_display = ""
        self.magic_enemy_message_display = ""
        self.choices = ["Heads", "Tails", "Magic"]
        self.yes_or_no_menu = ["Yes", "No"]
        self.magic_menu_selector = ["Bluff", "Reveal", "Lucky", "Back"]
        self.game_state = "welcome_screen"
        self.choice_sequence = True
        self.bet = 0
        self.font = pygame.font.Font(None, 36)
        self.coinFlipSandyMoney = 700
        self.coinFlipSandyDefeated = False
        self.current_index = 0
        self.yes_no_current_index = 0
        self.magic_menu_index = 0
        self.leave_or_replay_index = 0
        self.high_exp = False
        self.low_exp = False

        self.bluff_text_list = ["I bet you triple my bet that your coin will land on tails 3 times in a row","Hehehe, your on sucker"]
        self.luck_activated = 0
        self.sandy_focus_points = 30
        self.reveal_hand = False
        self.cheating_alert = False

    def giveExp(self, state: "GameState"):
        if state.player.level == 1:
            if self.high_exp == True:
                state.player.exp += 15
            elif self.low_exp == True:
                state.player.exp += 50
        elif state.player.level == 2:
            if self.high_exp == True:
                state.player.exp += 5
            elif self.low_exp == True:
                state.player.exp += 15
        else:
            print("your level is too high no exp for you")





    def place_bet(self, state: "GameState"):
        controller = state.controller
        controller.update(state)

        if controller.isUpPressed:
            self.bet += 10
            pygame.time.delay(200)
            self.isUpPressed = False

        elif controller.isDownPressed:
            self.bet -= 10
            pygame.time.delay(200)
            self.isDownPressed = False

        if self.bet < 10:
            self.bet = 10

        if self.bet > 100:
            self.bet = 100


    def flipCoin(self):
        # currently at .6 because heads is favored
        # in the future will have states to handle coin flip percentages
        # an item can add .1 to your rolls for heads, or -.1 for tails
        coin = random.random()
        if coin < 0.5:
            print("coin landed on heads")
            self.result = "heads"
        else:
            print("coin landed on tails")
            self.result = "tails"

    def cheatCoin(self):
        coin=random.random()
        if coin < 0.3:
            print("coin landed on heads")
            self.result = "heads"
        else:
            print("coin landed on tails")
            self.result = "tails"

    def update(self, state: "GameState"):
        if self.coinFlipSandyMoney <= 0:
            self.coinFlipSandyDefeated = True
        # Update the controller
        controller = state.controller
        controller.update(state)

        if state.player.stamina_points < 3:
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)

        if self.game_state == "welcome_screen" :

            self.message_display = "This is the welcome screen. Press R to continue"
            self.second_message_display = ""
            self.third_message_display = ""
            self.reveal_hand = False

            if controller.isRPressed:
                state.player.stamina_points -= 3

                self.game_state = "bet_screen"

        elif self.game_state == "bet_screen":
            self.message_display = "This is the bet screen. Press up and down to change your bet."
            self.second_message_display = "When you are ready press T to continue."
            controller = state.controller
            self.place_bet(state)
            if controller.isTPressed:
                print("t pressed")
                self.game_state = "coin_flip_time"


        elif self.game_state == "coin_flip_time":
            self.message_display = "I'm flipping the coin now."
            pygame.time.delay(500)
            if self.bet < 80:
                self.flipCoin()
                self.game_state = "choose_heads_or_tails_message"
            elif self.bet > 70:
                self.cheatCoin()
                self.game_state = "choose_heads_or_tails_message"






        elif self.game_state == "choose_heads_or_tails_message":
            self.message_display = "Now Choose heads or tails. Make your choice"
            if controller.isUpPressed:
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) - 1
                else:
                    self.current_index -= 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) + 1
                else:
                    self.current_index += 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isDownPressed = False


            if self.current_index == 0:
                if controller.isTPressed:
                    self.players_side = "heads"
                    self.game_state = "results_screen"

            elif self.current_index == 1:
                if controller.isTPressed:
                    self.players_side = "tails"
                    self.game_state = "results_screen"


            elif self.current_index == 2:
                if controller.isTPressed:
                    print("This is how you pick magic")
                    self.game_state = "magic_menu"





        elif self.game_state == "magic_menu":
            self.message_display = "Pick a magic spell and wreck havic. Press K to cast"

            if controller.isUpPressed:
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) - 1
                else:
                    self.magic_menu_index -= 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) + 1
                else:
                    self.magic_menu_index += 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isDownPressed = False


            if self.magic_menu_index == 0:
                if controller.isKPressed:
                    if self.luck_activated < 1 :
                        if state.player.focus_points >= 10:
                            state.player.focus_points -= 10

                            print("You cast bluff")
                            self.game_state = "bluff_state"

                        else:
                            self.third_message_display = "Sorry but you dont have enough focus points to cast"
                    elif self.luck_activated > 0 or self.reveal_hand == True:
                        self.third_message_display = "sorry but you can't stack magic spells"


            elif self.magic_menu_index == 1:
                if controller.isKPressed:
                    if self.luck_activated < 1:
                        print("You cast reveal")
                        if controller.isKPressed:
                            if state.player.focus_points >= 10:
                                state.player.focus_points -= 10
                                self.reveal_hand = True

                                print("You cast bluff")
                                self.game_state = "reveal_state"

                            elif state.player.focus_points < 10:
                                self.third_message_display = "Sorry but you dont have enough focus points to cast"
                    elif self.luck_activated > 0:
                        self.third_message_display = "sorry but you can't stack magic spells"





##########################have a message state reserved for buff states

            ##### boss enemies will use magic under more strict conditions
            elif self.magic_menu_index == 2:
                if controller.isKPressed:
                    print("you cast avatar of luck")
                    self.third_message_display = "Your luck is now increased for 3 losses"
                    self.luck_activated = 3
                    state.player.focus_points -= 20
                    self.game_state = "choose_heads_or_tails_message"


            elif self.magic_menu_index == 3:
                if controller.isKPressed:
                    print("going back")
                    self.game_state = "choose_heads_or_tails_message"

        elif self.game_state == "reveal_state":
            self.message_display = "time to reveal your coin"
            self.third_message_display = f"The coin will be on the {self.result}"
            if state.controller.isAPressed:
                self.game_state = "choose_heads_or_tails_message"
                state.controller.isAPressed = False




        elif self.game_state == "bluff_state":
            self.message_display = "Triple my bet that tails will land 3 times in a  row."
            bluffalo = random.random()

            if bluffalo < 0.7:
                print("you win tripple bet")
                state.player.playerMoney += self.bet * 3
                self.game_state = "welcome_screen"


            else:
                print("your bet lost")
                state.player.playerMoney -= self.bet
                self.game_state = "welcome_screen"






        elif self.game_state == "results_screen":
            self.second_message_display = " "
            if self.result == self.players_side:
                # self.third_message_display = "You won"
                state.player.playerMoney += self.bet
                self.coinFlipSandyMoney -= self.bet
                pygame.time.delay(1000)

                self.game_state = "you_won_the_toss"

                if self.coinFlipSandyMoney <= 0 or state.player.playerMoney <= 0:
                    print("At 0 ending match")
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)





            elif self.result != self.players_side:
                if self.luck_activated > 0:
                    lucky_draw = random.random()
                    if lucky_draw < 0.9:
                        self.third_message_display = f"Your feeling lucky.{self.luck_activated}remains. Push A"

                        if controller.isAPressed:
                            self.luck_activated -= 1
                            state.player.playerMoney += self.bet
                            self.coinFlipSandyMoney -= self.bet
                            self.result = self.players_side

                            self.game_state = "you_won_the_toss"
                    else:
                        # self.third_message_display = f"Your luck didn't pan out.{self.luck_activated}remains. Push A"
                        if controller.isAPressed:
                            self.luck_activated -= 1

                            state.player.playerMoney -= self.bet
                            self.coinFlipSandyMoney += self.bet

                            self.game_state = "you_lost_the_toss"

                elif self.luck_activated == 0:
                    pygame.time.delay(500)
                    state.player.playerMoney -= self.bet
                    self.coinFlipSandyMoney += self.bet

                    self.game_state = "you_lost_the_toss"











        elif self.game_state == "you_won_the_toss" :
            self.message_display = f"choice  {self.players_side} coin landed  {self.result} You WON"
            self.second_message_display = f"Play again? Press T on your choice"

            if self.coinFlipSandyMoney <= 0 or state.player.playerMoney <= 0:
                print("At 0 ending match")
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)





            elif controller.isUpPressed:
                if not hasattr(self, "leave_or_replay_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) - 1
                else:
                    self.leave_or_replay_index -= 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "yes_no_current_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) + 1
                else:
                    self.leave_or_replay_index += 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isDownPressed = False

            if self.leave_or_replay_index == 0:
                if controller.isTPressed:
                    self.game_state = "welcome_screen"

            elif self.leave_or_replay_index == 1:
                if controller.isTPressed:
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)



        elif self.game_state == "you_lost_the_toss" :

            self.message_display = f"choice  {self.players_side} coin landed  {self.result} lost! "
            self.second_message_display = f"Play again?Yes to continue and No to exi. Press T on your choice"
            if self.coinFlipSandyMoney <= 0 or state.player.playerMoney <= 0:
                print("At 0 ending match")
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)




            elif controller.isUpPressed:
                if not hasattr(self, "leave_or_replay_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) - 1
                else:
                    self.leave_or_replay_index -= 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "yes_no_current_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) + 1
                else:
                    self.leave_or_replay_index += 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isDownPressed = False

            if self.leave_or_replay_index == 0:
                if controller.isTPressed:
                    self.game_state = "welcome_screen"

            elif self.leave_or_replay_index == 1:
                if controller.isTPressed:
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)







    ########################we want up and down arrows on bet. have arrow disapear when an item is not in use

    def draw(self, state: "GameState"):
        # Fill the screen with a solid color
        DISPLAY.fill((0, 0, 0))

        DISPLAY.blit(self.new_font.render(
            f" CoinFlipSandysMoney: {self.coinFlipSandyMoney}",
            True, (255, 255, 255)), (10, 150))
        DISPLAY.blit(self.new_font.render(
            f" player Money: {state.player.playerMoney}",
            True, (255, 255, 255)), (10, 190))

        # Draw the welcome message or choose bet message based on the game state

        DISPLAY.blit(self.font.render(f"{self.message_display}", True, (255, 255, 255)), (10, 10))
        DISPLAY.blit(self.font.render(f"{self.second_message_display}", True, (255, 255, 255)), (10, 50))
        DISPLAY.blit(self.font.render(f"{self.third_message_display}", True, (255, 255, 255)), (10, 230))
        DISPLAY.blit(self.font.render(f"Your current bet is:{self.bet}", True, (255, 255, 255)), (10, 260))
        DISPLAY.blit(self.font.render(f"player health:{state.player.stamina_points}", True, (255, 255, 255)), (10, 290))
        DISPLAY.blit(self.font.render(f"player magic:{state.player.focus_points}", True, (255, 255, 255)), (10, 320))

        if self.game_state == "magic_menu" :
            if self.magic_menu_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.magic_menu_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))




            elif self.magic_menu_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 255))

            elif self.magic_menu_index == 3:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 305))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[1]}", True, (255, 255, 255)),
                (700, 210))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[2]}", True, (255, 255, 255)),
                (700, 260))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[3]}", True, (255, 255, 255)),
                (700, 310))

        elif self.game_state != "you_won_the_toss" and self.game_state != "you_lost_the_toss":
            DISPLAY.blit(
                self.font.render(f"{self.choices[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.choices[1]}", True, (255, 255, 255)),
                (700, 210))

            DISPLAY.blit(
                self.font.render(f"{self.choices[2]}", True, (255, 255, 255)),
                (700, 260))


        if self.game_state == "bet_screen":

            DISPLAY.blit(self.font.render(f"^", True, (255, 255, 255)), (240, 235))
            DISPLAY.blit(self.font.render(f"v", True, (255, 255, 255)), (240, 288))


        elif self.game_state == "choose_heads_or_tails_message":

            if self.current_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.current_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))




            elif self.current_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 255))

        elif self.game_state == "you_won_the_toss" or self.game_state == "you_lost_the_toss":
            DISPLAY.blit(
                self.font.render(f"{self.yes_or_no_menu[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.yes_or_no_menu[1]}", True, (255, 255, 255)),
                (700, 210))


            if self.yes_no_current_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.yes_no_current_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))







        pygame.display.flip()


class CoinFlipSandyScreen(Screen):
    def __init__(self):
        super().__init__("Casino Coin flip  Screen")

        self.result = ""
        self.play_again = True
        self.players_side = ""
        self.new_font = pygame.font.Font(None, 36)
        self.message_display = ""
        self.second_message_display = ""
        self.third_message_display = ""
        self.magic_player_message_display = ""
        self.magic_enemy_message_display = ""
        self.choices = ["Heads", "Tails", "Magic"]
        self.yes_or_no_menu = ["Yes", "No"]
        self.game_state = "welcome_screen"
        self.choice_sequence = True
        self.bet = 0
        self.font = pygame.font.Font(None, 36)
        self.coinFlipSandyMoney = 700
        self.coinFlipSandyDefeated = False
        self.current_index = 0
        self.yes_no_current_index = 0
        self.magic_menu_selector = ["Bluff", "Reveal", "Lucky", "Back"]
        self.magic_menu_index = 0
        self.leave_or_replay_index = 0
        self.high_exp = False
        self.low_exp = False

        self.bluff_text_list = ["I bet you triple my bet that your coin will land on tails 3 times in a row","Hehehe, your on sucker"]
        self.luck_activated = 0
        self.sandy_focus_points = 30
        self.reveal_hand = False
        self.cheating_alert = False

    def giveExp(self, state: "GameState"):
        if state.player.level == 1:
            if self.high_exp == True:
                state.player.exp += 15
            elif self.low_exp == True:
                state.player.exp += 50
        elif state.player.level == 2:
            if self.high_exp == True:
                state.player.exp += 5
            elif self.low_exp == True:
                state.player.exp += 15
        else:
            print("your level is too high no exp for you")





    def place_bet(self, state: "GameState"):
        controller = state.controller
        controller.update(state)

        if controller.isUpPressed:
            self.bet += 10
            pygame.time.delay(200)
            self.isUpPressed = False

        elif controller.isDownPressed:
            self.bet -= 10
            pygame.time.delay(200)
            self.isDownPressed = False

        if self.bet < 10:
            self.bet = 10

        if self.bet > 100:
            self.bet = 100


    def flipCoin(self):
        # currently at .6 because heads is favored
        # in the future will have states to handle coin flip percentages
        # an item can add .1 to your rolls for heads, or -.1 for tails
        coin = random.random()
        if coin < 0.1:
            print("coin landed on heads")
            self.result = "heads"
        else:
            print("coin landed on tails")
            self.result = "tails"

    def update(self, state: "GameState"):
        if self.coinFlipSandyMoney <= 0:
            self.coinFlipSandyDefeated = True
        # Update the controller
        controller = state.controller
        controller.update(state)

        if state.player.stamina_points < 3:
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)

        if self.game_state == "welcome_screen" :

            self.message_display = "This is the welcome screen. Press R to continue"
            self.second_message_display = ""
            self.third_message_display = ""
            self.reveal_hand = False

            if controller.isRPressed:
                state.player.stamina_points -= 3

                self.game_state = "bet_screen"

        elif self.game_state == "bet_screen":
            self.message_display = "This is the bet screen. Press up and down to change your bet."
            self.second_message_display = "When you are ready press T to continue."
            controller = state.controller
            self.place_bet(state)
            if controller.isTPressed:
                print("t pressed")
                self.game_state = "coin_flip_time"


        elif self.game_state == "coin_flip_time":
            self.message_display = "I'm flipping the coin now."
            pygame.time.delay(500)
            self.flipCoin()
            self.game_state = "choose_heads_or_tails_message"





#############fix bug with current index below and our yes and no menu to leave or replay a game

        elif self.game_state == "choose_heads_or_tails_message":
            self.message_display = "Now Choose heads or tails. Make your choice"
            if controller.isUpPressed:
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) - 1
                else:
                    self.current_index -= 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) + 1
                else:
                    self.current_index += 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isDownPressed = False


            if self.current_index == 0:
                if controller.isTPressed:
                    self.players_side = "heads"
                    self.game_state = "results_screen"

            elif self.current_index == 1:
                if controller.isTPressed:
                    self.players_side = "tails"
                    self.game_state = "results_screen"


            elif self.current_index == 2:
                if controller.isTPressed:
                    print("This is how you pick magic")
                    self.game_state = "magic_menu"





        elif self.game_state == "magic_menu":
            self.message_display = "Pick a magic spell and wreck havic. Press K to cast"

            if controller.isUpPressed:
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) - 1
                else:
                    self.magic_menu_index -= 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) + 1
                else:
                    self.magic_menu_index += 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isDownPressed = False


            if self.magic_menu_index == 0:
                if controller.isKPressed:
                    if self.luck_activated < 1:
                        if state.player.focus_points >= 10:
                            state.player.focus_points -= 10

                            print("You cast bluff")
                            self.game_state = "bluff_state"

                        else:
                            self.third_message_display = "Sorry but you dont have enough focus points to cast"
                    elif self.luck_activated > 0 or self.reveal_hand == True:
                        self.third_message_display = "sorry but you can't stack magic spells"


            elif self.magic_menu_index == 1:
                if controller.isKPressed:
                    if self.luck_activated < 1:
                        print("You cast reveal")
                        if controller.isKPressed:
                            if state.player.focus_points >= 10:
                                state.player.focus_points -= 10
                                self.reveal_hand = True

                                print("You cast bluff")
                                self.game_state = "reveal_state"

                            elif state.player.focus_points < 10:
                                self.third_message_display = "Sorry but you dont have enough focus points to cast"
                    elif self.luck_activated > 0:
                        self.third_message_display = "sorry but you can't stack magic spells"





##########################have a message state reserved for buff states

            ##### boss enemies will use magic under more strict conditions
            elif self.magic_menu_index == 2:
                if controller.isKPressed:
                    print("you cast avatar of luck")
                    self.third_message_display = "Your luck is now increased for 5 losses"
                    self.luck_activated = 3
                    state.player.focus_points -= 20
                    self.game_state = "choose_heads_or_tails_message"


            elif self.magic_menu_index == 3:
                if controller.isKPressed:
                    print("going back")
                    self.game_state = "choose_heads_or_tails_message"

        elif self.game_state == "reveal_state":
            self.message_display = "time to reveal your coin"
            self.third_message_display = f"The coin will be on the {self.result}"
            if state.controller.isAPressed:
                self.game_state = "choose_heads_or_tails_message"
                state.controller.isAPressed = False




        elif self.game_state == "bluff_state":
            self.message_display = "Triple my bet that tails will land 3 times in a  row."
            bluffalo = random.random()

            if bluffalo < 0.7:
                print("you win tripple bet")
                state.player.playerMoney += self.bet * 3
                self.game_state = "welcome_screen"


            else:
                print("your bet lost")
                state.player.playerMoney -= self.bet
                self.game_state = "welcome_screen"






        elif self.game_state == "results_screen":
            self.second_message_display = " "
            if self.result == self.players_side:
                # self.third_message_display = "You won"
                state.player.playerMoney += self.bet
                self.coinFlipSandyMoney -= self.bet
                pygame.time.delay(1000)

                self.game_state = "you_won_the_toss"

                if self.coinFlipSandyMoney <= 0 or state.player.playerMoney <= 0:
                    print("At 0 ending match")
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)





            elif self.result != self.players_side:
                if self.luck_activated > 0:
                    lucky_draw = random.random()
                    if lucky_draw < 0.9:
                        self.third_message_display = f"Your feeling lucky.{self.luck_activated}remains. Push A"

                        if controller.isAPressed:
                            self.luck_activated -= 1
                            state.player.playerMoney += self.bet
                            self.coinFlipSandyMoney -= self.bet
                            self.result = self.players_side

                            self.game_state = "you_won_the_toss"
                    else:
                        # self.third_message_display = f"Your luck didn't pan out.{self.luck_activated}remains. Push A"
                        if controller.isAPressed:
                            self.luck_activated -= 1

                            state.player.playerMoney -= self.bet
                            self.coinFlipSandyMoney += self.bet

                            self.game_state = "you_lost_the_toss"

                elif self.luck_activated == 0:
                    pygame.time.delay(500)
                    state.player.playerMoney -= self.bet
                    self.coinFlipSandyMoney += self.bet

                    self.game_state = "you_lost_the_toss"











        elif self.game_state == "you_won_the_toss" :
            if self.players_side == "tails" and self.sandy_focus_points > 0 and self.luck_activated < 1 and self.cheating_alert == False:
                self.players_side = "heads"
                print("I could have sworn I picked tails. Did they switch my bet?")
                if self.reveal_hand == True:
                    print("The other person is cheating. I'll hold up my hands to signafy which side I'll guess")
                    self.cheating_alert = True

                self.game_state = "you_lost_the_toss"

            self.message_display = f"choice  {self.players_side} coin landed  {self.result} You WON"
            self.second_message_display = f"Play again? Press T on your choice"

            if self.coinFlipSandyMoney <= 0 or state.player.playerMoney <= 0:
                print("At 0 ending match")
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)





            elif controller.isUpPressed:
                if not hasattr(self, "leave_or_replay_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) - 1
                else:
                    self.leave_or_replay_index -= 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "yes_no_current_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) + 1
                else:
                    self.leave_or_replay_index += 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isDownPressed = False

            if self.leave_or_replay_index == 0:
                if controller.isTPressed:
                    self.game_state = "welcome_screen"

            elif self.leave_or_replay_index == 1:
                if controller.isTPressed:
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)



        elif self.game_state == "you_lost_the_toss" :
            self.message_display = f"choice  {self.players_side} coin landed  {self.result} lost! "
            self.second_message_display = f"Play again?Yes to continue and No to exi. Press T on your choice"
            if self.coinFlipSandyMoney <= 0 or state.player.playerMoney <= 0:
                print("At 0 ending match")
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)




            elif controller.isUpPressed:
                if not hasattr(self, "leave_or_replay_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) - 1
                else:
                    self.leave_or_replay_index -= 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "yes_no_current_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) + 1
                else:
                    self.leave_or_replay_index += 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isDownPressed = False

            if self.leave_or_replay_index == 0:
                if controller.isTPressed:
                    self.game_state = "welcome_screen"

            elif self.leave_or_replay_index == 1:
                if controller.isTPressed:
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)







    ########################we want up and down arrows on bet. have arrow disapear when an item is not in use

    def draw(self, state: "GameState"):
        # Fill the screen with a solid color
        DISPLAY.fill((0, 0, 0))

        DISPLAY.blit(self.new_font.render(
            f" CoinFlipSandysMoney: {self.coinFlipSandyMoney}",
            True, (255, 255, 255)), (10, 150))
        DISPLAY.blit(self.new_font.render(
            f" player Money: {state.player.playerMoney}",
            True, (255, 255, 255)), (10, 190))

        # Draw the welcome message or choose bet message based on the game state

        DISPLAY.blit(self.font.render(f"{self.message_display}", True, (255, 255, 255)), (10, 10))
        DISPLAY.blit(self.font.render(f"{self.second_message_display}", True, (255, 255, 255)), (10, 50))
        DISPLAY.blit(self.font.render(f"{self.third_message_display}", True, (255, 255, 255)), (10, 230))
        DISPLAY.blit(self.font.render(f"Your current bet is:{self.bet}", True, (255, 255, 255)), (10, 260))
        DISPLAY.blit(self.font.render(f"player health:{state.player.stamina_points}", True, (255, 255, 255)), (10, 290))
        DISPLAY.blit(self.font.render(f"player magic:{state.player.focus_points}", True, (255, 255, 255)), (10, 320))

        if self.game_state == "magic_menu" :
            if self.magic_menu_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.magic_menu_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))




            elif self.magic_menu_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 255))

            elif self.magic_menu_index == 3:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 305))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[1]}", True, (255, 255, 255)),
                (700, 210))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[2]}", True, (255, 255, 255)),
                (700, 260))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[3]}", True, (255, 255, 255)),
                (700, 310))

        elif self.game_state != "you_won_the_toss" and self.game_state != "you_lost_the_toss":
            DISPLAY.blit(
                self.font.render(f"{self.choices[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.choices[1]}", True, (255, 255, 255)),
                (700, 210))

            DISPLAY.blit(
                self.font.render(f"{self.choices[2]}", True, (255, 255, 255)),
                (700, 260))


        if self.game_state == "bet_screen":

            DISPLAY.blit(self.font.render(f"^", True, (255, 255, 255)), (240, 235))
            DISPLAY.blit(self.font.render(f"v", True, (255, 255, 255)), (240, 288))


        elif self.game_state == "choose_heads_or_tails_message":

            if self.current_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.current_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))




            elif self.current_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 255))

        elif self.game_state == "you_won_the_toss" or self.game_state == "you_lost_the_toss":
            DISPLAY.blit(
                self.font.render(f"{self.yes_or_no_menu[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.yes_or_no_menu[1]}", True, (255, 255, 255)),
                (700, 210))


            if self.yes_no_current_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.yes_no_current_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))







        pygame.display.flip()

        ########have deals notice if player is low on stamina and magic and thus react to it
        #### have a dealer make a comment to player on this a few times.

#### no need to "defeat"people, but in doing so with some people you can complete quest
####or have it to where you only need to defeat 1 of each type as a quest.hmmmmm not sure
class OpossumInACanScreen(Screen):
    def __init__(self):
        super().__init__("Opossum in a can screen")
        self.third_message_display = ""
        self.desperate = False
        #we can set this as a variable that can get toggled on and off depending on who you are playing aginst
        self.sallyOpossumMoney = 100
        self.sallyOpossumIsDefeated = False
        self.opossum_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 36)
        self.game_state = "welcome_opposum"
        self.winner_or_looser: List[str] = ["win", "win", "insurance_eater", "win", "win","win","win","lucky_star", "lucky_star", "X3_star", "lose","win",

                                            "win", "insurance_eater"]
        self.result = "win"
        self.bet = 20
        self.insurance = 200
        self.X3 = False
        self.has_opossum_insurance = True

        self.choices = ["Grab", "Magic", "Quit"]
        self.choices_index = 0

        self.bet_or_flee = ["bet", "flee"]
        self.bet_or_flee_index = 0

        self.magic_menu_selector = ["Bluff", "Reveal", "Lucky", "Back"]
        self.magic_menu_index = 0

        self.play_again_or_quit = ["Play Again", "Quit"]

        self.play_again_or_quit_index = 0

        self.bluff_activated = 0
        self.bottom_message = ""
        self.opossum_rader = False

        self.luck_activated = 0




    def refresh(self):
        self.bet = 20
        self.has_opossum_insurance = True
        self.insurance = 200

        self.winner_or_looser = ["win", "win", "insurance_eater", "win", "win","win","win","lucky_star", "lucky_star", "X3_star","win",

                                            "win", "insurance_eater"]

    def shuffle_opposums(self) -> List[str]:
        """Creates a new list in a random order"""

        random.shuffle(self.winner_or_looser)
        if self.luck_activated > 0:
            self.luck_activated -= 1

        print(str(self.winner_or_looser))
        return self.winner_or_looser

    def check_results(self, state: "GameState"):
        if self.result == "X3_star":
            self.X3 = True
            print(self.game_state)
            self.game_state = "play_again_or_bail"


        elif self.result == "win":
            if self.X3 == False:
                self.bet = self.bet * 2
                self.sallyOpossumMoney -= self.bet // 2
                print("you win")
                print(self.bet)
                self.game_state = "play_again_or_bail"
            else:
                self.bet = self.bet * 3
                self.sallyOpossumMoney -= self.bet // 3 * 2
                self.X3 = False
                self.game_state = "play_again_or_bail"

        elif self.result == "lucky_star":
            self.insurance = self.insurance + 200
            self.sallyOpossumMoney -= 200
            self.game_state = "play_again_or_bail"


        elif self.result == "insurance_eater":

            if self.insurance <= 0:
                self.sallyOpossumMoney += self.bet

                print("oh no your in trouble")
                print(self.game_state)
                self.game_state = "loser_screen"
            else:
                print("what are you doing here?")
                self.sallyOpossumMoney += self.insurance
                self.insurance -= 200
                self.game_state = "play_again_or_bail"

        elif self.result == "lose":
            print("This is the losing screen")
            self.sallyOpossumMoney += self.bet
            self.sallyOpossumMoney += self.insurance
            self.bet = 0

            self.game_state = "loser_screen"

    def update(self, state: "GameState"):
        if self.sallyOpossumMoney <= 0:
            self.sallyOpossumIsDefeated = True
        controller = state.controller
        controller.update(state)
        if self.sallyOpossumMoney <= 300:
            self.desperate = True
        elif self.sallyOpossumMoney > 300:
            self.desperate = False

        if self.game_state == "welcome_opposum":


            if controller.isTPressed:
                pygame.time.delay(150)
                self.game_state = "choose_can"

        elif self.game_state == "choose_can":
            if controller.isUpPressed:
                if not hasattr(self, "choices_index"):
                    self.choices_index = len(self.choices) - 1
                else:
                    self.choices_index -= 1
                self.choices_index %= len(self.choices)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "choices_index"):
                    self.choices_index = len(self.choices) + 1
                else:
                    self.choices_index += 1
                self.choices_index %= len(self.choices)
                controller.isDownPressed = False

            elif self.choices_index == 0:
                if controller.isTPressed:
                    pygame.time.delay(150)
                    self.shuffle_opposums()
                    self.result = self.winner_or_looser[0]
                    if self.opossum_rader == True:
                        print("HEY THERE YOU GUY ITS POSSUM TIIIIIIME")
                        self.bottom_message = f"The next draw is a {self.winner_or_looser[0]}Press T to continue"
                        if controller.isTPressed:
                            self.game_state = "choose_or_flee"
                            self.opossum_rader = False

                    else:
                        del self.winner_or_looser[0]
                        self.check_results(state)
                        print("Get that opossum")

            elif self.choices_index == 1:
                if controller.isTPressed:
                    self.game_state = "magic_menu"
                    print("cast magic")


            elif self.choices_index == 2:
                if controller.isTPressed:
                    print("Quitting")



        elif self.game_state == "choose_or_flee":
            self.message_display = f"Will you go forward or retreat?"
            if controller.isUpPressed:
                if not hasattr(self, "bet_or_flee_index"):
                    self.bet_or_flee_index = len(self.bet_or_flee) - 1
                else:
                    self.bet_or_flee_index -= 1
                self.bet_or_flee_index %= len(self.bet_or_flee)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "bet_or_flee_index"):
                    self.bet_or_flee_index = len(self.bet_or_flee) + 1
                else:
                    self.bet_or_flee_index += 1
                self.bet_or_flee_index %= len(self.bet_or_flee)
                controller.isDownPressed = False

            elif self.bet_or_flee_index == 0:
                if controller.isTPressed:
                    print("lets go with it")
                    self.game_state = "choose_can"

            elif self.bet_or_flee_index == 1:
                if controller.isTPressed:

                    print("lets get out")




        elif self.game_state == "magic_menu":
            self.message_display = "Pick a magic spell and wreck havic. Press K to cast"

            if controller.isUpPressed:
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) - 1
                else:
                    self.magic_menu_index -= 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) + 1
                else:
                    self.magic_menu_index += 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isDownPressed = False

            if self.magic_menu_index == 0:
                if controller.isKPressed and state.player.focus_points > 9:
                    if len(self.winner_or_looser) < 6:
                        if state.player.focus_points >= 10:
                            state.player.focus_points -= 10

                            print("You cast bluff")
                            print("I'll bet you I'll get the rst of the wins")
                            state.player.playerMoney += self.sallyOpossumMoney
                            self.sallyOpossumIsDefeated = True
                            self.sallyOpossumMoney = 0
                            print("exiting now")

                        else:
                            self.third_message_display = "Sorry but you dont have enough focus points to cast"
                    else:
                        self.third_message_display = "sorry but you can't stack magic spells.Wait till 3 wins left to cast."


            elif self.magic_menu_index == 1:
                if controller.isKPressed and self.luck_activated == 0:
                    print("You cast reveal")
                    if state.player.focus_points >= 10:
                        state.player.focus_points -= 10
                        self.opossum_rader = True

                        self.game_state = "choose_can"

                    elif state.player.focus_points < 10:
                        self.third_message_display = "Sorry but you dont have enough focus points to cast"
                else:
                    self.third_message_display = "sorry but you can't stack magic spells"





            ##########################have a message state reserved for buff states

            ##### boss enemies will use magic under more strict conditions
            elif self.magic_menu_index == 2:
                if controller.isKPressed and self.luck_activated == 0:
                    print("you cast avatar of luck")
                    self.third_message_display = "The god of luck shines on you, looks like another trash can was hiding behind one of the others"
                    state.player.focus_points -= 20
                    self.winner_or_looser.append("win")

                    self.game_state = "choose_can"
                    self.luck_activated = 5



            elif self.magic_menu_index == 3:
                if controller.isKPressed:
                    print("going back")
                    self.game_state = "choose_can"







                    #########################################################################


        elif self.game_state == "play_again_or_bail":
            if controller.isUpPressed:
                if not hasattr(self, "play_again_or_quit_index"):
                    self.play_again_or_quit_index = len(self.play_again_or_quit) - 1
                else:
                    self.play_again_or_quit_index -= 1
                self.play_again_or_quit_index %= len(self.play_again_or_quit)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "play_again_or_quit_index"):
                    self.play_again_or_quit_index = len(self.play_again_or_quit) + 1
                else:
                    self.play_again_or_quit_index += 1
                self.play_again_or_quit_index %= len(self.play_again_or_quit)
                controller.isDownPressed = False

            elif self.play_again_or_quit_index == 0:
                if controller.isTPressed:
                    print("lets go with it")
                    pygame.time.delay(150)
                    self.game_state = "choose_can"

            elif self.play_again_or_quit_index == 1:
                if controller.isTPressed:
                    print("lets get out")










        elif self.game_state == "loser_screen":
            time.sleep(3)
            self.refresh()
            self.game_state = "welcome_opposum"
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)

    def draw(self, state: "GameState"):
        DISPLAY.fill((0,0,0))

        if self.desperate == True:
            DISPLAY.blit(self.font.render(
                f" I Take care of the orphanage here Please think of the children!",
                True, (255, 255, 255)), (10, 530))

        DISPLAY.blit(self.font.render(f"{self.winner_or_looser}", True, (255, 255, 255)), (1, 333))

        DISPLAY.blit(self.font.render(
            f" SallyOpossum Money: {self.sallyOpossumMoney}",
            True, (255, 255, 255)), (10, 190))
        DISPLAY.blit(self.font.render(
            f" player Money: {state.player.playerMoney}",
            True, (255, 255, 255)), (10, 290))

        DISPLAY.blit(self.font.render(
            f" Players Bet: {self.bet}",
            True, (255, 255, 255)), (10, 390))
        DISPLAY.blit(self.font.render(
            f" player Insurance: {self.insurance} here is your luck duck : {self.luck_activated}",
            True, (255, 255, 255)), (10, 490))

        DISPLAY.blit(self.font.render(
            f" bottom message: {self.bottom_message}  rader is: {self.opossum_rader}",
            True, (255, 255, 255)), (10, 33))


        if self.game_state == "choose_can":

            DISPLAY.blit(
                self.font.render(f"{self.choices[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.choices[1]}", True, (255, 255, 255)),
                (700, 210))

            DISPLAY.blit(
                self.font.render(f"{self.choices[2]}", True, (255, 255, 255)),
                (700, 260))


            if self.choices_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.choices_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))




            elif self.choices_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 255))

        elif self.game_state == "choose_or_flee":
            if self.bet_or_flee_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.bet_or_flee_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))

            DISPLAY.blit(
                self.font.render(f"{self.bet_or_flee[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.bet_or_flee[1]}", True, (255, 255, 255)),
                (700, 210))



        elif self.game_state == "magic_menu" :
            if self.magic_menu_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.magic_menu_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))




            elif self.magic_menu_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 255))

            elif self.magic_menu_index == 3:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 305))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[1]}", True, (255, 255, 255)),
                (700, 210))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[2]}", True, (255, 255, 255)),
                (700, 260))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[3]}", True, (255, 255, 255)),
                (700, 310))



        elif self.game_state == "welcome_opposum":
            DISPLAY.blit(self.font.render(f"press T", True, (255, 255, 255)), (10, 10))
        elif self.game_state == "choose_can":
            DISPLAY.blit(self.font.render(f"Press 1 to choose  a opossum", True, (255, 255, 255)), (100, 10))



        elif self.game_state == "play_again_or_bail":
            DISPLAY.blit(self.font.render(f"your result is {self.result}", True, (255, 255, 255)), (388, 50))
            if self.play_again_or_quit_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.play_again_or_quit_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))

            DISPLAY.blit(
                self.font.render(f"{self.play_again_or_quit[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.play_again_or_quit[1]}", True, (255, 255, 255)),
                (700, 210))

        elif self.game_state == "loser_screen":
            DISPLAY.blit(self.font.render(f"You drew the {self.result} you lose goodbye", True, (255, 255, 255)), (210, 50))


        pygame.display.flip()

class OpossumInACanNellyScreen(Screen):
    def __init__(self):
        super().__init__("Opossum in a can screen")
        self.third_message_display = ""
        self.desperate = False
        #we can set this as a variable that can get toggled on and off depending on who you are playing aginst
        self.sallyOpossumMoney = 100
        self.sallyOpossumIsDefeated = False
        self.opossum_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 36)
        self.game_state = "welcome_opposum"
        self.winner_or_looser: List[str] = ["win", "win", "insurance_eater", "win", "win","win","win","lucky_star", "lucky_star", "X3_star", "lose","win",

                                            "win", "insurance_eater", "lose"]
        self.result = "win"
        self.bet = 20
        self.insurance = 200
        self.X3 = False
        self.has_opossum_insurance = True

        self.choices = ["Grab", "Magic", "Quit"]
        self.choices_index = 0

        self.bet_or_flee = ["bet", "flee"]
        self.bet_or_flee_index = 0

        self.magic_menu_selector = ["Bluff", "Reveal", "Lucky", "Back"]
        self.magic_menu_index = 0

        self.play_again_or_quit = ["Play Again", "Quit"]

        self.play_again_or_quit_index = 0

        self.bluff_activated = 0
        self.bottom_message = ""
        self.opossum_rader = False

        self.luck_activated = 0




    def refresh(self):
        self.bet = 20
        self.has_opossum_insurance = True
        self.insurance = 200

        self.winner_or_looser = ["win", "win", "insurance_eater", "win", "win","win","win","lucky_star", "lucky_star", "X3_star", "lose","win",

                                            "win", "insurance_eater", "lose"]

    def shuffle_opposums(self) -> List[str]:
        """Creates a new list in a random order"""

        random.shuffle(self.winner_or_looser)
        if self.luck_activated > 0:
            self.luck_activated -= 1

        print(str(self.winner_or_looser))
        return self.winner_or_looser

    def check_results(self, state: "GameState"):
        if self.result == "X3_star":
            self.X3 = True
            print(self.game_state)
            self.game_state = "play_again_or_bail"


        elif self.result == "win":
            if self.X3 == False:
                self.bet = self.bet * 2
                self.sallyOpossumMoney -= self.bet // 2
                print("you win")
                print(self.bet)
                self.game_state = "play_again_or_bail"
            else:
                self.bet = self.bet * 3
                self.sallyOpossumMoney -= self.bet // 3 * 2
                self.X3 = False
                self.game_state = "play_again_or_bail"

        elif self.result == "lucky_star":
            self.insurance = self.insurance + 200
            self.sallyOpossumMoney -= 200
            self.game_state = "play_again_or_bail"


        elif self.result == "insurance_eater":

            if self.insurance <= 0:
                self.sallyOpossumMoney += self.bet

                print("oh no your in trouble")
                print(self.game_state)
                self.game_state = "loser_screen"
            else:
                print("what are you doing here?")
                self.sallyOpossumMoney += self.insurance
                self.insurance -= 200
                self.game_state = "play_again_or_bail"

        elif self.result == "lose":
            print("This is the losing screen")
            self.sallyOpossumMoney += self.bet
            self.sallyOpossumMoney += self.insurance
            self.bet = 0

            self.game_state = "loser_screen"

    def update(self, state: "GameState"):
        if self.sallyOpossumMoney <= 0:
            self.sallyOpossumIsDefeated = True
        controller = state.controller
        controller.update(state)
        if self.sallyOpossumMoney <= 300:
            self.desperate = True
        elif self.sallyOpossumMoney > 300:
            self.desperate = False

        if self.game_state == "welcome_opposum":


            if controller.isTPressed:
                pygame.time.delay(150)
                self.game_state = "choose_can"

        elif self.game_state == "choose_can":
            if controller.isUpPressed:
                if not hasattr(self, "choices_index"):
                    self.choices_index = len(self.choices) - 1
                else:
                    self.choices_index -= 1
                self.choices_index %= len(self.choices)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "choices_index"):
                    self.choices_index = len(self.choices) + 1
                else:
                    self.choices_index += 1
                self.choices_index %= len(self.choices)
                controller.isDownPressed = False

            elif self.choices_index == 0:
                if controller.isTPressed:
                    pygame.time.delay(150)
                    self.shuffle_opposums()
                    self.result = self.winner_or_looser[0]
                    if self.opossum_rader == True:
                        print("HEY THERE YOU GUY ITS POSSUM TIIIIIIME")
                        self.bottom_message = f"The next draw is a {self.winner_or_looser[0]}Press T to continue"
                        if self.result == "lose":
                            print("you notice this dealer is cheating")
                            state.player.playerMoney += self.sallyOpossumMoney
                            self.sallyOpossumMoney = 0
                            print("time to leave we got the  cheater")
                        if controller.isTPressed:
                            self.game_state = "choose_or_flee"
                            self.opossum_rader = False

                    else:
                        del self.winner_or_looser[0]
                        self.check_results(state)
                        print("Get that opossum")

            elif self.choices_index == 1:
                if controller.isTPressed:
                    self.game_state = "magic_menu"
                    print("cast magic")


            elif self.choices_index == 2:
                if controller.isTPressed:
                    print("Quitting")



        elif self.game_state == "choose_or_flee":
            self.message_display = f"Will you go forward or retreat?"
            if controller.isUpPressed:
                if not hasattr(self, "bet_or_flee_index"):
                    self.bet_or_flee_index = len(self.bet_or_flee) - 1
                else:
                    self.bet_or_flee_index -= 1
                self.bet_or_flee_index %= len(self.bet_or_flee)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "bet_or_flee_index"):
                    self.bet_or_flee_index = len(self.bet_or_flee) + 1
                else:
                    self.bet_or_flee_index += 1
                self.bet_or_flee_index %= len(self.bet_or_flee)
                controller.isDownPressed = False

            elif self.bet_or_flee_index == 0:
                if controller.isTPressed:
                    print("lets go with it")
                    self.game_state = "choose_can"

            elif self.bet_or_flee_index == 1:
                if controller.isTPressed:

                    print("lets get out")




        elif self.game_state == "magic_menu":
            self.message_display = "Pick a magic spell and wreck havic. Press K to cast"

            if controller.isUpPressed:
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) - 1
                else:
                    self.magic_menu_index -= 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) + 1
                else:
                    self.magic_menu_index += 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isDownPressed = False

            if self.magic_menu_index == 0:
                if controller.isKPressed and state.player.focus_points > 9:
                    if len(self.winner_or_looser) < 6:
                        if state.player.focus_points >= 10:
                            state.player.focus_points -= 10

                            print("You cast bluff")
                            print("I'll bet you I'll get the rst of the wins")
                            state.player.playerMoney += self.sallyOpossumMoney
                            self.sallyOpossumIsDefeated = True
                            self.sallyOpossumMoney = 0
                            print("exiting now")

                        else:
                            self.third_message_display = "Sorry but you dont have enough focus points to cast"
                    else:
                        self.third_message_display = "sorry but you can't stack magic spells.Wait till 3 wins left to cast."


            elif self.magic_menu_index == 1:
                if controller.isKPressed and self.luck_activated == 0:
                    print("You cast reveal")
                    if state.player.focus_points >= 10:
                        state.player.focus_points -= 10
                        self.opossum_rader = True

                        self.game_state = "choose_can"

                    elif state.player.focus_points < 10:
                        self.third_message_display = "Sorry but you dont have enough focus points to cast"
                else:
                    self.third_message_display = "sorry but you can't stack magic spells"





            ##########################have a message state reserved for buff states

            ##### boss enemies will use magic under more strict conditions
            elif self.magic_menu_index == 2:
                if controller.isKPressed and self.luck_activated == 0:
                    print("you cast avatar of luck")
                    self.third_message_display = "The god of luck shines on you, looks like another trash can was hiding behind one of the others"
                    state.player.focus_points -= 20
                    self.winner_or_looser.append("win")

                    self.game_state = "choose_can"
                    self.luck_activated = 5



            elif self.magic_menu_index == 3:
                if controller.isKPressed:
                    print("going back")
                    self.game_state = "choose_can"







                    #########################################################################


        elif self.game_state == "play_again_or_bail":
            if controller.isUpPressed:
                if not hasattr(self, "play_again_or_quit_index"):
                    self.play_again_or_quit_index = len(self.play_again_or_quit) - 1
                else:
                    self.play_again_or_quit_index -= 1
                self.play_again_or_quit_index %= len(self.play_again_or_quit)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "play_again_or_quit_index"):
                    self.play_again_or_quit_index = len(self.play_again_or_quit) + 1
                else:
                    self.play_again_or_quit_index += 1
                self.play_again_or_quit_index %= len(self.play_again_or_quit)
                controller.isDownPressed = False

            elif self.play_again_or_quit_index == 0:
                if controller.isTPressed:
                    print("lets go with it")
                    pygame.time.delay(150)
                    self.game_state = "choose_can"

            elif self.play_again_or_quit_index == 1:
                if controller.isTPressed:
                    print("lets get out")










        elif self.game_state == "loser_screen":
            time.sleep(3)
            self.refresh()
            self.game_state = "welcome_opposum"
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)

    def draw(self, state: "GameState"):
        DISPLAY.fill((0,0,0))

        if self.desperate == True:
            DISPLAY.blit(self.font.render(
                f" I Take care of the orphanage here Please think of the children!",
                True, (255, 255, 255)), (10, 530))

        DISPLAY.blit(self.font.render(f"{self.winner_or_looser}", True, (255, 255, 255)), (1, 333))

        DISPLAY.blit(self.font.render(
            f" SallyOpossum Money: {self.sallyOpossumMoney}",
            True, (255, 255, 255)), (10, 190))
        DISPLAY.blit(self.font.render(
            f" player Money: {state.player.playerMoney}",
            True, (255, 255, 255)), (10, 290))

        DISPLAY.blit(self.font.render(
            f" Players Bet: {self.bet}",
            True, (255, 255, 255)), (10, 390))
        DISPLAY.blit(self.font.render(
            f" player Insurance: {self.insurance} here is your luck duck : {self.luck_activated}",
            True, (255, 255, 255)), (10, 490))

        DISPLAY.blit(self.font.render(
            f" bottom message: {self.bottom_message}  rader is: {self.opossum_rader}",
            True, (255, 255, 255)), (10, 33))


        if self.game_state == "choose_can":

            DISPLAY.blit(
                self.font.render(f"{self.choices[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.choices[1]}", True, (255, 255, 255)),
                (700, 210))

            DISPLAY.blit(
                self.font.render(f"{self.choices[2]}", True, (255, 255, 255)),
                (700, 260))


            if self.choices_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.choices_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))




            elif self.choices_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 255))

        elif self.game_state == "choose_or_flee":
            if self.bet_or_flee_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.bet_or_flee_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))

            DISPLAY.blit(
                self.font.render(f"{self.bet_or_flee[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.bet_or_flee[1]}", True, (255, 255, 255)),
                (700, 210))



        elif self.game_state == "magic_menu" :
            if self.magic_menu_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.magic_menu_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))




            elif self.magic_menu_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 255))

            elif self.magic_menu_index == 3:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 305))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[1]}", True, (255, 255, 255)),
                (700, 210))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[2]}", True, (255, 255, 255)),
                (700, 260))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[3]}", True, (255, 255, 255)),
                (700, 310))



        elif self.game_state == "welcome_opposum":
            DISPLAY.blit(self.font.render(f"press T", True, (255, 255, 255)), (10, 10))
        elif self.game_state == "choose_can":
            DISPLAY.blit(self.font.render(f"Press 1 to choose  a opossum", True, (255, 255, 255)), (100, 10))



        elif self.game_state == "play_again_or_bail":
            DISPLAY.blit(self.font.render(f"your result is {self.result}", True, (255, 255, 255)), (388, 50))
            if self.play_again_or_quit_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.play_again_or_quit_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))

            DISPLAY.blit(
                self.font.render(f"{self.play_again_or_quit[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.play_again_or_quit[1]}", True, (255, 255, 255)),
                (700, 210))

        elif self.game_state == "loser_screen":
            DISPLAY.blit(self.font.render(f"You drew the {self.result} you lose goodbye", True, (255, 255, 255)), (210, 50))


        pygame.display.flip()




class DiceGameScreen(Screen, Dice):
    def __init__(self):
        super().__init__("Dice game")
        self.game_state = "choose_player_2_or_ai"
        self.isPlayer2 = False
        self.isAI = False
        self.game_state_started_at = 0
        start_time = pygame.time.get_ticks()

        self.diceFont = pygame.font.Font(None, 36)
        self.player_1_turn = False
        self.player_2_turn = False
        self.player1pile = 0
        self.player2pile = 0
        self.ante = 1000
        self.anteXero = 0
        self.player_1_won_game = False
        self.player_2_won_game = False

        self.roll_state = ""
        self.player_1_lost_game = False
        self.player_2_lost_game = False
        self.its_a_draw = False
        self.start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_delay = 500  # input delay in milliseconds
        self.input_time = 0  # time when input was last read
        self.chiliWilleyMoney = 500
        self.chiliWilleyIsDefeated = False

    def refresh(self):
        self.player1pile = 0
        self.player2pile = 0
        self.ante = 1000
        self.game_state = "choose_player_2_or_ai"





    def hot_bet(self):

        if self.game_state == "player_1_going_hot":
            self.roll_two_d_six()
            if self.rolls[0] == self.rolls[1]:

                self.player2pile += self.ante + self.player1pile
                self.player1pile = 0
                self.ante = 0
                self.roll_state = "you got a double at the wrong time, you lose"
                print("you rolled a double get ready for trouble")
                self.player_1_lost_game = True
                self.game_state = "player_1_results"



            elif self.add() == 5 or self.add() == 6 or self.add() == 7 or self.add() == 8 or self.add() == 9:
                self.roll_one_d_hundred()
                subtracted_amount = min(self.one_hundred_rolls[0], self.player2pile)
                self.player2pile -= subtracted_amount * 3
                self.player1pile += subtracted_amount * 3
                self.roll_state = "attacking enemy player pile"

                if self.player2pile < 0:
                    self.player2pile = 0
                    print("if its 0:")
                    print(self.player2pile)
                self.game_state = "player_2_declare_intent_stage"

            else:
                self.roll_state = "Your roll was wasted"

        ########player 2 below

        if self.game_state == "player_2_going_hot":
            self.roll_two_d_six()
            if self.rolls[0] == self.rolls[1]:

                self.player1pile += self.ante + self.player2pile
                self.ante = 0
                self.roll_state = "you got a double at the wrong time, you lose"

                self.player2pile = 0
                self.player_2_lost_game = True

            elif self.add() == 5 or self.add() == 6 or self.add() == 7 or self.add() == 8 or self.add() == 9:

                self.roll_one_d_hundred()
                print("you rolled the dice as an AI")
                subtracted_amount = min(self.one_hundred_rolls[0], self.player1pile)
                self.player2pile += subtracted_amount * 3
                self.player1pile -= subtracted_amount * 3
                self.roll_state = "attacking enemy player pile"

                if self.player1pile < 0:
                    self.player1pile = 0

                self.game_state = "player_1_declare_intent_stage"

            else:
                self.roll_state = "Your roll was wasted"



        elif self.game_state == "player_1_going_hot":
            print("no dice you wasted your chance")
            self.game_state = "player_2_declare_intent_stage"

        elif self.game_state == "player_2_going_hot":
            print("no dice you wasted your chance")

        print("end state: " + self.game_state)

    def cold_bet(self):

        self.roll_two_d_six()
        if self.rolls[0] == 1 and self.rolls[1] == 1:
            if self.game_state == "player_1_rolls":
                print(self.game_state)
                self.player2pile = self.player2pile + self.player1pile + self.ante
                self.player1pile = 0
                self.ante = 0
                self.roll_state = "You got the wrong kind of double, you lose everything player 1!"
                print(self.player1pile)
                self.player_2_won_game = True



            elif self.game_state == "player_2_rolls":
                print(self.game_state)

                self.player1pile = self.player2pile + self.player1pile + self.ante
                self.player1pile = 0
                self.ante = 0
                self.roll_state = "You got the wrong kind of double, you lose everything player 2!"
                print(self.player2pile)
                self.player_1_won_game = True


        elif self.rolls[0] == 6 and self.rolls[1] == 6:
            if self.game_state == "player_1_rolls":
                print("you win =======================================================================")
                self.player1pile = self.player2pile + self.player1pile + self.ante
                self.player2pile = 0
                self.ante = 0
                self.roll_state = "lucky double 6, player 1 wins!"
                self.game_state = "player_1_wins"
                self.player_1_won_game = True



            elif self.game_state == "player_2_rolls":
                print("you win ==================================================================")
                self.player2pile = self.player2pile + self.player1pile + self.ante
                self.player1pile = 0
                self.ante = 0
                self.roll_state = "lucky double 6, player 2 wins!"
                self.game_state = "player_2_wins"
                self.player_2_won_game = True


        #
        elif self.add() == 6:
            if self.game_state == "player_1_rolls":
                self.roll_state = "Devil's 6 go after enemy pile."

                self.roll_one_d_hundred()
                if self.one_hundred_rolls[0] > self.player2pile:
                    self.one_hundred_rolls[0] = self.player2pile
                self.player1pile += self.one_hundred_rolls[0]
                self.player2pile -= self.one_hundred_rolls[0]
                if self.player2pile < 0:
                    self.player2pile = 0
                self.game_state = "player_2_intent_stage"
            elif self.game_state == "player_2_rolls":
                self.roll_state = "Devil's 6 go after enemy pile"
                self.roll_one_d_hundred()
                if self.one_hundred_rolls[0] > self.player2pile:
                    self.one_hundred_rolls[0] = self.player2pile
                self.player2pile += self.one_hundred_rolls[0]

                self.player1pile -= self.one_hundred_rolls[0]
                if self.player1pile < 0:
                    self.player1pile = 0
                self.game_state = "player_1_intent_stage"

        #
        elif self.add() == 7 or self.add() == 8 or self.add() == 9 or self.add() == 10 or self.add() == 11:
            if self.game_state == "player_1_rolls":
                self.roll_state = "Go after the ante"

                self.roll_one_d_hundred()
                subtracted_amount = min(self.one_hundred_rolls[0], self.ante)
                self.ante -= subtracted_amount
                self.player1pile += subtracted_amount

                if self.ante < 0:
                    self.ante = 0
                self.game_state = "player_2_intent_stage"



            elif self.game_state == "player_2_rolls":
                self.roll_state = "Go after the ante"

                self.roll_one_d_hundred()
                subtracted_amount = min(self.one_hundred_rolls[0], self.ante)
                self.ante -= subtracted_amount
                self.player2pile += subtracted_amount

                if self.ante < 0:
                    self.ante = 0
                self.game_state = "player_1_intent_stage"
        else:
            self.roll_state = "wasted roll"

    def start_state(self, gamestate):
        self.game_state = gamestate
        self.game_state_started_at = pygame.time.get_ticks()

    def update(self, state: "GameState"):
        if self.chiliWilleyMoney <= 0:
            self.chiliWilleyIsDefeated = True
        # delta between last update time in milliseconds
        delta = pygame.time.get_ticks() - self.game_state_started_at
        # this is to track what state we currently in DO NOT DELTE THIS
        # print("update() - state: " + str(self.game_state) + ", start at: " + str(delta))

        controller = state.controller
        controller.update(state)
        print("HERE WE GOO OOOOOO")

        if self.game_state == "player_1_wins":

            pygame.time.delay(5000)
            self.refresh()

            state.player.playerMoney += 500
            self.chiliWilleyMoney -= 500
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)

        elif self.game_state == "player_2_wins":

            pygame.time.delay(5000)
            self.refresh()

            state.player.playerMoney -= 500
            self.chiliWilleyMoney += 500
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)


        elif self.game_state == "choose_player_2_or_ai":
            if controller.is1Pressed:
                self.isPlayer2 = True
                self.game_state = "player_1_declare_intent_stage"
                print("player 2")

            else:
                if controller.isOPressed:
                    self.isAI = True
                    self.game_state = "player_1_declare_intent_stage"

        elif self.game_state == "player_1_declare_intent_stage":
            self.one_hundred_rolls = 0
            # if delta > 500: # don't read keyboard input for at least 500 ms.

            if controller.isTPressed:

                self.start_state("player_1_rolls")
                # print(self.game_state)

            elif controller.isPPressed:
                self.start_state("player_1_going_hot")




        elif self.game_state == "player_1_rolls":
            # if delta > 1500: # don't read keyboard input for at least 500 ms.

            if controller.isEPressed:

                print("pressing T")
                self.cold_bet()
                if self.one_hundred_rolls == 0:
                    self.start_state("player_1_results")

                    if self.player_1_won_game == True:

                        self.start_state("player_1_wins")
                        pygame.time.delay(2000)



                else:
                    self.start_state("player_1_results_one_hundred")



        elif self.game_state == "player_1_going_hot":
            if controller.is1Pressed:
                print("pressing 1")
                self.hot_bet()
                if self.one_hundred_rolls == 0:
                    self.game_state = "player_1_results"
                    print("Player 1 got set to 1player 1 rsults")
                else:
                    self.game_state = "player_1_results_one_hundred"



        elif self.game_state == "player_1_results" or self.game_state == "player_1_results_one_hundred":
            print("player jadfllasf;jslfjls;jaf")
            if self.player_1_lost_game == True:
                pygame.time.delay(3000)
                state.player.playerMoney -= 500
                self.chiliWilleyMoney += 500

                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)

            elif controller.isBPressed:
                print("Houstan we got a problem here")
                self.game_state = "player_2_declare_intent_stage"


        ######player 2 stuff down here

        elif self.game_state == "player_2_declare_intent_stage":
            self.one_hundred_rolls = 0

            if self.isPlayer2 == True:

                if controller.isTPressed:
                    print("WE in update")
                    self.game_state = "player_2_rolls"

                elif controller.isPPressed:
                    self.game_state = "player_2_going_hot"

            elif self.isAI == True:
                time.sleep(2)
                if self.player1pile < 300:
                    controller.isTPressed = True
                    self.game_state = "player_2_rolls"
                    controller.isTPressed = False
                else:
                    controller.isPPressed = True
                    self.game_state = "player_2_going_hot"
                    controller.isPPressed = False




        elif self.game_state == "player_2_rolls":
            if self.isPlayer2 == True:
                if controller.isEPressed:
                    print("pressing T")
                    self.cold_bet()
                    if self.one_hundred_rolls == 0:
                        self.game_state = "player_2_results"
                    else:
                        self.game_state = "player_2_results_one_hundred"

            elif self.isAI == True:
                time.sleep(2)
                controller.isEPressed = True
                print("pressing T")
                self.cold_bet()
                controller.isEPressed = False
                if self.one_hundred_rolls == 0:
                    self.game_state = "player_2_results"
                else:
                    self.game_state = "player_2_results_one_hundred"


        ####PLAYER 2 HOT PHASE DOWN HERE!!!!!!!

        elif self.game_state == "player_2_going_hot":
            if self.isPlayer2 == True:
                if controller.is1Pressed:
                    print("pressing 1")
                    self.hot_bet()
                    if self.one_hundred_rolls == 0:
                        self.game_state = "player_2_results"
                    else:
                        self.game_state = "player_2_results_one_hundred"

            elif self.isAI == True:
                time.sleep(2)
                controller.is1Pressed = True

                self.hot_bet()
                controller.is1Pressed = False
                if self.one_hundred_rolls == 0:
                    self.game_state = "player_2_results"
                else:
                    self.game_state = "player_2_results_one_hundred"






        elif self.game_state == "player_2_results" \
                or self.game_state == "player_2_results_one_hundred":
            print("we're walking here")
            print(str(self.isPlayer2))
            # if self.isPlayer2 == True:
            print("We're sitting here")
            if self.isPlayer2 == True:
                if controller.isBPressed:
                    print("HEY THER YOU U YO UYOU YOU YOU YO U ;sdfakl;sfd")
                    self.game_state = "player_1_declare_intent_stage"

            elif self.isAI == True:
                time.sleep(2)
                controller.isBPressed = True
                self.game_state = "player_1_declare_intent_stage"
                controller.isBPressed = False

        if self.ante == 0:
            print("THE ANTIE IS AT 00000000000000000000o0-o0o00o0o0o0o0o0o")
            if self.player1pile > self.player2pile:
                self.game_state = "player_1_wins"
                self.player_2_lost_game = True

            elif self.player1pile < self.player2pile:
                self.game_state = "player_2_wins"
                self.player_1_lost_game = True

            elif self.player1pile == self.player2pile:
                self.roll_state = "It's a draw,  you both walk away whole"
                self.its_a_draw = True
                print("its a draw")

    def draw(self, state: "GameState"):
        DISPLAY.fill((0, 0, 0))

        if self.game_state == "choose_player_2_or_ai":
            DISPLAY.blit(self.diceFont.render(f"Press 1 key for human or O key for AI", True, (255, 255, 255)),
                         (10, 10))

        if self.game_state == "player_1_declare_intent_stage":
            DISPLAY.blit(self.diceFont.render(f"Player 1: press T for cold P For hot", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))

        elif self.game_state == "player_2_declare_intent_stage":
            DISPLAY.blit(self.diceFont.render(f"Player 2: press T for cold P for hot", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))



        elif self.game_state == "player_1_going_cold":
            DISPLAY.blit(self.diceFont.render(f"Player 1 is going cold. ", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))

        elif self.game_state == "player_2_going_cold":
            DISPLAY.blit(self.diceFont.render(f"Player 1 is going cold. ", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))

        elif self.game_state == "player_1_going_hot":
            DISPLAY.blit(self.diceFont.render(f"Player 1 is going hot PRESS 1", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))

        elif self.game_state == "player_2_going_hot":
            DISPLAY.blit(self.diceFont.render(f"Player 2 is going hot PRESS 1", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))

        elif self.game_state == "player_1_wins":
            DISPLAY.blit(self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 10))
            DISPLAY.blit(self.diceFont.render(f"Player 1 MONEY: {state.player.playerMoney}", True, (255, 255, 255)), (200, 100))
            DISPLAY.blit(self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.diceFont.render(f"Player 2 MONEY: {self.chiliWilleyMoney}", True, (255, 255, 255)), (200, 300))
            DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True, (255, 255, 255)), (200, 400))
            DISPLAY.blit(self.diceFont.render(f"Player 1 wins", True, (255, 255, 255)), (200, 500))


        elif self.game_state == "player_2_wins":
            DISPLAY.blit(self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (155, 10))
            DISPLAY.blit(self.diceFont.render(f"Player 1 Money: {state.player.playerMoney}", True, (255, 255, 255)), (155, 100))
            DISPLAY.blit(self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (155, 200))
            DISPLAY.blit(self.diceFont.render(f"Player 2 Money: {self.chiliWilleyMoney}", True, (255, 255, 255)), (155, 300))
            DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True, (255, 255, 255)), (155, 400))
            DISPLAY.blit(self.diceFont.render(f"Player 2 wins", True, (255, 255, 255)), (155, 500))


        elif self.game_state == "player_1_rolls":
            DISPLAY.blit(self.diceFont.render(f"PLAYER 1 PRESS E to roll the dice", True, (255, 255, 255)), (255, 255))

        elif self.game_state == "player_2_rolls":
            DISPLAY.blit(self.diceFont.render(f"PLAYER 2 PRESS E to roll the dice", True, (255, 255, 255)), (255, 255))


        elif self.game_state == "player_1_results":
            DISPLAY.blit(self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))
            DISPLAY.blit(
                self.diceFont.render(f" Player 1 rolls a {self.rolls} PRESS B when ready", True, (255, 255, 255)),
                (155, 255))
            DISPLAY.blit(self.diceFont.render(f" {self.roll_state}", True, (255, 255, 255)), (5, 355))
            if self.player_1_lost_game == True:
                DISPLAY.blit(
                    self.diceFont.render(f"Sorry player 1: GAME OVER!!!: ", True, (255, 255, 255)),
                    (1, 555))


            elif self.its_a_draw == True:
                DISPLAY.blit(
                    self.diceFont.render(f"It's a draw sorry player 1: ", True, (255, 255, 255)),
                    (1, 555))
                pygame.time.delay(5000)

                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)


        elif self.game_state == "player_2_results":
            DISPLAY.blit(self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))
            DISPLAY.blit(
                self.diceFont.render(f" Player 2 rolls a {self.rolls} PRESS B when ready", True, (255, 255, 255)),
                (155, 255))
            DISPLAY.blit(self.diceFont.render(f" {self.roll_state}", True, (255, 255, 255)), (5, 355))
            if self.player_2_lost_game == True:
                DISPLAY.blit(
                    self.diceFont.render(f"Sorry player 2: GAME OVER!!!: ", True, (255, 255, 255)),
                    (1, 555))

            elif self.its_a_draw == True:
                DISPLAY.blit(
                    self.diceFont.render(f"It's a draw sorry player 2: ", True, (255, 255, 255)),
                    (1, 555))




        elif self.game_state == "player_1_results_one_hundred":
            DISPLAY.blit(self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))
            DISPLAY.blit(
                self.diceFont.render(f" Player 1 rolls a {self.rolls} PRESS B when ready", True, (255, 255, 255)),
                (155, 255))
            DISPLAY.blit(self.diceFont.render(f" {self.roll_state}", True, (255, 255, 255)), (5, 355))
            DISPLAY.blit(self.diceFont.render(f"1d100 ROLLED: {self.one_hundred_rolls}", True, (255, 255, 255)),
                         (5, 555))



        elif self.game_state == "player_2_results_one_hundred":
            DISPLAY.blit(self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))
            DISPLAY.blit(
                self.diceFont.render(f" Player 2 rolls a {self.rolls} PRESS B when ready", True, (255, 255, 255)),
                (155, 255))
            DISPLAY.blit(self.diceFont.render(f" {self.roll_state}", True, (255, 255, 255)), (5, 355))
            DISPLAY.blit(self.diceFont.render(f"1d100 ROLLED: {self.one_hundred_rolls}", True, (255, 255, 255)),
                         (5, 555))

        pygame.display.flip()


ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
suits = ['Spades', 'Diamonds', 'Clubs', 'Hearts'] # TODO use enum

#dsf;dsaf;dsfjdajfdsafjsa;fjldsjjsdafjds;ajf;dj;sjfldsjafldsjaf;ldsjfldsajf
# if a player has 3 cards, then an ace value is equal to one
# ace should be set that if a value is less than 10, then at least one of them should be
#set to 11
#need to set up test cases for many up to having 4 aces in hand


#betting is also broken, a black jack should net X 2 winnings
class Deck:
    def __init__(self, ranks, suits):
        self.ranks = ranks
        self.isBlackJack =  False
        self.suits = suits
        self.rank_strings = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8",
                             9: "9", 10: "10", "Jack": "Jack", "Queen": "Queen", "King": "King", "Ace": "Ace"}
        self.suit_strings = {"Spades": "Spades", "Diamonds": "Diamonds", "Clubs": "Clubs", "Hearts": "Hearts"}
        self.rank_values = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, "Jack": 10, "Queen": 10,
                            "King": 10, "Ace": 11}
        self.cards = [(self.rank_strings[rank], self.suit_strings[suit], self.rank_values[rank]) for suit in self.suits
                      for rank in self.ranks]
        self.black_jack_counter = 0
        self.sprite_size = (67, 95)
        self.card_width = 68
        self.card_height = 98

        self.sprite_sheet = pygame.image.load("images/playingcards.png")


        self.suit_index = {
            "Clubs": 0,
            "Diamonds": 1,
            "Hearts": 2,
            "Spades": 3
        }
        self.value_index = {
            "2": 0,
            "3": 1,
            "4": 2,
            "5": 3,
            "6": 4,
            "7": 5,
            "8": 6,
            "9": 7,
            "10": 8,
            "Jack": 9,
            "Queen": 10,
            "King": 11,
            "Ace": 12
        }


        self.card_value = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "jack": 10,
            "queen": 10,
            "king": 10,
            "ace": 11
        }


        for suit in self.suits:
            if "Ace" in self.ranks:
                self.cards.append(("Ace", suit, 1))
                self.cards.append(("Ace", suit, 11))
        # self.cards.append(('Joker', 'red', 0))
        # self.cards.append(('Joker', 'black', 0))

    def compute_hand_value(self, hand: List[Tuple[str, str, int]]) -> int:
        # Initialize the point value of the hand to 0
        hand_value = 0
        # Initialize a counter to track the number of aces in the hand
        num_aces = 0
        # Iterate through the cards in the hand
        for card in hand:
            if card[0] == "Ace":
                num_aces += 1
                if len(hand) == 2:
                    new_card = [card[0], card[1], 11]
                else:
                    new_card = [card[0], card[1], 1]
                hand_value += new_card[2]
            else:
                hand_value += card[2]

        while num_aces > 0 and hand_value > 21:
            hand_value -= 10
            num_aces -= 1
        # print(f"final hand_value: {hand_value}")

        if len(hand) == 2 and (
                (hand[0][0] == "Ace" and hand[1][0] in (10, "Jack", "Queen", "King")) or
                (hand[1][0] == "Ace" and hand[0][0] in (10, "Jack", "Queen", "King"))
        ):
            print("you got the black jack")
            self.black_jack_counter += 1

            print("black jack counter at:" + str(self.black_jack_counter))

        return hand_value

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position):
        return self.cards[position]

    def face_down_card(self, position: tuple[int, int]):
        top_card_position = (self.card_width * 13, 0)
        sprite = self.sprite_sheet.subsurface(pygame.Rect(top_card_position, (self.card_width, self.card_height)))
        sprite.set_colorkey((0, 190, 0))
        DISPLAY.blit(sprite, position)

    def show_card(self, suit: str, value: str, position: tuple[int, int]):
        x_offset = self.value_index[value]
        y_offset = self.suit_index[suit]
        card_position = (x_offset * self.card_width, y_offset * self.card_height)
        sprite = self.sprite_sheet.subsurface(pygame.Rect(card_position, (self.card_width, self.card_height)))
        sprite.set_colorkey((0, 190, 0))
        DISPLAY.blit(sprite, position)


    #maybe make two functions, a player draw_card and enemy draw_card
    def player_draw_card(self):
        pygame.display.update()

        card = self.cards.pop()
        player_cards_list.append((card[1], card[0]))
        # print("hidey hoe")
        # print(player_cards_list)

        # self.show_card(card[1], card[0], (self.card_width, self.card_height))
        # pygame.time.delay(500)


        return card

    def enemy_draw_card(self):
        pygame.display.update()

        card = self.cards.pop()
        enemy_cards_list.append((card[1], card[0]))
        # print("hidey hoe")
        # print(enemy_cards_list)

        # self.show_card(card[1], card[0], (self.card_width, self.card_height))
        # pygame.time.delay(500)


        return card

    def shuffle(self):

        self.cards.clear()
        self.cards = [(self.rank_strings[rank], self.suit_strings[suit], self.rank_values[rank]) for suit in self.suits
                      for rank in self.ranks]


        random.shuffle(self.cards)
        return self.cards

    def player_draw_hand(self, num_cards):
        hand = []
        for i in range(num_cards):
            hand.append(self.player_draw_card())
        return hand

    def enemy_draw_hand(self, num_cards):
        hand = []
        for i in range(num_cards):
            hand.append(self.enemy_draw_card())
        return hand

    def add_rank(self, rank):
        self.ranks.append(rank)
        self.cards = [(self.rank_strings[rank], self.suit_strings[suit]) for suit in self.suits for rank in self.ranks]

    def add_suit(self, suit):
        self.suits.append(suit)
        self.cards = [(self.rank_strings[rank], self.suit_strings[suit]) for suit in self.suits
                      for rank in self.ranks]






class TextBox(Entity):
    def __init__(self, messages: list[str], rect: tuple[int, int, int, int], font_size: int, delay: int,):
        super().__init__(rect[0], rect[1], rect[2], rect[3])
        self.messages = messages
        self.message_index = 0
        self.text = self.messages[self.message_index]
        self.characters_to_display = 0
        self.font_size = font_size
        self.delay = delay
        self.time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 36)


    def update(self, state: "GameState"):
        controller = state.controller

        # show characters of text one at a time, not whole message.
        if self.characters_to_display < len(self.text):
            self.characters_to_display += 1

        # handle button press to see next message
        if controller.isTPressed and \
                pygame.time.get_ticks() - self.time > self.delay and \
                self.message_index < len(self.messages) - 1:
            pygame.time.delay(650)


            self.time = pygame.time.get_ticks()
            self.message_index += 1
            self.text = self.messages[self.message_index]
            self.characters_to_display = 0
            state.controller.isTPressed = False


        # print("is finished? " + str(self.is_finished()))

    def draw(self, state: "GameState"):
        text_to_display = self.text[:self.characters_to_display]
        wrapped_text = textwrap.wrap(text_to_display, 60)
        for i, line in enumerate(wrapped_text):
            text_surface = self.font.render(line, True, (255, 255, 255))
            DISPLAY.blit(text_surface, (self.position.x, self.position.y + (i * 40)))

    def is_finished(self) -> bool:
        return self.message_index == len(self.messages) - 1 and \
            pygame.time.get_ticks() - self.time > self.delay


class BorderedBox(Entity):
    def __init__(self, rect: tuple[int, int, int, int], border_width: int = 5):
        super().__init__(rect[0], rect[1], rect[2], rect[3])
        self.border_width = border_width

    def update(self, state: "GameState"):
        pass

    def draw(self, state: "GameState"):
        # draw text box border
        black_box = pygame.Surface((self.collision.width, self.collision.height))
        black_box.fill((0, 0, 0))
        # Create the white border
        white_border = pygame.Surface((self.collision.width + 2 * self.border_width, self.collision.height + 2 * self.border_width))
        white_border.fill((255, 255, 255))
        black_box = pygame.Surface((self.collision.width, self.collision.height))
        black_box.fill((0, 0, 0))
        white_border.blit(black_box, (self.border_width, self.border_width))
        DISPLAY.blit(white_border, (self.position.x, self.position.y))

# demonstrating encapsulation
class BorderedTextBox(Entity):
    def __init__(self, messages: list[str], rect: tuple[int, int, int, int], font_size: int, delay: int):
        super().__init__(rect[0], rect[1], rect[2], rect[3])
        self.border_box = BorderedBox(rect)
        padding = self.border_box.border_width + 10
        text_box_rect = (rect[0] + padding, rect[1] + padding, rect[2] - padding * 2, rect[3] - padding * 2)
        self.text_box = TextBox(messages, text_box_rect, font_size, delay)

    def update(self, state: "GameState"):
        self.border_box.update(state)
        self.text_box.update(state)

    def draw(self, state: "GameState"):
        self.border_box.draw(state)
        self.text_box.draw(state)

    def is_finished(self) -> bool:
        return self.text_box.is_finished()


class BlackJackScreen(Screen, Deck, TextBox):
    def __init__(self, ranks, suits):
        Screen.__init__(self, " Black Jack Game")
        Deck.__init__(self, ranks, suits)

        self.font = pygame.font.Font(None, 36)
        self.black_ace = False # this is our boss level when talk to NPC set to true set false if game is set to quit
        self.ace_up_sleeve_jack = False
        self.ace_up_sleeve_jack_cheat_mode = False
        self.first_message_display = ""
        self.second_message_display = ""
        self.third_message_display = ""
        self.game_state = "welcome_screen"
        self.bet = 10
        self.cheater_bob_money = 1000
        self.player_score = 0
        self.enemy_score = 0
        self.player_hand = []
        self.enemy_hand = []
        self.choices = ["Ready", "Draw", "Redraw"]
        self.current_index = 0
        self.welcome_screen_choices = ["Play", "Magic", "Quit"]
        self.welcome_screen_index = 0
        self.magic_menu_selector = ["Bluff", "Reveal", "Lucky", "Back"]
        self.magic_menu_index = 0
        self.ace_value = 1
        self.bust_protection = False
        self.avatar_of_luck_card_redraw_counter = 3

        self.player_black_jack_win = False
        self.enemy_black_jack_win = False
        self.black_jack_draw = False

        self.current_speaker = ""
        self.npc_speaking = False
        self.hero_speaking = False
        self.music_loop = True

        self.despair = False
        # self.despair = True

        self.hero_losing_text_state = False
        self.hero_winning_text_state = False
        self.player_status = ""
        self.enemy_status = ""



        self.black_jack_bluff_counter = 0
        self.reveal_hand = 11
        self.magic_lock = False
        self.luck_of_jack = 7
        self.avatar_of_luck = False
        self.redraw_lock = False
        #maybe include a self.turn_counter = 0 that can be +1 in our welcome screen in conjection with our reveal spell
        # incldue a double bet spell that is CHR based that player gets for free maybe4

        self.locked_text = self.font.render("Locked", True, (255, 255, 255))

        self.messages = {
            "welcome_screen": ["Cheater Bob: My name's Cheater Bob. I promise it's the name my parents gave me.", ""],
            "hero_intro_text": ["I can press up and down to select. Play to start, quit to leave, or magic for an advantage"],

            "bet_intro_text": ["Cheater Bob: Min Bet is 10 and Max Bet is 100. The more you bet the more your  stamina is drained "],

            "hero_losing_text": ["Hero: This isn't good, I'll need to get serious if I want to make a comeback.","Maybe I should lower my bet until I get the hang of my enemy", ""],
            "enemy_winning_text": ["Cheater Bob: HA HA HA HA! Do you know what happens to people that lose all their coins?","You might as well just give me all your coins.", ""],
            "hero_losing_confused_text": ["Hero: ........Either he's good at bluffing or he's serious,or just flat out crazy","This casino keeps getting stranger....I need to put it out of my mind ,focus, and regain my composure.", "You know what Cheater Bob, This entire place is strange, I believe you! ", "....BRING IT ON!!!",""],



            "enemy_losing_text": ["Cheater Bob: How is this possible? I'm....Cheater Bob...I'm not supposed to lose.",
                                 "Your Cheating! There is no way I'd lose to an amateur like you", ""],
            "hero_winning_text": ["Hero: I never cheat Cheater Bob. I'm just that good. Why are you sweating so much for?",
                                   "Care to tell me why your so worried? Is it that stupid chilli swimming lie I keep hearing about? I mean come on, the joke's already getting old with me",
                                   ""],
            "enemy_losing_confused_text": ["Cheater Bob: It's not a lie you fool!",
                                          ".......",
                                          "If you take all my coins, and if the boss doesn't give me replacement coins..........",
                                          "NO!!! I won't end up like the others....I won't have you make a fool out of me.....",""],


            "final_strike_text": ["Hero: You don't have a lot of coins left.I'll bet you the rest that my next hand will be a black jack.",
                               "Of course, if you happen to win you'll be back in the game, sounds pretty nice of me right?","",
                              ],
            "enemy_bluffed_text": ["Cheater Bob: Do you Realize the odds of that happening? Why would you take such a bet for?",
                               "It doesn't make any sense",
                              ""],



            "hero_bluffing_text": ["Hero: Well it's simple really, based on the card positions, and the way you shuffled ",
                               "I can pretty easily tell where each card landed in the deck",
                               "Simply put, I'm not doing a random bet, or a bluff, when you deal out the cards, I will get a black jack. It's all about my intellect and high perception", ""],
            "enemy_falling_for_bluff_text": ["Cheater Bob: That's bull crap, there's no way you have that much perception  ",
                               "I'll take your bet, and then I'll tell everyone how much of a fool you are",
                               "I'll teach you to underestimate me", ""],

            "enemy_crying_text": ["Cheater Bob: Impossible...how did you????",
                             ""],
            "hero_reveal_text": ["Hero: To be honest, it was all a bluff, you were right all along.",
                               "However, I never bet against myself, and because of that lady luck is always on my side",
                               "You lost,not because I cheated, but  because you didnt' believe in yourself and gave in to despair", ""],

            "bluff_magic_explain": ["Casts Bluff on the enemy. When the enemy seems desperate this will be unlocked. Enemy less likely to hit due to fear of a bust. Magic Lock Permanent .25MP"],
            "reveal_magic_explain": ["Based on muscle twitches of enemy plus the way they shuffle cards, you can tell what score they have.Protects you from busts. Magic lock 10 turns.25MP"],
            "avatar_magic_explain": ["Your faith is so strong that lady luck herself blesses you. Allows up to 3 redraws per turn.Deck is not reshuffled and cards are burned.Magic lock 5 turns 25MP"],
            "back_magic_explain": ["Back to previous menu"],

        }

        self.welcome_screen_text_box = TextBox(self.messages["welcome_screen"], (50, 450, 50, 45), 30, 500)
        self.welcome_screen_text_box_hero = TextBox(self.messages["hero_intro_text"], (50, 450, 50, 45), 30, 500)

        self.bet_screen_text = TextBox(self.messages["bet_intro_text"], (50, 450, 50, 45), 30, 500)
        self.hero_losing_money_text = TextBox(self.messages["hero_losing_text"], (50, 450, 50, 45), 30, 500)
        self.enemy_losing_money_text = TextBox(self.messages["enemy_losing_text"], (50, 450, 50, 45), 30, 500)

        self.enemy_winning_money_text = TextBox(self.messages["enemy_winning_text"], (50, 450, 50, 45), 30, 500)
        self.hero_winning_money_text = TextBox(self.messages["hero_winning_text"], (50, 450, 50, 45), 30, 500)

        self.hero_losing_confused_money_text = TextBox(self.messages["hero_losing_confused_text"], (50, 450, 50, 45), 30, 500)
        self.enemy_losing_confused_money_text = TextBox(self.messages["enemy_losing_confused_text"], (50, 450, 50, 45), 30, 500)

        self.final_strike_text_component = TextBox(self.messages["final_strike_text"], (50, 450, 50, 45), 30, 500)
        self.enemy_bluffed_text_component = TextBox(self.messages["enemy_bluffed_text"], (50, 450, 50, 45), 30, 500)

        self.hero_bluffing_text_component = TextBox(self.messages["hero_bluffing_text"], (50, 450, 50, 45), 30, 500)
        self.enemy_falling_for_bluff_text_component = TextBox(self.messages["enemy_falling_for_bluff_text"], (50, 450, 50, 45), 30, 500)

        self.enemy_crying_text_component = TextBox(self.messages["enemy_crying_text"], (50, 450, 50, 45), 30, 500)
        self.hero_reveal_text_component = TextBox(self.messages["hero_reveal_text"], (50, 450, 50, 45), 30, 500)

        self.bluff_magic_explain_component = TextBox(self.messages["bluff_magic_explain"], (50, 450, 50, 45), 30, 500)
        self.reveal_magic_explain_component = TextBox(self.messages["reveal_magic_explain"], (50, 450, 50, 45), 30, 500)
        self.avatar_magic_explain_component = TextBox(self.messages["avatar_magic_explain"], (50, 450, 50, 45), 30, 500)
        self.back_magic_explain_component = TextBox(self.messages["back_magic_explain"], (50, 450, 50, 45), 30, 500)




        # self.bordered_text_box = BorderedTextBox(self.messages["list2"], (230, 200, 250, 45), 30, 500)
        self.main_bordered_box = BorderedBox((25, 425, 745, 150))

        #DO NOT DELETE THIS CODE
        mixer.init()

        # Load audio file
        mixer.music.load('audio/8-Bit-Espionage_Looping.mp3')

        print("music started playing....")

        # Set preferred volume
        mixer.music.set_volume(0.2)

        # Play the music
        pygame.mixer.music.play(-1, 0.0, 5000)

        pygame.init()




    pygame.init()

    def place_bet(self, state: "GameState"):
        if state.controller.isUpPressed:
            self.bet += 10
            pygame.time.delay(100)
            state.controller.isUpPressed = False

        elif state.controller.isDownPressed:
            self.bet -= 10
            pygame.time.delay(100)
            state.controller.isDownPressed = False

        if self.bet < 10:
            self.bet = 10

        if self.bet > 100:
            self.bet = 100



    def update(self, state: "GameState"):


        # print("update() - state: " + str(self.game_state) + ", start at: " )
        # pygame.time.wait(100)

        controller = state.controller
        controller.update(state)
        state.player.update(state)

        #
        # print("p: " + self.hand_to_str(self.player_hand))
        # print("e: " + self.hand_to_str(self.enemy_hand))

        if self.game_state == "welcome_screen":
            # NOTE NOTE NOTE NOTE NOTE NOTE NOTE
            # if enemy hits 1000 coins, desperate lock needs to go away for future ref so that despiar ends and player can use magic again
            if self.cheater_bob_money >= 1300 and self.hero_losing_text_state == False:
                self.game_state = "hero_is_desperate_state"

            elif self.cheater_bob_money <= 300 and self.despair == True:
                self.game_state = "final_strike_screen"

            elif self.cheater_bob_money <= 500 and self.hero_winning_text_state == False:
                self.game_state = "enemy_is_desperate_state"


            # if self.cheater_bob_money == 1000 and self.hero_losing_text == False:
            #     self.bet_screen_text = TextBox(self.messages["hero_losing_text"], (50, 400, 50, 45), 30, 500)
            #     self.hero_losing_text = True
            if state.player.stamina_points < 1:
                print("time to leave")

            self.welcome_screen_text_box.update(state)

            self.npc_speaking = True
            self.hero_speaking = False



            # self.second_message_display = "Press the T key, which is our action key"
            # self.third_message_display = "To go forward with the game"
            self.redraw_lock = False
            self.ace_up_sleeve_jack_cheat_mode = False
            self.bust_protection = False
            self.avatar_of_luck_card_redraw_counter = 3
            self.current_index = 0
            self.enemy_score = 0
            global player_cards_list
            global enemy_cards_list

            player_cards_list.clear()
            enemy_cards_list.clear()

            if self.welcome_screen_text_box.is_finished():
                self.npc_speaking = False
                self.hero_speaking = True
                self.welcome_screen_text_box_hero.update(state)



                if self.welcome_screen_text_box_hero.is_finished():

                    if controller.isUpPressed:
                        channel3 = pygame.mixer.Channel(3)
                        sound3 = pygame.mixer.Sound("audio/Fotstep_Carpet_Right_3.mp3")
                        channel3.play(sound3)
                        if not hasattr(self, "welcome_screen_index"):
                            self.welcome_screen_index = len(self.welcome_screen_choices) - 1
                        else:
                            self.welcome_screen_index -= 1
                        self.welcome_screen_index %= len(self.welcome_screen_choices)
                        controller.isUpPressed = False

                    elif controller.isDownPressed:
                        channel3 = pygame.mixer.Channel(3)
                        sound3 = pygame.mixer.Sound("audio/Fotstep_Carpet_Right_3.mp3")
                        channel3.play(sound3)
                        if not hasattr(self, "welcome_screen_index"):
                            self.welcome_screen_index = len(self.welcome_screen_choices) + 1
                        else:
                            self.welcome_screen_index += 1
                        self.welcome_screen_index %= len(self.welcome_screen_choices)
                        controller.isDownPressed = False

        elif self.game_state ==  "hero_is_desperate_state":
            self.npc_speaking = False
            self.hero_speaking = True
            self.hero_losing_money_text.update(state)

            self.hero_losing_text_state = True

            if self.hero_losing_money_text.is_finished():
                self.npc_speaking = True
                self.hero_speaking = False
                self.enemy_winning_money_text.update(state)
                if self.enemy_winning_money_text.is_finished():
                    self.npc_speaking = False
                    self.hero_speaking = True
                    self.hero_losing_confused_money_text.update(state)
                    if self.hero_losing_confused_money_text.is_finished():
                        self.game_state = "welcome_screen"

                # if self.enemy_winning_money_text.is_finished():
                #     self.game_state = "welcome_screen"
        elif self.game_state == "enemy_is_desperate_state":
            self.npc_speaking = True
            self.hero_speaking = False
            self.enemy_losing_money_text.update(state)

            self.hero_winning_text_state = True

            if self.enemy_losing_money_text.is_finished():
                self.npc_speaking = False
                self.hero_speaking = True
                self.hero_winning_money_text.update(state)
                if self.hero_winning_money_text.is_finished():
                    self.npc_speaking = True
                    self.hero_speaking = False
                    self.enemy_losing_confused_money_text.update(state)
                    if self.enemy_losing_confused_money_text.is_finished():
                        self.game_state = "welcome_screen"

        elif self.game_state == "final_strike_screen":
            #NOTE NOTE NOTE NOTE NOTE NOTE NOTE
            # if enemy hits 1000 coins, desperate lock needs to go away for future ref
            self.npc_speaking = False
            self.hero_speaking = True
            self.final_strike_text_component.update(state)
            if self.final_strike_text_component.is_finished():
                self.npc_speaking = True
                self.hero_speaking = False
                self.enemy_bluffed_text_component.update(state)
                if self.enemy_bluffed_text_component.is_finished():
                    self.npc_speaking = False
                    self.hero_speaking = True
                    self.hero_bluffing_text_component.update(state)
                    if self.hero_bluffing_text_component.is_finished():
                        self.npc_speaking = True
                        self.hero_speaking = False
                        self.enemy_falling_for_bluff_text_component.update(state)
                        if self.enemy_falling_for_bluff_text_component.is_finished():
                            #this is how we hard code
                            # self.player_hand = [('10', 'Diamonds', 10), ('Ace', 'Spades', 11)]
                            # player_cards_list = [ ('Diamonds', '10'), ('Spades', 'Ace')]
                            while self.player_score <= 20:
                                self.shuffle()
                                self.player_hand = self.player_draw_hand(2)
                                self.enemy_hand = self.enemy_draw_hand(2)
                                print("Player hand is" + str(self.player_hand))
                                self.player_score = self.compute_hand_value(self.player_hand)
                                # print(self.player_score)
                                if self.player_score > 20:
                                    player_cards_list[:-2] = []
                                    enemy_cards_list[:-2] = []
                                    print(player_cards_list)


                            print("out of the loop")
                            self.npc_speaking = True
                            self.hero_speaking = False
                            self.enemy_crying_text_component.update(state)
                            if self.enemy_crying_text_component.is_finished():
                                self.npc_speaking = False
                                self.hero_speaking = True
                                self.hero_reveal_text_component.update(state)
                                state.player.playerMoney += self.cheater_bob_money
                                self.cheater_bob_money = 0
                                if self.hero_reveal_text_component.is_finished():
                                    player_cards_list = []
                                    enemy_cards_list = []
                                    pygame.quit()














        elif self.game_state == "bet_phase":

            self.bet_screen_text.update(state)

            self.npc_speaking = True
            self.hero_speaking = False



            self.third_message_display = " "
            self.place_bet(state)
            if controller.isTPressed:
                if self.bet > 70:
                    state.player.stamina_points -= 3
                    print("-3")
                elif (self.bet < 30):

                    state.player.stamina_points -= 1

                    print("-1")
                elif (self.bet < 70) or (self.bet > 20):
                    state.player.stamina_points -= 2
                    print("-2")

                pygame.time.wait(300)
                self.game_state = "draw_phase"
                controller.isTPressed = False

        elif self.game_state == "draw_phase":
            # need to reformat have a reset function
            self.first_message_display = ""
            self.second_message_display = ""
            self.thrid_message_display = ""
            self.black_jack_counter = 0
            self.player_black_jack_win = False
            self.enemy_black_jack_win = False
            self.black_jack_draw = False
            self.player_hand = self.player_draw_hand(2)
            print("Player hand is" + str(self.player_hand))
            self.player_score = self.compute_hand_value(self.player_hand)





            print("Player score is: " + str(self.player_score))


            # Check if the player has an ACE in their hand
            if self.black_jack_counter > 0:
                print("Player black jack win set to true and it might be true?")
                self.player_black_jack_win = True
                self.black_jack_bluff_counter += 1
            else:
                self.player_black_jack_win = False

            #################################need to test aces if a player gets multiple aces



            # If the player has an ACE, check which value is better for the player



            self.enemy_hand = self.enemy_draw_hand(2)
            print("Enemy hand is" + str(self.enemy_hand))
            self.enemy_score = self.compute_hand_value(self.enemy_hand)
            print("enemy score is: " + str(self.enemy_score))

            if self.black_jack_counter > 0:
                print("Enemy black jack win set to true and the code is right here")

                self.enemy_black_jack_win = True
            elif self.black_jack_counter == 0:
                self.enemy_black_jack_win = False

            print(self.player_black_jack_win)

            if self.black_ace == True:
                if self.enemy_score < 7:
                    self.enemy_hand = self.enemy_draw_hand(2)
                    print("Enemy hand is" + str(self.enemy_hand))
                    print("You get the sense the enemy is somewhat lucky")
                    self.enemy_score = self.compute_hand_value(self.enemy_hand)
                    print("enemy score is: " + str(self.enemy_score))
                    if self.black_jack_counter > 0:
                        print("Enemy black jack win set to true")

                        self.enemy_black_jack_win = True
                    elif self.black_jack_counter == 0:
                        self.enemy_black_jack_win = False

                    print(self.player_black_jack_win)


            if self.player_black_jack_win == True and self.enemy_black_jack_win == True:
                self.black_jack_draw = True
                self.thrid_message_display = "Its a draw"
                print("Its a draw")
                self.game_state = "results_screen"
            elif self.player_black_jack_win == True and self.enemy_black_jack_win == False:

                print("its time for you to have double winnings")
                # state.player.playerMoney += self.bet
                # state.player.playerMoney += self.bet
                # self.cheater_bob_money -= self.bet
                # self.cheater_bob_money -= self.bet
                self.game_state = "results_screen"
            elif self.player_black_jack_win == False and self.enemy_black_jack_win == True:
                print("THE ENEMY HAS A BLAK Jack SORRRYYYYYY")
                # state.player.playerMoney -= self.bet
                # state.player.playerMoney -= self.bet
                # self.cheater_bob_money += self.bet
                # self.cheater_bob_money += self.bet

                self.game_state = "results_screen"

            else:
                self.game_state = "menu_screen"








        elif self.game_state == "player_draw_one_card":
            self.player_hand += self.player_draw_hand(1)
            self.compute_hand_value(self.player_hand)
            self.player_score = self.compute_hand_value(self.player_hand)

            if self.player_score > 10:
                print("hi greater than 10")
                self.rank_values["Ace"] = 1

            print("Player hand is now" + str(self.player_hand))
            print("Player score is now" + str(self.player_score))
            if self.player_score > 21 and self.reveal_hand > 10:
                state.player.playerMoney -= self.bet
                self.cheater_bob_money += self.bet
                self.second_message_display = "player bust you lose"
                self.game_state = "results_screen"

            elif self.player_score > 21 and self.reveal_hand < 11:
                print("you almost busted")
                print(self.player_hand)
                self.player_hand.pop()
                self.compute_hand_value(self.player_hand)
                self.player_score = self.compute_hand_value(self.player_hand)
                print("here is your new hand")
                print(self.player_hand)
                self.reveal_hand -= 2
                self.bust_protection = True



            if self.bust_protection == True:
                self.game_state = "results_screen"
            else:
                self.game_state = "menu_screen"

        elif self.game_state == "enemy_draw_one_card":
            print("this is the start of enemy draw one card")
            while self.enemy_score < 15:    # this is 15 in order to make game a little easier
                print("thi sis our while loop")


                self.enemy_hand += self.enemy_draw_hand(1)
                self.compute_hand_value(self.enemy_hand)
                self.enemy_score = self.compute_hand_value(self.enemy_hand)
                print("enemy hand is now" + str(self.enemy_hand))
                print("enemy score is now" + str(self.enemy_score))
                self.game_state = "results_screen"



                if self.enemy_score > 21:
                    print("if the enemy is going to bust")
                    state.player.playerMoney += self.bet
                    self.cheater_bob_money -= self.bet
                    print("enemy bust")
                    self.second_message_display = "enemy bust player wins"
                    self.game_state = "results_screen"

            if self.enemy_score > 14 and self.enemy_score < 22:
                print("stay here")
                self.game_state = "results_screen"

        elif self.game_state == "enemy_despair_draw_one_card":
            print("enemy is in despair")
            while self.enemy_score < 14:  # this is 15 in order to make game a little easier
                print("this is our despair loop")

                self.enemy_hand += self.enemy_draw_hand(1)
                self.compute_hand_value(self.enemy_hand)
                self.enemy_score = self.compute_hand_value(self.enemy_hand)
                print("enemy hand is now" + str(self.enemy_hand))
                print("enemy score is now" + str(self.enemy_score))
                self.game_state = "results_screen"

                if self.enemy_score > 21:
                    print("if the enemy is going to bust")
                    state.player.playerMoney += self.bet
                    self.cheater_bob_money -= self.bet
                    print("enemy bust")
                    self.second_message_display = "enemy bust player wins"
                    self.game_state = "results_screen"

            if self.enemy_score > 14 and self.enemy_score < 22:
                print("stay here")
                self.game_state = "results_screen"




        elif self.game_state == "menu_screen":




            if self.player_score > 21:
                self.message_display = "You bust and lose."
                # state.player.playerMoney -= self.bet
                # self.cheater_bob_money += self.bet
                self.game_state = "results_screen"

            if controller.isUpPressed:
                channel3 = pygame.mixer.Channel(3)
                sound3 = pygame.mixer.Sound("audio/Fotstep_Carpet_Right_3.mp3")
                channel3.play(sound3)
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) - 1
                else:
                    self.current_index -= 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isUpPressed = False

            if controller.isDownPressed:
                channel3 = pygame.mixer.Channel(3)
                sound3 = pygame.mixer.Sound("audio/Fotstep_Carpet_Right_3.mp3")
                channel3.play(sound3)
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) + 1
                else:
                    self.current_index += 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isDownPressed = False

            if self.current_index == 2 and state.controller.isTPressed and self.avatar_of_luck == True and self.redraw_lock == False:
                print("Redrawing your hand")
                player_cards_list.clear()
                # enemy_cards_list.clear()

                self.player_hand = self.player_draw_hand(2)
                print("Player hand is" + str(self.player_hand))
                print("Enemy hand is" + str(self.enemy_hand))
                print("player card list is " + str(player_cards_list))
                print("enemy card list is " + str(enemy_cards_list))
                self.player_score = self.compute_hand_value(self.player_hand)
                self.avatar_of_luck_card_redraw_counter -= 1


                if self.avatar_of_luck_card_redraw_counter < 1:
                    self.redraw_lock = True

                # deck = Deck(ranks, suits)
                # player_card_x = 235
                # player_card_y = 195
                # enemy_card_x = 235
                # enemy_card_y = 15
                #
                # for i, card in enumerate(player_cards_list):
                #     if i > 3:
                #         player_card_y = 305
                #         player_card_x = 235
                #     deck.show_card(card[0], card[1], (player_card_x, player_card_y))
                #     player_card_x += 75

                self.game_state = "menu_screen"
                state.controller.isTPressed = False



                # 534534543535353525532535353354

        elif self.game_state == "magic_menu":


            self.message_display = "Pick a magic spell and wreck havic. Press K to cast"

            if controller.isUpPressed:
                channel3 = pygame.mixer.Channel(3)
                sound3 = pygame.mixer.Sound("audio/Fotstep_Carpet_Right_3.mp3")
                channel3.play(sound3)
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) - 1
                else:
                    self.magic_menu_index -= 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                channel3 = pygame.mixer.Channel(3)
                sound3 = pygame.mixer.Sound("audio/Fotstep_Carpet_Right_3.mp3")
                channel3.play(sound3)
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) + 1
                else:
                    self.magic_menu_index += 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isDownPressed = False



            # we need to make this work right after a black jack
            # set a counter to minus 1 this is the counter is above 0
            if self.magic_menu_index == 0:
                self.bluff_magic_explain_component.update(state)

                if controller.isTPressed and self.cheater_bob_money <= 900 and state.player.focus_points > 24:
                    pygame.time.delay(300)
                    state.player.focus_points -= 25
                    self.despair = True
                    self.magic_lock = True
                    self.player_status = "Bluffalo"
                    self.enemy_status = "Despair"
                    self.game_state = "welcome_screen"
                    state.controller.isTPressed = False







            elif self.magic_menu_index == 1:
                self.reveal_magic_explain_component.update(state)


                if controller.isTPressed:
                    pygame.time.delay(300)
                    if state.player.focus_points >= 10:
                        state.player.focus_points -= 10
                        self.reveal_hand = 10
                        self.magic_lock = True
                        self.player_status = "Focus"
                        self.enemy_status = "Reveal"
                        self.isTPressed = False



                        print("You cast reveal")
                        self.game_state = "welcome_screen"


                    elif state.player.focus_points < 10:
                        self.third_message_display = "Sorry but you dont have enough focus points to cast"
                # elif self.luck_activated > 0:
                #     self.third_message_display = "sorry but you can't stack magic spells"





            ##########################have a message state reserved for buff states

            ##### boss enemies will use magic under more strict conditions
            elif self.magic_menu_index == 2:
                self.avatar_magic_explain_component.update(state)

                if controller.isTPressed:
                    pygame.time.delay(300)
                    print("you cast avatar of luck")
                    self.luck_of_jack = 6
                    self.magic_lock = True
                    self.avatar_of_luck = True
                    state.player.focus_points -= 20
                    self.game_state = "welcome_screen"
                    self.player_status = "Lucky"
                    state.controller.isTPressed = False


            elif self.magic_menu_index == 3:
                self.back_magic_explain_component.update(state)

                if controller.isTPressed:
                    pygame.time.delay(300)

                    self.game_state = "welcome_screen"
                    self.isTPressed = False







        elif self.game_state == "results_screen":




            if self.player_black_jack_win == True and self.enemy_black_jack_win == False:
                self.second_message_display = "You win with a black jack press T when ready"
                if state.player.level == 1:
                    self.first_message_display = f"You gain 50 exp and {self.bet * 2} gold "
                elif state.player.level == 2:
                    self.first_message_display = f"You gain 25 exp and {self.bet * 2} gold "




            elif self.player_black_jack_win == True and self.enemy_black_jack_win == True:
                self.second_message_display = "It's a draw press T when ready"
                if state.player.level == 1:
                    self.first_message_display = f"You gain 50 exp and 0 gold "
                elif state.player.level == 2:
                    self.first_message_display = f"You gain 25 exp and 0 gold "


            elif self.player_black_jack_win == False and self.enemy_black_jack_win == True:
                self.second_message_display = "Enemy gets blackjack you lose "
                if state.player.level == 1:
                    self.first_message_display = f"You gain 100 exp and 0 gold "
                elif state.player.level == 2:
                    self.first_message_display = f"You gain 50 exp and 0 gold "



            elif self.player_score > self.enemy_score and self.player_score < 22:
                self.second_message_display = "You win player press T when ready"
                if state.player.level == 1:
                    self.first_message_display = f"You gain 25 exp and {self.bet} gold "
                elif state.player.level == 2:
                    self.first_message_display = f"You gain 12 exp and {self.bet} gold "




            elif self.player_score < self.enemy_score and self.enemy_score < 22:
                self.second_message_display = "You lose player press T when ready"
                if state.player.level == 1:
                    self.first_message_display = f"You gain 50 exp and lose {self.bet} gold "
                elif state.player.level == 2:
                    self.first_message_display = f"You gain 25 exp and lose {self.bet} gold "




            elif self.player_score == self.enemy_score:
                self.second_message_display = "It's a draw nobody wins press T when Ready"
                if state.player.level == 1:
                    self.first_message_display = f"You gain 25 exp and 0 gold "
                elif state.player.level == 2:
                    self.first_message_display = f"You gain 12 exp and 0 gold "


            if controller.isTPressed:

                # Load audio file
                channel2 = pygame.mixer.Channel(1)
                sound2 = pygame.mixer.Sound("audio/Coins1.mp3")
                channel2.play(sound2)

                if self.player_black_jack_win == True and self.enemy_black_jack_win == False:
                    state.player.playerMoney += self.bet * 2
                    self.cheater_bob_money -= self.bet * 2
                    if state.player.level == 1:
                        state.player.exp += 50

                    elif state.player.level == 2:
                        self.first_message_display = f"You gain 12 exp and {self.bet * 2} gold "

                        state.player.exp += 25


                elif self.player_black_jack_win == True and self.enemy_black_jack_win == True:
                    if state.player.level == 1:
                        self.first_message_display = f"You gain 50 exp and 0 gold "

                        state.player.exp += 75
                    elif state.player.level == 2:
                        self.first_message_display = f"You gain 25 exp and 0 gold "

                        state.player.exp += 33


                elif self.player_black_jack_win == False and self.enemy_black_jack_win == True:
                    state.player.playerMoney -= self.bet * 2
                    self.cheater_bob_money += self.bet * 2
                    if state.player.level == 1:
                        state.player.exp += 100

                    elif state.player.level == 2:
                            state.player.exp += 50



                elif self.player_score > self.enemy_score and self.player_score < 22:
                    self.second_message_display = "You win player press T when ready"

                    state.player.playerMoney += self.bet
                    self.cheater_bob_money -= self.bet
                    if state.player.level == 1:
                        self.first_message_display = f"You gain 25 exp and {self.bet} gold "

                        state.player.exp += 25

                    elif state.player.level == 2:
                        self.first_message_display = f"You gain 12 exp and {self.bet} gold "

                        state.player.exp += 12


                elif self.player_score < self.enemy_score and self.enemy_score < 22:
                    self.second_message_display = "You lose player press T when ready"
                    state.player.playerMoney -= self.bet
                    self.cheater_bob_money += self.bet
                    if state.player.level == 1:
                        self.first_message_display = f"You gain 50 exp and lose {self.bet} gold "

                        state.player.exp += 50
                    elif state.player.level == 2:
                        self.first_message_display = f"You gain 25 exp and lose {self.bet} gold "

                        state.player.exp += 25



                elif self.player_score == self.enemy_score:
                    self.second_message_display = "It's a draw nobody wins press T when Ready"

                    if state.player.level == 1:
                        self.first_message_display = f"You gain 25 exp and 0 gold "

                        state.player.exp += 25

                    elif state.player.level == 2:
                        self.first_message_display = f"You gain 12 exp and 0 gold "

                        state.player.exp += 12


                if self.reveal_hand < 11 :
                    self.reveal_hand -= 1

                if self.reveal_hand == 0:
                    print("Magic time")
                    self.reveal_hand = 11
                    self.magic_lock = False

                if self.luck_of_jack < 7:
                    self.luck_of_jack -= 1

                if self.luck_of_jack == 0:
                    print("Magic time")
                    self.luck_of_jack = 6
                    self.avatar_of_luck = False
                    self.magic_lock = False


                pygame.time.wait(300)
                print("Hey there going to the welcome_screen")

                self.game_state = "welcome_screen"
                controller.isTPressed = False




    def hand_to_str(self, hand) -> str:
        msg = ""
        i = 0
        for card in hand:
            if i > 0:
                msg += ", "
            msg += card[0] + " " + card[1]
            i += 1
        return msg





    def draw(self, state: "GameState"):
        # change to dealer image
        character_image = pygame.image.load("images/128by128.png")
        hero_image = pygame.image.load("images/hero.png")


        DISPLAY.fill((0, 0, 51))


        black_box = pygame.Surface((200 - 10, 180 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        DISPLAY.blit(white_border, (25, 235))

        black_box = pygame.Surface((200 - 10, 45 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 45 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        DISPLAY.blit(white_border, (25, 195))



        DISPLAY.blit(self.font.render(f"Money:{state.player.playerMoney}", True, (255, 255, 255)), (37, 240))
        DISPLAY.blit(self.font.render(f"HP:{state.player.stamina_points}", True, (255, 255, 255)), (37, 275))
        DISPLAY.blit(self.font.render(f"Exp:{state.player.exp}", True, (255, 255, 255)), (111, 315))

        DISPLAY.blit(self.font.render(f"MP:{state.player.focus_points}", True, (255, 255, 255)), (37, 315))
        DISPLAY.blit(self.font.render(f"Status:{self.player_status}", True, (255, 255, 255)), (37, 355))
        DISPLAY.blit(self.font.render(f"Bet:{self.bet}", True, (255, 255, 255)), (37, 385))
        DISPLAY.blit(self.font.render(f"Hero", True, (255, 255, 255)), (37, 205))


        black_box = pygame.Surface((200 - 10, 110 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 110 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        DISPLAY.blit(white_border, (25, 20))

        black_box = pygame.Surface((200 - 10, 110 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 110 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        DISPLAY.blit(white_border, (25, 60))


        DISPLAY.blit(self.font.render(f"Money:{self.cheater_bob_money}", True, (255, 255, 255)), (37, 80))
        DISPLAY.blit(self.font.render(f"Status:{self.enemy_status}", True, (255, 255, 255)), (37, 110))
        if self.reveal_hand < 11:
            DISPLAY.blit(self.font.render(f"Score:{self.enemy_score}", True, (255, 255, 255)),
                         (37, 140))
        DISPLAY.blit(self.font.render(f"Cheater Bob", True, (255, 255, 255)), (37, 30))



        #
        # DISPLAY.blit(
        #     self.font.render(f"Hero Money:{state.player.playerMoney}", True, (255, 255, 255)),
        #     (55, 260))

        # if self.npc_speaking == True:
        #     DISPLAY.blit(character_image, (23, 245))
        #
        #     self.current_speaker = "cheater bob"
        # elif self.hero_speaking == True:
        #     DISPLAY.blit(hero_image, (23, 245))
        #
        #     self.current_speaker = "hero"
        #     DISPLAY.blit(self.font.render(f"{self.current_speaker}", True, (255, 255, 255)), (155, 350))



        self.main_bordered_box.draw(state)
        DISPLAY.blit(character_image, (650, 15))
        DISPLAY.blit(self.font.render(f"Cheater Bob", True, (255, 255, 255)), (650, 145))


        # self.face_down_card((0,0))









        if self.game_state == "welcome_screen":
            #
            black_box = pygame.Surface((160 - 10, 180 - 10))
            black_box.fill((0, 0, 0))
            border_width = 5
            white_border = pygame.Surface((160 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
            white_border.fill((255, 255, 255))
            white_border.blit(black_box, (border_width, border_width))
            DISPLAY.blit(white_border, (620 , 235))



            DISPLAY.blit(
                self.font.render(f"{self.welcome_screen_choices[0]}", True, (255, 255, 255)),
                (687, 260))





            if self.magic_lock == False:

                DISPLAY.blit(
                    self.font.render(f"{self.welcome_screen_choices[1]}", True, (255, 255, 255)),
                    (687, 310))
            elif self.magic_lock == True:
                DISPLAY.blit(self.font.render("Locked", True, (255, 255, 255)), (680, 315))


            DISPLAY.blit(
                self.font.render(f"{self.welcome_screen_choices[2]}", True, (255, 255, 255)),
                (687, 360))

            if self.welcome_screen_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (637, 255))
                if state.controller.isTPressed:
                    self.shuffle()


                    self.game_state = "bet_phase"
                    state.controller.isTPressed = False



            elif self.welcome_screen_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (637, 305))
                if state.controller.isTPressed and self.magic_lock == False:
                    pygame.time.wait(300)
                    self.game_state = "magic_menu"
                    self.isTPressed = False



            elif self.welcome_screen_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (637, 355))
                if state.controller.isTPressed:
                    print("Quit")
                    state.controller.isTPressed = False


            self.welcome_screen_text_box.draw(state)
            self.welcome_screen_text_box_hero.draw(state)
            # self.bordered_text_box.draw(state)

        elif self.game_state == "hero_is_desperate_state":
            self.hero_losing_money_text.draw(state)
            self.enemy_winning_money_text.draw(state)
            self.hero_losing_confused_money_text.draw(state)



        elif self.game_state == "enemy_is_desperate_state":
            self.enemy_losing_money_text.draw(state)
            self.hero_winning_money_text.draw(state)
            self.enemy_losing_confused_money_text.draw(state)





        elif self.game_state == "bet_phase":
            self.bet_screen_text.draw(state)

            # self.current_speaker = "cheater bob"

            # DISPLAY.blit(character_image, (23, 245))
            # DISPLAY.blit(self.font.render(f"{self.current_speaker}", True, (255, 255, 255)), (155, 350))


            DISPLAY.blit(self.font.render(f"Your Current bet:{self.bet}", True, (255, 255, 255)), (50, 530))
            DISPLAY.blit(self.font.render(f"v", True, (255, 255, 255)), (260, 550))
            DISPLAY.blit(self.font.render(f"^", True, (255, 255, 255)), (257, 510))


        elif self.game_state == "menu_screen":
            deck = Deck(ranks, suits)
            player_card_x = 235
            player_card_y = 195
            enemy_card_x = 235
            enemy_card_y = 15

            for i, card in enumerate(player_cards_list):
                if i > 3:
                    player_card_y = 305
                    player_card_x = 235
                deck.show_card(card[0], card[1], (player_card_x, player_card_y))
                player_card_x += 75

                # pygame.display.update()

            # pygame.display.update()

            for index, card in enumerate(enemy_cards_list):
                if index == 0:
                    deck.face_down_card((enemy_card_x, enemy_card_y))
                else:
                    deck.show_card(card[0], card[1], (enemy_card_x, enemy_card_y))
                enemy_card_x += 75



            # self.current_speaker = "hero"

            # DISPLAY.blit(self.font.render(f"{self.current_speaker}", True, (255, 255, 255)), (155, 350))



            # Create the black square box
            black_box = pygame.Surface((160 - 10, 180 - 10))
            black_box.fill((0, 0, 0))
            border_width = 5
            white_border = pygame.Surface((160 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
            white_border.fill((255, 255, 255))
            white_border.blit(black_box, (border_width, border_width))
            DISPLAY.blit(white_border, (620, 235))

            DISPLAY.blit(
                self.font.render(f"{self.choices[0]}", True, (255, 255, 255)),
                (687, 260))


            DISPLAY.blit(
                self.font.render(f"{self.choices[1]}", True, (255, 255, 255)),
                (687, 310))

            if self.avatar_of_luck == True and self.redraw_lock == False:
                DISPLAY.blit(self.font.render("Redraw", True, (255, 255, 255)), (687, 360))

            elif self.avatar_of_luck == False or self.redraw_lock == True:
                DISPLAY.blit(self.font.render("Locked", True, (255, 255, 255)), (687, 360))
            else:
                DISPLAY.blit(self.font.render("Locked", True, (255, 255, 255)), (687, 360))

            if self.current_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (637, 255))
                if state.controller.isTPressed:
                    pygame.time.wait(300)

                    print("code is broke right here")
                    if self.despair == False:
                        self.game_state = "enemy_draw_one_card"
                    elif self.despair == True:
                        self.game_state = "enemy_despair_draw_one_card"
                    state.controller.isTPressed = False
                    # self.betPhase = True
                    # self.game_state = "bet_phase"


            elif self.current_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (637, 305))
                if state.controller.isTPressed:
                    pygame.time.wait(300)
                    print("Time to draw a card")
                    self.game_state = "player_draw_one_card"
                    self.isTPressed = False



            elif self.current_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (637, 355))

                if state.controller.isTPressed and self.avatar_of_luck == True and self.redraw_lock == False:
                    pygame.display.update()
                    self.game_state = "menu_screen"



        # elif self.game_state == "refresh":
        #     print("going back to menu screen")
        #     self.game_state = "menu_screen"






            # DISPLAY.blit(self.font.render(f"Player bet:{self.bet}", True, (255, 255, 255)), (40, 390))
            #
            #
            # DISPLAY.blit(self.font.render(f"Player Hand{self.hand_to_str(self.player_hand)}", True, (255, 255, 255)), (40, 420))
            #
            # DISPLAY.blit(self.font.render(f"Enemy Hand{self.hand_to_str(self.enemy_hand)}", True, (255, 255, 255)), (40, 480))





        elif self.game_state == "magic_menu" :

            black_box = pygame.Surface((255, 215))
            black_box.fill((0, 0, 0))
            # Create the white border
            border_width = 5
            white_border = pygame.Surface((170 + 2 * border_width, 215 + 2 * border_width))
            white_border.fill((255, 255, 255))
            black_box = pygame.Surface((170, 215))
            black_box.fill((0, 0, 0))
            white_border.blit(black_box, (border_width, border_width))
            DISPLAY.blit(white_border, (620 - 20, 190))
            if self.magic_menu_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (640, 200))
                # DISPLAY.blit(
                #     self.font.render("Bluff status. When enemy ", True, (255, 255, 255)),
                #     (40, 445))
                self.bluff_magic_explain_component.draw(state)







            elif self.magic_menu_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (640, 250))
                self.reveal_magic_explain_component.draw(state)





            elif self.magic_menu_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (640, 300))
                self.avatar_magic_explain_component.draw(state)


            elif self.magic_menu_index == 3:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (630, 350))
                self.back_magic_explain_component.draw(state)


            if self.cheater_bob_money <= 900:

                DISPLAY.blit(
                    self.font.render(f"{self.magic_menu_selector[0]}", True, (255, 255, 255)),
                    (680, 205))
            else:
                DISPLAY.blit(
                    self.font.render("Locked", True, (255, 255, 255)),
                    (680, 205))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[1]}", True, (255, 255, 255)),
                (680, 255))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[2]}", True, (255, 255, 255)),
                (680, 305))

            DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[3]}", True, (255, 255, 255)),
                (680, 355))

        elif self.game_state == "final_strike_screen":
            self.final_strike_text_component.draw(state)
            self.enemy_bluffed_text_component.draw(state)
            self.hero_bluffing_text_component.draw(state)
            self.enemy_falling_for_bluff_text_component.draw(state)





            deck = Deck(ranks, suits)
            player_card_x = 300
            player_card_y = 250
            enemy_card_x = 300
            enemy_card_y = 25


            for card in player_cards_list:
                deck.show_card(card[0], card[1], (player_card_x, player_card_y))
                player_card_x += 100
                # pygame.display.update()

            # pygame.display.update()

            for index, card in enumerate(enemy_cards_list):
                deck.show_card(card[0], card[1], (enemy_card_x, enemy_card_y))
                enemy_card_x += 100

            self.enemy_crying_text_component.draw(state)
            self.hero_reveal_text_component.draw(state)
            pygame.display.update()


        elif self.game_state == "results_screen":
            deck = Deck(ranks, suits)
            player_card_x = 235
            player_card_y = 195
            enemy_card_x = 235
            enemy_card_y = 15

            for i, card in enumerate(player_cards_list):
                if i > 3:
                    player_card_y = 305
                    player_card_x = 235
                deck.show_card(card[0], card[1], (player_card_x, player_card_y))
                player_card_x += 75

                # pygame.display.update()

            # pygame.display.update()

            for index, card in enumerate(enemy_cards_list):

                deck.show_card(card[0], card[1], (enemy_card_x, enemy_card_y))
                enemy_card_x += 75

            # self.current_speaker = "cheater bob"

            # DISPLAY.blit(character_image, (23, 245))
            DISPLAY.blit(self.font.render(f"{self.current_speaker}", True, (255, 255, 255)), (155, 350))
            # DISPLAY.blit(self.font.render(f"{self.first_message_display}", True, (255, 255, 255)), (45, 390))

            DISPLAY.blit(self.font.render(f"{self.second_message_display}", True, (255, 255, 255)), (45, 450))
            DISPLAY.blit(self.font.render(f"{self.first_message_display}", True, (255, 255, 255)), (45, 500))
            # DISPLAY.blit(self.font.render(f"{self.third_message_display}", True, (255, 255, 255)), (45, 510))



            # DISPLAY.blit(self.font.render(f"Player bet:{self.bet}", True, (255, 255, 255)), (10, 155))




        pygame.display.flip()



class GameState:
    def __init__(self):
        self.controller: Controller = Controller()
        self.player: Player = Player(222, 111)
        self.npcs = [  CoinFlipFred(175,138), SalleyOpossum(65,28),  ChiliWilley(311, 28)]
        self.obstacle: Obstacle = Obstacle(22, 622)
        self.isRunning: bool = True
        self.isPaused: bool = False
        self.delta: float = 0.0
        self.mainScreen = MainScreen()
        self.coinFlipSandyScreen = CoinFlipSandyScreen()
        self.opossumInACanScreen = OpossumInACanScreen()
        self.OpossumInACanNellyScreen = OpossumInACanNellyScreen()
        self.BlackJackScreen = BlackJackScreen(ranks, suits)
        self.diceGameScreen = DiceGameScreen()
        # self.textBox = TextBox("", any, any)
        self.currentScreen = self.BlackJackScreen  # assign a value to currentScreen here

class Game:
    def __init__(self):
        self.state = GameState()  # create a new GameState()

    def start(self):
        self.state.currentScreen.start(self.state)
        while self.state.isRunning:

            self.state.delta = clock.tick(60)

            # will need to move this to Screen class
            # TODO maintain framerate pygame.
            self.state.currentScreen.update(self.state)
            self.state.currentScreen.draw(self.state)
            # self.textBox.update(self.state)
            # self.textBox.display()


        pygame.quit()


game = Game()
game.start()