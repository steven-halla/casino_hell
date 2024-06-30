from typing import Optional
import pygame
from entity.gui.textbox.text_box import TextBox
from screen.examples.screen import Screen

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

    def update(self, state: "GameState") -> None:
        pygame.mixer.music.stop()
        if state.controller.isQPressed:
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return

        controller = state.controller
        controller.update()

    def draw(self, state: "GameState") -> None:
        state.DISPLAY.fill((0, 0, 51))
        self.draw_box_boundary(state)
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

