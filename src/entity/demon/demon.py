import pygame
import random
import math
from typing import Tuple

from entity.entity import Entity
from constants import GREEN, PURPLE, BLUE
from physics.rectangle import Rectangle

class Demon(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 16, 16)
        self.color: Tuple[int, int, int] = GREEN
        self.last_move_time = pygame.time.get_ticks()
        self.move_interval = 5555  # 3 seconds in milliseconds
        self.move_distance = 10  # distance to move each step
        self.last_color_change_time = pygame.time.get_ticks()
        self.color_change_interval = 3000
        self.LOScounter = 0
        self.los_blocked = False
        self.last_vertical_move_time = pygame.time.get_ticks()
        self.vertical_move_interval = 1111
        self.vertical_direction = 1  # 1 for down, -1 for up
        self.last_fast_move_time = pygame.time.get_ticks()  # Initialize with the current time
        self.fast_move_interval = 55  # Time interval between fast moves, in milliseconds
        self.fast_move_distance = 15
        self.player_spotted = False
        self.los_horizontal_range = 220
        self.los_vertical_range = 32


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

    def move_down_fast(self, state):
        # Set an initial timer value
        timer = 0
        current_time = pygame.time.get_ticks()

        # Check if the required time has passed to update the movement
        if current_time - self.last_fast_move_time > self.fast_move_interval:
            self.last_fast_move_time = current_time

            # Move the character down fast by a larger fixed amount
            self.position.y += self.fast_move_distance  # fast_move_distance is greater than move_distance

            # Update the collision rectangle's position
            self.collision.y = self.position.y

            # Optional: You can add logic to handle what happens when the entity moves down fast
            # For example, checking for collisions or changing state

    # You will need to initialize last_fast_move_time and fast_move_interval in your entity's __init__ method:
    # self.last_fast_move_time = pygame.time.get_ticks()  # Initialize with the current time
    # self.fast_move_interval = some_value  # Time interval between fast moves
    # self.fast_move_distance = larger_value_than_normal  # The distance to move down fast

    def move_up_and_down(self, state):

        # Set an initial timer value
        timer = 0
        current_time = pygame.time.get_ticks()
        if current_time - self.last_vertical_move_time > self.vertical_move_interval:
            self.last_vertical_move_time = current_time

            if self.color == GREEN:
                # Move the character down by a fixed amount
                self.position.y += self.move_distance
            elif self.color == PURPLE:
                # Move the character up by a fixed amount
                self.position.y -= self.move_distance

            # Update the collision rectangle's position
            self.collision.y = self.position.y

            # Check for collisions with other demons and turn only self.demon PURPLE if colliding
            for other_demon in state.demons:
                if other_demon != self and self.isOverlap(other_demon):
                    self.color = PURPLE
            if self.color == PURPLE:
                if current_time - self.last_color_change_time > 8500:  # 1000 milliseconds = 1 second
                    print("Green")
                    self.last_color_change_time = current_time
                    self.color = GREEN

            # You can break here if you want to change colors of only the first pair of colliding demons
                # break

    def LOSLeft(self, state):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_color_change_time > self.color_change_interval:
            self.last_color_change_time = current_time
            self.color = PURPLE if self.color == GREEN else GREEN

        # Define the LOS horizontal and vertical range
        # los_horizontal_range = 220
        # los_vertical_range = 32

        if self.color == PURPLE:  # Demon facing left
            los_left_boundary = self.collision.x - self.los_horizontal_range
            los_upper_boundary = self.collision.y - self.los_vertical_range
            los_lower_boundary = self.collision.y +  self.los_vertical_range

            # Flag to indicate if LOS is blocked by a shielding demon
            los_blocked = False
            for demon in state.demons:
                if demon != self:  # Ensure we're not checking the demon against itself
                    distance_to_left_demon = self.collision.x - (demon.collision.x + demon.collision.width)
                    y_distance = abs(self.collision.y - demon.collision.y)  # Calculate the absolute y-position difference

                    # print(f"Checking demon at ({demon.collision.x}, {demon.collision.y}) with horizontal distance: {distance_to_left_demon} and vertical distance: {y_distance}")

                    # Check if the demon is within 130 pixels to the left and the y-position difference is 30 pixels or less
                    if 0 < distance_to_left_demon <= 130 and y_distance <= 30:
                        self.color = BLUE  # Turn the current demon BLUE
                        print(f"Demon {self} turned BLUE because of nearby demon {demon} at ({demon.collision.x}, {demon.collision.y}) with y-distance: {y_distance}")
                        los_blocked = True  # Set the flag indicating LOS is blocked
                        break  # A demon is found within the range, no need to check further

            # Check if the player is in LOS and the LOS is not blocked
            if not los_blocked:
                if state.player.collision.x < self.collision.x and \
                        state.player.collision.x > los_left_boundary and \
                        state.player.collision.y > los_upper_boundary and \
                        state.player.collision.y < los_lower_boundary:
                    self.player_spotted = True
                    print("Player is in LOS!")
                    self.LOScounter += 1
                    print(self.LOScounter)
                    if state.player.collision.x < self.collision.x:
                        print("I see you to the left")
                    return False  # Player is in LOS and not shielded

        # LOS is blocked by a demon or LOS is not towards the player
        return True  # Safe, either LOS is blocked or player is not in LOS

    def update(self, state):
        super().update(state)
        # Reset velocity after moving

    def draw(self, state):
        rect = (
            self.collision.x + state.camera.x, self.collision.y + state.camera.y,
            self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.color == GREEN and hasattr(self, 'los_rect'):
            # Offset the LOS rect by the camera position for correct positioning on the screen
            los_rect_screen = self.los_rect.move(state.camera.x, state.camera.y)
            pygame.draw.rect(state.DISPLAY, (255, 255, 255), los_rect_screen, 1)
