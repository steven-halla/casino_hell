from entity.gui.screen.gamble_screen import GambleScreen


class BlackJackAlbertScreen(GambleScreen):
    def __init__(self, screenName: str = "Black Jack") -> None:
        super().__init__(screenName)
        self.game_state: str = self.WELCOME_SCREEN

