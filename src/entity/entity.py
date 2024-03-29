import pygame

from constants import RED
from physics.rectangle import Rectangle
from physics.vector import Vector


class Entity:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.position: Vector = Vector(x, y)
        self.velocity: Vector = Vector(0, 0)
        self.collision: Rectangle = Rectangle(x, y, width, height)

    def update(self, state: "GameState"):
        self.setPosition(self.position.x + self.velocity.x,
                         self.position.y + self.velocity.y)

    def draw(self, state: "GameState"):
        pygame.draw.rect(state.DISPLAY, RED, self.collision.toTuple())

    def undoLastMove(self):
        self.setPosition(self.position.x - self.velocity.x,
                         self.position.y - self.velocity.y)

    def moveDownBy100(self):
        self.setPosition(self.position.x, self.position.y + 100)


    def setPosition(self, x: float, y: float):
        self.position.x = x
        self.position.y = y
        self.collision.x = x
        self.collision.y = y

    def isOverlap(self, entity: "Entity") -> bool:
        # print("Overlap called")
        return self.collision.isOverlap(entity.collision)
