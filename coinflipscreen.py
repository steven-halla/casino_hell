import random
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

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_1:
                        self.is1Pressed = False
                    elif event.key == pygame.K_1:
                        self.is1Pressed = False


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
        self.winner_or_looser: List[str] = ["lose", "win", "win"]  # List to store the loaded bullets

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


    def update(self):
        if self.game_state == "welcome_opposum":
            print("yo")
    def draw(self):
        DISPLAY.fill((0,0,0))

        if self.game_state == "welcome_opposum":
            DISPLAY.blit(self.font.render(f"Press J to play again or L to quit", True, (255, 255, 255)), (10, 10))










game = BunnyTimes(SCREEN_WIDTH, SCREEN_HEIGHT)
game.start()