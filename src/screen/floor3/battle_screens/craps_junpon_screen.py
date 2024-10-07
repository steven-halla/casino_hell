import pygame
import random

from constants import WHITE, RED
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from entity.gui.textbox.text_box import TextBox
from game_constants.events import Events
from game_constants.magic import Magic


class CrapsJunponScreen(GambleScreen):

    def __init__(self, screenName: str = "Craps") -> None:
        super().__init__(screenName)
        self.game_state: str = self.WELCOME_SCREEN
        self.sprite_sheet: pygame.Surface = pygame.image.load("./assets/images/dice45.png")
        self.come_out_roll_total: int = 0
        self.dealer_name = "Junpon"

        self.dice_roll_1: int = 0
        self.dice_roll_2: int = 0
        self.dice_roll_2: int = 0
        self.power_meter_index: int = 0
        self.point_roll_total: int = 0
        self.point_roll_choices: list[str] = ["Play", "Bet"]
        self.magic_screen_choices: list[str] = [Magic.CRAPS_LUCKY_7.value, "Back"]
        self.bet_screen_choices: list[str] = ["Back"]
        self.welcome_screen_index: int = 0
        self.magic_screen_index: int = 0
        self.point_roll_index: int = 0
        self.bet: int = 100
        self.bet_minimum: int = 100
        pygame.mixer.music.stop()
        self.lucky_seven_buff_counter: int = 0
        self.magic_lock: bool = False
        self.lucky_seven_buff_not_active = 0
        self.junpon_bankrupt = 0
        self.player_stamina_low_cost = 5
        self.magic_screen_menu_lucky_seven_index = 0
        self.magic_screen_menu_back_index = 1
        self.lock_down_inactive = 0

        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "This is the first message"
            ]),
            self.BET_MESSAGE: MessageBox([
                "Max bet of 75 during Come out Roll. Point Roll Max is 200"
            ]),
            self.MAGIC_MENU_TRIPLE_DICE_DESCRIPTION: MessageBox([
                "description for magic meter"
            ]),
        }
    POWER_METER_SCREEN = "power_meter_screen"
    MAGIC_MENU_TRIPLE_DICE_DESCRIPTION = "magic_menu_triple_dice_description"
    TRIPLE_DICE = "Triple Dice"

    def start(self, state: 'GameState'):
        pass

    def reset_craps_game(self, state: 'GameState'):
        self.welcome_screen_quit_index = self.welcome_screen_play_index
        self.lucky_seven_buff_counter = self.lucky_seven_buff_not_active
        self.magic_lock = False
        self.bet = self.bet_minimum
        state.player.canMove = True

    def update(self, state: 'GameState'):
        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)

        if self.money <= self.junpon_bankrupt:
            Events.add_event_to_player(state.player, Events.CRAPS_JUNPON_DEFEATED)

        try:
            if self.lucky_seven_buff_counter > self.lucky_seven_buff_not_active:
                self.magic_lock = True
            elif self.lucky_seven_buff_counter == self.lucky_seven_buff_not_active:
                self.magic_lock = False
        except AttributeError:
            print("AttributeError: lucky_seven_buff_counter does not exist")
            self.magic_lock = False
        except TypeError:
            print("TypeError: lucky_seven_buff_counter is not of the expected type")
            self.magic_lock = False

        if self.game_state == self.WELCOME_SCREEN:
            self.battle_messages[self.WELCOME_MESSAGE].update(state)
            if state.controller.isTPressed:
                state.controller.isTPressed = False
                if self.welcome_screen_index == self.welcome_screen_play_index:
                    self.game_state = self.POWER_METER_SCREEN
                    state.player.stamina_points -= self.player_stamina_low_cost

                elif self.welcome_screen_index == self.welcome_screen_magic_index and self.magic_lock == False \
                        and Magic.CRAPS_LUCKY_7.value in state.player.magicinventory:
                    self.magic_screen_index = self.magic_screen_menu_lucky_seven_index
                    self.battle_messages[self.MAGIC_MENU_TRIPLE_DICE_DESCRIPTION].reset()
                    self.game_state = self.MAGIC_MENU_SCREEN

                elif self.welcome_screen_index == self.welcome_screen_bet_index:
                    self.game_state = self.BET_MENU_SCREEN

                elif self.welcome_screen_index == self.welcome_screen_quit_index and self.lock_down == self.lock_down_inactive:
                    self.reset_craps_game(state)
                    # state.current_player = state.area3GamblingScreen
                    # state.area3GamblingScreen.start(state)





    def draw_box_info(self, state: 'GameState'):
        arrow_x_coordinate_padding = 12
        arrow_y_coordinate_padding_play = 12
        arrow_y_coordinate_padding_magic = 52
        arrow_y_coordinate_padding_bet = 92
        arrow_y_coordinate_padding_quit = 132
        player_enemy_box_info_x_position = 37
        enemy_name_y_position = 33
        enemy_money_y_position = 70
        enemy_status_y_position = 110
        bet_y_position = 370
        player_money_y_position = 250
        hero_name_y_position = 205
        hero_stamina_y_position = 290
        hero_focus_y_position = 330
        box_width_offset = 10
        horizontal_padding = 25
        vertical_position = 240
        spacing_between_choices = 40
        text_x_offset = 60
        text_y_offset = 15
        black_box_width = 200 - box_width_offset
        start_x_right_box = state.DISPLAY.get_width() - black_box_width - horizontal_padding
        start_y_right_box = vertical_position

        state.DISPLAY.blit(self.font.render(self.dealer_name, True, WHITE), (player_enemy_box_info_x_position, enemy_name_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER} {self.money}", True, WHITE), (player_enemy_box_info_x_position, enemy_money_y_position))
        if self.lucky_seven_buff_counter == self.lucky_seven_buff_not_active:
            state.DISPLAY.blit(self.font.render(f"{self.STATUS_GREEN}", True, WHITE), (player_enemy_box_info_x_position, enemy_status_y_position))
        elif self.lucky_seven_buff_counter > self.lucky_seven_buff_not_active:
            state.DISPLAY.blit(self.font.render(f"{self.TRIPLE_DICE}: {self.lucky_seven_buff_counter} ", True, WHITE), (player_enemy_box_info_x_position, enemy_status_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.BET_HEADER}: {self.bet}", True, WHITE), (player_enemy_box_info_x_position, bet_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER}: {state.player.money}", True, WHITE), (player_enemy_box_info_x_position, player_money_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.HP_HEADER}: {state.player.stamina_points}", True, WHITE), (player_enemy_box_info_x_position, hero_stamina_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MP_HEADER}: {state.player.focus_points}", True, WHITE), (player_enemy_box_info_x_position, hero_focus_y_position))

        if self.lock_down <= self.lock_down_inactive:
            state.DISPLAY.blit(self.font.render(f"{self.HERO_HEADER}", True, WHITE), (player_enemy_box_info_x_position, hero_name_y_position))
        elif self.lock_down > self.lock_down_inactive:
            state.DISPLAY.blit(self.font.render(f"{self.LOCKED_DOWN_HEADER}:{self.lock_down}", True, RED), (player_enemy_box_info_x_position, hero_name_y_position))

        for idx, choice in enumerate(self.welcome_screen_choices):
            y_position = start_y_right_box + idx * spacing_between_choices  # Adjust spacing between choices
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )

        if Magic.CRAPS_LUCKY_7.value not in state.player.magicinventory:
            self.magic_lock = True
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        elif Magic.CRAPS_LUCKY_7.value in state.player.magicinventory:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

        if self.magic_lock == True:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        elif self.magic_lock == False:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

        if self.welcome_screen_index == self.welcome_screen_play_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_play)
            )
        elif self.welcome_screen_index == self.welcome_screen_magic_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_magic)
            )
        elif self.welcome_screen_index == self.welcome_screen_bet_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_bet)
            )
        elif self.welcome_screen_index == self.welcome_screen_quit_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_quit)
            )

    def draw(self, state: 'GameState'):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)
        self.draw_menu_selection_box(state)
        self.draw_box_info(state)

        pygame.display.flip()












#Charge: hold A button and rock d pad left and right
# Release right after last d pad button press
# this is for point roll
# the longer you wait the more of a bonus you get
# this is to get rid of times that you can roll 12 rolls
# this move requires stamina to use