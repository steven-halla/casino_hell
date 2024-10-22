import pygame

from entity.gui.screen.gamble_screen import GambleScreen


class DiceFighterSirSiegfried(GambleScreen):
    def __init__(self, screenName: str = "Coin FLip") -> None:
        super().__init__(screenName)
        self.bet = 100
        self.bet_stepper = 50
        self.dealer_name: str = "Sir Siegfried"
        self.blit_message_x: int = 65
        self.blit_message_y: int = 460
        self.game_state: str = self.WELCOME_SCREEN
        self.welcome_screen_choices: list[str] = ["Play", "Magic", "Bet", "Quit"]
        self.magic_menu_selector: list[str] = []
        self.menu_movement_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)
        self.spell_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)


    BACK: str = "Back"

    RESULTS_SCREEN: str = "results_screen"
    PLAYER_WIN_SCREEN: str = "player_win_screen"
    PLAYER_LOSE_SCREEN: str = "player_lose_screen"

    def start(self):
        pass
    def restart_dice_fighter_game(self):
        pass
    def restart_dice_fighter_round(self):
        pass

    def update(self, state):
        pass
    def draw(self, state):
        pass






