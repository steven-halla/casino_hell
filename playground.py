import random
from typing import *

import pygame as pygame

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
WINDOWS_SIZE: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)

DISPLAY: pygame.Surface = pygame.display.set_mode(WINDOWS_SIZE)
import pygame


class NewController:
    def __init__(self):
        self.is1Pressed: bool = False
        self.isTPressed: bool = False
        self.isPPressed: bool = False
        self.isOPressed: bool = False

        pygame.init()


    def keyPress(self, state: "GameState"):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

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

    def roll(self) -> int:
        roll_result = random.randint(1, self.sides)
        self.rolls.append(roll_result)
        return roll_result

    def add(self):
        return self.rolls[0] + self.rolls[1]

# Example usage




class DiceGame(Dice, NewController):
    def __init__(self, sides: int):
        super().__init__(sides)
        NewController.__init__(self)
        self.game_state = "player_1_declare_intent_stage"
        self.font = pygame.font.Font(None, 36)
        self.player_1_turn = False
        self.player_2_turn = False
        self.player1pile = 10
        self.player2pile = 10
        self.ante = 1000

    def start(self):
        running = True
        while running:
            self.update()
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()



    def cold_bet(self):
        print("player 1 pile is:" + str(self.player1pile))
        print("your ante is:" + str(self.ante))
        self.roll()
        if rolls[0] == 1 and rolls[1] == 1:
            print("snake eyes")
        elif rolls[0] == 2 and rolls[1] == 2:
            print("Double twos")
        elif rolls[0] == 3 and rolls[1] == 3:
            print("double threes")
        elif self.add() == 8:
            print("it adds to 8")
        elif self.add() == 7 or self.add() == 9 or self.add() == 11:
            print("you got a 7, 8, or 9")
        else:
            print("no luck this round")

    def hot_bet(self):
        if rolls[0] == 1 and rolls[1] == 1:
            print("snake eyes")
        elif rolls[0] == 2 and rolls[1] == 2:
            print("Double twos")
        elif rolls[0] == 3 and rolls[1] == 3:
            print("double threes")

        elif rolls[0] == 4 and rolls[1] == 4:
            print("Double twos")
        elif rolls[0] == 5 and rolls[1] == 5:
            print("double fives")
        elif rolls[0] == 6 and rolls[1] == 6:
            print("double sixes")

        elif self.add() == 3 or self.add() == 5 or self.add() == 7 or self.add() == 9 or self.add() == 11:
            print("roll a 1d100 and win double the amount")



    def update(self):
        self.keyPress(self.game_state)
        if self.game_state == "player_1_declare_intent_stage":
            if self.isTPressed:
                self.cold_bet()
            elif self.isPPressed:
                self.hot_bet()
        elif self.game_state == "player_2_declare_intent_stage":
            if self.isTPressed:
                self.cold_bet()
            elif self.isPPressed:
                self.hot_bet()


    def draw(self):
        DISPLAY.fill((0,0,0))

        if self.game_state == "player_1_declare_intent_stage":
            DISPLAY.blit(self.font.render(f"Player 1: press T forr cold, press P for hot", True, (255, 255, 255)), (10, 10))

        elif self.game_state == "player_2_declare_intent_stage":
            DISPLAY.blit(self.font.render(f"Player 2: press T forr cold, press P for hot", True, (255, 255, 255)), (10, 10))




game = DiceGame(6)
game.start()


