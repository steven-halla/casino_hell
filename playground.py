import random
from typing import *

class Dice:
    def __init__(self, sides: int):
        self.sides = sides


    def roll(self) -> int:
        return random.randint(1, self.sides)




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

    def results(self):
        print("hi")
        print(type(six_sided_dice.roll()))
        print(self.player1pile)
        print(self.ante)
        if rolls[0] == 1 and rolls[1] == 1:
            print("snake eyes")




game = DiceGame(6)
game.results()


