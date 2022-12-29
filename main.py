import math
import sys
import time
import random
from typing import *

import pygame



clock = pygame.time.Clock()
FPS = 60

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
TILE_SIZE: int = 32

# nextScreen = false

font = pygame.font.Font('freesansbold.ttf', 24)
text_surface = font.render('Casino', True, GREEN, BLUE)
speech_bubble = font.render('We"re adding here', True, GREEN, BLUE)
textRect = text_surface.get_rect()
speechRect = speech_bubble.get_rect()


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







class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.color: Tuple[int, int, int] = RED
        self.walkSpeed = 3.5
        self.playerMoney = 1000





        # self.getMoney: bool = False

    # def speaking(self, player, npc):
    #     if npc.collision.x < player.collision.x:
    #         print("Nice")

    def update(self, state: "GameState"):
        controller = state.controller
        controller.update(state)


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
        self.messages = ["Did you hear I use a weighted coin? It's a lie. ", "Press the T key in order to start a battle with me."]
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

        elif state.controller.isTPressed and current_time - self.input_time >= self.input_delay and state.coinFlipScreen.coinFlipFredMoney > 0:
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
        self.messages = ["Are you sure you want to play opossum in a can?.","My opossums have Rabies that'll wear down your stamina","Press T to start the game"]
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

        elif state.controller.isTPressed and current_time - self.input_time >= self.input_delay and state.coinFlipScreen.coinFlipFredMoney > 0:
            state.currentScreen = state.opossumInACanScreen
            state.opossumInACanScreen.start(state)
        elif state.opossumInACanScreen.SallyOpossumMoney <= 0:
            print("coin flip freddy is defeated already move on you vulture")

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
        DISPLAY.fill(WHITE)
        DISPLAY.blit(font.render(
            f" player Money: {state.player.playerMoney}",
            True, (5, 5, 5)), (10, 10))
        state.player.draw(state)
        # state.npc.draw(state)
        for npc in state.npcs:
            npc.draw(state)
        state.obstacle.draw(state)
        pygame.display.update()

