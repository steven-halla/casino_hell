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
        coin_image_position = (122, 100)  # The position on the screen where the coin will always be shown

        # Parameters for the subsurface
        initial_x_position = 70  # Starting x-coordinate of the first coin in the sprite sheet
        initial_x_position = 230  # Starting x-coordinate of the second coin in the sprite sheet

        initial_x_position = 380  # Starting x-coordinate of the third coin in the sprite sheet
        initial_x_position = 520  # Starting x-coordinate of the third coin in the sprite sheet
        initial_x_position = 670  # Starting x-coordinate of the third coin in the sprite sheet
        initial_x_position = 815  # Starting x-coordinate of the third coin in the sprite sheet
        initial_x_position = 960  # Starting x-coordinate of the third coin in the sprite sheet
        initial_x_position = 1110  # Starting x-coordinate of the third coin in the sprite sheet
        initial_x_position = 1250  # Starting x-coordinate of the third coin in the sprite sheet
        initial_x_position = 1400  # Starting x-coordinate of the third coin in the sprite sheet
        initial_x_position = 1550  # Starting x-coordinate of the third coin in the sprite sheet

        y_position = 110  # Fixed y-coordinate for all coins in the sprite sheet
        width, height = 170, 190  # Size of each coin in the sprite sheet

        # Define the rectangle for the third coin in the sprite sheet
        subsurface_rect = pygame.Rect(initial_x_position, y_position, width, height)

        # Get the subsurface from the sprite sheet
        sprite = self.sprite_sheet.subsurface(subsurface_rect)

        # Blit (draw) the subsurface (the third coin) onto the display surface at a fixed position
        state.DISPLAY.blit(sprite, coin_image_position)

    # def draw_coin_image(self, state: 'GameState'):
    #     # Fixed position to draw the coin on the screen
    #     coin_image_position = (122, 100)  # The position on the screen where the coin will always be shown
    #
    #     # Parameters for the subsurface
    #     initial_x_position = 230  # Starting x-coordinate of the second coin in the sprite sheet
    #     y_position = 110  # Fixed y-coordinate for all coins in the sprite sheet
    #     width, height = 170, 190  # Size of each coin in the sprite sheet
    #
    #     # Define the rectangle for the second coin in the sprite sheet
    #     subsurface_rect = pygame.Rect(initial_x_position, y_position, width, height)
    #
    #     # Get the subsurface from the sprite sheet
    #     sprite = self.sprite_sheet.subsurface(subsurface_rect)
    #
    #     # Blit (draw) the subsurface (the second coin) onto the display surface at a fixed position
    #     state.DISPLAY.blit(sprite, coin_image_position)

    # def draw_coin_image(self, state: 'GameState'):
    #     # Fixed position to draw the coin on the screen
    #     coin_image_position = (122, 100)  # The position on the screen where the coin will always be shown
    #
    #     # Parameters for the subsurface
    #     initial_x_position = 70  # Starting x-coordinate of the first coin in the sprite sheet
    #     y_position = 110  # Fixed y-coordinate for all coins in the sprite sheet
    #     width, height = 170, 190  # Size of each coin in the sprite sheet
    #
    #     # Define the rectangle for the first coin in the sprite sheet
    #     subsurface_rect = pygame.Rect(initial_x_position, y_position, width, height)
    #
    #     # Get the subsurface from the sprite sheet
    #     sprite = self.sprite_sheet.subsurface(subsurface_rect)
    #
    #     # Blit (draw) the subsurface (the first coin) onto the display surface at a fixed position
    #     state.DISPLAY.blit(sprite, coin_image_position)





