import random
from typing import *

import pygame


class BunnyTimes:
    def __init__(self, screen_width: int = 640, screen_height: int = 480):
        # Initialize Pygame
        pygame.init()

        # Set the screen size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Set the title and icon
        pygame.display.set_caption("Russian Roulette")
        # icon = pygame.image.load("roulette_icon.png")
        # pygame.display.set_icon(icon)

        # Load the font
        self.font = pygame.font.Font(None, 36)

        # Set the colors
        self.WHITE: Tuple[int, int, int] = (255, 255, 255)

        # Set the game variables
        self.winner_or_looser: List[str] = ["lose", "win", "win"]  # List to store the loaded bullets


    def start(self):
        print("hi")
        """Creates a new list in a random order"""
        # Create a copy of the original list
        shuffled_list = self.winner_or_looser.copy()

        # Shuffle the list in place
        random.shuffle(shuffled_list)

        print(str(shuffled_list))

bunbun = BunnyTimes()
bunbun.start()