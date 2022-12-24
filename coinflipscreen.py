import random
import sys
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
        self.winner_or_looser: List[str] = ["win", "win", "win", "win", "win", "lucky_star",  "X3_star", "lose",  "insurance_eater", "insurance_eater"]
        self.result = "win"
        self.bet = 10
        self.insurance = 1000
        self.X3 = False
        self.has_opossum_insurance = True


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

        if self.result == "X3_star":
            self.X3 = True
            print(self.game_state)
            self.game_state = "play_again_or_bail"


        elif self.result == "win":
            if self.X3 == False:
                self.bet = self.bet * 2
                print("you win")
                print(self.bet)
                self.game_state = "play_again_or_bail"
            else:
                self.bet = self.bet * 3
                self.X3 = False
                self.game_state = "play_again_or_bail"

        elif self.result == "lucky_star":
            self.insurance = self.insurance * 2
            self.game_state = "play_again_or_bail"


        elif self.result == "insurance_eater":
            if self.insurance == 0:
                print("oh no your in trouble")
                print(self.game_state)
                self.game_state = "loser_screen"
            else:
                self.insurance = 0
                self.game_state = "play_again_or_bail"

        elif self.result == "lose":
            self.bet = 0
            print(self.bet)
            print("you lose")
            self.game_state = "loser_screen"


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

        elif self.game_state == "play_again_or_bail":
            if self.isPPressed:
                print("bye")
                sys.exit()

            elif self.isOPressed:
                print(str(self.isTPressed))
                print("ok here we go")
                self.game_state = "choose_can"

        elif self.game_state == "loser_screen":
            time.sleep(3)
            sys.exit()


    def draw(self):
        DISPLAY.fill((0,0,0))

        if self.game_state == "welcome_opposum":
            DISPLAY.blit(self.font.render(f"press T", True, (255, 255, 255)), (10, 10))
        elif self.game_state == "choose_can":
            DISPLAY.blit(self.font.render(f"Press 1 to choose  a opossum", True, (255, 255, 255)), (10, 10))

        elif self.game_state == "play_again_or_bail":
            DISPLAY.blit(self.font.render(f"Press O to continue, or P to exit", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.font.render(f"your result is {self.result}", True, (255, 255, 255)), (110, 110))
            DISPLAY.blit(self.font.render(f"your toal money is {self.bet}", True, (255, 255, 255)), (210, 210))
            DISPLAY.blit(self.font.render(f"your opossum insurance is {self.insurance}", True, (255, 255, 255)), (410, 410))

        elif self.game_state == "loser_screen":
            DISPLAY.blit(self.font.render(f"yyou drew the {self.result} you lose goodbye", True, (255, 255, 255)), (210, 210))











game = BunnyTimes(SCREEN_WIDTH, SCREEN_HEIGHT)
game.start()