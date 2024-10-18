import pygame

from entity.gui.screen.gamble_screen import GambleScreen


class CoinFlipDexterScreen(GambleScreen):
    def __init__(self, screenName: str = "Coin FLip") -> None:
        super().__init__(screenName)
        self.bet = 100
        self.sprite_sheet = pygame.image.load("./assets/images/coin_flipping_alpha.png").convert_alpha()
        self.game_state = self.WELCOME_SCREEN

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







