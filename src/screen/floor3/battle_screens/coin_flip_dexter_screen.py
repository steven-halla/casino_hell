import random

import pygame

from entity.gui.screen.gamble_screen import GambleScreen
from game_constants.coin_flip_constants import CoinFlipConstants


class CoinFlipDexterScreen(GambleScreen):
    # I believe in the yin yang of coin flip, balance is needed in all things
    def __init__(self, screenName: str = "Coin FLip") -> None:
        super().__init__(screenName)
        self.bet:int = 100
        self.sprite_sheet = pygame.image.load("./assets/images/coin_flipping_alpha.png").convert_alpha()
        self.game_state: str = self.WELCOME_SCREEN
        self.welcome_screen_choices: list[str] = ["Play", "Magic", "Bet", "Quit"]
        self.heads_or_tails_Menu: list[str] = ["Heads", "Tails", "Back"]
        self.magic_menu_selector: list[str] = ["Back"]
        self.welcome_screen_index: int = 0
        self.spell_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.phase = 1

        self.menu_movement_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)
        self.weighted_coin: bool = False  # this is our magic spell heads force
        self.balance_modifier: int = 0
        self.player_choice = CoinFlipConstants.HEADS.value
        self.coin_landed = CoinFlipConstants.HEADS.value


    def reset_coin_flip_game(self):
        self.phase = 1
        self.weighted_coin = False
        self.balance_modifier: int = 0

        self.welcome_screen_index = 0


    def reset_round(self):
        self.weighted_coin = False
        self.phase += 1
        if self.phase == 6:
            self.phase = 1
        if self.phase == 1:
            self.balance_modifier = 0


    def flip_coin(self):
        if self.weighted_coin == True:
            self.balance_modifier += 15
            self.coin_landed = CoinFlipConstants.HEADS.value
        coin_fate = random.randint(1, 100) + self.balance_modifier
        if coin_fate >= 51:
            self.balance_modifier += 15
            if self.balance_modifier >= 85:
                self.balance_modifier -= 125
            self.coin_landed = CoinFlipConstants.HEADS.value
        elif coin_fate <= 50:
            self.balance_modifier -= 15
            if self.balance_modifier <= 15:
                self.balance_modifier += 125
            self.coin_landed = CoinFlipConstants.TAILS.value

    def update(self, state):
        super().update(state)
        pass

    def draw(self, state: 'GameState'):
        super().draw(state)

        # Draw the coin image
        self.draw_coin_image(state)

        pygame.display.flip()  # Update the display with the drawn content

    def draw_coin_image(self, state: 'GameState'):
        # Fixed position to draw the coin on the screen
        initial_coin_image_position = (300, 1)  # Starting position on the screen for the coin

        # List of predefined x-positions for each coin in the sprite sheet
        x_positions = [85, 235, 380, 525, 670, 815, 960, 1108, 1250, 1394]
        y_position = 110  # Fixed y-coordinate for all coins in the sprite sheet
        width, height = 170, 190  # Size of each coin in the sprite sheet

        # Parameters for the animation
        time_interval = 50  # Time interval in milliseconds for changing images
        fall_speed = 3 # Fall speed in pixels per time interval

        # Determine which coin to display based on time
        current_time = pygame.time.get_ticks()
        current_coin_index = (current_time // time_interval) % len(x_positions)

        # Define the rectangle for the current coin in the sprite sheet
        subsurface_rect = pygame.Rect(x_positions[current_coin_index], y_position, width, height)

        # Get the subsurface from the sprite sheet
        sprite = self.sprite_sheet.subsurface(subsurface_rect)

        # Calculate the y position as the coin falls
        fall_distance = min(fall_speed * (current_time // time_interval), 200)  # Fall up to a maximum of 100 pixels
        coin_image_position = (initial_coin_image_position[0], initial_coin_image_position[1] + fall_distance)

        # Blit (draw) the subsurface (the selected coin) onto the display surface at a calculated position
        state.DISPLAY.blit(sprite, coin_image_position)







