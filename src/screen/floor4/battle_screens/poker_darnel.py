import pygame

from deck import Deck
from entity.gui.screen.gamble_screen import GambleScreen


class PokerDarnel(GambleScreen):
    def __init__(self, screenName: str = "poker_darnel"):
        super().__init__(screenName)
        self.money: int = 1000
        self.game_state = self.WELCOME_SCREEN
        deck = Deck()

    DEAL_CARDS_SCREEN: str = "deal_cards_screen"
    FOURTH_ROUND_SHOW: str = "fourth_round_show"
    FOURTH_ROUND_DEAL: str = "fourth_round_deal"
    FIFTH_ROUND_SHOW: str = "fifth_round_show"
    FIFTH_ROUND_DEAL: str = "fifth_round_deal"
    FINAL_RESULTS: str = "final_results"
    PLAYER_WINS: str = "player_wins"
    ENEMY_WINS: str = "enemy_wins"
    DRAW: str = "draw"



    def update(self, state):

        if self.game_state == self.WELCOME_SCREEN:
            print("In welcome screen")
        elif self.game_state == self.BET_SCREEN:
            print("In bet screen")
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            print("Magic screen")
        elif self.game_state == self.DEAL_CARDS_SCREEN:
            print("Dealing cards screen")
            # First we dela out 3 cards, players can fold/hold
            # 4th round we show cards , then shuffle and deal
            # 5th round is the same
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
            print("In welcome screen")
        elif self.game_state == self.BET_SCREEN:
            print("In bet screen")
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            print("Magic screen")
        elif self.game_state == self.DEAL_CARDS_SCREEN:
            print("Dealing cards screen")
            # First we dela out 3 cards, players can fold/hold
            # 4th round we show cards , then shuffle and deal
            # 5th round is the same
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