class OpossumInACanScreen(Screen):
    def __init__(self):
        super().__init__("Opossum in a can screen")
        self.SallyOpossumMoney = 1000
        self.opossum_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 36)
        self.game_state = "welcome_opposum"
        self.winner_or_looser: List[str] = ["win", "win", "win", "win", "win", "lucky_star", "X3_star", "lose",
                                            "insurance_eater", "insurance_eater"]
        self.result = "win"
        self.bet = 20
        self.insurance = 300
        self.X3 = False
        self.has_opossum_insurance = True

    def refresh(self):
        self.bet = 20
        self.has_opossum_insurance = True
        self.insurance = 300
        self.winner_or_looser = ["win", "win", "win", "win", "win", "lucky_star", "X3_star", "lose",
                                            "insurance_eater", "insurance_eater"]

    def shuffle_opposums(self) -> List[str]:
        """Creates a new list in a random order"""

        random.shuffle(self.winner_or_looser)

        print(str(self.winner_or_looser))
        return self.winner_or_looser

    def check_results(self):
        if self.result == "X3_star":
            self.X3 = True
            print(self.game_state)
            self.game_state = "play_again_or_bail"


        elif self.result == "win":
            if self.X3 == False:
                self.bet = self.bet * 2
                print("you win")
                print(self.bet)
                self.game_state = "play_again_or_bail"
            else:
                self.bet = self.bet * 3
                self.X3 = False
                self.game_state = "play_again_or_bail"

        elif self.result == "lucky_star":
            self.insurance = self.insurance * 2
            self.game_state = "play_again_or_bail"


        elif self.result == "insurance_eater":
            if self.insurance == 0:
                print("oh no your in trouble")
                print(self.game_state)
                self.game_state = "loser_screen"
            else:
                self.insurance = 0
                self.game_state = "play_again_or_bail"

        elif self.result == "lose":
            self.bet = 0
            print(self.bet)
            print("you lose")
            self.game_state = "loser_screen"

    def update(self, state: "GameState"):
        controller = state.controller
        controller.update(state)

        if self.game_state == "welcome_opposum":
            if controller.isTPressed:
                self.game_state = "choose_can"

        elif self.game_state == "choose_can":
            if controller.is1Pressed:
                self.shuffle_opposums()
                self.result = self.winner_or_looser[0]
                del self.winner_or_looser[0]
                self.check_results()

            #this code is not reachable perhaps
            player = state.player

            player.update(state)

        elif self.game_state == "play_again_or_bail":
            if controller.isPPressed:
                time.sleep(1)
                self.refresh()
                self.game_state = "welcome_opposum"
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)


            elif controller.isOPressed:
                print(str(controller.isTPressed))
                print("ok here we go")
                self.game_state = "choose_can"

        elif self.game_state == "loser_screen":
            time.sleep(3)
            self.refresh()
            self.game_state = "welcome_opposum"
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)

    def draw(self, state: "GameState"):
        DISPLAY.fill((0,0,0))

        if self.game_state == "welcome_opposum":
            DISPLAY.blit(self.font.render(f"press T", True, (255, 255, 255)), (10, 10))
        elif self.game_state == "choose_can":
            DISPLAY.blit(self.font.render(f"Press 1 to choose  a opossum", True, (255, 255, 255)), (10, 10))

        elif self.game_state == "play_again_or_bail":
            DISPLAY.blit(self.font.render(f"Press O to continue, or P to exit", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.font.render(f"your result is {self.result}", True, (255, 255, 255)), (110, 110))
            DISPLAY.blit(self.font.render(f"your toal money is {self.bet}", True, (255, 255, 255)), (210, 210))
            DISPLAY.blit(self.font.render(f"your opossum insurance is {self.insurance}", True, (255, 255, 255)), (410, 410))

        elif self.game_state == "loser_screen":
            DISPLAY.blit(self.font.render(f"yyou drew the {self.result} you lose goodbye", True, (255, 255, 255)), (210, 210))


        pygame.display.flip()







class CoinFlipScreen(Screen):
    def __init__(self):
        super().__init__("Casino Coin flip  Screen")
        self.lowBet = 50
        self.medBet = 150
        self.highBet = 800
        self.result = "tails"
        self.play_again = True
        self.players_side = "heads"
        self.new_font = pygame.font.Font(None, 36)

        self.welcome_text = self.new_font.render(
            f"Welcome to Coin Flip! Press R to continue.",
            True, (255, 255, 255))
        self.choose_bet_display = self.new_font.render(f"T for {self.lowBet}, W for {self.medBet}, E for {self.highBet}", True, (255, 255, 255))
        self.players_coin_side_choice = self.new_font.render(f"You choosed heads", True, (255, 255, 255))
        self.time_to_choose_heads_or_tails = self.new_font.render(f"K for tails, Q for heads", True, (255, 255, 255))
        self.flipping_now = self.new_font.render(f"flipping coin now", True, (255, 255, 255))
        self.game_state = "welcome"
        self.choice_sequence = True
        self.bet = 0
        self.font = pygame.font.Font(None, 36)
        self.coinFlipFredMoney = 1000



    def flipCoin(self):
        # Generate a random number between 0 and 1 to simulate the coin flip
        coin = random.random()
        if coin < 0.6:
            print("coin landed on heads")
            self.result = "heads"
        else:
            print("coin landed on tails")
            self.result = "tails"

    def update(self, state: "GameState"):
        # Update the controller
        controller = state.controller
        controller.update(state)

        if self.game_state == "welcome" :
            if controller.isRPressed:
                self.game_state = "choose_bet"
        elif self.game_state == "choose_bet":
            if controller.isTPressed:
                self.bet = self.lowBet
                if self.bet < self.coinFlipFredMoney:
                    self.bet = self.coinFlipFredMoney
                self.game_state = "choose_heads_or_tails_message"
            elif controller.isWPressed:
                self.bet = self.medBet
                if self.bet < self.coinFlipFredMoney:
                    self.bet = self.coinFlipFredMoney
                self.game_state = "choose_heads_or_tails_message"
            elif controller.isEPressed:
                self.bet = self.highBet
                print(self.bet)
                if self.bet > self.coinFlipFredMoney:
                    self.bet = self.coinFlipFredMoney
                self.game_state = "choose_heads_or_tails_message"


        elif self.game_state == "choose_heads_or_tails_message":
            if controller.isKPressed:
                self.players_side = "tails"
                print("you choosed tails")
                print(str(self.players_side))
                self.game_state = "coin_flip_time"
            elif controller.isQPressed:
                self.players_side = "heads"
                print("you choosed heads")
                print(str(self.players_side))
                self.game_state = "coin_flip_time"


        elif self.game_state == "coin_flip_time":
            time.sleep(2)
            self.flipCoin()
            if self.result == self.players_side:
                print("you won")
                state.player.playerMoney += self.bet
                self.coinFlipFredMoney -= self.bet
                self.game_state = "you_won_the_toss"

            else:
                state.player.playerMoney -= self.bet
                self.coinFlipFredMoney += self.bet
                if self.coinFlipFredMoney < 0:
                    self.coinFlipFredMoney = 0
                self.game_state = "you_lost_the_toss"

        elif self.game_state == "you_won_the_toss" or self.game_state == "you_lost_the_toss":
            time.sleep(3) # don't sleep, use a "state start time" and check current_time() - "state start time" > 3 seconds (3000ms)
            print("play_agin screen incoming ")
            self.game_state = "play_again_or_quit"

        elif self.game_state == "play_again_or_quit":
            if self.coinFlipFredMoney <= 0 or state.player.playerMoney <= 0:
                print("At 0 ending match")
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)

            print("in state: play_again_or_quit")
            if controller.isJPressed:
                print("play again")
                self.play_again = True
                self.game_state = "choose_bet"
            elif controller.isLPressed:
                print("bye")
                # self.play_again = False
                self.game_state = "welcome"
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)



    def draw(self, state: "GameState"):
        # Fill the screen with a solid color
        DISPLAY.fill((0, 0, 0))

        DISPLAY.blit(self.new_font.render(
            f" CoinFlipFredsMoney: {self.coinFlipFredMoney}",
            True, (255, 255, 255)), (10, 90))
        DISPLAY.blit(self.new_font.render(
            f" player Money: {state.player.playerMoney}",
            True, (255, 255, 255)), (10, 190))

        # Draw the welcome message or choose bet message based on the game state
        if self.game_state == "welcome":
            DISPLAY.blit(self.welcome_text, (10, 10))
        elif self.game_state == "choose_bet":
            DISPLAY.blit(self.choose_bet_display, (10, 10))
        elif self.game_state == "choose_heads_or_tails_message":
            DISPLAY.blit(self.time_to_choose_heads_or_tails, (10, 10))
        elif self.game_state == "coin_flip_time":
            DISPLAY.blit(self.flipping_now, (10, 10))

        elif self.game_state == "you_won_the_toss":
            DISPLAY.blit(self.new_font.render(f" choice  {self.players_side} coin landed  {self.result} won! YOUR BALANCE is {state.player.playerMoney}", True, (255, 255, 255)), (10, 10))
        elif self.game_state == "you_lost_the_toss":
            DISPLAY.blit(self.new_font.render(f" choice  {self.players_side} coin landed  {self.result} lost! YOUR BALANCE is {state.player.playerMoney}", True, (255, 255, 255)), (10, 10))
        elif self.game_state == "play_again_or_quit":
            DISPLAY.blit(self.new_font.render(f"Press J to play again or L to quit", True, (255, 255, 255)), (10, 10))


        # Draw the player and money
        # state.player.draw(state)
        # state.money.draw(state)

        # Update the display
        pygame.display.flip()




