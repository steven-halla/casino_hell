import random
import time
from typing import *

import pygame
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
WINDOWS_SIZE: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)

DISPLAY: pygame.Surface = pygame.display.set_mode(WINDOWS_SIZE)

class NewController:
    def __init__(self):
        self.is1Pressed: bool = False
        self.isTPressed: bool = False

        pygame.init()


    def keyPress(self, state: "GameState"):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    self.is1Pressed = True
                if event.key == pygame.K_t:
                    self.isTPressed = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_1:
                        self.is1Pressed = False
                    elif event.key == pygame.K_t:
                        self.isTPressed = False


class BunnyTimes(NewController):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        # Initialize Pygame
        super().__init__()
        pygame.init()
        self.opposum_font = pygame.font.Font(None, 36)
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Russian Roulette")
        self.font = pygame.font.Font(None, 36)
        self.game_state = "welcome_opposum"
        self.winner_or_looser: List[str] = ["lose", "win", "win"]
        self.result = "win"
        self.bet = 10


    def start(self):
        running = True
        while running:
            self.update()
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()

    def shuffle_opposums(self) -> List[str]:
        """Creates a new list in a random order"""

        random.shuffle(self.winner_or_looser)

        print(str(self.winner_or_looser))
        return self.winner_or_looser

    def check_results(self):
        print("checking result")
        if self.result == "win":
            self.bet = self.bet * 2
            print("you win")
            print(self.bet)

        elif self.result == "lose":
            self.bet = 0
            print(self.bet)
            print("you lose")



    def update(self):
        self.keyPress(self.game_state)
        if self.game_state == "welcome_opposum":
            if self.isTPressed:
                self.game_state = "choose_can"

        elif self.game_state == "choose_can":
            if self.is1Pressed:
                self.shuffle_opposums()
                self.result = self.winner_or_looser[0]
                del self.winner_or_looser[0]
                self.check_results()
                self.game_state = "play_again_or_bail"









    def draw(self):
        DISPLAY.fill((0,0,0))

        if self.game_state == "welcome_opposum":
            DISPLAY.blit(self.font.render(f"press T", True, (255, 255, 255)), (10, 10))
        elif self.game_state == "choose_can":
            DISPLAY.blit(self.font.render(f"Press 1", True, (255, 255, 255)), (10, 10))
        elif self.game_state == "play_again_or_bail":
            DISPLAY.blit(self.font.render(f"Press C to continue, or E to exit", True, (255, 255, 255)), (10, 10))










game = BunnyTimes(SCREEN_WIDTH, SCREEN_HEIGHT)
game.start()