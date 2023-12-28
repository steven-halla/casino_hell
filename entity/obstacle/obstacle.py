import pygame

from core.constants import GREEN
from entity.entity import Entity


class Obstacle(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 32, 32)
        self.color: (int, int, int) = GREEN

    def update(self, state):
        super().update(state)

    def draw(self, state):
        pygame.draw.rect(state.DISPLAY, self.color, self.collision.toTuple())
