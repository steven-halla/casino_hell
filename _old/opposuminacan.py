import sys
import pygame
import random


class OpposumInACan:
    def __init__(self, screen_width=640, screen_height=480):
        pygame.init()

        # Set the screen size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Russian Roulette")
        self.font = pygame.font.Font(None, 36)
        self.bullet_count = 3  # Number of bullets in the gun
        self.bullets = []  # List to store the loaded bullets
        self.loaded_chamber = -1  # Index of the loaded chamber (-1 means no chamber is loaded)
        self.game_over = False  # Flag to check if the game is over



