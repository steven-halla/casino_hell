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


# class ComponentScreen():
#     def __init__(self):
#         super().__init__()
#         self.choices: list = ["Choice 1", "Choice 2", "Choice 3"]
#
#     def update(self):




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
        self.choices = ["choice 1", "choice 2", "choice 3"]
        self.current_index = 0



        self.pd1Total = 0
        self.pd2Total = 0
        self.pd3Total = 0


        self.ed1Total = 0
        self.ed2Total = 0
        self.ed3Total = 0


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

        elif self.game_state == "roll_screen":
            self.roll_two_d_six()

            print("count")
            self.pd1Total = self.rolls
            print(self.pd1Total)
            self.roll_state_display = True
            pygame.time.delay(3000)

            self.game_state = "results"


        elif self.game_state == "results":


            if self.isUpPressed:
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) - 1
                else:
                    self.current_index -= 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                self.isUpPressed = False

            elif self.isPPressed:
                for i, choice in enumerate(self.choices):
                    if self.current_index == i:
                        print(f"You pressed E and got {choice}")
                self.isPPressed = False

    def draw(self):
        DISPLAY.fill((0,0,0))

        if self.game_state == "welcome_screen":
            DISPLAY.blit(self.font.render(f"welcome to game name: press 1", True, (255, 255, 255)), (10, 10))

        elif self.game_state == "roll_screen":
            DISPLAY.blit(self.font.render(f"Time to roll the bones:", True, (255, 255, 255)), (10, 10))

        elif self.game_state == "results":
            DISPLAY.blit(
                self.font.render(f"Your roll is a {self.pd1Total}: Press E to cointinue", True, (255, 255, 255)),
                (10, 10))

        elif self.game_state == "choice_screen":
            pass



game = DiceGameTwo(SCREEN_WIDTH, SCREEN_HEIGHT, 6)
game.start()