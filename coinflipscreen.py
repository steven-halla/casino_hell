import random
import sys
from typing import *
import time

import pygame

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
WINDOWS_SIZE: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
DISPLAY: pygame.Surface = pygame.display.set_mode(WINDOWS_SIZE)


def nowMilliseconds() -> int:
    return round(time.time() * 1000)


class NewController:
    def __init__(self):
        self.is1Pressed: bool = False
        self.isTPressed: bool = False
        self.isPPressed: bool = False
        self.isOPressed: bool = False
        self.keyPressedTimes: Dict[int, int] = {}  # Map<key number, key pressed millisecond
        self.keyReleasedTimes: Dict[int, int] = {}  # Map<key number, key pressed millisecond

        pygame.init()

    def timeSinceKeyPressed(self, key: int):
        if key not in self.keyPressedTimes:
            return -1
        return nowMilliseconds() - self.keyPressedTimes[key]

    def timeSinceKeyReleased(self, key: int):
        if key not in self.keyReleasedTimes:
            return -1
        return nowMilliseconds() - self.keyReleasedTimes[key]


    def keyPress(self, state: "GameState"):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                self.keyPressedTimes[event.key] = nowMilliseconds()
                print(self.keyPressedTimes)
                if event.key == pygame.K_1:
                    self.is1Pressed = True
                elif event.key == pygame.K_t:
                    self.isTPressed = True
                elif event.key == pygame.K_p:
                    self.isPPressed = True
                elif event.key == pygame.K_o:
                    self.isOPressed = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    self.is1Pressed = False
                elif event.key == pygame.K_t:
                    self.isTPressed = False
                elif event.key == pygame.K_p:
                    self.isPPressed = False
                elif event.key == pygame.K_o:
                    self.isOPressed = False

class Dice:
    def __init__(self, sides: int):
        self.sides = sides
        self.rolls = []
    #rename roll method to roll 2d6 method
    def roll_two_d_six(self) -> List[int]:
        self.sides = 6
        roll1 = random.randint(1, self.sides)
        roll2 = random.randint(1, self.sides)
        self.rolls = [roll1, roll2]
        print(self.rolls)
        return self.rolls

    def roll_one_d_hundred(self) -> List[int]:
        self.sides = 100
        roll1 = random.randint(1, self.sides)

        self.rolls = [roll1]
        print("rolling 2d10")
        print("your dice results" + str(self.rolls))
        return self.rolls


    def add(self):
        # print(str(self.rolls))
        return self.rolls[0] + self.rolls[1]


