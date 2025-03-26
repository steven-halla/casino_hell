from typing import Tuple

import pygame
import os

FPS = 60
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
WINDOWS_SIZE: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
DISPLAY: pygame.Surface = pygame.display.set_mode(WINDOWS_SIZE)

# this used to be 16
TILE_SIZE: int = 32
GREEN: Tuple[int, int, int] = (0, 255, 0)
BLACK: Tuple[int, int, int] = (0, 0, 0)
BLUEBLACK: Tuple[int, int, int] = (0, 0, 51)
WHITE: Tuple[int, int, int] = (255, 255, 255)
BLUE: Tuple[int, int, int] = (0, 0, 255)
RED: Tuple[int, int, int] = (255, 0, 0)
PURPLE: Tuple[int, int, int] = (200, 0, 125)
#player position
PLAYER_OFFSET = (16 * 23, 16 * 16)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # path to current file
ASSETS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "..", "assets", "images")