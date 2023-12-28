import math
import time
from typing import Tuple

import pygame

from core.constants import BLUE
from entity.entity import Entity


class Npc(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 16, 16)
        self.color: Tuple[int, int, int] = BLUE
        self.speakStartTime: int = 0
        self.isSpeaking: bool = False

    def update(self, state):
        super().update(state)

        player = state.player
        # print(time.process_time() - self.speakStartTime)
        if state.controller.isTPressed and (
                time.process_time() - self.speakStartTime) > .20:
            print("hi there partner")

            distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                            player.collision.y - self.collision.y) ** 2)
            # Check if distance is within the sum of the widths and heights of the rectangles
            if 48 >= distance <= player.collision.width + player.collision.height + self.collision.width + self.collision.height:
                self.isSpeaking = not self.isSpeaking
                self.speakStartTime = time.process_time()
                print("yo")

    def draw(self, state):
        rect = (
        self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.isSpeaking:
            pygame.display.get_surface().blit(state.TEXT_SURFACE, (
                self.position.x + self.collision.width / 2,
                self.position.y - self.collision.height))
