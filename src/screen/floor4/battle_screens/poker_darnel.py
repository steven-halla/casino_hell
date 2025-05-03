import pygame

from deck import Deck
from entity.gui.screen.gamble_screen import GambleScreen
from tests.test_poker_darnel import test_poker_score_tracker


class PokerDarnel(GambleScreen):
    def __init__(self, screenName: str = "poker_darnel"):
        super().__init__(screenName)
        self.money: int = 1000
        self.player_bet: int = 0
        self.enemy_bet: int = 0
        self.game_state = self.WELCOME_SCREEN
        self.deck = Deck()
        self.player_hand_score: int = 0
        self.player_value_score: int = 0
        self.enemy_hand_score: int = 0
        self.enemy_value_score: int = 0
        # self.player_hand: list[tuple[str, str, int]] = [
        #
        # ]
        #
        # self.enemy_hand: list[tuple[str, str, int]] = [
        #
        # ]
        self.player_hand = [
            ("7", "Hearts", 7),
            ("7", "Clubs", 7),
            ("7", "Diamonds", 7),
            ("2", "Spades", 2),
            ("9", "Hearts", 9),
        ]

        self.enemy_hand = [
            ("5", "Spades", 5),
            ("5", "Hearts", 5),
            ("5", "Diamonds", 5),
            ("3", "Clubs", 3),
            ("Jack", "Spades", 11),
        ]


    DEAL_CARDS_SCREEN: str = "deal_cards_screen"
    FOURTH_ROUND_SHOW: str = "fourth_round_show"
    FOURTH_ROUND_DEAL: str = "fourth_round_deal"
    FIFTH_ROUND_SHOW: str = "fifth_round_show"
    FIFTH_ROUND_DEAL: str = "fifth_round_deal"
    FINAL_RESULTS: str = "final_results"
    PLAYER_WINS: str = "player_wins"
    ENEMY_WINS: str = "enemy_wins"
    DRAW: str = "draw"
    ACTION_SCREEN: str = "action_screen"



    def update(self, state):
        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)

        if self.game_state == self.WELCOME_SCREEN:
            if controller.confirm_button:
                self.poker_score_tracker()

        elif self.game_state == self.BET_SCREEN:
            print("In bet screen")
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            print("Magic screen")
        elif self.game_state == self.DEAL_CARDS_SCREEN:
            print("Dealing cards screen")
            # First we dela out 3 cards, players can fold/hold
            # 4th round we show cards , then shuffle and deal
            # 5th round is the same
        elif self.game_state == self.ACTION_SCREEN:
            print("Action screen")
        elif self.game_state == self.FOURTH_ROUND_SHOW:
            print("showing next cards")
        elif self.game_state == self.FOURTH_ROUND_DEAL:
            print("dealing 4th cards")
        elif self.game_state == self.FIFTH_ROUND_SHOW:
            print("showing next cards 5th round")
        elif self.game_state == self.FIFTH_ROUND_DEAL:
            print("Dealing final cards")
        elif self.game_state == self.FINAL_RESULTS:
            print("final resutls")
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
            print("In bet screen")
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            print("Magic screen")
        elif self.game_state == self.DEAL_CARDS_SCREEN:
            print("Dealing cards screen")
            # First we dela out 3 cards, players can fold/hold
            # 4th round we show cards , then shuffle and deal
            # 5th round is the same
        elif self.game_state == self.ACTION_SCREEN:
            print("Action screen")
        elif self.game_state == self.FOURTH_ROUND_SHOW:
            print("showing next cards")
        elif self.game_state == self.FOURTH_ROUND_DEAL:
            print("dealing 4th cards")
        elif self.game_state == self.FIFTH_ROUND_SHOW:
            print("showing next cards 5th round")
        elif self.game_state == self.FIFTH_ROUND_DEAL:
            print("Dealing final cards")
        elif self.game_state == self.FINAL_RESULTS:
            print("final resutls")
        elif self.game_state == self.PLAYER_WINS:
            print("Player wins ")
        elif self.game_state == self.ENEMY_WINS:
            print("ENEMY WINS")
        elif self.game_state == self.DRAW:
            print("Draw")

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
        for rank, _, _ in hand:
            rank_counts.setdefault(rank, 0)
            rank_counts[rank] += 1

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

        player_hand_type = ""
        enemy_hand_type = ""

        royal_values = {10, 11, 12, 13, 14}

        # ---- ROYAL FLUSH CHECK ----
        if not player_hand_type and set(card[2] for card in self.player_hand) == royal_values:
            suit = self.player_hand[0][1]
            if all(card[1] == suit for card in self.player_hand):
                player_hand_type = "royal_straight_flush"
        if not enemy_hand_type and set(card[2] for card in self.enemy_hand) == royal_values:
            suit = self.enemy_hand[0][1]
            if all(card[1] == suit for card in self.enemy_hand):
                enemy_hand_type = "royal_straight_flush"

        # ---- STRAIGHT FLUSH CHECK ----
        if not player_hand_type:
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
                            player_hand_type = "straight_flush"
                            break
                    else:
                        consecutive = 1
                if player_hand_type:
                    break

        if not enemy_hand_type:
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
                            enemy_hand_type = "straight_flush"
                            break
                    else:
                        consecutive = 1
                if enemy_hand_type:
                    break

        # ---- FOUR OF A KIND ----
        player_ranks = [card[0] for card in self.player_hand]
        player_rank_counts = {rank: player_ranks.count(rank) for rank in set(player_ranks)}
        if not player_hand_type and 4 in player_rank_counts.values():
            player_hand_type = "four_of_a_kind"

        enemy_ranks = [card[0] for card in self.enemy_hand]
        enemy_rank_counts = {rank: enemy_ranks.count(rank) for rank in set(enemy_ranks)}
        if not enemy_hand_type and 4 in enemy_rank_counts.values():
            enemy_hand_type = "four_of_a_kind"

        # ---- FULL HOUSE ----
        if not player_hand_type and 3 in player_rank_counts.values() and 2 in player_rank_counts.values():
            player_hand_type = "full_house"
        if not enemy_hand_type and 3 in enemy_rank_counts.values() and 2 in enemy_rank_counts.values():
            enemy_hand_type = "full_house"

        # ---- FLUSH ----
        if not player_hand_type and any(player_suits.count(suit) >= 5 for suit in set(player_suits)):
            player_hand_type = "flush"
        if not enemy_hand_type and any(enemy_suits.count(suit) >= 5 for suit in set(enemy_suits)):
            enemy_hand_type = "flush"

        # ---- STRAIGHT ----
        if not player_hand_type:
            consecutive = 1
            for i in range(len(player_values) - 1):
                if player_values[i + 1] == player_values[i] + 1:
                    consecutive += 1
                    if consecutive == 5:
                        player_hand_type = "straight"
                        break
                else:
                    consecutive = 1

        if not enemy_hand_type:
            consecutive = 1
            for i in range(len(enemy_values) - 1):
                if enemy_values[i + 1] == enemy_values[i] + 1:
                    consecutive += 1
                    if consecutive == 5:
                        enemy_hand_type = "straight"
                        break
                else:
                    consecutive = 1

        # ---- PAIR/TRIPS ----
        if not player_hand_type:
            if 3 in player_rank_counts.values():
                player_hand_type = "three_of_a_kind"
            elif list(player_rank_counts.values()).count(2) == 2:
                player_hand_type = "two_pair"
            elif 2 in player_rank_counts.values():
                player_hand_type = "one_pair"

        if not enemy_hand_type:
            if 3 in enemy_rank_counts.values():
                enemy_hand_type = "three_of_a_kind"
            elif list(enemy_rank_counts.values()).count(2) == 2:
                enemy_hand_type = "two_pair"
            elif 2 in enemy_rank_counts.values():
                enemy_hand_type = "one_pair"

        if not player_hand_type:
            player_hand_type = "no_hand"
        if not enemy_hand_type:
            enemy_hand_type = "no_hand"

        print(f"Player has: {player_hand_type.replace('_', ' ').title()}")
        print(f"Enemy has: {enemy_hand_type.replace('_', ' ').title()}")
        # player_score = self.get_hand_score(player_hand_type)
        # enemy_score = self.get_hand_score(enemy_hand_type)
        player_score = self.get_hand_score(player_hand_type)
        enemy_score = self.get_hand_score(enemy_hand_type)

        if player_hand_type == enemy_hand_type:
            player_score += self.get_bonus_score_if_tied(player_hand_type, self.player_hand)
            enemy_score += self.get_bonus_score_if_tied(enemy_hand_type, self.enemy_hand)
        print(f"Player score: {player_score}")
        print(f"Enemy score: {enemy_score}")





