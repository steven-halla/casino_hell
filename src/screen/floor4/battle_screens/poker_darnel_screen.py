import pygame

from constants import WHITE, BLACK, RED, DISPLAY
from deck import Deck
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from game_constants.equipment import Equipment
from game_constants.magic import Magic
from tests.test_poker_darnel import test_poker_score_tracker
from types import *
import random

# New spell: inflict heat
# this spell doubles heat increse/decrease


class PokerDarnelScreen(GambleScreen):
    def __init__(self, screenName: str = "poker_darnel"):
        super().__init__(screenName)
        self.deck = Deck()
        self.deck.poker_cards_shuffle()

        self.enemy_pressure: int = 0

        self.welcome_screen_choices: list[str] = ["Play", "Magic", "Bet", "Quit"]
        self.deal_cards_screen_choices: list[str] = ["Accept", "ReDraw"]
        self.welcome_screen_play_index: int = 0
        self.welcome_screen_magic_index: int = 1
        self.welcome_screen_bet_index: int = 2
        self.welcome_screen_quit_index: int = 3
        self.welcome_screen_index: int = 0
        self.deal_cards_screen_index: int = 0
        self.bet: int = 100


        self.last_screen_check_time = pygame.time.get_ticks()
        self.enemy_cards_swap_container = []
        self.player_cards_swap_container = []
        self.swap_player_cards: bool = False
        self.swap_enemy_cards: bool = True
        self.magic_lock: bool = False
        self.magic_menu_index: int = 0
        self.money: int = 1000
        self.enemy_compare_hand: str = ""
        self.enemy_temp_discard_storage: list = []
        self.player_hand_type = ""
        self.enemy_hand_type = ""
        self.bet: int = 50
        self.enemy_bet: int = 50
        self.player_redraw_menu_index = 0
        self.player_card_discard_index = 0
        self.player_card_garbage_can = []
        self.bet: int = 0
        self.add_enemy_bet:int = 0
        self.action_menu_index: int = 0
        self.action_menu_choices: list[str] = ["Play", "Magic", "Fold"]
        self.future_cards_container: list = []
        self.magic_menu_options: list = []
        self.swap_cards_menu_options: list = []
        self.swap_cards_menu_index: int = 0
        self.enemy_bet_heat: int = 0
        self.enemy_hand_bet_strength: int = 0
        self.bluffalo_allowed: bool = True


        self.game_state = self.WELCOME_SCREEN
        self.enemy_making_bet: bool = False



        # Remove duplicate Aces
        # self.deck.cards = [card if card[0] != "Ace" else ("Ace", card[1], 14) for card in self.deck.cards]
        self.deck.cards = [
            ("Ace", card[1], 14) if card[0] == "Ace" else
            ("King", card[1], 13) if card[0] == "King" else
            ("Queen", card[1], 12) if card[0] == "Queen" else
            ("Jack", card[1], 11) if card[0] == "Jack" else
            card
            for card in self.deck.cards
        ]

        self.player_hand_score: int = 0
        self.player_value_score: int = 0
        self.enemy_hand_score: int = 0
        self.enemy_value_score: int = 0
        self.enemy_hand_power: int = 0
        self.enemy_money = 2000

        # Initialize battle messages
        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "Welcome to Poker! I'm Darnel, your dealer today.",
                "Ready to test your luck and skill?",
                "Choose an option to continue."
            ]),
            self.BET_MESSAGE: MessageBox([
                "How much would you like to bet? Use up and down keys to adjust your bet."

            ]),
            self.DEAL_CARDS_MESSAGE: MessageBox([
                "Time to deal your cards",

            ]),
            self.PLAYER_DISCARD_MESSAGE: MessageBox([
                "Press up/down to go through menu, as well as left/right to go through cards you want to discard.2 discard max.",

            ]),
            self.PLAYER_REDRAW_MESSAGE: MessageBox([
                "Press confirm button to get out of here of your PLAYER REDRAW SCREEN",

            ]),
            self.ENEMY_DISCARD_MESSAGE: MessageBox([
                "Press confirm button to get out of here of your ENEMY DISCARD MESSAGE" ,

            ]),
            self.ENEMY_REDRAW_MESSAGE: MessageBox([
                "Press confirm button to get out of here of your ENEMY REDRAW MESSAGE",

            ]),
            self.ACTION_MESSAGE: MessageBox([
                "Press confirm button to get out of here of your ACTION MESSAGE",

            ]),
            self.REVEAL_FUTURE_CARDS_MESSAGE: MessageBox([
                "Press confirm button to get out of here of your Reveal Future cards message",

            ])

        }

        self.player_hand = [


        ]

        # Enemy hand: Full House (Kings over Queens)
        self.enemy_hand = [


        ]

        # self.player_hand: list[tuple[str, str, int]] = [
        #
        # ]
        #
        # self.enemy_hand: list[tuple[str, str, int]] = [
        #
        # ]

    SWAP_CARDS_SCREEN: str = "swap_cards_screen"
    WELCOME_MESSAGE: str = "welcome_message"
    BET_MESSAGE: str = "bet_message"

    DEAL_CARDS_SCREEN: str = "deal_cards_screen"
    PLAYER_REDRAW_SCREEN: str = "player_redraw_screen"
    PLAYER_DISCARD_SCREEN: str = "player_discard_screen"
    ENEMY_REDRAW_SCREEN: str = "enemy_redraw_screen"
    ENEMY_REDRAW_MESSAGE: str = "enemy_redraw messages"
    ENEMY_DISCARD_SCREEN: str = "enemy_discard_screen"
    ENEMY_DISCARD_MESSAGE: str = "enemy_discard_,message"
    REVEAL_FUTURE_CARDS: str = "reveal_future_cards"
    REVEAL_FUTURE_CARDS_MESSAGE: str = "reveal_future_cards messages"
    DRAW_ONE_CARD: str = "draw_one_card"
    FIFTH_ROUND_SHOW: str = "fifth_round_show"
    FIFTH_ROUND_DEAL: str = "fifth_round_deal"
    FINAL_RESULTS: str = "final_results"
    PLAYER_WINS: str = "player_wins"
    ENEMY_WINS: str = "enemy_wins"
    DRAW: str = "draw"
    ACTION_SCREEN: str = "action_screen"
    ACTION_MESSAGE: str = "action_message"
    RESET: str = "reset"
    ENEMY_ACTION_SCREEN: str = "enemy action screen"
    BLUFFALO_SCREEN: str = "bluffalo screen"
    DEAL_CARDS_MESSAGE: str = "deal cards message"
    PLAYER_DISCARD_MESSAGE: str = "player discard message"
    PLAYER_REDRAW_MESSAGE: str = "player redraw message"




    # def start(self):
    #     print("Pew")

    def update_welcome_screen_logic(self, controller, state):
        if controller.up_button:
            self.welcome_screen_index = (self.welcome_screen_index - 1) % len(self.welcome_screen_choices)
            print(f"Selected option: {self.welcome_screen_choices[self.welcome_screen_index]}")
        elif controller.down_button:
            self.welcome_screen_index = (self.welcome_screen_index + 1) % len(self.welcome_screen_choices)
            print(f"Selected option: {self.welcome_screen_choices[self.welcome_screen_index]}")

        if controller.confirm_button:
            if self.welcome_screen_index == self.welcome_screen_play_index:
                print("Player money is: " + str(state.player.money))
                self.game_state = self.DEAL_CARDS_SCREEN
            elif self.welcome_screen_index == self.welcome_screen_magic_index and not self.magic_lock:
                self.game_state = self.MAGIC_MENU_SCREEN
            elif self.welcome_screen_index == self.welcome_screen_bet_index:
                self.game_state = self.BET_SCREEN
            elif self.welcome_screen_index == self.welcome_screen_quit_index:
                state.currentScreen = state.area4GamblingScreen
                state.area4GamblingScreen.start(state)
                state.player.canMove = True

    def restart_poker_round(self):
        self.deck.poker_cards_shuffle()
        self.enemy_cards_swap_container = []
        self.player_cards_swap_container = []
        self.swap_player_cards: bool = False
        self.swap_enemy_cards: bool = True
        self.magic_menu_index: int = 0
        self.bet: int = 50
        self.enemy_bet: int = 50
        self.player_redraw_menu_index = 0
        self.player_card_discard_index = 0
        self.player_card_garbage_can = []
        self.bet: int = 0
        self.add_enemy_bet: int = 0
        self.enemy_hand_bet_strength:int = 0
        self.bluffalo_allowed = True

        if self.enemy_pressure < 0:
            self.enemy_pressure = 0


    def update(self, state):
        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)

        if Equipment.POKER_BRACELET.value in state.player.equipped_items:
            for card in self.player_hand:
                if card[0] == "2":
                    print("ERROR WITH POKER BRACELET ERROR ERROR ERROR")
                    break

        current_time = pygame.time.get_ticks()
        if current_time - self.last_screen_check_time >= 8000:
            self.poker_score_tracker()

            print(f"Current screen: {self.game_state}")
            # print(f"PLAYER HAND: {self.player_hand}")
            # print(f"ENEMY HAND: {self.enemy_hand}")
            # print(f"Player bet is : " + str(self.bet))
            # print(f"Enemy bet is : " + str(self.enemy_bet))

            self.last_screen_check_time = current_time

        if Magic.POKER_CARD_SWAP.value in state.player.magicinventory and Magic.POKER_CARD_SWAP.value not in self.magic_menu_options:
                self.magic_menu_options.append(Magic.POKER_CARD_SWAP.value)
                self.magic_menu_options.append("Back")

        #BLUFF command should have a weight that over time grows the more money diff there is

        if self.game_state == self.WELCOME_SCREEN:
            # print("Hi welcome to the welcome screen press T to start")
            self.battle_messages[self.WELCOME_MESSAGE].update(state)
            self.update_welcome_screen_logic(state.controller, state)
        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].update(state)
            if state.controller.up_button:
                if self.bet + 25 <= 50:  # Check if adding 25 won't exceed max
                    self.bet += 25
                    print(f"Bet increased to: {self.bet}")

            elif state.controller.down_button:
                if self.bet - 25 >= 25:  # Check if subtracting 25 won't go below min
                    self.bet -= 25
                    print(f"Bet decreased to: {self.bet}")

            # Ensure bet stays within valid range
            if self.bet < 25:
                self.bet = 25
            elif self.bet > 50:
                self.bet = 50

            # Ensure bet doesn't exceed player's money
            if self.bet > state.player.money:
                self.bet = (state.player.money // 25) * 25  # Round down to nearest 25
                if self.bet < 0:  # If player has less than minimum bet
                    self.bet = 0  # Or handle insufficient funds cas

            if state.controller.action_and_cancel_button:
                self.game_state = self.WELCOME_SCREEN






        #---------------------enemy logic below
            if self.enemy_making_bet == True:

                if len(self.enemy_hand) > 5 and self.enemy_hand_bet_strength >= 5:
                    self.enemy_bet += 50
                    self.enemy_making_bet = False
                else:
                    bluff_roll = random.randint(1, 100)
                    bluff_roll += self.enemy_hand_bet_strength * 5
                    bluff_roll = min(bluff_roll, 100)

                    if bluff_roll <= 50:
                        extra_bet = 0
                    elif bluff_roll <= 70:
                        extra_bet = 25
                    elif bluff_roll <= 80:
                        extra_bet = 25
                    elif bluff_roll <= 85:
                        extra_bet = 50
                    else:
                        extra_bet = 50

                    self.enemy_bet += extra_bet
                    self.enemy_making_bet = False


                self.game_state = self.ACTION_SCREEN

        elif self.game_state == self.MAGIC_MENU_SCREEN:
            if state.controller.up_button:
                self.magic_menu_index = (self.magic_menu_index - 1) % len(self.magic_menu_options)
                print(f"{self.magic_menu_index}: {self.magic_menu_options[self.magic_menu_index]}")

            elif state.controller.down_button:
                self.magic_menu_index = (self.magic_menu_index + 1) % len(self.magic_menu_options)
                print(f"{self.magic_menu_index}: {self.magic_menu_options[self.magic_menu_index]}")


            if state.controller.confirm_button:
                if self.magic_menu_options[self.magic_menu_index] == Magic.POKER_CARD_SWAP.value:
                    print("cast spell")
                    self.game_state = self.SWAP_CARDS_SCREEN
                    self.magic_menu_index = 0



                elif self.magic_menu_options[self.magic_menu_index] == "Back":
                    self.game_state = self.ACTION_SCREEN
                    self.magic_menu_index = 0


        elif self.game_state == self.SWAP_CARDS_SCREEN:



            if self.swap_enemy_cards:
                if state.controller.up_button:
                    self.swap_cards_menu_index = (self.swap_cards_menu_index + 1) % len(self.enemy_hand)
                    print(
                        f"Selected enemy card {self.swap_cards_menu_index}: {self.enemy_hand[self.swap_cards_menu_index]}")
                elif state.controller.down_button:
                    self.swap_cards_menu_index = (self.swap_cards_menu_index - 1) % len(self.enemy_hand)
                    print(
                        f"Selected enemy card {self.swap_cards_menu_index}: {self.enemy_hand[self.swap_cards_menu_index]}")
                elif state.controller.confirm_button:
                    print(f"Before append: {self.enemy_cards_swap_container}")
                    self.enemy_cards_swap_container.append(self.swap_cards_menu_index)
                    print(f"After append: {self.enemy_cards_swap_container}")
                    self.swap_enemy_cards = False
                    self.swap_player_cards = True
                    self.swap_cards_menu_index = 0

            elif self.swap_player_cards:
                if state.controller.action_and_cancel_button:
                    self.swap_player_cards = False
                    self.swap_enemy_cards = True
                    self.enemy_cards_swap_container = []
                if state.controller.up_button:
                    self.swap_cards_menu_index = (self.swap_cards_menu_index + 1) % len(self.player_hand)
                    print(
                        f"Selected player card {self.swap_cards_menu_index}: {self.player_hand[self.swap_cards_menu_index]}")
                elif state.controller.down_button:
                    self.swap_cards_menu_index = (self.swap_cards_menu_index - 1) % len(self.player_hand)
                    print(
                        f"Selected player card {self.swap_cards_menu_index}: {self.player_hand[self.swap_cards_menu_index]}")
                elif state.controller.confirm_button:
                    print(f"Before append: {self.player_cards_swap_container}")
                    self.player_cards_swap_container.append(self.swap_cards_menu_index)
                    print(f"After append: {self.player_cards_swap_container}")
                    self.swap_player_cards = False

                    # Print hands before swap
                    print(f"\n--- Before Swap ---")
                    print(f"Enemy hand: {self.enemy_hand}")
                    print(f"Player hand: {self.player_hand}")

                    # Do the swap
                    enemy_index = self.enemy_cards_swap_container[0]
                    player_index = self.player_cards_swap_container[0]
                    self.enemy_hand[enemy_index], self.player_hand[player_index] = (
                        self.player_hand[player_index],
                        self.enemy_hand[enemy_index],
                    )

                    # Print hands after swap
                    print(f"\n--- After Swap ---")
                    print(f"Enemy hand: {self.enemy_hand}")
                    print(f"Player hand: {self.player_hand}")
                    self.game_state = self.ACTION_SCREEN


        elif self.game_state == self.DEAL_CARDS_SCREEN:
            self.battle_messages[self.DEAL_CARDS_MESSAGE].update(state)

            if state.controller.confirm_button:
                lucky_roll = random.randint(1, 100) + (state.player.luck * 5)
                if lucky_roll >= 90:

                    ace_cards = [c for c in self.deck.poker_cards if c[0] == "Ace"][:2]
                    for ace_card in ace_cards:
                        self.deck.poker_cards.remove(ace_card)
                        self.player_hand.append(ace_card)
                        print("Appended:", ace_card)

                    self.player_hand.extend(self.deck.poker_player_draw_hand(1,state))
                    self.enemy_hand = self.deck.poker_enemy_draw_hand(3)
                    print("Player hand:" + str(self.player_hand))
                    print("Enemy hand" + str(self.enemy_hand))
                    self.game_state = self.PLAYER_DISCARD_SCREEN
                else:
                    self.player_hand.extend(self.deck.poker_player_draw_hand(3, state))
                    self.enemy_hand = self.deck.poker_enemy_draw_hand(3)
                    print("Player hand:" + str(self.player_hand))
                    print("Enemy hand" + str(self.enemy_hand))

                    self.game_state = self.PLAYER_DISCARD_SCREEN


            # First we dela out 3 cards, players can fold/hold
            # 4th round we show cards , then shuffle and deal
            # 5th round is the same
        elif self.game_state == self.PLAYER_DISCARD_SCREEN:
            self.battle_messages[self.PLAYER_DISCARD_MESSAGE].update(state)

            # Initialize index if not already set
            if state.controller.up_button:
                if self.player_redraw_menu_index < 0:
                    self.player_redraw_menu_index = -1
                # Move up with wraparound
                self.player_redraw_menu_index = (self.player_redraw_menu_index - 1) % 2
                # Reset player_card_discard_index when up is pressed
                self.player_card_discard_index = 3  # Set to a value that won't trigger any card discard actions
                # Print current selection based on index
                if self.player_redraw_menu_index == 0:
                    print("Play selected")
                elif self.player_redraw_menu_index == 1:
                    print("Redraw selected")
                else:
                    print(f"Card {self.player_redraw_menu_index - 1} selected: {self.player_hand[self.player_redraw_menu_index - 2]}")

            elif state.controller.down_button:
                if self.player_redraw_menu_index < 0:
                    self.player_redraw_menu_index = -1
                # Move down with wraparound
                self.player_redraw_menu_index = (self.player_redraw_menu_index + 1) % 2
                # Reset player_card_discard_index when down is pressed
                self.player_card_discard_index = 3  # Set to a value that won't trigger any card discard actions
                # Print current selection based on index
                if self.player_redraw_menu_index == 0:
                    print("Play selected")
                elif self.player_redraw_menu_index == 1:
                    print("Redraw selected")
                else:
                    print(f"Card {self.player_redraw_menu_index - 1} selected: {self.player_hand[self.player_redraw_menu_index - 2]}")

            elif state.controller.left_button:
                # Move left with wraparound (3 indices: 0, 1, 2)
                self.player_card_discard_index = (self.player_card_discard_index - 1) % 3
                # Set player_redraw_menu_index to null when left is pressed
                self.player_redraw_menu_index = -100
                print(f"Card discard index: {self.player_card_discard_index}")

            elif state.controller.right_button:
                # Move right with wraparound (3 indices: 0, 1, 2)
                self.player_card_discard_index = (self.player_card_discard_index + 1) % 3
                # Set player_redraw_menu_index to null when right is pressed
                self.player_redraw_menu_index = -100
                print(f"Card discard index: {self.player_card_discard_index}")

            if state.controller.confirm_button and len(self.player_card_garbage_can) <= 2:
                if self.player_redraw_menu_index == 0:
                    print("go to play screen and keep your hand")
                    self.game_state = self.ENEMY_DISCARD_SCREEN
                elif self.player_redraw_menu_index == 1 and len(self.player_card_garbage_can) > 0:
                    if len(self.player_hand) >= 1:  # Make sure there's at least 1 card left in hand
                        print("Current player hand: " + str(self.player_hand))
                        print("Cards in garbage can: " + str(self.player_card_garbage_can))

                        # Create a new hand without the discarded cards
                        self.player_hand = [card for card in self.player_hand if card not in self.player_card_garbage_can]

                        print("Player hand after removing discarded cards: " + str(self.player_hand))
                        print("Moving to draw card screen...")
                        self.game_state = self.PLAYER_REDRAW_SCREEN

                elif self.player_card_discard_index == 0:
                    # Use the player_card_discard_index to determine which card to discard
                    card_index = self.player_card_discard_index
                    if len(self.player_card_garbage_can) < 2 and self.player_hand[card_index] not in self.player_card_garbage_can:
                        print("place card selected is: " + str(self.player_hand[card_index]))
                        self.player_card_garbage_can.append(self.player_hand[card_index])
                        print("your trash can contents" + str(self.player_card_garbage_can))
                    else:
                        print("Cannot discard more cards or this card is already in the discard pile")
                elif self.player_card_discard_index == 1:
                    # Use the player_card_discard_index to determine which card to discard
                    card_index = self.player_card_discard_index
                    if len(self.player_card_garbage_can) < 2 and self.player_hand[
                        card_index] not in self.player_card_garbage_can:
                        print("place card selected is: " + str(self.player_hand[card_index]))
                        self.player_card_garbage_can.append(self.player_hand[card_index])
                        print("your trash can contents" + str(self.player_card_garbage_can))
                    else:
                        print("Cannot discard more cards or this card is already in the discard pile")
                elif self.player_card_discard_index == 2:
                    # Use the player_card_discard_index to determine which card to discard
                    card_index = self.player_card_discard_index
                    if len(self.player_card_garbage_can) < 2 and self.player_hand[
                        card_index] not in self.player_card_garbage_can:
                        print("place card selected is: " + str(self.player_hand[card_index]))
                        self.player_card_garbage_can.append(self.player_hand[card_index])
                        print("your trash can contents" + str(self.player_card_garbage_can))
                    else:
                        print("Cannot discard more cards or this card is already in the discard pile")



            elif state.controller.action_and_cancel_button:
                # Use the player_card_discard_index to determine which card to remove from discard pile
                selected_card = self.player_hand[self.player_card_discard_index]
                if selected_card in self.player_card_garbage_can:
                    self.player_card_garbage_can.remove(selected_card)
                    print(f"Removed card from discard pile: {selected_card}")


        elif self.game_state == self.PLAYER_REDRAW_SCREEN:
            self.battle_messages[self.PLAYER_REDRAW_MESSAGE].update(state)

            while len(self.player_hand) < 3:
                drawn_card = self.deck.poker_get_next_card()

                if Equipment.POKER_BRACELET.value in state.player.equipped_items and drawn_card[0] == "2":
                    while self.deck.poker_cards and self.deck.poker_cards[0][0] == "2":
                        burned_card = self.deck.poker_cards.pop(0)
                        print(f"Burned '2' from bottom: {burned_card}")
                    if self.deck.poker_cards:
                        drawn_card = self.deck.poker_cards.pop(0)
                        print(f"Drew from bottom due to bracelet: {drawn_card}")

                self.player_hand.append(drawn_card)
                print(f"Drew card: {drawn_card}")
                print("Your player hand: " + str(self.player_hand))
            # while len(self.player_hand) < 3:
            #     drawn_card = self.deck.poker_get_next_card()
            #     self.player_hand.append(drawn_card)
            #     print(f"Drew card: {drawn_card}")
            #     print("your player hand" + str(self.player_hand))
            if state.controller.confirm_button and len(self.player_hand) > 2:
                print("yeippjfsladjlfjd;a;fj 532")
                self.game_state = self.ENEMY_DISCARD_SCREEN

        elif self.game_state == self.ENEMY_DISCARD_SCREEN:
            self.battle_messages[self.ENEMY_DISCARD_MESSAGE].update(state)

            # print("enemey ")
            if  state.controller.confirm_button:
                self.enemy_discard_logic()
                self.game_state = self.ENEMY_REDRAW_SCREEN
                # self.poker_score_tracker()

        elif self.game_state == self.ENEMY_REDRAW_SCREEN:
            self.battle_messages[self.ENEMY_REDRAW_MESSAGE].update(state)

            while len(self.enemy_hand) < 3:
                drawn_card = self.deck.poker_get_next_card()
                self.enemy_hand.append(drawn_card)
                print(f"Drew card: {drawn_card}")
                print("your enemy hand" + str(self.enemy_hand))
            if state.controller.confirm_button:
                self.enemy_making_bet = True
                self.game_state = self.BET_SCREEN


        elif self.game_state == self.ACTION_SCREEN:
            self.battle_messages[self.ACTION_MESSAGE].update(state)


            if state.controller.up_button:
                self.action_menu_index = (self.action_menu_index - 1) % len(self.action_menu_choices)
                print("the action menu index is: " + str(self.action_menu_index))
            elif state.controller.down_button:
                self.action_menu_index = (self.action_menu_index + 1) % len(self.action_menu_choices)
                print("the action menu index is: " + str(self.action_menu_index))

            if state.controller.confirm_button:
                if self.action_menu_index == 0:


                    if len(self.player_hand) == 3:
                        self.game_state = self.REVEAL_FUTURE_CARDS
                    elif len(self.player_hand) < 5:
                        self.game_state = self.DRAW_ONE_CARD
                    elif len(self.player_hand) == 5:
                        self.game_state = self.FINAL_RESULTS

                #
                # elif self.action_menu_index == 1 and self.bluffalo_allowed == True:
                #     print("time to bluffallo")
                #     self.game_state = self.BLUFFALO_SCREEN
                elif self.action_menu_index == 1:
                    print("time to cast a spell card swap")
                    self.game_state = self.MAGIC_MENU_SCREEN


                elif self.action_menu_index == 2:
                    print("time to fold")
                    print("Player money is now: " + str(state.player.money))
                    state.player.money -= self.bet
                    print("Player money is now: " + str(state.player.money))

                    self.restart_poker_round()
                    self.game_state = self.WELCOME_SCREEN

        elif self.game_state == self.BLUFFALO_SCREEN:
            self.bluffalo_allowed = False
            card_length = len(self.enemy_hand)  # assuming this exists
            card_modifier = card_length * 3 # dummy multiplier, tweak later
            bet_modifier = 0
            if self.bet < 150:
                bet_modifier += 5
            elif self.bet < 250:
                bet_modifier += 15
            elif self.bet < 350:
                bet_modifier += 20
            else:
                bet_modifier += 30

            if self.enemy_pressure < 100:
                if self.enemy_score > 4:
                    self.game_state = self.ACTION_SCREEN
                elif self.enemy_score == 3:
                    # max is 165
                    # 15 card len  3 min
                    # 50 random    1 min
                    # 115 bet       16 min
                    # 180 max
                    fold_chance = random.randint(1, 50) + bet_modifier + card_modifier
                    if fold_chance > 80:
                        self.game_state = self.PLAYER_WINS
                    else:
                        self.enemy_pressure -= 10
                        self.game_state = self.ACTION_SCREEN
                elif self.enemy_score < 3:
                    fold_chance = random.randint(1, 55) + bet_modifier + card_modifier
                    if fold_chance > 80:
                        self.game_state = self.PLAYER_WINS
                    else:
                        self.enemy_pressure -= 15
                        self.game_state = self.ACTION_SCREEN
            elif self.enemy_pressure >= 100:
                if self.enemy_score > 4:
                    self.game_state = self.ACTION_SCREEN
                elif self.enemy_score == 3:
                    # max is 165
                    # 15 card len  3 min
                    # 50 random    1 min
                    # 115 bet       16 min
                    # 180 max
                    fold_chance = random.randint(1, 60) + bet_modifier + card_modifier
                    if fold_chance > 80:
                        self.game_state = self.PLAYER_WINS
                    else:
                        self.enemy_pressure -= 10
                        self.game_state = self.ACTION_SCREEN
                elif self.enemy_score < 3:
                    fold_chance = random.randint(1, 65) + bet_modifier + card_modifier
                    if fold_chance > 80:
                        self.game_state = self.PLAYER_WINS
                    else:
                        self.enemy_pressure -= 15
                        self.game_state = self.ACTION_SCREEN




        elif self.game_state == self.ENEMY_ACTION_SCREEN:
            pass


        elif self.game_state == self.REVEAL_FUTURE_CARDS:
            self.battle_messages[self.REVEAL_FUTURE_CARDS_MESSAGE].update(state)

            if state.controller.confirm_button:
                self.reveal_future_cards(state)
                self.game_state = self.DRAW_ONE_CARD


        elif self.game_state == self.DRAW_ONE_CARD:

            if state.controller.confirm_button:

                drawn_card = self.deck.poker_get_next_card()

                if Equipment.POKER_BRACELET.value in state.player.equipped_items and drawn_card[0] == "2":
                    # Burn from the bottom until the bottom card is not a "2"
                    while self.deck.poker_cards and self.deck.poker_cards[0][0] == "2":
                        burned_card = self.deck.poker_cards.pop(0)
                        print(f"Burned '2' from bottom: {burned_card}")
                    # Draw from the bottom instead of top
                    if self.deck.poker_cards:
                        drawn_card = self.deck.poker_cards.pop(0)
                        print(f"Drew from bottom due to bracelet: {drawn_card}")
                self.player_hand.append(drawn_card)
                print(f"Player drew: {drawn_card}")

                # Update player score
                self.player_score = self.deck.compute_hand_value(self.player_hand)

                # Draw one card for enemy
                enemy_card = self.deck.poker_get_next_card()
                self.enemy_hand.append(enemy_card)
                print(f"Enemy drew: {enemy_card}")

                # Update enemy score
                self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)
                self.enemy_making_bet = True


                # Move to next game state after drawing
                self.game_state = self.BET_SCREEN




        elif self.game_state == self.FINAL_RESULTS:
            if state.controller.confirm_button:
                self.poker_score_tracker()

                # Get final scores
                player_score = self.get_hand_score(self.player_hand_type)
                enemy_score = self.get_hand_score(self.enemy_hand_type)

                # If hands are the same type, add bonus scores
                if self.player_hand_type == self.enemy_hand_type:
                    player_score += self.get_bonus_score_if_tied(self.player_hand_type, self.player_hand)
                    enemy_score += self.get_bonus_score_if_tied(self.enemy_hand_type, self.enemy_hand)

                # Debug prints
                print("\nFinal Results:")
                print("Player's Hand:", self.player_hand)
                print("Enemy's Hand:", self.enemy_hand)
                print("\nHand Types:")
                print(f"Player Hand Type: {self.player_hand_type} (Score: {player_score})")
                print(f"Enemy Hand Type: {self.enemy_hand_type} (Score: {enemy_score})")

                if player_score > enemy_score:
                    self.game_state = self.PLAYER_WINS
                elif player_score < enemy_score:
                    self.game_state = self.ENEMY_WINS
                else:
                    self.game_state = self.DRAW



        elif self.game_state == self.PLAYER_WINS:
            print("Player wins ")
            state.player.money += self.enemy_bet
            self.money -= self.enemy_bet
            if self.bet <= 150:
                self.enemy_pressure += 10
            elif self.bet <= 250:
                self.enemy_pressure += 15
            elif self.bet <= 350:
                self.enemy_pressure += 20
            else:
                self.enemy_pressure += 25




        elif self.game_state == self.ENEMY_WINS:
            print("ENEMY WINS")
            state.player.money -= self.enemy_bet
            self.money += self.enemy_bet
            if self.bet <= 150:
                self.enemy_pressure -= 10
            elif self.bet <= 250:
                self.enemy_pressure -= 15
            elif self.bet <= 350:
                self.enemy_pressure -= 20
            else:
                self.enemy_pressure -= 25

        elif self.game_state == self.DRAW:
            print("Draw")








