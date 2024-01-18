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

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"


    def update(self, state):

        # use enums for facing

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


            if state.controller.isTPressed:
                self.isSpeaking = False
                self.move_player_down = True  # This is the flag to indicate the player needs to move down.
                state.controller.isTPressed = False
                state.player.setPosition(100, 500)  # Set the player's position to fixed coordinates



            # Update the textbox visibility based on the demon's speaking state
        if self.isSpeaking:
            self.textbox.update(state)

    def draw(self, state):
        if self.isSpeaking:
            self.textbox.draw(state)
        rect = (
        self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)
        distance = math.sqrt(
            (state.player.collision.x - self.collision.x) ** 2 + (
                        state.player.collision.y - self.collision.y) ** 2)
