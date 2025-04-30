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
        # --- PLAYER CHECK ---
        player_values = sorted(card[2] for card in self.player_hand)
        print("DEBUG player_values:", player_values)

        player_hand_type = "no_hand"
        consecutive_count = 1

        for i in range(len(player_values) - 1):
            print("fd;slkjfl;dsajfljsal;fjlsajfl;sjf;lsajfsafj;saf")

            print(f"Comparing {player_values[i]} to {player_values[i + 1]}")
            if player_values[i + 1] == player_values[i] + 1:
                consecutive_count += 1
                print("Consecutive count is now:", consecutive_count)
                if consecutive_count == 5:
                    player_hand_type = "straight"
                    print("✅ STRAIGHT DETECTED")
                    break
            else:
                consecutive_count = 1

        player_value_counts = {value: player_values.count(value) for value in set(player_values)}
        if player_hand_type == "no_hand":
            if 3 in player_value_counts.values():
                player_hand_type = "three_of_a_kind"
            elif list(player_value_counts.values()).count(2) == 2:
                player_hand_type = "two_pair"
            elif 2 in player_value_counts.values():
                player_hand_type = "one_pair"

        match player_hand_type:
            case "straight":
                print("You have a Straight!")
            case "three_of_a_kind":
                print("You have Three of a Kind!")
            case "two_pair":
                print("You have Two Pair!")
            case "one_pair":
                print("You have One Pair!")
            case "no_hand":
                print("You have No Hand.")




