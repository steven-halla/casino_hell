from typing import Optional
import pygame

from entity.gui.screen.battle_screen import BattleScreen
from entity.gui.textbox.text_box import TextBox
from globalclasses.money_balancer import MoneyBalancer
from screen.examples.screen import Screen
from screen.floor2.map_screens.area_2_start_screen import Area2StartScreen


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

            "game_over_no_stamina_message": TextBox(
                ["Hero: Crap I can't...keep...going...(You ran out of stamina", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

            "game_over_no_money_message": TextBox(
                ["You ran out of money game over, enjoy eternity in rib demon hell", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

            "game_over_low_stamina_message": TextBox(
                ["Hero: I'm too tired to keep gambling i need to rest)", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

            "game_over_low_money_message": TextBox(
                ["I don't have enough money to keep playing time to leave", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

            "you_win": TextBox(
                ["Rib Demon: well looks like I lost...", ""],
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

        if self.game_state == "welcome_screen":


            self.battle_messages["welcome_message"].update(state)

            if self.money < 1:
                self.battle_messages["you_win"].update(state)
                if self.battle_messages["you_win"].message_index == 1:
                    state.currentScreen = Area2StartScreen()

            if state.player.stamina_points < 1:
                self.battle_messages["game_over_no_stamina_message"].update(state)
                if self.battle_messages["game_over_no_stamina_message"].message_index == 1:
                    state.currentScreen = Area2StartScreen()

            elif state.player.stamina_points <= 10 and state.player.stamina_points > 0:
                self.battle_messages["game_over_low_stamina_message"].update(state)
                if self.battle_messages["game_over_low_stamina_message"].message_index == 1:
                    state.currentScreen = Area2StartScreen()


            elif state.player.money < 50 and state.player.money > 0:
                self.battle_messages["game_over_low_money_message"].update(state)
                if self.battle_messages["game_over_low_money_message"].message_index == 1:
                    state.currentScreen = Area2StartScreen()

            elif state.player.money <= 0:
                self.battle_messages["game_over_no_money_message"].update(state)
                if self.battle_messages["game_over_no_money_message"].message_index == 1:
                    state.currentScreen = Area2StartScreen()

            if controller.isUpPressed:
                self.welcome_screen_index = (self.welcome_screen_index - 1) % len(self.welcome_screen_choices)
                controller.isUpPressed = False
            elif controller.isDownPressed:
                self.welcome_screen_index = (self.welcome_screen_index + 1) % len(self.welcome_screen_choices)
                controller.isDownPressed = False

            if self.welcome_screen_index == 0 and controller.isTPressed:
                self.game_state = "spin_screen"
                state.player.stamina_points -= 4
                state.player.money -= self.bet
                self.money += self.bet
                controller.isTPressed = False
            elif self.welcome_screen_index == 1 and controller.isTPressed and self.magic_lock == False:
                self.magic_screen_index = 0
                self.battle_messages["magic_message"].reset()
                self.game_state = "magic_screen"
                controller.isTPressed = False
            elif self.welcome_screen_index == 2 and controller.isTPressed and "Lucky Shoes" not in state.player.items:
                self.battle_messages["bet_message"].reset()
                self.game_state = "bet_screen"
                controller.isTPressed = False
            elif self.welcome_screen_index == 3 and controller.isTPressed and self.lock_down == 0:
                state.currentScreen = state.area2StartScreen
                controller.isTPressed = False

        elif self.game_state == "magic_screen":
            if self.magic_screen_index == 0:
                self.battle_messages["magic_message"].messages = [f""]
            elif self.magic_screen_index == 1:
                self.battle_messages["magic_message"].messages = [f"Go back to main menu."]
            self.battle_messages["magic_message"].update(state)
            if controller.isUpPressed:
                self.magic_screen_index = (self.magic_screen_index - 1) % len(self.magic_screen_choices)
                controller.isUpPressed = False
            elif controller.isDownPressed:
                self.magic_screen_index = (self.magic_screen_index + 1) % len(self.magic_screen_choices)
                controller.isDownPressed = False
            if self.magic_screen_index == 0 and controller.isTPressed:
                controller.isTPressed = False
            elif self.magic_screen_index == 1 and controller.isTPressed:
                self.battle_messages["magic_message"].update(state)
                self.game_state = "welcome_screen"
                controller.isTPressed = False













    def draw(self, state: "GameState") -> None:
        state.DISPLAY.fill((0, 0, 51))
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)

        self.draw_bottom_black_box(state)
        pygame.display.flip()