class DiceGame(Dice, NewController):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, sides):
        super().__init__(sides)
        NewController.__init__(self)
        self.game_state = "player_1_declare_intent_stage"
        self.font = pygame.font.Font(None, 36)
        self.player_1_turn = False
        self.player_2_turn = False
        self.player1pile = 1000
        self.player2pile = 1000
        self.ante =1000
        self.anteXero = 0
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.player_1_bad_roll = False
        self.player_2_bad_roll = False

    def start(self):
        running = True
        while running:
            self.update()
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()

    def hot_bet(self):
        print("player  1 pile   is:" + str(self.player1pile))
        print("player  2 pile   is:" + str(self.player2pile))
        print("your ante is:" + str(self.ante) + "dollars")
        self.roll_two_d_six()
        if self.rolls[0] == self.rolls[1]:
            print("Matching double you lose everything")
            if self.game_state == "player_1_going_hot":
                self.player_1_bad_roll = True
                self.player1pile = 0
                print("player 1 pile is " + str(self.player1pile))
                print("player 2 pile is " + str(self.player2pile))

                self.player2pile += self.ante
                self.ante = 0
                print("Player 2 pile is")
                print(self.player2pile)
                print("ante is now")
                print(self.ante)
                time.sleep(3)
                sys.exit()


            elif self.game_state == "player_2_going_hot":
                self.player2pile = 0
                print(self.player1pile)
                self.player1pile += self.ante
                self.ante = 0
                time.sleep(3)
                sys.exit()

        elif self.add() == 2 or self.add() == 4 or self.add() == 6 or self.add() == 8 or self.add() == 10 or self.add() == 12:
            if self.game_state == "player_1_going_hot":
                self.roll_one_d_hundred()
                subtracted_amount = min(self.rolls[0], self.player2pile)
                self.player2pile -= subtracted_amount * 2
                self.player1pile += subtracted_amount * 2
                print("player2 pile is")
                print(self.player2pile)
                print("player1 pile is")
                print(self.player1pile)

                if self.player2pile < 0:
                    self.player2pile = 0
                    print("if its 0:")
                    print(self.player2pile)
                self.game_state = "player_2_declare_intent_stage"
            elif self.game_state == "player_2_going_hot":
                self.roll_one_d_hundred()
                subtracted_amount = min(self.rolls[0], self.player2pile)
                self.player2pile -= subtracted_amount * 2
                self.player1pile += subtracted_amount * 2
                print("player2 pile is")
                print(self.player2pile)
                print("player1 pile is")
                print(self.player1pile)

                if self.player1pile < 0:
                    self.player1pile = 0
                    print("if its 0:")
                    print(self.player1pile)
                self.game_state = "player_1_declare_intent_stage"

        elif self.game_state == "player_1_going_hot":
            print("no dice you wasted your chance")
            self.game_state = "player_2_declare_intent_stage"
        elif self.game_state == "player_2_going_hot":
            print("no dice you wasted your chance")
            self.game_state = "player_1_declare_intent_stage"

    def cold_bet(self):
        print("player  1 pile   is:" + str(self.player1pile))
        print("player  2 pile   is:" + str(self.player2pile))
        print("your ante is:" + str(self.ante) + "dollars")
        self.roll_two_d_six()
        if self.rolls[0] == 1 and self.rolls[1] == 1:
            if self.game_state == "player_1_declare_intent_stage":
                self.player_1_bad_roll = True
                self.player1pile = 0
                print(self.player1pile)
                print("snake eyes with a poop worm going through the eyes")

            elif self.game_state == "player_2_declare_intent_stage":
                self.player_2_bad_roll = True
                self.player2pile = 0
                print(self.player2pile)
                print("snake eyes with a poop worm going through the eyes")
        elif self.rolls[0] == 2 and self.rolls[1] == 2:
            if self.game_state == "player_1_declare_intent_stage":
                self.player_1_bad_roll = True
                self.player1pile = 0
                print(self.player1pile)
                print("4 eyes you die")

            elif self.game_state == "player_2_declare_intent_stage":
                self.player_2_bad_roll = True
                self.player2pile = 0
                print(self.player2pile)
                print("4 eyes you die")
        #
        elif self.rolls[0] == 3 and self.rolls[1] == 3:
            if self.game_state == "player_1_declare_intent_stage":
                self.player_1_bad_roll = True
                self.player1pile = 0
                print(self.player1pile)
                print("double threes are bad")

            elif self.game_state == "player_2_declare_intent_stage":
                self.player_2_bad_roll = True
                self.player2pile = 0
                print(self.player2pile)
                print("double threes are bad")

        elif self.rolls[0] == 6 and self.rolls[1] == 6:
            if self.game_state == "player_1_declare_intent_stage":
                print("you win =======================================================================")
                self.player1pile += self.ante

            elif self.game_state == "player_2_declare_intent_stage":
                print("you win ==================================================================")
                self.player2pile += self.ante
        #
        elif self.add() == 8:
            print("it adds to 8")
            if self.game_state == "player_1_declare_intent_stage":

                print("attacking player 2 pile")
                print(self.player1pile)
                print(self.player2pile)
                self.roll_one_d_hundred()
                self.player2pile -= self.rolls[0]
                if self.player2pile < 0:
                    self.player2pile = 0


            elif self.game_state == "player_2_declare_intent_stage":
                print("attacking player 2 pile")
                print(self.player1pile)
                print(self.player2pile)
                self.roll_one_d_hundred()
                self.player1pile -= self.rolls[0]
                if self.player1pile < 0:
                    self.player1pile = 0

        #
        elif self.add() == 7 or self.add() == 9 or self.add() == 11:
            print("you got a 7, 9, or 11")
            if self.game_state == "player_1_declare_intent_stage":

                print("attacking player 2 pile")
                print(self.player1pile)
                print(self.player2pile)
                self.roll_one_d_hundred()
                subtracted_amount = min(self.rolls[0], self.ante)
                self.ante -= subtracted_amount
                self.player1pile += subtracted_amount
                if self.ante < 0:
                    self.ante = 0





            elif self.game_state == "player_2_declare_intent_stage":
                print("attacking player 2 pile")
                print(self.player1pile)
                print(self.player2pile)
                self.roll_one_d_hundred()
                subtracted_amount = min(self.rolls[0], self.ante)
                self.ante -= subtracted_amount
                self.player2pile += subtracted_amount

                if self.ante < 0:
                    self.ante = 0



        #
        else:
            print("no luck this round")


    def update(self):
        self.keyPress(self.game_state)
        if self.game_state == "player_1_declare_intent_stage":
            if self.isTPressed:
                self.cold_bet()
                print("play 1 bet +++++++++++++++++++++++")
                self.game_state = "player_2_declare_intent_stage"
            elif self.isPPressed:
                print("going in hot")
                self.game_state = "player_1_going_hot"

                self.hot_bet()

        elif self.game_state == "player_2_declare_intent_stage":
            if self.isOPressed:
                self.game_state = "player_1_declare_intent_stage"
                self.cold_bet()
                print("player 2 bet ----------")
            elif self.is1Pressed:
                print("going in hot")
                self.game_state = "player_2_going_hot"

                self.hot_bet()





    def draw(self):
        DISPLAY.fill((0,0,0))

        if self.game_state == "player_1_declare_intent_stage":
            DISPLAY.blit(self.font.render(f"Player 1: press T forr cold P For hot", True, (255, 255, 255)), (10, 10))

        elif self.game_state == "player_2_declare_intent_stage":
            DISPLAY.blit(self.font.render(f"Player 2: press O forr cold 1 for hot", True, (255, 255, 255)), (10, 10))

        elif self.game_state == "player_1_going_hot":
            DISPLAY.blit(self.font.render(f"Player 1 is going hot PRESS P", True, (255, 255, 255)), (10, 10))

        elif self.game_state == "player_2_going_hot":
            DISPLAY.blit(self.font.render(f"Player 2 is going hot PRESS 1", True, (255, 255, 255)), (10, 10))


game = DiceGame(SCREEN_WIDTH, SCREEN_HEIGHT, 6)
game.start()