#-----------------------------------------------------------------------------------------------------------------------


    def draw(self, state):
        super().draw(state)
        self.draw_enemy_info_box(state)
        self.draw_hero_info_boxes(state)
        self.draw_menu_selection_box(state)
        self.draw_bottom_black_box(state)
        self.draw_box_info(state)
        self.draw_hands(
            player_hand=self.player_hand,
            enemy_hand=self.enemy_hand,
        )

        if self.game_state == self.WELCOME_SCREEN:
            self.draw_welcome_screen_box_info(state)
            self.battle_messages[self.WELCOME_MESSAGE].draw(state)
        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].draw(state)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            pass
        elif self.game_state == self.DEAL_CARDS_SCREEN:
            self.battle_messages[self.DEAL_CARDS_MESSAGE].draw(state)


            # First we dela out 3 cards, players can fold/hold
            # 4th round we show cards , then shuffle and deal
            # 5th round is the same
        elif self.game_state == self.PLAYER_REDRAW_SCREEN:
            self.battle_messages[self.PLAYER_REDRAW_MESSAGE].draw(state)


        elif self.game_state == self.PLAYER_DISCARD_SCREEN:
            self.draw_player_discard_screen_box_info(state)
            self.battle_messages[self.PLAYER_DISCARD_MESSAGE].draw(state)

        elif self.game_state == self.ENEMY_DISCARD_SCREEN:
            self.battle_messages[self.ENEMY_DISCARD_MESSAGE].draw(state)


        elif self.game_state == self.ENEMY_REDRAW_SCREEN:
            self.battle_messages[self.ENEMY_REDRAW_MESSAGE].draw(state)

        elif self.game_state == self.ACTION_SCREEN:
            self.draw_action_screen_box_info(state)
            self.battle_messages[self.ACTION_MESSAGE].draw(state)
        elif self.game_state == self.REVEAL_FUTURE_CARDS:
            self.battle_messages[self.REVEAL_FUTURE_CARDS_MESSAGE].draw(state)


        elif self.game_state == self.DRAW_ONE_CARD:
            pass


        elif self.game_state == self.FINAL_RESULTS:
            pass
        elif self.game_state == self.PLAYER_WINS:
            pass
        elif self.game_state == self.ENEMY_WINS:
            pass
        elif self.game_state == self.DRAW:
            pass

        pygame.display.flip()



    def get_hand_score(self, hand_type: str) -> int:
        hand_scores = {
            "royal_straight_flush": 10,
            "straight_flush": 9,
            "four_of_a_kind": 8,
            "full_house": 7,
            "flush": 6,
            "straight": 5,
            "three_of_a_kind": 4,
            "two_pair": 3,
            "one_pair": 2,
            "no_hand": 1,
        }
        return hand_scores.get(hand_type, 1)

    def get_bonus_score_if_tied(self, hand_type: str, hand: list[tuple[str, str, int]]) -> int:
        bonus_rank_values = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
            "7": 7, "8": 8, "9": 9, "10": 10,
            "Jack": 11, "Queen": 12, "King": 13, "Ace": 14,
        }

        bonus_score = 0
        rank_counts = {}
        for rank, suit, value in hand:
            #setDefautl works with DICT data types
            rank_counts.setdefault(rank, 0)
            rank_counts[rank] += 1

        #items() works only on DICT data types
        if hand_type == "one_pair":
            for rank, count in rank_counts.items():
                if count == 2:
                    bonus_score += bonus_rank_values[rank]
        elif hand_type == "two_pair":
            for rank, count in rank_counts.items():
                if count == 2:
                    bonus_score += bonus_rank_values[rank]
        elif hand_type == "three_of_a_kind":
            for rank, count in rank_counts.items():
                if count == 3:
                    bonus_score += bonus_rank_values[rank]
        elif hand_type == "four_of_a_kind":
            for rank, count in rank_counts.items():
                if count == 4:
                    bonus_score += bonus_rank_values[rank]
        elif hand_type in {"full_house", "flush", "straight", "straight_flush", "royal_straight_flush"}:
            for rank, _, _ in hand:
                bonus_score += bonus_rank_values[rank]

        return bonus_score

    def poker_score_tracker(self) -> None:
        player_values = sorted(card[2] for card in self.player_hand)
        player_suits = sorted(card[1] for card in self.player_hand)
        enemy_values = sorted(card[2] for card in self.enemy_hand)
        enemy_suits = sorted(card[1] for card in self.enemy_hand)

        print("DEBUG player_values:", player_values)
        print("DEBUG enemy_values:", enemy_values)
        print("DEBUG player suit:", player_suits)
        print("DEBUG enemy suits:", enemy_suits)

        self.player_hand_type = ""
        self.enemy_hand_type = ""

        royal_values = {10, 11, 12, 13, 14}

        # ---- ROYAL FLUSH CHECK ----
        if not self.player_hand_type and set(card[2] for card in self.player_hand) == royal_values:
            suit = self.player_hand[0][1]
            if all(card[1] == suit for card in self.player_hand):
                self.player_hand_type = "royal_straight_flush"
        if not self.enemy_hand_type and set(card[2] for card in self.enemy_hand) == royal_values:
            suit = self.enemy_hand[0][1]
            if all(card[1] == suit for card in self.enemy_hand):
                self.enemy_hand_type = "royal_straight_flush"

        # ---- STRAIGHT FLUSH CHECK ----
        if not self.player_hand_type:
            player_suit_groups = {}
            for value, suit in ((card[2], card[1]) for card in self.player_hand):
                player_suit_groups.setdefault(suit, []).append(value)
            for suit, values in player_suit_groups.items():
                values = sorted(set(values))
                consecutive = 1
                for i in range(len(values) - 1):
                    if values[i + 1] == values[i] + 1:
                        consecutive += 1
                        if consecutive == 5:
                            self.player_hand_type = "straight_flush"
                            break
                    else:
                        consecutive = 1
                if self.player_hand_type:
                    break

        if not self.enemy_hand_type:
            enemy_suit_groups = {}
            for value, suit in ((card[2], card[1]) for card in self.enemy_hand):
                enemy_suit_groups.setdefault(suit, []).append(value)
            for suit, values in enemy_suit_groups.items():
                values = sorted(set(values))
                consecutive = 1
                for i in range(len(values) - 1):
                    if values[i + 1] == values[i] + 1:
                        consecutive += 1
                        if consecutive == 5:
                            self.enemy_hand_type = "straight_flush"
                            break
                    else:
                        consecutive = 1
                if self.enemy_hand_type:
                    break

        # ---- FOUR OF A KIND ----
        player_ranks = [card[0] for card in self.player_hand]
        player_rank_counts = {rank: player_ranks.count(rank) for rank in set(player_ranks)}
        if not self.player_hand_type and 4 in player_rank_counts.values():
            self.player_hand_type = "four_of_a_kind"

        enemy_ranks = [card[0] for card in self.enemy_hand]
        enemy_rank_counts = {rank: enemy_ranks.count(rank) for rank in set(enemy_ranks)}
        if not self.enemy_hand_type and 4 in enemy_rank_counts.values():
            self.enemy_hand_type = "four_of_a_kind"

        # ---- FULL HOUSE ----
        if not self.player_hand_type and 3 in player_rank_counts.values() and 2 in player_rank_counts.values():
            self.player_hand_type = "full_house"
        if not self.enemy_hand_type and 3 in enemy_rank_counts.values() and 2 in enemy_rank_counts.values():
            self.enemy_hand_type = "full_house"

        # ---- FLUSH ----
        if not self.player_hand_type and any(player_suits.count(suit) >= 5 for suit in set(player_suits)):
            self.player_hand_type = "flush"
        if not self.enemy_hand_type and any(enemy_suits.count(suit) >= 5 for suit in set(enemy_suits)):
            self.enemy_hand_type = "flush"

        # ---- STRAIGHT ----
        if not self.player_hand_type:
            consecutive = 1
            for i in range(len(player_values) - 1):
                if player_values[i + 1] == player_values[i] + 1:
                    consecutive += 1
                    if consecutive == 5:
                        self.player_hand_type = "straight"
                        break
                else:
                    consecutive = 1

        if not self.enemy_hand_type:
            consecutive = 1
            for i in range(len(enemy_values) - 1):
                if enemy_values[i + 1] == enemy_values[i] + 1:
                    consecutive += 1
                    if consecutive == 5:
                        self.enemy_hand_type = "straight"
                        break
                else:
                    consecutive = 1

        # ---- PAIR/TRIPS ----
        if not self.player_hand_type:
            if 3 in player_rank_counts.values():
                self.player_hand_type = "three_of_a_kind"
            elif list(player_rank_counts.values()).count(2) == 2:
                self.player_hand_type = "two_pair"
            elif 2 in player_rank_counts.values():
                self.player_hand_type = "one_pair"

        if not self.enemy_hand_type:
            if 3 in enemy_rank_counts.values():
                self.enemy_hand_type = "three_of_a_kind"
            elif list(enemy_rank_counts.values()).count(2) == 2:
                self.enemy_hand_type = "two_pair"
            elif 2 in enemy_rank_counts.values():
                self.enemy_hand_type = "one_pair"

        if not self.player_hand_type:
            self.player_hand_type = "no_hand"
        if not self.enemy_hand_type:
            self.enemy_hand_type = "no_hand"

        print(f"Player has: {self.player_hand_type.replace('_', ' ').title()}")
        print(f"Enemy has: {self.enemy_hand_type.replace('_', ' ').title()}")
        # player_score = self.get_hand_score(self.player_hand_type)
        # enemy_score = self.get_hand_score(self.enemy_hand_type)
        player_score = self.get_hand_score(self.player_hand_type)
        enemy_score = self.get_hand_score(self.enemy_hand_type)

        if self.player_hand_type == self.enemy_hand_type:
            player_score += self.get_bonus_score_if_tied(self.player_hand_type, self.player_hand)
            enemy_score += self.get_bonus_score_if_tied(self.enemy_hand_type, self.enemy_hand)
        print(f"Player score: {player_score}")
        print(f"Enemy score: {enemy_score}")
        self.enemy_hand_bet_strength = enemy_score

    ## def #generate_dummy_hand(self, index: int) -> list[tuple[str, str, int]]:#
    #     #dummy_enemy_hands = [#
    #         [("9", "Hearts", 9), ("9", "Spades", 9), ("2", "Clubs", 2)],        # One Pair
    #         [("5", "Diamonds", 5), ("5", "Clubs", 5), ("5", "Hearts", 5)],      # Three of a Kind
    #         [("10", "Hearts", 10), ("Jack", "Spades", 11), ("Queen", "Clubs", 12)],  # No Hand
    #         [("2", "Spades", 2), ("2", "Hearts", 2), ("3", "Clubs", 3)],        # Three of a Kind
    #         [("7", "Diamonds", 7), ("7", "Clubs", 7), ("9", "Hearts", 9)],      # One Pair
    #
    #         [("9", "Hearts", 9), ("4", "Spades", 4), ("2", "Clubs", 2)],  # All junk → discard 2, keep high card
    #         [("King", "Hearts", 13), ("3", "Spades", 3), ("5", "Clubs", 5)],  # No hand, keep King only
    #         [("10", "Hearts", 10), ("2", "Diamonds", 2), ("7", "Clubs", 7)],  # No sequence, no pair, keep 10
    #         [("Jack", "Spades", 11), ("3", "Hearts", 3), ("5", "Diamonds", 5)],  # Only high card valuable
    #         [("8", "Clubs", 8), ("4", "Diamonds", 4), ("6", "Hearts", 6)],  # Spread too far for straight, no match
    #         # One Pair, all Hearts (second Hearts case)
    #
    #         [("5", "Hearts", 5), ("8", "Clubs", 8), ("9", "Diamonds", 9)],  # ❌ diff = 2 → discard allowed
    #         [("4", "Spades", 4), ("7", "Hearts", 7), ("9", "Clubs", 9)],  # ❌ 4 too far from 7/9
    #         [("6", "Diamonds", 6), ("9", "Spades", 9), ("10", "Hearts", 10)],  # ❌ 6 is far from 9/10
    #         [("3", "Hearts", 3), ("6", "Clubs", 6), ("7", "Diamonds", 7)],  # ❌ 3 too far from 6/7
    #         [("5", "Spades", 5), ("7", "Hearts", 7), ("8", "Diamonds", 8)]
    #         # ✅ 7-8 close, 5 is borderline → prevent discard
    #         # ✅ 5-7 close, but Queen invalidates sequence
    #
    #
    #
    #     ]
    #     return dummy_enemy_hands[index % len(dummy_enemy_hands)]  # Cycle if limit > length

    def reveal_future_cards(self, state):
        # Print initial top 6 cards
        print("Initial top 6 cards of deck:")
        for i in range(min(6, len(self.deck.poker_cards))):
            print(self.deck.poker_cards[-(i+1)])
        print("\n")

        # Draw 4 cards and store them
        self.future_cards_container = self.deck.poker_enemy_draw_hand(4)

        print("Initial 4 drawn cards:")
        for card in self.future_cards_container:
            print(card)
        print("\n")

        # Shuffle the drawn cards
        random.shuffle(self.future_cards_container)

        print("4 cards after shuffling:")
        for card in self.future_cards_container:
            print(card)
        print("\n")

        # Place the shuffled cards back on top of the deck
        for card in reversed(self.future_cards_container):
            self.deck.poker_cards.append(card)

        print("Top 6 cards after placing shuffled cards on deck:")
        for i in range(min(6, len(self.deck.poker_cards))):
            print(self.deck.poker_cards[-(i+1)])

    def enemy_discard_logic(self, index: int = 0, limit: int = 1):
        if index >= limit:
            print("All tests complete.")
            return

        original_hand = self.enemy_hand
        self.enemy_hand = original_hand.copy()
        self.enemy_temp_discard_storage.clear()

        self.poker_score_tracker()
        original_type = self.enemy_hand_type

        print(f"\nTest #{index + 1}")
        print(f"Starting enemy hand: {[c[2] for c in self.enemy_hand]} (Type: {original_type})")

        values = sorted([card[2] for card in self.enemy_hand])
        if values[-1] - values[0] <= 3 and min(values) >= 4 and max(values) <= 12:
            print("Cards are close together and mid-range. Potential for flush or straight. No discard will occur.")
            print(f"This is your hand and we are moving on: {[c[2] for c in self.enemy_hand]}\n")
            self.enemy_discard_logic(index + 1, limit)
            return

        suits = [card[1] for card in self.enemy_hand]
        if all(suit == suits[0] for suit in suits):
            print("All cards are the same suit. No discard will occur.")
            print(f"This is your hand and we are moving on: {[c[2] for c in self.enemy_hand]}\n")
            self.enemy_discard_logic(index + 1, limit)
            return

        valid_discard_indexes = []
        for i, card in enumerate(original_hand):
            temp_hand = original_hand[:i] + original_hand[i + 1:]
            self.enemy_hand = temp_hand.copy()
            self.poker_score_tracker()
            if self.enemy_hand_type == original_type:
                valid_discard_indexes.append(i)

        # Apply valid discards safely (max 2)
        if valid_discard_indexes:
            for i in sorted(valid_discard_indexes[:2], reverse=True):
                self.enemy_temp_discard_storage.append(original_hand[i])
            self.enemy_hand = [card for j, card in enumerate(original_hand) if j not in valid_discard_indexes[:2]]
            print(f"Valid discards: {[original_hand[i] for i in valid_discard_indexes[:2]]}")
            print(f"Enemy hand after discard: {[c[2] for c in self.enemy_hand]}")
            print(f"Discard pile: {[c[2] for c in self.enemy_temp_discard_storage]}")
        else:
            print("No discardable card found that preserves the hand type.")

        print(f"This is your hand and we are moving on: {[c[2] for c in self.enemy_hand]}\n")
        self.enemy_discard_logic(index + 1, limit)

    def draw_bet_screen_info(self, state: 'GameState'):
        # Draw a box showing current bet amount and options
        box_width_offset = 10
        horizontal_padding = 25
        vertical_position = 240
        text_x_offset = 60
        text_y_offset = 15
        black_box_width = 200 - box_width_offset
        black_box_height = 150
        border_width = 5
        start_x_right_box = state.DISPLAY.get_width() - black_box_width - horizontal_padding
        start_y_right_box = vertical_position

        # Create and draw the black box with white border
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
            y_position = start_y_right_box + idx * spacing_between_choices
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )

        # Check if player has the required magic for poker
        # if Magic.BLUFFALO.value not in state.player.magicinventory and Magic.INFLICT_HEAT.value not in state.player.magicinventory:
        #     self.magic_lock = True
        #     self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        # elif Magic.BLUFFALO.value in state.player.magicinventory or Magic.INFLICT_HEAT.value in state.player.magicinventory:
        #     self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC
        #
        # # Add available magic to the magic menu options
        # if Magic.BLUFFALO.value in state.player.magicinventory and Magic.BLUFFALO.value not in self.magic_menu_options:
        #     self.magic_menu_options.append(Magic.BLUFFALO.value)
        #
        # if Magic.INFLICT_HEAT.value in state.player.magicinventory and Magic.INFLICT_HEAT.value not in self.magic_menu_options:
        #     self.magic_menu_options.append(Magic.INFLICT_HEAT.value)

        # Add BACK option to magic menu if not already there
        if "Back" not in self.magic_menu_options:
            self.magic_menu_options.append("Back")

        # Update magic menu based on lock status
        if self.magic_lock == True:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        elif self.magic_lock == False:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

        # Draw the selection arrow based on current menu index
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

    def draw_action_screen_box_info(self, state: 'GameState'):
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

        # Display action menu choices
        for idx, choice in enumerate(self.action_menu_choices):
            y_position = start_y_right_box + idx * spacing_between_choices
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )

        # Draw the selection arrow based on current action menu index
        arrow_y_coordinate = start_y_right_box + (self.action_menu_index * spacing_between_choices) + 12
        state.DISPLAY.blit(
            self.font.render("->", True, RED),  # Using RED to make it stand out
            (start_x_right_box + arrow_x_coordinate_padding, arrow_y_coordinate)
        )

    def draw_poker_table(self, state: 'GameState'):
        # Draw the poker table background
        table_color = (0, 100, 0)  # Dark green
        table_rect = pygame.Rect(200, 150, 600, 300)
        pygame.draw.ellipse(state.DISPLAY, table_color, table_rect)

        # Draw table border
        border_color = (139, 69, 19)  # Brown
        pygame.draw.ellipse(state.DISPLAY, border_color, table_rect, 10)

    def draw_player_cards(self, state: 'GameState'):
        # Draw player's cards at the bottom of the table
        if self.player_hand:
            card_width = 80
            card_height = 120
            card_spacing = 20
            start_x = 300
            y_position = 350

            for i, card in enumerate(self.player_hand):
                card_x = start_x + i * (card_width + card_spacing)
                self.draw_card(state, card, card_x, y_position, card_width, card_height)

    def draw_enemy_cards(self, state: 'GameState'):
        # Draw enemy's cards at the top of the table
        if self.enemy_hand:
            card_width = 80
            card_height = 120
            card_spacing = 20
            start_x = 300
            y_position = 130

            for i, card in enumerate(self.enemy_hand):
                card_x = start_x + i * (card_width + card_spacing)
                # Draw cards face down unless they should be revealed
                if self.game_state in [self.FINAL_RESULTS, self.PLAYER_WINS, self.ENEMY_WINS, self.DRAW]:
                    self.draw_card(state, card, card_x, y_position, card_width, card_height)
                else:
                    self.draw_card_back(state, card_x, y_position, card_width, card_height)

    def draw_card(self, state: 'GameState', card, x, y, width, height):
        # Draw a single card
        card_color = (255, 255, 255)  # White
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(state.DISPLAY, card_color, card_rect)
        pygame.draw.rect(state.DISPLAY, (0, 0, 0), card_rect, 2)  # Black border

        # Draw card value and suit
        rank, suit, _ = card
        suit_color = (255, 0, 0) if suit in ["Hearts", "Diamonds"] else (0, 0, 0)  # Red for hearts/diamonds, black for clubs/spades

        # Draw rank at top-left
        state.DISPLAY.blit(
            self.font.render(str(rank), True, suit_color),
            (x + 5, y + 5)
        )

        # Draw suit below rank
        state.DISPLAY.blit(
            self.font.render(suit[0], True, suit_color),  # Just the first letter of the suit
            (x + 5, y + 30)
        )

    def draw_card_back(self, state: 'GameState', x, y, width, height):
        # Draw the back of a card
        back_color = (0, 0, 139)  # Dark blue
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(state.DISPLAY, back_color, card_rect)
        pygame.draw.rect(state.DISPLAY, (0, 0, 0), card_rect, 2)  # Black border

        # Draw a pattern on the back
        pattern_color = (255, 255, 255)  # White
        for i in range(5):
            pygame.draw.line(state.DISPLAY, pattern_color,
                            (x + 10, y + 10 + i * 20),
                            (x + width - 10, y + 10 + i * 20), 2)
            pygame.draw.line(state.DISPLAY, pattern_color,
                            (x + 10 + i * 15, y + 10),
                            (x + 10 + i * 15, y + height - 10), 2)

    def draw_box_info(self, state: 'GameState'):
        player_enemy_box_info_x_position = 37
        enemy_name_y_position = 33
        enemy_pressure_y_position = 70
        enemy_status_y_position = 110
        bet_y_position = 370
        player_money_y_position = 250
        hero_name_y_position = 205
        hero_stamina_y_position = 290
        hero_focus_y_position = 330

        # Draw dealer name
        state.DISPLAY.blit(self.font.render("Poker Darnel", True, WHITE),
                          (player_enemy_box_info_x_position, enemy_name_y_position))

        # Draw enemy money and pressure
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER}: {self.enemy_money}", True, WHITE),
                          (player_enemy_box_info_x_position, enemy_pressure_y_position))

        # Draw enemy status (pressure)
        if self.enemy_pressure > 0:
            state.DISPLAY.blit(self.font.render(f"Pressure: {self.enemy_pressure}", True, RED),
                              (player_enemy_box_info_x_position, enemy_status_y_position))
        else:
            state.DISPLAY.blit(self.font.render(f"{self.STATUS_GREEN}", True, WHITE),
                              (player_enemy_box_info_x_position, enemy_status_y_position))

        # Draw bet amount
        state.DISPLAY.blit(self.font.render(f"{self.BET_HEADER}: {self.bet}", True, WHITE),
                          (player_enemy_box_info_x_position, bet_y_position))

        # Draw player money
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER}: {state.player.money}", True, WHITE),
                          (player_enemy_box_info_x_position, player_money_y_position))

        # Draw player stats
        state.DISPLAY.blit(self.font.render(f"{self.HP_HEADER}: {state.player.stamina_points}", True, WHITE),
                          (player_enemy_box_info_x_position, hero_stamina_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MP_HEADER}: {state.player.focus_points}", True, WHITE),
                          (player_enemy_box_info_x_position, hero_focus_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.HERO_HEADER}", True, WHITE),
                          (player_enemy_box_info_x_position, hero_name_y_position))

    def draw_player_discard_screen_box_info(self, state: 'GameState'):
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

        # Define the choices for the player discard screen
        player_discard_choices = ["Play", "Redraw"]

        # Add card options if they exist
        # for i, card in enumerate(self.player_hand):
        #     player_discard_choices.append(f"Card {i+1}: {card[0]} of {card[1]}")

        # Draw the choices
        for idx, choice in enumerate(player_discard_choices):
            y_position = start_y_right_box + idx * spacing_between_choices
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )

        # Draw the selection arrow based on current menu index
        arrow_y_position = start_y_right_box + self.player_redraw_menu_index * spacing_between_choices + text_y_offset
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_coordinate_padding, arrow_y_position)
        )

        # # Draw card discard index indicator
        # if len(self.player_hand) > 0:
        #     card_indicator_y = start_y_right_box + 120  # Position below the menu options
        #     state.DISPLAY.blit(
        #         self.font.render("Card Selection (Left/Right):", True, WHITE),
        #         (start_x_right_box, card_indicator_y)
        #     )
        #
        #     # Draw indicators for each card
        #     for i in range(3):
        #         card_x = start_x_right_box + i * 60 + 20
        #         card_y = card_indicator_y + 30
        #
        #         # Highlight the selected card
        #         if i == self.player_card_discard_index:
        #             # Draw a highlighted box for the selected card
        #             highlight_rect = pygame.Rect(card_x - 5, card_y - 5, 50, 30)
        #             pygame.draw.rect(state.DISPLAY, RED, highlight_rect, 2)
        #
        #         # Draw card number
        #         state.DISPLAY.blit(
        #             self.font.render(f"Card {i+1}", True, WHITE),
        #             (card_x, card_y)
        #         )

    def draw_hands(self, player_hand: list, enemy_hand: list):
        initial_x_position = 250
        player_target_y_position = 300
        enemy_target_y_position = 50
        move_card_x = 75
        flip_y_position = 145
        deck = self.deck
        display = DISPLAY

        for i, card in enumerate(player_hand):
            player_x_position = initial_x_position + i * move_card_x
            player_y_position = player_target_y_position

            if i == 1 and player_y_position >= flip_y_position:
                deck.draw_card_face_up(card[1], card[0], (player_x_position,
                                                          player_y_position), display)
            else:
                deck.draw_card_face_up(card[1], card[0], (player_x_position,
                                                          player_y_position), display)

            # Draw a red square around the selected card when in the PLAYER_DISCARD_SCREEN state
            if self.game_state == self.PLAYER_DISCARD_SCREEN and i == self.player_card_discard_index:
                # Create a rectangle around the card with a 2-pixel border
                card_rect = pygame.Rect(player_x_position - 2, player_y_position - 2,
                                       deck.card_width + 4, deck.card_height + 4)
                pygame.draw.rect(display, RED, card_rect, 2)

        for i, card in enumerate(enemy_hand):
            enemy_x_position = initial_x_position + i * move_card_x
            enemy_y_position = enemy_target_y_position


            deck.draw_card_face_up(card[1], card[0], (enemy_x_position, enemy_y_position), display)
