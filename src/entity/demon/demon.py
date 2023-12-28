import math
from typing import Tuple

import pygame

from constants import GREEN
from entity.entity import Entity


class Demon(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 16, 16)
        self.color: Tuple[int, int, int] = GREEN
        self.hp = 100

    def update(self, state):

        # use enums for facing

        # print("updating")
        super().update(state)
        distance = math.sqrt(
            (state.player.collision.x - self.collision.x) ** 2 + (
                        state.player.collision.y - self.collision.y) ** 2)
        # print("distance: " + str(distance))
        if state.player.collision.x - self.collision.x < 0 and distance < 30:
            print("yupp")
            distance = math.sqrt(
                (state.player.collision.x - self.collision.x) ** 2 + (
                            state.player.collision.y - self.collision.y) ** 2)
        else:
            distance = float('inf')

    def draw(self, state):
        rect = (
        self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)
        distance = math.sqrt(
            (state.player.collision.x - self.collision.x) ** 2 + (
                        state.player.collision.y - self.collision.y) ** 2)
