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
        self.isEPressed: bool = False
        self.isMPressed: bool = False
        self.isBPressed: bool = False
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


    def keyPress(self):
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
                elif event.key == pygame.K_e:
                    self.isEPressed = True
                elif event.key == pygame.K_b:
                    self.isBPressed = True

            elif event.type == pygame.KEYUP:
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
        self.rolls = [roll1, roll2]
        print(self.rolls)
        return self.rolls

    def roll_one_d_hundred(self) -> List[int]:
        self.sides = 100
        roll1 = random.randint(1, self.sides)
        self.one_hundred_rolls = [roll1]
        print("rolling 2d10")
        print("your dice results" + str(self.one_hundred_rolls))
        return self.one_hundred_rolls


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
        self.roll_state = ""
        self.player_1_lost_game = False
        self.player_2_lost_game = False


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

        if self.game_state == "player_1_going_hot":
            self.roll_two_d_six()
            if self.rolls[0] == self.rolls[1]:
                self.player1pile = 0

                self.player2pile += self.ante + self.player1pile
                self.player1pile = 0
                self.ante = 0
                print("you rolled a double get ready for trouble")
                self.game_state = "player_1_game_over"
                self.player_1_lost_game = True



            elif self.add() == 2 or self.add() == 4 or self.add() == 6 or self.add() == 8 or self.add() == 10 or self.add() == 12:
                self.roll_one_d_hundred()
                subtracted_amount = min(self.one_hundred_rolls[0], self.player2pile)
                self.player2pile -= subtracted_amount * 3
                self.player1pile += subtracted_amount * 3

                if self.player2pile < 0:
                    self.player2pile = 0
                    print("if its 0:")
                    print(self.player2pile)
                self.game_state = "player_2_declare_intent_stage"

            else:
                print("unhandled dice roll in player_1_going_hot")


        elif self.game_state == "player_2_going_hot":
            self.roll_two_d_six()
            if self.rolls[0] == self.rolls[1]:
                self.player2pile = 0

                self.player1pile += self.ante + self.player2pile
                self.ante = 0
                self.player2pile = 0
                self.player_2_lost_game = True


            elif self.add() == 2 or self.add() == 4 or self.add() == 6 or self.add() == 8 or self.add() == 10 or self.add() == 12:
                self.roll_one_d_hundred()
                subtracted_amount = min(self.one_hundred_rolls[0], self.player2pile)
                self.player2pile -= subtracted_amount * 3
                self.player1pile += subtracted_amount * 3

                if self.player1pile < 0:
                    self.player1pile = 0
                    print("if its 0:")
                    print(self.player1pile)
                self.game_state = "player_1_declare_intent_stage"

            else:
                print("unhandled dice roll in player_2_going_hot")

        # elif self.game_state == "player_1_wins":
        #     print("hi")
        # elif self.game_state == "player_2_wins":
        #     print("bye")

        #
        # elif self.add() == 2 or self.add() == 4 or self.add() == 6 or self.add() == 8 or self.add() == 10 or self.add() == 12:
        #     if self.game_state == "player_1_going_hot":
        #         self.roll_one_d_hundred()
        #         subtracted_amount = min(self.one_hundred_rolls[0], self.player2pile)
        #         self.player2pile -= subtracted_amount * 3
        #         self.player1pile += subtracted_amount * 3
        #
        #
        #         if self.player2pile < 0:
        #             self.player2pile = 0
        #             print("if its 0:")
        #             print(self.player2pile)
        #         self.game_state = "player_2_declare_intent_stage"
        #     elif self.game_state == "player_2_going_hot":
        #         self.roll_one_d_hundred()
        #         subtracted_amount = min(self.one_hundred_rolls[0], self.player2pile)
        #         self.player2pile -= subtracted_amount * 3
        #         self.player1pile += subtracted_amount * 3
        #
        #
        #         if self.player1pile < 0:
        #             self.player1pile = 0
        #             print("if its 0:")
        #             print(self.player1pile)
        #         self.game_state = "player_1_declare_intent_stage"

        elif self.game_state == "player_1_going_hot":
            print("no dice you wasted your chance")
            self.game_state = "player_2_declare_intent_stage"

        elif self.game_state == "player_2_going_hot":
            print("no dice you wasted your chance")

        print("end state: " + self.game_state)

    def cold_bet(self):
        print("player  1 pile   is:" + str(self.player1pile))
        print("player  2 pile   is:" + str(self.player2pile))
        print("your ante is:" + str(self.ante) + "dollars")
        self.roll_two_d_six()
        if self.rolls[0] == 1 and self.rolls[1] == 1 or self.rolls[0] == 2 and self.rolls[1] == 2 or \
                self.rolls[0] == 3 and self.rolls[1] == 3:
            if self.game_state == "player_1_rolls":
                print(self.game_state)
                self.player2pile = self.player2pile + self.player1pile + self.ante
                self.player1pile = 0
                self.ante = 0
                self.roll_state = "You got the wrong kind of double, you lose everything player 1!"
                print(self.player1pile)
                self.player_1_lost_game = True



            elif self.game_state == "player_2_rolls":
                print(self.game_state)

                self.player2pile = self.player2pile + self.player1pile + self.ante
                self.player1pile = 0
                self.ante = 0
                self.roll_state = "You got the wrong kind of double, you lose everything player 2!"
                print(self.player2pile)
                self.player_2_lost_game = True


        elif self.rolls[0] == 6 and self.rolls[1] == 6:
            if self.game_state == "player_1_rolls":
                print("you win =======================================================================")
                self.player1pile = self.player2pile + self.player1pile + self.ante
                self.player2pile = 0
                self.ante = 0
                self.roll_state = "lucky double sixes, player 1 wins!"

                self.game_state = "player_1_wins"

            elif self.game_state == "player_2_rolls":
                print("you win ==================================================================")
                self.player2pile = self.player2pile + self.player1pile + self.ante
                self.player1pile = 0
                self.ante = 0
                self.roll_state = "lucky double sixes, player 2 wins!"

                self.game_state = "player_2_wins"

        #
        elif self.add() == 8:
            print("it adds to 8")
            if self.game_state == "player_1_rolls":
                self.roll_state = "THe result is an 8, attack player pile"

                print("attacking player 2 pile")
                print(self.player1pile)
                print(self.player2pile)
                self.roll_one_d_hundred()
                self.player1pile += self.one_hundred_rolls[0]
                self.player2pile -= self.one_hundred_rolls[0]
                if self.player2pile < 0:
                    self.player2pile = 0
                self.game_state = "player_2_intent_stage"



            elif self.game_state == "player_2_rolls":
                self.roll_state = "THe result is an 8, attack player pile"

                print("attacking player 2 pile")
                print(self.player1pile)
                print(self.player2pile)
                self.roll_one_d_hundred()
                self.player2pile += self.one_hundred_rolls[0]

                self.player1pile -= self.one_hundred_rolls[0]
                if self.player1pile < 0:
                    self.player1pile = 0
                self.game_state = "player_1_intent_stage"

        #
        elif self.add() == 7 or self.add() == 9 or self.add() == 11:
            print("you got a 7, 9, or 11")
            if self.game_state == "player_1_rolls":
                self.roll_state = "High Even Number, Attack the ante "


                print(self.player1pile)
                print(self.player2pile)
                self.roll_one_d_hundred()
                subtracted_amount = min(self.one_hundred_rolls[0], self.ante)
                self.ante -= subtracted_amount
                self.player1pile += subtracted_amount


                if self.ante < 0:
                    self.ante = 0
                self.game_state = "player_2_intent_stage"



            elif self.game_state == "player_2_rolls":
                self.roll_state = "High Even Number, Attack the ante"

                print(self.player1pile)
                print(self.player2pile)
                self.roll_one_d_hundred()
                subtracted_amount = min(self.one_hundred_rolls[0], self.ante)
                self.ante -= subtracted_amount
                self.player2pile += subtracted_amount

                if self.ante < 0:
                    self.ante = 0
                self.game_state = "player_1_intent_stage"

        #
        else:
            self.roll_state = "Your roll means nothing!"

            print("no luck this round")


    def update(self):
        self.keyPress()
        print("update: " + str(self.game_state))
        if self.game_state == "player_1_declare_intent_stage":
            self.one_hundred_rolls = 0
            if self.isTPressed:
                print("hithere you ")
                self.game_state = "player_1_rolls"
                print(self.game_state)

            elif self.isPPressed:
                print("going in hot")
                self.game_state = "player_1_going_hot"



        elif self.game_state == "player_1_rolls":
            if self.isEPressed:
                print("pressing T")
                self.cold_bet()
                if self.one_hundred_rolls == 0:
                    self.game_state = "player_1_results"
                else:
                    self.game_state = "player_1_results_one_hundred"

        elif self.game_state == "player_1_going_hot":
            if self.is1Pressed:
                print("pressing 1")
                self.hot_bet()
                if self.one_hundred_rolls == 0:
                    self.game_state = "player_1_results"
                else:
                    self.game_state = "player_1_results_one_hundred"

        elif self.game_state == "player_1_results" or self.game_state == "player_1_results_one_hundred":
            if self.isBPressed:
                self.game_state = "player_2_declare_intent_stage"






        elif self.game_state == "player_2_declare_intent_stage":
            self.one_hundred_rolls = 0

            if self.isTPressed:
                print("hithere you ")
                self.game_state = "player_2_rolls"
                print(self.game_state)

            elif self.isPPressed:
                print("going in hot")
                self.game_state = "player_2_going_hot"




        elif self.game_state == "player_2_rolls":
            if self.isEPressed:
                print("pressing T")
                self.cold_bet()
                if self.one_hundred_rolls == 0:
                    self.game_state = "player_2_results"
                else:
                    self.game_state = "player_2_results_one_hundred"



        elif self.game_state == "player_2_going_hot":
            if self.is1Pressed:
                print("pressing 1")
                self.hot_bet()
                if self.one_hundred_rolls == 0:
                    self.game_state = "player_2_results"
                else:
                    self.game_state = "player_2_results_one_hundred"

        elif self.game_state == "player_2_results" or self.game_state == "player_2_results_one_hundred":
            if self.isBPressed:
                self.game_state = "player_1_declare_intent_stage"



        #
        # elif self.player_1_lost_game == True:
        #     self.game_state = "player_1_game_over"
        #     print("hi")
        #
        # elif self.player_2_lost_game == True:
        #     self.game_state = "player_2_game_over"
        #     print("hi")


    def draw(self):
        DISPLAY.fill((0,0,0))



        if self.game_state == "player_1_declare_intent_stage":
            DISPLAY.blit(self.font.render(f"Player 1: press T forr cold P For hot", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.font.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.font.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.font.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))

        elif self.game_state == "player_2_declare_intent_stage":
            DISPLAY.blit(self.font.render(f"Player 2: press T forr cold P for hot", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.font.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.font.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.font.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))



        elif self.game_state == "player_1_going_cold":
            DISPLAY.blit(self.font.render(f"Player 1 is going cold. ", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.font.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.font.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.font.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))

        elif self.game_state == "player_2_going_cold":
            DISPLAY.blit(self.font.render(f"Player 1 is going cold. ", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.font.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.font.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.font.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))

        elif self.game_state == "player_1_going_hot":
            DISPLAY.blit(self.font.render(f"Player 1 is going hot PRESS 1", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.font.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.font.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.font.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))

        elif self.game_state == "player_2_going_hot":
            DISPLAY.blit(self.font.render(f"Player 2 is going hot PRESS 1", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.font.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.font.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.font.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))

        elif self.game_state == "player_1_wins":
            DISPLAY.blit(self.font.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.font.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.font.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))
            DISPLAY.blit(self.font.render(f"Player 1 wins", True, (255, 255, 255)), (500, 500))

        elif self.game_state == "player_2_wins":
            DISPLAY.blit(self.font.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.font.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.font.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))
            DISPLAY.blit(self.font.render(f"Player 2 wins", True, (255, 255, 255)), (500, 500))

        elif self.game_state == "player_1_rolls":
            DISPLAY.blit(self.font.render(f"PLAYER 1 PRESS E to roll the dice", True, (255, 255, 255)), (255, 255))

        elif self.game_state == "player_2_rolls":
            DISPLAY.blit(self.font.render(f"PLAYER 2 PRESS E to roll the dice", True, (255, 255, 255)), (255, 255))


        elif self.game_state == "player_1_results":
            DISPLAY.blit(self.font.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.font.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.font.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))
            DISPLAY.blit(self.font.render(f" Player 1 rolls a {self.rolls} PRESS B when ready", True, (255, 255, 255)), (155, 255))
            DISPLAY.blit(self.font.render(f" {self.roll_state}", True, (255, 255, 255)), (5, 355))
            if self.player_1_lost_game == True:
                DISPLAY.blit(
                    self.font.render(f"Sorry player 1: GAME OVER!!!: {self.player1pile}", True, (255, 255, 255)),
                    (1, 555))


        elif self.game_state == "player_2_results":
            DISPLAY.blit(self.font.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.font.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.font.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))
            DISPLAY.blit(self.font.render(f" Player 2 rolls a {self.rolls} PRESS B when ready", True, (255, 255, 255)),
                         (155, 255))
            DISPLAY.blit(self.font.render(f" {self.roll_state}", True, (255, 255, 255)), (5, 355))
            if self.player_2_lost_game == True:
                DISPLAY.blit(
                    self.font.render(f"Sorry player 2: GAME OVER!!!: {self.player1pile}", True, (255, 255, 255)),
                    (1, 555))



        elif self.game_state == "player_1_results_one_hundred":
            DISPLAY.blit(self.font.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.font.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.font.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))
            DISPLAY.blit(self.font.render(f" Player 1 rolls a {self.rolls} PRESS B when ready", True, (255, 255, 255)),
                         (155, 255))
            DISPLAY.blit(self.font.render(f" {self.roll_state}", True, (255, 255, 255)), (5, 355))
            DISPLAY.blit(self.font.render(f"1d100 ROLLED: {self.one_hundred_rolls}", True, (255, 255, 255)),
                         (5, 555))



        elif self.game_state == "player_2_results_one_hundred":
            DISPLAY.blit(self.font.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (200, 200))
            DISPLAY.blit(self.font.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (300, 300))
            DISPLAY.blit(self.font.render(f"Ante: {self.ante}", True, (255, 255, 255)), (400, 400))
            DISPLAY.blit(self.font.render(f" Player 2 rolls a {self.rolls} PRESS B when ready", True, (255, 255, 255)),
                         (155, 255))
            DISPLAY.blit(self.font.render(f" {self.roll_state}", True, (255, 255, 255)), (5, 355))
            DISPLAY.blit(self.font.render(f"1d100 ROLLED: {self.one_hundred_rolls}", True, (255, 255, 255)),
                         (5, 555))








game = DiceGame(SCREEN_WIDTH, SCREEN_HEIGHT, 6)
game.start()