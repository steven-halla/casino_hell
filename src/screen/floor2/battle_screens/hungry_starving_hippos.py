import pygame
from entity.gui.textbox.text_box import TextBox
from screen.examples.screen import Screen
import time

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
        self.ball_pos = [0, 0]
        self.ball_vel = [0, -200]  # Negative for upward movement
        self.move_left_speed = 200  # Speed for leftward movement

        # Initialize box attributes
        self.box_top_left = (0, 0)
        self.box_bottom_right = (0, 0)

        self.last_time = time.time()


        # Initialize ball position (this should be done only once)
        self.initialize_ball_position()

        self.last_time = time.time()
        self.human_eating = False

        self.ball_y_position = 0
        self.move_left_speed = 30  # Speed for leftward movement

    def initialize_ball_position(self):
        # Set the initial position of the ball near the right edge of the box
        width, height = 600, 300
        y_axis_position_adjuster = 80
        top_left_x = (800 - width) // 2
        top_left_y = (600 - height) // 2 - y_axis_position_adjuster
        top_left = (top_left_x, top_left_y)
        self.box_top_left = top_left
        self.box_bottom_right = (top_left[0] + width, top_left[1] + height)
        self.ball_x_position = self.box_bottom_right[0] - self.ball_size - 20  # 20 pixels from the right edge
        self.ball_y_position = self.box_top_left[1] + height // 2 - self.ball_size // 2
        self.ball_pos = [self.ball_x_position, self.ball_y_position]

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
        # Define the color for the text
        color = (255, 255, 255)

        # Render the text "A1"
        text_surface = self.font.render("A1", True, color)

        # Get the text's rectangle and set its position to the ball's position
        text_rect = text_surface.get_rect(center=(self.ball_pos[0] + self.ball_size // 2, self.ball_pos[1] + self.ball_size // 2))

        # Draw the text
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
        # Move the ball left by its speed scaled by delta_time
        self.ball_pos[0] -= self.move_left_speed * delta_time

        # Check for collision with the left and right lines of the box
        if self.ball_pos[0] <= self.box_top_left[0] or self.ball_pos[0] + self.ball_size >= self.box_bottom_right[0]:
            self.ball_pos[0] = max(self.box_top_left[0], min(self.ball_pos[0], self.box_bottom_right[0] - self.ball_size))
            self.move_left_speed = -self.move_left_speed  # Reverse the horizontal direction

        # Debugging print statements to verify movement logic
        print(f"Delta Time: {delta_time}")
        print(f"Ball Position after move: {self.ball_pos}")
        print(f"Move Left Speed: {self.move_left_speed}")
