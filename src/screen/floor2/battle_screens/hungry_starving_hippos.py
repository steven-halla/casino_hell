import pygame
from entity.gui.textbox.text_box import TextBox
from screen.examples.screen import Screen
import time
import random
import math
from typing import Dict, Tuple, Optional, Any

# its possible to eat two humans need unique oen for htat
class HungryStarvingHippos(Screen):
    def __init__(self, screenName: str = "Casino Slots Screen") -> None:
        super().__init__(screenName)
        self.game_state: str = "welcome_screen"
        self.font = pygame.font.Font(None, 36)  # Initialize the font with size 36
        self.commentary = False
        self.comment_to_use = 0

        self.battle_messages: Dict[str, TextBox] = {
            "bet_message": TextBox(
                ["Select whom you think is going to win"],
                (65, 460, 700, 130),
                36,
                500
            ),
            "hippo_message_1": TextBox(
                ["Oh wow folks it's total carnage did you see him rip that human in half? The blood is in the water today for sure, it's too bad humans are terrible at swimming.  "],
                (65, 460, 700, 130),
                36,
                500
            ),
            "hippo_message_2": TextBox(
                ["I would like to remind everyone watching that hungry starving hipppos is sponsored by chicken nuggz. The only nuggz you need is chicken nuggz."],
                (65, 460, 700, 130),
                36,
                500
            ),
            "hippo_message_3": TextBox(
                ["That one is going in the books for sure folks, the way he tosssed her in the air and swallowed her whole!"],
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
        # self.initialize_human_position()

        self.last_time: float = time.time()
        self.start_time: float = time.time()  # Timer to track elapsed time

        self.winners = [] #important
        self.game_state: str = "bet_screen" #important
        self.bet_selection = ["A1", "B1", "C1", "D1", "E1", "A2", "B2", "C2", "D2", "E2"] #important
        self.bet_selection_index = 0 #important
        self.human_picks = []

    def draw_bet_selection(self, state: "GameState") -> None:
        screen_width, screen_height = state.DISPLAY.get_size()
        box_width, box_height = 300, len(self.bet_selection) * 40  # Adjust height based on the number of items

        top_left_x = (screen_width - box_width) // 2
        top_left_y = (screen_height - box_height) // 2 - 50  # Move up by 50 pixels
        arrow_x_axis = top_left_x - 30 + 100  # Move arrow to the right by 100 pixels

        # Update the bet_message with selected humans
        selected_humans_text = "Press A when ready: Selected humans: " + ", ".join(self.human_picks)
        self.battle_messages["bet_message"].messages = [selected_humans_text]

        for i, item in enumerate(self.bet_selection):
            color = (0, 255, 0) if i == self.bet_selection_index else (255, 255, 255)  # Green for selected item
            text_surface = self.font.render(item, True, color)
            text_rect = text_surface.get_rect(center=(top_left_x + box_width // 2, top_left_y + (i * 40) + 20))
            state.DISPLAY.blit(text_surface, text_rect)

            if i == self.bet_selection_index:
                arrow_surface = self.font.render("->", True, (255, 255, 255))
                arrow_rect = arrow_surface.get_rect(center=(arrow_x_axis, top_left_y + (i * 40) + 20))
                state.DISPLAY.blit(arrow_surface, arrow_rect)

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

        if self.game_state == "bet_screen":
            self.battle_messages["bet_message"].update(state)

            if controller.isTPressed and len(self.human_picks) < 3:
                controller.isTPressed = False
                selected_human = self.bet_selection[self.bet_selection_index]
                if selected_human not in self.human_picks:
                    self.human_picks.append(selected_human)
                    print(f"Human picks: {self.human_picks}")

            if controller.isBPressed and self.human_picks:
                controller.isBPressed = False
                self.human_picks.pop()
                print(f"Human picks: {self.human_picks}")

            if controller.isDownPressed:
                controller.isDownPressed = False
                if self.bet_selection_index < len(self.bet_selection) - 1:
                    self.bet_selection_index += 1
            elif controller.isUpPressed:
                controller.isUpPressed = False
                if self.bet_selection_index > 0:
                    self.bet_selection_index -= 1

            if controller.isAPressed and len(self.human_picks) == 3:
                self.game_state = "human_race"
                print("Game state changed to human_race")
                self.initialize_human_position()  # Ensure humans are initialized for the race
                self.start_time = time.time()  # Reset the timer for the race

        if self.game_state == "human_race":
            if not self.humans:
                print("All humans have been eaten or escaped!")
                self.game_state = "game_over"  # Example: Change the game state or take another action
                for bet in self.bet_selection:
                    if bet in self.human_picks:
                        print("Yay, you won!")
                        break  # Exit the loop after finding the first match

            # Calculate delta_time
            current_time = time.time()
            delta_time = current_time - self.last_time
            self.last_time = current_time

            # Initialize hippo position after 10 seconds
            if self.hippo is None and current_time - self.start_time >= 10:
                self.initialize_hippo_position()

            # Move the humans
            self.move_human(delta_time)

            # Move the hippo if it exists
            if self.hippo:
                self.move_hippo(delta_time)
                self.check_collisions()

            if self.commentary:
                if self.comment_to_use == 1:
                    self.battle_messages["hippo_message_1"].update(state)
                elif self.comment_to_use == 2:
                    self.battle_messages["hippo_message_2"].update(state)
                elif self.comment_to_use == 3:
                    self.battle_messages["hippo_message_3"].update(state)





    def draw(self, state: "GameState") -> None:
        state.DISPLAY.fill((0, 0, 51))
        self.draw_bottom_black_box(state)

        if self.game_state == "bet_screen":
            self.battle_messages["bet_message"].draw(state)
            self.draw_bet_selection(state)  # Add this line

        if self.game_state == "human_race":
            self.draw_box_boundary(state)
            self.draw_human(state)


            if self.commentary == True:

                if self.comment_to_use == 1:
                    self.battle_messages["hippo_message_1"].draw(state)
                elif self.comment_to_use == 2:
                    self.battle_messages["hippo_message_2"].draw(state)
                elif self.comment_to_use == 3:
                    self.battle_messages["hippo_message_3"].draw(state)

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
        # If the race just started, set the start time
        if not hasattr(self, 'human_race_start_time'):
            self.human_race_start_time = time.time()

        # Calculate the elapsed time
        elapsed_time = time.time() - self.human_race_start_time

        # Wait for 2 seconds before allowing humans to move
        if elapsed_time < 2.0:
            return

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
            activate_talking = random.randint(1,3)
            if activate_talking == 3:
                print("acticate talk")
                self.commentary = True
                self.comment_to_use = random.randint(1, 4)

            del self.humans[label]

            # i should build a counter for every human eating incrase counter by +1 for every even numbers, create the message.
