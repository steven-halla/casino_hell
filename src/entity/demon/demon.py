import pygame
import random
import math
from typing import Tuple

from entity.entity import Entity
from constants import GREEN
from physics.rectangle import Rectangle


class Demon(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 16, 16)
        self.color: Tuple[int, int, int] = GREEN
        self.last_move_time = pygame.time.get_ticks()
        self.move_interval = 3000  # 3 seconds in milliseconds
        self.move_distance = 5  # distance to move each step

    def update(self, state):
        super().update(state)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.move_interval:
            self.last_move_time = current_time
            direction = random.choice(['up', 'down', 'left', 'right'])

            if direction == 'up':
                self.velocity.y = -self.move_distance
            elif direction == 'down':
                self.velocity.y = self.move_distance
            elif direction == 'left':
                self.velocity.x = -self.move_distance
            elif direction == 'right':
                self.velocity.x = self.move_distance

        # Reset velocity after moving

    def draw(self, state):
        rect = (
            self.collision.x + state.camera.x, self.collision.y + state.camera.y,
            self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)

