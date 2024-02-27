import pygame
import pytmx
import time  # Import the time module

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.gui.textbox.npc_text_box import NpcTextBox
from entity.npc.battle_screen.Guy import Guy

from entity.npc.chilli_screen.sir_leopold_the_hedgehog import SirLeopoldTheHedgeHog

from entity.npc.rest_screen.bar_keep import BarKeep

from entity.npc.rest_screen.quest_giver_janet import QuestGiverJanet

from entity.npc.start_screen.cindy_long_hair import CindyLongHair
from entity.player.player import Player
from screen.examples.screen import Screen
from physics.rectangle import Rectangle

class StartLoadScreen(Screen):

    def __init__(self):
        super().__init__("StartLoadScreen")
        self.font = pygame.font.Font(None, 36)
        self.arrow_index = 0  # Initialize the arrow index to the first item (e.g., "Yes")
        self.choices = ["Yes", "No"]
        self.spell_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/startloadaccept.wav")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.timer_start_time = None  # New attribute for timer start time

        self.music_file = "/Users/stevenhalla/code/casino_hell/assets/music/startscreen4.mp3"
        self.music_volume = 0.5  # Adjust as needed
        # self.initialize_music()
        self.title_colors = [(0, 0, 51),(120, 0, 0), (160, 0, 0), (200, 0, 0), (255, 0, 0)]  # Deeper shades of red

        # self.title_colors = [(255, 100, 100), (255, 50, 50), (200, 0, 0)]  # Different shades of red
        self.current_color_index = 0  # Start with the first color
        self.color_change_interval = 2000  # 2 seconds in milliseconds
        self.last_color_change_time = pygame.time.get_ticks()  # Record the start time
        self.title_font = pygame.font.SysFont('Times New Roman', 100, bold=True, italic=True)
        self.last_color = False

        self.menu_movement_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)
        self.t_key_pressed = False  # Add this line


    def start_timer(self, duration_ms):
        """Start the timer with a specified delay in milliseconds."""
        self.timer_start_time = pygame.time.get_ticks() + duration_ms

    def timer_finished(self):
        """Check if the timer has finished."""
        if self.timer_start_time is None:
            return False  # Timer was not started
        if pygame.time.get_ticks() >= self.timer_start_time:
            self.timer_start_time = None  # Reset timer for future use
            return True
        return False

    def stop_music(self):
        pygame.mixer.music.stop()

    def initialize_music(self):
        # Initialize the mixer
        pygame.mixer.init()

        # Load the music file
        pygame.mixer.music.load(self.music_file)

        # Set the volume for the music (0.0 to 1.0)
        pygame.mixer.music.set_volume(self.music_volume)

        # Play the music, -1 means the music will loop indefinitely
        pygame.mixer.music.play(-1)

    def start(self, state: "GameState") -> None:
        super().start(state)
        self.stop_music()
        self.initialize_music()

    def update(self, state: "GameState"):
        controller = state.controller
        controller.update()

        # if state.controller.isTPressed:
            # Set the current color index to the last index in the title_colors array
            # self.current_color_index = len(self.title_colors) - 1
            # # Indicate that the last color has been reached
            # self.last_color = True
            # Reset the T pressed state
            # state.controller.isTPressed = False

        # Check if it's time to change the title color
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_color_change_time) >= self.color_change_interval:
            # Check if the current index is less than the last index in the array
            if self.current_color_index < len(self.title_colors) - 1:
                # Only update the color index if we haven't reached the last color
                self.current_color_index += 1
            else:
                # We've reached the last color, so set last_color to True
                self.last_color = True
            # Reset the timer
            self.last_color_change_time = current_time

        # Additional update logic...

        if state.controller.isUpPressed and self.t_key_pressed == False:
            state.controller.isUpPressed = False
            self.menu_movement_sound.play()  # Play the sound effect once


            self.arrow_index = (self.arrow_index - 1) % len(self.choices)
            print("Up pressed, arrow_index:", self.arrow_index)  # Debugging line

        elif state.controller.isDownPressed and self.t_key_pressed == False:
            state.controller.isDownPressed = False
            self.menu_movement_sound.play()  # Play the sound effect once

            self.arrow_index = (self.arrow_index + 1) % len(self.choices)
            print("Down pressed, arrow_index:", self.arrow_index)

        selected_option = self.choices[self.arrow_index]

        if selected_option == "Yes" and state.controller.isTPressed:
            self.t_key_pressed = True  # Add this line

            pygame.mixer.music.stop()
            state.controller.isTPressed = False
            if self.timer_start_time is None:
                self.start_timer(1200)  # Start a 1.2-second delay
                self.spell_sound.play()  # Play the sound effect

        elif selected_option == "No" and state.controller.isTPressed:
            self.t_key_pressed = True  # Add this line

            pygame.mixer.music.stop()

            state.controller.isTPressed = False
            if self.timer_start_time is None:
                self.start_timer(2000)  # Start a 2-second delay
                self.spell_sound.play()  # Play the sound effect

        # Outside your conditional blocks for handling "Yes" or "No" selection
        # Ensure this check happens every update cycle, not just when a key is pressed
        if self.timer_start_time is not None and self.timer_finished():
            # Now that the timer has finished, check which option was selected and proceed
            if selected_option == "Yes":
                # Actions to take if "Yes" was selected and the timer has elapsed
                state.start_new_game_entry_point = True
                state.currentScreen = state.startScreen
                state.startScreen.start(state)
                print("Transitioning to start screen after delay")
            elif selected_option == "No":
                # Actions to take if "No" was selected and the timer has elapsed
                state.player.load_game(state)
                print("Loading game after delay")

    # this is the best implementation of a box

    def draw(self, state):
        state.DISPLAY.fill(BLUEBLACK)

        title_font = pygame.font.Font(None, 100)  # Use None for default font

        # Get the current color based on the index
        # Get the current color based on the index
        current_color = self.title_colors[self.current_color_index]

        # Render the title text with the current color
        title_text = self.title_font.render("Hell Casino", True, current_color)

        # Calculate the X and Y positions to center the title and set a top margin
        screen_width, screen_height = state.DISPLAY.get_size()
        title_x = (screen_width - title_text.get_width()) // 2 + 10
        title_y = 160  # 40 pixels from the top

        # Draw the title text on the screen
        state.DISPLAY.blit(title_text, (title_x, title_y))

        if self.current_color_index == len(self.title_colors) - 1:

            bet_box_width = 180
            bet_box_height = 100
            border_width = 5

            screen_width, screen_height = state.DISPLAY.get_size()
            bet_box_x = screen_width - bet_box_width - border_width - 30 - 295  # Shift left by 300
            bet_box_y = screen_height - 130 - bet_box_height - border_width + 15

            bet_box = pygame.Surface((bet_box_width, bet_box_height))
            bet_box.fill((0, 0, 0))
            white_border = pygame.Surface((bet_box_width + 2 * border_width, bet_box_height + 2 * border_width))
            white_border.fill((255, 255, 255))
            white_border.blit(bet_box, (border_width, border_width))

            # Calculate text positions relative to the bet_box_x
            text_x = bet_box_x + 40 + border_width  # Position based on bet_box_x
            text_y_start_game = bet_box_y + 20
            text_y_load = text_y_start_game + 40

            # Draw the box on the screen
            state.DISPLAY.blit(white_border, (bet_box_x, bet_box_y))

            # Draw the text on the screen (over the box)
            state.DISPLAY.blit(self.font.render("New Game", True, (255, 255, 255)), (text_x, text_y_start_game))
            state.DISPLAY.blit(self.font.render("Load", True, (255, 255, 255)), (text_x, text_y_load))

            arrow_x = text_x - 25  # Adjust the position of the arrow based on your preference
            arrow_y = text_y_start_game + self.arrow_index * 40  # Adjust based on the item's height

            # Draw the arrow using pygame's drawing functions (e.g., pygame.draw.polygon)
            # Here's a simple example using a triangle:
            pygame.draw.polygon(state.DISPLAY, (255, 255, 255),
                                [(arrow_x, arrow_y), (arrow_x - 10, arrow_y + 10), (arrow_x + 10, arrow_y + 10)])

        pygame.display.update()

