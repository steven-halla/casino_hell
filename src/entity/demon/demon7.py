import math
from typing import Tuple

import pygame

from constants import GREEN
from entity.demon.demon import Demon
from entity.entity import Entity
from entity.gui.textbox.npc_text_box import NpcTextBox


class Demon7(Demon):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.color: Tuple[int, int, int] = GREEN
        self.speakStartTime: int = 0
        self.isSpeaking: bool = False
        self.textbox = NpcTextBox(
            [
                "Demon777: Your not a hedge human git out of here.!,"
                ],
            (50, 450, 50, 45), 30, 500)
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.move_player_down = False

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"


        #the below is for testing never delete this
        self.show_los = False  # LOS visibility flag

    def update(self, state):

        # use enums for facing
        self.LOSLeft(state)  # Specific to this subclass
        self.LOSRight(state)  # Specific to this subclass


        # print("updating")
        super().update(state)


        distance = math.sqrt(
            (state.player.collision.x - self.collision.x) ** 2 + (
                        state.player.collision.y - self.collision.y) ** 2)
        # print("distance: " + str(distance))
        if state.player.collision.x - self.collision.x < 0 and distance < 30:
            self.isSpeaking = True
            print("Demon bumped, starting conversation...")
            self.move_player_down = True  # S


        if self.player_spotted == True:
            print("Player spot detected")

            self.isSpeaking = True
            state.player.canMove = False
            if self.textbox.is_finished() and state.controller.isTPressed:

                # self.isSpeaking = False
                self.move_player_down = True  # This is the flag to indicate the player needs to move down.
                state.controller.isTPressed = False
                self.isSpeaking = False
                self.player_spotted = False
                state.player.setPosition(660, 2800)  # Set the player's position to fixed coordinates
                state.player.canMove = True

            # Update the textbox visibility based on the demon's speaking state
        self.textbox.update(state)

    def draw(self, state):
        # Existing drawing code for the demon and the textbox
        if self.isSpeaking:
            self.textbox.draw(state)

        # Draw the demon itself
        rect = (self.collision.x + state.camera.x, self.collision.y + state.camera.y,
                self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)

        # Draw LOS if enabled
        if self.show_los:
            # Horizontal Line (already working)
            start_pos_h = (self.collision.x + state.camera.x, self.collision.y + state.camera.y + self.collision.height // 2)
            end_pos_h = (start_pos_h[0] - self.los_horizontal_range, start_pos_h[1])  # Extend to the left

            # Vertical Line
            start_pos_v = (start_pos_h[0] - self.los_horizontal_range // 2, start_pos_h[1] - self.los_vertical_range // 2)  # Midpoint of horizontal line
            end_pos_v = (start_pos_v[0], start_pos_v[1] + self.los_vertical_range)  # Extend vertically

            # Draw the LOS lines in white
            pygame.draw.line(state.DISPLAY, (255, 255, 255), start_pos_h, end_pos_h, 1)  # Horizontal
            pygame.draw.line(state.DISPLAY, (255, 255, 255), start_pos_v, end_pos_v, 1)  # Vertical

    # def draw(self, state):
    #     if self.isSpeaking:
    #         self.textbox.draw(state)
    #     rect = (
    #     self.collision.x + state.camera.x, self.collision.y + state.camera.y,
    #     self.collision.width, self.collision.height)
    #     pygame.draw.rect(state.DISPLAY, self.color, rect)
    #     distance = math.sqrt(
    #         (state.player.collision.x - self.collision.x) ** 2 + (
    #                     state.player.collision.y - self.collision.y) ** 2)
