import pygame

from deck import Deck
from entity.gui.screen.gamble_screen import GambleScreen


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
        self.player_hand: list[tuple[str, str, int]] = [
            ("Queen", "Clubs", 10),
            ("Queen", "Diamonds", 10),
            ("3", "Spades", 3),
            ("7", "Hearts", 7),
            ("Jack", "Spades", 10)
        ]

        self.enemy_hand: list[tuple[str, str, int]] = [
            ("5", "Hearts", 5),
            ("5", "Spades", 5),
            ("2", "Clubs", 2),
            ("9", "Diamonds", 9),
            ("King", "Hearts", 10)
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

    def poker_score_tracker(self) -> None:
        player_ranks = [player_card[0] for player_card in self.player_hand]
        player_rank_counts = {player_rank: player_ranks.count(player_rank) for player_rank in set(player_ranks)}

        if 2 in player_rank_counts.values():
            for player_rank, player_count in player_rank_counts.items():
                if player_count == 2:
                    print(f"You have a Pair of {player_rank}s!")
                    break

            print("Your full hand for player: ")
            for player_card in self.player_hand:
                print(f"{player_card[0]} of {player_card[1]}")

        enemy_ranks = [enemy_card[0] for enemy_card in self.enemy_hand]
        enemy_rank_counts = {enemy_rank: enemy_ranks.count(enemy_rank) for enemy_rank in set(enemy_ranks)}

        if 2 in enemy_rank_counts.values():
            for enemy_rank, enemy_count in enemy_rank_counts.items():
                if enemy_count == 2:
                    print(f"Enemy has a Pair of {enemy_rank}s!")
                    break

            print("Enemy's full hand:")
            for enemy_card in self.enemy_hand:
                print(f"{enemy_card[0]} of {enemy_card[1]}")

        if 2 in player_rank_counts.values() and 2 in enemy_rank_counts.values():
            player_pair_rank = None
            enemy_pair_rank = None

            for player_rank, player_count in player_rank_counts.items():
                if player_count == 2:
                    player_pair_rank = player_rank
                    break

            for enemy_rank, enemy_count in enemy_rank_counts.items():
                if enemy_count == 2:
                    enemy_pair_rank = enemy_rank
                    break

            if self.deck.rank_order_poker[player_pair_rank] > self.deck.rank_order_poker[enemy_pair_rank]:
                print("Player wins with the higher pair!")
            elif self.deck.rank_order_poker[player_pair_rank] < self.deck.rank_order_poker[enemy_pair_rank]:
                print("Enemy wins with the higher pair!")
            else:
                print("Both players have the same pair! It's a draw!")







