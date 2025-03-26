import pygame
import random
from constants import WHITE, RED, DISPLAY, BLACK
from deck import Deck
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic
from game_state import GameState


class HighLowScreenDienaScreen(GambleScreen):
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
        self.diena_bankrupt: int = 0


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
    DRAW_CARD_SCREEN = "draw_card_screen"
    PLAYER_DRAWS_ACE_SCREEN = "player_draws_ace_screen"
    ENEMY_DRAWS_ACE_SCREEN = "enemy_draws_ace_screen"
    PLAYER_WINS_SCREEN = "player_wins_screen"
    ENEMY_WINS_SCREEN = "enemy_wins_screen"
    PLAYER_SPREAD_SCREEN = "player_spread_screen"

    def start(self, state: 'GameState'):
        self.deck.shuffle()
        self.build_custom_26_card_deck()

    def build_custom_26_card_deck(self):
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


    def round_reset_high_low(self):
        self.deck.shuffle()
        self.build_custom_26_card_deck()
        self.player_score = 0
        self.enemy_score = 0
        self.player_hand: str = ""
        self.enemy_hand: str = ""

    def reset_high_low_game(self):
        self.deck.shuffle()
        self.build_custom_26_card_deck()
        self.player_score = 0
        self.enemy_score = 0
        self.player_hand: str = ""
        self.enemy_hand: str = ""

    def update(self, state: 'GameState'):
        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)

        if self.money <= self.diena_bankrupt:
            state.currentScreen = state.area3RestScreen
            state.area3RestScreen.start(state)
            Events.add_level_three_event_to_player(state.player, Events.HIGH_LOW_DIENA_DEFEATED)



        if self.game_state == self.WELCOME_SCREEN:
            pass

        elif self.game_state == self.BET_SCREEN:
            pass

        elif self.game_state == self.MAGIC_MENU_SCREEN:
            pass

        elif self.game_state == self.DRAW_CARD_SCREEN:
            pass

        elif self.game_state == self.PLAYER_DRAWS_ACE_SCREEN:
            pass

        elif self.game_state == self.ENEMY_DRAWS_ACE_SCREEN:
            pass

        elif self.game_state == self.PLAYER_SPREAD_SCREEN:
            pass


        elif self.game_state == self.PLAYER_WINS_SCREEN:
            pass

        elif self.game_state == self.ENEMY_WINS_SCREEN:
            pass


        elif self.game_state == self.GAME_OVER_SCREEN:

            no_money_game_over = 0

            no_stamina_game_over = 0

            if state.player.money <= no_money_game_over:

                if controller.isTPressed or state.controller.isAPressedSwitch:
                    controller.isTPressed = False

                    controller.isAPressedSwitch = False

                    state.currentScreen = state.gameOverScreen

                    state.gameOverScreen.start(state)

            elif state.player.stamina_points <= no_stamina_game_over:

                if controller.isTPressed or state.controller.isAPressedSwitch:
                    controller.isTPressed = False

                    controller.isAPressedSwitch = False

                    state.player.money -= 100

                    self.reset_high_low_game()

                    state.currentScreen = state.area3RestScreen

                    state.area3RestScreen.start(state)

    def draw(self, state: GameState):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)

        if self.game_state == self.WELCOME_SCREEN:
            pass

        elif self.game_state == self.BET_SCREEN:
            pass

        elif self.game_state == self.MAGIC_MENU_SCREEN:
            pass

        elif self.game_state == self.DRAW_CARD_SCREEN:
            pass

        elif self.game_state == self.PLAYER_DRAWS_ACE_SCREEN:
            pass

        elif self.game_state == self.ENEMY_DRAWS_ACE_SCREEN:
            pass

        elif self.game_state == self.PLAYER_SPREAD_SCREEN:
            pass

        elif self.game_state == self.PLAYER_WINS_SCREEN:
            pass

        elif self.game_state == self.ENEMY_WINS_SCREEN:
            pass


        elif self.game_state == self.GAME_OVER_SCREEN:
            pass









        

