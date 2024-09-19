import math
from typing import Tuple

import pygame

from constants import GREEN
from entity.demon.demon import Demon
from entity.gui.textbox.npc_text_box import NpcTextBox


class Demon9(Demon):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.color: Tuple[int, int, int] = GREEN
        self.isSpeaking: bool = False
        self.textbox = NpcTextBox(
            [
                "Demon: You're not a hedge pog, git on out of here human!"
            ],
            (50, 450, 50, 45), 30, 500
        )
        self.move_distance = 3.8  # Movement speed
        self.velocity = pygame.math.Vector2(0, 0)

        # For storing the last position (needed for undoLastMove)
        self.last_position = pygame.math.Vector2(self.position.x, self.position.y)

        # Additional attributes
        self.move_player_down = False
        self.player_spotted = False
        self.los_radius = 210  # Line-of-sight radius

        # For testing; do not delete
        self.show_los = False  # LOS visibility flag
        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/Game Boy Advance - Breath of Fire - Doof.png"
        ).convert_alpha()

        # Initialize facing direction
        self.facing_left = False
        self.facing_right = True

    def update(self, state):
        # Store the last position before moving (to allow undoing movement)
        self.last_position.x = self.position.x
        self.last_position.y = self.position.y

        # Calculate the direction vector towards the player
        direction_x = state.player.collision.x - self.collision.x
        direction_y = state.player.collision.y - self.collision.y
        distance = math.hypot(direction_x, direction_y)

        if distance != 0:
            normalized_x = direction_x / distance
            normalized_y = direction_y / distance
        else:
            normalized_x = 0
            normalized_y = 0

        # Update the demon's velocity to move towards the player
        self.velocity.x = normalized_x * self.move_distance
        self.velocity.y = normalized_y * self.move_distance

        # Update the demon's position based on the velocity
        self.setPosition(self.position.x + self.velocity.x, self.position.y + self.velocity.y)

        # Update facing direction for sprite rendering
        if self.velocity.x < 0:
            self.facing_left = True
            self.facing_right = False
        else:
            self.facing_left = False
            self.facing_right = True

    def draw(self, state):
        # Draw the demon itself
        if self.facing_left:
            sprite_rect = pygame.Rect(1, 40, 22, 31)
        elif self.facing_right:
            sprite_rect = pygame.Rect(111, 40, 22, 31)
        else:
            sprite_rect = pygame.Rect(1, 40, 22, 31)

        sprite = self.character_sprite_image.subsurface(sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))

        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # Draw LOS if enabled (optional)
        if self.show_los:
            # Optional: Draw LOS radius for debugging
            pygame.draw.circle(
                state.DISPLAY,
                (255, 0, 0),
                (int(self.collision.x + state.camera.x), int(self.collision.y + state.camera.y)),
                self.los_radius,
                1
            )

        # Draw the textbox if the demon is speaking
        if self.isSpeaking:
            self.textbox.draw(state)

    def setPosition(self, x, y):
        # Update the position and collision rectangle
        self.position.x = x
        self.position.y = y
        self.collision.x = x
        self.collision.y = y

    def undoLastMove(self):
        # Revert the demon's position to the last stored position
        self.setPosition(self.last_position.x, self.last_position.y)

    def isOverlap(self, other_rect):
        # Check if the demon's collision rectangle overlaps with another rectangle
        return self.collision.isOverlap(other_rect)

    def LOSLeft(self, state):
        dx = state.player.collision.x - self.collision.x
        dy = state.player.collision.y - self.collision.y
        distance = math.hypot(dx, dy)

        # Assuming that you want the player to be spotted if they're within a certain distance
        if distance <= self.los_radius:
            self.player_spotted = True
        else:
            self.player_spotted = False

