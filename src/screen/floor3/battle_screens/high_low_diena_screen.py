import pygame
import random
from constants import WHITE, RED, DISPLAY, BLACK
from deck import Deck
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic


class HighLowScreen(GambleScreen):
    def __init__(self, screenName: str = "high low") -> None:
        super().__init__(screenName)
        self.game_state: str = self.WELCOME_SCREEN
        self.enemy_cad_y_position :int = 0
        self.player_card_y_position: int = 0
        self.deck: Deck() = Deck()
        self.player_hand: str = ""
        self.enemy_hand: str = ""
        self.player_score: int = 0
        self.enemy_score: int = 0
        self.bet: int = 100
        self.money: int = 1000
        self.diena_bankrupt: int = 0
        self.magic_lock: bool = False
        self.dealer_name: str = "diena"
        self.magic_screen_choices: list[str] = []
        self.magic_menu_screen_index: int = 0
        self.welcome_menu_screen_index: int = 0
        self.low_exp: int = 10
        self.medium_exp: int = 25
        self.high_exp: int = 50


        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "This is the welcome screen"
            ]),

            self.BET_MESSAGE: MessageBox([
                "Min bet of 50, max of 200. Press up and down keys to increase/decrease bet. Press B to Exit."
            ]),


            self.MAGIC_MENU_BACK_DESCRIPTION: MessageBox([
                "go back to previous menu"
            ]),

            self.LEVEL_UP_SCREEN: MessageBox([
                f"You leveld up!"
            ]),
            self.LEVEL_UP_MESSAGE: MessageBox([
                f"You leveld up!"
            ]),

        }

    MAGIC_MENU_BACK_DESCRIPTION: str = "magic_menu_back_description"
    BET_MESSAGE: str = "bet_message"
    LEVEL_UP: str = "level_up_message"
    BACK = "back"
    LEVEL_UP_SCREEN = "level_up_screen"

    def start(self, state: 'GameState'):
        print("start")
        self.deck.shuffle()

    def build_custom_26_card_deck(self):
        print("build custom deck")
        # Start fresh
        self.deck.cards.clear()

        # Define allowed suits and ranks
        allowed_suits = ["Hearts", "Clubs"]
        allowed_ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]

        # Rebuild the deck with only the allowed suits and ranks
        self.deck.cards = [
            (self.deck.rank_strings[rank], suit, self.deck.rank_values[rank])
            for suit in allowed_suits
            for rank in allowed_ranks
        ]

        random.shuffle(self.deck.cards)
        print(f"Custom deck built with {len(self.deck.cards)} cards: Only Hearts and Clubs, 2–Ace.")



