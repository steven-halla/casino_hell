from typing import Optional
import pygame

from entity.gui.screen.battle_screen import BattleScreen
from entity.gui.textbox.text_box import TextBox
from globalclasses.money_balancer import MoneyBalancer
from screen.examples.screen import Screen

class Craps(BattleScreen):
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
        self.welcome_screen_choices: list[str] = ["Play", "Magic", "Bet", "Quit"]
        self.magic_screen_choices: list[str] = ["Hack", "Back"]
        self.welcome_screen_index: int = 0
        self.magic_screen_index: int = 0

        self.money_balancer = MoneyBalancer(self.money)

        self.game_over_message = []  # Initialize game_over_message


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
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)

        self.draw_bottom_black_box(state)
        pygame.display.flip()





