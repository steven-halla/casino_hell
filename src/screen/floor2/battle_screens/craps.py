from typing import Optional
import pygame

from entity.gui.screen.battle_screen import BattleScreen
from entity.gui.textbox.text_box import TextBox
from globalclasses.money_balancer import MoneyBalancer
from screen.examples.screen import Screen
from screen.floor2.map_screens.area_2_start_screen import Area2StartScreen

# maybe we can have craps be more about saving people? that would be a fun mission
# poison dice  is -1 to all dice rolls , this makes it less likely to get a 7 on come out
class Craps(BattleScreen):
    def __init__(self, screenName: str = "Casino Slots Screen") -> None:
        super().__init__(screenName)
        self.game_state: str = "welcome_screen"
        self.battle_messages: dict[str, TextBox] = {
            "welcome_message": TextBox(
                ["Time to take a crap with some craps"],
                (65, 460, 700, 130),
                36,
                500
            ),

            "bet_message": TextBox(
                ["Time to take a crap with some craps"],
                (65, 460, 700, 130),
                36,
                500
            ),

            "magic_message": TextBox(
                ["Time to take a crap with some craps"],
                (65, 460, 700, 130),
                36,
                500
            ),

            "game_over_no_stamina_message": TextBox(
                ["Hero: Crap I can't...keep...going...(You ran out of stamina)", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

            "game_over_no_money_message": TextBox(
                ["You ran out of money, game over, enjoy eternity in chicken nugget  hell", ""],
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
        self.magic_screen_choices: list[str] = ["Magnet", "Back"]
        self.welcome_screen_index: int = 0
        self.magic_screen_index: int = 0
        self.magic_magnet = 0
        self.bet = 50

        self.money_balancer = MoneyBalancer(self.money)

        self.game_over_message = []  # Initialize game_over_message

        self.lucky_seven = 0
        self.magic_lock = False


    def update(self, state: "GameState") -> None:
        self.lucky_seven = state.player.luck * 2
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
                # state.player.stamina_points -= 4
                # state.player.money -= self.bet
                # self.money += self.bet
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
                self.battle_messages["magic_message"].messages = [f"Add an extra dice to your rolls"]
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

        if self.game_state == "welcome_screen":
            self.battle_messages["welcome_message"].draw(state)

            if self.money < 1:
                self.battle_messages["you_win"].draw(state)

            if state.player.stamina_points < 1:
                self.battle_messages["game_over_no_stamina_message"].draw(state)

            elif state.player.money <= 0:
                self.battle_messages["game_over_no_money_message"].draw(state)


            elif state.player.stamina_points <= 10 and state.player.stamina_points > 0:
                self.battle_messages["game_over_low_stamina_message"].draw(state)



            elif state.player.money < 50 and state.player.money > 0:
                self.battle_messages["game_over_low_money_message"].draw(state)


            black_box_height = 221 - 50  # Adjust height
            black_box_width = 200 - 10  # Adjust width to match the left box
            border_width = 5
            start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
            start_y_right_box = 240  # Adjust vertical alignment

            # Create the black box
            black_box = pygame.Surface((black_box_width, black_box_height))
            black_box.fill((0, 0, 0))

            # Create a white border
            white_border = pygame.Surface(
                (black_box_width + 2 * border_width, black_box_height + 2 * border_width)
            )
            white_border.fill((255, 255, 255))
            white_border.blit(black_box, (border_width, border_width))

            # Determine the position of the white-bordered box
            black_box_x = start_x_right_box - border_width
            black_box_y = start_y_right_box - border_width

            # Blit the white-bordered box onto the display
            state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

            # Draw the menu options
            for idx, choice in enumerate(self.welcome_screen_choices):
                y_position = start_y_right_box + idx * 40  # Adjust spacing between choices
                state.DISPLAY.blit(
                    self.font.render(choice, True, (255, 255, 255)),
                    (start_x_right_box + 60, y_position + 15)
                )
            if "Magnet" not in state.player.magicinventory:
                self.magic_lock = True
                self.welcome_screen_choices[1] = "Locked"


            if self.welcome_screen_index == 0:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 12)
                )
            elif self.welcome_screen_index == 1:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 52)
                )
            elif self.welcome_screen_index == 2:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 92)
                )
            elif self.welcome_screen_index == 3:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 132)
                )

        elif self.game_state == "magic_screen":
            self.battle_messages["magic_message"].draw(state)

            black_box_height = 221 - 50  # Adjust height
            black_box_width = 200 - 10  # Adjust width to match the left box
            border_width = 5
            start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
            start_y_right_box = 240  # Adjust vertical alignment

            # Create the black box
            black_box = pygame.Surface((black_box_width, black_box_height))
            black_box.fill((0, 0, 0))

            # Create a white border
            white_border = pygame.Surface(
                (black_box_width + 2 * border_width, black_box_height + 2 * border_width)
            )
            white_border.fill((255, 255, 255))
            white_border.blit(black_box, (border_width, border_width))

            # Determine the position of the white-bordered box
            black_box_x = start_x_right_box - border_width
            black_box_y = start_y_right_box - border_width

            # Blit the white-bordered box onto the display
            state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

            # Draw the menu options
            for idx, choice in enumerate(self.magic_screen_choices):
                y_position = start_y_right_box + idx * 40  # Adjust spacing between choices
                state.DISPLAY.blit(
                    self.font.render(choice, True, (255, 255, 255)),
                    (start_x_right_box + 60, y_position + 15)
                )

            if self.magic_screen_index == 0:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 12)
                )
            elif self.magic_screen_index == 1:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 52)
                )

        elif self.game_state == "bet_screen":
            self.battle_messages["bet_message"].draw(state)

        pygame.display.flip()





