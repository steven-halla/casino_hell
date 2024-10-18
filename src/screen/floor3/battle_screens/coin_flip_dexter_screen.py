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
        # Fixed starting position for the coin
        initial_coin_image_position = (300, 100)  # Initial starting position for the coin

        # List of predefined x-positions for each coin in the sprite sheet
        x_positions = [85, 235, 380, 525, 670, 815, 960, 1108, 1250, 1394]
        y_position = 110  # Fixed y-coordinate for all coins in the sprite sheet
        width, height = 170, 190  # Size of each coin in the sprite sheet

        # Adjustable fall height for the y-axis
        fall_height = 222

        # Determine which coin to display based on time
        time_interval = 50  # Time interval in milliseconds (spinning speed)
        current_time = pygame.time.get_ticks()
        current_coin_index = (current_time // time_interval) % len(x_positions)

        # Define the rectangle for the current coin in the sprite sheet
        subsurface_rect = pygame.Rect(x_positions[current_coin_index], y_position, width, height)

        # Get the subsurface from the sprite sheet
        sprite = self.sprite_sheet.subsurface(subsurface_rect)

        # Calculate the falling distance based on time
        fall_distance = min(fall_height, (current_time // time_interval) % (fall_height + 1))

        # Update the y position as the coin falls down
        coin_image_position = (initial_coin_image_position[0], initial_coin_image_position[1] + fall_distance)

        # Blit (draw) the subsurface (the selected coin) onto the display surface at the updated position
        state.DISPLAY.blit(sprite, coin_image_position)







