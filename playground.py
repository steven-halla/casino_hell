import random
from typing import *

class Dice:
    def __init__(self, sides: int):
        self.sides = sides

    def roll(self) -> int:
        return random.randint(1, self.sides)

# Example usage
dice = Dice(6)
rolls = [dice.roll() for num in range(1)]
print(rolls)


