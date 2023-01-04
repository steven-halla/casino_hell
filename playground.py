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
        # roll1 = 6
        # roll2 = 5
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






class Craps(Dice, NewController):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, sides):
        super().__init__(sides)
        NewController.__init__(self)
        self.font = pygame.font.Font(None, 36)
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.message_display = ""
        self.game_state = "welcome_screen"
        self.exit_point_rolling_loop = False

        self.choices = ["Bet", "Quit", "Magic"]

        self.bet = 0
        self.bet_total = 0
        self.bet_counter = 0


        self.rollState = True
        self.betState = True
        self.round1 = True
        self.point_roll_phase = False

        self.comingOutRoll = True
        self.roll_phase = False


        self.phase_two_bet = False

        self.point_roll = 0



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



    def resultsComeOutRoll(self):
        if self.add() == 2 or self.add() == 3 or self.add() == 12:
            self.message_display = f"You rolled an {self.rolls}"

        elif self.add() == 7:
            print("You win the game congrats")

        else:
            self.point_roll = self.add()
            print("Your point roll is now an:" + str(self.point_roll))
            self.message_display = f"Your point roll is now an {self.point_roll} Match it to win!"


    def resultsPointRoll(self):
        if self.add() == self.point_roll:
            self.message_display = "you win"
            print("you win")

        elif self.add() == 7:
            self.message_display = "you lose"
            print("you lose")

        else:
            self.message_display = "roll again"
            print("roll agian")
            self.bet_counter += 1
            print(self.bet_counter)







    def place_bet(self):
        self.message_display = "Make your  bet Press UP or DOWN on Dpad to change bet"

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

        if self.isBPressed:
            self.bet_total += self.bet
            self.comingOutRoll = False
            self.roll_phase = True
            self.isBPressed = False
            if self.game_state == "point_roll_screen":
                if self.bet < 50:
                    self.bet = 50
                self.game_state = "point_rolling"





    def update(self):
        # delta between last update time in milliseconds
        # print("update() - state: " + str(self.game_state) + ", start at: " )

        self.handle_keyboard_input()
        if self.game_state == "welcome_screen":
           if self.is1Pressed:
               self.game_state = "craps_screen"

        elif self.game_state == "craps_screen":
            if self.comingOutRoll is True:
                self.place_bet()

            elif self.comingOutRoll is False and self.roll_phase == True:

                self.message_display = "time to roll the dice"

                self.roll_two_d_six()
                self.resultsComeOutRoll()
                self.roll_phase = False
                self.phase_two_bet = True
                self.roll_phase = False
                self.game_state = "point_roll_screen"

        elif self.game_state == "point_roll_screen":

            self.message_display = "Time to place your 2nd bet"
            self.place_bet()

        if self.game_state == "point_rolling" :
            if self.exit_point_rolling_loop == True:
                print("Hi")
            self.message_display = "press 1 to start rolling again"
            if self.is1Pressed:
                self.message_display = "time to roll the dice"
                self.roll_two_d_six()
                self.resultsPointRoll()
                self.message_display = f"your result is :{self.rolls}"
                self.is1Pressed = False











    def draw(self):
        DISPLAY.fill((0,0,0))

        if self.game_state == "welcome_screen":
            DISPLAY.blit(self.font.render(f"welcome to craps: press 1", True, (255, 255, 255)), (10, 10))

        elif self.game_state == "craps_screen":
            DISPLAY.blit(self.font.render(f"{self.message_display}", True, (255, 255, 255)), (33, 500))
            DISPLAY.blit(self.font.render(f"Player total bet:{self.bet_total}", True, (255, 255, 255)), (425, 222))
            DISPLAY.blit(self.font.render(f"Your betting: {self.bet} this round", True, (255, 255, 255)), (425, 255))
            DISPLAY.blit(self.font.render(f"Dice landed on: {self.rolls} ", True, (255, 255, 255)), (11, 255))


        elif self.game_state == "point_roll_screen" or "point_rolling":
            DISPLAY.blit(self.font.render(f"{self.message_display}", True, (255, 255, 255)), (33, 500))
            DISPLAY.blit(self.font.render(f"Player total bet:{self.bet_total}", True, (255, 255, 255)), (425, 222))
            DISPLAY.blit(self.font.render(f"Your betting: {self.bet} this round", True, (255, 255, 255)), (425, 255))
            DISPLAY.blit(self.font.render(f"Dice landed on: {self.rolls} ", True, (255, 255, 255)), (11, 255))
            DISPLAY.blit(self.font.render(f"Point Roll: {self.point_roll} ", True, (255, 255, 255)), (11, 205))

        elif self.game_state == "point_bet_phase":
            DISPLAY.blit(self.font.render(f"{self.message_display}", True, (255, 255, 255)), (33, 500))
            DISPLAY.blit(self.font.render(f"Player total bet:{self.bet_total}", True, (255, 255, 255)), (425, 222))
            DISPLAY.blit(self.font.render(f"Your betting: {self.bet} this round", True, (255, 255, 255)), (425, 255))
            DISPLAY.blit(self.font.render(f"Dice landed on: {self.rolls} ", True, (255, 255, 255)), (11, 255))
            DISPLAY.blit(self.font.render(f"Point Roll: {self.point_roll} ", True, (255, 255, 255)), (11, 205))


















game = Craps(SCREEN_WIDTH, SCREEN_HEIGHT, 6)
game.start()