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







    def start(self, state: "GameState") -> None:
        super().start(state)

    def update(self, state: "GameState"):
        controller = state.controller
        controller.update()

        if state.controller.isUpPressed:
            state.controller.isUpPressed = False

            self.arrow_index = (self.arrow_index - 1) % len(self.choices)
            print("Up pressed, arrow_index:", self.arrow_index)  # Debugging line

        elif state.controller.isDownPressed:
            state.controller.isDownPressed = False
            self.arrow_index = (self.arrow_index + 1) % len(self.choices)
            print("Down pressed, arrow_index:", self.arrow_index)

        selected_option = self.choices[self.arrow_index]

        if selected_option == "Yes" and state.controller.isTPressed:
            state.controller.isTPressed = False
            state.currentScreen = state.startScreen
            state.startScreen.start(state)
            print("start game")
        elif selected_option == "No" and state.controller.isTPressed:
            state.controller.isTPressed = False
            state.player.load_game(state)
            print("Load")




    def draw(self, state):
        state.DISPLAY.fill(BLUEBLACK)




        bet_box_width = 150
        bet_box_height = 100
        border_width = 5

        screen_width, screen_height = state.DISPLAY.get_size()
        bet_box_x = screen_width - bet_box_width - border_width - 30
        bet_box_y = screen_height - 130 - bet_box_height - border_width - 60

        bet_box = pygame.Surface((bet_box_width, bet_box_height))
        bet_box.fill((0, 0, 0))
        white_border = pygame.Surface((bet_box_width + 2 * border_width, bet_box_height + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(bet_box, (border_width, border_width))

        # Calculate text positions
        text_x = bet_box_x + 40 + border_width
        text_y_start_game = bet_box_y + 20
        text_y_load = text_y_start_game + 40

        # Draw the box on the screen
        state.DISPLAY.blit(white_border, (bet_box_x, bet_box_y))

        # Draw the text on the screen (over the box)
        state.DISPLAY.blit(self.font.render("Start New Game", True, (255, 255, 255)), (text_x, text_y_start_game))
        state.DISPLAY.blit(self.font.render("Load", True, (255, 255, 255)), (text_x, text_y_load))

        arrow_x = text_x - 40  # Adjust the position of the arrow based on your preference
        arrow_y = text_y_start_game + self.arrow_index * 40  # Adjust based on the item's height

        # Draw the arrow using pygame's drawing functions (e.g., pygame.draw.polygon)
        # Here's a simple example using a triangle:
        pygame.draw.polygon(state.DISPLAY, (255, 255, 255),
                            [(arrow_x, arrow_y), (arrow_x - 10, arrow_y + 10), (arrow_x + 10, arrow_y + 10)])


        pygame.display.update()
