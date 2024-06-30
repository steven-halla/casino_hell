import pygame
from entity.gui.textbox.text_box import TextBox
from screen.examples.screen import Screen
import time

class HungryStarvingHippos(Screen):
    def __init__(self, screenName: str = "Casino Slots Screen") -> None:
        super().__init__(screenName)
        self.game_state: str = "welcome_screen"
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
        self.ball_pos = [0, 0]
        self.ball_vel = [0, -200]  # Negative for upward movement

        # Initialize box attributes
        self.box_top_left = (0, 0)
        self.box_bottom_right = (0, 0)

        # Initialize ball position (this should be done only once)
        self.initialize_ball_position()

        self.last_time = time.time()

    def initialize_ball_position(self):
        # Set the initial position of the ball
        width, height = 600, 300
        y_axis_position_adjuster = 80
        top_left_x = (800 - width) // 2
        top_left_y = (600 - height) // 2 - y_axis_position_adjuster
        top_left = (top_left_x, top_left_y)
        self.box_top_left = top_left
        self.box_bottom_right = (top_left[0] + width, top_left[1] + height)
        self.ball_pos = [self.box_top_left[0] + width // 2 - self.ball_size // 2, self.box_top_left[1] + height // 2 - self.ball_size // 2]

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

        # Move the ball
        self.move_ball(delta_time)

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
        # Define the color for the ball
        color = (255, 255, 255)

        # Draw the ball
        pygame.draw.rect(state.DISPLAY, color, (*self.ball_pos, self.ball_size, self.ball_size))

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
        # Move the ball by its velocity scaled by delta_time
        self.ball_pos[1] += self.ball_vel[1] * delta_time

        # Check for collision with the top and bottom lines of the box
        if self.ball_pos[1] <= self.box_top_left[1] or self.ball_pos[1] + self.ball_size >= self.box_bottom_right[1]:
            self.ball_pos[1] = max(self.box_top_left[1], min(self.ball_pos[1], self.box_bottom_right[1] - self.ball_size))
            self.ball_vel[1] = -self.ball_vel[1]  # Reverse the vertical direction

        # Debugging print statements to verify movement logic
        print(f"Delta Time: {delta_time}")
        print(f"Ball Position after move: {self.ball_pos}")
        print(f"Ball Velocity: {self.ball_vel}")
