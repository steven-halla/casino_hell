import random
import sys
from typing import *
import time
import pygame.freetype
from collections import defaultdict

import pygame

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
WINDOWS_SIZE: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
DISPLAY: pygame.Surface = pygame.display.set_mode(WINDOWS_SIZE)
FPS = 60
clock = pygame.time.Clock()
# pygame.time.get_ticks()



def nowMilliseconds() -> int:
    return round(time.time() * 1000)


class NewController:
    def __init__(self):
        self.is1Pressed: bool = False
        self.isUpPressed: bool = False
        self.isDownPressed: bool = False
        self.isTPressed: bool = False
        self.isPPressed: bool = False
        self.isOPressed: bool = False
        self.isEPressed: bool = False
        self.isMPressed: bool = False
        self.isBPressed: bool = False
        self.keyPressedTimes: Dict[int, int] = {}  # Map<key number, key pressed millisecond
        self.keyReleasedTimes: Dict[int, int] = {}  # Map<key number, key pressed millisecond
        self.t = defaultdict(lambda: 0)
        self.tPressed = 0


        pygame.init()


    def timeSinceKeyPressed(self, key: int):
        if key not in self.keyPressedTimes:
            return -1
        return pygame.time.get_ticks() - self.keyPressedTimes[key]

    def timeSinceKeyReleased(self, key: int):
        if key not in self.keyReleasedTimes:
            return -1
        return pygame.time.get_ticks() - self.keyReleasedTimes[key]



    def handle_keyboard_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.keyPressedTimes[event.key] = pygame.time.get_ticks()
                print(self.keyPressedTimes)
                if event.key == pygame.K_1:
                    self.is1Pressed = True
                elif event.key == pygame.K_t:

                    self.isTPressed = True
                elif event.key == pygame.K_p:
                    self.isPPressed = True
                elif event.key == pygame.K_o:
                    self.isOPressed = True
                elif event.key == pygame.K_e:
                    self.isEPressed = True
                elif event.key == pygame.K_b:
                    self.isBPressed = True
                elif event.key == pygame.K_UP:
                    self.isUpPressed = True
                elif event.key == pygame.K_DOWN:
                    self.isDownPressed = True

            elif event.type == pygame.KEYUP:
                self.keyReleasedTimes[event.key] = pygame.time.get_ticks()

                if event.key == pygame.K_1:
                    self.is1Pressed = False
                elif event.key == pygame.K_t:
                    self.isTPressed = False
                elif event.key == pygame.K_p:
                    self.isPPressed = False
                elif event.key == pygame.K_o:
                    self.isOPressed = False
                elif event.key == pygame.K_e:
                    self.isEPressed = False
                elif event.key == pygame.K_b:
                    self.isBPressed = False
                elif event.key == pygame.K_UP:
                    self.isUpPressed = False
                elif event.key == pygame.K_DOWN:
                    self.isDownPressed = False



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
        # roll1 = 5
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




