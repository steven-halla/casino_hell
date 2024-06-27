import random
import pygame
import pytmx
from typing import Optional

from constants import BLUEBLACK


class BattleScreen:
    def __init__(self, screenName: str, map_path: str = None):
        self.screenName: str = screenName
        self.startedAt: int = pygame.time.get_ticks()
        self.tiled_map: Optional[pytmx.TiledMap] = None
        self.font = pygame.font.Font(None, 36)
        self.bet = 0
        self.money = 0
        if map_path:
            self.load_map(map_path)

    def load_map(self, map_path: str) -> None:
        """Loads the tile map for the screen."""
        self.tiled_map = pytmx.load_pygame(map_path)

    def draw_tiles(self, state: 'GameState') -> None:
        """Draws the background and collision layers if a tile map is loaded."""
        if not self.tiled_map:
            return

        for layer in self.tiled_map.visible_layers:
            self.draw_layer(state, layer)

    def draw_layer(self, state: 'GameState', layer) -> None:
        """Helper function to draw a specific layer of the tile map."""
        tile_width = self.tiled_map.tilewidth
        tile_height = self.tiled_map.tileheight
        for x, y, image in layer.tiles():
            if image:  # Only draw if there's an image for this tile
                pos_x = x * tile_width + state.camera.x
                pos_y = y * tile_height + state.camera.y
                scaled_image = pygame.transform.scale(image, (int(tile_width * 1.3), int(tile_height * 1.3)))
                state.DISPLAY.blit(scaled_image, (pos_x, pos_y))

    def draw_hud(self, state: 'GameState') -> None:
        """Draws the HUD for the battle screen."""
        # background
        state.DISPLAY.fill((0, 0, 51))



        # this is for black box this is just helper code should not stay here forever






        # this box is for hero money, bet amount, and other info
        black_box = pygame.Surface((200 - 10, 180 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 235))
        # holds hero name
        black_box = pygame.Surface((200 - 10, 45 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 45 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 195))

        state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True, (255, 255, 255)), (37, 250))
        state.DISPLAY.blit(self.font.render(f"HP: {state.player.stamina_points}", True, (255, 255, 255)), (37, 290))
        state.DISPLAY.blit(self.font.render(f"MP: {state.player.focus_points}", True, (255, 255, 255)), (37, 330))
        state.DISPLAY.blit(self.font.render(f"Hero", True, (255, 255, 255)), (37, 205))
        # holds enemy name
        black_box = pygame.Surface((200 - 10, 110 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 110 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 20))

        state.DISPLAY.blit(self.font.render("Enemy", True, (255, 255, 255)), (37, 33))
        # holds enemy status, money, and other info
        black_box = pygame.Surface((200 - 10, 130 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 130 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 60))

        state.DISPLAY.blit(self.font.render(f"Money: {self.money}", True, (255, 255, 255)), (37, 70))
        state.DISPLAY.blit(self.font.render(f"Status: ", True, (255, 255, 255)), (37, 110))

        state.DISPLAY.blit(self.font.render(f"Bet: {self.bet}", True, (255, 255, 255)), (37, 370))

        black_box_height = 130
        black_box_width = 700
        border_width = 5  # Width of the white border

        # Create the black box
        black_box = pygame.Surface((black_box_width, black_box_height))
        black_box.fill((0, 0, 0))  # Fill the box with black color

        # Create a white border
        white_border = pygame.Surface((black_box_width + 2 * border_width, black_box_height + 2 * border_width))
        white_border.fill((255, 255, 255))  # Fill the border with white color
        white_border.blit(black_box, (border_width, border_width))

        # Determine the position of the white-bordered box
        screen_width, screen_height = state.DISPLAY.get_size()
        black_box_x = (screen_width - black_box_width) // 2 - border_width
        black_box_y = screen_height - black_box_height - 20 - border_width  # Subtract 20 pixels and adjust for border

        # Blit the white-bordered box onto the display
        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

        pygame.display.flip()

    def start(self, state: 'GameState') -> None:
        pygame.display.set_caption(self.screenName)

    def update(self, state: 'GameState') -> None:
        pass

    def draw(self, state: 'GameState') -> None:
        state.DISPLAY.fill(BLUEBLACK)
        self.draw_tiles(state)
        self.draw_hud(state)

    def draw_black_box(self, state: 'GameState') -> None:
        """Draws a black box in the middle of the screen."""
        print("draw the blcak box")


