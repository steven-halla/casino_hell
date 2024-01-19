import pygame
import random
import math
from typing import Tuple

from entity.entity import Entity
from constants import GREEN, PURPLE
from physics.rectangle import Rectangle

class Demon(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 16, 16)
        self.color: Tuple[int, int, int] = GREEN
        self.last_move_time = pygame.time.get_ticks()
        self.move_interval = 3000  # 3 seconds in milliseconds
        self.move_distance = 32  # distance to move each step
        self.last_color_change_time = pygame.time.get_ticks()
        self.color_change_interval = 3000

    def move_randomly(self, state):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.move_interval:
            self.last_move_time = current_time
            direction = random.choice(['up', 'down', 'left', 'right'])

            # Adjust position based on direction
            if direction == 'up':
                self.position.y -= self.move_distance
            elif direction == 'down':
                self.position.y += self.move_distance
            elif direction == 'left':
                self.position.x -= self.move_distance
            elif direction == 'right':
                self.position.x += self.move_distance

            # Update the collision rectangle's position
            self.collision.x = self.position.x
            self.collision.y = self.position.y

        super().update(state)  # Call update at the end

    def LOSLeft(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_color_change_time > self.color_change_interval:
            self.last_color_change_time = current_time
            if self.color == GREEN:
                self.color = PURPLE
            else:
                self.color = GREEN

    def update(self, state):
        super().update(state)
        # Reset velocity after moving

    def draw(self, state):
        rect = (
            self.collision.x + state.camera.x, self.collision.y + state.camera.y,
            self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)
