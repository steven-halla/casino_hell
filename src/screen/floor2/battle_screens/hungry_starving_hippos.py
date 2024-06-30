from typing import Optional
import pygame
import random
from entity.gui.screen.battle_screen import BattleScreen
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
            "spin_message": TextBox(
                ["Press the A key to stop the spin."],
                (65, 460, 700, 130),
                36,
                500
            ),
            "magic_message": TextBox(
                ["Casts a spell"],
                (65, 460, 700, 130),
                36,
                500
            ),
            "bet_message": TextBox(
                ["Min Bet of 50, Max Bet of 250. Press UP button to add +50 to bet, Press DOWN button to decrease -50 from bet, Press B to go back to main menu."],
                (65, 460, 700, 130),
                36,
                500
            ),
            "results_message": TextBox(
                ["Your spinssss is {0} {1} {2}", ""],
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


        pygame.display.flip()







