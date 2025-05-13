import pygame

from deck import Deck
from entity.gui.screen.gamble_screen import GambleScreen
from game_constants.magic import Magic
from tests.test_poker_darnel import test_poker_score_tracker
from types import *
import random


class PokerDarnel(GambleScreen):
    def __init__(self, screenName: str = "poker_darnel"):
        super().__init__(screenName)
        self.deck = Deck()
        self.deck.poker_cards_shuffle()


        self.last_screen_check_time = pygame.time.get_ticks()
        self.enemy_cards_swap_container = []
        self.player_cards_swap_container = []
        self.swap_player_cards: bool = False
        self.swap_enemy_cards: bool = True
        self.magic_menu_index: int = 0
        self.money: int = 1000
        self.enemy_compare_hand: str = ""
        self.enemy_temp_discard_storage: list = []
        self.player_hand_type = ""
        self.enemy_hand_type = ""
        self.player_bet: int = 50
        self.enemy_bet: int = 50
        self.player_redraw_menu_index = 0
        self.player_card_garbage_can = []
        self.add_player_bet: int = 0
        self.add_enemy_bet:int = 0
        self.action_menu_index: int = 0
        self.future_cards_container: list = []
        self.magic_menu_options: list = []
        self.swap_cards_menu_options: list = []
        self.swap_cards_menu_index: int = 0
        self.enemy_bet_heat: int = 0
        self.enemy_hand_bet_strength: int = 0


        self.game_state = self.WELCOME_SCREEN



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


    DEAL_CARDS_SCREEN: str = "deal_cards_screen"
    PLAYER_REDRAW_SCREEN: str = "player_redraw_screen"
    PLAYER_DISCARD_SCREEN: str = "player_discard_screen"
    ENEMY_REDRAW_SCREEN: str = "enemy_redraw_screen"
    ENEMY_DISCARD_SCREEN: str = "enemy_discard_screen"
    REVEAL_FUTURE_CARDS: str = "reveal_future_cards"
    DRAW_ONE_CARD: str = "draw_one_card"
    FIFTH_ROUND_SHOW: str = "fifth_round_show"
    FIFTH_ROUND_DEAL: str = "fifth_round_deal"
    FINAL_RESULTS: str = "final_results"
    PLAYER_WINS: str = "player_wins"
    ENEMY_WINS: str = "enemy_wins"
    DRAW: str = "draw"
    ACTION_SCREEN: str = "action_screen"
    RESET: str = "reset"
    ENEMY_ACTION_SCREEN: str = "enemy action screen"




    def start(self):
        print("Pew")

    def restart_poker_round(self):
        self.enemy_cards_swap_container = []
        self.player_cards_swap_container = []
        self.swap_player_cards: bool = False
        self.swap_enemy_cards: bool = True
        self.magic_menu_index: int = 0
        self.player_bet: int = 50
        self.enemy_bet: int = 50
        self.player_redraw_menu_index = 0
        self.player_card_garbage_can = []
        self.add_player_bet: int = 0
        self.add_enemy_bet: int = 0
        self.deck.poker_cards_shuffle()


    def update(self, state):
        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)

        current_time = pygame.time.get_ticks()
        if current_time - self.last_screen_check_time >= 7000:
            self.poker_score_tracker()

            print(f"Current screen: {self.game_state}")
            print("ENEMY HAND TYPE: " + str(self.enemy_hand_type))
            print(f"PLAYER HAND: {self.player_hand}")
            print(f"ENEMY HAND: {self.enemy_hand}")

            self.last_screen_check_time = current_time

        if Magic.POKER_CARD_SWAP.value in state.player.magicinventory and Magic.POKER_CARD_SWAP.value not in self.magic_menu_options:
                self.magic_menu_options.append(Magic.POKER_CARD_SWAP.value)
                self.magic_menu_options.append("Back")

        #BLUFF command should have a weight that over time grows the more money diff there is

        if self.game_state == self.WELCOME_SCREEN:
            # print("Hi welcome to the welcome screen press T to start")

            if state.controller.confirm_button:
                print("Player money is: " + str(state.player.money))
                self.game_state = self.DEAL_CARDS_SCREEN
        elif self.game_state == self.BET_SCREEN:
            if state.controller.up_button:
                if self.add_player_bet + 25 <= 100:  # Check if adding 25 won't exceed max
                    self.add_player_bet += 25
                    print(f"Bet increased to: {self.add_player_bet}")

            elif state.controller.down_button:
                if self.add_player_bet - 25 >= 25:  # Check if subtracting 25 won't go below min
                    self.add_player_bet -= 25
                    print(f"Bet decreased to: {self.add_player_bet}")

            # Ensure bet stays within valid range
            if self.add_player_bet < 25:
                self.add_player_bet = 25
            elif self.add_player_bet > 100:
                self.add_player_bet = 100

            # Ensure bet doesn't exceed player's money
            if self.add_player_bet > state.player.money:
                self.add_player_bet = (state.player.money // 25) * 25  # Round down to nearest 25
                if self.add_player_bet < 0:  # If player has less than minimum bet
                    self.add_player_bet = 0  # Or handle insufficient funds cas

            if state.controller.confirm_button:
                self.player_bet += self.add_player_bet
                print("How much will you add?" + str(self.add_player_bet))
                print("Your total bet amount" + str(self.player_bet))
                self.add_player_bet = 0


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
            if state.controller.confirm_button:

                self.player_hand = self.deck.poker_player_draw_hand(3)
                self.enemy_hand = self.deck.poker_enemy_draw_hand(3)
                print("Player hand:" + str(self.player_hand))
                print("Enemy hand" + str(self.enemy_hand))

                self.game_state = self.PLAYER_DISCARD_SCREEN

            # First we dela out 3 cards, players can fold/hold
            # 4th round we show cards , then shuffle and deal
            # 5th round is the same
        elif self.game_state == self.PLAYER_DISCARD_SCREEN:
            # Initialize index if not already set
            if state.controller.up_button:
                # Move up with wraparound
                self.player_redraw_menu_index = (self.player_redraw_menu_index - 1) % 5
                # Print current selection based on index
                if self.player_redraw_menu_index == 0:
                    print("Play selected")
                elif self.player_redraw_menu_index == 1:
                    print("Redraw selected")
                else:
                    print(f"Card {self.player_redraw_menu_index - 1} selected: {self.player_hand[self.player_redraw_menu_index - 2]}")

            elif state.controller.down_button:

                # Move down with wraparound
                self.player_redraw_menu_index = (self.player_redraw_menu_index + 1) % 5
                # Print current selection based on index
                if self.player_redraw_menu_index == 0:
                    print("Play selected")
                elif self.player_redraw_menu_index == 1:
                    print("Redraw selected")
                else:
                    print(f"Card {self.player_redraw_menu_index - 1} selected: {self.player_hand[self.player_redraw_menu_index - 2]}")

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

                elif self.player_redraw_menu_index == 2:
                    if len(self.player_card_garbage_can) < 2 and self.player_hand[0] not in self.player_card_garbage_can:
                        print("place card selected is: " + str(self.player_hand[0]))
                        self.player_card_garbage_can.append(self.player_hand[0])
                        print("your trash can contents" + str(self.player_card_garbage_can))
                    else:
                        print("Cannot discard more cards or this card is already in the discard pile")
                elif self.player_redraw_menu_index == 3:
                    if len(self.player_card_garbage_can) < 2 and self.player_hand[1] not in self.player_card_garbage_can:
                        print("place card selected is: " + str(self.player_hand[1]))
                        self.player_card_garbage_can.append(self.player_hand[1])
                        print("your trash can contents" + str(self.player_card_garbage_can))
                    else:
                        print("Cannot discard more cards or this card is already in the discard pile")
                elif self.player_redraw_menu_index == 4:
                    if len(self.player_card_garbage_can) < 2 and self.player_hand[2] not in self.player_card_garbage_can:
                        print("place card selected is: " + str(self.player_hand[2]))
                        self.player_card_garbage_can.append(self.player_hand[2])
                        print("your trash can contents" + str(self.player_card_garbage_can))
                    else:
                        print("Cannot discard more cards or this card is already in the discard pile")



            elif state.controller.action_and_cancel_button:
                if self.player_redraw_menu_index == 2 and self.player_hand[0] in self.player_card_garbage_can:
                    self.player_card_garbage_can.remove(self.player_hand[0])
                    print(f"Removed first card from discard pile: {self.player_hand[0]}")
                elif self.player_redraw_menu_index == 3 and self.player_hand[1] in self.player_card_garbage_can:
                    self.player_card_garbage_can.remove(self.player_hand[1])
                    print(f"Removed second card from discard pile: {self.player_hand[1]}")
                elif self.player_redraw_menu_index == 4 and self.player_hand[2] in self.player_card_garbage_can:
                    self.player_card_garbage_can.remove(self.player_hand[2])
                    print(f"Removed third card from discard pile: {self.player_hand[2]}")


        elif self.game_state == self.PLAYER_REDRAW_SCREEN:
            while len(self.player_hand) < 3:
                drawn_card = self.deck.poker_get_next_card()
                self.player_hand.append(drawn_card)
                print(f"Drew card: {drawn_card}")
                print("your player hand" + str(self.player_hand))
                if state.controller.confirm_button:
                    self.game_state = self.ENEMY_DISCARD_SCREEN

        elif self.game_state == self.ENEMY_DISCARD_SCREEN:
            # print("enemey ")
            if  state.controller.confirm_button:
                self.enemy_discard_logic()
                self.game_state = self.ENEMY_REDRAW_SCREEN
                # self.poker_score_tracker()

        elif self.game_state == self.ENEMY_REDRAW_SCREEN:
            while len(self.enemy_hand) < 3:
                drawn_card = self.deck.poker_get_next_card()
                self.enemy_hand.append(drawn_card)
                print(f"Drew card: {drawn_card}")
                print("your enemy hand" + str(self.enemy_hand))
            if state.controller.confirm_button:
                self.game_state = self.ACTION_SCREEN


        elif self.game_state == self.ACTION_SCREEN:
            if state.controller.up_button:
                self.action_menu_index = (self.action_menu_index + 1) % 5
                print("the action menu index is: " + str(self.action_menu_index))
            elif state.controller.down_button:
                self.action_menu_index = (self.action_menu_index - 1) % 5
                print("the action menu index is: " + str(self.action_menu_index))

            if state.controller.confirm_button:
                if self.action_menu_index == 0:
                    if len(self.player_hand) == 3:
                        self.game_state = self.REVEAL_FUTURE_CARDS
                    elif len(self.player_hand) < 5:
                        self.game_state = self.DRAW_ONE_CARD
                    elif len(self.player_hand) == 5:
                        self.game_state = self.FINAL_RESULTS


                elif self.action_menu_index == 1:
                    print("time to bluffallo")
                elif self.action_menu_index == 2:
                    print("time to cast a spell card swap")
                    self.game_state = self.MAGIC_MENU_SCREEN
                elif self.action_menu_index == 3:
                    print("time to place your bet")
                    self.game_state = self.BET_SCREEN
                elif self.action_menu_index == 4:
                    print("time to fold")
                    print("Player money is now: " + str(state.player.money))
                    state.player.money -= self.player_bet
                    print("Player money is now: " + str(state.player.money))

                    self.restart_poker_round()


                    self.game_state = self.WELCOME_SCREEN

        elif self.game_state == self.ENEMY_ACTION_SCREEN:
            pass


        elif self.game_state == self.REVEAL_FUTURE_CARDS:
            if state.controller.confirm_button:
                self.reveal_future_cards()
                self.game_state = self.DRAW_ONE_CARD


        elif self.game_state == self.DRAW_ONE_CARD:

            if state.controller.confirm_button:

                drawn_card = self.deck.poker_get_next_card()
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

                # Move to next game state after drawing
                self.game_state = self.ACTION_SCREEN




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
        elif self.game_state == self.ENEMY_WINS:
            print("ENEMY WINS")
        elif self.game_state == self.DRAW:
            print("Draw")


    def draw(self, state):
        super().draw(state)

        if self.game_state == self.WELCOME_SCREEN:
            pass
        elif self.game_state == self.BET_SCREEN:
            pass
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            pass
        elif self.game_state == self.DEAL_CARDS_SCREEN:
            pass
            # First we dela out 3 cards, players can fold/hold
            # 4th round we show cards , then shuffle and deal
            # 5th round is the same
        elif self.game_state == self.PLAYER_REDRAW_SCREEN:
            pass

        elif self.game_state == self.PLAYER_DISCARD_SCREEN:
            pass
        elif self.game_state == self.ENEMY_DISCARD_SCREEN:
            pass

        elif self.game_state == self.ENEMY_REDRAW_SCREEN:
            pass
        elif self.game_state == self.ACTION_SCREEN:
            pass
        elif self.game_state == self.REVEAL_FUTURE_CARDS:
            pass

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

    def reveal_future_cards(self):
        # Print initial top 6 cards
        print("Initial top 6 cards of deck:")
        for i in range(min(6, len(self.deck.poker_cards))):
            print(self.deck.poker_cards[-(i+1)])
        print("\n")

        # Draw 4 cards and store them
        self.future_cards_container = self.deck.poker_player_draw_hand(4)

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

