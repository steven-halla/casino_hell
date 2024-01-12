

from typing import Tuple

import pygame

from constants import PURPLE
from entity.entity import Entity

class TreasureChest(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 16, 16)  # Assuming 16x16 is the size of the chest
        self.color: Tuple[int, int, int] = PURPLE

    def update(self, state: "GameState"):
        # Check for collision with the player
        if self.collision.isOverlap(state.player.collision):
            # Prevent the player from moving through the chest
            state.player.undoLastMove()

    def draw(self, state: "GameState"):
        rect = (
            self.collision.x + state.camera.x,
            self.collision.y + state.camera.y,
            self.collision.width,
            self.collision.height
        )
        pygame.draw.rect(state.DISPLAY, self.color, rect)


