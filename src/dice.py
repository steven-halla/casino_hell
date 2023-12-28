import random
from typing import List


class Dice:
    def __init__(self, sides: int):
        self.sides = sides
        self.rolls = []
        self.one_hundred_rolls = [0]

    # rename roll method to roll 2d6 method
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
