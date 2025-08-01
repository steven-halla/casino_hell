import pygame
from entity.gui.textbox.text_box import TextBox
from game_constants.equipment import Equipment
from screen.examples.screen import Screen
import time
import random
import math
from typing import Dict, Tuple, List, Optional,Union ,  Any

# its possible to eat two humans need unique message for that
# hippo should appear at random locations to make it more fare
class HungryStarvingHipposLucyScreen(Screen):
    def __init__(self, screenName: str = "Casino Hippo Screen") -> None:
        super().__init__(screenName)
        self.game_state: str = "welcome_screen"
        self.money_reward = 500
        self.font = pygame.font.Font(None, 36)  # Initialize the font with size 36
        self.commentary = False
        self.comment_to_use = 0

        self.hippo2_stopping_eating: float = 0

        self.sprite_sheet_hippo_facing_right: pygame.Surface = pygame.image.load("./assets/images/hippo_facing_right.png")

        self.human_stats = {
            "A1": {"name": "A1", "speed": 22, "stamina": 7, "win_chance": 30},
            "B1": {"name": "B1", "speed": 7, "stamina": 10, "win_chance": 40},
            "C1": {"name": "C1", "speed": 9, "stamina": 5, "win_chance": 20},
            "E1": {"name": "E1", "speed": 9, "stamina": 6, "win_chance": 25},
            "A2": {"name": "A2", "speed": 10, "stamina": 5, "win_chance": 50},
            "B2": {"name": "B2", "speed": 6, "stamina": 9, "win_chance": 15},
            "C2": {"name": "C2", "speed": 9, "stamina": 7, "win_chance": 45},
            "D2": {"name": "D2", "speed": 8, "stamina": 8, "win_chance": 30},
            "E2": {"name": "E2", "speed": 7, "stamina": 9, "win_chance": 20},
            "D1": {"name": "D1", "speed": 6, "stamina": 8, "win_chance": 35},

        }

        self.battle_messages: Dict[str, TextBox] = {
            "bet_message": TextBox(
                ["Select whom you think is going to win"],
                (65, 460, 700, 130),
                36,
                500
            ),
            "you_win": TextBox(
                ["Congrats on your win here is 500 coins and a special prize enjoy", ""],
                (65, 460, 700, 130),
                36,
                500
            ),
            "you_lose": TextBox(
                ["Better luck next time", ""],
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
                ["I would like to remind everyone watching that hungry starving hipppos is sponsored by chicken nuggz. The    only nuggz you need is chicken nuggz."],
                (65, 460, 700, 130),
                36,
                500
            ),
            "hippo_message_3": TextBox(
                ["That one is going in the books for sure folks, the way he tossed her in the air and swallowed her whole was AMAZING!!! The crowd is going wild!!!"],
                (65, 460, 700, 130),
                36,
                500
            ),
            "hippo_message_4": TextBox(
                ["That human must be a pop star because they just    exploded!"],
                (65, 460, 700, 130),
                36,
                500
            ),

        }

        # Second hippo attributes
        self.hippo2: Optional[Dict[str, Any]] = None
        self.hippo2_charge_used: bool = False
        self.hippo2_charge_start_time: Optional[float] = None

        # human attributes
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
        self.win = False

    def human_stamina(self) -> None:
        # Ensure human stamina reduction only starts after the initial 10 seconds
        if not hasattr(self, 'stamina_start_time'):
            self.stamina_start_time = time.time()

        # Calculate elapsed time
        elapsed_time = time.time() - self.stamina_start_time

        # After 10 seconds, start reducing stamina every 3 seconds
        if elapsed_time > 10:
            # Calculate how many 3-second intervals have passed
            stamina_intervals = int((elapsed_time - 10) // 5)

            # Reduce stamina for each human based on the number of intervals passed
            for label, data in self.humans.items():
                if not hasattr(data, 'last_stamina_tick'):
                    data['last_stamina_tick'] = 0  # Initialize if not already set

                # Check if it's time to reduce stamina
                if stamina_intervals > data['last_stamina_tick']:
                    data['last_stamina_tick'] = stamina_intervals

                    # Reduce stamina by 1
                    if self.human_stats[label]['stamina'] > 0:  # Make sure you reference `self.human_stats`
                        self.human_stats[label]['stamina'] -= 1
                        print(f"Reduced stamina for {label} to {self.human_stats[label]['stamina']}")

                    # If stamina reaches 0, reduce speed by 4
                    if self.human_stats[label]['stamina'] == 0 and self.human_stats[label]['speed'] > 4:
                        self.human_stats[label]['speed'] = 4
                        print(f"{label}'s speed reduced to {self.human_stats[label]['speed']} due to low stamina.")

    def draw_bet_selection(self, state: "GameState") -> None:
        screen_width, screen_height = state.DISPLAY.get_size()
        box_width, box_height = 300, len(self.bet_selection) * 40  # Adjust height based on the number of items

        top_left_x = (screen_width - box_width) // 2 - 120  # Move box 120 pixels to the left
        top_left_y = (screen_height - box_height) // 2 - 50  # Move up by 50 pixels
        arrow_x_axis = top_left_x - 50 + 100  # Adjust arrow position

        # Dictionary holding unique stats for each human
        self.human_stats = {
            "A1": {"name": "A1", "speed": 10, "stamina": 7, "win_chance": 30},
            "B1": {"name": "B1", "speed": 7, "stamina": 10, "win_chance": 40},
            "C1": {"name": "C1", "speed": 9, "stamina": 5, "win_chance": 20},
            "E1": {"name": "E1", "speed": 9, "stamina": 6, "win_chance": 25},
            "A2": {"name": "A2", "speed": 10, "stamina": 5, "win_chance": 50},
            "B2": {"name": "B2", "speed": 6, "stamina": 9, "win_chance": 15},
            "C2": {"name": "C2", "speed": 9, "stamina": 7, "win_chance": 45},
            "D2": {"name": "D2", "speed": 8, "stamina": 8, "win_chance": 30},
            "E2": {"name": "E2", "speed": 7, "stamina": 9, "win_chance": 20},
            "D1": {"name": "D1", "speed": 6, "stamina": 8, "win_chance": 35},

        }

        # Update the bet_message with selected humans
        selected_humans_text = "Press A when ready: Selected humans: " + ", ".join(self.human_picks)
        self.battle_messages["bet_message"].messages = [selected_humans_text]

        for i, item in enumerate(self.bet_selection):
            # Change this line

            # To this line, since `human_stats` is a class attribute
            human = self.human_stats[item]

            # Render human label (A1, B1, etc.) and move it 30 pixels further left to prevent overlap
            color = (0, 255, 0) if i == self.bet_selection_index else (255, 255, 255)  # Green for selected item
            text_surface = self.font.render(f"{human['name']}", True, color)
            text_rect = text_surface.get_rect(center=(top_left_x + box_width // 2 - 50, top_left_y + (i * 40) + 20))
            state.DISPLAY.blit(text_surface, text_rect)

            # Display speed, stamina, and win chance next to the human's name
            stats_surface = self.font.render(
                f"Speed: {human['speed']}, Stamina: {human['stamina']}", True, (255, 255, 255)
            )
            stats_rect = stats_surface.get_rect(center=(text_rect.centerx + 250, text_rect.centery))
            state.DISPLAY.blit(stats_surface, stats_rect)

            if i == self.bet_selection_index:
                arrow_surface = self.font.render("->", True, (255, 255, 255))
                arrow_rect = arrow_surface.get_rect(center=(arrow_x_axis, top_left_y + (i * 40) + 16))
                state.DISPLAY.blit(arrow_surface, arrow_rect)

    def initialize_human_position(self, state) -> None:
        # Set the initial position of the humans
        width, height = 600, 300
        y_axis_position_adjuster = 80
        top_left_x = (800 - width) // 2
        top_left_y = (600 - height) // 2 - y_axis_position_adjuster
        top_left = (top_left_x, top_left_y)
        self.box_top_left = top_left
        self.box_bottom_right = (top_left[0] + width, top_left[1] + height)

        labels = ["A1", "B1", "C1", "D1", "E1", "A2", "B2", "C2", "D2", "E2"]
        random.shuffle(labels)  # ← This line randomizes the order every time

        # DO NOT ERASE THE BELOW EVER
        # THE BELOW IS WHAT ACTUALLY SETS FOR THE GAME
        self.human_stats = {
            "A1": {"speed": 9, "stamina": 4, "win_chance": 30},
            "B1": {"speed": 6, "stamina": 10, "win_chance": 40},
            "C1": {"speed": 7, "stamina": 6, "win_chance": 20},
            "E1": {"speed": 9, "stamina": 5, "win_chance": 25},
            "A2": {"speed": 5, "stamina": 15, "win_chance": 50},
            "B2": {"speed": 6, "stamina": 11, "win_chance": 15},
            "C2": {"speed": 7, "stamina": 7, "win_chance": 45},
            "D2": {"speed": 8, "stamina": 8, "win_chance": 30},
            "E2": {"speed": 7, "stamina": 9, "win_chance": 20},
            "D1": {"speed": 6, "stamina": 8, "win_chance": 35},

        }




        if Equipment.BACKWARDS_WATCH.value in state.player.equipped_items:
            for label in self.human_stats:
                if label not in self.human_picks:
                    self.human_stats[label]["speed"] -= 1
                    self.human_stats[label]["stamina"] -= 1


        for label in self.human_picks:
            if label in self.human_stats:
                if state.player.luck == 1:
                    self.human_stats[label]["speed"] += 1
                elif state.player.luck == 2:
                    self.human_stats[label]["speed"] += 1
                    self.human_stats[label]["stamina"] += 1
                elif state.player.luck == 3:
                    self.human_stats[label]["speed"] += 2
                    self.human_stats[label]["stamina"] += 1
                elif state.player.luck == 4:
                    self.human_stats[label]["speed"] += 2
                    self.human_stats[label]["stamina"] += 2
                elif state.player.luck == 5:
                    self.human_stats[label]["speed"] += 3
                    self.human_stats[label]["stamina"] += 3

        # Assign positions and sttats to each human
        for i, label in enumerate(labels):
            initial_x = self.box_bottom_right[0] - self.human_size - 20
            initial_y = self.box_top_left[1] + height // 2 - self.human_size // 2 - (i * 20) + 60  # Move down by 60 pixels

            # Assign position and stats
            self.humans[label] = {
                "pos": [initial_x, initial_y],
                "speed": self.human_stats[label]["speed"],
                "stamina": self.human_stats[label]["stamina"]
                # "win_chance": self.human_stats[label]["win_chance"]
            }

    def initialize_hippo_position(self) -> None:
        width, height = 600, 200
        initial_x = self.box_bottom_right[0] - self.human_size - 20
        initial_y = self.box_top_left[1] + height // 2 - self.human_size // 2 + 60
        move_speed = 16
        self.hippo = {"pos": [initial_x, initial_y], "speed": move_speed}

    def find_closest_human(self) -> Tuple[Optional[str], Optional[int], Optional[int]]:
        if not self.hippo or not self.humans:
            # No human X, Y, no string name
            return None, None, None

        # Get the current position of the hippo
        hippo_x, hippo_y = self.hippo["pos"]
        # Initialize the closest human as None and set the starting distance to infinity

        closest_human = None
        closest_distance = float('inf')
        detection_range = 10

        # First: find someone close enough
        for label, data in self.humans.items():
            human_x, human_y = data["pos"]
            distance = math.hypot(human_x - hippo_x, human_y - hippo_y)

            if distance < detection_range:
                return label, human_x, human_y  # Immediate priority

            if distance < closest_distance:
                closest_distance = distance
                closest_human = (label, human_x, human_y)

        # No one close → stick with existing random target or pick one
        if not hasattr(self, "hippo_target_label") or self.hippo_target_label not in self.humans:
            self.hippo_target_label = random.choice(list(self.humans.keys()))

        pos = self.humans[self.hippo_target_label]["pos"]
        return self.hippo_target_label, pos[0], pos[1]

    def update(self, state: "GameState") -> None:
        # print(self.human_stats)
        # for label, stats in self.human_stats.items():
        #     print(f"{label}: Speed={stats['speed']}, Stamina={stats['stamina']}, Win Chance={stats['win_chance']}")
        pygame.mixer.music.stop()
        if state.controller.isQPressed:
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return

        controller = state.controller
        controller.update()

        if self.game_state == "bet_screen":
            self.battle_messages["bet_message"].update(state)

            if controller.confirm_button and len(self.human_picks) < 3:

                selected_human = self.bet_selection[self.bet_selection_index]
                if selected_human not in self.human_picks:
                    self.human_picks.append(selected_human)
                    print(f"Human picks: {self.human_picks}")

            if controller.action_and_cancel_button and self.human_picks:

                self.human_picks.pop()

            if controller.down_button:

                if self.bet_selection_index < len(self.bet_selection) - 1:
                    self.bet_selection_index += 1
            elif controller.up_button:

                if self.bet_selection_index > 0:
                    self.bet_selection_index -= 1

            if controller.start_button and len(self.human_picks) == 3:
                self.game_state = "human_race"
                self.initialize_human_position(state)  # Ensure humans are initialized for the race
                self.start_time = time.time()  # Reset the timer for the race

        if self.game_state == "human_race":
            if not self.humans:
                print("All humans have been eaten or escaped!")
                print(self.winners)
                print(self.human_picks)

                self.game_state = "game_over"  # Example: Change the game state or take another action
                for bet in self.winners:
                    if bet in self.human_picks:
                        state.player.money += self.money_reward
                        print("Yay, you won!")
                        self.game_state = "you_win_screen"
                        break  # Exit the loop after finding a winning bet
                else:
                    self.game_state = "you_lose_screen"
                    print("Sorry, you lost.")

            # Calculate delta_time
            current_time = time.time()
            delta_time = current_time - self.last_time
            self.last_time = current_time

            self.human_stamina()

            # Initialize hippo position after 10 seconds
            if self.hippo is None and current_time - self.start_time >= 10 and Equipment.HIPPO_HOUR_GLASS.value not in state.player.equipped_items:
                self.initialize_hippo_position()
                print("No item equipped")

            if self.hippo2 is None and current_time - self.start_time >= 15 and Equipment.HIPPO_HOUR_GLASS.value not in state.player.equipped_items:
                initial_x = self.box_bottom_right[0] - self.human_size - 150
                initial_y = self.box_top_left[1] + (600 // 2) - (self.human_size // 2)

                self.hippo2 = {
                    "pos": [initial_x, initial_y]
                }
                print("Second hippo appeared!")

            if self.hippo is None and current_time - self.start_time >= 13 and Equipment.HIPPO_HOUR_GLASS.value in state.player.equipped_items:
                self.initialize_hippo_position()
                print("No item equipped")

            if self.hippo2 is None and current_time - self.start_time >= 18 and Equipment.HIPPO_HOUR_GLASS.value in state.player.equipped_items:
                initial_x = self.box_bottom_right[0] - self.human_size - 150
                initial_y = self.box_top_left[1] + (600 // 2) - (self.human_size // 2)

                self.hippo2 = {
                    "pos": [initial_x, initial_y]
                }
                print("Second hippo appeared!")



            # Move the humans
            self.move_human(delta_time)

            # Move the hippo if it exists
            if self.hippo:
                self.move_hippo(delta_time)
                self.check_collisions()
            if self.hippo2:
                self.move_hippo2(delta_time)
                self.check_collisions_for_hippo2()



            if self.commentary:
                if self.comment_to_use == 1:
                    self.battle_messages["hippo_message_1"].update(state)
                elif self.comment_to_use == 2:
                    self.battle_messages["hippo_message_2"].update(state)
                elif self.comment_to_use == 3:
                    self.battle_messages["hippo_message_3"].update(state)

                elif self.comment_to_use == 4:
                    self.battle_messages["hippo_message_4"].update(state)

        if self.game_state == "you_win_screen":
            print("you win scren is here")
            self.battle_messages["you_win"].update(state)

            if self.battle_messages["you_win"].message_index == 1:
                state.area_2_gambling_area_to_rest_point = True
                state.currentScreen = state.area2GamblingScreen
                state.area2GamblingScreen.start(state)
                state.area_2_gambling_area_to_rest_point = False
                print("yupper")
                state.player.canMove = True
                # state.player.items.append(Equipment.HIPPO_HOUR_GLASS.value)
                if state.player.current_stage == 2:
                    state.player.items.append(Equipment.HIPPO_HOUR_GLASS.value)

                # self.end_screen()

        if self.game_state == "you_lose_screen":
            print("you lose scren is here")
            self.battle_messages["you_lose"].update(state)

            if self.battle_messages["you_lose"].message_index == 1:

                self.battle_messages["you_lose"].update(state)
                state.area_2_gambling_area_to_rest_point = True
                state.player.canMove = True

                state.currentScreen = state.area2GamblingScreen
                state.area2GamblingScreen.start(state)
                state.area_2_gambling_area_to_rest_point = False





    def draw(self, state: "GameState") -> None:
        state.DISPLAY.fill((0, 0, 51))
        self.draw_bottom_black_box(state)

        if self.game_state == "bet_screen":
            self.battle_messages["bet_message"].draw(state)
            self.draw_bet_selection(state)  # Add this line
            self.display_hippos(state)

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
                elif self.comment_to_use == 4:
                    self.battle_messages["hippo_message_4"].draw(state)

        if self.game_state == "you_win_screen":
            self.battle_messages["you_win"].draw(state)

        if self.game_state == "you_lose_screen":
            self.battle_messages["you_lose"].draw(state)


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
        # Define the default color for the text (white)
        color = (255, 255, 255)
        # Define the color for the player's choice (green)
        player_choice_color = (0, 255, 0)

        for label, data in self.humans.items():
            # Check if the current human is in the player's picks
            if label in self.human_picks:
                # Use green for picked humans
                text_surface = self.font.render(label, True, player_choice_color)
            else:
                # Use white for other humans
                text_surface = self.font.render(label, True, color)

            # Get the text's rectangle and set its position to the human's position
            text_rect = text_surface.get_rect(center=(data["pos"][0] + self.human_size // 2, data["pos"][1] + self.human_size // 2))
            # Draw the text
            state.DISPLAY.blit(text_surface, text_rect)

        if self.hippo:
            # Render the hippo text
            # text_surface = self.font.render("H1", True, color)
            # text_rect = text_surface.get_rect(center=(self.hippo["pos"][0] + self.human_size // 2, self.hippo["pos"][1] + self.human_size // 2))
            # state.DISPLAY.blit(text_surface, text_rect)
            self.display_hippos(state)

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
        # print("Moving humans...")

        # If the race just started, set the start time
        if not hasattr(self, 'human_race_start_time'):
            self.human_race_start_time = time.time()

        # Calculate the elapsed time
        elapsed_time = time.time() - self.human_race_start_time
        # print(f"Elapsed time: {elapsed_time}")

        # Wait for 2 seconds before allowing humans to move
        if elapsed_time < 2.0:
            # print("Humans cannot move yet, waiting for 2 seconds.")
            return

        # print(f"Humans before move: {self.humans}")  # Debug to ensure humans are initialized

        for label, data in list(self.humans.items()):
            # Print human position before moving
            # print(f"Before move - {label}: {data['pos'][0]}")

            # Move the humans left by their speed scaled by delta_time
            data["pos"][0] -= data["speed"] * delta_time

            # Print human position after moving
            # print(f"After move - {label}: {data['pos'][0]}")

            # Check if the human reached the finish line
            if data["pos"][0] <= self.box_top_left[0]:
                data["pos"][0] = self.box_top_left[0]
                self.winners.append(label)  # Add the human to the winners list
                del self.humans[label]  # Remove the human from the dictionary
                # print(f"{label} reached the finish line!")

    def move_hippo(self, delta_time: float) -> None:
        # Check if the hippo is currently eating
        if time.time() - self.hippo_stopping_eating < 8:
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

        # print(f"Hippo pos before move: {self.hippo['pos'][0]}")
        # print(f"Hippo pos after move: {self.hippo['pos'][0]}")

    def check_collisions(self) -> None:
        hippo_rect = pygame.Rect(self.hippo["pos"][0], self.hippo["pos"][1], self.human_size, self.human_size)
        humans_to_remove: List[str] = []

        for label, data in self.humans.items():
            label: str
            # Label is each item in the  self.bet list such as A1 or D2

            data: Dict[str, Union[List[int], int]]  # Using Union for compatibility with Python 3.9
            # example data{'pos': [379.94802474975586, 90], 'speed': 8}

            ball_rect = pygame.Rect(data["pos"][0], data["pos"][1], self.human_size, self.human_size)
            #  ball_rect : <rect(578, 90, 20, 20)>
            if hippo_rect.colliderect(ball_rect):
                humans_to_remove.append(label)
                self.hippo_stopping_eating = time.time()  # Set the time when the hippo starts eating

        for label in humans_to_remove:
            activate_talking = random.randint(1, 3)
            if activate_talking == 3:

                self.commentary = True
                self.comment_to_use = random.randint(1, 4)
            print("Your label is" + str(label))
            del self.humans[label]

            # i should build a counter for every human eating incrase counter by +1 for every even numbers, create the message.
            # i need to give exp for each human that  lives that the player bet on
            # need a final report after the race for the user as well as a prize award


    def display_hippos(self, state):
        # Local box dimensions for cropping
        crop_width = 350
        crop_height = 600
        crop_x = 20
        crop_y = 400

        # Local display dimensions for rendering the hippo
        hippo_width = 100
        hippo_height = 100

        crop_box = pygame.Rect(crop_x, crop_y, crop_width, crop_height)
        cropped_surface = self.sprite_sheet_hippo_facing_right.subsurface(crop_box)
        flipped_surface = pygame.transform.flip(cropped_surface, True, False)

        scaled_hippo = pygame.transform.scale(flipped_surface, (hippo_width, hippo_height))

        # if self.hippo:
        #     state.DISPLAY.blit(scaled_hippo, (self.hippo["pos"][0] - 10, self.hippo["pos"][1] - 10))
        #
        # if self.hippo2:
        #     state.DISPLAY.blit(scaled_hippo, (self.hippo2["pos"][0] - 10, self.hippo2["pos"][1] - 10))

        if self.hippo:
            x = round(self.hippo["pos"][0]) - 10
            y = round(self.hippo["pos"][1]) - 10
            state.DISPLAY.blit(scaled_hippo, (x, y))

        if self.hippo2:
            x2 = round(self.hippo2["pos"][0]) - 10
            y2 = round(self.hippo2["pos"][1]) - 10
            state.DISPLAY.blit(scaled_hippo, (x2, y2))

    def move_hippo2(self, delta_time: float) -> None:
        if time.time() - self.hippo2_stopping_eating < 8:
            return

        label, human_x, human_y = self.find_closest_human_for_hippo2()
        if label is None:
            return

        hippo2_x, hippo2_y = self.hippo2["pos"]

        if hippo2_x < human_x:
            self.hippo2["pos"][0] += 16 * delta_time
        elif hippo2_x > human_x:
            self.hippo2["pos"][0] -= 16 * delta_time

        if hippo2_y < human_y:
            self.hippo2["pos"][1] += 16 * delta_time
        elif hippo2_y > human_y:
            self.hippo2["pos"][1] -= 16 * delta_time

    def check_collisions_for_hippo2(self) -> None:
        hippo2_rect = pygame.Rect(self.hippo2["pos"][0], self.hippo2["pos"][1], self.human_size, self.human_size)
        for label, data in list(self.humans.items()):
            rect = pygame.Rect(data["pos"][0], data["pos"][1], self.human_size, self.human_size)
            if hippo2_rect.colliderect(rect):
                self.hippo2_stopping_eating = time.time()  # ← Only update on actual collision
                del self.humans[label]
                break

    def find_closest_human_for_hippo2(self) -> Tuple[Optional[str], Optional[int], Optional[int]]:
        if not self.hippo2 or not self.humans:
            return None, None, None

        hippo2_x, hippo2_y = self.hippo2["pos"]
        closest_label = None
        closest_distance = float('inf')

        for label, data in self.humans.items():
            human_x, human_y = data["pos"]
            distance = math.hypot(human_x - hippo2_x, human_y - hippo2_y)
            if distance < closest_distance:
                closest_distance = distance
                closest_label = label

        if closest_label:
            pos = self.humans[closest_label]["pos"]
            return closest_label, pos[0], pos[1]
        return None, None, None


