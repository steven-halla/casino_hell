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
        # Initial starting positions
        initial_x_position = 80
        y_position = 100
        width, height = 170, 190
        x_offset = 170  # Adjust how far apart each coin should be displayed
        row_offset = 200  # Vertical space between the two rows

        # Loop to draw 10 images
        for i in range(10):
            # Determine which row and column to place the coin in
            if i < 5:
                # First row
                coin_image_position = (i * x_offset, y_position)
            else:
                # Second row (5 coins below the first row)
                coin_image_position = ((i - 5) * x_offset, y_position + row_offset)

            # Define the rectangle for the current image
            subsurface_rect = pygame.Rect(initial_x_position + (i * width), y_position, width, height)

            # Get the subsurface from the sprite sheet
            sprite = self.sprite_sheet.subsurface(subsurface_rect)

            # Blit (draw) the subsurface on the display surface
            state.DISPLAY.blit(sprite, coin_image_position)



