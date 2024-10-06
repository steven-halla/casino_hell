import pygame
import random

from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from entity.gui.textbox.text_box import TextBox
from game_constants.magic import Magic
from game_state import GameState


class CrapsJunponScreen(GambleScreen):

    def __init__(self, screenName: str = "Craps") -> None:
        super().__init__(screenName)
        self.game_state: str = self.WELCOME_SCREEN
        self.sprite_sheet: pygame.Surface = pygame.image.load("./assets/images/dice45.png")
        self.come_out_roll_total: int = 0

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
        self.welcome_screen_choices: list[str] = ["Play", "Magic", "Bet", "Quit"]
        pygame.mixer.music.stop()
        self.lucky_seven_buff_counter: int = 0
        self.magic_lock: bool = False
        self.lucky_seven_buff_not_active = 0




        self.battle_messages: dict[str, MessageBox] = {
            "welcome_message": MessageBox([
                "This is the first message"
            ]),

            "bet_message": MessageBox(
                ["Max bet of 75 during Come out Roll. Point Roll Max is 200"]),
        }


    def start(self, state: 'GameState'):
        pass

    def update(self, state: 'GameState'):
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







#Charge: hold A button and rock d pad left and right
# Release right after last d pad button press
# this is for point roll
# the longer you wait the more of a bonus you get
# this is to get rid of times that you can roll 12 rolls
# this move requires stamina to use