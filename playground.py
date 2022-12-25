import random
from typing import *

class Dice:
    def __init__(self, sides: int):
        self.sides = sides


    def roll(self) -> int:
        return random.randint(1, self.sides)

    def add(self):
        return rolls[0] + rolls[1]




# Example usage

six_sided_dice = Dice(6)
rolls = [six_sided_dice.roll() for num in range(2)]
print(rolls)

class DiceGame(Dice):
    def __init__(self, sides: int):
        super().__init__(sides)
        self.player1pile = 10
        self.player2pile = 10
        self.ante = 1000
        self.hot_bet = False



    def results(self):
        print("hi")
        print(type(six_sided_dice.roll()))
        print("player 1 pile is:" + str(self.player1pile))
        print("your ante is:" + str(self.ante))
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

        elif self.hot_bet == True:
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





game = DiceGame(6)
game.results()


