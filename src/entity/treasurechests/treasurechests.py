

from typing import Tuple

import pygame

from constants import PURPLE
from entity.entity import Entity

class TreasureChest(Entity):
    def __init__(self, x: float, y: float, treasure_item: str):
        super().__init__(x, y, 16, 16)  # Assuming 16x16 is the size of the chest
        self.color: Tuple[int, int, int] = PURPLE
        self.treasure_item = treasure_item  # The item in the chest



    def update(self, state: "GameState"):
        # Check for collision with the player
        if self.collision.isOverlap(state.player.collision):
            # Prevent the player from moving through the chest
            state.player.undoLastMove()

        if not self.isOpened and state.controller.isTPressed:
            # Open the chest and give the item


            self.open_chest(state)

    def give_item(self, state: "GameState"):

        print(f"Received item: {self.item}")
        state.player.items.append(self.item)

        print("Your inventory so far: " + str(state.player.inventory))

    def draw(self, state: "GameState"):
        rect = (
            self.collision.x + state.camera.x,
            self.collision.y + state.camera.y,
            self.collision.width,
            self.collision.height
        )
        pygame.draw.rect(state.DISPLAY, self.color, rect)


