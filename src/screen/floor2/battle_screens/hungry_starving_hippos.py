import pygame
from entity.gui.textbox.text_box import TextBox
from screen.examples.screen import Screen
import time
import random

class HungryStarvingHippos(Screen):
    def __init__(self, screenName: str = "Casino Slots Screen") -> None:
        super().__init__(screenName)
        self.game_state: str = "welcome_screen"
        self.font = pygame.font.Font(None, 36)  # Initialize the font with size 36

        self.battle_messages: dict[str, TextBox] = {
            "welcome_message": TextBox(
                [" "],
                (65, 460, 700, 130),
                36,
                500
            ),
        }

        # Ball attributes
        self.ball_size = 20
        self.balls = {}  # Dictionary to store ball positions and speeds
        self.hippo = None  # Dictionary to store hippo position and speed

        # Initialize box attributes
        self.box_top_left = (0, 0)
        self.box_bottom_right = (0, 0)

        # Initialize ball positions (this should be done only once)
        self.initialize_ball_position()

        self.last_time = time.time()
        self.start_time = time.time()  # Timer to track elapsed time

    def initialize_ball_position(self):
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
            initial_x = self.box_bottom_right[0] - self.ball_size - 20
            initial_y = self.box_top_left[1] + height // 2 - self.ball_size // 2 - (i * 20) + 60  # Move down by 60 pixels
            move_speed = random.randint(150, 250)  # Assign a unique speed for each ball
            self.balls[label] = {"pos": [initial_x, initial_y], "speed": move_speed}

    def initialize_hippo_position(self):
        width, height = 600, 300
        initial_x = self.box_bottom_right[0] - self.ball_size - 20
        initial_y = self.box_top_left[1] + height // 2 - self.ball_size // 2 + 60
        move_speed = random.randint(150, 250)
        self.hippo = {"pos": [initial_x, initial_y], "speed": move_speed}

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
        self.move_ball(delta_time)

        # Move the hippo if it exists
        if self.hippo:
            self.move_hippo(delta_time)
            self.check_collisions()

    def draw(self, state: "GameState") -> None:
        state.DISPLAY.fill((0, 0, 51))
        self.draw_box_boundary(state)
        self.draw_ball(state)
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

    def draw_ball(self, state: "GameState") -> None:
        # Define the color for the text
        color = (255, 255, 255)

        for label, data in self.balls.items():
            # Render the text
            text_surface = self.font.render(label, True, color)
            # Get the text's rectangle and set its position to the ball's position
            text_rect = text_surface.get_rect(center=(data["pos"][0] + self.ball_size // 2, data["pos"][1] + self.ball_size // 2))
            # Draw the text
            state.DISPLAY.blit(text_surface, text_rect)

        if self.hippo:
            # Render the hippo text
            text_surface = self.font.render("H1", True, color)
            text_rect = text_surface.get_rect(center=(self.hippo["pos"][0] + self.ball_size // 2, self.hippo["pos"][1] + self.ball_size // 2))
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

    def move_ball(self, delta_time: float) -> None:
        for label, data in self.balls.items():
            # Move the balls left by their speed scaled by delta_time
            data["pos"][0] -= data["speed"] * delta_time

            # Check for collision with the left and right lines of the box
            if data["pos"][0] <= self.box_top_left[0] or data["pos"][0] + self.ball_size >= self.box_bottom_right[0]:
                data["pos"][0] = max(self.box_top_left[0], min(data["pos"][0], self.box_bottom_right[0] - self.ball_size))
                data["speed"] = -data["speed"]  # Reverse the horizontal direction

    def move_hippo(self, delta_time: float) -> None:
        # Move the hippo left by its speed scaled by delta_time
        self.hippo["pos"][0] -= self.hippo["speed"] * delta_time

        # Check for collision with the left and right lines of the box
        if self.hippo["pos"][0] <= self.box_top_left[0] or self.hippo["pos"][0] + self.ball_size >= self.box_bottom_right[0]:
            self.hippo["pos"][0] = max(self.box_top_left[0], min(self.hippo["pos"][0], self.box_bottom_right[0] - self.ball_size))
            self.hippo["speed"] = -self.hippo["speed"]  # Reverse the horizontal direction

    def check_collisions(self) -> None:
        # Check for collisions between the hippo and the balls
        hippo_rect = pygame.Rect(self.hippo["pos"][0], self.hippo["pos"][1], self.ball_size, self.ball_size)
        balls_to_remove = []
        for label, data in self.balls.items():
            ball_rect = pygame.Rect(data["pos"][0], data["pos"][1], self.ball_size, self.ball_size)
            if hippo_rect.colliderect(ball_rect):
                balls_to_remove.append(label)

        for label in balls_to_remove:
            del self.balls[label]
