import math
from typing import Tuple

import pygame

from constants import GREEN
from entity.demon.demon import Demon
from entity.entity import Entity
from entity.gui.textbox.npc_text_box import NpcTextBox


class Demon4(Demon):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.color: Tuple[int, int, int] = GREEN
        self.speakStartTime: int = 0
        self.isSpeaking: bool = False
        self.textbox = NpcTextBox(
            [
                "Demon: Hey human, what are you doing here, get out !,"
                ,
                ],
            (50, 450, 50, 45), 30, 500)
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.move_player_down = False
        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/PlayStation - Breath of Fire 3 - Gonger.png").convert_alpha()
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"


    def update(self, state):
        # self.move_down_fast(state)

        # use enums for facing

        # print("updating")
        super().update(state)
        distance = math.sqrt(
            (state.player.collision.x - self.collision.x) ** 2 + (
                        state.player.collision.y - self.collision.y) ** 2)
        # print("distance: " + str(distance))
        if state.player.collision.x - self.collision.x < 0 and distance < 40:
            # self.isSpeaking = True
            print("Demon bumped, starting conversation...")
            self.move_player_down = True  # S
            state.player.setPosition(660, 2800)  # Set the player's position to fixed coordinates
            self.move_player_down = True  # This is the flag to indicate the player needs to move down.




            # Update the textbox visibility based on the demon's speaking state
        # if self.isSpeaking:
        #     self.textbox.update(state)

    def draw(self, state):
        # if self.isSpeaking:
        #     self.textbox.draw(state)
        sprite_rect = pygame.Rect(7, 77, 40, 60)

        # Get the subsurface for the area you want
        sprite = self.character_sprite_image.subsurface(sprite_rect)

        # Scale the subsurface to make it two times bigger
        scaled_sprite = pygame.transform.scale(sprite, (60, 60))  # 44*2 = 88

        # Define the position where you want to draw the sprite
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the scaled sprite portion on the display
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))
