from typing import Optional

import pygame
import pytmx

from constants import BLUEBLACK


class Screen:
    def __init__(self, screenName: str, map_path: str = None):
        self.screenName: str = screenName
        self.startedAt: int = pygame.time.get_ticks()
        self.tiled_map: Optional[pytmx.TiledMap] = None
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

    def start(self, state: 'GameState') -> None:
        pygame.display.set_caption(self.screenName)

    def update(self, state: 'GameState') -> None:
        pass

    def draw(self, state: 'GameState') -> None:
        state.DISPLAY.fill(BLUEBLACK)
        self.draw_tiles(state)

    def draw_player_box(self, state: 'GameState') -> None:
        state.DISPLAY.fill((BLUEBLACK))
        black_box = pygame.Surface((190, 170))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 235))

        black_box = pygame.Surface((200 - 10, 45 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 45 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 195))

    def draw_enemy_box(self, state: 'GameState') -> None:
        black_box = pygame.Surface((190, 100))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 110 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 20))

        black_box = pygame.Surface((200 - 10, 130 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 130 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 60))




