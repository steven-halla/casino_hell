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
        self.player_hand: list[tuple[str, str, int]] = [

        ]

        self.enemy_hand: list[tuple[str, str, int]] = [

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
                test_poker_score_tracker()
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
        enemy_ranks = [enemy_card[0] for enemy_card in self.enemy_hand]
        enemy_rank_counts = {enemy_rank: enemy_ranks.count(enemy_rank) for enemy_rank in set(enemy_ranks)}


        player_pair_type = None

        if list(player_rank_counts.values()).count(2) == 2:
            player_pair_type = "two_pair"
        elif 2 in player_rank_counts.values():
            player_pair_type = "one_pair"

        match player_pair_type:
            case "two_pair":
                player_two_pairs = []
                for player_rank, player_count in player_rank_counts.items():
                    if player_count == 2:
                        player_two_pairs.append(player_rank)
                print(f"You have Two Pair: {player_two_pairs[0]}s and {player_two_pairs[1]}s!")
                print("Your full hand for player:")
                for player_card in self.player_hand:
                    print(f"{player_card[0]} of {player_card[1]}")

            case "one_pair":
                for player_rank, player_count in player_rank_counts.items():
                    if player_count == 2:
                        print(f"You have a Pair of {player_rank}s!")
                        break
                print("Your full hand for player:")
                for player_card in self.player_hand:
                    print(f"{player_card[0]} of {player_card[1]}")

            case _:
                pass  # No pairs found

        enemy_pair_type = None

        if list(enemy_rank_counts.values()).count(2) == 2:
            enemy_pair_type = "two_pair"
        elif 2 in enemy_rank_counts.values():
            enemy_pair_type = "one_pair"

        match enemy_pair_type:
            case "two_pair":
                enemy_two_pairs = []
                for enemy_rank, enemy_count in enemy_rank_counts.items():
                    if enemy_count == 2:
                        enemy_two_pairs.append(enemy_rank)
                print(f"Enemy has Two Pair: {enemy_two_pairs[0]}s and {enemy_two_pairs[1]}s!")
                print("Enemy's full hand:")
                for enemy_card in self.enemy_hand:
                    print(f"{enemy_card[0]} of {enemy_card[1]}")

            case "one_pair":
                for enemy_rank, enemy_count in enemy_rank_counts.items():
                    if enemy_count == 2:
                        print(f"Enemy has a Pair of {enemy_rank}s!")
                        break
                print("Enemy's full hand:")
                for enemy_card in self.enemy_hand:
                    print(f"{enemy_card[0]} of {enemy_card[1]}")

            case _:
                pass  # No pairs found







