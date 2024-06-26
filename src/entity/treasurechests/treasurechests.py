

from typing import Tuple

import pygame
import math

from constants import PURPLE
from entity.entity import Entity

# class TreasureChest(Entity):
#     def __init__(self, x: float, y: float, treasure_item: str):
#         super().__init__(x, y, 16, 16)  # Assuming 16x16 is the size of the chest
#         self.color: Tuple[int, int, int] = PURPLE
#         self.treasure_item = treasure_item  # The item in the chest
#         self.character_sprite_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/NES - Magician - Treasure Chest.png").convert_alpha()
#
#
#
#
#     def update(self, state: "GameState"):
#         # Check for collision with the player
#         if self.collision.isOverlap(state.player.collision):
#             # Prevent the player from moving through the chest
#             state.player.undoLastMove()
#
#         if not self.isOpened and state.controller.isTPressed:
#             # Open the chest and give the item
#
#
#             self.open_chest(state)
#
#     def give_item(self, state: "GameState"):
#
#         print(f"Received item: {self.item}")
#         state.player.items.append(self.item)
#
#         print("Your inventory so far: " + str(state.player.inventory))
#
#     def draw(self, state: "GameState"):
#         sprite_rect = pygame.Rect(1, 1, 26, 18)
#         sprite = self.character_sprite_image.subsurface(sprite_rect)
#         scaled_sprite = pygame.transform.scale(sprite, (40, 40))
#         sprite_x = self.collision.x + state.camera.x - 20
#         sprite_y = self.collision.y + state.camera.y - 10
#         state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))


from typing import Tuple
import pygame
from constants import PURPLE
from entity.entity import Entity

class TreasureChest(Entity):
    def __init__(self, x: float, y: float, treasure_item: str):
        super().__init__(x, y, 16, 16)  # Assuming 16x16 is the size of the chest
        self.color: Tuple[int, int, int] = PURPLE
        self.treasure_item: str = treasure_item  # The item in the chest
        self.character_sprite_image: pygame.Surface = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/NES - Magician - Treasure Chest.png").convert_alpha()
        self.isOpened: bool = False  # Initialize 'isOpened' attribute
        self.state_start_time: int = pygame.time.get_ticks()  # Initialize start_time to the current time
        self.treasure_open_sound: pygame.mixer.Sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/open_treasure.mp3")
        self.treasure_open_sound.set_volume(0.5)

    def update(self, state: "GameState"):
        # Check for collision with the player
        if self.collision.isOverlap(state.player.collision):
            # Prevent the player from moving through the chest
            state.player.undoLastMove()

        if not self.isOpened and state.controller.isTPressed:
            self.open_chest(state)

    def open_chest(self, state: "GameState"):
        # Implement the logic for opening the chest here
        if state.controller.isTPressed and (pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt(
                (state.player.collision.x - self.collision.x) ** 2 + (state.player.collision.y - self.collision.y) ** 2
            )
            if distance < 40:
                self.give_item(state)  # Call the give_item method to add the item to the player's inventory
                self.treasure_open_sound.play()  # Play the sound effect once
                self.isOpened = True

    def give_item(self, state: "GameState"):
        print(f"Received item: {self.treasure_item}")
        state.player.items.append(self.treasure_item)
        print("Your inventory so far: " + str(state.player.items))
        state.treasurechests.remove(self)  # Remove the chest from the game

    def draw(self, state: "GameState"):
        sprite_rect: pygame.Rect = pygame.Rect(1, 1, 26, 18)
        sprite: pygame.Surface = self.character_sprite_image.subsurface(sprite_rect)
        scaled_sprite: pygame.Surface = pygame.transform.scale(sprite, (40, 40))
        sprite_x: int = self.collision.x + state.camera.x - 20
        sprite_y: int = self.collision.y + state.camera.y - 10
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))



