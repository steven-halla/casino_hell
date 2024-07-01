import pygame
from entity.gui.textbox.text_box import TextBox
from screen.examples.screen import Screen
import time
import random
import math
from typing import Dict, Tuple, Optional, Any


class HungryStarvingHippos(Screen):
    def __init__(self, screenName: str = "Casino Slots Screen") -> None:
        super().__init__(screenName)
        self.game_state: str = "welcome_screen"
        self.font = pygame.font.Font(None, 36)  # Initialize the font with size 36

        self.battle_messages: Dict[str, TextBox] = {
            "welcome_message": TextBox(
                [" "],
                (65, 460, 700, 130),
                36,
                500
            ),
        }

        # Ball attributes
        self.human_size: int = 20
        self.humans: Dict[str, Dict[str, Any]] = {}  # Dictionary to store ball positions and speeds
        self.hippo: Optional[Dict[str, Any]] = None  # Dictionary to store hippo position and speed
        self.hippo_stopping_eating: float = 0  # Time when the hippo starts eating

        # Initialize box attributes
        self.box_top_left: Tuple[int, int] = (0, 0)
        self.box_bottom_right: Tuple[int, int] = (0, 0)

        # Initialize ball positions (this should be done only once)
        self.initialize_human_position()

        self.last_time: float = time.time()
        self.start_time: float = time.time()  # Timer to track elapsed time
        self.winners = []

    def initialize_human_position(self) -> None:
        # Set the initial position of the balls
        width, height = 600, 300
        y_axis_position_adjuster = 80
        top_left_x = (800 - width) // 2
        top_left_y = (600 - height) // 2 - y_axis_position_adjuster
        top_left = (top_left_x, top_left_y)
        self.box_top_left = top_left
        self.box_bottom_right = (top_left[0] + width, top_left[1] + height)

        labels = ["A1", "B1", "C1", "D1", "E1", "A2", "B2", "C2", "D2", "E2"]
        for i, label in enumerate(labels):
            initial_x = self.box_bottom_right[0] - self.human_size - 20
            initial_y = self.box_top_left[1] + height // 2 - self.human_size // 2 - (i * 20) + 60  # Move down by 60 pixels
            move_speed = random.randint(5, 10)  # Assign a unique speed for each ball
            self.humans[label] = {"pos": [initial_x, initial_y], "speed": move_speed}

    def initialize_hippo_position(self) -> None:
        width, height = 600, 200
        initial_x = self.box_bottom_right[0] - self.human_size - 20
        initial_y = self.box_top_left[1] + height // 2 - self.human_size // 2 + 60
        move_speed = 15
        self.hippo = {"pos": [initial_x, initial_y], "speed": move_speed}

    def find_closest_human(self) -> Tuple[Optional[str], Optional[int], Optional[int]]:
        if not self.hippo or not self.humans:
            return None, None, None

        closest_human = None
        closest_distance = float('inf')
        hippo_x, hippo_y = self.hippo["pos"]

        for label, data in self.humans.items():
            human_x, human_y = data["pos"]
            distance = math.sqrt((human_x - hippo_x) ** 2 + (human_y - hippo_y) ** 2)

            if distance < closest_distance:
                closest_distance = distance
                closest_human = (label, human_x, human_y)

        return closest_human

    def update(self, state: "GameState") -> None:
        pygame.mixer.music.stop()
        if state.controller.isQPressed:
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return

        controller = state.controller
        controller.update()

        # Calculate delta_time
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time

        # Check if 10 seconds have passed to spawn the hippo
        if self.hippo is None and current_time - self.start_time >= 10:
            self.initialize_hippo_position()

        # Move the balls
        self.move_human(delta_time)

        # Move the hippo if it exists
        if self.hippo:
            self.move_hippo(delta_time)
            self.check_collisions()

    def draw(self, state: "GameState") -> None:
        state.DISPLAY.fill((0, 0, 51))
        self.draw_box_boundary(state)
        self.draw_human(state)
        self.draw_bottom_black_box(state)
        pygame.display.flip()

    def draw_box_boundary(self, state: "GameState") -> None:
        # Get the size of the display
        screen_width, screen_height = state.DISPLAY.get_size()

        # Define the box size
        width, height = 600, 300

        y_axis_position_adjuster = 80

        # Calculate the top left position to center the box
        top_left_x = (screen_width - width) // 2
        top_left_y = (screen_height - height) // 2 - y_axis_position_adjuster
        top_left = (top_left_x, top_left_y)

        # Define the color for the box
        color = (255, 255, 255)

        # Draw the four lines to create the box
        pygame.draw.line(state.DISPLAY, color, top_left, (top_left[0] + width, top_left[1]), 2)  # Top line
        pygame.draw.line(state.DISPLAY, color, top_left, (top_left[0], top_left[1] + height), 2)  # Left line
        pygame.draw.line(state.DISPLAY, color, (top_left[0] + width, top_left[1]), (top_left[0] + width, top_left[1] + height), 2)  # Right line
        pygame.draw.line(state.DISPLAY, color, (top_left[0], top_left[1] + height), (top_left[0] + width, top_left[1] + height), 2)  # Bottom line

        # Save box boundaries
        self.box_top_left = top_left
        self.box_bottom_right = (top_left[0] + width, top_left[1] + height)

    def draw_human(self, state: "GameState") -> None:
        # Define the color for the text
        color = (255, 255, 255)

        for label, data in self.humans.items():
            # Render the text
            text_surface = self.font.render(label, True, color)
            # Get the text's rectangle and set its position to the ball's position
            text_rect = text_surface.get_rect(center=(data["pos"][0] + self.human_size // 2, data["pos"][1] + self.human_size // 2))
            # Draw the text
            state.DISPLAY.blit(text_surface, text_rect)

        if self.hippo:
            # Render the hippo text
            text_surface = self.font.render("H1", True, color)
            text_rect = text_surface.get_rect(center=(self.hippo["pos"][0] + self.human_size // 2, self.hippo["pos"][1] + self.human_size // 2))
            state.DISPLAY.blit(text_surface, text_rect)

    def draw_bottom_black_box(self, state: "GameState") -> None:
        black_box_height = 130
        black_box_width = 700
        border_width = 5

        black_box = pygame.Surface((black_box_width, black_box_height))
        black_box.fill((0, 0, 0))

        white_border = pygame.Surface((black_box_width + 2 * border_width, black_box_height + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))

        screen_width, screen_height = state.DISPLAY.get_size()
        black_box_x = (screen_width - black_box_width) // 2 - border_width
        black_box_y = screen_height - black_box_height - 20 - border_width

        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

    def move_human(self, delta_time: float) -> None:
        for label, data in list(self.humans.items()):
            # Move the balls left by their speed scaled by delta_time
            data["pos"][0] -= data["speed"] * delta_time

            # Check for collision with the left line of the box (indicating they've reached the boundary)
            if data["pos"][0] <= self.box_top_left[0]:
                data["pos"][0] = self.box_top_left[0]
                self.winners.append(label)  # Add the human to the winners list
                del self.humans[label]  # Remove the human from the dictionary
                print(str(self.winners))

    def move_hippo(self, delta_time: float) -> None:
        # Check if the hippo is currently eating
        if time.time() - self.hippo_stopping_eating < 4:
            return

        closest_human = self.find_closest_human()
        if closest_human[0] is None:
            return

        label, human_x, human_y = closest_human
        hippo_x, hippo_y = self.hippo["pos"]

        # Calculate direction to move
        if hippo_x < human_x:
            self.hippo["pos"][0] += self.hippo["speed"] * delta_time
        elif hippo_x > human_x:
            self.hippo["pos"][0] -= self.hippo["speed"] * delta_time

        if hippo_y < human_y:
            self.hippo["pos"][1] += self.hippo["speed"] * delta_time
        elif hippo_y > human_y:
            self.hippo["pos"][1] -= self.hippo["speed"] * delta_time

        # Check for collision and remove human if collided
        self.check_collisions()

    def check_collisions(self) -> None:
        hippo_rect = pygame.Rect(self.hippo["pos"][0], self.hippo["pos"][1], self.human_size, self.human_size)
        humans_to_remove = []
        for label, data in self.humans.items():
            ball_rect = pygame.Rect(data["pos"][0], data["pos"][1], self.human_size, self.human_size)
            if hippo_rect.colliderect(ball_rect):
                humans_to_remove.append(label)
                self.hippo_stopping_eating = time.time()  # Set the time when the hippo starts eating

        for label in humans_to_remove:
            del self.humans[label]
