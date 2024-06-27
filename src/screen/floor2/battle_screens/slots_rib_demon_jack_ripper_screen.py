import pygame
from entity.gui.screen.battle_screen import BattleScreen


class SlotsRibDemonJackRipperScreen(BattleScreen):
    def __init__(self):
        super().__init__("Casino Coin Flip Screen")

        self.play_again = True
        self.new_font = pygame.font.Font(None, 36)
        self.game_state = "welcome_screen"
        self.bet = 0
        self.money = 19

    def update(self, state: "GameState"):
        if state.controller.isQPressed:
            # Transition to the main screen
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return

        # Update the controller
        controller = state.controller
        controller.update()

    def draw(self, state: "GameState"):
        super().draw(state)
        # You can add any additional drawing logic specific to SlotsRibDemonJackRipperScreen here