class TestScreen(Screen):
    def __init__(self):
        super().__init__("Casino Test Screen")

    def update(self, state: "GameState"):
        controller = state.controller
        player = state.player
        npc = state.npcs
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
        state.npcs.draw(state)
        state.obstacle.draw(state)
        state.money.draw(state)

        pygame.display.update()


class GameState:
    def __init__(self):

        self.controller: Controller = Controller()
        self.player: Player = Player(50, 100)

        self.npcs = [ CoinFlipExplanationGuy(270, 270), CoinFlipFred(450,200), OposumInACanExplainGirl(244,433), SalleyOpossum(444,488)]
        self.obstacle: Obstacle = Obstacle(22, 622)
        self.isRunning: bool = True
        self.isPaused: bool = False

        self.mainScreen = MainScreen()
        self.testScreen = TestScreen()
        self.coinFlipScreen = CoinFlipScreen()
        self.opossumInACanScreen = OpossumInACanScreen()
        self.currentScreen = self.mainScreen  # assign a value to currentScreen here



class Game:
    def __init__(self):
        self.state = GameState()  # create a new GameState()

    def start(self):
        self.state.currentScreen.start(self.state)

        while self.state.isRunning:
            if self.state.player.playerMoney <= 0:
                print("game over ")

            # will need to move this to Screen class

            self.state.currentScreen.update(self.state)
            self.state.currentScreen.draw(self.state)

        pygame.quit()


game = Game()
game.start()






