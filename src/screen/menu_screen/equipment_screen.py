import random

import pygame

from entity.gui.textbox.text_box import TextBox
from game_constants.coin_flip_constants import CoinFlipConstants
from game_constants.events import Events
from game_constants.magic import Magic
from screen.examples.screen import Screen

# need more testing for self.quest_money

class EquipmentScreen(Screen):
    def __init__(self):
        super().__init__("Casino Coin flip  Screen")




        self.equipment_index = 0
        self.equipment_state = False














        self.equipment_messages = {
            "welcome_message": TextBox(
                ["Press T to select options and go through T messages"],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            # You can add more game state keys and TextBox instances here
        }



    def update(self, state: "GameState"):

        if state.controller.isBPressed:
            state.player.draw_player_stats(state)
            print("j;dslfksfsa")



        controller = state.controller
        controller.update()

        state.player.update(state)






    ########################we want up and down arrows on bet. have arrow disapear when an item is not in use






    def draw(self, state: "GameState"):
        # Get the dimensions of the display
        screen_width = state.DISPLAY.get_width()
        screen_height = state.DISPLAY.get_height()

        # Fill the entire screen with black
        state.DISPLAY.fill((0, 0, 0))  # Black color

        # background


        pygame.display.flip()












