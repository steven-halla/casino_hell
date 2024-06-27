import pygame
import random
from entity.gui.screen.battle_screen import BattleScreen
from entity.gui.textbox.text_box import TextBox
from screen.examples.screen import Screen


#lets keep it random
# maybe have an item that changes it to non random
#or perhaps the 2nd rib demon slots machine just has it that way to where its non random?

class SlotsRibDemonJackRipperScreen(Screen):
    def __init__(self) -> None:
        super().__init__("Casino Slots Screen")

        self.slot1: list[int] = [random.randint(0, 9) for _ in range(3)]  # Extra number for next row
        self.slot2: list[int] = [random.randint(0, 9) for _ in range(3)]
        self.slot3: list[int] = [random.randint(0, 9) for _ in range(3)]
        self.slot_positions: list[int] = [-50, 0, 50]  # Adjust positions to fit 3 numbers
        self.last_a_press_time: int = 0  # Initialize in __init__ method
        self.counter = 0
        self.stopping: bool = False  # Flag to indicate if stopping
        self.stop_start_time: int = 0  # Time when stopping started




        self.new_font: pygame.font.Font = pygame.font.Font(None, 36)
        self.game_state: str = "welcome_screen"
        self.bet: int = 0
        self.money: int = 1000
        self.font: pygame.font.Font = pygame.font.Font(None, 36)
        self.battle_messages: dict[str, TextBox] = {
            "welcome_message": TextBox(
                ["Are you here for some rib demon slots?", ""],
                (65, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "spin_message": TextBox(
                ["Press the A key in order to Spin", ""],
                (65, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            # You can add more game state keys and TextBox instances here
        }

        self.spinning: bool = False
        self.hide_numbers: bool = True  # Initialize hide_numbers variable
        self.last_update_time: int = pygame.time.get_ticks()
        self.spin_delay: int = 44  # Speed of the spin (lower is faster)
        self.last_a_press_time: int = 0  # Initialize in __init__ method

    def print_current_slots(self) -> None:
        """Prints the current numbers visible in the slots."""
        # Assuming slot1, slot2, slot3 contain the numbers
        # And slot_positions contain the vertical positions of these numbers
        visible_slots = [self.slot1[1], self.slot2[1], self.slot3[1]]  # Adjust to get the visible numbers
        # print(f"Current Slots: {visible_slots}")

    def update(self, state: "GameState") -> None:
        current_time: int = pygame.time.get_ticks()

        if self.game_state == "welcome_screen":
            self.battle_messages["welcome_message"].update(state)

        if self.battle_messages["welcome_message"].message_index == 1:
            self.game_state = "spin_screen"

        if self.game_state == "spin_screen":
            self.battle_messages["spin_message"].update(state)

        if self.spinning:
            if current_time - self.last_update_time > self.spin_delay:
                self.last_update_time = current_time
                for i in range(3):
                    self.slot_positions[i] += 10
                    if self.slot_positions[i] >= 100:
                        self.slot_positions[i] = -50
                        self.slot1[i] = random.randint(0, 9)
                        self.slot2[i] = random.randint(0, 9)
                        self.slot3[i] = random.randint(0, 9)

            # Check if we need to stop the spin
            if self.stopping:
                if current_time - self.stop_start_time >= 2000:  # 2 seconds delay
                    self.counter += 1
                    if self.counter >= 5:  # Stop after 5 iterations
                        self.spinning = False
                        self.stopping = False
                        self.counter = 0  # Reset counter
                        print("Spinning stopped.")
                        # Ensure middle index is aligned
                        self.slot_positions = [0, 50, 100]
                        print(f"Stopped Slots: {[self.slot1[0], self.slot2[0], self.slot3[0]]}")

        if state.controller.isQPressed:
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return

        if state.controller.isAPressed and not self.a_key_pressed:
            self.a_key_pressed = True
            self.last_a_press_time = current_time
            if not self.spinning:
                self.spinning = True
                self.stopping = False
                self.spin_delay = 70  # Reset spin delay
                print("Spinning started.")
            else:
                self.stopping = True
                self.stop_start_time = current_time  # Start the delay timer
                print("Stopping initiated.")

        if not state.controller.isAPressed:
            self.a_key_pressed = False

        if state.controller.isBPressed:
            self.hide_numbers = not self.hide_numbers  # Toggle hide_numbers

        # Update the controller
        controller = state.controller
        controller.update()

    def draw_bottom_black_box(self, state: "GameState") -> None:
        # Define the dimensions and position of the bottom black box
        black_box_height = 130
        black_box_width = 700
        border_width = 5  # Width of the white border

        # Create the black box
        black_box = pygame.Surface((black_box_width, black_box_height))
        black_box.fill((0, 0, 0))  # Fill the box with black color

        # Create a white border
        white_border = pygame.Surface((black_box_width + 2 * border_width, black_box_height + 2 * border_width))
        white_border.fill((255, 255, 255))  # Fill the border with white color
        white_border.blit(black_box, (border_width, border_width))

        # Determine the position of the white-bordered box
        screen_width, screen_height = state.DISPLAY.get_size()
        black_box_x = (screen_width - black_box_width) // 2 - border_width
        black_box_y = screen_height - black_box_height - 20 - border_width  # Subtract 20 pixels and adjust for border

        # Blit the white-bordered box onto the display
        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

    def draw(self, state: "GameState") -> None:
        state.DISPLAY.fill((0, 0, 51))

        # Draw the hero's info boxes
        self.draw_hero_info_boxes(state)

        # Draw the grid box with the current slot values
        self.draw_grid_box(state)

        # Draw the mask box if hide_numbers is True
        if self.hide_numbers:
            self.draw_mask_box(state)

        # Draw the bottom black box
        self.draw_bottom_black_box(state)

        # Draw battle messages
        if self.game_state == "welcome_screen":
            self.battle_messages["welcome_message"].draw(state)

        elif self.game_state == "spin_screen":
            self.battle_messages["spin_message"].draw(state)

        # Flip the display
        pygame.display.flip()

    def draw_hero_info_boxes(self, state: "GameState") -> None:
        # Draw the black box for hero info
        black_box = pygame.Surface((200 - 10, 180 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 235))

        # Draw the black box for hero name
        black_box = pygame.Surface((200 - 10, 45 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 45 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 195))

        # Draw hero info texts
        state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True, (255, 255, 255)), (37, 250))
        state.DISPLAY.blit(self.font.render(f"HP: {state.player.stamina_points}", True, (255, 255, 255)), (37, 290))
        state.DISPLAY.blit(self.font.render(f"MP: {state.player.focus_points}", True, (255, 255, 255)), (37, 330))
        state.DISPLAY.blit(self.font.render(f"Hero", True, (255, 255, 255)), (37, 205))

        # Draw enemy info box and texts
        self.draw_enemy_info_box(state)

    def draw_enemy_info_box(self, state: "GameState") -> None:
        black_box = pygame.Surface((200 - 10, 110 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 110 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 20))

        state.DISPLAY.blit(self.font.render("Enemy", True, (255, 255, 255)), (37, 33))

        black_box = pygame.Surface((200 - 10, 130 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 130 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 60))

        state.DISPLAY.blit(self.font.render(f"Money: {self.money}", True, (255, 255, 255)), (37, 70))
        state.DISPLAY.blit(self.font.render(f"Status: ", True, (255, 255, 255)), (37, 110))
        state.DISPLAY.blit(self.font.render(f"Bet: {self.bet}", True, (255, 255, 255)), (37, 370))

    def draw_grid_box(self, state: "GameState") -> None:
        """Draws a single row of 3 black boxes with the current slot values in the middle of the screen."""
        screen_width, screen_height = state.DISPLAY.get_size()
        grid_size = 3  # Number of columns
        box_size = 50
        line_thickness = 2
        total_grid_width = grid_size * box_size + (grid_size - 1) * line_thickness
        start_x = (screen_width - total_grid_width) // 2
        start_y = (screen_height - box_size) // 2  # Center vertically for a single row
        black_color = (0, 0, 0)
        white_color = (255, 255, 255)

        font = pygame.font.Font(None, 36)

        slots = [self.slot1, self.slot2, self.slot3]

        for col in range(grid_size):
            for i, pos in enumerate(self.slot_positions):
                box_x = start_x + col * (box_size + line_thickness)
                box_y = start_y + pos
                pygame.draw.rect(state.DISPLAY, black_color, (box_x, box_y, box_size, box_size))

                # Draw the current slot number in the center of each box
                number_text = font.render(str(slots[col][i]), True, white_color)
                text_rect = number_text.get_rect(center=(box_x + box_size // 2, box_y + box_size // 2))
                state.DISPLAY.blit(number_text, text_rect)

        # Draw the white lines
        y = start_y - line_thickness // 2
        pygame.draw.line(state.DISPLAY, white_color, (start_x, y), (start_x + total_grid_width - line_thickness, y), line_thickness)
        y = start_y + box_size + line_thickness // 2
        pygame.draw.line(state.DISPLAY, white_color, (start_x, y), (start_x + total_grid_width - line_thickness, y), line_thickness)

        for col in range(grid_size + 1):
            x = start_x + col * (box_size + line_thickness) - line_thickness // 2
            pygame.draw.line(state.DISPLAY, white_color, (x, start_y), (x, start_y + box_size), line_thickness)

    def draw_mask_box(self, state: "GameState") -> None:
        """Draws a mask box to hide numbers outside the white lines."""
        screen_width, screen_height = state.DISPLAY.get_size()
        grid_size = 3  # Number of columns
        box_size = 50
        line_thickness = 2
        total_grid_width = grid_size * box_size + (grid_size - 1) * line_thickness
        start_x = (screen_width - total_grid_width) // 2
        start_y = (screen_height - box_size) // 2  # Center vertically for a single row

        # Draw the mask box (black rectangle covering areas outside the grid)
        mask_box_top = pygame.Surface((total_grid_width, start_y))
        mask_box_bottom = pygame.Surface((total_grid_width, screen_height - (start_y + box_size)))
        mask_box_top.fill((0, 0, 51))
        mask_box_bottom.fill((0, 0, 51))

        # Adjust the mask box bottom to not overlap with the bottom white line
        state.DISPLAY.blit(mask_box_top, (start_x, 0))
        state.DISPLAY.blit(mask_box_bottom, (start_x, start_y + box_size + line_thickness))

    def print_current_slots(self) -> None:
        """Prints the current numbers visible in the slots."""
        # Assuming slot1, slot2, slot3 contain the numbers
        # And slot_positions contain the vertical positions of these numbers
        visible_slots = [self.slot1[1], self.slot2[1], self.slot3[1]]  # Adjust to get the visible numbers
        print(f"Current Slots: {visible_slots}")


