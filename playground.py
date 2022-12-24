import random
from typing import *

class Dice:
    def __init__(self, sides: int):
        self.sides = sides

    def roll(self) -> int:
        return random.randint(1, self.sides)


# Example usage

six_sided_dice = Dice(6)
rolls = [six_sided_dice.roll() for num in range(1)]
print(rolls)