class DiceGameTwo(Dice, NewController):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, sides):
        super().__init__(sides)
        NewController.__init__(self)
        self.font = pygame.font.Font(None, 36)
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.message_display = ""
        self.game_state = "welcome_screen"
        self.roll_state_display = False
        self.choices = ["Bet", "Quit", "Magic"]
        self.round1 = True
        self.round2 = False
        self.round3 = False
        self.reveal = False


        self.current_index = 0

        self.betPhase = False


        self.bet = 0
        self.playerTotalBet = 0
        self.aiBet = 0
        self.aiTotalBet = 0



        self.pd1Total = 0
        self.pd2Total = 0
        self.pd3Total = 0

        self.p1diceTotal = 0



        self.ed1Total = 0
        self.ed2Total = 0
        self.ed3Total = 0

        self.e1diceTotal = 0



    def start(self):
        running = True
        while running:
            clock.tick(FPS)


            self.update()

            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()



    def update(self):
        # delta between last update time in milliseconds
        # print("update() - state: " + str(self.game_state) + ", start at: " )

        self.handle_keyboard_input()
        if self.game_state == "welcome_screen":
            if self.is1Pressed:
                self.game_state = "roll_screen"
                self.is1Pressed = False

        elif self.game_state == "roll_screen":
            # we can have AI at this state have a bet state self.betLow self.betMed self.betHigh based on its rolls

            print("count")
            if self.round1 == True:
                self.roll_two_d_six()
                self.pd1Total = self.rolls
                self.p1diceTotal += self.add()
                print(self.pd1Total)
                self.roll_two_d_six()
                self.ed1Total = self.rolls
                self.e1diceTotal += self.add()

                self.roll_state_display = True
                pygame.time.delay(3000)
                self.game_state = "results"
                self.round1 = False
                self.round2 = True

            elif self.round2 == True:
                self.roll_two_d_six()
                self.pd2Total = self.rolls
                self.p1diceTotal += self.add()
                print(self.pd2Total)
                self.roll_two_d_six()
                self.ed2Total = self.rolls
                self.e1diceTotal += self.add()

                self.roll_state_display = True
                pygame.time.delay(3000)
                self.game_state = "results"
                self.round2 = False
                self.round3 = True

            elif self.round3 == True:
                print("round 3")
                self.roll_two_d_six()
                self.pd3Total = self.rolls
                self.p1diceTotal += self.add()
                print(self.pd2Total)
                self.roll_two_d_six()
                self.ed1Total = self.rolls
                self.e1diceTotal += self.add()

                self.roll_state_display = True
                pygame.time.delay(3000)
                self.game_state = "results"




        elif self.game_state == "results":
            if self.isEPressed and self.reveal == False:
                print("Hi")
                self.game_state = "choice_screen"
                self.isEPressed = False





        elif self.game_state == "choice_screen":
            if self.isUpPressed:
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) - 1
                else:
                    self.current_index -= 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                self.isUpPressed = False

            if self.isDownPressed:
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) + 1
                else:
                    self.current_index += 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                self.isDownPressed = False



            elif self.isPPressed:
                for i, choice in enumerate(self.choices):
                    if self.current_index == i:
                        print(f"You pressed E and got {choice}")
                self.isPPressed = False

        # I need to figure out bets its broke

        elif self.game_state == "bet_phase":
            if self.isUpPressed:

                self.bet += 10
                pygame.time.delay(100)
                self.isUpPressed = False

            elif self.isDownPressed:
                self.bet -= 10
                pygame.time.delay(100)
                self.isDownPressed = False

            if self.bet < 10:
                self.bet = 10

            if self.bet > 100:
                self.bet = 100

            if self.isBPressed and self.pd3Total == 0 :
                self.playerTotalBet += self.bet
                print("Player 1 bet total" + str(self.playerTotalBet))
                self.aiTotalBet += 50
                print("Player 2 bet total" + str(self.aiTotalBet))


                print("going back to welcome screen")
                self.game_state = "welcome_screen"



            elif self.isBPressed and self.pd3Total != 0:
                self.playerTotalBet += self.bet
                self.aiTotalBet += 50
                self.game_state = "reveal"
                print("Ok its time to show high or low")

        elif self.game_state == "reveal":
            if self.p1diceTotal > self.e1diceTotal:
                self.message_display = "Player 1 wins"

            elif self.p1diceTotal < self.e1diceTotal:
                self.message_display = "player 2 wins"

            elif self.p1diceTotal == self.e1diceTotal:
                self.message_display = "it's a draw too bad for the two of you"



    def draw(self):
        DISPLAY.fill((0,0,0))

        if self.game_state == "welcome_screen":
            DISPLAY.blit(self.font.render(f"welcome to game name: press 1", True, (255, 255, 255)), (10, 10))

        elif self.game_state == "roll_screen":
            DISPLAY.blit(self.font.render(f"Time to roll the bones:", True, (255, 255, 255)), (10, 10))

        elif self.game_state == "results":
            DISPLAY.blit(self.font.render(f"Your 1st roll made: {self.pd1Total}: Press E to continue", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.font.render(f"Your 2nd roll made: {self.pd2Total}: Press E to continue", True, (255, 255, 255)), (10, 60))
            DISPLAY.blit(self.font.render(f"Your 3rd roll made: {self.pd3Total}: Press E to continue", True, (255, 255, 255)), (10, 110))
            DISPLAY.blit(self.font.render(f"Player Current Bet {self.playerTotalBet}: Player 2 Bet: {self.aiTotalBet}", True, (255, 255, 255)), (10, 160))

        elif self.game_state == "choice_screen":
            DISPLAY.blit(
                self.font.render(f"Press the T key", True, (255, 255, 255)),
                (50, 10))
            DISPLAY.blit(
                self.font.render(f"{self.choices[0]}", True, (255, 255, 255)),
                (50, 60))

            DISPLAY.blit(
                self.font.render(f"{self.choices[1]}", True, (255, 255, 255)),
                (50, 110))

            DISPLAY.blit(
                self.font.render(f"{self.choices[2]}", True, (255, 255, 255)),
                (50, 160))
            DISPLAY.blit(self.font.render(f"P1 Roll 1: {self.pd1Total}Player 2 Roll 1: {self.ed1Total} ", True, (255, 255, 255)), (222,60))
            DISPLAY.blit(self.font.render(f"P1 Roll 1: {self.pd2Total} Player 2 Roll 1: {self.ed2Total}", True, (255, 255, 255)), (222,110))
            DISPLAY.blit(self.font.render(f"P1 Roll 1: {self.pd3Total} Player 2 Roll 1: {self.ed3Total}  ", True, (255, 255, 255)), (222,160))
            DISPLAY.blit(self.font.render(f"P1 Total {self.p1diceTotal}======== Enemy Total: {self.e1diceTotal}  ", True, (255, 255, 255)), (222,210))
            DISPLAY.blit(self.font.render(f"Player Current Bet {self.playerTotalBet}: Player 2 Bet: {self.aiTotalBet}", True, (255, 255, 255)), (222, 260))



            if self.current_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (10, 60))
                if self.isTPressed:
                    print("time to bet")
                    self.betPhase = True
                    self.game_state = "bet_phase"


            elif self.current_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (10, 110))
                if self.isTPressed:
                    print("This will exit our game")
                    self.isTPressed = False



            elif self.current_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (10, 160))
                if self.isTPressed:
                    print("In the future you can cast magic here")
                    self.isTPressed = False

        elif self.game_state == "bet_phase":
            DISPLAY.blit(self.font.render(f"Up and down to increase bet. Press B when ready {self.bet}", True,
                                          (255, 255, 255)), (10, 10))


        elif self.game_state == "reveal":
            DISPLAY.blit(self.font.render(f" Player 1 Roll 1: {self.pd1Total} Player 2 Roll 1: {self.ed1Total} ", True, (255, 255, 255)), (55,60))
            DISPLAY.blit(self.font.render(f"Player 1 Roll 2: {self.pd2Total} Player 2 Roll 2: {self.ed2Total} ", True, (255, 255, 255)), (55,110))
            DISPLAY.blit(self.font.render(f"Player 1 Roll 3: {self.pd3Total} Player 2 Roll 3: {self.ed3Total} ", True, (255, 255, 255)), (55,160))
            DISPLAY.blit(self.font.render(f"Player 1 dice total: {self.p1diceTotal} Player 2 dice: {self.e1diceTotal} ", True, (255, 255, 255)), (55,210))
            DISPLAY.blit(self.font.render(f"Player Current Bet {self.playerTotalBet}: Player 2 Bet: {self.aiTotalBet}", True, (255, 255, 255)), (10, 260))
            DISPLAY.blit(self.font.render(f"Player Current Bet {self.playerTotalBet}: Player 2 Bet: {self.aiTotalBet}", True, (255, 255, 255)), (10, 310))
            DISPLAY.blit(self.font.render(f"The result: {self.message_display}", True, (255, 255, 255)), (10, 360))








game = DiceGameTwo(SCREEN_WIDTH, SCREEN_HEIGHT, 6)
game.start()