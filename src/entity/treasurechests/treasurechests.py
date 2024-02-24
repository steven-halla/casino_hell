

from typing import Tuple

import pygame

from constants import PURPLE
from entity.entity import Entity

class TreasureChest(Entity):
    def __init__(self, x: float, y: float, treasure_item: str):
        super().__init__(x, y, 16, 16)  # Assuming 16x16 is the size of the chest
        self.color: Tuple[int, int, int] = PURPLE
        self.treasure_item = treasure_item  # The item in the chest
        self.character_sprite_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/NES - Magician - Treasure Chest.png").convert_alpha()




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
        sprite_rect = pygame.Rect(1, 1, 26, 18)
        sprite = self.character_sprite_image.subsurface(sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (40, 40))
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))


