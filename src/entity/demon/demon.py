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
        if current_time - self.last_move_time > self.move_interval:
            # ... [existing direction choosing code]

            # Predict next position
            next_x = self.position.x + self.velocity.x
            next_y = self.position.y + self.velocity.y

            # Create a temporary rectangle for the next position
            next_rect = Rectangle(next_x, next_y, self.collision.width, self.collision.height)

            # Check for collisions with obstacles, npcs, etc.
            collision = False
            if next_rect.isOverlap(state.obstacle):
                self.undoLastMove()

            for demon in state.demons:
                if next_rect.isOverlap(demon.collision):
                    collision = True
                    break

            if not collision:
                self.position.x = next_x
                self.position.y = next_y
                self.collision.x = next_x
                self.collision.y = next_y
            else:
                # Reset velocity to stop movement
                self.velocity.x = 0
                self.velocity.y = 0

    def draw(self, state):
        rect = (
            self.collision.x + state.camera.x, self.collision.y + state.camera.y,
            self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)

