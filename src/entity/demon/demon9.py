import math
from typing import Tuple

import pygame

from constants import GREEN
from entity.demon.demon import Demon
from entity.gui.textbox.npc_text_box import NpcTextBox


class Demon8(Demon):
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
        self.move_distance = 1.8  # Movement speed
        # self.facing_left = True  # Start facing left
        # self.facing_right = False
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

    def update(self, state):
        # Call the LOS method to check for player detection
        self.LOSLeft(state)

        # Store the last position before moving
        self.last_position.x = self.position.x
        self.last_position.y = self.position.y

        # Movement based on facing direction
        if self.facing_left:
            self.velocity.x = -self.move_distance
        elif self.facing_right:
            self.velocity.x = self.move_distance
        else:
            self.velocity.x = 0  # Not moving horizontally

        # Move the demon by its velocity
        self.setPosition(self.position.x + self.velocity.x, self.position.y)

        # Handle interactions and speaking
        distance = math.hypot(
            state.player.collision.x - self.collision.x,
            state.player.collision.y - self.collision.y
        )
        # if state.player.collision.x - self.collision.x < 0 and distance < 30:
        #     self.isSpeaking = True
        #     print("Demon bumped, starting conversation...")
        #     self.move_player_down = True  # This is the flag to indicate the player needs to move down.
        #
        # if self.player_spotted:
        #     print("Player spot detected")
        #     self.isSpeaking = True
        #     state.player.canMove = False
        #     if self.textbox.is_finished() and state.controller.isTPressed:
        #         self.move_player_down = True  # This is the flag to indicate the player needs to move down.
        #         state.controller.isTPressed = False
        #         self.isSpeaking = False
        #         self.player_spotted = False
        #         state.player.setPosition(660, 2800)  # Set the player's position to fixed coordinates
        #         state.player.canMove = True

        # Update the textbox visibility based on the demon's speaking state
        # if self.isSpeaking:
        #     self.textbox.update(state)

    def draw(self, state):
        # Draw the aura around the demon
        self.drawAura(state)

        # Draw the demon itself
        if self.facing_left:
            sprite_rect = pygame.Rect(1, 40, 22, 31)
        elif self.facing_right:
            sprite_rect = pygame.Rect(111, 40, 22, 31)
        else:
            # Default sprite rectangle if neither facing_left nor facing_right is set
            sprite_rect = pygame.Rect(1, 40, 22, 31)  # Adjust these values if needed

        # Get the subsurface for the area you want
        sprite = self.character_sprite_image.subsurface(sprite_rect)

        # Scale the subsurface to make it bigger
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))  # Adjust the size as needed

        # Define the position where you want to draw the sprite
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the scaled sprite portion on the display
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # Draw LOS if enabled (optional)
        if self.show_los:
            # LOS drawing code (if needed)
            pass

        # Draw the textbox if the demon is speaking
        if self.isSpeaking:
            self.textbox.draw(state)

    def setPosition(self, x, y):
        # Store the last position before updating
        self.last_position.x = self.position.x
        self.last_position.y = self.position.y

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
        # Calculate the distance between the demon and the player
        dx = self.collision.x - state.player.collision.x
        dy = self.collision.y - state.player.collision.y
        distance = math.hypot(dx, dy)

        # Check if the player is within line-of-sight and not hiding
        if distance <= self.los_radius and not state.area2RibDemonMazeScreen.player_hiding:
            print("found you")
            self.player_spotted = True
        else:
            self.player_spotted = False

    def drawAura(self, state):
        # Transparent grey color (adjust the alpha value for more or less transparency)
        grey_with_alpha = (128, 128, 128, 128)

        # Create a surface for the aura with the same dimensions as the LOS radius
        aura_surface = pygame.Surface((self.los_radius * 2, self.los_radius * 2), pygame.SRCALPHA)

        # Draw a transparent circle on the surface
        pygame.draw.circle(aura_surface, grey_with_alpha, (self.los_radius, self.los_radius), self.los_radius)

        # Calculate the position of the aura based on the demon's position and camera offset
        aura_x = self.collision.x + state.camera.x - self.los_radius
        aura_y = self.collision.y + state.camera.y - self.los_radius

        # Blit the aura surface onto the main display
        state.DISPLAY.blit(aura_surface, (aura_x, aura_y))
