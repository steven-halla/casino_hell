import pygame
import random
from constants import WHITE, RED, DISPLAY, BLACK
from deck import Deck
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic

# new spell
# if there is an ACE in the next 4 top cards, you win the ace
# stamina loss needs to be high for fucking up maybe higher spreads should have higher stamina loss

class HighLowDienaScreen(GambleScreen):
    def __init__(self, screenName: str = "high low") -> None:
        super().__init__(screenName)
        self.game_state: str = self.WELCOME_SCREEN
        self.enemy_cad_y_position: int = 0
        self.player_card_y_position: int = 0
        self.deck: Deck() = Deck()
        self.player_hand: list = []
        self.index_stepper: int = 1

        self.enemy_hand: list = []
        self.player_score: int = 0
        self.enemy_score: int = 0
        self.bet: int = 100
        self.money: int = 1000
        self.buff_red_card_only_in_deck_cost = 50
        self.cody_magic_points = 0

        self.diena_bankrupt: int = 0
        self.magic_lock: bool = False
        self.dealer_name: str = "diena"
        self.magic_menu_screen_index: int = 0
        self.low_exp: int = 10
        self.medium_exp: int = 25
        self.high_exp: int = 50
        self.magic_menu_selector: list[str] = [Magic.FLUSH_DECK.value, self.BACK]
        self.magic_screen_index: int = 0
        self.spread_counter: int = 1
        self.buff_red_card_only_in_deck: bool = False
        self.spirit_bonus: int = 0
        self.magic_bonus: int = 0
        self.deck_adder: int = 4

        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "Diena: This is the welcome screendffdasdfasfafafsafa"
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
            self.PLAYER_DRAWS_ACE_MESSAGE: MessageBox([
                f"You drw an ACE. You win "
            ]),

            self.ENEMY_DRAWS_ACE_MESSAGE: MessageBox([
                f"Enemy drw an ACE. You lose "
            ]),
            self.SPLIT_MESSAGE: MessageBox([
                f"Choose from a split from 1-3"
            ]),
            self.PLAYER_WIN_SPREAD_MESSAGE: MessageBox([
                f"You win the spread "
            ]),
            self.PLAYER_LOSE_SPREAD_MESSAGE: MessageBox([
                f"you lose the spread"
            ]),
            self.DRAW_CARD_MESSAGE: MessageBox([
                f"Here are your cards"
            ]),
            self.CODY_CASTING_SPELL_MESSAGE: MessageBox([
                f"4 pillars of society, rust and collapse , let your ownership be humanities downfall...countdown rot"
            ]),
        }

    MAGIC_MENU_BACK_DESCRIPTION: str = "magic_menu_back_description"
    BET_MESSAGE: str = "bet_message"
    LEVEL_UP: str = "level_up_message"
    BACK = "back"
    PLAYER_DRAWS_ACE_MESSAGE: str = "player draws ace message"
    ENEMY_DRAWS_ACE_MESSAGE: str = "enemy draws ace message"
    PLAYER_LOSE_SPREAD_MESSAGE: str = "player lose spread message"
    PLAYER_WIN_SPREAD_MESSAGE: str = "player win spread message"
    SPLIT_MESSAGE: str = "split message"
    DRAW_CARD_MESSAGE: str = "draw card message"
    LEVEL_UP_SCREEN = "level_up_screen"
    DRAW_CARD_SCREEN = "draw_card_screen"
    PLAYER_DRAWS_ACE_SCREEN = "player_draws_ace_screen"
    ENEMY_DRAWS_ACE_SCREEN = "enemy_draws_ace_screen"
    PLAYER_WINS_SCREEN = "player_wins_screen"
    ENEMY_WINS_SCREEN = "enemy_wins_screen"
    PLAYER_SPREAD_SCREEN = "player_spread_screen"
    CODY_CASTING_SPELL_MESSAGE = "cody_casting_message"
    CODY_CASTING_SPELL_SCREEN = "cody casting spell screen"

    def start(self, state: 'GameState'):
        self.deck.shuffle()
        self.build_custom_26_card_deck()
        self.spirit_bonus: int = state.player.spirit
        self.magic_bonus: int = state.player.mind

    def build_custom_26_card_deck(self):

        self.deck.cards.clear()

        # Define allowed suits and ranks
        if self.buff_red_card_only_in_deck == False:

            allowed_suits = ["Hearts", "Clubs"]
            allowed_ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]

            # Rebuild the deck with only the allowed suits and ranks
            self.deck.cards = [
                (self.deck.rank_strings[rank], suit, self.deck.rank_values_high_low[rank])
                for suit in allowed_suits
                for rank in allowed_ranks
            ]



            for suit in ["Spades", "Diamonds"]:
                self.deck.cards.append(
                    (self.deck.rank_strings[2], suit, self.deck.rank_values_high_low[2])
                )

            self.deck.cards.remove(
                ("Ace", "Hearts", self.deck.rank_values_high_low["Ace"])
            )





        # elif self.buff_red_card_only_in_deck == True:
        #     allowed_suits = ["Hearts"]
        #     allowed_ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
        #
        #     # Rebuild the deck with only the allowed suits and ranks
        #     self.deck.cards = [
        #         (self.deck.rank_strings[rank], suit, self.deck.rank_values_high_low[rank])
        #         for suit in allowed_suits
        #         for rank in allowed_ranks
        #     ]
        #
        #
        #
        #     for suit in ["Clubs", "Spades", "Diamonds"]:
        #         self.deck.cards.append(
        #             (self.deck.rank_strings[2], suit, self.deck.rank_values_high_low[2])
        #         )

        elif self.magic_bonus == 5 and self.buff_red_card_only_in_deck == True:
            allowed_suits = ["Hearts"]
            allowed_ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]

            # Rebuild the deck with only the allowed suits and ranks
            self.deck.cards = [
                (self.deck.rank_strings[rank], suit, self.deck.rank_values_high_low[rank])
                for suit in allowed_suits
                for rank in allowed_ranks
            ]

            for suit in ["Clubs", "Spades", "Diamonds"]:
                self.deck.cards.append(
                    (self.deck.rank_strings[2], suit, self.deck.rank_values_high_low[2])
                )

        elif self.magic_bonus >= 3 and self.buff_red_card_only_in_deck == True:
            # Separate allowed ranks for Hearts and Clubs
            hearts_ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]

            clubs_ranks = [10, "Jack", "Queen", "King", "Ace"]

            # Rebuild the deck with Hearts cards
            self.deck.cards = [
                (self.deck.rank_strings[rank], "Hearts", self.deck.rank_values_high_low[rank])
                for rank in hearts_ranks
            ]

            # Add Clubs cards
            self.deck.cards.extend([
                (self.deck.rank_strings[rank], "Clubs", self.deck.rank_values_high_low[rank])
                for rank in clubs_ranks
            ])

            # Add 2s for Spades and Diamonds
            for suit in ["Spades", "Diamonds"]:
                self.deck.cards.append(
                    (self.deck.rank_strings[2], suit, self.deck.rank_values_high_low[2])
                )

        elif self.magic_bonus < 3 and self.buff_red_card_only_in_deck == True:
            # self.magic_bonus < 3
            # Separate allowed ranks for Hearts and Clubs
            hearts_ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
            clubs_ranks = [6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]

            # Rebuild the deck with Hearts cards
            self.deck.cards = [
                (self.deck.rank_strings[rank], "Hearts", self.deck.rank_values_high_low[rank])
                for rank in hearts_ranks
            ]

            # Add Clubs cards
            self.deck.cards.extend([
                (self.deck.rank_strings[rank], "Clubs", self.deck.rank_values_high_low[rank])
                for rank in clubs_ranks
            ])

            # Add 2s for Spades and Diamonds
            for suit in ["Spades", "Diamonds"]:
                self.deck.cards.append(
                    (self.deck.rank_strings[2], suit, self.deck.rank_values_high_low[2])
                )

        random.shuffle(self.deck.cards)

    # this is for when we are still waiting on an ace
    def reset_spread_no_ace(self, state):

        self.player_score = 0
        self.enemy_score = 0
        self.player_hand: list = []
        self.enemy_hand: list = []




    # if an ace is gotten we do this
    def round_reset_high_low(self):
        self.deck.shuffle()
        self.build_custom_26_card_deck()
        self.player_score = 0
        self.enemy_score = 0
        self.player_hand: list = []
        self.enemy_hand: list = []



    # if an ace is gotten we do this
    def reset_high_low_game(self):
        self.deck.shuffle()
        self.build_custom_26_card_deck()
        self.player_score = 0
        self.enemy_score = 0
        self.player_hand: list = []
        self.enemy_hand: list = []

    def update(self, state: 'GameState'):
        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)



        if self.money <= self.diena_bankrupt:
            state.currentScreen = state.area3GamblingScreen
            state.area3GamblingScreen.start(state)
            Events.add_level_three_event_to_player(state.player, Events.HIGH_LOW_DIENA_DEFEATED)

        if self.game_state == self.WELCOME_SCREEN:
            self.update_welcome_screen_helper(state, controller)
            self.battle_messages[self.WELCOME_MESSAGE].update(state)
            # print(self.deck.cards)

        elif self.game_state == self.CODY_CASTING_SPELL_SCREEN:
            self.battle_messages[self.CODY_CASTING_SPELL_MESSAGE].update(state)
            self.update_cody_casting_spell_screen_helper(state)
        elif self.game_state == self.BET_SCREEN:
            self.update_bet_screen_helper(state, controller)
            self.battle_messages[self.BET_MESSAGE].update(state)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.update_magic_menu_selection_box(controller, state)
        elif self.game_state == self.DRAW_CARD_SCREEN:
            self.battle_messages[self.DRAW_CARD_MESSAGE].update(state)
            self.update_draw_card_screen_logic(state)
        elif self.game_state == self.PLAYER_DRAWS_ACE_SCREEN:
            # self.draw_player_and_enemy_cards_face_up(state.DISPLAY)
            self.update_player_draws_ace_helper(state)
        elif self.game_state == self.ENEMY_DRAWS_ACE_SCREEN:
            # self.draw_player_and_enemy_cards_face_up(state.DISPLAY)
            self.update_enemy_draws_ace_helper(state)
        elif self.game_state == self.PLAYER_SPREAD_SCREEN:
            self.battle_messages[self.SPLIT_MESSAGE].update(state)
            self.update_player_spread_screen_helper(state, controller)
        elif self.game_state == self.PLAYER_WINS_SCREEN:
            self.battle_messages[self.PLAYER_WIN_SPREAD_MESSAGE].update(state)
            self.update_spread_over(controller, state)
        elif self.game_state == self.ENEMY_WINS_SCREEN:
            self.battle_messages[self.PLAYER_LOSE_SPREAD_MESSAGE].update(state)
            self.update_spread_over(controller, state)
        elif self.game_state == self.GAME_OVER_SCREEN:
            self.game_over_helper(controller, state)

    def draw(self, state: 'GameState'):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)
        self.draw_box_info(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info(state)
            self.battle_messages[self.WELCOME_MESSAGE].draw(state)
        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].draw(state)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.draw_magic_menu_selection_box(state)
        elif self.game_state == self.DRAW_CARD_SCREEN:
            self.battle_messages[self.DRAW_CARD_MESSAGE].draw(state)
            self.draw_draw_card_screen(state)
        elif self.game_state == self.PLAYER_DRAWS_ACE_SCREEN:
            self.draw_player_and_enemy_cards_face_up(state.DISPLAY)
            self.battle_messages[self.PLAYER_DRAWS_ACE_MESSAGE].draw(state)
            # self.draw_draw_card_screen(state)
        elif self.game_state == self.ENEMY_DRAWS_ACE_SCREEN:
            self.draw_player_and_enemy_cards_face_up(state.DISPLAY)
            self.battle_messages[self.ENEMY_DRAWS_ACE_MESSAGE].draw(state)
            # self.draw_draw_card_screen(state)
        elif self.game_state == self.PLAYER_SPREAD_SCREEN:
            self.battle_messages[self.SPLIT_MESSAGE].draw(state)
            self.draw_draw_card_screen(state)
        elif self.game_state == self.PLAYER_WINS_SCREEN:
            self.draw_player_and_enemy_cards_face_up(state.DISPLAY)
            self.battle_messages[self.PLAYER_WIN_SPREAD_MESSAGE].draw(state)
        elif self.game_state == self.ENEMY_WINS_SCREEN:
            self.draw_player_and_enemy_cards_face_up(state.DISPLAY)
            self.battle_messages[self.PLAYER_LOSE_SPREAD_MESSAGE].draw(state)
        elif self.game_state == self.GAME_OVER_SCREEN:
            pass

        pygame.display.flip()

    def update_enemy_draws_ace_helper(self, state):
        self.battle_messages[self.ENEMY_DRAWS_ACE_MESSAGE].update(state)
        self.battle_messages[self.ENEMY_DRAWS_ACE_MESSAGE].messages = [
            f"You lose {self.bet} money and lose {self.high_exp} exp points"]
        if state.controller.confirm_button:
            if self.battle_messages[self.ENEMY_DRAWS_ACE_MESSAGE].is_finished():
                self.round_reset_high_low()
                self.player_hand.clear()
                self.enemy_hand.clear()
                state.player.money -= self.bet
                state.player.exp += self.medium_exp

                self.money += self.bet
                self.buff_red_card_only_in_deck = False

                self.game_state = self.WELCOME_SCREEN

    def update_cody_casting_spell_screen_helper(self, state: 'GameState'):
        if state.controller.confirm_button:
            self.cody_magic_points -= 1
            self.build_custom_26_card_deck()
            self.game_state = self.WELCOME_SCREEN

    def update_player_draws_ace_helper(self, state):
        self.battle_messages[self.PLAYER_DRAWS_ACE_MESSAGE].update(state)
        self.battle_messages[self.PLAYER_DRAWS_ACE_MESSAGE].messages = [
            f"You win {self.bet} money and gain {self.high_exp} exp points"]
        if state.controller.confirm_button:
            if self.battle_messages[self.PLAYER_DRAWS_ACE_MESSAGE].is_finished():
                self.buff_red_card_only_in_deck = False
                state.player.money += self.bet
                state.player.exp += self.high_exp
                self.money -= self.bet
                self.round_reset_high_low()
                self.player_hand.clear()
                self.enemy_hand.clear()
                self.game_state = self.WELCOME_SCREEN

    def update_spread_over(self, controller, state: 'GameState'):
        if controller.confirm_button:
            if self.game_state == self.PLAYER_WINS_SCREEN:
                if self.battle_messages[self.PLAYER_WIN_SPREAD_MESSAGE].is_finished():
                    self.reset_spread_no_ace(state)
                    state.player.exp += self.low_exp

                    if self.spread_counter == 1:
                        state.player.exp += self.high_exp
                        state.player.money += self.bet * 3
                        self.money -= self.bet * 3
                    elif self.spread_counter == 2:
                        state.player.exp += self.medium_exp
                        state.player.money += self.bet * 2
                        self.money -= self.bet * 2
                    elif self.spread_counter == 3:
                        state.player.exp += self.medium_exp
                        state.player.money += self.bet
                        self.money -= self.bet

                    elif self.spread_counter == 4:
                        state.player.exp += self.low_exp
                        state.player.money += self.bet // 2
                        self.money -= self.bet // 2
                    self.game_state = self.WELCOME_SCREEN
            elif self.game_state == self.ENEMY_WINS_SCREEN:
                if self.battle_messages[self.PLAYER_LOSE_SPREAD_MESSAGE].is_finished():
                    self.reset_spread_no_ace(state)
                    if self.spread_counter == 1:
                        state.player.exp -= self.high_exp
                        state.player.money -= self.bet * 3
                        self.money += self.bet * 3
                    elif self.spread_counter == 2:
                        state.player.exp -= self.medium_exp
                        state.player.money -= self.bet * 2
                        self.money += self.bet * 2
                    elif self.spread_counter == 3:
                        state.player.exp -= self.medium_exp
                        state.player.money -= self.bet
                        self.money += self.bet
                    self.game_state = self.WELCOME_SCREEN

    def update_draw_card_screen_logic(self, state: 'GameState'):
        # Only draw if hands are empty
        if len(self.player_hand) == 0 and len(self.enemy_hand) == 0:
            print(f"Deck size before drawing: {len(self.deck.cards)}")
            print(f"Top 5 cards before draw: {self.deck.cards[-5:]}")

            self.player_hand = self.deck.player_draw_hand(1)
            self.enemy_hand = self.deck.enemy_draw_hand(1)
            self.player_score = self.deck.compute_hand_value_high_low(self.player_hand)
            self.enemy_score = self.deck.compute_hand_value_high_low(self.enemy_hand)

            print(f"Deck size after drawing: {len(self.deck.cards)}")
            print(f"Top 5 cards after draw: {self.deck.cards[-5:]}")
        if state.controller.confirm_button:
            print(self.enemy_hand)
            print(self.player_hand)

            if ('Ace', 'Hearts', 20) in self.player_hand or ('Ace', 'Clubs', 20) in self.player_hand:
                self.game_state = self.PLAYER_DRAWS_ACE_SCREEN

            elif ('Ace', 'Hearts', 20) in self.enemy_hand or ('Ace', 'Clubs', 20) in self.enemy_hand:
                lucky_attack: int = random.randint(1, 100)
                lucky_attack += state.player.luck * 3

                if lucky_attack > 85:
                    self.player_hand, self.enemy_hand = self.enemy_hand, self.player_hand
                    self.player_score = self.deck.compute_hand_value_high_low(self.player_hand)
                    self.enemy_score = self.deck.compute_hand_value_high_low(self.enemy_hand)
                    self.game_state = self.PLAYER_DRAWS_ACE_SCREEN
                else:
                    self.game_state = self.ENEMY_DRAWS_ACE_SCREEN
            else:
                self.game_state = self.PLAYER_SPREAD_SCREEN

    def update_player_spread_screen_helper(self, state: 'GameState', controller):
        if Equipment.HIGH_LOW_PANTS.value in state.player.equipped_items:
            spread_bonus: int = 1
        else:
            spread_bonus: int = 0

        if controller.up_button:
            if self.spread_counter < (3 + spread_bonus):
                self.spread_counter += 1
        elif controller.down_button:
            if self.spread_counter > 1:
                self.spread_counter -= 1
        elif controller.confirm_button:
            player_split_low = self.player_score - self.spread_counter
            player_split_high = self.player_score + self.spread_counter
            new_range = range(player_split_low, player_split_high + 1)
            # we take away extra HP for balance reasons
            if self.spread_counter > 3:
                state.player.stamina_points -= 5
            if self.enemy_score in new_range:
                self.game_state = self.PLAYER_WINS_SCREEN
            else:
                self.game_state = self.ENEMY_WINS_SCREEN

        self.battle_messages[self.SPLIT_MESSAGE].messages = [
            f"Press up and down for your spread: {self.spread_counter}"]

    def update_welcome_screen_helper(self, state: 'GameState', controller):
        draw_screen = 0
        magic_screen = 1
        bet_screen = 2
        leave_game = 3
        # print(self.welcome_screen_index)
        if state.player.money <= 0:
            self.game_state = self.GAME_OVER_SCREEN
            return
        elif state.player.stamina_points <= 0:
            self.game_state = self.GAME_OVER_SCREEN
            return
        elif self.money <= 0:
            print("enemy defeated")

        if len(self.deck.cards) < 2:
            self.reset_high_low_game()

        if controller.confirm_button:
            if self.welcome_screen_index == draw_screen:
                self.game_state = self.DRAW_CARD_SCREEN

            elif self.welcome_screen_index == magic_screen:
                self.game_state = self.MAGIC_MENU_SCREEN

            elif self.welcome_screen_index == bet_screen:
                self.game_state = self.BET_SCREEN

            elif self.welcome_screen_index == leave_game:
                state.currentScreen = state.area3GamblingScreen
                state.area3GamblingScreen.start(state)

    def update_bet_screen_helper(self, state, controller):

        if controller.isBPressed or controller.isBPressedSwitch:
            controller.isBPressed = False
            controller.isBPressedSwitch = False
            self.game_state = self.WELCOME_SCREEN
        min_bet = 50
        max_bet = 200

        if controller.up_button:
            self.menu_movement_sound.play()  # Play the sound effect once
            self.bet += min_bet
        elif controller.down_button:
            self.menu_movement_sound.play()  # Play the sound effect once
            self.bet -= min_bet

        if self.bet <= min_bet:
            self.bet = min_bet
        elif self.bet >= max_bet:
            self.bet = max_bet

    def update_magic_menu_selection_box(self, controller, state):
        if controller.confirm_button:
            if self.magic_menu_selector[self.magic_screen_index] == Magic.FLUSH_DECK.value:
                self.buff_red_card_only_in_deck = True
                self.reset_high_low_game()
                state.player.focus_points -= self.buff_red_card_only_in_deck_cost
                self.game_state = self.WELCOME_SCREEN

            elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
                self.game_state = self.WELCOME_SCREEN
                self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].update(state)

        if controller.up_button:
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index - self.index_stepper) % len(self.magic_menu_selector)
            # print(f"Current Magic Menu Selector: {self.magic_menu_selector[self.magic_screen_index]}")
        elif controller.down_button:
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index + self.index_stepper) % len(self.magic_menu_selector)

        if controller.confirm_button:
            if self.magic_menu_selector[self.magic_screen_index] == Magic.SHIELD.value:
                self.game_state = self.WELCOME_SCREEN
            elif self.magic_menu_selector[self.magic_screen_index] == Magic.HEADS_FORCE.value:
                self.game_state = self.WELCOME_SCREEN
            elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
                self.game_state = self.WELCOME_SCREEN

    def game_over_helper(self, controller, state: "GameState"):
        no_money_game_over = 0
        no_stamina_game_over = 0

        if state.player.money <= no_money_game_over:
            if controller.confirm_button:
                state.currentScreen = state.gameOverScreen
                state.gameOverScreen.start(state)

        elif state.player.stamina_points <= no_stamina_game_over:
            if controller.confirm_button:
                state.player.money -= 100
                self.reset_high_low_game()
                state.currentScreen = state.area3GamblingScreen
                state.area3GamblingScreen.start(state)

    def draw_magic_menu_selection_box(self, state):
        if self.magic_menu_selector[self.magic_screen_index] == Magic.SHIELD.value:
            pass
        elif self.magic_menu_selector[self.magic_screen_index] == Magic.HEADS_FORCE.value:
            pass
        elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)

        choice_spacing = 40
        text_x_offset = 60
        text_y_offset = 15
        arrow_x_offset = 12
        arrow_y_offset_triple_dice = 12
        arrow_y_offset_back = 52
        black_box_height = 221 - 50  # Adjust height
        black_box_width = 200 - 10  # Adjust width to match the left box
        border_width = 5
        start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
        start_y_right_box = 240  # Adjust vertical alignment
        black_box = pygame.Surface((black_box_width, black_box_height))
        black_box.fill(BLACK)

        white_border = pygame.Surface(
            (black_box_width + 2 * border_width, black_box_height + 2 * border_width)
        )
        white_border.fill(WHITE)
        white_border.blit(black_box, (border_width, border_width))

        black_box_x = start_x_right_box - border_width
        black_box_y = start_y_right_box - border_width

        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

        for idx, choice in enumerate(self.magic_menu_selector):
            y_position = start_y_right_box + idx * choice_spacing  # Use the defined spacing variable
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)  # Use the defined offsets
            )

        # Draw the arrow at the current magic screen index position
        arrow_y_position = start_y_right_box + (self.magic_screen_index * choice_spacing) + text_y_offset
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, arrow_y_position)  # Use the arrow offsets
        )

    def draw_draw_card_screen(self, state: 'GameState'):
        initial_x_position = 400
        initial_y_position = 1
        player_target_y = 300
        enemy_target_y = 50
        move_card_x = 75
        card_speed = 3
        flip_y_position = 145

        # Validate hands
        if not self.player_hand or not self.enemy_hand:
            print("Error: player_hand or enemy_hand is empty.")
            return

        # Initialize player positions
        if not hasattr(self, 'player_card_y_positions'):
            self.player_card_y_positions = [initial_y_position]
            self.player_card_x_positions = [initial_x_position]

        # Initialize enemy positions
        if not hasattr(self, 'enemy_card_y_positions'):
            self.enemy_card_y_positions = [initial_y_position]
            self.enemy_card_x_positions = [initial_x_position]

        # Deal player card
        if self.player_card_y_positions[0] < player_target_y:
            self.player_card_y_positions[0] += card_speed
            if self.player_card_y_positions[0] > player_target_y:
                self.player_card_y_positions[0] = player_target_y

            if self.player_card_y_positions[0] >= flip_y_position:
                self.deck.draw_card_face_up(self.player_hand[0][1], self.player_hand[0][0],
                                            (self.player_card_x_positions[0], self.player_card_y_positions[0]), DISPLAY)
            else:
                self.deck.draw_card_face_down((self.player_card_x_positions[0], self.player_card_y_positions[0]),
                                              DISPLAY)
            return  # Wait until card reaches position before continuing

        # Draw final player card
        self.deck.draw_card_face_up(self.player_hand[0][1], self.player_hand[0][0],
                                    (self.player_card_x_positions[0], self.player_card_y_positions[0]), DISPLAY)

        # Deal enemy card
        if self.enemy_card_y_positions[0] < enemy_target_y:
            self.enemy_card_y_positions[0] += card_speed
            if self.enemy_card_y_positions[0] > enemy_target_y:
                self.enemy_card_y_positions[0] = enemy_target_y

            # self.deck.draw_card_face_up(self.enemy_hand[0][1], self.enemy_hand[0][0],
            #                             (self.enemy_card_x_positions[0], self.enemy_card_y_positions[0]), DISPLAY)
            self.deck.draw_card_face_down((self.enemy_card_x_positions[0], self.enemy_card_y_positions[0]), DISPLAY)

            return  # Wait until enemy card is placed before continuing

        # Draw final enemy card (face down)
        # self.deck.draw_card_face_up(self.enemy_hand[0][1], self.enemy_hand[0][0],
        #                             (self.enemy_card_x_positions[0], self.enemy_card_y_positions[0]), DISPLAY)

        # draw  enemy card face up
        self.deck.draw_card_face_down((self.enemy_card_x_positions[0], self.enemy_card_y_positions[0]), DISPLAY)

        # Transition logic
        # self.game_state = self.PLAYER_ACTION_SCREEN

    def draw_player_and_enemy_cards_face_up(self, display_surface):
        # Use standard positions to match your layout
        player_position = (400, 300)
        enemy_position = (400, 50)

        if self.player_hand:
            self.deck.draw_card_face_up(
                self.player_hand[0][1],  # suit
                self.player_hand[0][0],  # rank
                player_position,
                display_surface
            )

        if self.enemy_hand:
            self.deck.draw_card_face_up(
                self.enemy_hand[0][1],  # suit
                self.enemy_hand[0][0],  # rank
                enemy_position,
                display_surface
            )

    def draw_welcome_screen_box_info(self, state: 'GameState'):
        box_width_offset = 10
        horizontal_padding = 25
        vertical_position = 240
        spacing_between_choices = 40
        text_x_offset = 60
        text_y_offset = 15
        black_box_width = 200 - box_width_offset
        start_x_right_box = state.DISPLAY.get_width() - black_box_width - horizontal_padding
        start_y_right_box = vertical_position
        arrow_x_coordinate_padding = 12
        arrow_y_coordinate_padding_play = 12
        arrow_y_coordinate_padding_magic = 52
        arrow_y_coordinate_padding_bet = 92
        arrow_y_coordinate_padding_quit = 132

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

    def draw_box_info(self, state: 'GameState'):
        player_enemy_box_info_x_position = 37
        enemy_name_y_position = 33
        enemy_money_y_position = 70
        bet_y_position = 370
        player_money_y_position = 250
        hero_stamina_y_position = 290
        hero_focus_y_position = 330

        state.DISPLAY.blit(self.font.render(self.dealer_name, True, WHITE),
                           (player_enemy_box_info_x_position, enemy_name_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER} {self.money}", True, WHITE),
                           (player_enemy_box_info_x_position, enemy_money_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.BET_HEADER}: {self.bet}", True, WHITE),
                           (player_enemy_box_info_x_position, bet_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER}: {state.player.money}", True, WHITE),
                           (player_enemy_box_info_x_position, player_money_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.HP_HEADER}: {state.player.stamina_points}", True, WHITE),
                           (player_enemy_box_info_x_position, hero_stamina_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MP_HEADER}: {state.player.focus_points}", True, WHITE),
                           (player_enemy_box_info_x_position, hero_focus_y_position))
        #

    def draw_menu_selection_box(self, state: "GameState"):
        # Define local variables for dimensions and positions
        box_height_offset = 50
        box_width_offset = 10
        border_width = 5
        horizontal_padding = 25
        vertical_position = 240
        box_initial_height = 221
        white_border_top_left = 2
        box_initial_width = 200
        black_box_height = box_initial_height - box_height_offset
        black_box_width = box_initial_width - box_width_offset
        start_x_right_box = state.DISPLAY.get_width() - black_box_width - horizontal_padding
        start_y_right_box = vertical_position
        black_box = pygame.Surface((black_box_width, black_box_height))
        black_box.fill(BLACK)
        white_border = pygame.Surface(
            (black_box_width + white_border_top_left * border_width,
             black_box_height + white_border_top_left * border_width)
        )
        white_border.fill(WHITE)
        white_border.blit(black_box, (border_width, border_width))
        black_box_x = start_x_right_box - border_width
        black_box_y = start_y_right_box - border_width
        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))
